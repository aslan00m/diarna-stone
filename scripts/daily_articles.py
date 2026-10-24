#!/usr/bin/env python3
"""Daily article pipeline for dyarnaa.com (diarna-stone).

Publishes 4 SEO articles per day from the topic bank in
src/data/blog-topics.js, each with a generated cover image.

Commands
--------
plan              Pick today's 4 unpublished topics (diverse categories) and
                  print a JSON plan with ready-to-run commands.
author-rules      Print the exact schema + content rules for authoring new
                  topics into the bank.
publish --ids ..  Generate images (if missing), append the topics as posts to
                  src/data/blog.js, build, verify, commit, push, and confirm
                  the live pages. Prints PASS/FAIL per article.
check             Validate blog.js integrity without touching anything.

This script never guesses content: everything it publishes comes from
TOPIC_BANK. A corrupted article (CJK/latin leaks, missing image, invalid
product slug) blocks the publish.
"""

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_JS = ROOT / "src" / "data" / "blog.js"
IMAGE_DIR = ROOT / "public" / "images" / "blog-ai"
IMAGE_LIB = ROOT / "src" / "data" / "blog-images.js"
SITE = "https://dyarnaa.com"

CJK = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]+")
CYRILLIC = re.compile(r"[\u0400-\u04ff]+")
ARABIC = re.compile(r"[\u0600-\u06ff]")
PAREN_LATIN = re.compile(r"\([A-Za-z][A-Za-z\- ]*\)")

# category keyword -> product category (for the "related" products row)
CATEGORY_MAP = [
    ("مغاسل", "sinks"),
    ("أحواض", "sinks"),
    ("واجهات", "travertine"),
    ("ترافرتينو", "travertine"),
    ("جرانيت", "granite"),
    ("رخام", "marble"),
    ("جيري", "limestone"),
    ("حجر طبيعي", "limestone"),
]


def sh(cmd, cwd=ROOT, timeout=300, check=True, env=None):
    r = subprocess.run(
        cmd, cwd=cwd, timeout=timeout, capture_output=True, text=True, env=env
    )
    if check and r.returncode != 0:
        raise RuntimeError(
            f"command failed ({r.returncode}): {' '.join(map(str, cmd))}\n"
            f"{(r.stdout or '')[-2000:]}{(r.stderr or '')[-2000:]}"
        )
    return r


def load_data():
    out = sh(["node", "scripts/data_dump.mjs"], timeout=60).stdout
    data = json.loads(out)
    if not isinstance(data.get("topics"), list):
        raise RuntimeError("TOPIC_BANK is not an array — check blog-topics.js")
    return data


# ---------------------------------------------------------------- validation
def scan_strings(obj, where="", bad=None):
    """Collect every string value with its path."""
    if bad is None:
        bad = []
    if isinstance(obj, str):
        bad.append((where, obj))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan_strings(v, f"{where}[{i}]", bad)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            scan_strings(v, f"{where}.{k}", bad)
    return bad


def leak_report(post):
    """Return a list of corruption problems found in a post object."""
    problems = []
    for path, s in scan_strings(post):
        if (m := CJK.search(s)):
            problems.append(f"CJK token in {path}: {m.group(0)!r}")
        if (m := CYRILLIC.search(s)):
            problems.append(f"Cyrillic in {path}: {m.group(0)!r}")
        if ARABIC.search(s):
            stripped = PAREN_LATIN.sub("", s)
            m = re.search(r"[A-Za-z]{2,}", stripped)
            if m:
                problems.append(f"latin-in-arabic in {path}: {m.group(0)!r}")
    return problems


def structural_report(post, products, existing_slugs):
    problems = []
    if not re.fullmatch(r"[a-z0-9][a-z0-9\-]*", post["slug"]):
        problems.append(f"bad slug: {post['slug']}")
    if post["slug"] in existing_slugs:
        problems.append(f"duplicate slug: {post['slug']}")
    if not post.get("title") or len(post["title"]) < 10:
        problems.append("title too short")
    if not post.get("excerpt") or len(post["excerpt"]) < 60:
        problems.append("excerpt/description too short (need >= 60 chars)")
    secs = post.get("sections") or []
    if len(secs) < 4:
        problems.append(f"only {len(secs)} sections (need >= 4)")
    for s in secs:
        if not s.get("h"):
            problems.append("section without heading")
        if not s.get("p") or len(s["p"]) < 1:
            problems.append(f"section '{s.get('h')}' has no paragraphs")
    faq = post.get("faq") or []
    if len(faqq := faq) < 3:
        problems.append(f"only {len(faqq)} FAQ (need >= 3)")
    for f in faq:
        if not f.get("q") or not f.get("a"):
            problems.append("FAQ without q or a")
    for r in post.get("related") or []:
        if r not in products:
            problems.append(f"related product slug not in catalog: {r}")
    img = ROOT / "public" / (post.get("image") or "").lstrip("/")
    if not post.get("image") or not img.exists():
        problems.append(f"image missing on disk: {post.get('image')}")
    return problems


# ------------------------------------------------------------------ js writer
def js(s):
    return (
        str(s)
        .replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\n", "\\n")
        .replace("\r", "")
    )


def js_list(items, indent):
    pad = " " * indent
    if not items:
        return "[]"
    body = "".join(f"{pad}  '{js(i)}',\n" for i in items)
    return "[\n" + body + pad + "]"


def post_block(p):
    L = []
    L.append("  {")
    L.append(f"    slug: '{js(p['slug'])}',")
    L.append(f"    title: '{js(p['title'])}',")
    L.append(f"    image: '{js(p['image'])}',")
    L.append(f"    imageAlt: '{js(p['imageAlt'])}',")
    L.append(f"    takeaways: {js_list(p['takeaways'], 4)},")
    L.append(f"    excerpt: '{js(p['excerpt'])}',")
    L.append(f"    category: '{js(p['category'])}',")
    L.append(f"    date: '{p['date']}',")
    L.append(f"    readTime: '{js(p['readTime'])}',")
    L.append("    sections: [")
    for s in p["sections"]:
        L.append("      {")
        L.append(f"        h: '{js(s['h'])}',")
        L.append(f"        p: {js_list(s['p'], 8)},")
        if s.get("bullets"):
            L.append(f"        bullets: {js_list(s['bullets'], 8)},")
        if s.get("steps"):
            L.append("        steps: [")
            for st in s["steps"]:
                L.append(
                    f"          ['{js(st[0])}', '{js(st[1])}'],"
                )
            L.append("        ],")
        if s.get("table"):
            L.append("        table: {")
            L.append(f"          head: {js_list(s['table']['head'], 10)},")
            L.append("          rows: [")
            for row in s["table"]["rows"]:
                L.append(f"            {js_list(row, 12)},")
            L.append("          ],")
            L.append("        },")
        if s.get("note"):
            L.append(f"        note: '{js(s['note'])}',")
        if s.get("warn"):
            L.append(f"        warn: '{js(s['warn'])}',")
        L.append("      },")
    L.append("    ],")
    L.append("    faq: [")
    for f in p["faq"]:
        L.append("      {")
        L.append(f"        q: '{js(f['q'])}',")
        L.append(f"        a: '{js(f['a'])}',")
        L.append("      },")
    L.append("    ],")
    L.append(f"    related: {js_list(p['related'], 4)},")
    L.append("  },")
    return "\n".join(L)


# ------------------------------------------------------------------ builders
def word_count(post):
    n = 0
    for s in post.get("sections") or []:
        n += sum(len(x.split()) for x in s.get("p", []))
        n += sum(len(x.split()) for x in s.get("bullets", []))
        n += sum(len(a.split()) + len(b.split()) for a, b in s.get("steps", []))
        t = s.get("table")
        if t:
            n += sum(len(c.split()) for r in t["rows"] for c in r)
    n += sum(len(x.split()) for x in post.get("takeaways", []))
    n += sum(len(f["q"].split()) + len(f["a"].split()) for f in post.get("faq", []))
    return n


def pick_related(topic, products):
    cat = "marble"
    for kw, c in CATEGORY_MAP:
        if kw in topic.get("category", "") or kw in topic.get("primary", ""):
            cat = c
            break
    pool = [p for p in products if p["category"] == cat]
    if not pool:
        pool = [p for p in products if p["category"] == "marble"]
    pool.sort(key=lambda p: -(p.get("featured") or 0))
    return [p["slug"] for p in pool[:3]]


def build_post(topic, today, products):
    words = word_count({"sections": topic["sections"], "takeaways": topic.get("takeaways", []), "faq": topic.get("faq", [])})
    minutes = max(4, round(words / 170))
    excerpt = topic.get("description") or ""
    if len(excerpt) < 60:
        first = topic["sections"][0]["p"][0]
        excerpt = (excerpt + " " + first)[:150].strip()
    return {
        "slug": topic["id"],
        "title": topic["title"],
        "image": f"/images/blog-ai/{topic['id']}.jpg",
        "imageAlt": topic.get("imageScene") or topic["title"],
        "takeaways": topic.get("takeaways") or [],
        "excerpt": excerpt,
        "category": topic.get("category") or "دليل الشراء",
        "date": today,
        "readTime": f"{minutes} دقائق",
        "sections": topic["sections"],
        "faq": topic.get("faq") or [],
        "related": pick_related(topic, products),
    }


def pick_topics(data, n=4):
    published = {p["slug"] for p in data["posts"]}
    unused = [t for t in data["topics"] if t["id"] not in published]
    by_cat = {}
    for t in unused:
        by_cat.setdefault(t.get("category", "?"), []).append(t)
    picks = []
    cats = sorted(by_cat)
    while len(picks) < min(n, len(unused)):
        progressed = False
        for c in cats:
            if len(picks) >= min(n, len(unused)):
                break
            if by_cat[c]:
                picks.append(by_cat[c].pop(0))
                progressed = True
        if not progressed:
            break
    return picks, len(unused)


# ------------------------------------------------------------------ commands
def cmd_plan(args):
    data = load_data()
    picks, bank_unused = pick_topics(data, 4)
    n_need = max(0, 4 - len(picks))
    out = {
        "today": date.today().isoformat(),
        "bank_unused": bank_unused,
        "need_authoring": n_need,
        "picks": [
            {
                "id": t["id"],
                "primary": t.get("primary", ""),
                "title": t.get("title", ""),
                "category": t.get("category", ""),
                "imagePrompt": t.get("imagePrompt", ""),
                "imageScene": t.get("imageScene", ""),
                "imageTopics": t.get("imageTopics", ""),
            }
            for t in picks
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print("\n--- COMMANDS (run exactly, one per line) ---")
    for t in out["picks"]:
        print(
            f"python3 scripts/blog_image_gen.py {t['id']} "
            f"{_q(t['imagePrompt'])} {_q(t['imageScene'])} {_q(t['imageTopics'])}"
        )
    if out["picks"]:
        ids = ",".join(t["id"] for t in out["picks"])
        print(f"python3 scripts/daily_articles.py publish --ids {ids}")
    if n_need:
        print(
            f"AUTHOR {n_need} new topics first: "
            "python3 scripts/daily_articles.py author-rules  (read the rules), "
            "write a JSON array to topics/batch_<date>.json, then: "
            "node scripts/_add_topics.mjs topics/batch_<date>.json "
            "and re-run: python3 scripts/daily_articles.py plan"
        )
    return 0


def _q(s):
    return "'" + str(s).replace("'", "'\\''") + "'"


def cmd_claim(args):
    """Atomically claim ONE unpublished topic for a single-article cron run.

    Four jobs run per day; a lock file + claims ledger guarantees each gets a
    different topic even if they fire at the same moment. A claim expires after
    3 days so a failed publish gets retried instead of being lost forever.
    Prints JSON: {"claimed": <id|null>, ...} on stdout for the cron agent.
    """
    import fcntl

    data = load_data()
    published = {p["slug"] for p in data["posts"]}
    topics_dir = ROOT / "topics"
    topics_dir.mkdir(exist_ok=True)
    lock_path = topics_dir / ".claim.lock"
    claims_path = topics_dir / "claims.json"

    with open(lock_path, "w") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        claims = []
        if claims_path.exists():
            try:
                claims = json.loads(claims_path.read_text(encoding="utf-8"))
            except Exception:
                claims = []
        now = time.time()
        fresh = {c["id"] for c in claims if now - c.get("ts", 0) < 3 * 86400}
        unused = [
            t
            for t in data["topics"]
            if t["id"] not in published and t["id"] not in fresh
        ]
        if not unused:
            print(
                json.dumps(
                    {"claimed": None, "bank_unused": 0, "need_authoring": 1},
                    ensure_ascii=False,
                )
            )
            return 0

        # category rotation: the Nth claim of the day takes the first unused
        # topic from the (N mod K)th category, so the day stays diverse
        cats = sorted({t.get("category", "?") for t in unused})
        n = len(claims)
        pick = None
        for offset in range(len(cats)):
            cat = cats[(n + offset) % len(cats)]
            for t in unused:
                if t.get("category", "?") == cat:
                    pick = t
                    break
            if pick:
                break
        if pick is None:
            pick = unused[0]

        claims.append({"id": pick["id"], "ts": now})
        claims_path.write_text(
            json.dumps(claims, ensure_ascii=False), encoding="utf-8"
        )
        print(
            json.dumps(
                {
                    "claimed": pick["id"],
                    "title": pick.get("title", ""),
                    "primary": pick.get("primary", ""),
                    "category": pick.get("category", ""),
                    "bank_unused": len(unused) - 1,
                    "need_authoring": 0,
                },
                ensure_ascii=False,
            )
        )
    return 0


def cmd_author_rules(args):
    print(
        RULES
    )
    return 0


def cmd_publish(args):
    ids = [i.strip() for i in args.ids.split(",") if i.strip()]
    if not ids:
        print("FAIL: no ids given")
        return 1
    data = load_data()
    topics_by_id = {t["id"]: t for t in data["topics"]}
    published = {p["slug"] for p in data["posts"]}
    products = [p["slug"] for p in data["products"]]
    today = date.today().isoformat()
    report = []

    chosen = []
    for i in ids:
        t = topics_by_id.get(i)
        if not t:
            report.append(("FAIL", i, "topic id not in TOPIC_BANK"))
        elif i in published:
            report.append(("FAIL", i, "already published"))
        else:
            chosen.append(t)
    if not chosen:
        for st, slug, why in report:
            print(f"{st} {slug}: {why}")
        return 1

    # 1) images
    ready = []
    for t in chosen:
        i = t["id"]
        # gate: an Arabic prompt makes the generator produce garbage images
        # (one live article got a random portrait). English only.
        prompt = t.get("imagePrompt", "")
        if re.search(r"[\u0600-\u06ff]", prompt):
            report.append(
                ("FAIL", i, "imagePrompt is Arabic — the generator needs English; fix the topic's imagePrompt and retry")
            )
            continue
        lib_has = IMAGE_LIB.exists() and f"slug: '{i}'" in IMAGE_LIB.read_text(encoding="utf-8")
        dest = IMAGE_DIR / f"{i}.jpg"
        if lib_has and dest.exists():
            print(f"image ok (reused library): {i}")
            ready.append(t)
            continue
        # Image generation moved to the cron agent via Hermes image_generate tool.
        # The agent generates the image and registers it before calling publish.
        if not dest.exists():
            report.append(("FAIL", i, "image not found — agent must generate it with image_generate before publish"))
            continue
    if not ready:
        for st, slug, why in report:
            print(f"{st} {slug}: {why}")
        return 1

    # 2) build post objects + validate BEFORE writing anything
    posts = [build_post(t, today, data["products"]) for t in ready]
    problems = []
    for p in posts:
        for x in leak_report(p):
            problems.append(f"{p['slug']}: {x}")
        for x in structural_report(p, set(products), published):
            problems.append(f"{p['slug']}: {x}")
    if problems:
        print("FAIL: validation blocked the publish:")
        for x in problems:
            print("  -", x)
        print("nothing was written; fix the topics in the bank and retry")
        for st, slug, why in report:
            print(f"{st} {slug}: {why}")
        return 1

    # 3) append to blog.js
    src = BLOG_JS.read_text(encoding="utf-8")
    cut = src.rfind("];")
    if cut < 0:
        print("FAIL: could not find end of POSTS array in blog.js")
        return 1
    block = "\n" + "\n\n".join(post_block(p) for p in posts) + "\n"
    BLOG_JS.write_text(src[:cut] + block + src[cut:], encoding="utf-8")

    # 4) node parse + scans on the file we just wrote
    chk = sh(
        ["node", "--input-type=module", "-e", PARSE_CHECK],
        timeout=60,
        check=False,
    )
    if chk.returncode != 0:
        print("FAIL: blog.js does not parse after append — reverting")
        sh(["git", "checkout", "src/data/blog.js"], check=False)
        print((chk.stdout or "")[-800:] + (chk.stderr or "")[-800:])
        return 1
    print("PASS: blog.js parses, 4 posts appended" if len(posts) == 4 else f"note: {len(posts)} posts appended")

    # 5) build
    print("building site ...")
    b = sh(["npm", "run", "build"], timeout=600, check=False)
    if b.returncode != 0:
        print("FAIL: astro build failed — reverting blog.js")
        sh(["git", "checkout", "src/data/blog.js"], check=False)
        print(((b.stdout or "") + (b.stderr or ""))[-1500:])
        return 1
    print("PASS: build ok")

    # 6) commit + push (owner pushes concurrently — rebase, never force)
    image_files = [f"public/images/blog-ai/{p['slug']}.jpg" for p in posts]
    rc = publish_guarded(image_files=image_files)
    if rc:
        return rc

    # 7) confirm live pages
    print("waiting for GitHub Pages deploy ...")
    time.sleep(45)
    for post in posts:
        url = f"{SITE}/blog/{post['slug']}/"
        ok, why = wait_live(url, post["title"][:24], timeout_s=170)
        report.append(("PASS" if ok else "FAIL", post["slug"], url if ok else why))

    for st, slug, why in report:
        print(f"{st} {slug}: {why}")
    n_fail = sum(1 for st, _, _ in report if st == "FAIL")
    print(f"\nSUMMARY: {len(posts) - n_fail}/{len(posts)} published live")
    return 1 if n_fail else 0


PARSE_CHECK = """
import {POSTS} from './src/data/blog.js';
const bad=[];
const strs=(o,p='')=>{ if(typeof o==='string') bad.push([p,o]);
  else if(Array.isArray(o)) o.forEach((v,i)=>strs(v,p+'['+i+']'));
  else if(o&&typeof o==='object') for(const k in o) strs(o[k],p+'.'+k); };
for(const post of POSTS) strs(post);
const cjk = s => /[\\u4e00-\\u9fff\\u3040-\\u30ff]/.test(s);
const slugset = new Set();
for(const post of POSTS){
  if(slugset.has(post.slug)) throw new Error('duplicate slug '+post.slug);
  slugset.add(post.slug);
  for(const [p,s] of bad){ if(cjk(s)) throw new Error('CJK leak in '+post.slug+' at '+p); }
}
console.log('parse ok, posts:', POSTS.length);
"""


def git(*a, **kw):
    """Run git as the repo's owner identity (the global identity is sharikat)."""
    return sh(
        ["git", "-c", "user.name=aslan00m",
         "-c", "user.email=aslan00m@users.noreply.github.com", *a], **kw
    )


def publish_guarded(image_files=(), extra_files=()):
    """Commit + rebase-push the article, committing ANY leftovers first.

    The bank file (blog-topics.js) is written by the authoring step of the same
    job. If it is left uncommitted, `git pull --rebase` aborts with "You have
    unstaged changes" and no article is pushed. So: commit the article's own
    files, then sweep every remaining modified file into a second commit, then
    rebase and push. Nothing is force-pushed and nothing is dropped.
    """
    files = {"src/data/blog.js", "src/data/blog-images.js", *image_files, *extra_files}
    G = ["git", "-c", "user.name=aslan00m", "-c", "user.email=aslan00m@users.noreply.github.com"]
    sh(G + ["add", *sorted(files)], check=False)
    today = date.today().isoformat()
    c = sh(G + ["commit", "-m",
                f"feat(blog): مقال SEO جديد ({today})" if len(image_files) <= 1
                else f"feat(blog): {len(image_files)} مقالات SEO جديدة ({today})"],
           timeout=120, check=False)
    if c.returncode != 0 and "nothing to commit" not in (c.stdout + c.stderr):
        print("FAIL: commit failed")
        print(((c.stdout or "") + (c.stderr or ""))[-800:])
        return 1

    # sweep leftovers (the topic bank the authoring step just appended to)
    st = sh(["git", "status", "--porcelain"], check=False).stdout or ""
    dirty = [ln[3:].strip().strip('"') for ln in st.splitlines() if ln[3:].strip()]
    if dirty:
        print("note: committing leftover files too: " + ", ".join(dirty))
        sh(G + ["add", "--"] + dirty, check=False)
        s = sh(G + ["commit", "-m", f"chore(blog): تزامن الملفات المعلّقة ({today})"],
               timeout=120, check=False)
        if s.returncode != 0 and "nothing to commit" not in (s.stdout + s.stderr):
            print("FAIL: sweep commit failed")
            print(((s.stdout or "") + (s.stderr or ""))[-800:])
            return 1

    git("fetch", "origin", "main", timeout=180)
    r = git("pull", "--rebase", "origin", "main", timeout=180, check=False)
    if r.returncode != 0:
        print("FAIL: rebase conflict with owner's push — aborting, nothing pushed")
        git("rebase", "--abort", check=False)
        print(((r.stdout or "") + (r.stderr or ""))[-1000:])
        return 1
    pushed = False
    push_out = ""
    for attempt in range(3):
        p = git("push", "origin", "HEAD:main", timeout=180, check=False)
        push_out = f"{p.stdout or ''}{p.stderr or ''}"
        if p.returncode == 0:
            pushed = True
            break
        print(f"push attempt {attempt + 1} failed, retrying in 20s")
        print(push_out[-400:])
        time.sleep(20)
    if not pushed:
        print("FAIL: push failed after 3 attempts")
        print(push_out[-800:])
        return 1
    print("PASS: pushed")
    return 0


def wait_live(url, needle, timeout_s=170):
    deadline = time.time() + timeout_s
    last = ""
    while time.time() < deadline:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                html = r.read().decode("utf-8", "ignore")
                if needle in html:
                    return True, ""
                last = "page 200 but title not found yet"
        except Exception as e:
            last = str(e)
        time.sleep(15)
    return False, f"not live after {timeout_s}s ({last})"


def cmd_check(args):
    data = load_data()
    posts = data["posts"]
    slugs = set()
    products = {p["slug"] for p in data["products"]}
    problems = []
    for p in posts:
        for x in leak_report(p):
            problems.append(f"{p.get('slug')}: {x}")
        for x in structural_report(p, products, slugs):
            problems.append(f"{p.get('slug')}: {x}")
        slugs.add(p.get("slug"))
    if problems:
        print("FAIL")
        for x in problems:
            print("  -", x)
        return 1
    print(f"PASS: {len(posts)} posts, no leaks, no dup slugs, images + related ok")
    return 0


RULES = """\
TOPIC AUTHORING RULES — dyarnaa.com daily bank (src/data/blog-topics.js)

Every topic is a JSON object with EXACTLY these fields (all strings unless noted):

  id            lowercase-hyphen ascii slug, unique across the whole bank
  primary       THE one primary Arabic keyword — never reused by another topic
                or existing post (existing posts cover: رخام vs جرانيت، واجهات
                الترافرتينو، قراءة المواصفات، أخطاء التركيب، الحجر الأبيض في
                الرياض، الحجر البازلتي في المدينة المنورة، الحجر vs السيراميك،
                تقويم صيانة الحجر)
  keywords      6-10 Arabic search keywords (long-tail included)
  intent        informational | commercial | transactional | local
  title         Arabic SEO title, <= 60 chars, contains primary keyword,
                mentions المدينة المنورة when natural
  description   Arabic meta description, 140-160 chars, contains primary keyword
  category      one of: دليل الشراء | الواجهات | المغاسل | التركيب | الصيانة |
                التصميم | المقارنات
  takeaways     4-5 short bolded sentences, each a real actionable fact
  sections      4-8 sections. Each: {h, p: [2-4 real paragraphs],
                optional bullets: [3-5], optional table: {head: [3-5],
                rows: [[...]]}, optional steps: [[label, text]],
                optional note, optional warn}
  faq           3-4 {q, a} — practical answers, 2-3 sentences each
  imagePrompt   English prompt for the AI cover image: an EDITORIAL SCENE
                (workshop, hands, facade detail, design office) — never a
                plain quarry slab/product shot, no text in the image
  imageScene    Arabic description of what the image shows -> becomes alt text
  imageTopics   4-6 comma-separated Arabic topic keywords (for reuse matching)
  related       omit this field — the publisher picks real catalog products
                automatically; hand-written slugs are rejected if wrong

CONTENT RULES (owner's standing rules):
- Site targets المدينة المنورة — write for Medina, Saudi Arabia. Mention it
  where natural. Do NOT write for الرياض.
- Every article must be genuinely useful and specific: real numbers from stone
  properties (mohs hardness, density, thickness in mm), real trade practice.
  No filler, no "في عالم اليوم".
- NEVER invent prices. Talk about cost FACTORS, not amounts.
- Phone 0536089153 appears via the template; don't put contact info in body text.
- Arabic only inside strings. NO CJK, NO Cyrillic, NO latin words inside
  Arabic (a latin mineral name inside ( ) is OK, e.g. "موهس (Mohs)").
- No emoji. No markdown syntax inside strings. Single quotes are escaped by
  the tooling; write normal prose.
- Do not repeat content between topics — each primary keyword is its own article.

Write the batch as a JSON array to topics/batch_<date>.json, then append with:
  node scripts/_add_topics.mjs topics/batch_<date>.json
The script reverts the bank automatically if the result doesn't parse.
"""


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("plan")
    sub.add_parser("claim")
    sub.add_parser("author-rules")
    sub.add_parser("check")
    pp = sub.add_parser("publish")
    pp.add_argument("--ids", required=True)
    args = ap.parse_args()
    return {
        "plan": cmd_plan,
        "claim": cmd_claim,
        "author-rules": cmd_author_rules,
        "publish": cmd_publish,
        "check": cmd_check,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
