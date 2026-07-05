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
const { resolveCardFile, renderCardPdf, snapshotCardHtml, scopeCss, DC_FONTS_LINK } = require('./render_cards_lib');

// Args in any order: a language (en|he) and an optional project key (1|2).
// Defaults to project 1 for backward compatibility.
const args = process.argv.slice(2);
const lang = args.find((a) => ['en', 'he'].includes(a));
const projectKey = args.find((a) => ['1', '2'].includes(a)) || '1';
if (!lang) {
  console.error('Usage: node build_overview_with_cards.js <en|he> [project: 1|2]');
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

const suffix = isHe ? '_he' : '';

// Card render order per project. 'R:' stems live in reference_cards[_he];
// 'T:' stems live in task_cards[_he].
const CARD_STEMS = {
  '1': [
    'R:R0_breadboard_basics',
    'R:R1_wiring_reference',
    'R:R2_stuck_protocol',
    'R:R3_claude_code_prompts',
    'R:R4_safety_reminder',
    'R:R5_sketch_index',
    'T:T1_M1_setup_workspace',
    'T:T1_M2_first_upload',
    'T:T1_M3_wire_first_led',
    'T:T1_M4_light_up_led',
    'T:T1_M5_add_second_led',
    'T:T1_M6_alternating_blink',
    'T:T1_M7_wire_button',
    'T:T1_M8_button_control',
    'T:T2_M1_startup',
    'T:T2_M2_pick_pattern',
    'T:T2_M2b_wire_third_led',
    'T:T2_M3_claude_code_level2',
    'T:T2_M4_button_behavior',
    'T:T2_M5_signature_pattern',
    'T:T3_project_planner',
  ],
  '2': [
    'R:R0_breadboard_basics',
    'R:R1_wiring_reference',
    'R:R2_stuck_protocol',
    'R:R3_claude_code_prompts',
    'R:R4_safety_reminder',
    'R:R5_sketch_index',
    'T:T1_M1_wire_led_and_button',
    'T:T1_M2_upload_wait_flash_measure',
    'T:T1_M3_play_five_rounds',
    'T:T1_M4_add_buzzer',
    'T:T1_M5_upload_buzzer_sketch',
    'T:T1_M6_record_fastest_time',
    'T:T2_M1_startup',
    'T:T2_M2_pick_feedback_mode',
    'T:T2_M2b_wire_three_leds',
    'T:T2_M3_pick_difficulty_and_modify',
    'T:T2_M4_upload_test_tune',
    'T:T2_M5_signature_game',
    'T:T3_project_planner',
  ],
};

const PROJECT_DIRS = {
  '1': 'Project_1_Light_Signals',
  '2': 'Project_2_Reaction_Time_Game',
};

const projectDir = path.join(ROOT, 'Arduino_Projects', PROJECT_DIRS[projectKey]);
const refDir = path.join(projectDir, isHe ? 'reference_cards_he' : 'reference_cards');
const taskDir = path.join(projectDir, isHe ? 'task_cards_he' : 'task_cards');

// HE task cards prefer their .dc.html twin; reference cards and EN builds stay
// classic (resolveCardFile falls back automatically).
const cardOrder = CARD_STEMS[projectKey].map((stem) => {
  const [kind, name] = stem.split(':');
  const dir = kind === 'R' ? refDir : taskDir;
  const key = kind === 'T' ? projectKey : null;
  return [dir, resolveCardFile(dir, name, suffix, key)];
});

const MARKER = '<!-- INSERT_CARDS_HERE -->';

function renderMdToPdf(mdPath) {
  execSync(
    `npx --yes md-to-pdf --config-file ${overviewConfig} "${mdPath}"`,
    { cwd: ROOT, stdio: 'inherit' }
  );
  return path.join(ROOT, path.basename(mdPath).replace(/\.md$/, '.pdf'));
}

async function renderOverview() {
  const src = fs.readFileSync(path.join(ROOT, overviewMd), 'utf8');
  if (!src.includes(MARKER)) {
    console.log(`[1/3] Rendering overview PDF (no marker — cards will append at end)`);
    const pdf = renderMdToPdf(overviewMd);
    return { parts: [pdf], splitAtEnd: true };
  }
  console.log(`[1/3] Rendering overview PDF in two parts (split at INSERT_CARDS_HERE marker)`);
  const [before, after] = src.split(MARKER);
  const part1Md = overviewMd.replace(/\.md$/, '.part1.md');
  const part2Md = overviewMd.replace(/\.md$/, '.part2.md');
  fs.writeFileSync(path.join(ROOT, part1Md), before, 'utf8');
  fs.writeFileSync(path.join(ROOT, part2Md), after, 'utf8');
  const pdf1 = renderMdToPdf(part1Md);
  const pdf2 = renderMdToPdf(part2Md);
  fs.unlinkSync(path.join(ROOT, part1Md));
  fs.unlinkSync(path.join(ROOT, part2Md));
  return { parts: [pdf1, pdf2], splitAtEnd: false };
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
    // renderCardPdf runs the dc runtime (JS on) + waits for it to settle before
    // capturing; classic cards render as before (JS harmlessly on, dialog dismissed).
    const buf = await renderCardPdf(browser, full);
    pdfBuffers.push(buf);
    console.log(`  ok: ${file}`);
  }
  return pdfBuffers;
}

async function mergePdfs(overviewInfo, cardBuffers) {
  console.log(`[3/3] Merging PDFs into ${finalPdf}`);
  const out = await PDFDocument.create();

  async function appendPdfFile(p) {
    const doc = await PDFDocument.load(fs.readFileSync(p));
    const pages = await out.copyPages(doc, doc.getPageIndices());
    pages.forEach((pg) => out.addPage(pg));
  }
  async function appendPdfBuf(buf) {
    const doc = await PDFDocument.load(buf);
    const pages = await out.copyPages(doc, doc.getPageIndices());
    pages.forEach((pg) => out.addPage(pg));
  }

  if (overviewInfo.splitAtEnd) {
    await appendPdfFile(overviewInfo.parts[0]);
    for (const buf of cardBuffers) await appendPdfBuf(buf);
  } else {
    await appendPdfFile(overviewInfo.parts[0]);
    for (const buf of cardBuffers) await appendPdfBuf(buf);
    await appendPdfFile(overviewInfo.parts[1]);
    // Clean up intermediate part PDFs
    for (const p of overviewInfo.parts) {
      try { fs.unlinkSync(p); } catch (_) {}
    }
  }
  const bytes = await out.save();
  fs.writeFileSync(finalPdf, bytes);
  console.log(`Done: ${finalPdf} (${out.getPageCount()} pages)`);
}

async function buildMergedHtml(browser) {
  const overviewHtmlName = overviewMd.replace('.md', '.html');
  console.log(`[4/4] Building merged HTML: ${overviewHtmlName}`);
  execSync(
    `npx --yes md-to-pdf --config-file ${overviewConfig} --as-html "${overviewMd}"`,
    { cwd: ROOT, stdio: 'inherit' }
  );
  const src = path.join(ROOT, overviewHtmlName);
  let overviewHtml = fs.readFileSync(src, 'utf8');
  fs.unlinkSync(src);

  const styleSet = new Map(); // scoped <style> block -> true (dedup, ordered)
  const cardSections = [];
  let anyDc = false;
  for (const [dir, file] of cardOrder) {
    const full = path.join(dir, file);
    if (!fs.existsSync(full)) continue;
    const snap = await snapshotCardHtml(browser, full);
    if (snap.fonts) anyDc = true;
    // Scope each card's CSS to its flavor wrapper so classic element rules can't
    // bleed onto the inline-styled dc cards (and vice versa).
    const flavorClass = snap.fonts ? 'appendix-card--dc' : 'appendix-card--classic';
    for (const m of (snap.styles || '').matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)) {
      const scoped = `<style>${scopeCss(m[1], '.' + flavorClass)}</style>`;
      if (!styleSet.has(scoped)) styleSet.set(scoped, true);
    }
    const d = snap.dir || 'rtl';
    const l = snap.lang || 'he';
    cardSections.push(
      `<div class="appendix-card ${flavorClass}" dir="${d}" lang="${l}" style="page-break-before: always;">${snap.body}</div>`
    );
  }

  const headInject = (anyDc ? DC_FONTS_LINK : '') + '\n' + [...styleSet.keys()].join('\n');
  overviewHtml = overviewHtml.replace(/<\/head>/i, headInject + '\n</head>');
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
    await buildMergedHtml(browser);
  } finally {
    await browser.close();
  }
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
