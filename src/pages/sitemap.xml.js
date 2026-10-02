import PRODUCTS from '../data/products.js';
import { CATEGORIES } from '../data/company.js';
import POSTS from '../data/blog.js';

import { BASE } from '../data/urls.js';

export async function GET() {
  const base = ('https://aslan00m.github.io' + BASE).replace(/\/$/, '');
  const pages = ['/', '/products', '/products/all', '/services', '/about', '/contact'];
  for (const c of CATEGORIES) pages.push(`/products/${c.slug}`);
  for (const p of PRODUCTS) pages.push(`/products/${p.slug}`);
  pages.push('/blog', '/consulting', '/sinks', '/installation-external', '/installation-internal');
  for (const b of POSTS) pages.push(`/blog/${b.slug}`);

  const urls = pages
    .map((p) => `  <url><loc>${base}${p}</loc></url>`)
    .join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>`;

  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}