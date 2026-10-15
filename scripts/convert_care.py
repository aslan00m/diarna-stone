#!/usr/bin/env python3
"""Salvage the 2 non-duplicate topics from the rate-limited care/prices sibling.

Source: /opt/data/cache/scratch/build_stone/part*.py (8 post-shaped articles).
Six of the eight duplicate primaries already in the bank or published today;
only the three-stone comparison and the marble-countertops buying guide are
new. Converts post shape -> TOPIC_BANK shape and writes topics/batch_care.json.
"""

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/opt/data/projects/diarna-stone")
SRC = Path("/opt/data/cache/scratch/build_stone")
OUT = ROOT / "topics" / "batch_care.json"

# source title fragment -> (id, primary, intent, imagePrompt, imageScene)
PLAN = {
    "الرخام أم الجرانيت أم الترافرتينو": (
        "three-stones-comparison-table",
        "مقارنة الرخام والجرانيت والترافرتينو",
        "commercial",
        "Three stone sample tiles arranged in a row on a workshop table, marble granite and travertine, a technician comparing them, editorial photography",
        "ثلاث عيّنات حجر في صف على طاولة ورشة: رخام وجرانيت وترافرتينو، وفني يقارن بينها",
    ),
    "أسطح مطبخ الرخام": (
        "marble-countertops-buying-guide",
        "أسطح مطبخ الرخام",
        "commercial",
        "A kitchen with a marble countertop and a homeowner choosing edge profile from samples, warm daylight, editorial photography",
        "مطبخ بسطح عمل من الرخام ورب منزل يختار شكل الحافة من عيّنات",
    ),
}


def main():
    items = []
    for i in (1, 2, 3, 4):
        spec = importlib.util.spec_from_file_location("p%d" % i, SRC / f"part{i}.py")
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        items += getattr(m, "PART%d" % i)

    topics = []
    for t in items:
        hit = None
        for frag, plan in PLAN.items():
            if frag in t["title"]:
                hit = plan
                break
        if not hit:
            continue
        tid, primary, intent, prompt, scene = hit
        sections = []
        for s in t.get("sections", []):
            sec = {"h": s.get("title") or "", "p": list(s.get("paragraphs", []))}
            if s.get("table"):
                sec["table"] = s["table"]
            if s.get("bullets"):
                sec["bullets"] = list(s["bullets"])
            if s.get("steps"):
                sec["steps"] = list(s["steps"])
            if s.get("note"):
                sec["note"] = s["note"]
            if s.get("warn"):
                sec["warn"] = s["warn"]
            sections.append(sec)
        topics.append(
            {
                "id": tid,
                "primary": primary,
                "keywords": list(t.get("keywords", [])),
                "intent": intent,
                "title": t["title"],
                "description": t["description"],
                "category": "دليل الشراء",
                "takeawayTitle": "أهم ما في هذا المقال",
                "takeaways": list(t.get("takeaways", [])),
                "ctaHeading": "محتاج مساعدة في اختيار الخامة؟",
                "ctaBody": "فريقنا يراجع استخدامك ويقترح الأنسب ضمن ميزانيتك.",
                "imagePrompt": prompt,
                "imageScene": scene,
                "imageTopics": "مقارنة أحجار, رخام, جرانيت, ترافرتينو, أسطح مطبخ",
                "related": list(t.get("related", [])),
                "sections": sections,
                "faq": list(t.get("faq", [])),
            }
        )

    if len(topics) != 2:
        print(f"ERROR: expected 2 topics, got {len(topics)}")
        return 1

    # leaks
    cjk = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af\u0400-\u04ff]")
    bad = []

    def w(o, p=""):
        if isinstance(o, str):
            if cjk.search(o):
                bad.append((p, o[:60]))
            elif re.search(r"[\u0600-\u06FF]", o):
                s = re.sub(r"\([A-Za-z][A-Za-z\- ]*\)", "", o)
                m = re.search(r"[A-Za-z]{2,}", s)
                if m:
                    bad.append((p, "latin:" + m.group(0) + " :: " + o[:70]))
        elif isinstance(o, list):
            [w(v, p + "[" + str(i) + "]") for i, v in enumerate(o)]
        elif isinstance(o, dict):
            [w(v, p + "." + k) for k, v in o.items()]

    w(topics)
    print("leaks:", len(bad))
    for b in bad:
        print("  ", b)
    if bad:
        return 1

    # related slugs + collisions
    dump = json.loads(
        subprocess.run(
            ["node", "scripts/data_dump.mjs"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        ).stdout
    )
    slugs = {p["slug"] for p in dump["products"]}
    have = {t["id"] for t in dump["topics"]} | {p["slug"] for p in dump["posts"]}
    have_prim = {t["primary"] for t in dump["topics"]}
    for t in topics:
        for r in list(t["related"]):
            if r not in slugs:
                print(f"  dropping invalid related slug {r}")
                t["related"].remove(r)
        if t["id"] in have:
            print("  ID COLLISION:", t["id"])
            return 1
        if t["primary"] in have_prim:
            print("  PRIMARY COLLISION:", t["primary"])
            return 1
        print(
            f"  {t['id']}: {len(t['sections'])} sections, {len(t['faq'])} faq, related={t['related']}"
        )

    OUT.write_text(json.dumps(topics, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
