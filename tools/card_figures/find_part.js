// find_part.js <svg> — list each top-level partID group with its bbox (in viewBox units)
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
(async () => {
  const svgPath = path.resolve(process.argv[2]);
  const b = await puppeteer.launch({ headless: 'new' });
  const pg = await b.newPage();
  await pg.goto('file:///' + svgPath.replace(/\\/g, '/'), { waitUntil: 'load' });
  const out = await pg.evaluate(() => {
    const svg = document.querySelector('svg');
    const vb = svg.getAttribute('viewBox');
    const res = [];
    for (const g of document.querySelectorAll('g[partID]')) {
      let bb;
      try { bb = g.getBBox(); } catch (e) { continue; }
      if (!bb.width) continue;
      res.push({ id: g.getAttribute('partID'), x: Math.round(bb.x), y: Math.round(bb.y), w: Math.round(bb.width), h: Math.round(bb.height) });
    }
    return { viewBox: vb, parts: res };
  });
  await b.close();
  console.log('viewBox:', out.viewBox);
  out.parts.sort((a, b2) => a.w * a.h - b2.w * b2.h).forEach((p) => console.log(`  part ${p.id}: x=${p.x} y=${p.y} w=${p.w} h=${p.h}`));
})();
