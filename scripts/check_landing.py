#!/usr/bin/env python3
"""فحص صفحة الهبوط /stoneads قبل أي تأكيد.

يفحص ثلاث طبقات ويطبع PASS/FAIL:
  1. البيانات — كل حجر ومغسلة مسجّلة في الكتالوج، وكل صورة لها ملف حقيقي.
  2. البناء — astro build ينجح والصفحة موجودة في dist.
  3. الحية — dyarnaa.com/stoneads ترجع 200 وتحتوي العنوان والهيرو.

أي FAIL يمنع التأكيد. لا يوجد وضع «ناشر رغم الأخطاء».
"""
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE = "https://dyarnaa.com/stoneads"
ARTICLE_CSS = ROOT / "src/styles/article.css"

fails, passes = [], []


def check(name, ok, detail=""):
    (passes if ok else fails).append(name)
    print(("PASS " if ok else "FAIL ") + name + (("  — " + detail) if detail else ""))


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "hermes-landing-check"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


# ── 1. البيانات ──────────────────────────────────────────────────────────
def check_data():
    node = subprocess.run(
        ["node", "--input-type=module", "-e", """
import { FACADE_STONES, SINKS } from './src/data/stoneads.js';
import PRODUCTS from './src/data/products.js';
import FAMILIES from './src/data/families.js';
const slugs = new Set(PRODUCTS.map(p => p.slug));
const fams = new Set(FAMILIES.map(f => f.slug));
const bad = [];
for (const s of FACADE_STONES) {
  if (!slugs.has(s.slug)) bad.push('stone not in catalog: ' + s.slug);
  if (!s.thickness) bad.push('no thickness: ' + s.slug);
  if (!s.hardness) bad.push('no hardness: ' + s.slug);
}
for (const s of SINKS) {
  if (!slugs.has(s.slug)) bad.push('sink not in catalog: ' + s.slug);
  if (!s.thickness) bad.push('no thickness: ' + s.slug);
}
if (FACADE_STONES.length !== 6) bad.push('facade stones = ' + FACADE_STONES.length);
if (SINKS.length !== 6) bad.push('sinks = ' + SINKS.length);
const json = { bad, stones: FACADE_STONES, sinks: SINKS };
console.log(JSON.stringify(json));
"""],
        cwd=ROOT, capture_output=True, text=True,
    )
    if node.returncode != 0:
        check("data: stoneads.js loads", False, node.stderr.strip()[:300])
        return
    out = json.loads(node.stdout.strip().splitlines()[-1])
    check("data: stoneads.js loads", True)

    for b in out["bad"]:
        check(f"data: {b}", False)
    check("data: كل الأصناف في الكتالوج ولها مواصفات", not out["bad"])

    missing = []
    for s in out["stones"] + out["sinks"]:
        for key in ("image", "beforeImage"):
            img = s.get(key)
            if img and not (ROOT / "public" / img.lstrip("/")).is_file():
                missing.append(f"{s['slug']}:{img}")
    check("data: كل الصور لها ملف على القرص", not missing, ", ".join(missing))

    # لا سعر مكتوب في ملف البيانات
    src = (ROOT / "src/data/stoneads.js").read_text(encoding="utf-8")
    price_words = re.findall(r"(ريال|سعر\s*[:=]\s*['\"]?\d|\bprice\b)", src)
    check("data: لا سعر في بيانات الصفحة", not price_words, str(price_words[:5]))


# ── 2. البناء ────────────────────────────────────────────────────────────
def check_build():
    build = subprocess.run(["npm", "run", "build"], cwd=ROOT, capture_output=True, text=True)
    check("build: astro build", build.returncode == 0, build.stderr.strip()[-400:])
    page = ROOT / "dist/stoneads/index.html"
    check("build: الصفحة مبنية", page.is_file(), str(page))
    return page.read_text(encoding="utf-8") if page.is_file() else ""


# ── 3. المحتوى المبني ─────────────────────────────────────────────────────
def check_html(html):
    if not html:
        return
    text = re.sub(r"<[^>]+>", " ", html)

    # تسرّب CJK/لاتيني داخل نص عربي
    cjk = re.findall(r"[\u4e00-\u9fff\u3040-\u30ff]+", text)
    check("html: لا تسرّب CJK", not cjk, str(cjk[:5]))

    # أخطاء نحوية لاتينية ملتصقة بالعربي (已知 نمط التلف المعتاد)
    leeks = re.findall(r"[A-Za-z]{2,}(?:[\u0600-\u06FF]+[A-Za-z]+)+", text)
    check("html: لا لاتيني ملتصق بالعربي", not leeks, str(leaks[:5]) if (leaks := leeks) else "")

    for needle in ["بيع الحجر وتركيب الواجهات والمغاسل", "حجر الواجهات المتوفر", "المغاسل الحجرية", "wa.me/966536089153"]:
        check(f"html: يحتوي «{needle}»", needle in html)

    # canonical مطلق وصحيح
    canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    check("html: canonical مطلق", bool(canon) and canon.group(1).startswith("http"), canon.group(1) if canon else "")

    # JSON-LD صحيح
    ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    ok_ld = False
    for block in ld:
        try:
            d = json.loads(block)
            ok_ld = ok_ld or "@graph" in d
        except Exception as e:
            check("html: JSON-LD يتحلل", False, str(e)[:150])
    check("html: JSON-LD صحيح", ok_ld)

    # لا noindex — صفحة إعلانية يجب أن تُفهرس
    check("html: مفهرسة (لا noindex)", "noindex" not in html)

    # كل الصور المطلوبة لها ملف — نفحص فعلياً على القرص
    imgs = set(re.findall(r'src="(/images/[^"]+)"', html))
    missing = [i for i in imgs if not (ROOT / "public" / i.lstrip("/")).is_file()]
    check(f"html: {len(imgs)} صورة كلها موجودة على القرص", not missing, ", ".join(missing[:6]))

    # كل الروابط الداخلية لصفحات موجودة في الموقع (لا placeholders)
    hrefs = set(re.findall(r'href="(/[^"]*)"', html))
    hrefs = {h for h in hrefs if not h.startswith(("/fonts", "/images", "/favicon", "/apple-touch", "/_astro"))}
    missing_pages = [h for h in hrefs if not (ROOT / "dist" / h.lstrip("/") / "index.html").is_file()
                     and not (ROOT / "dist" / (h.lstrip("/") + ".html")).is_file()]
    check(f"html: {len(hrefs)} رابطاً داخلياً كلها صفحات مبنية", not missing_pages, ", ".join(sorted(missing_pages)[:6]))


# ── 4. الصفحة الحية ───────────────────────────────────────────────────────
def check_live():
    try:
        status, body = get(LIVE)
        check("live: الصفحة ترجع 200", status == 200, str(status))
    except Exception as e:
        check("live: الصفحة ترجع 200", False, str(e)[:200])
        return
    for needle in ["بيع الحجر وتركيب الواجهات والمغاسل", "حجر الواجهات المتوفر", "wa.me/966536089153"]:
        check(f"live: يحتوي «{needle}»", needle in body)


if __name__ == "__main__":
    print("=== فحص صفحة الهبوط /stoneads ===\n")
    check_data()
    print()
    html = check_build()
    print()
    check_html(html)
    print()
    check_live()
    print(f"\n{passes.__len__()} PASS / {fails.__len__()} FAIL")
    if fails:
        print("\nمرفوض:")
        for f in fails:
            print("  - " + f)
    sys.exit(1 if fails else 0)
