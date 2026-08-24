/* shot_cards.js — screenshot Hebrew task cards so a figure can be PROVED to reach the page.
 *
 *   node _blender/shot_cards.js <project-dir> [outdir] [--full]
 *   node _blender/shot_cards.js Arduino_Projects/Project_4_Line_Following_Car
 *
 * Publishing a render under a name no card references is the failure mode this exists to catch:
 * the figures looked finished on disk and the cards showed the old artwork. A screenshot of the
 * card itself is the only check that actually answers "did the work reach the student".
 *
 * Writes one PNG per card plus a contact sheet, and reports any <img> that failed to load.
 */
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const args = process.argv.slice(2);
const proj = args.find(a => !a.startsWith('--'));
const outdir = args.filter(a => !a.startsWith('--'))[1]
  || path.join(__dirname, 'work', 'cardshots');
const full = args.includes('--full');
if (!proj) {
  console.error('usage: node shot_cards.js <project-dir> [outdir] [--full]');
  process.exit(2);
}

const cardsDir = path.join(proj, 'task_cards_he');
const cards = fs.readdirSync(cardsDir).filter(f => f.endsWith('.dc.html')).sort();
fs.mkdirSync(outdir, { recursive: true });

(async () => {
  const browser = await puppeteer.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1000, height: 1400, deviceScaleFactor: 1 });
  const broken = [];
  for (const c of cards) {
    const url = 'file:///' + path.resolve(cardsDir, c).replace(/\\/g, '/');
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 60000 });
    // an <img> that 404s still lays out; naturalWidth is the only honest signal
    const bad = await page.evaluate(() => Array.from(document.images)
      .filter(i => !i.complete || i.naturalWidth === 0)
      .map(i => i.getAttribute('src')));
    if (bad.length) broken.push({ card: c, bad });
    const out = path.join(outdir, c.replace(/\.dc\.html$/, '') + '.png');
    await page.screenshot({ path: out, fullPage: full });
    console.log((bad.length ? 'BROKEN IMG  ' : 'ok          ') + c
      + (bad.length ? '  -> ' + bad.join(', ') : ''));
  }
  await browser.close();
  if (broken.length) {
    console.log('\n' + broken.length + ' card(s) reference an image that did not load.');
    process.exitCode = 1;
  } else {
    console.log('\nall ' + cards.length + ' cards loaded every image they reference.');
  }
})();
