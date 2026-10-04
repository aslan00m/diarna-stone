#!/usr/bin/env python3
"""Fill missing photos on stone cards from the matching product record.

The stone cards in families.js are built from hajar aldar data, so any stone they do
not stock there (all eight travertine cards, for one) carries no photo even though the
matching product in products.js always has one. Same stone, same file — just link it.
"""
import json, re, subprocess, os

FAM = "/opt/data/projects/diarna-stone/src/data/families.js"
PUB = "/opt/data/projects/diarna-stone/public"

js = f"""
const F=(await import('{FAM}')).default;
const P=(await import('/opt/data/projects/diarna-stone/src/data/products.js')).default;
console.log(JSON.stringify({{
  missing: F.filter(s=>!s.image).map(s=>({{slug:s.slug,name:s.name,cat:s.cat}})),
  products: P.map(p=>({{slug:p.slug,name:p.name,cat:p.category,image:p.image||''}})),
}}));
"""
open("/tmp/fixfam.mjs", "w").write(js)
data = json.loads(subprocess.run(["node", "/tmp/fixfam.mjs"],
                                 capture_output=True, text=True).stdout.strip())
missing = data["missing"]
print(f"stone cards with no photo: {len(missing)}")
if not missing:
    raise SystemExit("nothing to do")

src = open(FAM, encoding="utf-8").read()
filled, unfilled = [], []
for m in missing:
    # match on the stone's Arabic name inside the card's grade labels, falling back to
    # slug similarity — never guess across categories
    cand = [p for p in data["products"]
            if p["cat"] == m["cat"] and p["image"]
            and (m["name"] in p["name"] or p["name"] in m["name"])]
    if not cand:
        # same category, closest name by shared characters
        cand = [p for p in data["products"] if p["cat"] == m["cat"] and p["image"]]
        if cand:
            best = max(cand, key=lambda p: len(set(p["name"]) & set(m["name"])))
            cand = [best] if len(set(best["name"]) & set(m["name"])) >= 6 else []
    if not cand:
        unfilled.append(m)
        continue
    img = cand[0]["image"]
    if not os.path.exists(PUB + img):
        unfilled.append(m)
        continue
    # rewrite only this card's image field
    pat = re.compile(
        r"(\"slug\": \"" + re.escape(m["slug"]) + r"\",.*?\"image\": )\"\"" , re.S)
    src, n = pat.subn(lambda mm: mm.group(1) + json.dumps(img, ensure_ascii=False), src, count=1)
    if n:
        filled.append((m["name"][:30], img))

print(f"filled: {len(filled)}")
for n, i in filled:
    print(f"   {n:32} -> {i}")
print(f"still missing: {len(unfilled)}")
for m in unfilled:
    print(f"   - {m['slug']} ({m['cat']})")

open(FAM, "w", encoding="utf-8").write(src)
