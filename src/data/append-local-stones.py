#!/usr/bin/env python3
"""Keep stones that exist only in our own catalogue in families.js.

build-families.py generates families.js from the hajar aldar reference data, so any
stone we sell that hajar aldar does not list would be wiped on the next regeneration.
Indian Black Galaxy is exactly that case: hajar aldar has one product for it (ID
282772, listed as "رخام جلاكسي الهندي") but it never reached the 138-page extraction,
so the stone has to be re-added after every generation.

Run AFTER build-families.py.
"""
import json, re, subprocess, os, sys

ROOT = "/opt/data/projects/diarna-stone"
FAM = f"{ROOT}/src/data/families.js"
PROD = f"{ROOT}/src/data/products.js"

# stones we sell that the hajar aldar extraction does not cover
EXTRA = [
    {
        "slug": "indian-galaxy-black",
        "sourceNote": "hajar aldar product 282772 — رخام جلاكسي الهندي. They call it "
                      "marble; the photograph shows Black Galaxy granite (black with "
                      "gold and silver flecks), so it is catalogued as granite.",
    },
]

# keys a stone card must carry, taken from the product record
NEEDED = ["code", "color", "colorCode", "hardness", "density", "origin", "thickness",
          "finish", "uses"]


def load(f):
    js = f"""
    const M=(await import('{f}')).default;
    console.log(JSON.stringify(M));
    """
    tmp = "/tmp/_load.mjs"
    open(tmp, "w").write(js)
    r = subprocess.run(["node", tmp], capture_output=True, text=True)
    if r.returncode:
        print("cannot load", f, r.stderr[-300:])
        sys.exit(1)
    return json.loads(r.stdout.strip())


def main():
    stones = load(FAM)
    products = {p["slug"]: p for p in load(PROD)}
    have = {s["slug"] for s in stones}
    added = []

    for x in EXTRA:
        if x["slug"] in have:
            print(f"already present: {x['slug']}")
            continue
        p = products.get(x["slug"])
        if not p:
            print(f"no product record for {x['slug']} — skipped")
            continue
        spec = {k: p.get(k) for k in NEEDED if p.get(k)}
        card = {
            "slug": p["slug"],
            "name": p["name"].split(" - ")[-1] if " - " in p["name"] else p["name"],
            "nameEn": p["nameEn"],
            "cat": p["category"],
            "origin": p["origin"],
            "image": p["image"],
            "color": p.get("color", "غير محدد"),
            "count": 1,
            "multi": False,
            "grades": [{
                "slug": p["slug"],
                "label": p["name"].split(" - ")[-1] if " - " in p["name"] else p["name"],
                "name": p["name"],
                "nameEn": p["nameEn"],
                "color": p.get("color", "غير محدد"),
                "refColor": p.get("refColor", ""),
                "colorCode": p.get("colorCode", "غير محدد"),
                "spec": spec,
                "isMain": True,
            }],
            "note": x["sourceNote"],
        }
        stones.append(card)
        added.append(p["slug"])

    if not added:
        print("nothing to add")
        return

    src = open(FAM, encoding="utf-8").read()
    src = src.rstrip()
    assert src.endswith("];"), "families.js does not end with ];"
    body = src[:-3].rstrip()
    if not body.endswith(","):
        body += ","
    body += "\n " + ",\n ".join(json.dumps(c, ensure_ascii=False, indent=1)
                                for c in stones[len(stones) - len(added):])
    open(FAM, "w", encoding="utf-8").write(body + "\n];\n")
    print("added to families.js:", added)
    print("stones now:", len(stones))


if __name__ == "__main__":
    main()
