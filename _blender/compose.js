#!/usr/bin/env node
/**
 * compose.js — hangs the Hebrew callouts on a render, and emits one self-contained SVG.
 *
 *   node compose.js <render.png> <callouts.json> <out.svg>
 *
 * The PNG goes in as a base64 <image>; the callouts are drawn as vector text over it. That keeps
 * a wording change a one-second re-compose instead of a two-minute re-render, and keeps the type
 * crisp at print size.
 *
 * Three things this does that the first version did not, each fixing a defect that shipped:
 *
 * 1. THE FONT TRAVELS WITH THE FIGURE. These SVGs are loaded by the cards through <img src>, and
 *    an <img>-loaded SVG renders in a restricted mode: the document's webfonts do not reach it.
 *    Naming 'Rubik' in font-family therefore did nothing — every callout in every published
 *    figure was falling back to Segoe UI or Arial while the card body was Rubik. The two Rubik
 *    subsets are now embedded as data: URIs inside the SVG, which IS honoured inside <img>.
 *
 * 2. BOXES ARE MEASURED, NOT GUESSED. Width used to be `longest line * size * 0.56`, an average
 *    guessed for a font the figure never actually got. Real per-glyph advances now come from
 *    fonts/rubik700-widths.json, so a box fits its text.
 *
 * 3. LABELS AVOID THE SUBJECT AND EACH OTHER. The renders have a transparent background, so the
 *    alpha channel is an exact mask of where the hardware is. A label is placed on empty pixels
 *    where it can be, never on top of another label, and leaders are discouraged from crossing.
 *    The author's dx/dy stays the strong prior — it only moves when it has to.
 *
 * Colours come from the card's own oklch tokens so a figure reads as native to the page it sits
 * on rather than as clip-art dropped into it.
 */
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const [pngPath, calloutPath, outPath] = process.argv.slice(2);
if (!pngPath || !calloutPath || !outPath) {
  console.error('usage: node compose.js <render.png> <callouts.json> <out.svg>');
  process.exit(2);
}

const FONTS = path.join(__dirname, 'fonts');
const spec = JSON.parse(fs.readFileSync(calloutPath, 'utf8'));
const metaPath = pngPath.replace(/\.png$/i, '.anchors.json');
const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
const W = meta.width, H = meta.height;
const K = W / 1200;                      // callout sizes are authored against a 1200px frame

/* ---------- palette, straight off the card's oklch tokens ---------- */
const C = {
  ink:    '#25292f',   // oklch(0.28 0.012 260)  card body text
  rule:   '#2d333d',   // oklch(0.32 0.02 260)   box border + leader
  ring:   '#da7e1e',   // oklch(0.68 0.15 60)    anchor ring, the card's amber
  badge:  '#14588f',   // oklch(0.45 0.11 248)   brand blue, numbered badges
  paper:  '#ffffff',
};

/* ---------- text measurement against the real font ---------- */
const WT = JSON.parse(fs.readFileSync(path.join(FONTS, 'rubik700-widths.json'), 'utf8'));
function advance(ch) {
  const w = WT.w[ch.codePointAt(0)];
  return w === undefined ? WT.default : w;
}
function textWidth(s, size) {
  let t = 0;
  for (const ch of s) t += advance(ch);
  return t * size;
}

/* ---------- a minimal RGBA PNG reader, so the alpha channel can be used as a subject mask ----
   Blender writes 8-bit RGBA, non-interlaced, which is all this needs to handle. If the file is
   anything else the mask degrades to "everything is empty", which just restores the old
   author-hint-only placement rather than breaking the build. */
function alphaGrid(buf, cols, rows) {
  try {
    let p = 8, w = 0, h = 0, bitDepth = 0, colourType = 0, interlace = 0;
    const idat = [];
    while (p < buf.length) {
      const len = buf.readUInt32BE(p);
      const type = buf.toString('ascii', p + 4, p + 8);
      const data = buf.slice(p + 8, p + 8 + len);
      if (type === 'IHDR') {
        w = data.readUInt32BE(0); h = data.readUInt32BE(4);
        bitDepth = data[8]; colourType = data[9]; interlace = data[12];
      } else if (type === 'IDAT') idat.push(data);
      else if (type === 'IEND') break;
      p += 12 + len;
    }
    if (bitDepth !== 8 || colourType !== 6 || interlace !== 0) return null;
    const raw = zlib.inflateSync(Buffer.concat(idat));
    const bpp = 4, stride = w * bpp;
    const grid = new Float32Array(cols * rows);
    const count = new Float32Array(cols * rows);
    let prev = Buffer.alloc(stride);
    let off = 0;
    for (let y = 0; y < h; y++) {
      const filter = raw[off++];
      const line = Buffer.from(raw.slice(off, off + stride)); off += stride;
      for (let x = 0; x < stride; x++) {
        const a = x >= bpp ? line[x - bpp] : 0;
        const b = prev[x];
        const c = x >= bpp ? prev[x - bpp] : 0;
        let v = line[x];
        if (filter === 1) v += a;
        else if (filter === 2) v += b;
        else if (filter === 3) v += (a + b) >> 1;
        else if (filter === 4) {
          const pp = a + b - c, pa = Math.abs(pp - a), pb = Math.abs(pp - b), pc = Math.abs(pp - c);
          v += (pa <= pb && pa <= pc) ? a : (pb <= pc ? b : c);
        }
        line[x] = v & 0xff;
      }
      prev = line;
      const gy = Math.min(rows - 1, Math.floor(y * rows / h));
      for (let x = 0; x < w; x++) {
        const gx = Math.min(cols - 1, Math.floor(x * cols / w));
        grid[gy * cols + gx] += line[x * bpp + 3] / 255;
        count[gy * cols + gx] += 1;
      }
    }
    for (let i = 0; i < grid.length; i++) grid[i] = count[i] ? grid[i] / count[i] : 0;
    return { cols, rows, grid };
  } catch (e) {
    console.warn('  (alpha mask unavailable:', e.message + ') — falling back to author offsets');
    return null;
  }
}

const pngBuf = fs.readFileSync(pngPath);
const GC = 64, GR = 48;
const mask = alphaGrid(pngBuf, GC, GR);

/** How much hardware a rectangle covers, 0 (empty) .. 1 (solid). */
function subjectCost(x0, y0, x1, y1) {
  if (!mask) return 0;
  let s = 0, n = 0;
  const gx0 = Math.max(0, Math.floor(x0 * GC / W)), gx1 = Math.min(GC - 1, Math.floor(x1 * GC / W));
  const gy0 = Math.max(0, Math.floor(y0 * GR / H)), gy1 = Math.min(GR - 1, Math.floor(y1 * GR / H));
  for (let gy = gy0; gy <= gy1; gy++) for (let gx = gx0; gx <= gx1; gx++) { s += mask.grid[gy * GC + gx]; n++; }
  return n ? s / n : 0;
}

/* ---------- geometry helpers ---------- */
const overlap = (a, b) => !(a.x1 <= b.x0 || b.x1 <= a.x0 || a.y1 <= b.y0 || b.y1 <= a.y0);
function overlapArea(a, b) {
  const w = Math.min(a.x1, b.x1) - Math.max(a.x0, b.x0);
  const h = Math.min(a.y1, b.y1) - Math.max(a.y0, b.y0);
  return (w > 0 && h > 0) ? w * h : 0;
}
function segsCross(p1, p2, p3, p4) {
  const d = (a, b, c) => (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
  const d1 = d(p3, p4, p1), d2 = d(p3, p4, p2), d3 = d(p1, p2, p3), d4 = d(p1, p2, p4);
  return ((d1 > 0) !== (d2 > 0)) && ((d3 > 0) !== (d4 > 0));
}
/** Where a leader should meet its box: the edge point facing the anchor, not the centre. */
function boxPort(box, from) {
  const cx = (box.x0 + box.x1) / 2, cy = (box.y0 + box.y1) / 2;
  const dx = from.x - cx, dy = from.y - cy;
  if (!dx && !dy) return { x: cx, y: cy };
  const hw = (box.x1 - box.x0) / 2, hh = (box.y1 - box.y0) / 2;
  const t = Math.min(hw / Math.abs(dx || 1e-6), hh / Math.abs(dy || 1e-6));
  return { x: cx + dx * t, y: cy + dy * t };
}

/* ---------- build the label list ---------- */
const edge = 10 * K;
const items = [];
for (const it of spec.items || []) {
  const a = meta.anchors[it.anchor];
  if (!a) { console.warn('  no such anchor:', it.anchor); continue; }
  if (a.onscreen === false || a.depth <= 0) {
    console.warn('  SKIPPED (anchor off-screen):', it.anchor, '-', String(it.he).split('\n')[0]);
    continue;
  }
  if (a.visible === false) {
    // lib.py ray-casts every anchor. A label whose part is hidden behind other geometry points at
    // a blank surface and reads as a mistake — the figure needs a different camera, not a nudge.
    console.warn('  HIDDEN (anchor behind geometry):', it.anchor, '-', String(it.he).split('\n')[0]);
  }
  const size = (it.size || 19) * K;
  const lines = String(it.he).split('\n');
  const pad = size * 0.62, lh = size * 1.34;
  const bw = Math.max(...lines.map(l => textWidth(l, size))) + pad * 2;
  const bh = lines.length * lh + pad * 1.25;
  items.push({ it, a, size, lines, pad, lh, bw, bh, hint: { dx: (it.dx || 0) * K, dy: (it.dy || 0) * K } });
}

/** Candidate centres for one label.
 *
 *  A ring of offsets around the anchor was not enough: near an edge every candidate clamps to
 *  the same place, so two labels would land on top of each other and the solver had nowhere
 *  better to go. Scanning the whole frame always leaves somewhere to put a box. The author's
 *  dx/dy is still the strong prior — it is offered first and everything else pays for how far
 *  it strays from it, so a hand-tuned offset only loses when it genuinely collides. */
function candidates(m) {
  const out = [];
  const hx = m.a.x + m.hint.dx, hy = m.a.y + m.hint.dy;
  const clamp = (cx, cy) => ({
    cx: Math.min(Math.max(cx, m.bw / 2 + edge), W - m.bw / 2 - edge),
    cy: Math.min(Math.max(cy, m.bh / 2 + edge), H - m.bh / 2 - edge),
  });
  const span = Math.hypot(W, H);
  const push = (cx, cy) => {
    const c = clamp(cx, cy);
    out.push({ cx: c.cx, cy: c.cy, penalty: Math.hypot(c.cx - hx, c.cy - hy) / span });
  };
  push(hx, hy);                                        // exactly what the author asked for
  const NX = 22, NY = 16;
  for (let iy = 0; iy < NY; iy++) {
    for (let ix = 0; ix < NX; ix++) {
      push(edge + m.bw / 2 + (ix / (NX - 1)) * Math.max(0, W - m.bw - 2 * edge),
           edge + m.bh / 2 + (iy / (NY - 1)) * Math.max(0, H - m.bh - 2 * edge));
    }
  }
  return out;
}

/* Greedy placement, longest label first — the big boxes are the ones with nowhere to go — then a
   few improvement sweeps so an early choice can give way to a later one. */
const order = items.map((m, i) => i).sort((a, b) => items[b].bw * items[b].bh - items[a].bw * items[a].bh);
const placed = new Array(items.length).fill(null);

function score(i, cand) {
  const m = items[i];
  const box = { x0: cand.cx - m.bw / 2, y0: cand.cy - m.bh / 2, x1: cand.cx + m.bw / 2, y1: cand.cy + m.bh / 2 };
  let s = cand.penalty * 1.05;                                     // stay near the author's offset
  s += subjectCost(box.x0, box.y0, box.x1, box.y1) * 6.0;          // don't cover the hardware
  // The boards carry printed pin numbers now, so covering hardware hides information a student
  // is being asked to read. Worth a longer leader almost every time.
  const port = boxPort(box, m.a);
  const len = Math.hypot(port.x - m.a.x, port.y - m.a.y);
  s += (len / Math.max(W, H)) * 1.3;                                // keep leaders short
  if (len < 14 * K) s += 0.8;                                       // but not zero-length
  const gap = 6 * K;                                                // breathing room between boxes
  const grown = { x0: box.x0 - gap, y0: box.y0 - gap, x1: box.x1 + gap, y1: box.y1 + gap };
  for (let j = 0; j < items.length; j++) {
    if (j === i) continue;
    const o = placed[j];
    // A label must never sit on another label. Weighted far above every other term so the
    // solver will accept a long leader or an awkward corner rather than an overlap.
    if (o) s += (overlapArea(grown, o.box) / (m.bw * m.bh)) * 26.0;
    if (o && segsCross(m.a, port, items[j].a, o.port)) s += 1.6;    // leaders shouldn't cross
    // and it must not bury another callout's ring, which is the thing being pointed at
    const r = 9 * K, aj = items[j].a;
    if (aj.x > box.x0 - r && aj.x < box.x1 + r && aj.y > box.y0 - r && aj.y < box.y1 + r) s += 2.2;
  }
  if (m.a.x > box.x0 && m.a.x < box.x1 && m.a.y > box.y0 && m.a.y < box.y1) s += 3.0;  // not on its own ring
  return { s, box, port };
}

for (const i of order) {
  let best = null;
  for (const cand of candidates(items[i])) {
    const r = score(i, cand);
    if (!best || r.s < best.s) best = r;
  }
  placed[i] = best;
}
for (let pass = 0; pass < 6; pass++) {
  for (const i of order) {
    const keep = placed[i]; placed[i] = null;
    let best = null;
    for (const cand of candidates(items[i])) {
      const r = score(i, cand);
      if (!best || r.s < best.s) best = r;
    }
    placed[i] = (best && best.s < keep.s - 1e-6) ? best : keep;
  }
}

/* ---------- draw ---------- */
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
let layer = '';
items.forEach((m, i) => {
  const p = placed[i];
  const { box, port } = p;
  layer += `<line x1="${m.a.x.toFixed(1)}" y1="${m.a.y.toFixed(1)}" x2="${port.x.toFixed(1)}" y2="${port.y.toFixed(1)}" `
    + `stroke="${C.rule}" stroke-width="${(1.5 * K).toFixed(2)}" stroke-dasharray="${(4.5 * K).toFixed(2)} ${(3.5 * K).toFixed(2)}" stroke-opacity="0.85"/>`;
  layer += `<circle cx="${m.a.x.toFixed(1)}" cy="${m.a.y.toFixed(1)}" r="${(4.5 * K).toFixed(2)}" `
    + `fill="none" stroke="${m.it.ring || C.ring}" stroke-width="${(2.4 * K).toFixed(2)}"/>`;
  layer += `<rect x="${box.x0.toFixed(1)}" y="${box.y0.toFixed(1)}" width="${m.bw.toFixed(1)}" height="${m.bh.toFixed(1)}" `
    + `rx="${(m.size * 0.42).toFixed(1)}" fill="${C.paper}" fill-opacity="0.97" stroke="${C.rule}" `
    + `stroke-width="${(1.6 * K).toFixed(2)}"/>`;
  const cx = (box.x0 + box.x1) / 2;
  m.lines.forEach((l, k) => {
    const ty = box.y0 + m.pad * 0.62 + m.lh * (k + 0.78);
    layer += `<text x="${cx.toFixed(1)}" y="${ty.toFixed(1)}" font-family="RubikFig" `
      + `font-size="${m.size.toFixed(1)}" font-weight="700" fill="${C.ink}" text-anchor="middle" `
      + `direction="rtl">${esc(l)}</text>`;
  });
});

/* numbered badges, unchanged in meaning, restyled to the card's blue */
for (const b of spec.badges || []) {
  const a = meta.anchors[b.anchor];
  if (!a || a.onscreen === false) { console.warn('  badge skipped:', b.anchor); continue; }
  const r = (b.r || 15) * K;
  const bx = a.x + (b.dx || 0) * K, by = a.y + (b.dy || 0) * K;
  layer += `<circle cx="${bx.toFixed(1)}" cy="${by.toFixed(1)}" r="${r.toFixed(1)}" fill="${C.badge}"/>`;
  layer += `<text x="${bx.toFixed(1)}" y="${(by + r * 0.36).toFixed(1)}" font-family="RubikFig" `
    + `font-size="${(r * 1.18).toFixed(1)}" font-weight="800" fill="#ffffff" `
    + `text-anchor="middle">${esc(b.n)}</text>`;
}

const png = pngBuf.toString('base64');
const heb = fs.readFileSync(path.join(FONTS, 'rubik700-hebrew.woff2')).toString('base64');
const lat = fs.readFileSync(path.join(FONTS, 'rubik700-latin.woff2')).toString('base64');
const face = (b64, range) => `@font-face{font-family:'RubikFig';font-style:normal;font-weight:700;`
  + `src:url(data:font/woff2;base64,${b64}) format('woff2');unicode-range:${range};}`;

const svg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" `
  + `viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">\n`
  + `<defs><style type="text/css">\n`
  + face(heb, 'U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F') + `\n`
  + face(lat, 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215') + `\n`
  + `</style></defs>\n`
  + `<image x="0" y="0" width="${W}" height="${H}" xlink:href="data:image/png;base64,${png}"/>\n`
  + layer + `\n</svg>\n`;

fs.writeFileSync(outPath, svg, 'utf8');
console.log('  composed', path.basename(outPath), `(${items.length} callouts, ${(svg.length / 1048576).toFixed(1)} MB)`);
