import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://www.dyarnaa.com',
  // دومين مخصص على جذر الموقع — لا يوجد مسار فرعي
  base: '/',
  output: 'static',
  trailingSlash: 'ignore',
});