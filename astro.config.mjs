import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://aslan00m.github.io',
  // يُنشر تحت مسار المستودع على GitHub Pages. عند الانتقال لدومين
  // على الجذر (Cloudflare Pages مثلاً) غيّر base إلى '/'
  base: '/diarna-stone/',
  output: 'static',
  trailingSlash: 'ignore',
});