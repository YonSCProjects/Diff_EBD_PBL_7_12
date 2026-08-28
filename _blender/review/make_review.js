#!/usr/bin/env node
/**
 * make_review.js — build a local review page for the step figures of one or more projects.
 *
 *   node _blender/review/make_review.js > build_output/figure_review.html
 *
 * It references the live SVGs relatively, so the file stays a few kilobytes and always shows
 * whatever is currently published. Each figure is shown at the width it occupies in the card,
 * so what you are judging is what a student sees on the page rather than a zoomed-in crop.
 */
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const PROJECTS = [
  ['Project 4 — Line-Following Car', 'Project_4_Line_Following_Car',
   ['w_p4_m3_step1','w_p4_m3_step2','w_p4_m3_step3','w_p4_m3_step4','w_p4_m3_step5','w_p4_m3_step6','w_p4_m3_step7',
    'w_p4_s01_soldering_station','w_p4_s02_solder_motor_leads','w_p4_s03a_cut_plate','w_p4_s03b_glue_motors',
    'w_p4_s03c_wheels_on','w_p4_s04_wiring','w_p4_s05_wheels_in_air','w_p4_s06_sensor_test','w_p4_s07_track','w_p4_s08_first_run']],
  ['Project 5 — Remote-Controlled Car', 'Project_5_Remote_Controlled_Car',
   ['w_p5_s01_meet_esp32','w_p5_s02_swap_brain','w_p5_s03_rewire','w_p5_s04_upload','w_p5_s05_connect_phone','w_p5_s06_first_drive','w_p5_s07_course']],
  ['Project 7 — Camera Explorer', 'Project_7_Camera_Explorer',
   ['w_p7_s01_ftdi_upload','w_p7_s02_upload_ritual','w_p7_s03_first_stream','w_p7_s04_mount_camera',
    'w_p7_s05_power_rails','w_p7_s06_cam_to_driver','w_p7_s07_drive_from_page','w_p7_s08_drive_by_video']],
];
const CHANGED = {
  w_p4_m3_step2: 'masking tape removed — it was not in the step',
  w_p4_m3_step3: 'the drill was upside down; it now stands on its bit',
  w_p4_m3_step4: 'the motor being placed was a bare box — it is the real part now, lifted clear',
  w_p4_m3_step5: 'motors glued, not screwed; re-centred',
  w_p4_m3_step6: 'shot from higher up so the Uno, the L298N and the battery box separate',
  w_p4_m3_step7: 'the sensors were hidden under the plate — new low view from the front',
  w_p4_s03a_cut_plate: 'masking tape removed',
  w_p4_s03c_wheels_on: 'callout no longer says the motors are screwed',
};
let rows = '';
for (const [title, dir, figs] of PROJECTS) {
  rows += `\n<h2>${title}</h2>\n<div class="grid">\n`;
  for (const f of figs) {
    const rel = `../Arduino_Projects/${dir}/task_cards_he/assets/${f}.svg`;
    const abs = path.join(ROOT, 'Arduino_Projects', dir, 'task_cards_he', 'assets', f + '.svg');
    const ok = fs.existsSync(abs);
    const note = CHANGED[f] ? `<p class="note">${CHANGED[f]}</p>` : '';
    rows += `  <figure${ok ? '' : ' class="missing"'}>
    <img src="${rel}" alt="${f}" loading="lazy">
    <figcaption><code>${f}.svg</code>${ok ? '' : ' <b>— MISSING</b>'}${note}</figcaption>
  </figure>\n`;
  }
  rows += '</div>\n';
}
const html = `<!doctype html><html lang="he"><head><meta charset="utf-8">
<title>Step figures — review</title>
<style>
 :root{--ink:#25292f;--muted:#6b7280;--line:#e6e4e0;--page:#f8f5f0}
 body{margin:0;background:var(--page);color:var(--ink);
      font:16px/1.55 Rubik,"Segoe UI",system-ui,sans-serif;padding:32px clamp(16px,4vw,56px)}
 h1{font-size:26px;margin:0 0 6px} h2{font-size:19px;margin:38px 0 14px;font-weight:700}
 .lede{color:var(--muted);max-width:64ch;margin:0 0 8px}
 .grid{display:grid;gap:22px;grid-template-columns:repeat(auto-fill,minmax(560px,1fr))}
 figure{margin:0;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}
 figure.missing{outline:2px solid #c0392b}
 img{display:block;width:100%;height:auto;background:#fff}
 figcaption{padding:10px 14px;border-top:1px solid var(--line);font-size:13px;color:var(--muted)}
 code{font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12.5px;color:var(--ink)}
 .note{margin:5px 0 0;color:#0f7b4f;font-size:12.5px}
 @media (max-width:700px){.grid{grid-template-columns:1fr}}
</style></head><body>
<h1>Step figures — Projects 4, 5 and 7</h1>
<p class="lede">Each figure is shown at roughly the width it occupies in a card, so this is what a
student sees on the page. Green notes mark figures whose content changed, not just their labels.</p>
${rows}</body></html>`;
process.stdout.write(html);
