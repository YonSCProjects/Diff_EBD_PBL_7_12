// Post-process Fritzing-exported breadboard SVGs to put both the GND rail and
// the +5V rail at the BOTTOM of the breadboard (where the Arduino's GND and 5V
// pins also live), rather than the default Fritzing convention of GND on top.
//
// Rail mapping (Half_breadboard_v2 has 4 INDEPENDENT power-rail buses):
//   Y rail (SVG y ≈  755)  TOP inner   — was GND, now unused for student wiring
//   Z rail (SVG y ≈  655)  TOP outer   — unused
//   X rail (SVG y ≈ 2455)  BOTTOM inner — NEW GND rail
//   W rail (SVG y ≈ 2555)  BOTTOM outer — POWER (+5V), unchanged
//
// What the .fzz source currently does:
//   - LED cathode jumpers: vertical from (col A, row N) → (col Y, row N)   [LONG, up to top rail]
//   - Arduino GND wire:    diagonal from Arduino-GND-pin → (col Y, row 3) [LONG, crosses signals]
//   - Pulldown jumper (w3, w5): col C row N → col Y row N                  [LONG, up to top rail]
//   - Arduino 5V wire (w3, w5): diagonal from Arduino-5V-pin → (col W, row 3)
//
// What we rewrite the SVG to show:
//   - Cathode jumpers and pulldown: vertical to X rail (just below col A/C). Short.
//   - Arduino GND wire: short direct diagonal to (col X, row 3) at SVG (3240.56, 2455.56).
//   - Arduino 5V wire: short direct diagonal to (col W, row 3) at SVG (3240.56, 2555.56).
//
// All wires now stay in the bottom strip of the canvas; no crossings.
//
// NOTE: The canonical fritzing_steps/Step*.fzz files still encode the wires as
// going to the Y rail. This post-processor only rewrites the EXPORTED SVG so the
// student-facing card image reflects the cleaner routing. Re-run after any
// future SVG re-export. If we ever update arduino_pbl_steps.py to use X rail
// natively, this script becomes a no-op.
//
// Usage:
//   node fix_wiring_svgs.js                       # process all w*_breadboard.svg
//   node fix_wiring_svgs.js path/to/single.svg    # process one file

const fs = require('fs');
const path = require('path');

const IMG_DIR = path.join(
  __dirname,
  'Arduino_Projects',
  'Project_1_Light_Signals',
  'images'
);

// SVG-pixel coordinates of the rails (derived empirically from the existing
// Fritzing exports — see comments above).
const Y_RAIL_Y = 755.556;
const X_RAIL_Y = 2455.56;
const W_RAIL_Y = 2555.56;
const COL_A_Y  = 2155.56;   // bottom-half component-area row (LED cathode side)

// Arduino-pin endpoints (start of the GND/5V wires emerging from the Arduino).
const ARD_GND_X = 1949.61;
const ARD_GND_Y = 2000;
const ARD_5V_X  = 1749.61;
const ARD_5V_Y  = 2000;

// Where the GND and 5V wires terminate on the breadboard (row 3 on each rail).
const RAIL_ROW3_X = 3240.56;

const TOL = 5;
function approxEq(a, b) { return Math.abs(a - b) <= TOL; }

// ---------- Replacement 1: vertical cathode/pulldown jumpers -----------------
// These are black vertical lines going from (X, COL_A_Y) up to (X, Y_RAIL_Y).
// Flip them so they go from (X, COL_A_Y) DOWN to (X, X_RAIL_Y).
function flipVerticalJumpers(svg) {
  const re = /<line stroke="#000000" stroke-linecap="round" stroke-width="([\d.]+)" x1="([\d.]+)" x2="([\d.]+)" y1="([\d.]+)" y2="([\d.]+)"\/>/g;
  let count = 0;
  const out = svg.replace(re, (match, w, x1, x2, y1, y2) => {
    const xx1 = parseFloat(x1), xx2 = parseFloat(x2);
    const yy1 = parseFloat(y1), yy2 = parseFloat(y2);
    // Must be a vertical line (x1 === x2) — diagonals are the Arduino-GND wire
    // (handled separately below).
    if (!approxEq(xx1, xx2)) return match;
    // Match (col A → Y rail) OR (col Y → col A); orientation can vary.
    const isCathodeToY =
      (approxEq(yy1, COL_A_Y) && approxEq(yy2, Y_RAIL_Y)) ||
      (approxEq(yy1, Y_RAIL_Y) && approxEq(yy2, COL_A_Y));
    if (!isCathodeToY) return match;
    count++;
    // Always render new wire as (col A, top end of the visible jumper) → (X rail).
    return `<line stroke="#000000" stroke-linecap="round" stroke-width="${w}" x1="${x1}" x2="${x2}" y1="${COL_A_Y}" y2="${X_RAIL_Y}"/>`;
  });
  return { svg: out, count };
}

// ---------- Replacement 2: Arduino GND wire ----------------------------------
// In the current SVG (after previous fix_wiring_svgs.js runs), the GND wire is a
// polyline arcing over the top to Y rail. We want it as a short direct line
// from Arduino-GND-pin to (col X, row 3) at the BOTTOM.
function rerouteGndWire(svg) {
  let count = 0;
  // Match either the over-the-top polyline (left from previous fix) OR the
  // original Fritzing-export straight line to Y rail.
  const polyRe = /<polyline fill="none" stroke="#000000" stroke-linecap="round" stroke-linejoin="round" stroke-width="([\d.]+)" points="1949\.61,2000 1500,2000 1500,50 5440,50 5440,755\.556"\/>/g;
  const lineRe = /<line stroke="#000000" stroke-linecap="round" stroke-width="([\d.]+)" x1="1949\.61" x2="3240\.56" y1="2000" y2="755\.556"\/>/g;
  let out = svg.replace(polyRe, (m, w) => {
    count++;
    return `<line stroke="#000000" stroke-linecap="round" stroke-width="${w}" x1="${ARD_GND_X}" x2="${RAIL_ROW3_X}" y1="${ARD_GND_Y}" y2="${X_RAIL_Y}"/>`;
  });
  out = out.replace(lineRe, (m, w) => {
    count++;
    return `<line stroke="#000000" stroke-linecap="round" stroke-width="${w}" x1="${ARD_GND_X}" x2="${RAIL_ROW3_X}" y1="${ARD_GND_Y}" y2="${X_RAIL_Y}"/>`;
  });
  return { svg: out, count };
}

// ---------- Replacement 3: Arduino 5V wire (w3, w5 only) ---------------------
// Currently a polyline (1749.61,2000 → 1749.61,2555.56 → 3240.56,2555.56) from
// the previous fix; replace with a short direct diagonal to W rail row 3.
function rerouteFiveVWire(svg) {
  let count = 0;
  const polyRe = /<polyline fill="none" stroke="#cc1414" stroke-linecap="round" stroke-linejoin="round" stroke-width="([\d.]+)" points="1749\.61,2000 1749\.61,2555\.56 3240\.56,2555\.56"\/>/g;
  const lineRe = /<line stroke="#cc1414" stroke-linecap="round" stroke-width="([\d.]+)" x1="1749\.61" x2="3240\.56" y1="2000" y2="2555\.56"\/>/g;
  let out = svg.replace(polyRe, (m, w) => {
    count++;
    return `<line stroke="#cc1414" stroke-linecap="round" stroke-width="${w}" x1="${ARD_5V_X}" x2="${RAIL_ROW3_X}" y1="${ARD_5V_Y}" y2="${W_RAIL_Y}"/>`;
  });
  out = out.replace(lineRe, (m, w) => {
    count++;
    return `<line stroke="#cc1414" stroke-linecap="round" stroke-width="${w}" x1="${ARD_5V_X}" x2="${RAIL_ROW3_X}" y1="${ARD_5V_Y}" y2="${W_RAIL_Y}"/>`;
  });
  return { svg: out, count };
}

// ---------- Replacement 4: resistor legs ------------------------------------
// In Fritzing's resistor part SVG, the breadboard-hole row (connector pin) is at
// local y=40.9 while the body's center wire is drawn at y=50.45. The legs are
// horizontal stubs at the wire's y, so visually they look ~10px LOW relative to
// the holes they're supposed to enter. They also use #8C8C8C (light gray) which
// blends into the breadboard.
//
// We rewrite each leg as a short DIAGONAL from the pin center down to the body's
// wire-line, and switch to a darker color so the leg reads as a discrete wire
// emerging from the hole rather than blending into the background.
function fixResistorLegs(svg) {
  let count = 0;
  // connector0 (LEFT pin): pin center local (10, 40.9), body wire starts at (29.1, 50.45)
  const reg0 = /<line fill="none" id="connector0leg" stroke="#8C8C8C" stroke-linecap="round" stroke-width="29\.1" x1="14\.55" x2="29\.1"  y1="50\.45" y2="50\.45"\/>/g;
  // connector1 (RIGHT pin): pin center local (419.17, 40.9), body wire ends at (400.07, 50.45)
  const reg1 = /<line fill="none" id="connector1leg" stroke="#8C8C8C" stroke-linecap="round" stroke-width="29\.1" x1="414\.62" x2="400\.07"  y1="50\.45" y2="50\.45"\/>/g;
  let out = svg.replace(reg0, () => {
    count++;
    return '<line fill="none" id="connector0leg" stroke="#404040" stroke-linecap="round" stroke-width="29.1" x1="10" x2="29.1" y1="40.9" y2="50.45"/>';
  });
  out = out.replace(reg1, () => {
    count++;
    return '<line fill="none" id="connector1leg" stroke="#404040" stroke-linecap="round" stroke-width="29.1" x1="419.17" x2="400.07" y1="40.9" y2="50.45"/>';
  });
  return { svg: out, count };
}

function processFile(filePath) {
  const fileName = path.basename(filePath);
  console.log(`  ${fileName}`);
  let svg = fs.readFileSync(filePath, 'utf8');
  let total = 0;

  let r = flipVerticalJumpers(svg);
  svg = r.svg;
  total += r.count;
  if (r.count) console.log(`    cathode/pulldown jumpers flipped to X rail: ${r.count}`);

  r = rerouteGndWire(svg);
  svg = r.svg;
  total += r.count;
  if (r.count) console.log(`    Arduino GND wire rerouted to X rail row 3: ${r.count} line(s)`);

  r = rerouteFiveVWire(svg);
  svg = r.svg;
  total += r.count;
  if (r.count) console.log(`    Arduino 5V wire simplified to direct diagonal: ${r.count} line(s)`);

  r = fixResistorLegs(svg);
  svg = r.svg;
  total += r.count;
  if (r.count) console.log(`    resistor legs realigned to hole + darkened: ${r.count} leg(s)`);

  if (total > 0) {
    fs.writeFileSync(filePath, svg, 'utf8');
    console.log(`    Wrote ${fileName} (${total} edit(s))`);
  } else {
    console.log(`    No matching wires found — file unchanged`);
  }
}

function main() {
  const arg = process.argv[2];
  const files = arg
    ? [path.resolve(arg)]
    : fs
        .readdirSync(IMG_DIR)
        .filter((f) => /^w\d.*_breadboard\.svg$/.test(f))
        .sort()
        .map((f) => path.join(IMG_DIR, f));

  if (files.length === 0) {
    console.error('No matching SVG files found');
    process.exit(1);
  }
  console.log(`Processing ${files.length} file(s):`);
  for (const f of files) processFile(f);
}

main();
