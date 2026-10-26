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
        site_url: Property URL (e.g., "sc-domain:dyarnaa.com" or "https://dyarnaa.com/")
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
        # Use list_sitemaps to find the sitemap entry
        list_result = list_sitemaps(service, site_url)
        if not list_result.get("ok"):
            result["error"] = list_result.get("error")
            return result

        # Find matching sitemap in the list
        for s in list_result.get("sitemaps", []):
            s_url = s.get("path", s.get("url", s.get("sitemapUrl", "")))
            if s_url == sitemap_url or s_url == sitemap_url.replace("https://", "http://"):
                result["ok"] = True
                result["status"] = s.get("status")
                result["last_submitted"] = s.get("lastSubmitted")
                result["last_read"] = s.get("lastDownloaded")
                contents = s.get("contents", [])
                if isinstance(contents, list) and contents:
                    for c in contents:
                        if isinstance(c, dict):
                            result["urls_indexed"] = c.get("indexed")
                            result["urls_not_indexed"] = c.get("notIndexed") or c.get("notIndexedAndExcluded")
                elif isinstance(contents, dict):
                    result["urls_indexed"] = contents.get("indexed")
                    result["urls_not_indexed"] = contents.get("notIndexed") or contents.get("notIndexedAndExcluded")
                result["errors"] = s.get("errors")
                result["warnings"] = s.get("warnings")
                return result

        # Sitemap not found in the list
        result["error"] = f"Sitemap not found in GSC. Available: {[s.get('url', s.get('sitemapUrl', '')) for s in list_result.get('sitemaps', [])]}"
        return result

    except Exception as e:
        result["error"] = str(e)

    return result


def submit_sitemap(service, site_url, sitemap_url):
    """Submit a sitemap to Google Search Console.

    NOTE: This does NOT guarantee indexing. It tells Google about your sitemap.
    Use sparingly — only when the sitemap content has changed significantly.

    Args:
        service: GSC API service
        site_url: Property URL (e.g., "sc-domain:dyarnaa.com" or "https://dyarnaa.com/")
        sitemap_url: Full sitemap URL to submit (e.g., "https://dyarnaa.com/sitemap.xml")

    Returns:
        dict with 'ok', 'submitted', 'error'
    """
    result = {"ok": False, "submitted": False, "sitemap_url": sitemap_url, "error": None}

    try:
        # The googleapiclient submit() method has a bug in some versions.
        # Use the underlying HTTP request directly.
        import urllib.parse
        encoded_site = urllib.parse.quote(site_url, safe='')
        encoded_sitemap = urllib.parse.quote(sitemap_url, safe='')
        url = f"https://searchconsole.googleapis.com/webmasters/v3/sites/{encoded_site}/sitemaps/{encoded_sitemap}:submit"

        # Use the service's credentials to make the request
        from google.auth.transport.requests import Request
        creds = service._http.credentials
        resp = Request(creds).urlopen(
            'POST',
            url,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data=b''
        )
        status_code = resp.status
        resp.close()

        if status_code in (200, 204):
            result["ok"] = True
            result["submitted"] = True
        else:
            result["error"] = f"HTTP {status_code}"
    except Exception as e:
        result["error"] = str(e)

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
