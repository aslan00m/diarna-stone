"""
Search Console Sitemaps API.

Lists, submits, and checks the status of sitemaps registered in Search Console.

Endpoint: https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/sitemaps

This module does NOT use Google Indexing API. It only:
- Reads sitemap entries already submitted to GSC
- Submits a sitemap URL via the official Sitemaps API
- Reads the sitemap's last-read/last-submitted status from Google

Submitting a sitemap tells Google about your URLs; it does NOT guarantee they
will be crawled or indexed.
"""
import time
from datetime import datetime


def list_sitemaps(service, site_url):
    """List all sitemaps submitted for a Search Console property.

    Returns dict with 'sitemaps' list and 'ok' flag.
    """
    result = {"ok": False, "sitemaps": [], "error": None}
    try:
        response = service.sitemaps().list(siteUrl=site_url).execute()
        result["ok"] = True
        result["sitemaps"] = response.get("sitemap", [])
    except Exception as e:
        result["error"] = str(e)
    return result


def get_sitemap_status(service, site_url, sitemap_url):
    """Get the status of a specific sitemap from Google's records.

    Args:
        service: GSC API service
        site_url: Property URL (e.g., "https://dyarnaa.com/")
        sitemap_url: The sitemap URL as submitted to Google (e.g., "https://dyarnaa.com/sitemap.xml")

    Returns dict with: ok, sitemap_url, status, last_submitted, last_read,
    urls_indexed, urls_not_indexed, errors, warnings
    """
    result = {
        "ok": False,
        "sitemap_url": sitemap_url,
        "status": None,
        "last_submitted": None,
        "last_read": None,
        "urls_indexed": None,
        "urls_not_indexed": None,
        "errors": None,
        "warnings": None,
        "error": None,
    }

    try:
        response = service.sitemaps().get(
            siteUrl=site_url,
            sitemapUrl=sitemap_url,
        ).execute()

        result["ok"] = True
        result["status"] = response.get("status")
        result["last_submitted"] = response.get("lastSubmitted")
        result["last_read"] = response.get("lastRead")

        # Parse the sitemap-specific stats
        contents = response.get("sitemapEntries", {})
        if isinstance(contents, dict):
            result["urls_indexed"] = contents.get("indexed")
            result["urls_not_indexed"] = contents.get("notIndexed") or contents.get("notIndexedAndExcluded")
            result["errors"] = contents.get("errors")
            result["warnings"] = contents.get("warnings")

        # Also check for common errors array
        errors = response.get("errors", [])
        if errors:
            result["error_list"] = [
                {"message": e.get("message"), "code": e.get("code")}
                for e in errors
            ]

    except Exception as e:
        result["error"] = str(e)

    return result


def submit_sitemap(service, site_url, sitemap_url):
    """Submit a sitemap to Google Search Console.

    NOTE: This does NOT guarantee indexing. It tells Google about your sitemap.
    Use sparingly — only when the sitemap content has changed significantly.

    Args:
        service: GSC API service
        site_url: Property URL (e.g., "https://dyarnaa.com/")
        sitemap_url: Full sitemap URL to submit (e.g., "https://dyarnaa.com/sitemap.xml")

    Returns:
        dict with 'ok', 'submitted', 'error'
    """
    result = {"ok": False, "submitted": False, "sitemap_url": sitemap_url, "error": None}

    try:
        # The Sitemaps API uses PUT to submit
        service.sitemaps().submit(
            siteUrl=site_url,
            body={"url": sitemap_url},
        ).execute()
        # The submit method returns empty on success
        # Verify by checking if it appears in list_sitemaps
        time.sleep(2)
        status = get_sitemap_status(service, site_url, sitemap_url)
        result["ok"] = True
        result["submitted"] = True
        result["verification"] = status
    except Exception as e:
        err_msg = str(e)
        result["error"] = err_msg

    return result


def compare_sitemaps(local_urls, gsc_sitemaps):
    """Compare locally-discovered sitemap URLs with what's registered in GSC.

    Args:
        local_urls: List of URLs from the local sitemap
        gsc_sitemaps: List of sitemap dicts from list_sitemaps()

    Returns:
        dict with 'matching', 'missing_in_gsc', 'extra_in_gsc'
    """
    gsc_urls = set()
    for s in gsc_sitemaps:
        gsc_urls.add(s.get("url", s.get("sitemapUrl", "")))

    local_set = set(local_urls)
    return {
        "matching": local_set & gsc_urls,
        "missing_in_gsc": local_set - gsc_urls,
        "extra_in_gsc": gsc_urls - local_set,
    }
