"""
Google Search Console API client package for dyarnaa.com indexing monitor.

This package provides a free, self-contained way to:
  - Authenticate with Google Search Console API (Service Account or OAuth2)
  - Inspect URLs via the URL Inspection API
  - Manage Sitemaps via the Sitemaps API
  - Query Search Analytics data
  - Generate structured reports

Usage:
    from search_console.auth import get_gsc_service
    from search_console.sites_api import list_sites, verify_site_access
    from search_console.inspect_urls import inspect_url, inspect_batch
    from search_console.sitemap_manager import submit_sitemap, list_sitemaps
    from search_console.search_analytics import query_search_analytics
"""
