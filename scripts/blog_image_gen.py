#!/usr/bin/env python3
"""Generate an AI cover image via Sogni AI and register it in the blog image library.

Usage:
    python3 scripts/blog_image_gen.py <slug> "<english prompt>" "<arabic scene>" \
        "kw1,kw2,kw3" [--seed N]

Pipeline: generate via Sogni AI (krea-2-turbo) -> crop to 16:9 1280x720 -> save to
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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMGDIR = ROOT / "public" / "images" / "blog-ai"
LIB = ROOT / "src" / "data" / "blog-images.js"
ADD = ROOT / "scripts" / "blog_image_add.py"

W, H = 1280, 720
# Keep original Sogni output for highest quality; no forced downscale.
GEN_W, GEN_H = None, None
# Quality boosters appended to every prompt.
QUALITY = "sharp focus, high detail, 8k, professional photography, crisp, clear, well-defined, ultra realistic"
# Candidate interpreters, in order. video-studio's venv is first because it
# is the one on this VPS that ships Pillow.
CANDIDATES = [
    "/opt/data/video-studio/.venv/bin/python3",
    os.environ.get("VIRTUAL_ENV", "") + "/bin/python3" if os.environ.get("VIRTUAL_ENV") else "",
]

# Sogni provider path
SOGNI_DIR = Path("/opt/data/projects/sogni")


def ensure_pillow():
    """If PIL is missing, continue without crop; Sogni output is kept as-is."""
    try:
        import PIL  # noqa: F401
        return True
    except ImportError:
        return False


def slug_ok(s):
    return re.fullmatch(r"[a-z0-9][a-z0-9\-]*", s) is not None


def generate_with_sogni(prompt: str, seed: int) -> Path:
    """Generate an image via Sogni AI (krea-2-turbo) and return the local file path."""
    sys.path.insert(0, str(SOGNI_DIR))
    try:
        from sogni_provider import generate_image
    except ImportError as exc:
        raise RuntimeError(f"Sogni provider not available: {exc}") from exc

    tmp = Path("/tmp/hermes_image_gen_sogni")
    tmp.mkdir(parents=True, exist_ok=True)
    dest = tmp / f"sogni_{seed}.png"

    # Do not force a specific resolution; keep Sogni's native output.
    res = generate_image(
        prompt=prompt,
        model="krea-2-turbo",
        title="Cron Generated Image",
        seed=seed,
    )
    if not res.ok or not res.local_path:
        raise RuntimeError(res.error or "Sogni generation failed")

    src = Path(res.local_path)
    if src.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp"):
        shutil.copy2(src, dest)
        return dest

    # Fallback: read bytes and write with proper extension
    data = src.read_bytes()
    dest.write_bytes(data)
    return dest


def crop_1690(path):
    """Centre-crop to exactly 1280x720 and re-encode as JPEG."""
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

    full_prompt = f"{args.prompt}, {QUALITY}"

    print(f"generating {slug} via Sogni krea-2-turbo ...")
    for attempt in range(4):
        try:
            src = generate_with_sogni(full_prompt, args.seed + attempt * 7)
            break
        except Exception as e:
            print(f"  attempt {attempt+1}: {type(e).__name__}: {e}")
            wait = 20 * (attempt + 1)
            print(f"  waiting {wait}s before retry")
            time.sleep(wait)
    else:
        print("ERROR: generation failed after retries", file=sys.stderr)
        sys.exit(1)

    try:
        shutil.copy2(src, dest)
    except Exception as e:
        print(f"WARNING: copy skipped ({e})")
        size = "uncopied"
    else:
        size = f"{dest.stat().st_size // 1024}KB"

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
