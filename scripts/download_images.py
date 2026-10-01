#!/usr/bin/env python3
"""نزّل صور الحجر الحرة من Wikimedia Commons إلى public/images/products/.

كل الصور المرشحة مرخّصة CC0 أو Public domain — استخدام تجاري بلا شرط.
ينشئ أيضاً public/images/CREDITS.md لتوثيق المصدر والرخصة.
"""
import json
import os
import re
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
POOL = "/opt/data/cache/scratch/pool.json"
OUT_DIR = os.path.join(ROOT, "public", "images", "products")

HEADERS = {
    "User-Agent": "diarna-stone/1.0 (+https://github.com/aslan00m/diarna-stone)",
}

# (category, slug) -> description of what the photo shows
WANTED = {
    "tundra-grey-marble":      ("marble", "رخام توندرا رمادي"),
    "emperador-light-marble": ("marble", "رخام إمبرادور فاتح"),
    "pietra-grey-marble":      ("marble", "رخام بيترا رمادي"),
    "levanto-marble":          ("marble", "رخام ليفانتو"),
    "bianco-carrara-marble":   ("marble", "رخام بيانكو كرارة"),
    "carrara-mugla-white-marble": ("marble", "رخام موغلا الأبيض"),
    "buccino-italian-marble":  ("marble", "رخام بوتشينو"),
    "desert-omani-marble":     ("marble", "رخام ديزرت عماني"),
    "glacier-indian-marble":   ("marble", "رخام جلاكسي الهندي"),
    "cipollino-italian-marble":("marble", "رخام تشيبولينو"),
    "calacatta-gold-marble":   ("marble", "رخام كالاكاتا الذهبي"),
    "atlantic-blue-marble":    ("marble", "رخام أتلانتيك الأزرق"),
    "statuario-marble":        ("marble", "رخام ستاتيواريو"),
    "markina-white-marble":    ("marble", "رخام ماركينا الأبيض"),
    "silver-grey-marble":      ("marble", "رخام سيلفر رمادي"),
    "roman-travertine":        ("travertine", "ترافنتينو روماني"),
    "yellow-travertine":       ("travertine", "ترافنتينو أصفر"),
    "silver-travertine":       ("travertine", "ترافنتينو فضي"),
    "veined-travertine":       ("travertine", "ترافنتينو معرّق"),
    "black-granite":           ("granite", "جرانيت أسود"),
    "egyptian-granite-red":    ("granite", "جرانيت أحمر مصري"),
    "grey-granite":            ("granite", "جرانيت رمادي"),
    "green-granite":           ("granite", "جرانيت أخضر"),
    "pink-granite":            ("granite", "جرانيت وردي"),
    "nero-assoluto":           ("granite", "جرانيت نيرو أسولوتو"),
    "cream-limestone":         ("limestone", "حجر جيري كريمي"),
    "white-limestone":         ("limestone", "حجر جيري أبيض"),
}


def slug_key(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def main():
    pool = json.load(open(POOL))
    os.makedirs(OUT_DIR, exist_ok=True)

    used = 0
    used_keys = set()
    mapping = {}
    credits = []

    for slug, (cat, label) in WANTED.items():
        for item in pool.get(cat, []):
            key = slug_key(item["title"])
            if key in used_keys:
                continue
            ext = ".jpg" if not item["url"].lower().endswith(".png") else ".png"
            fname = f"{slug}{ext}"
            dest = os.path.join(OUT_DIR, fname)
            try:
                req = urllib.request.Request(item["url"], headers=HEADERS)
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = r.read()
                if len(data) < 8000:
                    continue
                with open(dest, "wb") as fh:
                    fh.write(data)
            except Exception as exc:
                print(f"  ! {slug}: {exc}")
                continue
            used_keys.add(key)
            mapping[slug] = f"/images/products/{fname}"
            credits.append({
                "slug": slug, "label": label, "file": fname,
                "source": item["descurl"], "license": item["license"],
                "author": item["author"],
            })
            used += 1
            print(f"  ok {fname}")
            break

    with open("/opt/data/cache/scratch/mapping.json", "w") as fh:
        json.dump(mapping, fh, indent=1)
    with open(os.path.join(ROOT, "public", "images", "CREDITS.json"), "w") as fh:
        json.dump(credits, fh, indent=1, ensure_ascii=False)

    print(f"\nDOWNLOADED {used} / {len(WANTED)}")


if __name__ == "__main__":
    main()