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

// Args may be given in any order: a language (en|he) and an optional project
// key (1|2). Defaults to project 1 for backward compatibility, so the original
// `node build_cards_only.js he` invocation still builds Project 1.
const args = process.argv.slice(2);
const lang = args.find((a) => ['en', 'he'].includes(a));
const projectKey = args.find((a) => ['1', '2', '3', '4'].includes(a)) || '1';
if (!lang) {
  console.error('Usage: node build_cards_only.js <en|he> [project: 1|2|3|4]');
  process.exit(1);
}

const ROOT = __dirname;
const OUT = path.join(ROOT, 'build_output');
if (!fs.existsSync(OUT)) fs.mkdirSync(OUT);

const isHe = lang === 'he';
const suffix = isHe ? '_he' : '';

const PROJECTS = {
  '1': {
    dir: 'Project_1_Light_Signals',
    outBase: 'Project_1_Cards',
    titleHe: 'פרויקט 1 — אותות אור: חוברת כרטיסיות (עזר ומשימה)',
    titleEn: 'Project 1 — Light Signals: Cards Bundle (Reference + Task)',
  },
  '2': {
    dir: 'Project_2_Reaction_Time_Game',
    outBase: 'Project_2_Cards',
    titleHe: 'פרויקט 2 — משחק זמן תגובה: חוברת כרטיסיות (עזר ומשימה)',
    titleEn: 'Project 2 — Reaction-Time Game: Cards Bundle (Reference + Task)',
  },
  '3': {
    dir: 'Project_3_Dont_Get_Too_Close',
    outBase: 'Project_3_Cards',
    titleHe: 'פרויקט 3 — לא להתקרב יותר מדי: חוברת כרטיסיות (עזר ומשימה)',
    titleEn: 'Project 3 — Don\'t Get Too Close: Cards Bundle (Reference + Task)',
  },
  '4': {
    dir: 'Project_4_Line_Following_Car',
    outBase: 'Project_4_Cards',
    titleHe: 'פרויקט 4 — מכונית עוקבת קו: חוברת כרטיסיות (עזר ומשימה)',
    titleEn: 'Project 4 — Line-Following Car: Cards Bundle (Reference + Task)',
  },
};

// Card render order per project. 'R:' stems live in reference_cards[_he];
// 'T:' stems live in task_cards[_he]. The language suffix is applied below.
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
  '3': [
    'R:R0_breadboard_basics',
    'R:R1_wiring_reference',
    'R:R2_stuck_protocol',
    'R:R3_claude_code_prompts',
    'R:R4_safety_reminder',
    'R:R5_sketch_index',
    'T:T1_M1_wire_sensor',
    'T:T1_M2_upload_distance_sketch',
    'T:T1_M3_add_led_threshold',
    'T:T1_M4_add_buzzer_full_alarm',
    'T:T1_M5_test_real_objects',
    'T:T1_M6_show_celebrate',
    'T:T2_M1_startup',
    'T:T2_M2_pick_threshold',
    'T:T2_M3_pick_response_and_modify',
    'T:T2_M4_test_and_tune',
    'T:T2_M5_signature_alarm',
    'T:T3_project_planner',
  ],
  '4': [
    'R:R0_breadboard_basics',
    'R:R1_wiring_reference',
    'R:R2_stuck_protocol',
    'R:R3_claude_code_prompts',
    'R:R4_safety_reminder',
    'R:R5_sketch_index',
    'R:R6_soldering_basics',
    'T:T1_M1_meet_soldering',
    'T:T1_M2_solder_motor_leads',
    'T:T1_M3_assemble_chassis',
    'T:T1_M4_wire_driver_and_sensors',
    'T:T1_M5_drive_forward',
    'T:T1_M6_sensor_test',
    'T:T1_M7_line_follow_first_run',
    'T:T1_M8_run_track_celebrate',
    'T:T2_M1_startup',
    'T:T2_M2_pick_speed',
    'T:T2_M3_pick_correction_and_modify',
    'T:T2_M4_design_build_track',
    'T:T2_M5_test_and_tune',
    'T:T2_M6_signature_run',
    'T:T3_project_planner',
  ],
};

const P = PROJECTS[projectKey];
const projectDir = path.join(ROOT, 'Arduino_Projects', P.dir);
const refDir = path.join(projectDir, isHe ? 'reference_cards_he' : 'reference_cards');
const taskDir = path.join(projectDir, isHe ? 'task_cards_he' : 'task_cards');

const cardOrder = CARD_STEMS[projectKey].map((stem) => {
  const [kind, name] = stem.split(':');
  const dir = kind === 'R' ? refDir : taskDir;
  return [dir, `${name}${suffix}.html`];
});

const outName = `${P.outBase}${suffix}`;
const outHtml = path.join(OUT, `${outName}.html`);
const outPdf = path.join(OUT, `${outName}.pdf`);

const pageTitle = isHe ? P.titleHe : P.titleEn;

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
      // card.js opens a window.prompt() for the student nickname; auto-dismiss
      // it so page load doesn't block. The interactive indicator is print-hidden
      // anyway, so dismissing has no effect on the PDF.
      page.on('dialog', (d) => d.dismiss().catch(() => {}));
      await page.emulateMediaType('print');
      const url = 'file:///' + full.replace(/\\/g, '/');
      await page.goto(url, { waitUntil: 'load', timeout: 60000 });
      // Wait for fonts to finish loading — otherwise a cold Chromium start
      // can render with fallback metrics and reflow content onto extra pages.
      await page.evaluate(() => document.fonts.ready);
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
