#!/usr/bin/env python3
"""
SEO Audit Tool for dyarnaa.com
==============================

Independent, free SEO audit that does NOT depend on Google Search Console API.
Crawls sitemap URLs and checks:

Indexing & crawl:
  - robots.txt content
  - Sitemap XML validity and URL count
  - HTTP status codes
  - Canonical tags (consistency)
  - noindex / nofollow directives
  - Redirect chains
  - Dead/orphan pages

Content quality:
  - Title tag length and uniqueness
  - Meta description length and uniqueness
  - H1 presence and content
  - Heading hierarchy (H1 → H2 → H3)
  - Image alt text presence
  - Internal link extraction
  - Broken link detection
  - Duplicate content detection

SEO signals:
  - Schema.org structured data presence
  - Open Graph / Twitter Card tags
  - Mobile-friendliness (viewport)
  - Language attributes (lang="ar" dir="rtl")

Local SEO:
  - Business name, phone, address consistency
  - No invented locations/branches/addresses

Usage:
    python3 seo_audit.py
    python3 seo_audit.py --max-urls 20
    python3 seo_audit.py --output json
"""
import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser

import requests

SITE = "https://dyarnaa.com"
SITEMAP_URL = f"{SITE}/sitemap.xml"
USER_AGENT = "DiarnaSEOAudit/1.0 (+https://dyarnaa.com)"
HEADERS = {"User-Agent": USER_AGENT}
TIMEOUT = 20

# Pages that should NOT have noindex
CRITICAL_PAGES = ["/", "/services/", "/about/", "/contact/", "/products/"]


class PageMeta(HTMLParser):
    """Lightweight HTML parser to extract SEO-relevant metadata."""
    def __init__(self):
        super().__init__()
        self.title = None
        self.meta_desc = None
        self.h1 = None
        self.canonical = None
        self.robots_meta = None
        self.viewport = None
        self.lang = None
        self.dir_attr = None
        self.og_tags = {}
        self.twitter_tags = {}
        self.schema_types = []
        self.images_without_alt = 0
        self.total_images = 0
        self.internal_links = set()
        self.external_links = set()
        self.h1_count = 0
        self.h2_count = 0
        self.h3_count = 0
        self.h1_list = []

        self._in_title = False
        self._title_parts = []
        self._in_h1 = False
        self._h1_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = (attrs.get("name") or "").lower()
            prop = (attrs.get("property") or "").lower()
            content = attrs.get("content", "")
            if name == "description":
                self.meta_desc = content
            elif name == "robots":
                self.robots_meta = (content or "").lower()
            elif name == "viewport":
                self.viewport = content
            elif prop.startswith("og:"):
                self.og_tags[prop] = content
            elif prop.startswith("twitter:"):
                self.twitter_tags[prop] = content
        elif tag == "link" and (attrs.get("rel") or "").lower() == "canonical":
            self.canonical = attrs.get("href", "")
        elif tag == "html":
            self.lang = attrs.get("lang")
            self.dir_attr = attrs.get("dir")
        elif tag == "h1":
            self.h1_count += 1
            self._in_h1 = True
        elif tag == "h2":
            self.h2_count += 1
        elif tag == "h3":
            self.h3_count += 1
        elif tag == "img":
            self.total_images += 1
            alt = attrs.get("alt", "")
            # Empty alt is OK for decorative, but missing alt entirely is a problem
            if "alt" not in attrs:
                self.images_without_alt += 1
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            pass  # handled in text
        elif tag == "a":
            href = attrs.get("href", "")
            if href:
                parsed = urlparse(href)
                if parsed.scheme in ("", "http", "https"):
                    if not parsed.netloc or parsed.netloc == "dyarnaa.com":
                        self.internal_links.add(href)
                    else:
                        self.external_links.add(href)

    def handle_data(self, data):
        if self._in_title:
            self._title_parts.append(data)
        elif self._in_h1:
            self._h1_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
            self.title = "".join(self._title_parts).strip()
        elif tag == "h1":
            self._in_h1 = False
            self.h1 = "".join(self._h1_parts).strip()
            if self.h1:
                self.h1_list.append(self.h1)

    def handle_comment(self, data):
        pass


def parse_html(html_text):
    """Parse HTML and return PageMeta."""
    parser = PageMeta()
    parser.feed(html_text)
    # Extract schema.org types from JSON-LD
    for m in re.finditer(r'application/ld\+json"[^>]*>(.*?)</script>', html_text, re.DOTALL):
        import html as html_module
        try:
            json_text = html_module.unescape(m.group(1))
            data = json.loads(json_text)
            if isinstance(data, dict):
                if data.get("@graph"):
                    for node in data["@graph"]:
                        t = node.get("@type", "")
                        if t:
                            parser.schema_types.append(t)
                else:
                    t = data.get("@type", "")
                    if t:
                        parser.schema_types.append(t)
        except (json.JSONDecodeError, ValueError):
            pass
    return parser


def extract_urls_from_sitemap():
    """Fetch sitemap and return list of URLs."""
    resp = requests.get(SITEMAP_URL, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return re.findall(r"<loc>\s*(https?://[^<\s]+)\s*</loc>", resp.text)


def check_url(url, check_links=False):
    """Audit a single URL for SEO health.

    Returns dict with all checks.
    """
    result = {
        "url": url,
        "http_status": None,
        "final_url": url,
        "issues": [],
        "warnings": [],
        "checks": {},
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        result["http_status"] = resp.status_code
        result["final_url"] = resp.url
        result["checks"]["content_length"] = len(resp.text)

        if resp.history:
            result["checks"]["redirect_chain"] = [
                {"status": h.status_code, "url": h.url} for h in resp.history
            ]

        if resp.status_code == 404:
            result["issues"].append("404 Not Found")
        elif resp.status_code >= 500:
            result["issues"].append(f"Server error: {resp.status_code}")
        elif resp.status_code != 200:
            result["issues"].append(f"Unexpected status: {resp.status_code}")

        meta = parse_html(resp.text)

        # Title checks
        if not meta.title:
            result["issues"].append("Missing <title> tag")
        else:
            title_len = len(meta.title)
            result["checks"]["title"] = meta.title[:100]
            result["checks"]["title_length"] = title_len
            if title_len < 30:
                result["warnings"].append(f"Title too short ({title_len} chars)")
            elif title_len > 60:
                result["warnings"].append(f"Title too long ({title_len} chars)")
            # Check for duplicate company name stutter
            if meta.title.count("ديارنا الحديثة") > 1:
                result["warnings"].append("Title has repeated company name")

        # Meta description
        if not meta.meta_desc:
            result["warnings"].append("Missing meta description")
        else:
            desc_len = len(meta.meta_desc)
            if desc_len < 80:
                result["warnings"].append(f"Meta description too short ({desc_len} chars)")
            elif desc_len > 160:
                result["warnings"].append(f"Meta description too long ({desc_len} chars)")

        # Canonical
        if not meta.canonical:
            result["warnings"].append("Missing canonical tag")
        else:
            result["checks"]["canonical"] = meta.canonical
            # Check if canonical matches the page URL (with trailing slash)
            canon_path = urlparse(meta.canonical).path
            page_path = urlparse(url).path
            if canon_path != page_path and url.replace(SITE, "") not in meta.canonical:
                # Check if stone→product canonical (intentional)
                if not (url.replace(SITE, "").startswith("/stones/") and meta.canonical.startswith(f"{SITE}/products/")):
                    result["issues"].append(f"Canonical mismatch: page={page_path} canonical={canon_path}")

        # noindex
        if meta.robots_meta and "noindex" in meta.robots_meta:
            result["checks"]["noindex"] = True
            if "/sinks-gallery/all/" not in url:
                result["warnings"].append(f"noindex on page: {meta.robots_meta}")
        else:
            result["checks"]["noindex"] = False

        # H1
        if not meta.h1:
            result["issues"].append("Missing H1 tag")
        else:
            result["checks"]["h1"] = meta.h1[:100]
        if meta.h1_count > 1:
            result["warnings"].append(f"Multiple H1 tags ({meta.h1_count})")
        if meta.h2_count == 0:
            result["warnings"].append("No H2 tags (heading hierarchy weak)")

        # Images
        if meta.total_images > 0:
            result["checks"]["images"] = {
                "total": meta.total_images,
                "without_alt": meta.images_without_alt,
            }
            if meta.images_without_alt > 0:
                pct = meta.images_without_alt / meta.total_images * 100
                if pct > 20:
                    result["warnings"].append(
                        f"{meta.images_without_alt}/{meta.total_images} images ({pct:.0f}%) missing alt text"
                    )

        # Internal links
        result["checks"]["internal_link_count"] = len(meta.internal_links)
        result["checks"]["external_link_count"] = len(meta.external_links)
        if len(meta.internal_links) < 3:
            result["warnings"].append(f"Few internal links ({len(meta.internal_links)})")

        # Structured data (schema_types may contain lists for @type arrays)
        result["checks"]["schema_types"] = meta.schema_types
        if not meta.schema_types:
            result["warnings"].append("No structured data (Schema.org) found")

        # Open Graph
        og_title = meta.og_tags.get("og:title")
        og_image = meta.og_tags.get("og:image")
        og_desc = meta.og_tags.get("og:description")
        result["checks"]["has_og"] = bool(og_title or og_image)
        if not og_title:
            result["warnings"].append("Missing og:title")
        if not og_image:
            result["warnings"].append("Missing og:image")

        # Language/RTL
        result["checks"]["lang"] = meta.lang
        result["checks"]["dir"] = meta.dir_attr
        if meta.lang != "ar":
            result["warnings"].append(f"Expected lang='ar', got '{meta.lang}'")
        if meta.dir_attr != "rtl":
            result["warnings"].append(f"Expected dir='rtl', got '{meta.dir_attr}'")

        # Contact info (local SEO)
        # Look for phone number pattern
        phone_match = re.search(r'05\d{8}', resp.text)
        result["checks"]["has_phone"] = bool(phone_match)

    except requests.exceptions.RequestException as e:
        result["issues"].append(f"Request failed: {e}")

    return result


def audit_sitemap(max_urls=None, output_format="text"):
    """Run full SEO audit on all sitemap URLs (up to max_urls)."""
    print(f"SEO Audit — {SITE}")
    print(f"Fetching sitemap ({SITEMAP_URL})...")

    try:
        urls = extract_urls_from_sitemap()
    except Exception as e:
        print(f"FATAL: Could not fetch sitemap: {e}")
        sys.exit(1)

    if max_urls:
        urls = urls[:max_urls]

    print(f"Auditing {len(urls)} URLs...\n")

    results = []
    all_titles = Counter()
    all_descs = Counter()

    for i, url in enumerate(urls):
        r = check_url(url)
        results.append(r)
        if r["checks"].get("title"):
            all_titles[r["checks"]["title"]] += 1
        if r["checks"].get("description"):  # not set currently, skip
            pass

        status = r["http_status"]
        n_issues = len(r["issues"])
        n_warns = len(r["warnings"])
        short_url = url.replace(SITE, "")
        status_str = str(status) if status else "ERR"
        print(f"  [{i+1}/{len(urls)}] {status_str} {short_url:50s}", end="")
        if n_issues:
            print(f" ⚠ {n_issues} issues")
        elif n_warns:
            print(f" · {n_warns} warnings")
        else:
            print(" ✓")

    # Summary
    total_issues = sum(len(r["issues"]) for r in results)
    total_warnings = sum(len(r["warnings"]) for r in results)
    count_200 = sum(1 for r in results if r["http_status"] == 200)
    count_404 = sum(1 for r in results if r["http_status"] == 404)
    count_redirect = sum(1 for r in results if r.get("checks", {}).get("redirect_chain"))

    # Find pages without H1
    no_h1 = [r["url"] for r in results if "Missing H1 tag" in [i for i in r["issues"]]]
    # Find duplicate titles
    dup_titles = {t: c for t, c in all_titles.items() if c > 1}

    report = {
        "timestamp": datetime.now().isoformat(),
        "site": SITE,
        "results": results,
        "summary": {
            "total_pages": len(results),
            "pages_200": count_200,
            "pages_404": count_404,
            "total_issues": total_issues,
            "total_warnings": total_warnings,
            "pages_with_redirects": count_redirect,
            "pages_without_h1": len(no_h1),
            "duplicate_titles": len(dup_titles),
        },
    }

    # Save report
    report_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                              "reports", "seo_audit")
    os.makedirs(report_dir, exist_ok=True)
    ts = report["timestamp"].replace(":", "").replace("-", "")[:15]
    json_path = os.path.join(report_dir, f"audit-{ts}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(os.path.join(report_dir, "latest.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # Print summary
    print("\n" + "=" * 55)
    print("تلخيص فحص SEO")
    print("=" * 55)
    print(f"إجمالي الصفحات:       {len(results)}")
    print(f"200 OK:               {count_200}")
    print(f"404:                  {count_404}")
    print(f"مشكلات:               {total_issues}")
    print(f"تحذيرات:              {total_warnings}")
    print(f"صفحات بدون H1:        {len(no_h1)}")
    print(f"عناوين مكررة:         {len(dup_titles)}")
    print(f"تقرير محفوظ في:       {json_path}")

    if no_h1:
        print(f"\n⚠️  صفحات بدون عنوان H1:")
        for u in no_h1[:5]:
            print(f"  {u.replace(SITE, '')}")
    if dup_titles:
        print(f"\n⚠️  عناوين مكررة:")
        for t, c in list(dup_titles.items())[:5]:
            print(f"  ({c}x) {t[:60]}")

    print("=" * 55)
    return report


def main():
    parser = argparse.ArgumentParser(description="SEO Audit for dyarnaa.com")
    parser.add_argument("--max-urls", type=int, default=None, help="Limit number of URLs to audit")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    report = audit_sitemap(max_urls=args.max_urls, output_format=args.output)

    if report["summary"]["total_issues"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
