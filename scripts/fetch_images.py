#!/usr/bin/env python3
"""اجمع صور حجر بتراخيص حرة (CC0 / Public domain) من Wikimedia Commons."""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
FREE = {"CC0", "Public domain", "PD", "PDM"}


def get(params):
    # Wikimedia's API rejects %7C in multi-value params (iiprop), so build
    # the query string ourselves and leave `|` intact.
    qs = "&".join(
        f"{k}={urllib.parse.quote(str(v), safe='|:/')}"
        for k, v in params.items()
    )
    url = API + "?" + qs
    req = urllib.request.Request(url, headers={
        "User-Agent": "diarna-stone/1.0 (+https://github.com/aslan00m/diarna-stone)",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        out = resp.read().decode("utf-8", "replace")
    if os.environ.get("DEBUG_FETCH"):
        print(f"  [raw] {len(out)} bytes", file=sys.stderr)
    return json.loads(out)


def search(query, limit=25):
    d = get({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query, "gsrnamespace": 6, "gsrlimit": limit,
        "prop": "imageinfo", "iiprop": "url|extmetadata|size",
        "iiurlwidth": 1400,
    })
    pages = list(d.get("query", {}).get("pages", {}).values())
    if os.environ.get("DEBUG_FETCH"):
        print(f"  [dbg] {query!r} -> {len(pages)} pages", file=sys.stderr)
    return pages


def clean(html):
    return re.sub(r"<[^>]+>", "", html or "").strip()


QUERIES = {
    "marble": ["marble texture seamless", "white marble texture", "carrara marble"],
    "granite": ["granite surface texture", "granite stone surface"],
    "travertine": ["travertine stone texture", "travertine"],
    "limestone": ["limestone texture stone"],
    "interior": ["marble floor interior", "stone interior staircase"],
    "facade": ["stone facade building", "stone cladding building modern"],
    "workshop": ["marble quarry", "stone quarry"],
}

pool = {}
for key, queries in QUERIES.items():
    seen = set()
    for q in queries:
        for p in search(q):
            ii = (p.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata", {})
            lic = em.get("LicenseShortName", {}).get("value", "").strip()
            w, h = ii.get("width", 0), ii.get("height", 0)
            title = p.get("title", "")[5:]
            # CC0/PD images are often seamless square textures (width==height),
            # so only require a sane minimum dimension, not a landscape ratio.
            if lic not in FREE or w < 800 or h < 600 or title in seen:
                continue
            url = ii.get("thumburl", "")
            if not url:
                continue
            seen.add(title)
            pool.setdefault(key, []).append({
                "title": title,
                "license": lic,
                "author": clean(em.get("Artist", {}).get("value", ""))[:80],
                "url": url,
                "descurl": ii.get("descriptionurl", ""),
                "w": w, "h": h,
            })

total = sum(len(v) for v in pool.values())
print("TOTAL:", total)
for k, v in pool.items():
    print(f"  {k}: {len(v)}")
with open("/opt/data/cache/scratch/pool.json", "w") as f:
    json.dump(pool, f, indent=1)
print("saved")