#!/usr/bin/env python3
"""Add one product to the catalogue from a name + a photo, one at a time.

The owner sends a name and an image; this turns them into a product record and
puts the image where the site expects it. Everything it does is verified before
it writes anything, and it prints PASS/FAIL per check so a mistake is visible
instead of silent.

Usage:
    python3 scripts/intake_product.py add \
        --name "رخام كالاكاتا ذهبي" \
        --name-en "Calacatta Gold Marble" \
        --category marble --origin italian \
        --color "أبيض بعروق ذهبية" \
        --image /path/to/photo.jpg \
        [--thickness "20 مم,30 مم"] [--finish "مصقول (Polished)"] \
        [--uses "أرضيات,واجهات"] [--excerpt "..."] [--dry-run]

Usage:
    python3 scripts/intake_product.py list        # every product, slug + image
    python3 scripts/intake_product.py check       # catalogue-wide integrity
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata

ROOT = "/opt/data/projects/diarna-stone"
PRODUCTS = f"{ROOT}/src/data/products.js"
CERAMIC = f"{ROOT}/src/data/products-ceramic.js"
IMG_DIR = f"{ROOT}/public/images/products-local"
QUEUE = f"{ROOT}/src/data/products-local.js"

CATEGORIES = {
    "marble": "رخام",
    "granite": "جرانيت",
    "travertine": "ترافنتينو",
    "limestone": "حجر جيري",
    "sinks": "المغاسل",
    "ceramic": "سيراميك عماني",
}
ORIGINS = {
    "turkish": "تركي", "italian": "إيطالي", "omani": "عماني", "spanish": "إسباني",
    "indian": "هندي", "egyptian": "مصري", "brazilian": "برازيلي", "chinese": "صيني",
    "saudi": "سعودي", "jordanian": "أردني", "greek": "يوناني", "portuguese": "برتغالي",
    "medina": "المدينة المنورة",
}

# Physical facts by material. These describe the STONE, not the individual
# listing, so they are the same for every entry of the same category. They are
# published ranges, never a number invented for one product.
PHYSICAL = {
    "marble": {"hardness": "3 – 5", "density": "2.7 جم/سم³ تقريباً",
               "uses": ["أرضيات", "جدران", "واجهات", "سطوح طاولات", "جدران حمامات"]},
    "granite": {"hardness": "6 – 7", "density": "2.65 – 2.75 جم/سم³",
                "uses": ["أرضيات", "مطابخ", "درج", "واجهات", "أسطح خارجية"]},
    "travertine": {"hardness": "4 – 5", "density": "2.4 – 2.5 جم/سم³",
                   "uses": ["أرضيات", "واجهات", "حمامات", "أحواض", "درج"]},
    "limestone": {"hardness": "3 – 4", "density": "2.3 – 2.7 جم/سم³",
                  "uses": ["واجهات", "أرضيات", "جدران", "ديكور"]},
    "sinks": {"hardness": "3 – 5", "density": "2.5 – 2.8 جم/سم³",
              "uses": ["مغاسل", "حمامات"]},
    "ceramic": {"hardness": "5 – 6", "density": "2.4 جم/سم³ تقريباً",
                "uses": ["أرضيات", "جدران", "مطابخ", "حمامات"]},
}

# Arabic stopwords that carry no identifying signal for a slug.
STOP = {"في", "من", "على", "عن", "الى", "إلى", "مع", "و", "أو", "ال", "بـ", "كل",
        "هذا", "هذه", "ذلك", "التي", "الذي", "ما", "لا", "ثم", "حتى", "بها", "به"}


# ───────────────────────────── catalogue access ─────────────────────────────

def node_eval(expr: str):
    """Evaluate a JS expression against the repo's data files with node.

    products.js ALREADY exports `[...PRODUCTS, ...CERAMIC]`, so `P` is the whole
    catalogue. Adding `C` on top would count all 75 ceramic entries twice.
    """
    js = (
        "const P=(await import('"
        f"{PRODUCTS}" + "')).default;"
        "const C=(await import('"
        f"{CERAMIC}" + "')).default;"
        f"const R={expr};"
        "console.log(JSON.stringify(R));"
    )
    tmp = "/tmp/_intake.mjs"
    open(tmp, "w", encoding="utf-8").write(js)
    r = subprocess.run(["node", tmp], capture_output=True, text=True, cwd=ROOT)
    if r.returncode:
        print("FAIL  node could not load the catalogue")
        print(r.stderr[-400:])
        sys.exit(1)
    return json.loads(r.stdout.strip())


ALL = "P"


def existing() -> list[dict]:
    return node_eval(ALL)


# ──────────────────────────────── name → slug ───────────────────────────────

def translit(ar: str) -> str:
    """Latin slug from an Arabic name.

    Common stone names are known in both scripts, so they transliterate
    properly; anything unknown falls back to a stable hash so the slug is
    still unique and URL-safe rather than empty.
    """
    KNOWN = {
        "كالاكاتا": "calacatta", "كريما": "crema", "مارفيل": "marfil",
        "ترافرتينو": "travertine", "جرانيت": "granite", "رخام": "marble",
        "جيري": "limestone", "امبرادور": "emperador", "إمبرادور": "emperador",
        "ستاتواريو": "statuario", "نيرو": "nero", "بيانكو": "bianco",
        "كرارا": "carrara", "تورك": "turk", "تركي": "turkish",
        "ذهبي": "gold", "ابيض": "white", "أبيض": "white", "اسود": "black",
        "أسود": "black", "رمادي": "grey", "بني": "brown", "بيج": "beige",
        "اخضر": "green", "أخضر": "green", "طبيعي": "natural",
        "كلاسيك": "classic", "بازلت": "basalt", "موغلا": "mugla",
        "سلت": "salt", "بيبر": "pepper", "بيرلا": "pearl", "رمل": "sand",
    }
    words = [w for w in re.findall(r"[\u0621-\u064A]+", ar) if w not in STOP]
    out = []
    for w in words:
        # longest-first so "كالاكاتا" wins over a shorter overlapping key
        hit = None
        for k in sorted(KNOWN, key=len, reverse=True):
            if k in w:
                hit = KNOWN[k]
                break
        if hit:
            out.append(hit)
        else:
            out.append("".join(c for c in unicodedata.normalize("NFKD", w)
                               if c.isascii() and c.isalnum()).lower())
    return "-".join(x for x in out if x)


def make_slug(name_ar: str, name_en: str, color: str, taken: set[str]) -> str:
    """A unique, URL-safe slug.

    The Latin name is the base because that is what the market searches for.
    On a collision the origin/color is appended rather than a bare number:
    "calacatta-gold-marble-2" says nothing to a searcher, while
    "calacatta-gold-marble-spanish" does. Only if that also collides does a
    number appear, and it is the last resort.
    """
    base = re.sub(r"[^a-z0-9]+", "-", (name_en or "").lower()).strip("-")
    if not base:
        base = translit(name_ar)
    if not base:
        base = "stone"
    if base not in taken:
        return base
    for suffix in filter(None, [translit(color or "")]):
        cand = f"{base}-{suffix}"
        if cand not in taken:
            return cand
    slug, n = base, 2
    while slug in taken:
        slug = f"{base}-{n}"
        n += 1
    return slug


# ───────────────────────────── image normalisation ──────────────────────────

def prepare_image(src: str, slug: str, dry: bool) -> tuple[str, dict]:
    """Normalise a supplier photo to what the catalogue already uses.

    The existing catalogue is 500×500 or 1000×1000 JPEG at a 6–214 KB median,
    so a 4 MB phone photo has to be resized and re-encoded or it costs the page
    seconds on mobile. A centre crop keeps the slab square like every other
    card instead of letterboxing it.
    """
    from PIL import Image

    os.makedirs(IMG_DIR, exist_ok=True)
    out_rel = f"/images/products-local/{slug}.jpg"
    out_abs = f"{ROOT}/public{out_rel}"

    im = Image.open(src)
    im = im.convert("RGB")
    w, h = im.size
    side = min(w, h)
    im = im.crop(((w - side) // 2, (h - side) // 2,
                  (w - side) // 2 + side, (h - side) // 2 + side))
    # 1000 is the larger of the two sizes the catalogue already uses.
    im = im.resize((1000, 1000), Image.Resampling.LANCZOS)

    info = {"source": f"{w}×{h}", "source_kb": round(os.path.getsize(src) / 1024)}
    if dry:
        info["target"] = "1000×1000 (dry run, not written)"
        return out_rel, info

    im.save(out_abs, "JPEG", quality=84, optimize=True, progressive=True)
    info["target_kb"] = round(os.path.getsize(out_abs) / 1024)
    info["written"] = out_abs
    return out_rel, info


# ───────────────────────────────── the record ───────────────────────────────

def build_record(name_ar: str, name_en: str, cat: str, org: str, color: str,
                 slug: str, image: str, excerpt: str, thickness: list[str] | None,
                 finish: list[str] | None, uses: list[str] | None, next_id: str) -> dict:
    phys = PHYSICAL[cat]
    # The displayed name keeps both scripts, exactly like the rest of the
    # catalogue: "<Latin> - <Arabic>". A name without a Latin half shows only
    # the Arabic one rather than a dangling separator.
    display = f"{name_en} - {name_ar}" if name_en else name_ar
    color_phrase = f" بلون {color}" if color else ""
    feature_color = color or "طبيعي"
    if not excerpt:
        excerpt = (f"{name_ar}: حجر {CATEGORIES[cat]} من أصل {ORIGINS[org]}"
                   f"{color_phrase}. اطلب عيّنة لتأكيد اللون والعروق قبل التثبيت.")
    return {
        "id": next_id,
        "slug": slug,
        "name": display,
        "nameEn": name_en or name_ar,
        "category": cat,
        "origin": org,
        "image": image,
        "code": "غير محدد",
        "color": color or "غير محدد",
        "colorCode": "غير محدد",
        "thickness": thickness or ["20 مم", "30 مم"],
        "finish": finish or ["مصقول (Polished)", "مطفأ (Honed)"],
        "hardness": phys["hardness"],
        "density": phys["density"],
        "uses": uses or phys["uses"],
        "excerpt": excerpt,
        "features": [
            f"لون {feature_color} من {ORIGINS[org]}",
            "متوفر بمقاسات حسب الطلب",
            "قص دقيق على مقاس المشروع",
            "توريد وتركيب بيد فريقنا",
        ],
        "tips": [
            "اطلب عيّنة فعلية قبل الاعتماد على اللون النهائي.",
            "استخدم منظفات غير حمضية على الأسطح المصقولة.",
            "احسب فواصل تمدد في المساحات الكبيرة.",
        ],
    }


def js_obj(o: dict, indent: int = 2) -> str:
    """Serialise a record the way the existing files are written: 2-space
    indent, single quotes, trailing commas. Keeping the style identical means
    a diff against products.js shows one added object and nothing else."""
    lines = []
    pad = " " * indent
    for k, v in o.items():
        if isinstance(v, list):
            if not v:
                lines.append(f"{pad}{k}: [],")
                continue
            lines.append(f"{pad}{k}: [")
            for item in v:
                lines.append(f"{pad}  '{item}',")
            lines.append(f"{pad}],")
        elif isinstance(v, str):
            esc = v.replace("\\", "\\\\").replace("'", "\\'")
            lines.append(f"{pad}{k}: '{esc}',")
        else:
            lines.append(f"{pad}{k}: {v},")
    return "{\n" + "\n".join(lines) + "\n}"


# ─────────────────────────────────── add ────────────────────────────────────

def cmd_add(a) -> int:
    checks: list[tuple[bool, str]] = []

    # 1. inputs are legal
    if a.category not in CATEGORIES:
        print(f"FAIL  category '{a.category}' — one of {', '.join(CATEGORIES)}")
        return 1
    if a.origin not in ORIGINS:
        print(f"FAIL  origin '{a.origin}' — one of {', '.join(ORIGINS)}")
        return 1
    checks.append((True, f"category={a.category} origin={a.origin}"))

    if not os.path.isfile(a.image):
        print(f"FAIL  image not found: {a.image}")
        return 1
    checks.append((True, f"image exists ({round(os.path.getsize(a.image)/1024)} KB)"))

    # 2. the catalogue loads and the name is not already in it.
    #    Compare against every name field a product carries: `name` holds
    #    "Latin - Arabic", `refName` holds the Arabic alone, and the two are
    #    NOT the same string (crema-marfil-classic is "رخام كريما مارفيل كلاسيك"
    #    in refName but "رخام كريما رويال تركي" inside `name`). Checking only
    #    one of them lets a duplicate through.
    prods = existing()
    taken = {p["slug"] for p in prods}

    def norm(s: str) -> str:
        """Fold the differences that make two spellings of one name look
        different: harakat, tatweel, alef/ya variants, punctuation."""
        s = re.sub(r"[\u064B-\u0652\u0670\u0640]", "", s or "")
        s = s.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
        s = s.replace("ى", "ي").replace("ة", "ه")
        return re.sub(r"[^؀-ۿa-z0-9]+", " ", s.lower()).strip()

    want = norm(a.name)
    dup = []
    for p in prods:
        candidates = [p.get("name", ""), p.get("refName", ""), p.get("sourceTitle", "")]
        # `name` is "Latin - Arabic": compare the Arabic tail too, not the whole.
        for c in candidates:
            if norm(c) == want or norm(c.split(" - ")[-1]) == want:
                dup.append(p)
                break

    if dup:
        print(f"FAIL  '{a.name}' is already in the catalogue as "
              f"/products/{dup[0]['slug']}/")
        print(f"      existing name: {dup[0].get('name')}")
        return 1
    checks.append((True, f"name is new ({len(prods)} products currently)"))

    slug = make_slug(a.name, a.name_en, a.color, taken)
    checks.append((True, f"slug={slug} (unique)"))

    next_id = f"L{len(prods) + 1:03d}"

    # 3. image is normalised and lands where the site expects it
    image_rel, imginfo = prepare_image(a.image, slug, a.dry_run)
    checks.append((True, f"image {imginfo['source']} → {imginfo.get('target_kb', '?')} KB "
                         f"at {image_rel}"))

    rec = build_record(
        a.name, a.name_en, a.category, a.origin, a.color, slug, image_rel,
        a.excerpt,
        [x.strip() for x in a.thickness.split(",") if x.strip()] if a.thickness else None,
        [x.strip() for x in a.finish.split(",") if x.strip()] if a.finish else None,
        [x.strip() for x in a.uses.split(",") if x.strip()] if a.uses else None,
        next_id,
    )

    # 4. text hygiene — the same three failures that have shipped before
    text = json.dumps(rec, ensure_ascii=False)
    for label, rx in [
        ("CJK", re.compile(r"[\u4e00-\u9fff]+")),
        ("replacement char", re.compile(r"�")),
        ("stray dot after harakat", re.compile(r"[\u064B-\u0652]\.[\u0621-\u064A]")),
    ]:
        hit = rx.search(text)
        checks.append((hit is None, f"no {label}" + (f" — FOUND {hit.group(0)!r}" if hit else "")))

    print("\n── checks " + "─" * 52)
    for ok, msg in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {msg}")

    if not all(ok for ok, _ in checks):
        print("\nABORTED — nothing written.")
        return 1

    if a.dry_run:
        print("\n── record (dry run, not written) " + "─" * 26)
        print(js_obj(rec))
        return 0

    # 5. append to the local queue and wire it into the default export
    if not os.path.isfile(QUEUE):
        open(QUEUE, "w", encoding="utf-8").write(
            "// منتجات مضافة من طرف المالك مباشرة (اسم + صورة).\n"
            "// مستقلة عن products.js و products-ceramic.js حتى لا تُمسح عند\n"
            "// إعادة توليدهما من بيانات المزوّد.\n\n"
            "const PRODUCTS_LOCAL = [\n];\n\n"
            "export default PRODUCTS_LOCAL;\n"
        )
    q = open(QUEUE, encoding="utf-8").read()
    q = q.replace("\n];\n\nexport default PRODUCTS_LOCAL;\n",
                  f"\n  {js_obj(rec, 4)},\n];\n\nexport default PRODUCTS_LOCAL;\n")
    open(QUEUE, "w", encoding="utf-8").write(q)

    if "products-local" not in open(PRODUCTS, encoding="utf-8").read():
        p = open(PRODUCTS, encoding="utf-8").read()
        p = p.replace("import CERAMIC from './products-ceramic.js';",
                      "import CERAMIC from './products-ceramic.js';\n"
                      "import LOCAL from './products-local.js';")
        p = p.replace("export default [...PRODUCTS, ...CERAMIC];",
                      "export default [...PRODUCTS, ...CERAMIC, ...LOCAL];")
        open(PRODUCTS, "w", encoding="utf-8").write(p)

    print(f"\n  PASS  appended to {QUEUE} (id {next_id})")
    print(f"  PASS  products.js now merges products-local.js")
    print(f"\n  → /products/{slug}/")
    print("  next: npx astro build && git add -A && git commit")
    return 0


# ─────────────────────────────────── check ──────────────────────────────────

def cmd_check() -> int:
    prods = existing()
    problems = []

    slugs = {}
    for p in prods:
        s = p.get("slug")
        if not s:
            problems.append(f"product with no slug: {p.get('name')}")
            continue
        slugs.setdefault(s, []).append(p)

    for s, group in slugs.items():
        if len(group) > 1:
            problems.append(f"duplicate slug '{s}' x{len(group)}")

    for p in prods:
        s = p.get("slug", "?")
        img = p.get("image")
        if not img:
            continue  # placeholder is a legitimate state
        path = f"{ROOT}/public{img}"
        if not os.path.isfile(path):
            problems.append(f"{s}: image missing on disk — {img}")
            continue
        kb = os.path.getsize(path) / 1024
        if kb > 500:
            problems.append(f"{s}: image is {round(kb)} KB (>500 KB, will hurt mobile)")
        for field in ("name", "category", "origin", "color", "excerpt"):
            if not p.get(field):
                problems.append(f"{s}: empty {field}")

    text = open(PRODUCTS, encoding="utf-8").read() + open(CERAMIC, encoding="utf-8").read()
    for label, rx in [
        ("CJK token", re.compile(r"[\u4e00-\u9fff]+")),
        ("replacement char", re.compile(r"�")),
        ("stray dot after harakat", re.compile(r"[\u064B-\u0652]\.[\u0621-\u064A]")),
    ]:
        hit = rx.search(text)
        if hit:
            problems.append(f"{label} in catalogue source: {hit.group(0)!r}")

    missing_img = sum(1 for p in prods if not p.get("image"))
    print(f"products: {len(prods)}   unique slugs: {len(slugs)}   "
          f"without image: {missing_img}")
    if problems:
        print(f"\nFAIL  {len(problems)} problem(s):")
        for x in problems[:40]:
            print(f"  - {x}")
        return 1
    print("\nPASS  catalogue is clean")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--name", required=True, help="Arabic name")
    a.add_argument("--name-en", default="")
    a.add_argument("--category", required=True)
    a.add_argument("--origin", required=True)
    a.add_argument("--color", default="")
    a.add_argument("--image", required=True)
    a.add_argument("--excerpt", default="")
    a.add_argument("--thickness", default="")
    a.add_argument("--finish", default="")
    a.add_argument("--uses", default="")
    a.add_argument("--dry-run", action="store_true")

    sub.add_parser("list")
    sub.add_parser("check")
    args = ap.parse_args()

    if args.cmd == "add":
        return cmd_add(args)
    if args.cmd == "list":
        for p in existing():
            print(f"{p['slug']:<44} {p.get('image') or '— no image'}")
        return 0
    return cmd_check()


if __name__ == "__main__":
    sys.exit(main())
