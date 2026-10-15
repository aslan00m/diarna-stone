// Structured data builders — one JSON-LD @graph per page.
//
// Every page renders exactly one <script type="application/ld+json"> whose body
// is a @graph: the site-wide Organization/LocalBusiness node is the anchor and
// each page adds its own nodes (Product, Article, BreadcrumbList, FAQPage).
//
// Rules that keep the graph valid:
//   - ids are absolute URLs with a fragment (@id), so nodes reference each other
//     by @id instead of nesting — Google resolves the graph by id.
//   - no invented price, rating or availability. A missing price means the Offer
//     is dropped, never guessed.
//   - Arabic text goes in as-is; JSON.stringify handles the escaping.

import { COMPANY } from './company.js';

const ORG_ID = 'https://dyarnaa.com/#organization';

// City and hours come from company.js — the footer, the contact page and this
// schema all read the same value. Hardcoding a city here is how a site ends up
// telling Google it is in one city and its visitors another.
const CITY = COMPANY.city.split('،')[0].trim();

/** Absolute URL for a path. The site lives at the domain root. */
export const abs = (path) => `https://dyarnaa.com${path.startsWith('/') ? path : `/${path}`}`;

/** The node every page carries. `@id` is what other nodes point at. */
export function organization() {
  return {
    '@type': ['Organization', 'LocalBusiness'],
    '@id': ORG_ID,
    name: 'شركة ديارنا الحديثة',
    alternateName: 'ديارنا الحديثة',
    description:
      'تجارة الرخام والحجر الطبيعي وتركيب الواجهات والأرضيات في الرياض والمملكة العربية السعودية.',
    url: 'https://dyarnaa.com/',
    telephone: '+966536089153',
    email: 'info@diarna.sa',
    areaServed: [
      { '@type': 'City', name: CITY },
      { '@type': 'Country', name: 'المملكة العربية السعودية' },
    ],
    address: {
      '@type': 'PostalAddress',
      addressLocality: CITY,
      addressRegion: CITY,
      addressCountry: 'SA',
    },
    openingHoursSpecification: [
      {
        '@type': 'OpeningHoursSpecification',
        dayOfWeek: ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'],
        opens: '08:00',
        closes: '18:00',
      },
    ],
    priceRange: '$$',
    knowsAbout: [
      'الرخام',
      'الجرانيت',
      'الترافرتينو',
      'الحجر الجيري',
      'تركيب الواجهات الحجرية',
      'المغاسل الحجرية',
    ],
  };
}

/** Homepage only: adds the Website node with SearchAction. */
export function website() {
  return {
    '@type': 'WebSite',
    '@id': 'https://dyarnaa.com/#website',
    url: 'https://dyarnaa.com/',
    name: 'ديارنا الحديثة — رخام وحجر طبيعي',
    inLanguage: 'ar',
    publisher: { '@id': ORG_ID },
  };
}

/**
 * BreadcrumbList from a list of {name, path}. `path` '' is the root and is
 * skipped (the homepage is not a crumb).
 */
export function breadcrumb(trail) {
  return {
    '@type': 'BreadcrumbList',
    '@id': `${abs(trail[trail.length - 1]?.path || '/')}#breadcrumb`,
    itemListElement: trail
      .filter((t) => t.path !== '' && t.path !== '/')
      .map((t, i) => ({
        '@type': 'ListItem',
        position: i + 1,
        name: t.name,
        item: abs(t.path),
      })),
  };
}

/**
 * Product node for a catalog entry.
 *
 * `brand`/`manufacturer`/`countryOfOrigin` come from the product's own origin
 * slug, never guessed. `offers` is emitted only when the caller passes a
 * priceCurrency-bearing object — we publish no figures we do not have.
 */
export function product({ name, description, image, path, category, originName }) {
  const node = {
    '@type': 'Product',
    '@id': `${abs(path)}#product`,
    name,
    description: description || undefined,
    category: category || undefined,
    url: abs(path),
    brand: { '@type': 'Brand', name: 'ديارنا الحديثة' },
    manufacturer: { '@id': ORG_ID },
  };
  if (image) node.image = image.startsWith('http') ? image : abs(image);
  if (originName) node.countryOfOrigin = { '@type': 'Country', name: originName };
  return node;
}

/** Article node for a blog post. `datePublished` is required by the type. */
export function article({ title, description, path, datePublished, dateModified, image, section, wordCount }) {
  const node = {
    '@type': 'Article',
    '@id': `${abs(path)}#article`,
    headline: title,
    description: description || undefined,
    mainEntityOfPage: { '@type': 'WebPage', '@id': abs(path) },
    datePublished,
    dateModified: dateModified || datePublished,
    inLanguage: 'ar',
    author: { '@id': ORG_ID },
    publisher: { '@id': ORG_ID },
    isPartOf: { '@id': 'https://dyarnaa.com/#website' },
  };
  if (image) node.image = image.startsWith('http') ? image : abs(image);
  if (section) node.articleSection = section;
  if (wordCount) node.wordCount = wordCount;
  return node;
}

/**
 * FAQPage node. An empty list returns null — an empty Question array is a
 * rich-result error, not a no-op.
 */
export function faq(items) {
  const qs = (items || [])
    .filter((f) => f && f.q && f.a)
    .map((f) => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a },
    }));
  if (!qs.length) return null;
  return {
    '@type': 'FAQPage',
    '@id': 'https://dyarnaa.com/#faq',
    mainEntity: qs,
  };
}

/**
 * Merge every node into one @graph and serialise it.
 * Duplicate @ids are dropped (the organisation node is added by every caller).
 */
export function graph(nodes) {
  const seen = new Set();
  const list = [];
  for (const n of [organization(), ...(nodes || [])]) {
    if (!n || !n['@id']) continue;
    if (seen.has(n['@id'])) continue;
    seen.add(n['@id']);
    list.push(n);
  }
  return JSON.stringify({ '@context': 'https://schema.org', '@graph': list });
}
