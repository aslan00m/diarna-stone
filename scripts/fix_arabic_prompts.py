#!/usr/bin/env python3
"""One-off: replace the Arabic imagePrompts in the facades batch with English.

Pollinations generates garbage from Arabic prompts (one live article got a
random portrait). The bank rule is English-only; these 8 slipped through from
the subagent batch. Rewrites the imagePrompt line inside each topic block.
"""

import re
import sys
from pathlib import Path

BANK = Path("/opt/data/projects/diarna-stone/src/data/blog-topics.js")

PROMPTS = {
    "stone-facades-complete-selection-guide": "A row of modern villa exteriors with different natural stone cladding styles, granite travertine and limestone facades, soft morning sunlight, wide architectural photography, no people, no text",
    "travertine-facades-design-installation-maintenance": "A close view of a travertine stone facade on a modern house, warm beige tones, sunlight casting soft shadows on the stone texture, architectural photography, no people, no text",
    "facade-slab-thickness-20-30-50mm": "Three natural stone wall panels of different thicknesses standing side by side in a stone workshop, a caliper measuring the panel edge, diffused daylight, editorial photography, no text",
    "facade-fixing-clips-mortar-joints": "A worker installing a stone facade panel with metal clips and anchors on a building wall, close-up of the fixing system and the joint, daylight, editorial photography, no text",
    "stone-facade-annual-maintenance-cleaning": "A worker gently washing a natural stone facade with a soft brush and water from ground level, daylight, editorial photography, no text",
    "granite-vs-travertine-vs-limestone-facades": "Three large facade stone slabs leaning against a wall in a stone yard, grey granite beige travertine and pale limestone, soft daylight, editorial photography, no people, no text",
    "stone-facade-cost-per-meter": "An architect and a homeowner reviewing facade stone samples and a printed elevation drawing on a site office desk, warm daylight, editorial photography, no text",
    "medina-stone-facade-home-designs": "A quiet residential street with villas clad in natural stone, a different facade design per house, warm morning sunlight, wide architectural photography, no people, no text",
}

src = BANK.read_text(encoding="utf-8")
blocks = src.split("\n  {\n")
out = [blocks[0]]
n = 0
for b in blocks[1:]:
    m = re.search(r"id: '([^']+)'", b)
    tid = m.group(1) if m else None
    if tid in PROMPTS:
        b = re.sub(
            r"imagePrompt: '[^']*'",
            "imagePrompt: '" + PROMPTS[tid].replace("'", "\\'") + "'",
            b,
            count=1,
        )
        n += 1
    out.append(b)
BANK.write_text("\n  {\n".join(out), encoding="utf-8")
print(f"rewrote {n} imagePrompts")

# verify: no Arabic prompts remain and the file still parses
sys.exit(0)
