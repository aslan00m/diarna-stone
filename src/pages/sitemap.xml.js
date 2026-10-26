import { readFileSync, statSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import PRODUCTS from '../data/products.js';
import PRODUCTS_LOCAL from '../data/products-local.js';
import PROJECTS_FULL from '../data/projects-full.js';
import ABOUT_CARDS from '../data/about-cards.js';
import { CATEGORIES, ORIGINS } from '../data/company.js';
import POSTS from '../data/blog.js';
import STONES from '../data/families.js';
import GALLERY from '../data/sink-gallery.js';

import { BASE } from '../data/urls.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dataDir = join(__dirname, '..', 'data');

/** Date string (YYYY-MM-DD) of the most recently modified data file.
 *  Only changes when the underlying content data actually changes — never
 *  on every build — so lastmod is honest and useful for GSC. */
function lastmodFor(...files) {
  let latest = 0;
  for (const f of files) {
    try {
      const t = statSync(join(dataDir, f)).mtimeMs;
      if (t > latest) latest = t;
    } catch { /* file may not exist */ }
  }
  if (!latest) return new Date().toISOString().split('T')[0];
  return new Date(latest).toISOString().split('T')[0];
}

// Last-modified dates per content source
const DATE_PRODUCTS = lastmodFor('products.js', 'products-local.js', 'products-ceramic.js');
const DATE_STONES   = lastmodFor('families.js');
const DATE_BLOG     = lastmodFor('blog.js', 'blog-topics.js', 'blog-images.js');
const DATE_WORKS    = lastmodFor('projects-full.js');
const DATE_ABOUT    = lastmodFor('about-cards.js', 'company.js');
const DATE_ORIGINS  = lastmodFor('company.js');
const DATE_SINKS    = lastmodFor('sink-gallery.js');
const DATE_STATIC   = lastmodFor('../../astro.config.mjs', '../../src/pages/index.astro', '../../src/pages/services.astro', '../../src/pages/about.astro', '../../src/pages/contact.astro', '../../src/pages/stoneads.astro', '../../src/pages/sinks.astro', '../../src/pages/consulting.astro', '../../src/layouts/Base.astro');

/** Ensure a page path ends with exactly one trailing slash (root stays "/"). */
function withSlash(p) {
  if (p === '/' || p === '') return '/';
  return p.endsWith('/') ? p : `${p}/`;
}

// Build the list of [path, lastmod, priority, changefreq] tuples.
const entries = [];

// Static core pages
for (const p of ['/', '/products', '/products/all', '/services', '/about', '/contact',
                 '/blog', '/consulting', '/sinks', '/installation-external',
                 '/installation-internal', '/works', '/stoneads']) {
  entries.push([withSlash(p), DATE_STATIC, p === '/' ? 1.0 : 0.8, 'weekly']);
}

// Category landing pages
for (const c of CATEGORIES) entries.push([`/products/${c.slug}/`, DATE_PRODUCTS, 0.8, 'weekly']);

// Origin pages
const usedOrigins = new Set(PRODUCTS.map((p) => p.origin));
for (const o of ORIGINS) if (usedOrigins.has(o.slug)) entries.push([`/origins/${o.slug}/`, DATE_ORIGINS, 0.7, 'monthly']);

// Individual products
for (const p of PRODUCTS) entries.push([`/products/${p.slug}/`, DATE_PRODUCTS, 0.9, 'weekly']);
for (const p of PRODUCTS_LOCAL) entries.push([`/products/${p.slug}/`, DATE_PRODUCTS, 0.8, 'monthly']);

// Works / projects
for (const pr of PROJECTS_FULL) entries.push([`/works/${pr.slug}/`, DATE_WORKS, 0.8, 'monthly']);

// About cards
for (const c of ABOUT_CARDS) entries.push([`/about/${c.slug}/`, DATE_ABOUT, 0.7, 'monthly']);

// Blog posts
for (const b of POSTS) entries.push([`/blog/${b.slug}/`, DATE_BLOG, 0.8, 'weekly']);

// Sinks gallery (only individual sink pages — /sinks-gallery/all is noindex and excluded)
for (const g of GALLERY) entries.push([`/sinks-gallery/${g.slug}/`, DATE_SINKS, 0.7, 'monthly']);

// Stone family pages — ONLY stones that actually have a page (multi: true).
// The [slug].astro page only prerenders stones with multi === true, so every
// other stone would be a 404. Including only multi:true avoids dead URLs.
// All stone pages canonical to their /products/ twin, so priority is low.
for (const s of STONES.filter((s) => s.multi)) entries.push([`/stones/${s.slug}/`, DATE_STONES, 0.5, 'monthly']);

const base = ('https://dyarnaa.com' + BASE).replace(/\/$/, '');

const urls = entries
  .map(([path, lm, prio, freq]) =>
    `  <url><loc>${base}${path}</loc><lastmod>${lm}</lastmod><changefreq>${freq}</changefreq><priority>${prio}</priority></url>`
  )
  .join('\n');

const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/0.9">\n${urls}\n</urlset>`;

export async function GET() {
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
}
