#!/usr/bin/env python3
"""One-off: strip the pollinations.ai watermark from every existing blog image.

Every image generated before the crop fix carries the bottom-edge logo. Crops
the same 64px strip blog_image_gen.py now cuts at generation time. Idempotent:
a second run crops nothing new because the height check skips already-cropped
files (656 == 720-64).
"""

import subprocess
import sys
from pathlib import Path

IMGDIR = Path("/opt/data/projects/diarna-stone/public/images/blog-ai")
WATERMARK_PX = 64
PY = "/opt/data/video-studio/.venv/bin/python3"

code = r"""
import sys
from PIL import Image
p = sys.argv[1]
im = Image.open(p).convert("RGB")
w, h = im.size
if h - WATERMARK_PX >= 400:
    im = im.crop((0, 0, w, h - WATERMARK_PX))
    im.save(p, "JPEG", quality=86, optimize=True)
    print("cropped", p.split("/")[-1], (w, h), "->", im.size)
else:
    print("skip (already cropped)", p.split("/")[-1], (w, h))
""".replace("WATERMARK_PX", str(WATERMARK_PX))

n = 0
for f in sorted(IMGDIR.glob("*.jpg")):
    r = subprocess.run([PY, "-c", code, str(f)], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip()[:200])
    if "cropped" in r.stdout:
        n += 1
print(f"\n{n} images cropped, {len(list(IMGDIR.glob('*.jpg')))} total")
sys.exit(0)
