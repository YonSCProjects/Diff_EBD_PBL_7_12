// build_posters.js — compose the eight AI-generated hero images into print-ready A4
// classroom posters, movie-poster style: full-bleed image, a dark gradient at the foot,
// and the ONLY text is one title line, "פרויקט N: <name>". The names are Yon's existing
// project names, verbatim — nothing invented.
//
//   node Arduino_Projects/_posters/build_posters.js                    dark set -> out/
//   node Arduino_Projects/_posters/build_posters.js --variant bright   bright set -> out/
//   node Arduino_Projects/_posters/build_posters.js --chosen           Yon's pick -> out/chosen posters/
//
// --chosen rebuilds the eight posters Yon picked (2026-09-27: P1-P7 bright, P8 dark) under
// the filenames he saved them as, plus one print-ready PDF of the set.
//
// Outputs, next to this script:
//   out/poster_pN.png     one per project, 2480x3508 (A4 @ 300dpi)
//   out/Posters_A4.pdf    all eight, ready to print
//   out/contact_sheet.png quick look at the whole series
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const { pathToFileURL } = require('url');

const HERE = __dirname;
// --variant bright  ->  reads src_bright/ and writes *_bright outputs
const vi = process.argv.indexOf('--variant');
const VARIANT = vi > 0 ? process.argv[vi + 1] : '';
const SUFFIX = VARIANT ? '_' + VARIANT : '';
const SRC = path.join(HERE, VARIANT ? 'src_' + VARIANT : 'src');
const CHOSEN_MODE = process.argv.includes('--chosen');
const OUT = CHOSEN_MODE ? path.join(HERE, 'out', 'chosen posters') : path.join(HERE, 'out');
fs.mkdirSync(OUT, { recursive: true });

// Which source each chosen poster comes from ('' = the dark src/, 'bright' = src_bright/).
const CHOSEN = { 1: 'bright', 2: 'bright', 3: 'bright', 4: 'bright',
                 5: 'bright', 6: 'bright', 7: 'bright', 8: '' };

const POSTERS = [
  { n: 1, name: 'אותות אור' },
  { n: 2, name: 'משחק זמן תגובה' },
  { n: 3, name: 'לא להתקרב יותר מדי' },
  { n: 4, name: 'מכונית עוקבת קו' },
  { n: 5, name: 'מכונית נשלטת מרחוק' },
  { n: 6, name: 'תחנת מזג אוויר' },
  { n: 7, name: 'סייר עם מצלמה' },
  { n: 8, name: 'רחפן זעיר' },
];

// A4 @ 300dpi
const W = 2480, H = 3508;
// Title size is measured, not fixed: the numbered titles run long ("פרויקט 5: מכונית
// נשלטת מרחוק" overflows at 190px), so every poster in a set gets the one size that
// fits the longest title on a single line — the series then hangs with matching titles.
const REF = 190, AVAIL = W - 2 * 140;
let SIZE = REF;

const title = (p) => `<span class="num">פרויקט ${p.n}:</span> ${p.name}`;

const page = (p, imgUri) => `
  <div class="poster">
    <img class="hero" src="${imgUri}">
    <div class="foot">
      <div class="name" dir="rtl">${title(p)}</div>
    </div>
  </div>`;

const CSS = (size) => `
  * { box-sizing: border-box; margin: 0; }
  .poster { position: relative; width: ${W}px; height: ${H}px; overflow: hidden;
            background: #0a0e14; page-break-after: always; }
  .hero { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
  .foot { position: absolute; left: 0; right: 0; bottom: 0; padding: 340px 140px 150px;
          background: linear-gradient(to top, rgba(6,10,16,0.92) 0%,
                      rgba(6,10,16,0.72) 45%, rgba(6,10,16,0) 100%);
          text-align: center; font-family: 'Rubik', sans-serif; }
  .name { font-family: 'Rubik', sans-serif; font-size: ${size}px; font-weight: 700;
          line-height: 1.12; color: #ffffff;
          white-space: nowrap; text-shadow: 0 6px 40px rgba(0,0,0,0.85); }
  .num { color: oklch(0.85 0.15 90); }
`;

const HTML = (body) => `<!DOCTYPE html><html lang="he"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;600;700&display=swap" rel="stylesheet">
<style>${CSS(SIZE)}</style></head><body>${body}</body></html>`;

(async () => {
  const b = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const url = (f) => pathToFileURL(f).href;

  // one job per poster: its source image and its output file
  const JOBS = POSTERS.map((p) => {
    const v = CHOSEN_MODE ? CHOSEN[p.n] : VARIANT;
    const img = path.join(HERE, v ? 'src_' + v : 'src', 'p' + p.n + '.png');
    return { p, img, out: 'poster_p' + p.n + (v ? '_' + v : '') + '.png' };
  }).filter((j) => {
    if (fs.existsSync(j.img)) return true;
    console.log('  MISSING ' + path.relative(HERE, j.img) + ' — skipped');
    return false;
  });

  // measure every title at the reference size, then shrink the whole set to fit
  const mp = await b.newPage();
  await mp.setContent(HTML(JOBS.map((j) => '<div><span class="name m" dir="rtl">' + title(j.p) + '</span></div>').join('')),
                      { waitUntil: 'networkidle0' });
  await new Promise((r) => setTimeout(r, 700));   // let Rubik land
  const widths = await mp.evaluate(() => [...document.querySelectorAll('.m')].map((e) => e.getBoundingClientRect().width));
  await mp.close();
  SIZE = Math.min(REF, Math.floor(REF * (AVAIL / Math.max(...widths)) * 0.97));
  console.log('  title size ' + SIZE + 'px (longest title ' + Math.round(Math.max(...widths)) + 'px at ' + REF + 'px)');

  // per-poster PNGs
  for (const j of JOBS) {
    const tmp = path.join(OUT, '_tmp_p' + j.p.n + '.html');
    fs.writeFileSync(tmp, HTML(page(j.p, url(j.img))));
    const pg = await b.newPage();
    await pg.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
    await pg.goto(url(tmp), { waitUntil: 'networkidle0' });
    await new Promise((r) => setTimeout(r, 700));   // let Rubik land
    const clipped = await pg.evaluate(() => {
      const n = document.querySelector('.name');
      return n.scrollWidth > n.clientWidth + 1 || n.getBoundingClientRect().left < 0;
    });
    await pg.screenshot({ path: path.join(OUT, j.out) });
    await pg.close();
    fs.unlinkSync(tmp);
    console.log('  ' + j.out + '  פרויקט ' + j.p.n + ': ' + j.p.name + (clipped ? '   !! TITLE CLIPPED' : ''));
  }

  // one PDF with all posters
  const pdfName = CHOSEN_MODE ? 'Posters_A4_chosen.pdf' : 'Posters_A4' + SUFFIX + '.pdf';
  const tmpAll = path.join(OUT, '_tmp_all.html');
  fs.writeFileSync(tmpAll, HTML(JOBS.map((j) => page(j.p, url(j.img))).join('\n')));
  const pg = await b.newPage();
  await pg.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
  await pg.goto(url(tmpAll), { waitUntil: 'networkidle0' });
  await new Promise((r) => setTimeout(r, 900));
  await pg.pdf({ path: path.join(OUT, pdfName), width: W + 'px', height: H + 'px',
                 printBackground: true, pageRanges: '1-' + JOBS.length });
  await pg.close();
  fs.unlinkSync(tmpAll);
  console.log('  ' + pdfName);

  // contact sheet for a quick look
  const sheetName = CHOSEN_MODE ? 'contact_sheet_chosen.png' : 'contact_sheet' + SUFFIX + '.png';
  const thumbs = JOBS.map((j) => '<img style="width:24%;margin:0.5%" src="' + url(path.join(OUT, j.out)) + '">').join('');
  const tmpCs = path.join(OUT, '_tmp_cs.html');
  fs.writeFileSync(tmpCs, '<body style="margin:0;background:#111;display:flex;flex-wrap:wrap;">' + thumbs);
  const cs = await b.newPage();
  await cs.setViewport({ width: 2200, height: 1560, deviceScaleFactor: 1 });
  await cs.goto(url(tmpCs), { waitUntil: 'networkidle0' });
  await new Promise((r) => setTimeout(r, 600));
  await cs.screenshot({ path: path.join(OUT, sheetName), fullPage: true });
  await cs.close();
  fs.unlinkSync(tmpCs);
  console.log('  ' + sheetName);

  await b.close();
})();
