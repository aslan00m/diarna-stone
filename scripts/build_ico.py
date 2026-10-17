#!/usr/bin/env python3
"""Build a multi-size ICO from PNG files without external deps (PNG-in-ICO)."""
import struct, os

DIR = '/opt/data/projects/diarna-stone/public/favicons'
SIZES = [48, 32, 16]

def png_size(path):
    with open(path, 'rb') as f:
        return os.path.getsize(path)

entries = []
offset = 6 + 16 * len(SIZES)  # header + directory
blobs = []

for sz in SIZES:
    png_path = os.path.join(DIR, f'favicon-{sz}.png')
    with open(png_path, 'rb') as f:
        png = f.read()
    entries.append({
        'width': sz if sz < 256 else 0,
        'height': sz if sz < 256 else 0,
        'size': len(png),
        'offset': offset,
    })
    blobs.append(png)
    offset += len(png)

# ICO header
ico = struct.pack('<HHH', 0, 1, len(SIZES))
# Directory
for e in entries:
    ico += struct.pack('<BBBBHHII',
        e['width'], e['height'], 0, 0,
        1, 32, e['size'], e['offset'])
# Image data
for b in blobs:
    ico += b

out = os.path.join(DIR, 'favicon.ico')
with open(out, 'wb') as f:
    f.write(ico)
print(f'favicon.ico: {len(ico)} bytes, sizes {SIZES}')
