#!/usr/bin/env python3
"""Register a generated image in the AI blog image library.

Usage:
    python3 scripts/blog_image_add.py <slug> "<english prompt>" "<arabic scene>" \
        "kw1,kw2,kw3"

The image file itself must already exist at public/images/blog-ai/<slug>.jpg —
this script only records it, so the library can never reference a file that
was never produced. Use --file to point at a source file elsewhere.

The JS stays valid because the entry is appended as text in the exact shape
the reader in blog_image_match.py expects.
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "src" / "data" / "blog-images.js"
IMGDIR = ROOT / "public" / "images" / "blog-ai"


def js_str(v):
    """Single-quoted JS string literal, matching the library's existing style."""
    return "'" + str(v).replace("\\", "\\\\").replace("'", "\\'") + "'"


def replace_entry(src_js, slug, prompt, scene, topics):
    """Rewrite scene/prompt/topics inside an existing entry block."""
    start = src_js.index(f"slug: '{slug}'")
    # walk back to the opening brace of this entry
    start = src_js.rindex("  {", 0, start)
    end = src_js.index("  },", start) + len("  },")
    block = src_js[start:end]

    def sub(field, value):
        nonlocal block
        pat = re.compile(r"(    %s: ?\[?\n)(?:      [^\n]*\n)+" % field)
        vals = ([value] if field != "topics" else
                [k.strip() for k in value.split(",") if k.strip()])
        new = "".join("      %s,\n" % js_str(v) for v in vals)
        block, n = pat.subn(lambda m: m.group(1) + new, block, count=1)
        if n != 1:
            print(f"WARN: field {field} not found in {slug}", file=sys.stderr)

    sub("scene", scene)
    sub("prompt", prompt)
    sub("topics", topics)
    return src_js[:start] + block + src_js[end:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", help="unique library key, also the filename")
    ap.add_argument("prompt", help="the English prompt that produced the image")
    ap.add_argument("scene", help="Arabic description — becomes the alt text")
    ap.add_argument("topics", help="comma-separated Arabic keywords for matching")
    ap.add_argument("--file", help="copy this file into the library as <slug>.jpg")
    ap.add_argument("--update", action="store_true",
                    help="refresh scene/prompt/topics of an already-registered slug")
    args = ap.parse_args()

    slug = args.slug.strip()
    if not re_ok(slug):
        print(f"ERROR: slug must be lowercase letters, digits and hyphens: {slug}", file=sys.stderr)
        sys.exit(2)

    IMGDIR.mkdir(parents=True, exist_ok=True)
    dest = IMGDIR / f"{slug}.jpg"

    if args.file:
        src = Path(args.file)
        if not src.exists():
            print(f"ERROR: source file not found: {src}", file=sys.stderr)
            sys.exit(2)
        shutil.copy2(src, dest)
        print(f"copied  {src} -> {dest}")

    if not dest.exists():
        print(f"ERROR: no image at {dest} — generate it first, then re-run", file=sys.stderr)
        sys.exit(2)

    src_js = LIB.read_text(encoding="utf-8")
    if f"slug: '{slug}'" in src_js:
        if not args.update:
            print(f"ALREADY REGISTERED: {slug}")
            sys.exit(0)
        src_js = replace_entry(src_js, slug, args.prompt, args.scene, args.topics)
        LIB.write_text(src_js, encoding="utf-8")
        print(f"UPDATED: {slug}")
        sys.exit(0)

    topics = "".join(f"      '{k.strip()}',\n" for k in args.topics.split(",") if k.strip())
    entry = (
        "  {\n"
        f"    slug: '{slug}',\n"
        f"    file: '/images/blog-ai/{slug}.jpg',\n"
        f"    scene:\n"
        f"      '{esc(args.scene)}',\n"
        f"    prompt:\n"
        f"      '{esc(args.prompt)}',\n"
        "    topics: [\n"
        f"{topics}"
        "    ],\n"
        "    usedBy: [''],\n"
        "  },\n"
    )

    marker = "];"
    idx = src_js.rfind(marker)
    if idx < 0:
        print("ERROR: could not find end of BLOG_AI_IMAGES", file=sys.stderr)
        sys.exit(2)
    # insert before the closing bracket of the array
    arr_end = src_js.rfind("  },\n", 0, idx)
    if arr_end < 0:
        print("ERROR: array has no entries to append after", file=sys.stderr)
        sys.exit(2)
    new = src_js[: arr_end + len("  },\n")] + entry + src_js[arr_end + len("  },\n") :]
    LIB.write_text(new, encoding="utf-8")
    print(f"REGISTERED {slug} — library now has {new.count('slug: ')} entries")


def re_ok(slug):
    import re

    return re.fullmatch(r"[a-z0-9][a-z0-9\-]*", slug) is not None


def esc(s):
    """Escape for a single-quoted JS string: backslash then apostrophe."""
    return str(s).replace("\\", "\\\\").replace("'", "\\'")


if __name__ == "__main__":
    main()
