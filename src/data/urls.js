// مسار النشر — يجب أن يطابق `base` في astro.config.mjs
// GitHub Pages: '/diarna-stone/'   |   دومين على الجذر: '/'
export const BASE = '/diarna-stone/';

/** رابط داخلي يحترم مسار النشر. */
export const url = (path = '/') => {
  const b = BASE.replace(/\/$/, '');
  const p = path.startsWith('/') ? path : '/' + path;
  return (b + p) || '/';
};
