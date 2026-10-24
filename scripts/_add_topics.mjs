#!/usr/bin/env node
// Append authored topics to the topic bank.
// Usage: node scripts/_add_topics.mjs <batch.json>
// The batch file is an array of topic objects. This keeps the bank editable
// in bulk while guaranteeing the file still parses afterwards.

import { readFileSync, writeFileSync, appendFileSync, existsSync } from 'fs';
import { execFileSync } from 'child_process';

const BANK = 'src/data/blog-topics.js';
const batchPath = process.argv[2];
if (!batchPath) {
  console.error('usage: node _add_topics.mjs <batch.json>');
  process.exit(2);
}

const topics = JSON.parse(readFileSync(batchPath, 'utf8'));
if (!Array.isArray(topics) || !topics.length) {
  console.error('batch must be a non-empty array');
  process.exit(2);
}

// Insert BEFORE the array's closing ], never append after it — the bank is
// one live export and entries outside the brackets break the whole build.
const bankSrc = readFileSync(BANK, 'utf8');
const cut = bankSrc.lastIndexOf('];');
if (cut < 0 || !bankSrc.slice(0, cut).includes('=')) {
  console.error('BANK does not look like `export const TOPIC_BANK = [ ... ];` — aborting');
  process.exit(2);
}

// Two entries with one id means the LAST copy silently wins in publish, so a
// stale shell would be re-claimed later. Refuse instead of stacking a copy.
const existingIds = [...bankSrc.matchAll(/^ {4}id: '([^']+)',$/gm)].map((m) => m[1]);
const clash = [...new Set(topics.map((t) => t.id).filter((id) => existingIds.includes(id)))];
if (clash.length) {
  console.error(`batch ids already in the bank: ${clash.join(', ')}`);
  console.error('remove the existing entry first — a duplicate makes publish take the last copy');
  process.exit(2);
}

const esc = (s) => String(s).replace(/\\/g, '\\\\').replace(/'/g, "\\'");

const block = topics
  .map((t) => {
    const secs = t.sections
      .map((s) => {
        let out = `    {\n      h: '${esc(s.h)}',\n      p: [\n`;
        out += s.p.map((p) => `        '${esc(p)}',`).join('\n') + '\n      ],\n';
        if (s.bullets) {
          out += `      bullets: [\n` + s.bullets.map((b) => `        '${esc(b)}',`).join('\n') + '\n      ],\n';
        }
        if (s.table) {
          out += `      table: {\n        head: [\n` +
            s.table.head.map((h) => `          '${esc(h)}',`).join('\n') + '\n        ],\n        rows: [\n' +
            s.table.rows.map((r) => `          [\n` + r.map((c) => `            '${esc(c)}',`).join('\n') + '\n          ],').join('\n') +
            '\n        ],\n      },\n';
        }
        if (s.steps) {
          out += `      steps: [\n` + s.steps.map((st) => `        ['${esc(st[0])}', '${esc(st[1])}'],`).join('\n') + '\n      ],\n';
        }
        if (s.note) out += `      note: '${esc(s.note)}',\n`;
        if (s.warn) out += `      warn: '${esc(s.warn)}',\n`;
        return out + '    },';
      })
      .join('\n');

    // FAQ schema is {q, a}. Older batch files spelled it {question, answer},
    // and reading .q off those wrote the literal string 'undefined' into the
    // bank — and then into live posts (4 articles shipped it). Normalise both
    // spellings, and refuse an entry that resolves to nothing.
    const faqs = t.faq
      .map((f) => {
        const q = f.q ?? f.question;
        const a = f.a ?? f.answer;
        if (q == null || a == null || String(q) === 'undefined' || String(a) === 'undefined') {
          throw new Error(
            `topic ${t.id}: FAQ entry missing q/a (keys: ${Object.keys(f).join(',')})`
          );
        }
        return `    { q: '${esc(q)}', a: '${esc(a)}' },`;
      })
      .join('\n');

    return `  {
    id: '${esc(t.id)}',
    primary: '${esc(t.primary)}',
    keywords: [${t.keywords.map((k) => `'${esc(k)}'`).join(', ')}],
    intent: '${esc(t.intent || 'informational')}',
    title: '${esc(t.title)}',
    description: '${esc(t.description)}',
    category: '${esc(t.category || 'دليل الشراء')}',
    takeawayTitle: '${esc(t.takeawayTitle || 'أهم ما في هذا المقال')}',
    takeaways: [
${t.takeaways.map((x) => `      '${esc(x)}',`).join('\n')}
    ],
    ctaHeading: '${esc(t.ctaHeading || 'محتاج مساعدة في اختيار الخامة؟')}',
    ctaBody: '${esc(t.ctaBody || 'فريقنا يراجع استخدامك ويقترح الأنسب ضمن ميزانيتك.')}',
    imagePrompt: '${esc(t.imagePrompt)}',
    imageScene: '${esc(t.imageScene)}',
    imageTopics: '${esc(t.imageTopics)}',
    related: [${(t.related || []).map((r) => `'${esc(r)}'`).join(', ')}],
    sections: [
${secs}
    ],
    faq: [
${faqs}
    ],
  },`;
  })
  .join('\n');

writeFileSync(BANK, bankSrc.slice(0, cut) + '\n' + block + '\n' + bankSrc.slice(cut));

// verify
try {
  execFileSync('node', ['--input-type=module', '-e', `import {TOPIC_BANK as T} from './${BANK}'; if(!T.length) throw new Error('empty'); console.log('bank size', T.length);`], { stdio: 'inherit' });
} catch (e) {
  console.error('BROKEN — restoring bank from backup');
  writeFileSync(BANK, bankSrc);
  process.exit(1);
}
