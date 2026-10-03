/* ==========================================================================
   محرّك الحركة — ديارنا الحديثة
   GSAP + ScrollTrigger
   --------------------------------------------------------------------------
   قواعد التصميم:
   1. المحتوى ظاهر بدون JS. الحالات المخفية تُفعَّل بعد تأكيد الجاهزية فقط.
   2. transform و opacity فقط — لا top/left/width/height أبداً (لا إعادة تخطيط).
   3. الحركة المخفّضة = تعطيل كامل، وليس "أبطأ".
   4. الجوال = نسخة أخف (لا scrub ولا pin)، عبر gsap.matchMedia().
   5. أي خطأ في السكربت لا يوقف الموقع — المحتوى يبقى ظاهراً.
   ========================================================================== */

import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

const EASE = 'power3.out';

/* عتبات: متى تبدأ الحركة أثناء التمرير */
const START = 'top 86%';   // سطح المكتب
const START_M = 'top 90%'; // الجوال — نبدأ أبكر لأن التمرير أسرع

const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

const qa = (sel, root = document) => Array.from(root.querySelectorAll(sel));

/* --------------------------------------------------------------------------
   1) الهيرو — تسلسل سينمائي عند فتح الصفحة
      صورة تنكشف، ثم العنوان، ثم النص، ثم الأزرار، ثم النقاط
   -------------------------------------------------------------------------- */
function heroIntro() {
  const hero = document.querySelector('#hero');
  if (!hero) return;

  // GSAP يملك الحالة الابتدائية — لا CSS
  const mask = hero.querySelector('.reveal-mask');
  const lines = qa('.line-reveal > span', hero);
  const eyebrow = hero.querySelector('.hero-body .eyebrow');
  const p = hero.querySelector('.hero-body p');
  const btns = qa('.hero-actions .btn', hero);
  const dots = qa('.hero-dot', hero);
  const slides = qa('.hero-slide', hero);

  if (mask) gsap.set(mask, { clipPath: 'inset(0 0 100% 0)' });
  if (lines.length) gsap.set(lines, { yPercent: 110 });
  if (eyebrow) gsap.set(eyebrow, { y: 14, opacity: 0 });
  if (p) gsap.set(p, { y: 20, opacity: 0 });
  if (btns.length) gsap.set(btns, { y: 16, opacity: 0 });

  const tl = gsap.timeline({
    defaults: { ease: EASE },
    delay: 0.08,
    onComplete() {
      //// الحالة النهائية: نظّف أي inline transform متبقٍنظّف أي inline transform متبقٍ
      gsap.set([mask, ...lines, eyebrow, p, ...btns, ...dots].filter(Boolean),
        { clearProps: 'transform,opacity,clipPath' });
    },
  });

  if (mask) {
    tl.fromTo(mask,
      { clipPath: 'inset(0 0 100% 0)' },
      { clipPath: 'inset(0 0 0% 0)', duration: 1.5, ease: 'power2.inOut' }, 0);
  }

  // تكسر بطيء جدّاً — إحساس سينمائي
  if (slides.length) {
    tl.fromTo(slides,
      { scale: 1.14 },
      { scale: 1.0, duration: 2.6, ease: 'power2.out', stagger: 0.12 }, 0);
  }

  // السطر التعريفي الصغير قبل العنوان
  if (eyebrow) {
    tl.fromTo(eyebrow, { y: 14, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.7, ease: EASE }, 0.22);
  }

  // العنوان: كشف سطر بسطر
  if (lines.length) {
    tl.fromTo(lines,
      { yPercent: 110 },
      { yPercent: 0, duration: 1.15, ease: EASE, stagger: 0.11 }, 0.32);
  } else {
    const h1 = hero.querySelector('h1');
    if (h1) tl.fromTo(h1, { y: 26, opacity: 0 }, { y: 0, opacity: 1, duration: 1.1 }, 0.3);
  }

  // النص بعد العنوان
  if (p) tl.fromTo(p, { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.95 }, 0.55);

  // الأزرار بعد النص
  if (btns.length) {
    tl.fromTo(btns, { y: 16, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, stagger: 0.09 }, 0.75);
  }

  if (dots.length) {
    tl.fromTo(dots, { opacity: 0 }, { opacity: 1, duration: 0.6, stagger: 0.06 }, 1.0);
  }
}

/* --------------------------------------------------------------------------
   2) Parallax — سطح المكتب فقط
      الخلفية تتحرك أبطأ من التمرير بمقدار ضئيل.
   -------------------------------------------------------------------------- */
function parallax(isDesktop) {
  if (!isDesktop) return;

  qa('[data-parallax]').forEach((el) => {
    const speed = parseFloat(el.dataset.parallax) || 0.12;
    const scope = el.closest('section, .hero, [data-parallax-scope]') || el;

    gsap.fromTo(el,
      { yPercent: -speed * 50 },
      {
        yPercent: speed * 50,
        ease: 'none',
        scrollTrigger: {
          trigger: scope,
          start: 'top bottom',
          end: 'bottom top',
          scrub: 0.6,
          invalidateOnRefresh: true,
        },
      });
  });
}

/* --------------------------------------------------------------------------
   3) Image Reveal
      كشف عبر clip-path — أرخص من transform على حاويات كبيرة.
   -------------------------------------------------------------------------- */
function imageReveal(start) {
  qa('[data-anim="reveal"], [data-anim="reveal-r"]').forEach((el) => {
    const mask = el.querySelector('.reveal-mask');
    if (!mask) return;
    const vertical = el.dataset.anim === 'reveal-r';

    gsap.fromTo(mask,
      { clipPath: vertical ? 'inset(100% 0 0 0)' : 'inset(0 0 100% 0)' },
      {
        clipPath: vertical ? 'inset(0% 0 0 0)' : 'inset(0 0 0% 0)',
        duration: 1.25,
        ease: 'power3.inOut',
        onComplete() { gsap.set(mask, { clearProps: 'clipPath' }); },
        scrollTrigger: { trigger: el, start, once: true },
      });

    // تكسر بطيء مصاحب للكشف
    const img = el.querySelector('img');
    if (img) {
      gsap.fromTo(img,
        { scale: 1.12 },
        {
          scale: 1.0,
          duration: 1.5,
          ease: 'power2.out',
          scrollTrigger: { trigger: el, start, once: true },
        });
    }
  });
}

/* --------------------------------------------------------------------------
   4) العناصر المفردة — ستة أنماط مختلفة
      لا نستخدم الحركة نفسها للجميع.
   -------------------------------------------------------------------------- */
const ENTRANCES = {
  up:    { x: 0,   y: 34,  scale: 1,    duration: 0.95 },
  down:  { x: 0,   y: -34, scale: 1,    duration: 0.95 },
  start: { x: 52,  y: 0,   scale: 1,    duration: 1.0 },  // من اليمين في RTL
  end:   { x: -52, y: 0,   scale: 1,    duration: 1.0 },  // من اليسار
  scale: { x: 0,   y: 18,  scale: 0.94, duration: 1.15 },
  fade:  { x: 0,   y: 0,   scale: 1,    duration: 1.3 },
};

function entrances(start) {
  Object.keys(ENTRANCES).forEach((kind) => {
    const cfg = ENTRANCES[kind];
    qa(`[data-anim="${kind}"]`).forEach((el) => {
      gsap.fromTo(el,
        { opacity: 0, x: cfg.x, y: cfg.y, scale: cfg.scale },
        {
          opacity: 1, x: 0, y: 0, scale: 1,
          duration: cfg.duration,
          ease: EASE,
          onComplete() { gsap.set(el, { clearProps: 'transform' }); },
          scrollTrigger: { trigger: el, start, once: true },
        });
    });
  });
}

/* --------------------------------------------------------------------------
   5) Stagger — شبكات البطاقات
   -------------------------------------------------------------------------- */
function stagger(start, isMobile) {
  qa('[data-stagger]').forEach((group) => {
    const items = Array.from(group.children);
    if (!items.length) return;

    gsap.fromTo(items,
      { opacity: 0, y: 30 },
      {
        opacity: 1, y: 0,
        duration: 0.85,
        ease: EASE,
        stagger: isMobile ? 0.06 : 0.1,
        onComplete() { gsap.set(items, { clearProps: 'transform' }); },
        scrollTrigger: { trigger: group, start, once: true },
      });
  });
}

/* --------------------------------------------------------------------------
   6) عدّاد الأرقام — يتحرك عند ظهوره
   -------------------------------------------------------------------------- */
function counters(start, isMobile) {
  qa('[data-count]').forEach((el) => {
    const target = parseFloat(el.dataset.count);
    if (Number.isNaN(target)) return;

    const suffix = el.dataset.suffix || '';
    const obj = { v: 0 };

    gsap.to(obj, {
      v: target,
      duration: isMobile ? 1.4 : 2.0,
      ease: 'power2.out',
      snap: { v: 1 },
      scrollTrigger: { trigger: el, start, once: true },
      onUpdate() { el.textContent = Math.round(obj.v) + suffix; },
    });
  });
}

/* --------------------------------------------------------------------------
   7) Line Reveal — للعناوين المغلّفة
   -------------------------------------------------------------------------- */
function lineReveal(start, isMobile) {
  qa('[data-line-reveal]').forEach((el) => {
    const lines = qa('> span', el);
    if (!lines.length) return;

    gsap.fromTo(lines,
      { yPercent: 110 },
      {
        yPercent: 0,
        duration: isMobile ? 0.9 : 1.05,
        ease: EASE,
        stagger: isMobile ? 0.07 : 0.1,
        onComplete() { gsap.set(lines, { clearProps: 'transform' }); },
        scrollTrigger: { trigger: el, start, once: true },
      });
  });
}

/* --------------------------------------------------------------------------
   Bootstrap
   -------------------------------------------------------------------------- */
function init() {
  const html = document.documentElement;

  // الحركة المخفّضة: لا نفعل شيئاً — كل شيء ظاهر فوراً
  if (reduced) return;

  // الآن فقط نُفعّل الحالات المخفية
  html.classList.add('js-motion');

  // شبكة أمان: إن فشل أي شيء بعد هذه النقطة، نعيد كل العناصر
  // إلى الحالة المرئية بدل تركها مخفية.
  const bail = () => {
    html.classList.remove('js-motion');
    try {
      gsap.set('[data-anim], [data-stagger] > *', { clearProps: 'all' });
    } catch (e) { /* لا شيء */ }
  };

  try {
    gsap.registerPlugin(ScrollTrigger);

    // الهيرو خارج matchMedia عن قصد: تسلسل فتح الصفحة لا يعتمد على
    // حجم الشاشة، وحصره داخل matchMedia يجعله يُعاد (revert) عند أي
    // تغيّر في المقاس — فيعود العنوان محجوباً خلف قناعه.
    if (!document.body.dataset.heroPlayed) {
      document.body.dataset.heroPlayed = '1';
      heroIntro();
    }

    gsap.matchMedia()
      .add({
        isDesktop: '(min-width: 769px)',
        isMobile: '(max-width: 768px)',
      }, (ctx) => {
        const { isMobile } = ctx.conditions;
        const start = isMobile ? START_M : START;

        parallax(!isMobile);
        imageReveal(start);
        entrances(start);
        stagger(start, isMobile);
        counters(start, isMobile);
        lineReveal(start, isMobile);
      });

    ScrollTrigger.refresh();
  } catch (err) {
    bail();
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init, { once: true });
} else {
  init();
}