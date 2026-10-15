import PRODUCTS from '../data/products.js';
import PROJECTS_FULL from '../data/projects-full.js';
import ABOUT_CARDS from '../data/about-cards.js';
import { CATEGORIES, ORIGINS } from '../data/company.js';
import POSTS from '../data/blog.js';
import STONES from '../data/families.js';
import GALLERY from '../data/sink-gallery.js';

import { BASE } from '../data/urls.js';

export async function GET() {
  const base = ('https://dyarnaa.com' + BASE).replace(/\/$/, '');
  const pages = ['/', '/products', '/products/all', '/services', '/about', '/contact'];
  for (const c of CATEGORIES) pages.push(`/products/${c.slug}`);
  const usedOrigins = new Set(PRODUCTS.map((p) => p.origin));
  for (const o of ORIGINS) if (usedOrigins.has(o.slug)) pages.push(`/origins/${o.slug}`);
  for (const p of PRODUCTS) pages.push(`/products/${p.slug}`);
  for (const pr of PROJECTS_FULL) pages.push(`/works/${pr.slug}`);
  pages.push('/blog', '/consulting', '/sinks', '/installation-external', '/installation-internal', '/works');
  for (const b of POSTS) pages.push(`/blog/${b.slug}`);
  for (const c of ABOUT_CARDS) pages.push(`/about/${c.slug}`);

  // 112 صفحة /stones/ كانت خارج السايت ماب بالكامل. كل صفحة تحمل canonical
  // إلى توأمها في /products/، لكن canonical لا يمنع الفهرسة ولا يعلن الوجود:
  // بلا سايت ماب لا زاحف يعرف أن الصفحة موجودة.
  for (const s of STONES) pages.push(`/stones/${s.slug}`);

  // 37 صفحة /sinks-gallery/ — صور مغاسل حقيقية نفّذناها.
  // صفحة التجميع /sinks-gallery/all مستثناة: لاindex، والسايت ماب لا يسرد
  // صفحات noindex أبداً.
  for (const g of GALLERY) pages.push(`/sinks-gallery/${g.slug}`);

  const urls = pages
    .map((p) => `  <url><loc>${base}${p}</loc></url>`)
    .join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>`;

  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}