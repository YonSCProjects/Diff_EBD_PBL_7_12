// Post-process a kit-composited wiring SVG for print:
//   1. drop the Fritzing watermark — on several figures it sits on top of real parts
//   2. scale the composited callout labels so they reach a readable size once a dc card
//      renders the figure at 640 px, whatever extent the sketch itself spans.
// Labels come from _fritzing_kit/compose.js as a rounded <rect ... opacity="0.96"/> followed
// by its <text>; each pair is scaled about its own centre so its leader still lands right.
const fs = require('fs');

const CARD_PX = 640;      // width a dc card gives a figure
const TARGET_PX = 8.0;    // on-card cap height we want a label to reach (~2.1 mm at A4)
const MAX_K = 2.2;        // past this a label starts to swamp the artwork it sits on

// <g id="watermark"> holds nested <g>s, so a non-greedy match to the first </g> truncates it
// and leaves orphan closers behind — walk the nesting instead.
function stripWatermark(s) {
  const open = s.search(/<g[^>]*id="watermark"[^>]*>/);
  if (open < 0) return { s, cut: false };
  const tagEnd = s.indexOf('>', open) + 1;
  let depth = 1, i = tagEnd;
  const re = /<g\b[^>]*?(\/?)>|<\/g>/g;
  re.lastIndex = tagEnd;
  let m;
  while (depth > 0 && (m = re.exec(s))) {
    if (m[0] === '</g>') depth--;
    else if (m[1] !== '/') depth++;
    i = re.lastIndex;
  }
  if (depth !== 0) return { s, cut: false };
  return { s: s.slice(0, open) + s.slice(i), cut: true };
}

const PAIR = /<rect x="([-\d.]+)" y="([-\d.]+)" width="([\d.]+)" height="([\d.]+)"[^>]*opacity="0\.96"\/>\s*<text[^>]*font-size="([\d.]+)"[^>]*>[\s\S]*?<\/text>/g;

const MARK = 'data-print-scaled';

// Undo a previous polish so the script can be re-tuned in place. Without this a second run is a
// no-op, and the only way to change the scaling was a full Fritzing rebuild of the figure — slow,
// and impossible at all on a machine without Fritzing installed. The label wrapper holds nothing
// but the rect+text pair, so a non-greedy match to the first </g> is exact; the pre-growth
// viewBox is recorded on the <svg> below when it grows.
function unpolish(s) {
  if (!s.includes(MARK)) return s;
  s = s.replace(new RegExp('<g ' + MARK + '="1" transform="[^"]*">([\\s\\S]*?)<\\/g>', 'g'), '$1');
  const m = s.match(/\sdata-print-vb0="([^"]+)"/);
  if (m) {
    const [x, y, ww, hh] = m[1].trim().split(/\s+/);
    s = s.replace(/viewBox="[^"]+"/, `viewBox="${m[1]}"`);
    s = s.replace(/<rect x="[-\d.]+" y="[-\d.]+" width="[\d.]+" height="[\d.]+" fill="#ffffff"\/>/,
      `<rect x="${x}" y="${y}" width="${ww}" height="${hh}" fill="#ffffff"/>`);
    s = s.replace(/\sdata-print-vb0="[^"]*"/, '');
  }
  return s;
}

function polish(file) {
  let s = fs.readFileSync(file, 'utf8');
  const w = stripWatermark(s); s = w.s;
  // Already polished: the label pairs still match PAIR (the scale lives on a wrapper, not on
  // font-size), so scaling again on top would compound. Undo the previous pass instead of
  // bailing out, which makes the script re-runnable and its constants re-tunable.
  const wasPolished = s.includes(MARK);
  s = unpolish(s);
  const vw = Number(s.match(/viewBox="([-\d.]+)\s+([-\d.]+)\s+([\d.]+)\s+([\d.]+)"/)[3]);
  const first = new RegExp(PAIR.source).exec(s);
  if (!first) return { s, cut: w.cut, n: 0, px: null, wasPolished };
  const px = Number(first[5]) / vw * CARD_PX;
  // Collect the labels first: a tag with room around it can take the full scale, but a tight
  // cluster (the IN1..IN4 pins on an L298N, say) has to settle for less or it just becomes a
  // pile. Each label gets the largest scale that does not push it into a neighbour it was
  // clear of at 1x.
  //
  // Each label is scaled from ITS OWN font-size. Deriving one factor from the FIRST label and
  // applying it to all of them is what left the small tags unreadable: on w_p4_01_driver_wiring
  // the first label is "LEFT MOTORS" at size 80, which needs only 2.2x to clear the target, so
  // the size-54 pin tags beside it were handed 2.2x as well and stayed under 3 px on the card.
  // A label that starts smaller has to grow MORE, not the same.
  const labels = [];
  s.replace(PAIR, (whole, x, y, ww, hh, fsz) => {
    const ownPx = Number(fsz) / vw * CARD_PX;
    labels.push({
      x: Number(x), y: Number(y), w: Number(ww), h: Number(hh), px: ownPx,
      k: Math.min(MAX_K, Math.max(1, TARGET_PX / ownPx)),
    });
    return whole;
  });
  if (!labels.some(L => L.k > 1.02)) {
    return { s, cut: w.cut, n: labels.length, px, wasPolished, kmin: 1, kmax: 1,
             worst: Math.min(...labels.map(L => L.px)) };
  }
  const boxAt = (L, kk) => {
    const cx = L.x + L.w / 2, cy = L.y + L.h / 2;
    return [cx - L.w / 2 * kk, cy - L.h / 2 * kk, cx + L.w / 2 * kk, cy + L.h / 2 * kk];
  };
  const hits = (a, b) => a[0] < b[2] && b[0] < a[2] && a[1] < b[3] && b[1] < a[3];
  const clearAt1 = labels.map((L, i) => labels.map((M, j) =>
    i === j ? false : !hits(boxAt(L, 1), boxAt(M, 1))));
  for (let pass = 0; pass < 40; pass++) {
    let changed = false;
    for (let i = 0; i < labels.length; i++) {
      for (let j = i + 1; j < labels.length; j++) {
        if (!clearAt1[i][j]) continue;                       // already touching at 1x: leave them
        if (!hits(boxAt(labels[i], labels[i].k), boxAt(labels[j], labels[j].k))) continue;
        for (const L of [labels[i], labels[j]]) {
          if (L.k > 1.0) { L.k = Math.max(1.0, L.k - 0.05); changed = true; }
        }
      }
    }
    if (!changed) break;
  }

  let n = 0;
  const box = { x0: Infinity, y0: Infinity, x1: -Infinity, y1: -Infinity };
  s = s.replace(PAIR, (whole, x, y, ww, hh) => {
    const L = labels[n];
    const cx = Number(x) + Number(ww) / 2, cy = Number(y) + Number(hh) / 2;
    const b = boxAt(L, L.k);
    box.x0 = Math.min(box.x0, b[0]); box.y0 = Math.min(box.y0, b[1]);
    box.x1 = Math.max(box.x1, b[2]); box.y1 = Math.max(box.y1, b[3]);
    n++;
    if (L.k <= 1.001) return whole;
    return `<g ${MARK}="1" transform="translate(${cx.toFixed(2)} ${cy.toFixed(2)}) scale(${L.k.toFixed(3)}) translate(${(-cx).toFixed(2)} ${(-cy).toFixed(2)})">${whole}</g>`;
  });

  const vb = s.match(/viewBox="([-\d.]+)\s+([-\d.]+)\s+([\d.]+)\s+([\d.]+)"/);
  let [vx, vy, vwid, vhgt] = vb.slice(1).map(Number);
  const pad = vwid * 0.004;
  const nx = Math.min(vx, box.x0 - pad), ny = Math.min(vy, box.y0 - pad);
  const nx1 = Math.max(vx + vwid, box.x1 + pad), ny1 = Math.max(vy + vhgt, box.y1 + pad);
  const grew = (nx !== vx || ny !== vy || nx1 !== vx + vwid || ny1 !== vy + vhgt);
  if (grew) {
    // remember what it was, so unpolish() can put it back on a re-run
    if (!/data-print-vb0=/.test(s)) {
      s = s.replace(/<svg /, `<svg data-print-vb0="${vx} ${vy} ${vwid} ${vhgt}" `);
    }
    const nvb = `viewBox="${nx.toFixed(1)} ${ny.toFixed(1)} ${(nx1 - nx).toFixed(1)} ${(ny1 - ny).toFixed(1)}"`;
    s = s.replace(/viewBox="[^"]+"/, nvb);
    // the white backdrop rect must grow with it or the page shows through at the new edges
    s = s.replace(/<rect x="[-\d.]+" y="[-\d.]+" width="[\d.]+" height="[\d.]+" fill="#ffffff"\/>/,
      `<rect x="${nx.toFixed(1)}" y="${ny.toFixed(1)}" width="${(nx1 - nx).toFixed(1)}" height="${(ny1 - ny).toFixed(1)}" fill="#ffffff"/>`);
  }
  const ks = labels.map(L => L.k);
  const kmin = ks.length ? Math.min(...ks) : 1, kmax = ks.length ? Math.max(...ks) : 1;
  // the on-card size the smallest label actually ends up at — the number that decides whether
  // this figure is readable, and the one to watch when re-tuning
  const worst = Math.min(...labels.map(L => L.px * L.k));
  return { s, cut: w.cut, n, px, grew, kmin, kmax, worst, wasPolished };
}

// usage: node polish_for_print.js <figure_breadboard.svg> [more.svg ...]
// Rewrites each file in place. Re-runnable: a previously polished figure is unpolished first and
// scaled again from scratch, so the constants at the top of this file can be re-tuned and the
// script re-run over the published SVGs without rebuilding anything in Fritzing.
if (process.argv.length < 3) {
  console.error('usage: node polish_for_print.js <figure_breadboard.svg> [...]');
  process.exit(1);
}
for (const f of process.argv.slice(2)) {
  const r = polish(f);
  fs.writeFileSync(f, r.s);
  // "worst" is the on-card size of the smallest label after scaling — the readability number.
  console.log([require('path').basename(f).replace('_breadboard.svg', ''),
    'wm:' + (r.cut ? 'cut' : '--'), r.wasPolished ? 're-polished' : 'polished',
    'labels:' + r.n,
    'x' + (r.n ? r.kmin.toFixed(2) + '-' + r.kmax.toFixed(2) : '1.00'),
    'smallest:' + (r.worst ? r.worst.toFixed(1) : '-') + 'px',
    r.grew ? 'viewBox grown' : ''].join('  '));
}
