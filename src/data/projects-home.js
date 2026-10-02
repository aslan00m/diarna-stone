// أفضل 4 مشاريع تُعرض في الصفحة الرئيسية.
// معيار الاختيار: واجهة مكتملة واضحة (لا لقطة شاشة، لا عينات خام،
// لا أرقام مقاولين) + وجود صفحته الخاصة في /works.
import PROJECTS_FULL from './projects-full.js';

const PICKS = [
  'facade-beige-residence',
  'ornate-classic-facade',
  'residence-stone-glass',
  'neoclassical-facade',
];

export const HOMEPAGE_WORKS = PICKS.map((slug) => {
  const p = PROJECTS_FULL.find((x) => x.slug === slug);
  if (!p) throw new Error(`مشروع غير موجود في قائمة الأعمال: ${slug}`);
  return p;
});

export default HOMEPAGE_WORKS;