// build_posters.js — compose the eight AI-generated hero images into print-ready A4
// classroom posters, movie-poster style: full-bleed image, a dark gradient at the foot,
// and the ONLY text is the project's own Hebrew name plus a small "פרויקט N" chip.
// The names are Yon's existing project names, verbatim — nothing invented.
//
//   node Arduino_Projects/_posters/build_posters.js
//
// Outputs, next to this script:
//   out/poster_pN.png     one per project, 2480x3508 (A4 @ 300dpi)
//   out/Posters_A4.pdf    all eight, ready to print
//   out/contact_sheet.png quick look at the whole series
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const HERE = __dirname;
const SRC = path.join(HERE, 'src');
const OUT = path.join(HERE, 'out');
fs.mkdirSync(OUT, { recursive: true });

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

const page = (p, imgUri) => `
  <div class="poster">
    <img class="hero" src="${imgUri}">
    <div class="foot">
      <div class="chip" dir="rtl">פרויקט ${p.n}</div>
      <div class="name" dir="rtl">${p.name}</div>
    </div>
  </div>`;

const CSS = `
  * { box-sizing: border-box; margin: 0; }
  .poster { position: relative; width: ${W}px; height: ${H}px; overflow: hidden;
            background: #0a0e14; page-break-after: always; }
  .hero { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
  .foot { position: absolute; left: 0; right: 0; bottom: 0; padding: 340px 140px 150px;
          background: linear-gradient(to top, rgba(6,10,16,0.92) 0%,
                      rgba(6,10,16,0.72) 45%, rgba(6,10,16,0) 100%);
          text-align: center; font-family: 'Rubik', sans-serif; }
  .chip { display: inline-block; font-size: 64px; font-weight: 600; letter-spacing: 0.06em;
          color: oklch(0.85 0.15 90); border: 4px solid oklch(0.78 0.16 90);
          border-radius: 999px; padding: 14px 54px; margin-bottom: 44px;
          background: rgba(0,0,0,0.35); }
  .name { font-size: 190px; font-weight: 700; line-height: 1.12; color: #ffffff;
          text-shadow: 0 6px 40px rgba(0,0,0,0.85); }
`;

const HTML = (body) => `<!DOCTYPE html><html lang="he"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;600;700&display=swap" rel="stylesheet">
<style>${CSS}</style></head><body>${body}</body></html>`;

(async () => {
  const b = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });

  // per-poster PNGs
  for (const p of POSTERS) {
    const img = path.join(SRC, 'p' + p.n + '.png');
    if (!fs.existsSync(img)) { console.log('  MISSING src/p' + p.n + '.png — skipped'); continue; }
    const uri = '../src/p' + p.n + '.png';
    const tmp = path.join(OUT, '_tmp_p' + p.n + '.html');
    fs.writeFileSync(tmp, HTML(page(p, uri)));
    const pg = await b.newPage();
    await pg.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
    await pg.goto('file:///' + tmp.split(path.sep).join('/'), { waitUntil: 'networkidle0' });
    await new Promise((r) => setTimeout(r, 700));   // let Rubik land
    await pg.screenshot({ path: path.join(OUT, 'poster_p' + p.n + '.png') });
    await pg.close();
    fs.unlinkSync(tmp);
    console.log('  poster_p' + p.n + '.png  ' + p.name);
  }

  // one PDF with all posters — the page must live on the file:// origin to read the images
  const all = POSTERS
    .filter((p) => fs.existsSync(path.join(SRC, 'p' + p.n + '.png')))
    .map((p) => page(p, '../src/p' + p.n + '.png'))
    .join('\n');
  const tmpAll = path.join(OUT, '_tmp_all.html');
  fs.writeFileSync(tmpAll, HTML(all));
  const pg = await b.newPage();
  await pg.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
  await pg.goto('file:///' + tmpAll.split(path.sep).join('/'), { waitUntil: 'networkidle0' });
  await new Promise((r) => setTimeout(r, 900));
  await pg.pdf({ path: path.join(OUT, 'Posters_A4.pdf'), width: W + 'px', height: H + 'px',
                 printBackground: true, pageRanges: '1-' + POSTERS.length });
  await pg.close();
  fs.unlinkSync(tmpAll);
  console.log('  Posters_A4.pdf');

  // contact sheet for a quick look
  const thumbs = POSTERS.map((p) => {
    const f = path.join(OUT, 'poster_p' + p.n + '.png');
    return fs.existsSync(f)
      ? '<img style="width:24%;margin:0.5%" src="poster_p' + p.n + '.png">'
      : '';
  }).join('');
  const tmpCs = path.join(OUT, '_tmp_cs.html');
  fs.writeFileSync(tmpCs, '<body style="margin:0;background:#111;display:flex;flex-wrap:wrap;">' + thumbs);
  const cs = await b.newPage();
  await cs.setViewport({ width: 2200, height: 1560, deviceScaleFactor: 1 });
  await cs.goto('file:///' + tmpCs.split(path.sep).join('/'), { waitUntil: 'networkidle0' });
  await new Promise((r) => setTimeout(r, 600));
  await cs.screenshot({ path: path.join(OUT, 'contact_sheet.png'), fullPage: true });
  await cs.close();
  fs.unlinkSync(tmpCs);
  console.log('  contact_sheet.png');

  await b.close();
})();
