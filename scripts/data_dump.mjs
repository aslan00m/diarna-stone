#!/usr/bin/env node
// Dump blog data as JSON for the Python pipeline.
// Usage: node scripts/data_dump.mjs
import POSTS from '../src/data/blog.js';
import { TOPIC_BANK } from '../src/data/blog-topics.js';
import PRODUCTS from '../src/data/products.js';

console.log(
  JSON.stringify({
    posts: POSTS,
    topics: TOPIC_BANK,
    products: PRODUCTS.map((p) => ({
      slug: p.slug,
      category: p.category,
      featured: p.featured || 0,
      refName: p.refName || '',
    })),
  })
);
