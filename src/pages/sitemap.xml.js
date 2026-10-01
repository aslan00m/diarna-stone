import PRODUCTS from '../data/products.js';
import { CATEGORIES } from '../data/company.js';

export async function GET({ site }) {
  const base = (site?.toString() || 'https://diarna-stone.pages.dev').replace(/\/$/, '');
  const pages = ['/', '/products', '/products/all', '/services', '/about', '/contact'];
  for (const c of CATEGORIES) pages.push(`/products/${c.slug}`);
  for (const p of PRODUCTS) pages.push(`/products/${p.slug}`);

  const urls = pages
    .map((p) => `  <url><loc>${base}${p}</loc></url>`)
    .join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>`;

  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}