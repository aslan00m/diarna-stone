#!/usr/bin/env python3
"""Convert post-shaped sinks articles into TOPIC_BANK shape and append.

Source: /opt/data/cache/scratch/stone_topics_sinks.json (8 complete articles
written in post shape by a rate-limited subagent). The bank needs topic shape:
id, primary, intent, category, imagePrompt, imageScene in addition to the
content. Content itself (sections/faq/takeaways/keywords) is mapped 1:1.

Skips the cleaning/maintenance article - the bank already covers that keyword.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/opt/data/projects/diarna-stone")
SRC = Path("/opt/data/cache/scratch/stone_topics_sinks.json")
OUT = ROOT / "topics" / "batch_sinks2.json"

# index in source -> (new id, primary, intent, imagePrompt, imageScene)
PLAN = {
    0: (
        "marble-basins-buying-guide",
        "مغاسي الرخام",
        "commercial",
        "A customer's hands choosing between two marble vessel sinks in a stone showroom, warm daylight, editorial photography",
        "يد تختار بين مغسلتي رخام في معرض حجر بإضاءة نهارية دافئة",
    ),
    1: (
        "surface-vs-undermount-basins",
        "المغسى السطحية أم المدمجة",
        "commercial",
        "A bathroom counter with an undermount stone basin next to a vessel sink sample, a designer comparing the two, editorial photography",
        "طاولة حمام بمغسلة مدمجة بجانب عيّنة مغسى سطحية أثناء المقارنة",
    ),
    3: (
        "basin-materials-carrara-travertine",
        "مغاسل حجرية من كرارة وترافرتينو وجرانيت",
        "informational",
        "Four stone basin samples of different materials, Carrara marble travertine granite and limestone, arranged on a table, editorial photography",
        "أربع عيّنات مغاسل من خامات مختلفة: رخام كرارة وترافرتينو وجرانيت وحجر جيري",
    ),
    4: (
        "basin-sizes-heights",
        "مقاسات وارتفاعات المغسلة الحجرية",
        "informational",
        "A tape measure beside a stone basin on a bathroom counter showing height and diameter, editorial photography",
        "شريط قياس بجانب مغسلة حجرية على طاولة حمام يظهر الارتفاع والقطر",
    ),
    5: (
        "narrow-bathroom-basins",
        "مغاسل للحمامات الضيقة",
        "informational",
        "A narrow small bathroom with a compact stone basin and a wall-mounted tap, daylight, editorial photography",
        "حمام ضيق بمغسلة حجرية صغيرة وخلاط جداري",
    ),
    6: (
        "basin-installation-steps",
        "تركيب مغسلة حجرية",
        "informational",
        "A plumber's hands fixing a heavy stone basin onto a counter with brackets and silicone, editorial photography",
        "يد تركّب مغسلة حجرية ثقيلة على الطاولة بمساند وسيليكون",
    ),
    7: (
        "basin-price-factors",
        "أسعار المغاسل الحجرية",
        "commercial",
        "A written quotation for stone basins on a desk next to basin samples, editorial photography",
        "عرض سعر مكتوب لمغاسل حجرية على مكتب بجانب عيّنات",
    ),
}


def main():
    src = json.loads(SRC.read_text(encoding="utf-8"))
    topics = []
    for idx, (tid, primary, intent, prompt, scene) in PLAN.items():
        t = src[idx]
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
                "category": "المغاسل",
                "takeawayTitle": "أهم ما في هذا المقال",
                "takeaways": list(t.get("takeaways", [])),
                "ctaHeading": "محتاج مساعدة في اختيار المغسلة؟",
                "ctaBody": "فريقنا يراجع استخدامك ويقترح الأنسب ضمن ميزانيتك.",
                "imagePrompt": prompt,
                "imageScene": scene,
                "imageTopics": "مغاسل حجر, أحواض حمام, رخام, المدينة المنورة, الحمامات",
                "related": list(t.get("related", [])),
                "sections": sections,
                "faq": list(t.get("faq", [])),
            }
        )

    # ---- validation: leaks
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

    # ---- validation: related slugs exist in the catalog
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
    for t in topics:
        for r in t["related"]:
            if r not in slugs:
                print(f"  DROPPING invalid related slug {r} from {t['id']}")
                t["related"].remove(r)

    # ---- collision check vs bank + posts
    have = {t["id"] for t in dump["topics"]} | {p["slug"] for p in dump["posts"]}
    have_prim = {t["primary"] for t in dump["topics"]}
    for t in topics:
        if t["id"] in have:
            print("  ID COLLISION:", t["id"])
        if t["primary"] in have_prim:
            print("  PRIMARY COLLISION:", t["primary"])
    print(
        "shape ok |",
        [f"{t['id']}:{len(t['sections'])}s/{len(t['faq'])}f" for t in topics],
    )
    OUT.write_text(json.dumps(topics, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    sys.exit(main())
