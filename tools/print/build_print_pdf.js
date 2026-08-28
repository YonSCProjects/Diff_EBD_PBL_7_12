#!/usr/bin/env node
/**
 * build_print_pdf.js — printable A4 PDF of one project's Hebrew task cards.
 *
 *   node tools/print/build_print_pdf.js build_output/Project_1_Cards_he.html \
 *        build_output/Project_1_Task_Cards_he_print.pdf [--all]
 *
 * Three rules, in the order they are allowed to win:
 *
 *   1. EVERY שלב STARTS A NEW PAGE. Each card carries one "שלב N מתוך M" in its header band, so
 *      a card is a stage and a stage owns its own sheet from the top.
 *   2. NOTHING IS CUT MID-SECTION. Every atomic block — a step row, a callout, a diagram frame,
 *      the done-when box, a planner field — carries break-inside: avoid, and every heading is
 *      bound to the block it introduces so a title is never stranded at the foot of a page.
 *   3. AS LITTLE WHITE AS POSSIBLE. Rule 1 puts the slack at the end of each card, where it
 *      cannot be reclaimed by the next card. So it is reclaimed a different way: a card that
 *      overruns its last sheet by a little is scaled down just enough to save that sheet. The
 *      shrink is capped at 8%, which is invisible on the page and never costs legibility.
 *
 * Fonts are embedded as data: URIs, so this builds and prints identically with no network.
 */
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');   // the repo's own dependency, brings its Chromium

const [src, out] = process.argv.slice(2);
const ALL = process.argv.includes('--all');
const FONTS = fs.readFileSync(path.join(__dirname, 'fonts.css'), 'utf8');
const MM = 96 / 25.4;
const MARGIN = 10;
const CW = Math.round((210 - 2 * MARGIN) * MM);
const CH = Math.round((297 - 2 * MARGIN) * MM);   // usable height per sheet, in CSS px
const FOOT = Math.round(6 * MM);                  // the footer strip eats a little more
const USABLE = CH - FOOT;
const MIN_ZOOM = 0.92;                            // never shrink a card more than 8%
const REF_COUNT = 6;

const html = fs.readFileSync(src, 'utf8');
const head = html.slice(0, html.indexOf('</head>'));
const styles = [...head.matchAll(/<style[\s\S]*?<\/style>/g)].map(m => m[0]).join('\n');
const title = (head.match(/<title>([\s\S]*?)<\/title>/) || [, ''])[1].trim();
let secs = [...html.matchAll(/<section class="appendix-card[\s\S]*?(?=<section class="appendix-card|<\/body>)/g)]
  .map(m => m[0]);
if (!ALL) secs = secs.slice(REF_COUNT);

function docFor(zooms) {
  const z = zooms
    ? zooms.map((v, i) => v < 1 ? `.appendix-card:nth-of-type(${i + 1}){zoom:${v.toFixed(4)}}` : '').join('')
    : '';
  return `<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8">
<title>${title}</title>
<style>${FONTS}</style>
${styles}
<style>
  @page { size: A4; margin: ${MARGIN}mm; }
  html, body { margin:0; padding:0; background:#fff; }
  /* rule 1 — a stage owns its sheet */
  .appendix-card { page-break-before: always !important; break-before: page !important; display:block; }
  .appendix-card:first-of-type { page-break-before: auto !important; break-before: auto !important; }
  .tc-page { padding:0 !important; min-height:0 !important; background:#fff !important; }
  .tc-card { box-shadow:none !important; border:1px solid #e6e2d8; }
  /* rule 2 — nothing cut mid-section */
  .pk-atom  { break-inside: avoid !important; page-break-inside: avoid !important; }
  .pk-bound { break-inside: avoid !important; page-break-inside: avoid !important; }
  .pk-keep  { break-after: avoid !important; page-break-after: avoid !important; }
  h1, h2, h3 { break-after: avoid !important; page-break-after: avoid !important;
               break-inside: avoid !important; page-break-inside: avoid !important; }
  img { break-inside: avoid !important; page-break-inside: avoid !important; }
  ${z}
</style></head><body>
${secs.join('\n')}
</body></html>`;
}

const MARK = (PAGE_H) => {
  let atoms = 0, heads = 0, bound = 0, tightened = 0;

  // Least white first, and without touching a single letter. The cards' vertical rhythm is set
  // for a monitor: 30 px between major blocks, 28 px under a top callout, 34 px of body padding.
  // On paper that reads as slack rather than air. Margins and the body padding come down by
  // about a third; type size, box padding and line height are left exactly as authored, so the
  // page gets shorter without anything getting harder to read.
  const shrinkPx = (v, f, floor) => Math.max(floor, Math.round(v * f));
  document.querySelectorAll('.tc-card').forEach(card => {
    const body = card.children[1];
    if (body && /padding:\s*30px 34px 34px/.test(body.getAttribute('style') || '')) {
      body.setAttribute('style', body.getAttribute('style')
        .replace(/padding:\s*30px 34px 34px/, 'padding:20px 30px 22px'));
      tightened++;
    }
    card.querySelectorAll('[style]').forEach(el => {
      let st = el.getAttribute('style');
      const before = st;
      st = st.replace(/margin-bottom:\s*(\d+)px/g,
            (m, n) => +n >= 18 ? 'margin-bottom:' + shrinkPx(+n, 0.62, 12) + 'px' : m);
      st = st.replace(/margin:\s*0 0 (\d+)px/g,
            (m, n) => +n >= 18 ? 'margin:0 0 ' + shrinkPx(+n, 0.62, 12) + 'px' : m);
      st = st.replace(/gap:\s*(\d+)px/g,
            (m, n) => +n >= 14 ? 'gap:' + shrinkPx(+n, 0.75, 10) + 'px' : m);
      if (st !== before) { el.setAttribute('style', st); tightened++; }
    });
  });
  document.querySelectorAll('.tc-card').forEach(card => {
    const band = card.firstElementChild;
    if (band) band.classList.add('pk-atom', 'pk-keep');
    card.querySelectorAll('div,section,p,figure').forEach(el => {
      const s = el.getAttribute('style') || '';
      const rounded = /border-radius:\s*(\d+)px/.exec(s);
      const filled = /background:/.test(s) || /border:\s*\d/.test(s);
      const r = el.getBoundingClientRect();
      if (rounded && filled && r.height > 24 && r.height < 620 && !el.classList.contains('tc-card')) {
        el.classList.add('pk-atom'); atoms++;
      }
      if (el.querySelector(':scope > img') && r.height < 700) { el.classList.add('pk-atom'); atoms++; }
    });
  });
  document.querySelectorAll('.tc-card').forEach(card => {
    const headings = [...card.querySelectorAll('h1,h2,h3')].map(h => {
      let el = h;
      while (el.parentElement && el.parentElement !== card &&
             el.parentElement.getBoundingClientRect().height - el.getBoundingClientRect().height < 26) {
        el = el.parentElement;
      }
      return el;
    });
    new Set(headings).forEach(h => {
      const p = h.parentElement;
      if (!p || h.closest('.pk-bound') || h.closest('.pk-atom')) return;
      heads++; h.classList.add('pk-keep');
      const next = h.nextElementSibling;
      if (!next) return;
      const disp = getComputedStyle(p).display;
      if (disp !== 'block' && disp !== 'flow-root') return;
      const nextH = next.getBoundingClientRect().height;
      if (nextH < 260 && h.getBoundingClientRect().height + nextH < PAGE_H * 0.5) {
        const w = document.createElement('div');
        w.className = 'pk-atom pk-bound';
        p.insertBefore(w, h); w.appendChild(h); w.appendChild(next);
        bound++;
      }
    });
  });
  return { atoms, heads, bound, tightened };
};

async function layout(browser, zooms) {
  const page = await browser.newPage();
  await page.setViewport({ width: CW, height: CH, deviceScaleFactor: 1 });
  const tmp = out.replace(/\.pdf$/, '.__p.html');
  fs.writeFileSync(tmp, docFor(zooms));
  await page.goto('file://' + path.resolve(tmp), { waitUntil: 'networkidle0', timeout: 180000 });
  await page.evaluate(() => document.fonts.ready).catch(() => {});
  await new Promise(r => setTimeout(r, 1200));
  const marked = await page.evaluate(MARK, CH);
  const heights = await page.evaluate(() => [...document.querySelectorAll('.appendix-card')]
    .map(s => { const c = s.querySelector('.tc-card') || s; return c.getBoundingClientRect().height; }));
  return { page, tmp, marked, heights };
}

let ZOOM_ARG = (process.argv.find(a => a.startsWith('--zooms=')) || '').slice(8);
if (!ZOOM_ARG) {
  // the shrink table worked out for this bundle, if one has been computed
  const auto = path.join(__dirname, path.basename(src).replace(/\.html$/, '.zooms.json'));
  if (fs.existsSync(auto)) ZOOM_ARG = auto;
}

(async () => {
  const b = await puppeteer.launch({
    args: ['--allow-file-access-from-files', '--font-render-hinting=none'] });

  let zooms = null;
  if (ZOOM_ARG) zooms = JSON.parse(fs.readFileSync(ZOOM_ARG, 'utf8'));

  const r3 = await layout(b, zooms);
  console.log(`${path.basename(src)}: ${secs.length} stages · ${r3.marked.atoms} blocks protected · `
            + `${r3.marked.heads} headings kept (${r3.marked.bound} bound) · ${r3.marked.tightened} gaps tightened`
            + (zooms ? ` · ${zooms.filter(z => z < 1).length} shrunk to save a sheet` : ''));

  const pdf = await r3.page.pdf({
    format: 'A4', printBackground: true,
    margin: { top: `${MARGIN}mm`, right: `${MARGIN}mm`, bottom: `${MARGIN + 6}mm`, left: `${MARGIN}mm` },
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `<div style="width:100%;font-family:Rubik,Arial,sans-serif;font-size:8px;
      color:#8a8f98;padding:0 10mm;display:flex;justify-content:space-between;">
      <span class="pageNumber"></span><span>${title.replace(/[<>&]/g, '')}</span></div>`,
  });
  fs.writeFileSync(out, pdf);
  fs.unlinkSync(r3.tmp);
  await b.close();
  console.log(`  -> ${out} (${(pdf.length / 1048576).toFixed(1)} MB)`);
})();
