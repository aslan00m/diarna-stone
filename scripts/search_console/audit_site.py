#!/usr/bin/env python3
"""
Search Console Audit Orchestrator for dyarnaa.com
===================================================

Ties together all search_console submodules into a single workflow:

  1. Fetch and validate the live sitemap (XML well-formedness, URL count)
  2. Check HTTP status, canonical, and robots meta for every sitemap URL
  3. If GSC credentials available:
     a. Verify site property via Sites API
     b. Check sitemap registration status via Sitemaps API
     c. Run URL Inspection on top-N priority URLs
     d. Query Search Analytics for performance data
  4. Save timestamped JSON report + latest.json
  5. Compare with previous run and detect regressions

Usage:
    python3 -m search_console.audit_site            # Full audit, all local checks
    python3 -m search_console.audit_site --summary    # Summary output only
    python3 -m search_console.audit_site --inspect 20   # GSC URL Inspection on top 20
    python3 -m search_console.audit_site --submit    # Submit sitemap to GSC (if creds)
    python3 -m search_console.audit_site --analytics  # Fetch Search Analytics data

No paid services. No Google Indexing API for regular pages.
The script works fully without Google API credentials (local checks only).
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

# Import sibling modules (works whether called as module or directly)
if __package__:
    from .auth import load_config, gsc_available, get_gsc_service
    from .sites_api import verify_site_access
    from .inspect_urls import inspect_batch, classify_inspection_result
    from .sitemap_manager import get_sitemap_status, list_sitemaps, submit_sitemap
    from .search_analytics import query_analytics, query_top_pages, compare_periods
    from .report import build_report, save_report
else:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from auth import load_config, gsc_available, get_gsc_service
    from sites_api import verify_site_access
    from inspect_urls import inspect_batch, classify_inspection_result
    from sitemap_manager import get_sitemap_status, list_sitemaps, submit_sitemap
    from search_analytics import query_analytics, query_top_pages, compare_periods
    from report import build_report, save_report

USER_AGENT = "DiarnaGSCAudit/1.0 (+https://dyarnaa.com)"
HEADERS = {"User-Agent": USER_AGENT}
REQUEST_TIMEOUT = 20


def fetch_sitemap(sitemap_url):
    """Fetch sitemap XML and extract all URLs."""
    resp = requests.get(sitemap_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    urls = re.findall(r"<loc>\s*(https?://[^<\s]+)\s*</loc>", resp.text)
    return urls, resp.text


def validate_sitemap_xml(xml_text):
    """Validate XML well-formedness."""
    import xml.etree.ElementTree as ET
    try:
        ET.fromstring(xml_text)
        return None
    except ET.ParseError as e:
        return str(e)


def check_sitemap_consistency(urls):
    """Check URL format consistency (protocol, www, trailing slash)."""
    issues = []
    for u in urls:
        parsed = urlparse(u)
        if parsed.scheme != "https":
            issues.append(f"Non-HTTPS URL: {u}")
        if "www." in parsed.netloc:
            issues.append(f"WWW URL (should be non-www): {u}")
        path = parsed.path
        if path != "/" and not path.endswith("/"):
            issues.append(f"URL without trailing slash: {u}")

    # Check for duplicates
    from collections import Counter
    url_counts = Counter(urls)
    for u, count in url_counts.items():
        if count > 1:
            issues.append(f"Duplicate URL in sitemap ({count}x): {u}")

    if issues:
        return False, issues
    return True, []


def check_url(url, site_url):
    """Check a single URL: HTTP status, canonical, robots meta, redirect chain."""
    result = {
        "url": url,
        "http_status": None,
        "final_url": url,
        "canonical": None,
        "robots_meta": None,
        "redirect_chain": [],
        "issues": [],
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        result["http_status"] = resp.status_code
        result["final_url"] = resp.url

        if len(resp.history) > 0:
            for h in resp.history:
                result["redirect_chain"].append({"status": h.status_code, "url": h.url})

        # Canonical
        canon_match = re.search(
            r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']',
            resp.text, re.IGNORECASE
        )
        if canon_match:
            result["canonical"] = canon_match.group(1).strip()

        # Robots meta
        robots_match = re.search(
            r'<meta[^>]*name=["\']robots["\'][^>]*content=["\']([^"\']*)["\']',
            resp.text, re.IGNORECASE
        )
        if robots_match:
            result["robots_meta"] = robots_match.group(1).strip().lower()

        # Issue detection
        if resp.status_code == 404:
            result["issues"].append("404 Not Found")
        elif resp.status_code >= 500:
            result["issues"].append(f"HTTP {resp.status_code} server error")
        elif resp.status_code >= 400:
            result["issues"].append(f"HTTP {resp.status_code}")

        # Canonical redirect conflict
        if result["canonical"] and result["canonical"] != url:
            canon_path = urlparse(result["canonical"]).path
            url_path = urlparse(url).path
            is_stone_to_product = (
                url.startswith(f"{site_url}stones/")
                and result["canonical"].startswith(f"{site_url}products/")
            )
            if not is_stone_to_product:
                if canon_path.rstrip("/") != url_path.rstrip("/"):
                    result["issues"].append(
                        f"Canonical mismatch: page={url_path} canonical={canon_path}"
                    )

        # noindex on sitemap URL
        if result["robots_meta"] and "noindex" in result["robots_meta"]:
            result["issues"].append(f"noindex on sitemap URL")

    except requests.exceptions.RequestException as e:
        result["issues"].append(f"Request failed: {e}")
        result["http_status"] = "ERROR"

    return result


def priority_sort(url, site_url):
    """Sort URLs by importance for prioritized checking."""
    path = url.replace(site_url, "").rstrip("/")
    if not path or path == "/":
        return 0
    if path.startswith("/products/"):
        return 1
    if path.startswith("/works/"):
        return 2
    if path.startswith("/blog/"):
        return 3
    if path.startswith("/services"):
        return 4
    if path.startswith("/about"):
        return 5
    if path.startswith("/origins/"):
        return 6
    if path.startswith("/sinks-gallery/"):
        return 7
    if path.startswith("/stones/"):
        return 8
    return 9


def audit_site(max_urls=None, summary=False, inspect=0, submit=False, analytics=False):
    """Run the full audit workflow."""
    config = load_config()
    site_url = config["site_url"]
    sitemap_url = config["sitemap_url"]

    print(f"Audit target: {site_url}")
    print(f"Sitemap: {sitemap_url}")
    print(f"GSC available: {gsc_available()}")
    print()

    # Step 1: Fetch and validate sitemap
    print("Step 1: Fetching sitemap...")
    try:
        urls, raw_xml = fetch_sitemap(sitemap_url)
    except Exception as e:
        print(f"FATAL: Could not fetch sitemap: {e}")
        sys.exit(1)

    print(f"  Found {len(urls)} URLs in sitemap")

    # Validate XML
    xml_error = validate_sitemap_xml(raw_xml)
    if xml_error:
        print(f"  ⚠ XML parse error: {xml_error}")
    else:
        print(f"  ✓ XML is well-formed")

    # Check consistency (trailing slash, duplicates, protocol)
    consistent, sitemap_issues = check_sitemap_consistency(urls)
    if sitemap_issues:
        print(f"  ⚠ {len(sitemap_issues)} sitemap issues:")
        for issue in sitemap_issues[:10]:
            print(f"    - {issue}")
    else:
        print(f"  ✓ Sitemap is consistent (no duplicates, trailing slashes correct)")

    if max_urls:
        urls = urls[:max_urls]
        print(f"  (Limited to first {max_urls} URLs for this run)")

    # Step 2: Check each URL
    sorted_urls = sorted(urls, key=lambda u: priority_sort(u, site_url))
    print(f"\nStep 2: Checking {len(sorted_urls)} URLs...")
    url_checks = []
    for i, u in enumerate(sorted_urls):
        if not summary:
            short = u.replace(site_url, "")
            print(f"  [{i+1}/{len(sorted_urls)}] {short:50s}", end="", flush=True)
        result = check_url(u, site_url)
        url_checks.append(result)
        if not summary:
            status = result["http_status"]
            n = len(result["issues"])
            print(f" {status}" + (f" ⚠ {n} issues" if n else " ✓"))

    # Step 3: GSC integration
    gsc_result = {"available": gsc_available()}
    if gsc_available():
        print("\nStep 3: Google Search Console API integration...")

        # 3a: Verify site access
        service, err = get_gsc_service(config)
        if service:
            print("  Checking site property access...")
            site_check = verify_site_access(service, site_url)
            gsc_result["site_verification"] = {
                "has_access": site_check.get("has_access", False),
                "matching_site": site_check.get("matching_site"),
                "all_sites": [s["identifier"] for s in site_check.get("all_sites", [])],
            }
            if site_check.get("has_access"):
                print(f"    ✓ Property accessible: {site_check.get('matching_site', {}).get('identifier', 'N/A')}")
            else:
                print(f"    ✗ Property not found. Available sites: {[s['identifier'] for s in site_check.get('all_sites', [])]}")

            # 3b: Sitemap status
            print("  Checking sitemap registration in GSC...")
            sitemap_status = get_sitemap_status(service, site_url, sitemap_url)
            gsc_result["sitemap_status"] = sitemap_status
            if sitemap_status.get("ok"):
                print(f"    ✓ Sitemap registered. Status: {sitemap_status.get('status', 'unknown')}")
            else:
                print(f"    ✗ Sitemap status: {sitemap_status.get('error', 'unknown')}")

            # 3c: Submit sitemap if requested
            if submit:
                print("  Submitting sitemap to GSC...")
                submit_result = submit_sitemap(service, site_url, sitemap_url)
                gsc_result["submit_result"] = submit_result
                print(f"    Status: {submit_result.get('status', 'unknown')}")

            # 3d: URL Inspection
            if inspect > 0:
                print(f"\n  Running URL Inspection on top {inspect} URLs...")
                top_urls = [r["url"] for r in url_checks[:inspect]]
                inspection_results = inspect_batch(service, top_urls, site_url)
                gsc_result["inspections"] = inspection_results
                # Classify
                classifications = {}
                for r in inspection_results:
                    cls = classify_inspection_result(r)
                    classifications[r["url"]] = cls
                gsc_result["classifications"] = classifications

                # Summary
                from collections import Counter
                cls_counts = Counter(classifications.values())
                print(f"    Classification summary:")
                for cls, count in cls_counts.items():
                    print(f"      {cls}: {count}")

            # 3e: Search Analytics
            if analytics:
                print("\n  Querying Search Analytics...")
                analytics_result = query_top_pages(service, site_url, days=28, row_limit=50)
                gsc_result["analytics"] = analytics_result
                if analytics_result.get("ok"):
                    totals = analytics_result.get("totals", {})
                    print(f"    Clicks: {totals.get('clicks', '?')}, Impressions: {totals.get('impressions', '?')}")
                    print(f"    CTR: {totals.get('ctr', '?')}%, Avg Position: {totals.get('avg_position', '?')}")
                else:
                    print(f"    Analytics error: {analytics_result.get('error', 'unknown')}")
        else:
            gsc_result["error"] = err
            print(f"  Error building GSC service: {err}")
    else:
        gsc_result["note"] = (
            "Google Search Console API not configured. "
            "To enable: create a service account with Search Console API access "
            "and set GSC_SERVICE_ACCOUNT env var or place credentials at the expected path. "
            "See SETUP_GSC.md for instructions."
        )
        print("\n  (GSC API not available — local checks only)")

    # Step 4: Build report
    print("\n" + "=" * 50)
    total_issues = sum(len(r["issues"]) for r in url_checks)
    count_404 = sum(1 for r in url_checks if r["http_status"] == 404)
    count_200 = sum(1 for r in url_checks if r["http_status"] == 200)
    count_redirect = sum(1 for r in url_checks if r["redirect_chain"])

    report = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "site": site_url,
        "config": {k: v for k, v in config.items() if k not in ("credentials_file",)},
        "sitemap_validation": {
            "xml_valid": xml_error is None,
            "xml_error": xml_error,
            "url_count": len(urls),
            "issues": sitemap_issues,
            "consistency_ok": consistent,
        },
        "summary": {
            "total_urls": len(urls),
            "total_issues": total_issues,
            "urls_with_issues": len([r for r in url_checks if r["issues"]]),
            "status_200_count": count_200,
            "status_404_count": count_404,
            "redirects_count": count_redirect,
            "gsc_available": gsc_available(),
            "indexed_by_google": 0,
            "not_indexed_by_google": 0,
            "google_unknown": 0,
            "auth_errors": 0,
        },
        "gsc": gsc_result,
        "url_checks": url_checks,
    }

    # Count GSC classifications if available
    if "classifications" in gsc_result:
        from collections import Counter
        cls_counts = Counter(gsc_result["classifications"].values())
        report["summary"]["indexed_by_google"] = cls_counts.get("indexed", 0)
        report["summary"]["not_indexed_by_google"] = cls_counts.get("not-indexed", 0)
        report["summary"]["google_unknown"] = cls_counts.get("unknown", 0) + cls_counts.get("inspection-error", 0)
        report["summary"]["auth_errors"] = cls_counts.get("auth-error", 0) + cls_counts.get("api-quota-error", 0)

    # Compare with previous report
    prev_report = None
    report_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                              "reports", "indexing")
    prev_path = os.path.join(report_dir, "latest.json")
    if os.path.exists(prev_path):
        try:
            with open(prev_path, "r", encoding="utf-8") as f:
                prev_report = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    regressions = []
    if prev_report:
        prev_issues = {}
        for r in prev_report.get("url_checks", []):
            if r["issues"]:
                prev_issues[r["url"]] = set(r["issues"])
        for r in url_checks:
            curr = set(r["issues"])
            prev = prev_issues.get(r["url"], set())
            new_issues = curr - prev
            if new_issues:
                regressions.append({"url": r["url"], "new_issues": list(new_issues)})

    report["regressions"] = regressions

    # Print summary
    print(f"\nالملخص:")
    print(f"  إجمالي الروابط:       {len(urls)}")
    print(f"  200 OK:               {count_200}")
    print(f"  404:                  {count_404}")
    print(f"  مشاكل:                {total_issues}")
    print(f"  إعادة توجيه:          {count_redirect}")
    print(f"  XML صالح:             {'✓' if xml_error is None else '✗'}")
    print(f"  GSC API متاح:         {'✓' if gsc_available() else '✗'}")
    if regressions:
        print(f"  انحدارات جديدة:       {len(regressions)}")

    # Save report
    report_path = save_report(report, report_dir)
    print(f"\nالتقرير محفوظ في: {report_path['json']}")
    print("=" * 50)

    if regressions:
        print("\n🚨 انحدارات مكتشفة:")
        for reg in regressions:
            print(f"  {reg['url']}:")
            for issue in reg["new_issues"]:
                print(f"    - {issue}")

    if count_404 or regressions:
        sys.exit(1)
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Search Console Audit for dyarnaa.com")
    parser.add_argument("--summary", action="store_true", help="Print summary only (no per-URL detail)")
    parser.add_argument("--max-urls", type=int, default=None, help="Limit URLs to check")
    parser.add_argument("--inspect", type=int, default=0, help="URL Inspection on top N URLs (requires GSC)")
    parser.add_argument("--submit", action="store_true", help="Submit sitemap to GSC (requires creds)")
    parser.add_argument("--analytics", action="store_true", help="Fetch Search Analytics data (requires GSC)")
    args = parser.parse_args()

    audit_site(
        max_urls=args.max_urls,
        summary=args.summary,
        inspect=args.inspect,
        submit=args.submit,
        analytics=args.analytics,
    )


if __name__ == "__main__":
    main()
