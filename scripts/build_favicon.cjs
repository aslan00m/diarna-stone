const sharp = require('/opt/data/projects/diarna-stone/node_modules/sharp');
const path = require('path');

const dir = '/opt/data/projects/diarna-stone/public/favicons';
const svg = path.join(dir, 'favicon.svg');
const svgT = path.join(dir, 'favicon-transparent.svg');

(async () => {
  // PNG versions from the dark-background SVG
  await sharp(svg, { density: 96 }).resize(1024, 1024).png().toFile(path.join(dir, 'favicon-1024.png'));
  await sharp(svg, { density: 96 }).resize(512, 512).png().toFile(path.join(dir, 'favicon-512.png'));
  await sharp(svg, { density: 96 }).resize(48, 48).png().toFile(path.join(dir, 'favicon-48.png'));

  // ICO built separately in Python (see build_ico.py)
  // PNG 48x48 is used as the ICO payload below

  // Transparent PNGs
  await sharp(svgT, { density: 96 }).resize(1024, 1024).png().toFile(path.join(dir, 'favicon-transparent-1024.png'));
  await sharp(svgT, { density: 96 }).resize(512, 512).png().toFile(path.join(dir, 'favicon-transparent-512.png'));
  await sharp(svgT, { density: 96 }).resize(48, 48).png().toFile(path.join(dir, 'favicon-transparent-48.png'));

  // Apple touch icon (180x180, required by Apple)
  await sharp(svg, { density: 96 }).resize(180, 180).png().toFile(path.join(dir, 'apple-touch-icon.png'));

  // Maskable / Android (192, 512)
  await sharp(svg, { density: 96 }).resize(192, 192).png().toFile(path.join(dir, 'favicon-192.png'));
  await sharp(svg, { density: 96 }).resize(512, 512).png().toFile(path.join(dir, 'favicon-512-maskable.png'));

  // Site manifest icon
  await sharp(svg, { density: 96 }).resize(32, 32).png().toFile(path.join(dir, 'favicon-32.png'));
  await sharp(svg, { density: 96 }).resize(16, 16).png().toFile(path.join(dir, 'favicon-16.png'));

  console.log('Done — all favicon formats generated');
})();
