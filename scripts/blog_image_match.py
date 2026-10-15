#!/usr/bin/env python3
"""Match a blog article to the AI image library.

The library lives in src/data/blog-images.js. Every entry carries `topics` —
the words an article is matched against. This script is the single decision
point for article covers:

    python3 scripts/blog_image_match.py "اختيار الحجر"            # match only
    python3 scripts/blog_image_match.py "اختيار الحجر" --generate # generate if no match

Exit codes:
    0  a match was found in the library (prints its slug, file, alt)
    1  no match — caller must generate, then re-register
    2  usage / library error

The library is edited ONLY through scripts/blog_image_add.py so the JS stays
valid and every image is registered exactly once.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "src" / "data" / "blog-images.js"
IMGDIR = ROOT / "public" / "images" / "blog-ai"


def load_library():
    """Parse the JS file with a tolerant regex reader — no Node needed."""
    if not LIB.exists():
        print(f"ERROR: library not found: {LIB}", file=sys.stderr)
        sys.exit(2)
    src = LIB.read_text(encoding="utf-8")
    entries = []
    # each entry starts with `{` and ends with `},` inside BLOG_AI_IMAGES
    block = src.split("export const BLOG_AI_IMAGES = [", 1)
    if len(block) < 2:
        print("ERROR: BLOG_AI_IMAGES not found", file=sys.stderr)
        sys.exit(2)
    body = block[1].split("];", 1)[0]
    for raw in re.findall(r"\{(.*?)\n  \},", body, re.S):
        def field(name):
            m = re.search(rf"{name}:\s*'([^']*)'", raw)
            if m:
                return m.group(1)
            m = re.search(rf'{name}:\s*"([^"]*)"', raw)
            return m.group(1) if m else ""
        def arr(name):
            m = re.search(rf"{name}:\s*\[(.*?)\]", raw, re.S)
            if not m:
                return []
            return [s.strip().strip("'\"") for s in m.group(1).split(",") if s.strip()]
        entries.append(
            {
                "slug": field("slug"),
                "file": field("file"),
                "scene": field("scene"),
                "prompt": field("prompt"),
                "topics": arr("topics"),
                "usedBy": arr("usedBy"),
            }
        )
    return entries


def score(entry, text):
    """How well an entry fits the text. Topic keyword hits dominate; the
    scene text is a weaker signal so a matching topic always wins."""
    t = text.lower()
    hits = sum(1 for k in entry["topics"] if k.lower() in t)
    scene_hits = sum(1 for w in entry["scene"].split() if len(w) > 4 and w in text)
    return hits * 10 + scene_hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("title", help="article title or topic (Arabic or English)")
    ap.add_argument("--generate", action="store_true", help="report that generation is needed")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    lib = load_library()
    if not lib:
        print("ERROR: library is empty", file=sys.stderr)
        sys.exit(2)

    ranked = sorted(lib, key=lambda e: score(e, args.title), reverse=True)
    best = ranked[0]
    s = score(best, args.title)

    if s > 0:
        out = {
            "match": True,
            "slug": best["slug"],
            "file": best["file"],
            "alt": best["scene"],
            "score": s,
            "exists": (ROOT / "public" / best["file"].lstrip("/")).exists(),
        }
    else:
        out = {"match": False, "score": 0, "generate": bool(args.generate)}

    if args.json:
        print(json.dumps(out, ensure_ascii=False))
    else:
        if out["match"]:
            print(f"REUSE  {out['slug']}")
            print(f"file   {out['file']}{'' if out['exists'] else '  <-- FILE MISSING'}")
            print(f"alt    {out['alt']}")
        else:
            print("NO MATCH — generate a new image and register it")
            print(f"library size: {len(lib)}")

    sys.exit(0 if out["match"] else 1)


if __name__ == "__main__":
    main()
