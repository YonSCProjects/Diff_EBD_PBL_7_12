// Builds the overview PDF with Appendix 1 (cards) merged in.
// Usage: node build_overview_with_cards.js <en|he>
//
// For the chosen language:
//   1. Renders the overview markdown to PDF (via md-to-pdf).
//   2. Renders every reference/task card HTML to PDF (via puppeteer).
//   3. Merges overview + cards into a single PDF using pdf-lib.

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const puppeteer = require('puppeteer');
const { PDFDocument } = require('pdf-lib');

const lang = process.argv[2];
if (!['en', 'he'].includes(lang)) {
  console.error('Usage: node build_overview_with_cards.js <en|he>');
  process.exit(1);
}

const ROOT = __dirname;
const OUT = path.join(ROOT, 'build_output');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT);

const isHe = lang === 'he';
const overviewMd = isHe
  ? 'Arduino_PBL_Program_Overview_he.md'
  : 'Arduino_PBL_Program_Overview.md';
const overviewConfig = isHe ? 'md-to-pdf-he.config.js' : 'md-to-pdf.config.js';
const overviewPdf = overviewMd.replace('.md', '.pdf');
const finalPdf = path.join(OUT, overviewPdf);

const projectDir = path.join(
  ROOT,
  'Arduino_Projects',
  'Project_1_Light_Signals'
);
const refDir = path.join(projectDir, isHe ? 'reference_cards_he' : 'reference_cards');
const taskDir = path.join(projectDir, isHe ? 'task_cards_he' : 'task_cards');

const suffix = isHe ? '_he' : '';
const cardOrder = [
  [refDir, `R1_wiring_reference${suffix}.html`],
  [refDir, `R2_stuck_protocol${suffix}.html`],
  [refDir, `R3_claude_code_prompts${suffix}.html`],
  [refDir, `R4_safety_reminder${suffix}.html`],
  [refDir, `R5_sketch_index${suffix}.html`],
  [taskDir, `T1_M1_setup_workspace${suffix}.html`],
  [taskDir, `T1_M2_first_upload${suffix}.html`],
  [taskDir, `T1_M3_wire_first_led${suffix}.html`],
  [taskDir, `T1_M4_light_up_led${suffix}.html`],
  [taskDir, `T1_M5_add_second_led${suffix}.html`],
  [taskDir, `T1_M6_alternating_blink${suffix}.html`],
  [taskDir, `T1_M7_wire_button${suffix}.html`],
  [taskDir, `T1_M8_button_control${suffix}.html`],
  [taskDir, `T2_M1_startup${suffix}.html`],
  [taskDir, `T2_M2_pick_pattern${suffix}.html`],
  [taskDir, `T2_M3_claude_code_level2${suffix}.html`],
  [taskDir, `T2_M4_button_behavior${suffix}.html`],
  [taskDir, `T2_M5_signature_pattern${suffix}.html`],
  [taskDir, `T3_project_planner${suffix}.html`],
];

async function renderOverview() {
  console.log(`[1/3] Rendering overview PDF: ${overviewMd}`);
  execSync(
    `npx --yes md-to-pdf --config-file ${overviewConfig} "${overviewMd}"`,
    { cwd: ROOT, stdio: 'inherit' }
  );
  const src = path.join(ROOT, overviewPdf);
  const dst = path.join(OUT, overviewPdf);
  fs.renameSync(src, dst);
  return dst;
}

async function renderCards(browser) {
  console.log(`[2/3] Rendering ${cardOrder.length} card PDFs...`);
  const pdfBuffers = [];
  for (const [dir, file] of cardOrder) {
    const full = path.join(dir, file);
    if (!fs.existsSync(full)) {
      console.warn(`  SKIP (missing): ${file}`);
      continue;
    }
    const page = await browser.newPage();
    await page.setJavaScriptEnabled(false);
    const url = 'file:///' + full.replace(/\\/g, '/');
    await page.goto(url, { waitUntil: 'load', timeout: 60000 });
    const buf = await page.pdf({
      format: 'A4',
      printBackground: true,
      margin: { top: '10mm', right: '10mm', bottom: '10mm', left: '10mm' },
    });
    await page.close();
    pdfBuffers.push(buf);
    console.log(`  ok: ${file}`);
  }
  return pdfBuffers;
}

async function mergePdfs(overviewPath, cardBuffers) {
  console.log(`[3/3] Merging PDFs into ${finalPdf}`);
  const out = await PDFDocument.create();
  const overviewBytes = fs.readFileSync(overviewPath);
  const overviewDoc = await PDFDocument.load(overviewBytes);
  const overviewPages = await out.copyPages(
    overviewDoc,
    overviewDoc.getPageIndices()
  );
  overviewPages.forEach((p) => out.addPage(p));
  for (const buf of cardBuffers) {
    const doc = await PDFDocument.load(buf);
    const pages = await out.copyPages(doc, doc.getPageIndices());
    pages.forEach((p) => out.addPage(p));
  }
  const bytes = await out.save();
  fs.writeFileSync(finalPdf, bytes);
  console.log(`Done: ${finalPdf} (${out.getPageCount()} pages)`);
}

function buildMergedHtml() {
  const overviewHtmlName = overviewMd.replace('.md', '.html');
  console.log(`[4/4] Building merged HTML: ${overviewHtmlName}`);
  execSync(
    `npx --yes md-to-pdf --config-file ${overviewConfig} --as-html "${overviewMd}"`,
    { cwd: ROOT, stdio: 'inherit' }
  );
  const src = path.join(ROOT, overviewHtmlName);
  const overviewHtml = fs.readFileSync(src, 'utf8');
  fs.unlinkSync(src);

  const cardSections = [];
  for (const [dir, file] of cardOrder) {
    const full = path.join(dir, file);
    if (!fs.existsSync(full)) continue;
    let html = fs.readFileSync(full, 'utf8');
    const styleMatch = [...html.matchAll(/<link rel="stylesheet" href="([^"]+)">/g)];
    let inlineStyles = '';
    for (const m of styleMatch) {
      const cssPath = path.resolve(dir, m[1]);
      if (fs.existsSync(cssPath)) {
        inlineStyles += `<style>${fs.readFileSync(cssPath, 'utf8')}</style>`;
      }
    }
    const internalStyles = [...html.matchAll(/<style>[\s\S]*?<\/style>/g)]
      .map((m) => m[0])
      .join('\n');
    const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/);
    const body = bodyMatch ? bodyMatch[1] : '';
    const htmlDirMatch = html.match(/<html[^>]*\sdir="([^"]+)"/);
    const dir_ = htmlDirMatch ? htmlDirMatch[1] : 'ltr';
    const htmlLangMatch = html.match(/<html[^>]*\slang="([^"]+)"/);
    const lang_ = htmlLangMatch ? htmlLangMatch[1] : '';
    cardSections.push(
      `<div class="appendix-card" dir="${dir_}" lang="${lang_}" style="page-break-before: always;">${inlineStyles}${internalStyles}${body}</div>`
    );
  }

  const merged = overviewHtml.replace(
    /<\/body>/i,
    cardSections.join('\n') + '\n</body>'
  );
  const outPath = path.join(OUT, overviewHtmlName);
  fs.writeFileSync(outPath, merged, 'utf8');
  console.log(`Done: ${outPath}`);
}

(async () => {
  const overviewPath = await renderOverview();
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  try {
    const cardBuffers = await renderCards(browser);
    await mergePdfs(overviewPath, cardBuffers);
  } finally {
    await browser.close();
  }
  buildMergedHtml();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
