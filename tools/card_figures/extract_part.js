// extract_part.js <svg> <partID> <out.svg> [pad] — pull one Fritzing part group into
// a standalone, tightly-cropped SVG (vector, so it stays crisp at any size).
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
(async () => {
  const [src, partId, out, padArg] = process.argv.slice(2);
  const pad = Number(padArg) || 20;
  const abs = path.resolve(src);
  const b = await puppeteer.launch({ headless: 'new' });
  const pg = await b.newPage();
  await pg.goto('file:///' + abs.replace(/\\/g, '/'), { waitUntil: 'load' });
  const res = await pg.evaluate((pid, pad) => {
    const g = document.querySelector(`g[partID="${pid}"]`);
    if (!g) return null;
    const bb = g.getBBox();
    // include any transform on the group by measuring in root coords
    const svg = document.querySelector('svg');
    const ctm = g.getScreenCTM();
    const inv = svg.getScreenCTM().inverse();
    const pt = (x, y) => { const p = svg.createSVGPoint(); p.x = x; p.y = y; return p.matrixTransform(ctm).matrixTransform(inv); };
    const c = [pt(bb.x, bb.y), pt(bb.x + bb.width, bb.y), pt(bb.x, bb.y + bb.height), pt(bb.x + bb.width, bb.y + bb.height)];
    const xs = c.map((p) => p.x), ys = c.map((p) => p.y);
    const x0 = Math.min(...xs) - pad, y0 = Math.min(...ys) - pad;
    const w = Math.max(...xs) - Math.min(...xs) + pad * 2, h = Math.max(...ys) - Math.min(...ys) + pad * 2;
    // defs may hold gradients/patterns the part references — carry them along
    const defs = [...document.querySelectorAll('svg > defs')].map((d) => d.outerHTML).join('');
    return { markup: g.outerHTML, defs, x0, y0, w, h };
  }, partId, pad);
  await b.close();
  if (!res) { console.error('part not found:', partId); process.exit(1); }
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="${res.x0.toFixed(2)} ${res.y0.toFixed(2)} ${res.w.toFixed(2)} ${res.h.toFixed(2)}">${res.defs}${res.markup}</svg>`;
  fs.writeFileSync(out, svg);
  console.log(`wrote ${out}  viewBox="${res.x0.toFixed(1)} ${res.y0.toFixed(1)} ${res.w.toFixed(1)} ${res.h.toFixed(1)}"  ${(svg.length / 1024).toFixed(1)}KB`);
})();
