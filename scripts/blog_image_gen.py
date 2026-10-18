#!/usr/bin/env python3
"""Generate an AI cover image and register it in the blog image library.

Usage:
    python3 scripts/blog_image_gen.py <slug> "<english prompt>" "<arabic scene>" \
        "kw1,kw2,kw3" [--seed N]

Pipeline: generate via Pollinations -> crop to 16:9 1280x720 -> save to
public/images/blog-ai/<slug>.jpg -> register in src/data/blog-images.js.

The slug doubles as the library key, so an already-registered slug is never
regenerated — that is what keeps the library free of duplicates.

Why it re-execs: this VPS has several Python installs and only some have
Pillow. The script finds one that does instead of assuming.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / "public" / "images" / "blog-ai"
LIB = ROOT / "src" / "data" / "blog-images.js"
ADD = ROOT / "scripts" / "blog_image_add.py"

W, H = 1280, 720
# Pollinations stamps a small logo along the bottom edge; nologo=true is no
# longer honored, so every image loses this many pixels off the bottom.
WATERMARK_PX = 64
# Flux model = sharper, more detailed output (free, slightly slower).
MODEL = "flux"
# Generate at 2x then downscale = crisper edges than native 1280x720.
GEN_W, GEN_H = 2560, 1440
# Quality boosters appended to every prompt.
QUALITY = "sharp focus, high detail, 8k, professional photography, crisp, clear, well-defined, ultra realistic"
# Candidate interpreters, in order. video-studio's venv is first because it
# is the one on this VPS that ships Pillow.
CANDIDATES = [
    "/opt/data/video-studio/.venv/bin/python3",
    os.environ.get("VIRTUAL_ENV", "") + "/bin/python3" if os.environ.get("VIRTUAL_ENV") else "",
]


def ensure_pillow():
    """If PIL is missing, re-exec this script with an interpreter that has it."""
    try:
        import PIL  # noqa: F401

        return
    except ImportError:
        pass

    me = Path(__file__).resolve()
    for cand in CANDIDATES:
        if not cand or not os.path.isfile(cand):
            continue
        try:
            r = subprocess.run(
                [cand, "-c", "import PIL"],
                capture_output=True,
                timeout=20,
            )
        except Exception:
            continue
        if r.returncode == 0:
            os.execv(cand, [cand, str(me), *sys.argv[1:]])

    print("ERROR: no Python with Pillow found; image will not be cropped", file=sys.stderr)
    sys.exit(3)


def slug_ok(s):
    return re.fullmatch(r"[a-z0-9][a-z0-9\-]*", s) is not None


def fetch(prompt, seed, out_path, attempts=4, timeout=200):
    """Pollinations is free but rate-limits with HTTP 402 and times out.
    Back off, vary the seed, and only accept a file big enough to be an image."""
    for i in range(attempts):
        url = (
            "https://image.pollinations.ai/prompt/"
            + urllib.parse.quote(prompt + ", " + QUALITY)
            + f"?model={MODEL}&width={GEN_W}&height={GEN_H}&seed={seed + i * 7}"
        )
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
            if len(data) < 8000:
                print(f"  attempt {i+1}: too small ({len(data)}B), backing off")
            else:
                out_path.write_bytes(data)
                return True
        except urllib.error.HTTPError as e:
            print(f"  attempt {i+1}: HTTP {e.code} {e.reason}")
        except Exception as e:
            print(f"  attempt {i+1}: {type(e).__name__} {e}")
        # exponential-ish backoff; the 402s clear after a quiet period
        wait = 20 * (i + 1)
        print(f"  waiting {wait}s before retry")
        time.sleep(wait)
    return False


def crop_1690(path):
    """Centre-crop to exactly 1280x720, cut the generator watermark strip,
    and re-encode as JPEG. The watermark is a small logo pinned to the bottom
    edge; Pollinations stopped honoring nologo=true, so the bottom strip is
    cropped on every image rather than trusted."""
    from PIL import Image, ImageEnhance, ImageFilter

    im = Image.open(path).convert("RGB")
    w, h = im.size
    ratio = W / H
    if abs(w / h - ratio) > 0.01:
        if w / h > ratio:
            nw = int(h * ratio)
            box = ((w - nw) // 2, 0, (w - nw) // 2 + nw, h)
        else:
            nh = int(w / ratio)
            box = (0, (h - nh) // 2, w, (h - nh) // 2 + nh)
        im = im.crop(box)
    if im.size != (W, H):
        im = im.resize((W, H), Image.LANCZOS)
    # remove the bottom watermark strip
    im = im.crop((0, 0, W, H - WATERMARK_PX))
    # Sharpen + contrast boost for crisper final output
    im = im.filter(ImageFilter.UnsharpMask(radius=3, percent=120, threshold=1))
    im = ImageEnhance.Contrast(im).enhance(1.15)
    im.save(path, "JPEG", quality=92, optimize=True)
    return im.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("prompt", help="English prompt")
    ap.add_argument("scene", help="Arabic description -> alt text")
    ap.add_argument("topics", help="comma-separated Arabic keywords")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    ensure_pillow()

    slug = args.slug
    if not slug_ok(slug):
        print(f"ERROR: bad slug: {slug}", file=sys.stderr)
        sys.exit(2)

    if LIB.exists() and f"slug: '{slug}'" in LIB.read_text(encoding="utf-8"):
        print(f"ALREADY IN LIBRARY: {slug} — nothing generated")
        sys.exit(0)

    IMGDIR.mkdir(parents=True, exist_ok=True)
    dest = IMGDIR / f"{slug}.jpg"

    print(f"generating {slug} ...")
    if not fetch(args.prompt, args.seed, dest):
        print("ERROR: generation failed after retries", file=sys.stderr)
        sys.exit(1)

    try:
        size = crop_1690(dest)
    except Exception as e:
        print(f"WARNING: crop skipped ({e})")
        size = "uncropped"
    kb = dest.stat().st_size // 1024
    print(f"  saved {size} {kb}KB")

    r = subprocess.run(
        [sys.executable, str(ADD), slug, args.prompt, args.scene, args.topics],
        capture_output=True,
        text=True,
    )
    print(r.stdout.strip() or r.stderr.strip())
    sys.exit(0 if r.returncode == 0 else 1)


if __name__ == "__main__":
    main()
