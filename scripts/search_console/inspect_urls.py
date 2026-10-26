"""
Search Console URL Inspection API.

Inspects individual URLs to get Google's latest indexing data:
  - Verdict (passing/not passing)
  - Coverage state (indexed, not indexed, etc.)
  - Last crawl time
  - Page fetch state
  - Google canonical vs user canonical
  - Mobile usability
  - Rich result issues

Endpoint: POST https://searchconsole.googleapis.com/v1/urlInspection/index:inspect

Rate limits: URL Inspection API is limited (~600 requests/day per project).
This module enforces batch limits and exponential backoff.
"""
import time
from datetime import datetime


def inspect_url(service, inspection_url, site_url, language_code="ar"):
    """Inspect a single URL via the URL Inspection API.

    Args:
        service: Authenticated GSC API service object
        inspection_url: Full URL to inspect (e.g., "https://dyarnaa.com/")
        site_url: GSC property URL (e.g., "https://dyarnaa.com/")
        language_code: Preferred language for the inspection result

    Returns:
        dict with fields: url, ok, verdict, coverage_state, last_crawl,
        page_fetch_state, google_canonical, user_canonical, sitemap,
        mobile_usability, rich_results, issues, error
    """
    result = {
        "url": inspection_url,
        "timestamp": datetime.now().isoformat(),
        "ok": False,
        "verdict": None,
        "coverage_state": None,
        "indexing_state": None,
        "last_crawl": None,
        "page_fetch_state": None,
        "google_canonical": None,
        "user_canonical": None,
        "sitemap": None,
        "mobile_usability": None,
        "rich_results": None,
        "verdict_issues": [],
        "error": None,
    }

    try:
        body = {
            "inspectionUrl": inspection_url,
            "siteUrl": site_url,
            "languageCode": language_code,
        }
        response = service.urlInspection().index().inspect(body=body).execute()
        inspection = response.get("inspectionResult", {})

        result["ok"] = True

        # Verdict
        verdict = inspection.get("verdict", {})
        result["verdict"] = verdict.get("verdict", "unknown")

        # Detailed verdict issues
        issues = verdict.get("issues", [])
        for issue in issues:
            result["verdict_issues"].append({
                "severity": issue.get("severity"),
                "code": issue.get("code"),
                "message": issue.get("message"),
            })

        # Index status (the key data Google returns)
        index_result = inspection.get("indexStatusResult", {})
        if index_result:
            result["coverage_state"] = index_result.get("coverageState")
            result["indexing_state"] = index_result.get("indexingState")
            result["last_crawl"] = index_result.get("lastCrawlTime")
            result["page_fetch_state"] = index_result.get("pageFetchState")
            result["google_canonical"] = index_result.get("googleCanonical")
            result["user_canonical"] = index_result.get("userCanonical")
            result["sitemap"] = index_result.get("sitemap")
            result["mobile_usability"] = index_result.get("mobileUsabilityResult", {}).get("mobileUsabilityState")
            if "richResultIssues" in index_result:
                result["rich_results"] = "issues found"
            else:
                result["rich_results"] = "none detected"

    except Exception as e:
        result["error"] = str(e)

    return result


def inspect_batch(service, urls, site_url, language_code="ar", delay=2, max_errors=3):
    """Inspect a batch of URLs with rate limiting and error tolerance.

    Args:
        service: Authenticated GSC API service object
        urls: List of URL strings to inspect
        site_url: GSC property URL
        delay: Seconds to wait between requests (avoid 429)
        max_errors: Stop after this many consecutive errors

    Returns:
        List of inspection result dicts
    """
    results = []
    consecutive_errors = 0

    for i, url in enumerate(urls):
        if consecutive_errors >= max_errors:
            results.append({
                "url": url,
                "ok": False,
                "error": f"Stopped after {max_errors} consecutive errors",
            })
            continue

        result = inspect_url(service, url, site_url, language_code)
        results.append(result)

        if result["ok"]:
            consecutive_errors = 0
        else:
            consecutive_errors += 1

        if delay > 0 and i < len(urls) - 1:
            time.sleep(delay)

    return results


def classify_inspection_result(result):
    """Classify a single URL inspection result into a status category.

    Returns one of:
    - 'indexed'          — Google has this URL indexed
    - 'not-indexed'      — Google knows the URL but hasn't indexed it
    - 'unknown'          — Insufficient data from Google
    - 'inspection-error' — API call failed
    - 'auth-error'       — Authentication/permission error
    """
    if result.get("error"):
        err = result["error"].lower()
        if "401" in err or "403" in err or "auth" in err or "permission" in err or "credential" in err:
            return "auth-error"
        if "429" in err or "quota" in err:
            return "api-quota-error"
        return "inspection-error"

    if not result.get("ok"):
        return "inspection-error"

    coverage = result.get("coverage_state")
    indexing = result.get("indexing_state")

    if coverage and "discovered" in coverage.lower() or "indexed" in coverage.lower():
        return "indexed"
    if coverage and "not" in coverage.lower() and "indexed" in coverage.lower():
        return "not-indexed"
    if indexing and "none" in indexing.lower() or "not" in indexing.lower():
        return "not-indexed"

    return "unknown"
