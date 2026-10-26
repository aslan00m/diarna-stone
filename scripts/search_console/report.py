"""
Report generation for Google Search Console monitoring.

Combines results from:
  - Local HTTP sitemap audit (indexing_monitor.py)
  - URL Inspection API results
  - Sitemap API status
  - Search Analytics data

Produces structured JSON reports and human-readable Markdown summaries.
"""
import json
import os
from datetime import datetime


def build_report(site_url, config, local_audit, gsc_sites, gsc_sitemap_status,
                 gsc_inspection_results, gsc_analytics=None):
    """Assemble a comprehensive report from all monitoring components.

    Args:
        site_url: The site being monitored
        config: GSC config dict
        local_audit: Results from the HTTP-based sitemap audit
        gsc_sites: Result from sites_api.verify_site_access
        gsc_sitemap_status: Result from sitemap_manager.get_sitemap_status
        gsc_inspection_results: List of results from inspect_urls.inspect_batch
        gsc_analytics: Optional result from search_analytics

    Returns:
        Comprehensive report dict
    """
    timestamp = datetime.now().isoformat()

    # Classify inspection results
    classifications = {}
    for r in gsc_inspection_results:
        from search_console.inspect_urls import classify_inspection_result
        cls = classify_inspection_result(r)
        classifications[r["url"]] = cls

    report = {
        "timestamp": timestamp,
        "site": site_url,
        "summary": {
            "total_urls_in_sitemap": local_audit.get("sitemap_url_count", 0),
            "local_404_count": local_audit.get("count_404", 0),
            "local_200_count": local_audit.get("count_200", 0),
            "canonical_mismatches": len(local_audit.get("canonical_mismatches", [])),
            "sitemap_xml_valid": local_audit.get("sitemap_xml_valid", False),
            "sitemap_consistency_ok": local_audit.get("sitemap_consistency", False),
            "gsc_property_found": gsc_sites.get("has_access", False) if gsc_sites else False,
            "gsc_sitemap_registered": bool(gsc_sitemap_status and gsc_sitemap_status.get("status")),
            "inspection_urls_checked": len(gsc_inspection_results) if gsc_inspection_results else 0,
            "indexed_by_google": sum(1 for c in classifications.values() if c == "indexed"),
            "not_indexed_by_google": sum(1 for c in classifications.values() if c == "not-indexed"),
            "google_unknown": sum(1 for c in classifications.values() if c in ("unknown", "inspection-error")),
            "auth_errors": sum(1 for c in classifications.values() if c == "auth-error"),
        },
        "local_audit": local_audit,
        "gsc": {
            "property_verified": gsc_sites.get("has_access", False) if gsc_sites else False,
            "property_details": gsc_sites if gsc_sites else None,
            "sitemap_status": gsc_sitemap_status,
            "url_inspections": gsc_inspection_results,
            "classifications": classifications,
            "search_analytics": gsc_analytics,
        },
        "recommendations": _generate_recommendations(
            local_audit, gsc_sites, gsc_sitemap_status, gsc_inspection_results, classifications
        ),
    }

    return report


def _generate_recommendations(local_audit, gsc_sites, gsc_sitemap_status,
                               gsc_inspections, classifications):
    """Generate actionable recommendations based on audit results."""
    recs = []

    # 404 pages
    if local_audit.get("count_404", 0) > 0:
        recs.append({
            "priority": "high",
            "category": "broken_links",
            "message": f"{local_audit['count_404']} URLs return 404 in sitemap. Remove them or fix redirects.",
            "action": "Update sitemap.xml.js to exclude non-existent pages.",
        })

    # Sitemap not registered in GSC
    if gsc_sitemap_status and not gsc_sitemap_status.get("ok"):
        recs.append({
            "priority": "medium",
            "category": "sitemap",
            "message": "Sitemap not registered in Google Search Console. Submit via Sitemaps API or manually.",
            "action": "Run: python3 -m search_console.sitemap_manager --submit",
        })

    # Canonical mismatches
    if local_audit.get("canonical_mismatches"):
        recs.append({
            "priority": "medium",
            "category": "canonical",
            "message": f"{len(local_audit['canonical_mismatches'])} canonical mismatches detected.",
            "action": "Verify canonical tags match the actual served URLs.",
        })

    # URLs not indexed by Google
    not_indexed = [u for u, c in classifications.items() if c == "not-indexed"]
    if not_indexed:
        recs.append({
            "priority": "medium",
            "category": "indexing",
            "message": f"{len(not_indexed)} URLs are known to Google but not indexed. Consider internal linking or fresh content.",
            "action": "Review content quality and add internal links to these pages.",
            "urls": not_indexed[:10],
        })

    # Auth errors
    auth_errors = [u for u, c in classifications.items() if c == "auth-error"]
    if auth_errors:
        recs.append({
            "priority": "high",
            "category": "auth",
            "message": f"{len(auth_errors)} URL inspections failed due to auth/permission errors.",
            "action": "Verify Service Account has Search Console access. See SETUP_GSC.md.",
        })

    if not recs:
        recs.append({
            "priority": "info",
            "category": "all_clear",
            "message": "No issues detected. Sitemap is healthy, all URLs return 200, and Google shows indexing coverage.",
        })

    return recs


def save_report(report, report_dir):
    """Save a report as timestamped JSON and latest.json, plus Markdown summary."""
    os.makedirs(report_dir, exist_ok=True)
    timestamp = report["timestamp"].replace(":", "").replace("-", "")[:15]

    json_path = os.path.join(report_dir, f"report-{timestamp}.json")
    latest_path = os.path.join(report_dir, "latest.json")
    md_path = os.path.join(report_dir, f"summary-{timestamp}.md")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    _write_markdown_summary(report, md_path)

    return {"json": json_path, "latest": latest_path, "markdown": md_path}


def _write_markdown_summary(report, path):
    """Write a human-readable Markdown summary of the report."""
    s = report["summary"]
    lines = [
        f"# تقرير فحص dyarnaa.com",
        f"\n**التاريخ:** {report['timestamp']}",
        f"**الهدف:** {report.get('site', 'N/A')}",
        f"\n## الملخص",
        f"| المقياس | القيمة |",
        f"|---|---|",
        f"| إجمالي الروابط في Sitemap | {s.get('total_urls', s.get('total_urls_in_sitemap', 0))} |",
        f"| 200 OK | {s.get('status_200_count', s.get('local_200_count', 0))} |",
        f"| 404 | {s.get('status_404_count', s.get('local_404_count', 0))} |",
        f"| مشاكل | {s.get('total_issues', 0)} |",
        f"| إعادة توجيه | {s.get('redirects_count', 0)} |",
        f"| XML Sitemap صالح | {'✓' if report.get('sitemap_validation', {}).get('xml_valid', s.get('sitemap_xml_valid', True)) else '✗'} |",
        f"| تناسق Sitemap | {'✓' if report.get('sitemap_validation', {}).get('consistency_ok', s.get('sitemap_consistency_ok', True)) else '✗'} |",
        f"| GSC API متاح | {'✓' if s.get('gsc_available') else '✗'} |",
    ]

    # Add GSC classification summary if available
    gsc_data = report.get("gsc", {})
    if "classifications" in gsc_data:
        from collections import Counter
        cls_counts = Counter(gsc_data["classifications"].values())
        lines += [
            f"| مفهرس (Google) | {s.get('indexed_by_google', 0)} |",
            f"| غير مفهرس (Google) | {s.get('not_indexed_by_google', 0)} |",
            f"| غير معروف (Google) | {s.get('google_unknown', 0)} |",
            f"| أخطاء مصادقة | {s.get('auth_errors', 0)} |",
        ]
    lines.append("")
    lines.append("## التوصيات")
    for rec in report.get("recommendations", []):
        emoji = "🔴" if rec["priority"] == "high" else "🟡" if rec["priority"] == "medium" else "ℹ️"
        lines.append(f"\n{emoji} **{rec['category']}** — {rec['message']}")
        if "urls" in rec:
            lines.append(f"  URLs متأثرة: {', '.join(rec['urls'])}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
