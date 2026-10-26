"""
Search Console Search Analytics API.

Queries search performance data: clicks, impressions, CTR, and average position
for the site's pages and queries in Google Search results.

Endpoint: POST https://searchconsole.googleapis.com/webmasters/v3/sites/{siteUrl}/searchanalytics/query

Data is typically available with a 2-3 day delay. Queries for the last 28 days
by default, compared to the previous 28-day period.
"""
import urllib.parse
from datetime import datetime, timedelta


def query_analytics(service, site_url, dimensions=None, row_limit=100,
                    start_date=None, end_date=None, dimension_filter_groups=None):
    """Query Search Analytics data for a site.

    Args:
        service: Authenticated GSC API service
        site_url: Property URL (e.g., "https://dyarnaa.com/")
        dimensions: List of dimension names to group by (e.g., ["page", "query"])
        row_limit: Max rows to return (max 25000 for searchanalytics.query)
        start_date: "YYYY-MM-DD" or None for 28 days ago
        end_date: "YYYY-MM-DD" or None for today-3days (data lag)
        dimension_filter_groups: Optional filter groups

    Returns:
        dict with 'ok', 'rows', 'totals', 'error'
    """
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=28)).strftime("%Y-%m-%d")
    if end_date is None:
        end_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

    body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": dimensions or [],
        "rowLimit": row_limit,
    }
    if dimension_filter_groups:
        body["dimensionFilterGroups"] = dimension_filter_groups

    result = {
        "ok": False,
        "start_date": start_date,
        "end_date": end_date,
        "rows": [],
        "totals": None,
        "error": None,
    }

    try:
        response = service.searchanalytics().query(
            siteUrl=site_url, body=body
        ).execute()

        result["ok"] = True
        result["rows"] = response.get("rows", [])

        # Calculate totals
        total_clicks = sum(r.get("clicks", 0) for r in result["rows"])
        total_impressions = sum(r.get("impressions", 0) for r in result["rows"])
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        positions = [r.get("position", 0) for r in result["rows"] if r.get("impressions", 0) > 0]
        avg_position = sum(positions) / len(positions) if positions else 0

        result["totals"] = {
            "clicks": total_clicks,
            "impressions": total_impressions,
            "ctr": round(avg_ctr, 2),
            "avg_position": round(avg_position, 2),
        }

    except Exception as e:
        result["error"] = str(e)

    return result


def query_top_pages(service, site_url, days=28, row_limit=50):
    """Get top-performing pages by clicks.

    Returns list of {page, clicks, impressions, ctr, position}.
    """
    return query_analytics(
        service, site_url,
        dimensions=["page"],
        row_limit=row_limit,
        start_date=(datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"),
        end_date=(datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
    )


def query_top_queries(service, site_url, days=28, row_limit=50):
    """Get top-performing search queries by impressions.

    Returns list of {query, clicks, impressions, ctr, position}.
    """
    return query_analytics(
        service, site_url,
        dimensions=["query"],
        row_limit=row_limit,
        start_date=(datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"),
        end_date=(datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
    )


def query_country_performance(service, site_url, days=28):
    """Get performance by country, focusing on Saudi Arabia (SA).

    Returns list of {country, clicks, impressions, ctr, position}.
    """
    return query_analytics(
        service, site_url,
        dimensions=["country", "page"],
        row_limit=200,
        start_date=(datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"),
        end_date=(datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
    )


def query_page_query_combined(service, site_url, days=28, row_limit=100):
    """Get combined page + query performance.

    Returns list of {page, query, clicks, impressions, ctr, position}.
    """
    return query_analytics(
        service, site_url,
        dimensions=["page", "query"],
        row_limit=row_limit,
        start_date=(datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"),
        end_date=(datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
    )


def compare_periods(service, site_url, days=28):
    """Compare current period vs previous period performance.

    Returns dict with 'current' and 'previous' totals.
    """
    current_end = datetime.now() - timedelta(days=3)
    current_start = current_end - timedelta(days=days)
    prev_end = current_start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=days)

    current = query_analytics(
        service, site_url,
        dimensions=[],
        row_limit=1,
        start_date=current_start.strftime("%Y-%m-%d"),
        end_date=current_end.strftime("%Y-%m-%d"),
    )
    previous = query_analytics(
        service, site_url,
        dimensions=[],
        row_limit=1,
        start_date=prev_start.strftime("%Y-%m-%d"),
        end_date=prev_end.strftime("%Y-%m-%d"),
    )

    return {
        "current": current.get("totals") if current["ok"] else None,
        "previous": previous.get("totals") if previous["ok"] else None,
        "current_error": current.get("error"),
        "previous_error": previous.get("error"),
    }
