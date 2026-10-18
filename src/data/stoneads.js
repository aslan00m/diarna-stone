// صفحة الهبوط الإعلانية — dyarnaa.com/stoneads
//
// مصدر واحد للاختيار: هذه الصفحة تسحب حجرها ومغاسلها من الكتالوج نفسه
// (families.js / products.js) بدل تكرار الأسماء والأوصاف. بهذا لا يمكن أن
// تقول الصفحة «رخام» بينما صفحة المنتج تقول «حجر جيري» لنفس السلعة.
//
// قاعدتان ثابتتان هنا:
//   - لا أسعار في أي مكان. أي رقم يُكتب على هذه الصفحة هو رقم مخترع.
//   - لا صورة بلا ملف حقيقي على القرص. الفحص أدناه يطبع FAIL عند أي مسار مفقود.

import PRODUCTS from './products.js';
import FAMILIES from './families.js';

const bySlug = (s) => PRODUCTS.find((p) => p.slug === s);
const byFamily = (s) => FAMILIES.find((f) => f.slug === s);
const join = (arr) => (Array.isArray(arr) && arr.length ? arr.join(' · ') : '');

/**
 * الاسم العربي وحده. سجل الكتالوج يخزّن الاسم بصيغة "Latin - عربي"، فإظهاره
 * كما هو على بطاقة إعلانية يقرأ كخطأ تحريري. إن لم يوجد " - " فالسلسلة عربية
 * أصلاً (حجر الرياض، المجلي) وتؤخذ كاملة.
 */
const arabicName = (s) => (s && s.includes(' - ') ? s.split(' - ').pop().trim() : s || '');

/** بطاقة حجر: من سجل المنتج مباشرة، بلا نص مكتوب يدوياً. */
function stone({ slug, name, cat, origin, color, image, thickness, finish, hardness, density }) {
  const p = bySlug(slug);
  if (!p) throw new Error(`stoneads: product not found: ${slug}`);
  const f = byFamily(slug);
  const spec = (f && f.grades && f.grades[0] && f.grades[0].spec) || {};
  return {
    slug,
    name: arabicName(name || p.name),
    cat: cat || p.category,
    origin: origin || p.origin,
    color: color || p.color || '',
    image: image || p.image,
    thickness: join(thickness || p.thickness || spec.thickness),
    finish: join(finish || p.finish || spec.finish),
    hardness: hardness || p.hardness || spec.hardness || '',
    density: density || p.density || spec.density || '',
  };
}

// ── الواجهات: الحجر الخارجي الفعلي في الكتالوج ────────────────────────────
// حجر الرياض والمجلي من إضافات المالك (products-local) — هي ما يُباع للواجهات
// في السوق المحلي. الترافرتينو والجرانيت بدائل مستوردة نذكرها بلا أرقام.
const FACADE_STONES = [
  stone({ slug: 'riyadh-white-stone', cat: 'limestone', origin: 'saudi' }),
  stone({ slug: 'islamic-fluted-rounded-stone', cat: 'limestone', origin: 'saudi' }),
  stone({ slug: 'masri-megli', cat: 'limestone', origin: 'egyptian' }),
  stone({ slug: 'jordanian-pink-majli', cat: 'limestone', origin: 'jordanian' }),
  stone({ slug: 'roman-travertine-classic', cat: 'travertine', origin: 'italian' }),
  stone({ slug: 'granite-black-white', cat: 'granite', origin: 'saudi' }),
];

// ── المغاسل: ست قطع بمواصفات حقيقية من products.js ────────────────────────
const SINK_SLUGS = [
  'carrara-vessel-sink',
  'calacatta-vessel-sink',
  'nero-assoluto-sink',
  'travertine-bowl-sink',
  'limestone-trough-sink',
  'grey-granite-double-sink',
];
const SINKS = SINK_SLUGS.map((s) => {
  const p = bySlug(s);
  if (!p) throw new Error(`stoneads: sink not found: ${s}`);
  return {
    slug: s,
    name: p.name,
    nameEn: p.nameEn,
    origin: p.origin,
    color: p.color || '',
    image: p.image,
    beforeImage: p.beforeImage,
    thickness: join(p.thickness),
    finish: join(p.finish),
    hardness: p.hardness || '',
    density: p.density || '',
    excerpt: p.excerpt || '',
    features: Array.isArray(p.features) ? p.features : [],
  };
});

export { FACADE_STONES, SINKS, stone };
