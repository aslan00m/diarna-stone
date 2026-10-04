#!/usr/bin/env python3
"""Build the family data file used by both the grid card and the stone page.

A family is one stone sold in several grades. hajar aldar publishes ONE photo per
product page (no gallery), and our 122 photos collapse to 61 distinct files — grades of
the same stone are genuinely the same picture, byte for byte. So the stone page shows
the photo once, in the header, and lists every grade below it in a table with that
grade's own colour, colour code and full specification. No image is ever repeated.
"""
import json, hashlib, os, collections, re

ATTACH = "/opt/data/cache/scratch/attach_manifest.json"
OURS = "/opt/data/cache/scratch/ours3.json"
IMG_DIR = "/opt/data/projects/diarna-stone/public/images/products-hj"
OUT = "/opt/data/projects/diarna-stone/src/data/families.js"


def type_label(name):
    """Arabic half of a bilingual title, without the disambiguating suffix."""
    ar = name.split(" - ")[-1] if " - " in name else name
    ar = ar.split(" — كود")[0]
    return re.sub(r"\s*\(\d+\)$", "", ar).strip()


def latin_label(name):
    return name.split(" - ")[0].strip() if " - " in name else ""


SPEC_KEYS = ["size", "thickness", "finish", "hardness", "density", "uses", "code",
             "origin", "material"]


def main():
    man = json.load(open(ATTACH, encoding="utf-8"))
    att = man["attached"]
    ours = {p["slug"]: p for p in json.load(open(OURS, encoding="utf-8"))}

    by_hash = collections.defaultdict(list)
    for m in att:
        p = os.path.join(IMG_DIR, m["image"].split("/")[-1])
        by_hash[hashlib.md5(open(p, "rb").read()).hexdigest()].append(m)

    cards = []
    for members in by_hash.values():
        members = sorted(members, key=lambda m: (len(m["slug"]), m["slug"]))
        rep = members[0]
        ro = ours.get(rep["slug"], {})
        grades = []
        for m in members:
            o = ours.get(m["slug"], {})
            grades.append({
                "slug": m["slug"],
                "label": type_label(m["name"]),
                "name": m["name"],
                "nameEn": latin_label(m["name"]),
                "color": o.get("color") or "غير محدد",
                "refColor": o.get("refColor") or "",
                "colorCode": (o.get("colorCode") or o.get("refCode")
                              or "غير محدد"),
                "spec": {k: o.get(k) for k in SPEC_KEYS if o.get(k)},
                "isMain": m["slug"] == rep["slug"],
            })
        # the family's own name: prefer a grade label that reads as the stone itself
        labels = [g["label"] for g in grades]
        fam_label = min(labels, key=lambda s: (len(s), s))
        cards.append({
            "slug": rep["slug"],
            "name": fam_label,
            "nameEn": grades[0]["nameEn"],
            "cat": ro.get("cat", ""),
            "origin": ro.get("origin", ""),
            "image": rep["image"],
            "color": ro.get("color") or "غير محدد",
            "count": len(grades),
            "multi": len(grades) > 1,
            "grades": grades,
        })

    fam_slugs = {g["slug"] for c in cards for g in c["grades"]}

    def single(m_or_sk, slug, name, image):
        o = ours.get(slug, {})
        return {
            "slug": slug, "name": name, "nameEn": latin_label(name),
            "cat": o.get("cat", ""), "origin": o.get("origin", ""),
            "image": image, "color": o.get("color") or "غير محدد",
            "count": 1, "multi": False,
            "grades": [{"slug": slug, "label": type_label(name), "name": name,
                        "nameEn": latin_label(name),
                        "color": o.get("color") or "غير محدد",
                        "refColor": o.get("refColor") or "",
                        "colorCode": o.get("colorCode") or "غير محدد",
                        "spec": {k: o.get(k) for k in SPEC_KEYS if o.get(k)},
                        "isMain": True}],
        }

    for m in att:
        if m["slug"] not in fam_slugs:
            cards.append(single(m, m["slug"], type_label(m["name"]), m["image"]))
    for sk in man["skipped"]:
        o = ours.get(sk["slug"], {})
        cards.append(single(sk, sk["slug"], o.get("name", sk["name"]),
                            o.get("image", "")))

    cards.sort(key=lambda c: (c["cat"], c["name"]))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("// Generated from the hajar aldar reference catalogue by\n")
        f.write("// src/data/families.js — see scripts/build_family_cards.py.\n")
        f.write("// One entry per stone. A stone with several grades lists them in `grades`;\n")
        f.write("// the photo appears once (in the card header and the stone page header).\n")
        f.write("export default " + json.dumps(cards, ensure_ascii=False, indent=1) + ";\n")

    multi = [c for c in cards if c["multi"]]
    print(f"stones: {len(cards)}  | multi-grade: {len(multi)}  "
          f"| single: {len(cards) - len(multi)}")
    print(f"grades total: {sum(len(c['grades']) for c in cards)}")
    print(f"distinct photos referenced: "
          f"{len({c['image'] for c in cards if c['image']})}")
    print("categories:", dict(collections.Counter(c["cat"] for c in cards)))
    biggest = max(cards, key=lambda c: c["count"])
    print(f"\nlargest: {biggest['name']} ({biggest['count']} درجات)")
    for g in biggest["grades"]:
        print(f"   {g['label'][:36]:38} {g['color'][:16]:18} {g['colorCode']}")


if __name__ == "__main__":
    main()