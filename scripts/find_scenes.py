#!/usr/bin/env python3
"""ابحث عن صور مشاهد حجر بتراخيص حرة (CC0 / Public domain).

يستخدم Wikimedia Commons API مع فاصل زمني لتجنّب 429.
يستبعد ملفات PDF والكتب القديمة والنقوش.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
FREE = {"CC0", "Public domain", "PD", "PDM"}

BAD = [
    ".pdf", ".djvu", ".djv", "page1", "naval", "review vol", "literature",
    "boys'", "journal", "lithograph", "engraving", "plate ", "book",
    "illustration", "cover", "title page", "nasa", "map of",
]

QUERIES = {
    "interior": [
        "marble staircase interior", "luxury bathroom marble",
        "modern kitchen stone counter", "hotel lobby marble",
        "marble reception desk", "stone fireplace interior",
    ],
    "facade": [
        "modern building stone cladding", "contemporary facade stone",
        "villa stone facade", "office building facade",
        "residence stone exterior", "stone clad wall",
    ],
    "workshop": [
        "stone quarry mining", "marble quarry", "stone cutting workshop",
        "stone slabs warehouse", "granite blocks",
    ],
    "raw": [
        "marble slabs stacked", "polished stone slabs", "stone blocks pile",
    ],
}


def get(params, retries=3):
    qs = "&".join(
        f"{k}={urllib.parse.quote(str(v), safe='|:/')}" for k, v in params.items()
    )
    req = urllib.request.Request(
        API + "?" + qs,
        headers={"User-Agent": "diarna-stone/1.0 (+https://github.com/aslan00m/diarna-stone)"},
    )
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except Exception as exc:
            if attempt == retries - 1:
                raise
            wait = 5 * (attempt + 1)
            print(f"    retry after {wait}s ({exc})", file=sys.stderr)
            time.sleep(wait)
    return {}


def clean(html):
    return re.sub(r"<[^>]+>", "", html or "").strip()


def main():
    pool = {}
    for key, queries in QUERIES.items():
        seen = set()
        for q in queries:
            d = get({
                "action": "query", "format": "json", "generator": "search",
                "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": 15,
                "prop": "imageinfo", "iiprop": "url|extmetadata|size",
                "iiurlwidth": 1600,
            })
            for pg in list(d.get("query", {}).get("pages", {}).values()):
                ii = (pg.get("imageinfo") or [{}])[0]
                em = ii.get("extmetadata", {})
                lic = em.get("LicenseShortName", {}).get("value", "").strip()
                w, h = ii.get("width", 0), ii.get("height", 0)
                title = pg.get("title", "")[5:]
                low = title.lower()
                if any(b in low for b in BAD):
                    continue
                if lic not in FREE or w < 1200 or h < 800 or title in seen:
                    continue
                seen.add(title)
                pool.setdefault(key, []).append({
                    "title": title, "license": lic,
                    "author": clean(em.get("Artist", {}).get("value", ""))[:60],
                    "url": ii.get("thumburl", ""),
                    "descurl": ii.get("descriptionurl", ""),
                    "w": w, "h": h,
                })
            time.sleep(2.5)

    total = sum(len(v) for v in pool.values())
    for k, v in pool.items():
        print(f"{k}: {len(v)}")
        for i, x in enumerate(v[:8]):
            orient = "wide" if x["w"] > x["h"] else "portrait"
            print(f"  {i}: [{orient}] {x['title'][:48]} | {x['license']} | {x['w']}x{x['h']}")
    print("total:", total)
    with open("/opt/data/cache/scratch/pool2.json", "w") as f:
        json.dump(pool, f, indent=1)


if __name__ == "__main__":
    main()