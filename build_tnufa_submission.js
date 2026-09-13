// Builds the final Tnufa submission PDF from Yon's docx-derived proposal PDF:
// pages 1..SPLIT_AFTER stay (through נספח א'), the 130 task cards of projects
// 1-8 are inserted as the body of appendix A, and the remaining pages (נספח ב'
// — the budget) close the file. The cards are printed in ONE Chromium pass so
// their fonts embed once (the lesson of the 155 MB first attempt).
//
// Usage: node build_tnufa_submission.js
// Input:  build_output/הצעת_יוזמה_תנופה_תשפז_סדנת_ארדואינו.pdf  (from Word)
// Output: build_output/הצעת_יוזמה_תנופה_תשפז_סדנת_ארדואינו_עם_נספח_הכרטיסיות.pdf

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const { PDFDocument } = require('pdf-lib');
const { resolveCardFile, snapshotCardHtml, scopeCss, DC_FONTS_LINK } = require('./render_cards_lib');

const ROOT = __dirname;
const OUT = path.join(ROOT, 'build_output');
const PROPOSAL = path.join(OUT, 'הצעת_יוזמה_תנופה_תשפז_סדנת_ארדואינו.pdf');
const FINAL = path.join(OUT, 'הצעת_יוזמה_תנופה_תשפז_סדנת_ארדואינו_עם_נספח_הכרטיסיות.pdf');
const SPLIT_AFTER = 13; // last page of נספח א' in the Word-exported proposal PDF

// card order: T: stems of projects 1..8 from build_cards_only.js (single source of truth)
const bco = fs.readFileSync(path.join(ROOT, 'build_cards_only.js'), 'utf8');
const CARD_STEMS = new Function('return ' + bco.match(/const CARD_STEMS = (\{[\s\S]*?\n\});/)[1])();
const PROJECTS = new Function('return ' + bco.match(/const PROJECTS = (\{[\s\S]*?\n\});/)[1])();

const cardOrder = [];
for (const key of ['1', '2', '3', '4', '5', '6', '7', '8']) {
  const taskDir = path.join(ROOT, 'Arduino_Projects', PROJECTS[key].dir, 'task_cards_he');
  for (const stem of CARD_STEMS[key]) {
    const [kind, name] = stem.split(':');
    if (kind !== 'T') continue;
    cardOrder.push([taskDir, resolveCardFile(taskDir, name, '_he', key)]);
  }
}
console.log(`appendix A: ${cardOrder.length} task cards across projects 1-8`);

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  try {
    console.log('[1/3] snapshotting cards into one HTML...');
    const styleSet = new Map();
    const sections = [];
    let anyDc = false;
    for (const [dir, file] of cardOrder) {
      const full = path.join(dir, file);
      if (!fs.existsSync(full)) { console.warn(`  SKIP (missing): ${file}`); continue; }
      const snap = await snapshotCardHtml(browser, full);
      if (snap.fonts) anyDc = true;
      const flavorClass = snap.fonts ? 'appendix-card--dc' : 'appendix-card--classic';
      for (const m of (snap.styles || '').matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)) {
        const scoped = `<style>${scopeCss(m[1], '.' + flavorClass)}</style>`;
        if (!styleSet.has(scoped)) styleSet.set(scoped, true);
      }
      sections.push(`<div class="appendix-card ${flavorClass}" dir="${snap.dir || 'rtl'}" lang="${snap.lang || 'he'}" style="page-break-before: always;">${snap.body}</div>`);
    }
    const html = `<!DOCTYPE html><html lang="he" dir="rtl"><head><meta charset="utf-8">
${anyDc ? DC_FONTS_LINK : ''}
${[...styleSet.keys()].join('\n')}
<style>body{margin:0}</style>
</head><body>${sections.join('\n')}</body></html>`;
    const htmlPath = path.join(OUT, '_tnufa_cards_appendix.html');
    fs.writeFileSync(htmlPath, html, 'utf8');

    console.log('[2/3] printing all cards in one Chromium pass...');
    const page = await browser.newPage();
    page.setDefaultTimeout(600000);
    await page.goto('file:///' + htmlPath.replace(/\\/g, '/'), { waitUntil: 'networkidle0', timeout: 600000 });
    await new Promise((r) => setTimeout(r, 3000));
    const cardsPdf = await page.pdf({
      format: 'A4',
      margin: { top: '25mm', right: '20mm', bottom: '25mm', left: '20mm' },
      printBackground: true,
      timeout: 600000,
    });
    await page.close();
    fs.unlinkSync(htmlPath);

    console.log('[3/3] splicing cards into appendix A...');
    const proposal = await PDFDocument.load(fs.readFileSync(PROPOSAL));
    const cards = await PDFDocument.load(cardsPdf);
    const out = await PDFDocument.create();
    const head = await out.copyPages(proposal, [...Array(SPLIT_AFTER).keys()]);
    head.forEach((p) => out.addPage(p));
    const mid = await out.copyPages(cards, cards.getPageIndices());
    mid.forEach((p) => out.addPage(p));
    const tailIdx = proposal.getPageIndices().slice(SPLIT_AFTER);
    const tail = await out.copyPages(proposal, tailIdx);
    tail.forEach((p) => out.addPage(p));
    fs.writeFileSync(FINAL, await out.save());
    const mb = (fs.statSync(FINAL).size / 1048576).toFixed(1);
    console.log(`Done: ${FINAL} (${out.getPageCount()} pages, ${mb} MB)`);
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error(e); process.exit(1); });
