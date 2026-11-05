#!/usr/bin/env python3
"""Auto-refill the dyarnaa.com topic bank after a successful publish.

Usage: python3 auto_refill_bank.py <published_topic_id>

Generates 5 new unique topics and appends them to blog-topics.js.
Ensures no duplicate IDs or imagePrompts.
"""
import json, os, re, sys, subprocess
from datetime import date

ROOT = "/opt/data/projects/diarna-stone"
BANK = os.path.join(ROOT, "src/data/blog-topics.js")
TOPICS_DIR = os.path.join(ROOT, "topics")

POOL = [
    ("stone-terrace-maintenance-medina", "صيانة أرضيات الأفنية الحجرية في المدينة المنورة", "Editorial photo of a stone terrace being maintained, worker with soft brush, warm Medina sunlight, no text", "دليل الصيانة"),
    ("marble-staircase-installation-medina", "تركيب سلالم رخام في المدينة المنورة: دليل التثبيت والسلامة", "Marble staircase installation in progress, Medina villa, precise alignment, professional photography", "دليل تنفيذي"),
    ("granite-cladding-fixing-medina", "تثبيت تكسية جرانيت في المدينة المنورة: أنظمة التثبيت", "Granite cladding being installed on a villa facade, Medina, metal fixing system visible, daylight", "دليل تنفيذي"),
    ("travertine-pool-deck-medina", "أرضيات ترافرتينو حول المسابح في المدينة المنورة: الأمان والجمال", "Travertine pool deck in a Medina villa garden, textured finish, water nearby, warm light", "أفكار وتصميم"),
    ("limestone-facade-cleaning-medina", "تنظيف واجهات حجر جيري في المدينة المنورة: 5 خطوات", "Cleaning limestone facade with soft brush, Medina villa, morning light, no text", "دليل الصيانة"),
    ("stone-bathroom-accent-walls-medina", "جدران حجر accent في حمامات المدينة المنورة: تأثير بصري", "Bathroom accent wall in natural stone, Medina style, warm lighting, modern fixtures", "أفكار وتصميم"),
    ("marble-countertop-sealing-medina", " sealing أسطح رخام في المدينة المنورة: متى وكيف", "Applying sealant to marble countertop, Medina kitchen, close-up detail, professional", "دليل الصيانة"),
    ("granite-flooring-maintenance-medina", "صيانة أرضيات جرانيت في المدينة المنورة: دليل سنوي", "Granite floor maintenance, Medina home, cleaning process, warm light", "دليل الصيانة"),
    ("stone-facade-joint-sealing-medina", "تعبئة فواصل واجهات حجر في المدينة المنورة: مواد وطرق", "Sealing stone facade joints with polyurethane, Medina villa, close-up, professional", "دليل تنفيذي"),
    ("travertine-bathroom-walls-medina", "جدران ترافرتينو في حمامات المدينة المنورة: 6 نصائح", "Travertine bathroom walls, Medina style, warm LED lighting, elegant design", "أفكار وتصميم"),
    ("marble-countertop-stain-removal-medina", "إزالة بقع الرخام في المدينة المنورة: 5 طرق آمنة", "Removing stain from marble countertop, Medina kitchen, gentle cleaning, professional", "دليل الصيانة"),
    ("stone-outdoor-kitchen-medina", "مطابخ خارجية من الحجر في المدينة المنورة: 7 نصائح", "Outdoor stone kitchen in Medina villa garden, granite countertop, warm evening", "أفكار وتصميم"),
    ("granite-step-treads-medina", "درجات جرانيت لسلالم خارجية في المدينة المنورة", "Granite step treads on outdoor staircase, Medina, textured anti-slip surface", "دليل تنفيذي"),
    ("limestone-flooring-maintenance-medina", "صيانة أرضيات حجر جيري في المدينة المنورة: دليل", "Maintaining limestone floor, Medina home, gentle cleaning, warm light", "دليل الصيانة"),
    ("stone-facade-thermal-expansion-medina", "التمدد الحراري في واجهات الحجر: دليل prevent", "Thermal expansion in stone facade, Medina climate, technical illustration", "دليل هندسي"),
]

def load_bank_ids():
    with open(BANK, 'r', encoding='utf-8') as f:
        content = f.read()
    return set(re.findall(r"id: '([^']+)'", content))

def load_bank_prompts():
    with open(BANK, 'r', encoding='utf-8') as f:
        content = f.read()
    return set(re.findall(r"imagePrompt: '([^']+)'", content))

def generate_topics(n=5):
    existing_ids = load_bank_ids()
    existing_prompts = load_bank_prompts()
    new_topics = []
    for suffix, title, prompt, category in POOL:
        if len(new_topics) >= n:
            break
        tid = suffix
        if tid in existing_ids:
            continue
        if prompt in existing_prompts:
            continue
        primary = title.split(" في ")[0] if " في " in title else title
        entry = {
            "id": tid,
            "primary": primary,
            "keywords": [primary],
            "intent": "informational",
            "title": title,
            "description": title + ".",
            "category": category,
            "takeawayTitle": "أهم ما في هذا المقال",
            "takeaways": ["نصيحة 1", "نصيحة 2", "نصيحة 3"],
            "ctaHeading": "محتاج مساعدة؟",
            "ctaBody": "فريقنا يراجع استخدامك ويقترح الأنسب.",
            "imagePrompt": prompt,
            "imageScene": title,
            "imageTopics": primary,
            "related": [],
            "sections": [
                {"h": "مقدمة", "p": [f"مقدمة عن {primary} في المدينة المنورة."]},
                {"h": "التفاصيل", "p": [f"تفاصيل {primary} مع نصائح عملية."]},
                {"h": "الصيانة", "p": ["نصائح صيانة دورية."]},
                {"h": "التكلفة", "p": ["تقدير تكاليف تقريبية."]},
            ],
            "faq": [
                {"q": f"ما هو {primary}؟", "a": f"دليل {primary} في المدينة المنورة."},
                {"q": "كم تكلفة؟", "a": "حسب المساحة والمواد."},
                {"q": "متى أحتاج؟", "a": "حسب المشروع."},
                {"q": "هل أستطيع بنفسي؟", "a": "البعض نعم، والبعض يحتاج متخصص."},
            ],
        }
        new_topics.append(entry)
        existing_ids.add(tid)
        existing_prompts.add(prompt)

    return new_topics

def append_to_bank(topics):
    batch_path = os.path.join(TOPICS_DIR, f"batch_auto_{date.today().isoformat()}.json")
    with open(batch_path, 'w', encoding='utf-8') as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)

    result = subprocess.run(
        ["node", "scripts/_add_topics.mjs", batch_path],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    if result.returncode != 0:
        print("ERROR: _add_topics.mjs failed")
        return False
    return True

def main():
    published_id = sys.argv[1] if len(sys.argv) > 1 else None
    new_topics = generate_topics(5)
    if not new_topics:
        print("No new topics to add (all pool entries already in bank)")
        return
    print(f"Generated {len(new_topics)} new topics:")
    for t in new_topics:
        print(f"  - {t['id']}: {t['title'][:50]}")
    success = append_to_bank(new_topics)
    if success:
        print(f"Successfully added {len(new_topics)} topics to bank")
    else:
        print("FAILED to add topics to bank")

if __name__ == "__main__":
    main()
