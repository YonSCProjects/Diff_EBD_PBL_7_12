// Builds the Tnufa educational-initiative proposal PDF+HTML with the task cards
// of projects 1-8 merged in as the appendix (no Project 9, no reference cards).
// Usage: node build_yozma_tnufa.js
//
// Mechanics mirror build_overview_with_cards.js: render the markdown in two
// parts split at the INSERT_CARDS_HERE marker, render every task card of
// projects 1-8 to PDF (dc runtime settled), merge with pdf-lib, and emit a
// merged HTML twin. Card order comes from build_cards_only.js's CARD_STEMS
// (extracted at runtime so there is a single source of truth), T: stems only.

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const puppeteer = require('puppeteer');
const { PDFDocument } = require('pdf-lib');
const { resolveCardFile, renderCardPdf, snapshotCardHtml, scopeCss, DC_FONTS_LINK } = require('./render_cards_lib');

const ROOT = __dirname;
const OUT = path.join(ROOT, 'build_output');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT);

const SRC_MD = 'Arduino_Yozma_Tnufa_he.md';
const CONFIG = 'md-to-pdf-he.config.js';
const finalPdf = path.join(OUT, SRC_MD.replace('.md', '.pdf'));
const MARKER = '<!-- INSERT_CARDS_HERE -->';

// ---- card order: T: stems of projects 1..8 from build_cards_only.js ----
const bco = fs.readFileSync(path.join(ROOT, 'build_cards_only.js'), 'utf8');
const stemsMatch = bco.match(/const CARD_STEMS = (\{[\s\S]*?\n\});/);
if (!stemsMatch) throw new Error('CARD_STEMS not found in build_cards_only.js');
const CARD_STEMS = new Function('return ' + stemsMatch[1])();
const dirsMatch = bco.match(/const PROJECTS = (\{[\s\S]*?\n\});/);
if (!dirsMatch) throw new Error('PROJECTS not found in build_cards_only.js');
const PROJECTS = new Function('return ' + dirsMatch[1])();

const cardOrder = [];
for (const key of ['1', '2', '3', '4', '5', '6', '7', '8']) {
  const taskDir = path.join(ROOT, 'Arduino_Projects', PROJECTS[key].dir, 'task_cards_he');
  for (const stem of CARD_STEMS[key]) {
    const [kind, name] = stem.split(':');
    if (kind !== 'T') continue; // task cards only in this appendix
    cardOrder.push([taskDir, resolveCardFile(taskDir, name, '_he', key)]);
  }
}
console.log(`appendix: ${cardOrder.length} task cards across projects 1-8`);

function renderMdToPdf(mdPath) {
  execSync(`npx --yes md-to-pdf --config-file ${CONFIG} "${mdPath}"`, { cwd: ROOT, stdio: 'inherit' });
  return path.join(ROOT, path.basename(mdPath).replace(/\.md$/, '.pdf'));
}

async function renderDoc() {
  const src = fs.readFileSync(path.join(ROOT, SRC_MD), 'utf8');
  if (!src.includes(MARKER)) throw new Error('INSERT_CARDS_HERE marker missing from ' + SRC_MD);
  console.log(`[1/4] Rendering proposal PDF in two parts (split at marker)`);
  const [before, after] = src.split(MARKER);
  const p1 = SRC_MD.replace(/\.md$/, '.part1.md');
  const p2 = SRC_MD.replace(/\.md$/, '.part2.md');
  fs.writeFileSync(path.join(ROOT, p1), before, 'utf8');
  fs.writeFileSync(path.join(ROOT, p2), after, 'utf8');
  const pdf1 = renderMdToPdf(p1);
  const pdf2 = renderMdToPdf(p2);
  fs.unlinkSync(path.join(ROOT, p1));
  fs.unlinkSync(path.join(ROOT, p2));
  return [pdf1, pdf2];
}

async function renderCards(browser) {
  console.log(`[2/4] Rendering ${cardOrder.length} card PDFs...`);
  const bufs = [];
  for (const [dir, file] of cardOrder) {
    const full = path.join(dir, file);
    if (!fs.existsSync(full)) { console.warn(`  SKIP (missing): ${file}`); continue; }
    bufs.push(await renderCardPdf(browser, full));
    console.log(`  ok: ${file}`);
  }
  return bufs;
}

async function mergePdfs(parts, cardBuffers) {
  console.log(`[3/4] Merging into ${finalPdf}`);
  const out = await PDFDocument.create();
  const append = async (bytes) => {
    const doc = await PDFDocument.load(bytes);
    const pages = await out.copyPages(doc, doc.getPageIndices());
    pages.forEach((pg) => out.addPage(pg));
  };
  await append(fs.readFileSync(parts[0]));
  for (const buf of cardBuffers) await append(buf);
  await append(fs.readFileSync(parts[1]));
  for (const p of parts) { try { fs.unlinkSync(p); } catch (_) {} }
  const bytes = await out.save();
  fs.writeFileSync(finalPdf, bytes);
  console.log(`Done: ${finalPdf} (${out.getPageCount()} pages)`);
}

async function buildMergedHtml(browser) {
  const htmlName = SRC_MD.replace('.md', '.html');
  console.log(`[4/4] Building merged HTML: ${htmlName}`);
  execSync(`npx --yes md-to-pdf --config-file ${CONFIG} --as-html "${SRC_MD}"`, { cwd: ROOT, stdio: 'inherit' });
  const src = path.join(ROOT, htmlName);
  let html = fs.readFileSync(src, 'utf8');
  fs.unlinkSync(src);

  const styleSet = new Map();
  const sections = [];
  let anyDc = false;
  for (const [dir, file] of cardOrder) {
    const full = path.join(dir, file);
    if (!fs.existsSync(full)) continue;
    const snap = await snapshotCardHtml(browser, full);
    if (snap.fonts) anyDc = true;
    const flavorClass = snap.fonts ? 'appendix-card--dc' : 'appendix-card--classic';
    for (const m of (snap.styles || '').matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)) {
      const scoped = `<style>${scopeCss(m[1], '.' + flavorClass)}</style>`;
      if (!styleSet.has(scoped)) styleSet.set(scoped, true);
    }
    sections.push(`<div class="appendix-card ${flavorClass}" dir="${snap.dir || 'rtl'}" lang="${snap.lang || 'he'}" style="page-break-before: always;">${snap.body}</div>`);
  }
  const headInject = (anyDc ? DC_FONTS_LINK : '') + '\n' + [...styleSet.keys()].join('\n');
  html = html.replace(/<\/head>/i, headInject + '\n</head>');
  html = html.replace(/<\/body>/i, sections.join('\n') + '\n</body>');
  fs.writeFileSync(path.join(OUT, htmlName), html, 'utf8');
  console.log(`Done: ${path.join(OUT, htmlName)}`);
}

(async () => {
  const parts = await renderDoc();
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  try {
    const cardBuffers = await renderCards(browser);
    await mergePdfs(parts, cardBuffers);
    await buildMergedHtml(browser);
  } finally {
    await browser.close();
  }
})().catch((err) => { console.error(err); process.exit(1); });
