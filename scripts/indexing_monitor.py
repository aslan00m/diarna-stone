#!/usr/bin/env python3
"""
Google Indexing Monitor for dyarnaa.com
=========================================

Free, self-contained monitor that:
  1. Fetches and validates the sitemap (XML well-formedness, URL count, trailing-slash consistency)
  2. Crawls every sitemap URL and checks HTTP status, canonical tag, and robots meta
  3. If Google Service Account credentials are found, integrates with Search Console API:
     - Submits the sitemap via Sitemaps API when URLs change
     - Runs URL Inspection on top-priority pages within API quotas
  4. Saves a timestamped JSON report
  5. Compares with the previous run and alerts on regressions (new 404s, canonical drift, etc.)

No paid services, no Google Indexing API for regular pages.
Run daily via Hermes cron (see cron instructions at the bottom of this file).

Usage:
    python3 indexing_monitor.py            # full check + report
    python3 indexing_monitor.py --summary  # print summary only
    python3 indexing_monitor.py --submit   # also submit sitemap to GSC if creds available
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests

# ── Configuration ───────────────────────────────────────────────────────────

SITE = "https://dyarnaa.com"
SITEMAP_URL = f"{SITE}/sitemap.xml"
REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "reports", "indexing")
PREV_REPORT = os.path.join(REPORT_DIR, "latest.json")
GSC_CREDENTIALS = os.environ.get("GSC_SERVICE_ACCOUNT") or os.path.join(
    os.environ.get("HERMES_HOME", "/opt/data"), "secrets", "gsc-service-account.json"
)
GSC_SITE_PROPERTY = "sc-domain:dyarnaa.com"  # Domain property (preferred)
MAX_URL_INSPECTION = 50  # cap per run to stay within GSC API quotas
REQUEST_TIMEOUT = 20
USER_AGENT = "DiarnaIndexingMonitor/1.0 (+https://dyarnaa.com)"

HEADERS = {"User-Agent": USER_AGENT}


# ── Sitemap fetching & validation ───────────────────────────────────────────

def fetch_sitemap():
    """Fetch and return list of URL strings from the live sitemap."""
    resp = requests.get(SITEMAP_URL, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    text = resp.text
    # Extract all <loc> URLs
    urls = re.findall(r"<loc>\s*(https?://[^<\s]+)\s*</loc>", text)
    return urls, text


def validate_sitemap_xml(xml_text):
    """Validate XML well-formedness and return error if any."""
    import xml.etree.ElementTree as ET
    try:
        ET.fromstring(xml_text)
        return None
    except ET.ParseError as e:
        return str(e)


def check_sitemap_consistency(urls):
    """Check all URLs use trailing slash (except root). Returns list of issues."""
    issues = []
    for u in urls:
        parsed = urlparse(u)
        path = parsed.path
        if path != "/" and not path.endswith("/"):
            issues.append(f"Sitemap URL without trailing slash: {u}")
    return issues


# ── URL-level checks ────────────────────────────────────────────────────────

def check_url(url):
    """Check a single URL: HTTP status, canonical, robots meta."""
    result = {
        "url": url,
        "http_status": None,
        "final_url": url,
        "canonical": None,
        "robots_meta": None,
        "issues": [],
        "redirect_chain": [],
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        result["http_status"] = resp.status_code
        result["final_url"] = resp.url

        # Track redirect chain
        if len(resp.history) > 0:
            for h in resp.history:
                result["redirect_chain"].append(f"{h.status_code} {h.url}")

        # Canonical
        canon_match = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', resp.text, re.IGNORECASE)
        if canon_match:
            result["canonical"] = canon_match.group(1).strip()

        # Robots meta
        robots_match = re.search(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\']([^"\']*)["\']', resp.text, re.IGNORECASE)
        if robots_match:
            result["robots_meta"] = robots_match.group(1).strip().lower()

        # Issue detection
        if resp.status_code == 404:
            result["issues"].append(f"404 Not Found")
        elif resp.status_code == 410:
            result["issues"].append("410 Gone")
        elif resp.status_code >= 500:
            result["issues"].append(f"HTTP {resp.status_code} server error")
        elif resp.status_code >= 400:
            result["issues"].append(f"HTTP {resp.status_code}")

        if result["redirect_chain"]:
            result["issues"].append(f"Redirect chain ({len(resp.history)} hop(s))")

        # Canonical mismatch: canonical should match the URL (or its trailing-slash variant).
        # Exception: /stones/ pages intentionally canonical to their /products/ twin
        # to avoid duplicate content — this is by design, not an issue.
        is_stone_canonical_to_product = (
            result["canonical"]
            and url.startswith(f"{SITE}/stones/")
            and result["canonical"].startswith(f"{SITE}/products/")
        )
        if result["canonical"] and not is_stone_canonical_to_product:
            canon_normalized = result["canonical"].rstrip("/")
            url_normalized = url.rstrip("/")
            if canon_normalized != url_normalized:
                result["issues"].append(
                    f"Canonical mismatch: sitemap={url} canonical={result['canonical']}"
                )

        # Canonical redirect conflict: canonical URL itself redirects
        if result["canonical"] and result["canonical"] != url:
            try:
                canon_resp = requests.head(result["canonical"], headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
                if canon_resp.status_code in (301, 302) and len(canon_resp.history) > 0:
                    result["issues"].append(
                        f"Canonical URL redirects ({canon_resp.status_code})"
                    )
            except Exception:
                pass

        # noindex on a sitemap URL is suspicious
        if result["robots_meta"] and "noindex" in result["robots_meta"]:
            result["issues"].append(f"noindex on sitemap URL: {result['robots_meta']}")

    except requests.exceptions.RequestException as e:
        result["issues"].append(f"Request failed: {e}")
        result["http_status"] = "ERROR"

    return result


# ── Google Search Console API integration ───────────────────────────────────
# NOTE: Only activates if GSC service account credentials are found.
# The script works fully without Google API access (local checks only).

def gsc_available():
    """Check if Google Search Console API credentials are available."""
    return os.path.exists(GSC_CREDENTIALS)


def gsc_submit_sitemap():
    """Submit sitemap to Google Search Console via Sitemaps API."""
    if not gsc_available():
        return {"status": "skipped", "reason": "No GSC service account credentials found"}

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        creds = service_account.Credentials.from_service_account_file(
            GSC_CREDENTIALS,
            scopes=["https://www.googleapis.com/auth/webmasters"],
        )
        service = build("searchconsole", "v1", credentials=creds)

        # Use raw HTTP workaround due to client library bug
        import google.auth.transport.requests
        from urllib.parse import quote
        session = google.auth.transport.requests.AuthorizedSession(creds)
        site_enc = quote(GSC_SITE_PROPERTY, safe="")
        sitemap_enc = quote(SITEMAP_URL, safe="")
        url = f"https://searchconsole.googleapis.com/webmasters/v3/sites/{site_enc}/sitemaps/{sitemap_enc}:submit"
        resp = session.post(url, timeout=30)
        if resp.status_code == 200:
            return {"status": "submitted", "response": resp.json()}
        else:
            return {"status": "error", "http_status": resp.status_code, "body": resp.text[:500]}
    except ImportError:
        return {"status": "skipped", "reason": "google-api-python-client not installed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def gsc_inspect_urls(urls):
    """Use URL Inspection API on a sample of high-priority URLs."""
    if not gsc_available():
        return {"status": "skipped", "reason": "No GSC credentials"}

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        creds = service_account.Credentials.from_service_account_file(
            GSC_CREDENTIALS,
            scopes=["https://www.googleapis.com/auth/webmasters"],
        )
        service = build("searchconsole", "v1", credentials=creds)

        results = []
        for u in urls[:MAX_URL_INSPECTION]:
            try:
                resp = service.urlInspection().index().inspect(body={
                    "inspectionUrl": u,
                    "siteUrl": GSC_SITE_PROPERTY,
                    "languageCode": "ar",
                }).execute()
                inspection = resp.get("inspectionResult", {})
                result = {
                    "url": u,
                    "verdict": inspection.get("verdict", {}),
                    "coverage_state": inspection.get("indexStatusResult", {}).get("coverageState", "unknown"),
                    "last_crawled": inspection.get("indexStatusResult", {}).get("lastCrawlTime", "unknown"),
                    "google_url": inspection.get("indexStatusResult", {}).get("googleUrl", "unknown"),
                }
                results.append(result)
            except Exception as e:
                results.append({"url": u, "error": str(e)})

        return {"status": "complete", "results": results}
    except ImportError:
        return {"status": "skipped", "reason": "google-api-python-client not installed"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ── Report management ────────────────────────────────────────────────────────

def save_report(report):
    """Save report as timestamped file and as latest.json."""
    os.makedirs(REPORT_DIR, exist_ok=True)
    timestamp = report["timestamp"]
    ts_file = os.path.join(REPORT_DIR, f"report-{timestamp}.json")
    with open(ts_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(PREV_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return ts_file


def detect_regressions(prev_report, curr_report):
    """Compare current check results with previous run. Returns list of new regressions."""
    if prev_report is None:
        return []  # first run, no baseline

    prev_issues = {}
    for r in prev_report.get("url_checks", []):
        if r["issues"]:
            prev_issues[r["url"]] = set(r["issues"])

    regressions = []
    for r in curr_report.get("url_checks", []):
        curr_issue_set = set(r["issues"])
        prev_issue_set = prev_issues.get(r["url"], set())
        new_issues = curr_issue_set - prev_issue_set
        if new_issues:
            regressions.append({
                "url": r["url"],
                "new_issues": list(new_issues),
            })
    return regressions


def send_alert(regressions, summary):
    """Log-alert: print to stdout for cron capture. Could be extended for email/TG."""
    if not regressions:
        return
    print("\n" + "=" * 60)
    print("🚨 INDEXING REGRESSIONS DETECTED")
    print("=" * 60)
    for r in regressions:
        print(f"\nURL: {r['url']}")
        for issue in r["new_issues"]:
            print(f"  - {issue}")
    print(f"\nTotal: {len(regressions)} URLs with new issues")
    print("=" * 60)


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Google Indexing Monitor for dyarnaa.com")
    parser.add_argument("--summary", action="store_true", help="Print summary only")
    parser.add_argument("--submit", action="store_true", help="Submit sitemap to GSC (if creds available)")
    parser.add_argument("--inspect", type=int, default=0, help="URL Inspection API on top N URLs")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%dT%H%M%SZ")

    # Load previous report (if any) for regression comparison
    prev_report = None
    if os.path.exists(PREV_REPORT):
        try:
            with open(PREV_REPORT, "r", encoding="utf-8") as f:
                prev_report = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    # Step 1: Fetch and validate sitemap
    print(f"Fetching sitemap from {SITEMAP_URL}...")
    try:
        urls, raw_xml = fetch_sitemap()
    except Exception as e:
        print(f"FATAL: Could not fetch sitemap: {e}")
        sys.exit(1)

    print(f"Found {len(urls)} URLs in sitemap")

    # Validate XML
    xml_error = validate_sitemap_xml(raw_xml)
    sitemap_issues = []
    if xml_error:
        sitemap_issues.append(f"XML parse error: {xml_error}")

    # Check trailing slash consistency
    sitemap_issues.extend(check_sitemap_consistency(urls))

    # Step 2: Check each URL (prioritize important pages first)
    # Order: root, products, services, about, works, blog, origins, sinks-gallery, stones
    def priority_sort(u):
        path = urlparse(u).path.rstrip("/")
        if path == "" or path == "/": return 0
        if path.startswith("/products/"): return 1
        if path in ("/services", "/about", "/contact"): return 2
        if path.startswith("/works"): return 3
        if path.startswith("/blog"): return 4
        if path.startswith("/origins"): return 5
        if path.startswith("/sinks-gallery"): return 6
        if path.startswith("/stones"): return 7
        return 8

    sorted_urls = sorted(urls, key=priority_sort)

    print(f"Checking {len(sorted_urls)} URLs...")
    url_checks = []
    for i, u in enumerate(sorted_urls):
        if not args.summary:
            print(f"  [{i+1}/{len(sorted_urls)}] {u.replace('https://dyarnaa.com', '')} ...", end="", flush=True)
        result = check_url(u)
        url_checks.append(result)
        if not args.summary:
            status = result["http_status"]
            n_issues = len(result["issues"])
            print(f" {status}" + (f" ⚠ {n_issues} issues" if n_issues else " ✓"))

    # Step 3: GSC integration (optional)
    gsc_status: dict = {"available": gsc_available()}
    if gsc_available():
        gsc_status["credentials"] = GSC_CREDENTIALS
        if args.submit:
            print("\nSubmitting sitemap to Google Search Console...")
            gsc_status["submit_result"] = gsc_submit_sitemap()

        if args.inspect > 0:
            print(f"\nRunning URL Inspection on top {args.inspect} URLs...")
            top_urls = [r["url"] for r in url_checks[:args.inspect]]
            gsc_status["inspection"] = gsc_inspect_urls(top_urls)
    else:
        gsc_status["note"] = (
            "Google Search Console API not configured. "
            "To enable: create a service account with Search Console API access "
            "and set GSC_SERVICE_ACCOUNT env var or place credentials at the expected path. "
            "See SETUP_GSC.md for manual verification steps."
        )

    # Step 4: Build report
    total_issues = sum(len(r["issues"]) for r in url_checks)
    status_404 = [r for r in url_checks if r["http_status"] == 404]
    status_errors = [r for r in url_checks if r["http_status"] not in (200, 301) and r["http_status"] != 200]

    summary = {
        "total_urls": len(urls),
        "total_issues": total_issues,
        "urls_with_issues": len([r for r in url_checks if r["issues"]]),
        "status_404_count": len(status_404),
        "sitemap_xml_valid": xml_error is None,
        "sitemap_consistency_ok": len(sitemap_issues) == 0,
    }

    report = {
        "timestamp": timestamp,
        "site": SITE,
        "sitemap_url": SITEMAP_URL,
        "sitemap_validation": {
            "xml_valid": xml_error is None,
            "xml_error": xml_error,
            "url_count": len(urls),
            "issues": sitemap_issues,
        },
        "summary": summary,
        "gsc": gsc_status,
        "url_checks": url_checks,
    }

    # Step 5: Detect regressions
    regressions = detect_regressions(prev_report, report)
    report["regressions"] = regressions
    if regressions:
        send_alert(regressions, summary)

    # Step 6: Save report
    report_file = save_report(report)

    # Print final summary
    print("\n" + "=" * 50)
    print(f"Indexing Monitor Report — {timestamp}")
    print("=" * 50)
    print(f"Total URLs in sitemap:    {len(urls)}")
    print(f"URLs with issues:         {summary['urls_with_issues']}")
    print(f"404 errors:               {len(status_404)}")
    print(f"Sitemap XML valid:        {summary['sitemap_xml_valid']}")
    print(f"Sitemap consistency OK:   {summary['sitemap_consistency_ok']}")
    print(f"GSC API available:        {gsc_status['available']}")
    print(f"Regressions (vs prev):    {len(regressions)}")
    print(f"Report saved:             {report_file}")
    if "submit_result" in gsc_status:
        sr = gsc_status["submit_result"]
        print(f"GSC submit:               {sr.get('status', 'N/A')}")
    print("=" * 50)

    # Exit code: 0 if no 404s and no new regressions, 1 otherwise
    if status_404 or regressions:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
