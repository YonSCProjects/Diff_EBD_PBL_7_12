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
const { resolveCardFile, renderCardPdf, snapshotCardHtml, DC_FONTS_LINK, scopeCss } = require('./render_cards_lib');

// Args may be given in any order: a language (en|he) and an optional project
// key (1|2). Defaults to project 1 for backward compatibility, so the original
// `node build_cards_only.js he` invocation still builds Project 1.
const args = process.argv.slice(2);
const lang = args.find((a) => ['en', 'he'].includes(a));
const projectKey = args.find((a) => ['1', '2', '3', '4', '5', '6', '7', '8'].includes(a)) || '1';
if (!lang) {
  console.error('Usage: node build_cards_only.js <en|he> [project: 1|2|3|4|5|6|7|8]');
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
  '5': {
    dir: 'Project_5_Remote_Controlled_Car',
    outBase: 'Project_5_Cards',
    titleHe: 'פרויקט 5 — מכונית נשלטת מרחוק: חוברת כרטיסיות (משימה)',
    titleEn: 'Project 5 — Remote-Controlled Car: Cards Bundle (Task)',
  },
  '6': {
    dir: 'Project_6_ESP32_WiFi_Controller',
    outBase: 'Project_6_Cards',
    titleHe: 'פרויקט 6 — תחנת מזג אוויר ב-ESP32: חוברת כרטיסיות (משימה)',
    titleEn: 'Project 6 — ESP32 Wi-Fi Controller: Cards Bundle (Task)',
  },
  '7': {
    dir: 'Project_7_Camera_Explorer',
    outBase: 'Project_7_Cards',
    titleHe: 'פרויקט 7 — סייר עם מצלמה: חוברת כרטיסיות (משימה)',
    titleEn: 'Project 7 — Camera-Equipped Explorer: Cards Bundle (Task)',
  },
  '8': {
    dir: 'Project_8_Tiny_Quadcopter',
    outBase: 'Project_8_Cards',
    titleHe: 'פרויקט 8 — רחפן זעיר: חוברת כרטיסיות (משימה)',
    titleEn: 'Project 8 — Tiny ESP32 Quadcopter: Cards Bundle (Task)',
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
    'T:T2_M2a_wire_second_led',
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
  '5': [
    'T:T1_M1_prepare_esp32',
    'T:T1_M2_swap_brain',
    'T:T1_M3_rewire_driver',
    'T:T1_M4_upload_drive',
    'T:T1_M5_connect_phone',
    'T:T1_M6_first_drive',
    'T:T1_M7_course_celebrate',
    'T:T2_M1_startup',
    'T:T2_M2_car_identity',
    'T:T2_M3_speed_profile',
    'T:T2_M4_page_design',
    'T:T2_M5_layout_with_claude',
    'T:T2_M6_signature_drive',
    'T:T3_project_planner',
  ],
  '6': [
    'T:T1_M1_toolchain_and_libraries',
    'T:T1_M2_wire_dht22',
    'T:T1_M3_upload_sensor_serial',
    'T:T1_M4_wire_oled_i2c',
    'T:T1_M5_upload_screen',
    'T:T1_M6_upload_wifi_connect',
    'T:T1_M7_live_page',
    'T:T1_M8_show_celebrate',
    'T:T2_M1_startup',
    'T:T2_M2_pick_output',
    'T:T2_M3_set_threshold',
    'T:T2_M4_page_style_with_claude',
    'T:T2_M5_station_identity',
    'T:T2_M6_signature_station',
    'T:T3_project_planner',
  ],
  '7': [
    'T:T1_M1_meet_the_cam',
    'T:T1_M2_upload_camera_sketch',
    'T:T1_M3_first_stream',
    'T:T1_M4_mount_camera',
    'T:T1_M5_power_rail',
    'T:T1_M6_wire_motors',
    'T:T1_M7_drive_from_page',
    'T:T1_M8_drive_by_video',
    'T:T1_M9_exploration_celebrate',
    'T:T2_M1_startup',
    'T:T2_M2_explorer_identity',
    'T:T2_M3_speed_profile',
    'T:T2_M4_page_design',
    'T:T2_M5_interface_with_claude',
    'T:T2_M6_design_mission',
    'T:T2_M7_signature_exploration',
    'T:T3_project_planner',
  ],
  '8': [
    'R:R1_flight_safety',
    'T:T1_M1_meet_parts_contract',
    'T:T1_M2_press_fit_motors',
    'T:T1_M3_meet_mosfet_board',
    'T:T1_M4_mount_electronics',
    'T:T1_M5_power_tree',
    'T:T1_M6_motor_wiring',
    'T:T1_M7_signal_wiring',
    'T:T1_M8_pre_power_check',
    'T:T1_M9_upload_motor_test',
    'T:T1_M10_spin_no_props',
    'T:T1_M11_thrust_test',
    'T:T1_M12_upload_flight',
    'T:T1_M13_tethered_hover',
    'T:T1_M14_post_flight_celebrate',
    'T:T2_M1_startup',
    'T:T2_M2_solder_channel_1',
    'T:T2_M3_check_channel_1',
    'T:T2_M4_solder_channels_2_4',
    'T:T2_M5_tune_mt3608',
    'T:T2_M6_mount_and_wire',
    'T:T2_M7_pre_power_check',
    'T:T2_M8_upload_and_spin',
    'T:T2_M9_thrust_test',
    'T:T2_M10_choices_and_claude',
    'T:T2_M11_tethered_hover_tuning',
    'T:T2_M12_flight_sequence',
    'T:T2_M13_signature_flight',
    'T:T3_project_planner',
  ],
};

const P = PROJECTS[projectKey];
const projectDir = path.join(ROOT, 'Arduino_Projects', P.dir);
const refDir = path.join(projectDir, isHe ? 'reference_cards_he' : 'reference_cards');
const taskDir = path.join(projectDir, isHe ? 'task_cards_he' : 'task_cards');

// Resolve each stem to a real file: HE task cards prefer their .dc.html twin;
// reference cards and EN builds stay classic (resolveCardFile falls back).
const cardOrder = CARD_STEMS[projectKey].map((stem) => {
  const [kind, name] = stem.split(':');
  const dir = kind === 'R' ? refDir : taskDir;
  const key = kind === 'T' ? projectKey : null;
  return [dir, resolveCardFile(dir, name, suffix, key)];
});

const outName = `${P.outBase}${suffix}`;
const outHtml = path.join(OUT, `${outName}.html`);
const outPdf = path.join(OUT, `${outName}.pdf`);

const pageTitle = isHe ? P.titleHe : P.titleEn;

// Merge every card into one self-contained HTML file. Classic cards contribute
// their linked CSS + <style> + body; dc cards contribute their settled (post-JS)
// markup — all inline-styled — plus their helmet <style>. Identical <style>
// blocks are deduped and hoisted into the head.
async function buildMergedHtml(browser) {
  console.log(`[HTML] Merging ${cardOrder.length} cards into ${outHtml}`);
  const styleSet = new Map(); // scoped <style> block -> true (dedup, ordered)
  const cardSections = [];
  let anyDc = false;

  for (const [dir, file] of cardOrder) {
    const full = path.join(dir, file);
    if (!fs.existsSync(full)) { console.warn(`  SKIP (missing): ${file}`); continue; }
    const snap = await snapshotCardHtml(browser, full);
    if (snap.fonts) anyDc = true;
    // Scope every card's CSS to its own flavor wrapper so classic element rules
    // (h2 {}, table {}…) can't bleed onto the inline-styled dc cards and vice versa.
    const flavorClass = snap.fonts ? 'appendix-card--dc' : 'appendix-card--classic';
    const scopeSel = '.' + flavorClass;
    for (const m of (snap.styles || '').matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)) {
      const scoped = `<style>${scopeCss(m[1], scopeSel)}</style>`;
      if (!styleSet.has(scoped)) styleSet.set(scoped, true);
    }
    const d = snap.dir || (isHe ? 'rtl' : 'ltr');
    const l = snap.lang || (isHe ? 'he' : 'en');
    cardSections.push(
      `<section class="appendix-card ${flavorClass}" dir="${d}" lang="${l}" style="page-break-before: always;">${snap.body}</section>`
    );
    console.log(`  ok: ${file}`);
  }

  const sharedStyles = [...styleSet.keys()].join('\n');
  const wrapperDir = isHe ? 'rtl' : 'ltr';
  const wrapperLang = isHe ? 'he' : 'en';

  const merged = `<!doctype html>
<html lang="${wrapperLang}" dir="${wrapperDir}">
<head>
<meta charset="utf-8">
<title>${pageTitle}</title>
${anyDc ? DC_FONTS_LINK : ''}
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

async function buildMergedPdf(browser) {
  console.log(`[PDF] Rendering ${cardOrder.length} cards to PDF → ${outPdf}`);
  const out = await PDFDocument.create();
  for (const [dir, file] of cardOrder) {
    const full = path.join(dir, file);
    if (!fs.existsSync(full)) { console.warn(`  SKIP (missing): ${file}`); continue; }
    const buf = await renderCardPdf(browser, full);
    const doc = await PDFDocument.load(buf);
    const pages = await out.copyPages(doc, doc.getPageIndices());
    pages.forEach((pg) => out.addPage(pg));
    console.log(`  ok: ${file}`);
  }
  const bytes = await out.save();
  fs.writeFileSync(outPdf, bytes);
  console.log(`  Done: ${outPdf} (${out.getPageCount()} pages)`);
}

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  try {
    await buildMergedHtml(browser);
    await buildMergedPdf(browser);
  } finally {
    await browser.close();
  }
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
