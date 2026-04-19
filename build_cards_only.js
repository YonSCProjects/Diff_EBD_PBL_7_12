// Builds a standalone cards-only bundle (HTML + PDF) for one language.
// Usage: node build_cards_only.js <en|he>
//
// For the chosen language:
//   1. Merges all reference + task cards into a single HTML file
//      (stylesheets inlined so the file is self-contained).
//   2. Renders every card HTML to PDF via puppeteer and merges them
//      into a single PDF using pdf-lib.
//
// Outputs:
//   build_output/Project_1_Cards.html   /  Project_1_Cards.pdf   (en)
//   build_output/Project_1_Cards_he.html / Project_1_Cards_he.pdf (he)

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const { PDFDocument } = require('pdf-lib');

const lang = process.argv[2];
if (!['en', 'he'].includes(lang)) {
  console.error('Usage: node build_cards_only.js <en|he>');
  process.exit(1);
}

const ROOT = __dirname;
const OUT = path.join(ROOT, 'build_output');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT);

const isHe = lang === 'he';
const suffix = isHe ? '_he' : '';

const projectDir = path.join(ROOT, 'Arduino_Projects', 'Project_1_Light_Signals');
const refDir = path.join(projectDir, isHe ? 'reference_cards_he' : 'reference_cards');
const taskDir = path.join(projectDir, isHe ? 'task_cards_he' : 'task_cards');

const cardOrder = [
  [refDir, `R0_breadboard_basics${suffix}.html`],
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
  [taskDir, `T2_M2b_wire_third_led${suffix}.html`],
  [taskDir, `T2_M3_claude_code_level2${suffix}.html`],
  [taskDir, `T2_M4_button_behavior${suffix}.html`],
  [taskDir, `T2_M5_signature_pattern${suffix}.html`],
  [taskDir, `T3_project_planner${suffix}.html`],
];

const outName = `Project_1_Cards${suffix}`;
const outHtml = path.join(OUT, `${outName}.html`);
const outPdf = path.join(OUT, `${outName}.pdf`);

const pageTitle = isHe
  ? 'פרויקט 1 — אותות אור: חוברת כרטיסיות (עזר ומשימה)'
  : 'Project 1 — Light Signals: Cards Bundle (Reference + Task)';

function buildMergedHtml() {
  console.log(`[HTML] Merging ${cardOrder.length} cards into ${outHtml}`);

  // Deduplicate inlined stylesheets so we don't paste the same CSS 21 times.
  const cssCache = new Map(); // absolute path -> css content
  const cardSections = [];

  for (const [dir, file] of cardOrder) {
    const full = path.join(dir, file);
    if (!fs.existsSync(full)) {
      console.warn(`  SKIP (missing): ${file}`);
      continue;
    }
    const html = fs.readFileSync(full, 'utf8');

    // Collect <link rel="stylesheet" href="..."> → add to cache.
    const linkMatches = [...html.matchAll(/<link rel="stylesheet" href="([^"]+)">/g)];
    for (const m of linkMatches) {
      const cssPath = path.resolve(dir, m[1]);
      if (!cssCache.has(cssPath) && fs.existsSync(cssPath)) {
        cssCache.set(cssPath, fs.readFileSync(cssPath, 'utf8'));
      }
    }

    // Keep per-card <style> blocks inline (they may contain card-specific tweaks).
    const internalStyles = [...html.matchAll(/<style>[\s\S]*?<\/style>/g)]
      .map((m) => m[0])
      .join('\n');

    const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/);
    const body = bodyMatch ? bodyMatch[1] : '';

    const htmlDirMatch = html.match(/<html[^>]*\sdir="([^"]+)"/);
    const dir_ = htmlDirMatch ? htmlDirMatch[1] : (isHe ? 'rtl' : 'ltr');
    const htmlLangMatch = html.match(/<html[^>]*\slang="([^"]+)"/);
    const lang_ = htmlLangMatch ? htmlLangMatch[1] : (isHe ? 'he' : 'en');

    cardSections.push(
      `<section class="appendix-card" dir="${dir_}" lang="${lang_}" style="page-break-before: always;">${internalStyles}${body}</section>`
    );
  }

  const sharedStyles = [...cssCache.values()]
    .map((css) => `<style>${css}</style>`)
    .join('\n');

  const wrapperDir = isHe ? 'rtl' : 'ltr';
  const wrapperLang = isHe ? 'he' : 'en';

  const merged = `<!doctype html>
<html lang="${wrapperLang}" dir="${wrapperDir}">
<head>
<meta charset="utf-8">
<title>${pageTitle}</title>
${sharedStyles}
<style>
  /* Bundle-level: the first card shouldn't force a blank leading page. */
  .appendix-card:first-of-type { page-break-before: auto !important; }
  body { margin: 0; padding: 0; }
</style>
</head>
<body>
${cardSections.join('\n')}
</body>
</html>
`;

  fs.writeFileSync(outHtml, merged, 'utf8');
  console.log(`  Done: ${outHtml}`);
}

async function buildMergedPdf() {
  console.log(`[PDF] Rendering ${cardOrder.length} cards to PDF → ${outPdf}`);
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const out = await PDFDocument.create();
  try {
    for (const [dir, file] of cardOrder) {
      const full = path.join(dir, file);
      if (!fs.existsSync(full)) {
        console.warn(`  SKIP (missing): ${file}`);
        continue;
      }
      const page = await browser.newPage();
      await page.setJavaScriptEnabled(false);
      await page.emulateMediaType('print');
      const url = 'file:///' + full.replace(/\\/g, '/');
      await page.goto(url, { waitUntil: 'load', timeout: 60000 });
      const buf = await page.pdf({
        format: 'A4',
        printBackground: true,
        margin: { top: '10mm', right: '10mm', bottom: '10mm', left: '10mm' },
      });
      await page.close();
      const doc = await PDFDocument.load(buf);
      const pages = await out.copyPages(doc, doc.getPageIndices());
      pages.forEach((pg) => out.addPage(pg));
      console.log(`  ok: ${file}`);
    }
  } finally {
    await browser.close();
  }
  const bytes = await out.save();
  fs.writeFileSync(outPdf, bytes);
  console.log(`  Done: ${outPdf} (${out.getPageCount()} pages)`);
}

(async () => {
  buildMergedHtml();
  await buildMergedPdf();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
