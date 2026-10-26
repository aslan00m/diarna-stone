"""
Search Console Sites API.

Verifies which properties the authenticated account can access, and checks
whether the target site (dyarnaa.com) is registered.

Endpoint: GET https://searchconsole.googleapis.com/webmasters/v3/sites
"""
from datetime import datetime


def list_sites(service):
    """List all Search Console properties the account can access.

    Returns dict with 'sites' list and any error.
    Each site has: identifier (URL), permissionLevel, and siteType.
    """
    try:
        response = service.sites().list().execute()
        return {
            "ok": True,
            "sites": response.get("siteEntry", []),
        }
    except Exception as e:
        return {"ok": False, "error": str(e), "sites": []}


def find_site_property(service, target_url):
    """Find the Search Console property matching the target URL.

    Checks for exact match, domain property, and http/https variants.
    Returns dict with site info or None if not found.
    """
    target = target_url.rstrip("/")
    targets_to_check = [
        target + "/",          # https://dyarnaa.com/
        "sc-domain:" + target.replace("https://", "").replace("http://", ""),  # sc-domain:dyarnaa.com
        target,                # https://dyarnaa.com (no trailing slash)
        target.replace("https://", "https://www."),
    ]

    result = list_sites(service)
    if not result["ok"]:
        return {"found": False, "error": result["error"], "matching_site": None}

    for site in result["sites"]:
        ident = site.get("identifier", "")
        for t in targets_to_check:
            if ident == t:
                return {
                    "found": True,
                    "matching_site": {
                        "identifier": ident,
                        "permission_level": site.get("permissionLevel"),
                        "site_type": site.get("siteType"),
                        "url": ident,
                    },
                }
    return {"found": False, "matching_site": None, "available_sites": result["sites"]}


def verify_site_access(service, target_url):
    """Full verification: list sites, find matching property, check permissions.

    Returns a structured report.
    """
    config_targets = [
        target_url,
        target_url.replace("https://", "https://www."),
    ]

    result = {
        "timestamp": datetime.now().isoformat(),
        "target_url": target_url,
        "all_sites": [],
        "matching_property": None,
        "has_access": False,
        "permission_level": None,
        "site_type": None,
        "error": None,
    }

    list_result = list_sites(service)
    if not list_result["ok"]:
        result["error"] = list_result["error"]
        return result

    result["all_sites"] = [
        {"identifier": s.get("identifier"), "permission_level": s.get("permissionLevel"),
         "site_type": s.get("siteType")}
        for s in list_result["sites"]
    ]

    for target in config_targets:
        found = find_site_property(service, target)
        if found["found"]:
            result["matching_property"] = found["matching_site"]
            result["has_access"] = True
            result["permission_level"] = found["matching_site"]["permission_level"]
            result["site_type"] = found["matching_site"]["site_type"]
            return result

    return result
