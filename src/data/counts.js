// Single source of truth for how many cards each category page actually renders.
//
// The old counts came from PRODUCTS.filter(category).length, which is no longer what
// any category page shows:
//   - stones are grouped one card per STONE (several grades share one photo), so the
//     page lists ~30 marbles, not the 44 marble products;
//   - sinks are not in STONES at all — the page lists 37 gallery vanities plus 6
//     specification entries, which PRODUCTS alone reports as 6.
//
// Any page that shows a category count must import from here so a number can never
// disagree with the grid below it.
import PRODUCTS from './products.js';
import STONES from './families.js';
import GALLERY from './sink-gallery.js';

const productCount = (slug) => PRODUCTS.filter((p) => p.category === slug).length;
const stoneCount = (slug) => STONES.filter((s) => s.cat === slug).length;

// what /products/<slug> renders: sinks are gallery + spec cards, everything else is stones
export function categoryCardCount(slug) {
  if (slug === 'sinks') return GALLERY.length + productCount('sinks');
  return stoneCount(slug);
}

// what /products/all renders: stones only — the sinks grid is gated to cat === 'sinks'
export const ALL_CARD_COUNT = STONES.length;

export function categoryLabel(slug) {
  const n = categoryCardCount(slug);
  if (slug === 'sinks') return `${GALLERY.length} نموذج · ${productCount('sinks')} مواصفة`;
  return n === 1 ? 'نموذج واحد' : `${n} نموذج`;
}

export const SINK_GALLERY_COUNT = GALLERY.length;
export const SINK_PHOTO_COUNT = GALLERY.reduce((n, g) => n + g.count, 0);

// one real photo per category, for the homepage category grid
export const CATEGORY_COVER = {
  "marble": "/images/products-new/cream-marble.jpg",
  "granite": "/images/products-new/granite-black-white.jpg",
  "travertine": "/images/products-new/golden-travertine.jpg",
  "limestone": "/images/products-new/slate-grey.jpg",
  "sinks": "/images/sinks/white-gold-ceramic-double-vessel-00220bcf.jpg"
};

// نص بديل وصفي لكل غلاف فئة — يصف ما في الصورة فعلاً، وليس اسم الفئة فقط.
// قارئ الشاشة يقرأ هذا النص، ومحركات البحث تفهرس الصورة به.
export const CATEGORY_COVER_ALT = {
  "marble": "لوح رخام كريمي فاتح بعروق بنية ناعمة متفرعة",
  "granite": "جرانيت أبيض وأسود بنقشة ملح وفلفل",
  "travertine": "ترافنتينو ذهبي بعروق أفقية طبيعية",
  "limestone": "حجر جيري رمادي داكن بسطح طبيعي مشقوق",
  "sinks": "مغسلة سيراميك سطحية مزدوجة باللون الأبيض والذهبي"
};
