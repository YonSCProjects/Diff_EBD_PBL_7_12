/* compose.js — render + anchors + Hebrew callouts -> one self-contained SVG for a card.
 *
 *   node _blender/compose.js <render.png> <callouts.json> <out.svg>
 *
 * The PNG goes in as a base64 <image>; the callouts are drawn as vector text over it. That keeps
 * the Hebrew crisp at any print size and means a wording change costs a re-compose, not a
 * re-render — which at a minute a frame is the difference that matters.
 *
 * callouts.json:
 *   { "captionBox": true,
 *     "items": [ { "anchor": "uno", "he": "...", "dx": 90, "dy": -70, "size": 20 }, ... ] }
 *
 * dx/dy are offsets in RENDER pixels from the anchor to the label box centre.
 */
const fs = require('fs');
const path = require('path');

const [pngPath, calloutPath, outPath] = process.argv.slice(2);
if (!outPath) {
  console.error('usage: node compose.js <render.png> <callouts.json> <out.svg>');
  process.exit(2);
}

const meta = JSON.parse(fs.readFileSync(pngPath.replace(/\.png$/, '.anchors.json'), 'utf8'));
const spec = JSON.parse(fs.readFileSync(calloutPath, 'utf8'));
const png = fs.readFileSync(pngPath).toString('base64');
const W = meta.width, H = meta.height;

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// Type is sized as a fraction of the render width, so a callout keeps the same visual weight
// whatever resolution the frame was rendered at.
const K = W / 1500;
const FONT = "'Rubik','Segoe UI',Arial,sans-serif";

let layer = '';
for (const it of spec.items || []) {
  const a = meta.anchors[it.anchor];
  if (!a) { console.warn('no anchor:', it.anchor); continue; }
  if (a.onscreen === false) console.warn('anchor off-screen:', it.anchor);

  const size = (it.size || 19) * K;
  const lines = String(it.he).split('\n');
  const pad = size * 0.62;
  const lh = size * 1.34;
  const wch = size * 0.56;                       // Rubik at this weight, Hebrew average
  const bw = Math.max(...lines.map(l => l.length)) * wch + pad * 2;
  const bh = lines.length * lh + pad * 1.25;
  const cx = a.x + (it.dx || 0) * K;
  const cy = a.y + (it.dy || 0) * K;
  const bx = cx - bw / 2, by = cy - bh / 2;

  // leader: a hairline from the box edge to a ring on the part itself
  layer += `<line x1="${a.x.toFixed(1)}" y1="${a.y.toFixed(1)}" x2="${cx.toFixed(1)}" y2="${cy.toFixed(1)}" `
    + `stroke="#2a3442" stroke-width="${(1.5 * K).toFixed(2)}" stroke-dasharray="${4.5 * K} ${3.5 * K}" stroke-opacity="0.85"/>`;
  layer += `<circle cx="${a.x.toFixed(1)}" cy="${a.y.toFixed(1)}" r="${(4.5 * K).toFixed(2)}" `
    + `fill="none" stroke="${it.ring || '#e0651a'}" stroke-width="${(2.4 * K).toFixed(2)}"/>`;
  layer += `<rect x="${bx.toFixed(1)}" y="${by.toFixed(1)}" width="${bw.toFixed(1)}" height="${bh.toFixed(1)}" `
    + `rx="${(size * 0.42).toFixed(1)}" fill="#ffffff" fill-opacity="0.97" stroke="#2a3442" `
    + `stroke-width="${(1.6 * K).toFixed(2)}"/>`;
  lines.forEach((l, i) => {
    const ty = by + pad * 0.62 + lh * (i + 0.78);
    layer += `<text x="${cx.toFixed(1)}" y="${ty.toFixed(1)}" font-family="${FONT}" `
      + `font-size="${size.toFixed(1)}" font-weight="700" fill="#16202c" text-anchor="middle" `
      + `direction="rtl">${esc(l)}</text>`;
  });
}

// arrows: straight, with a head, in the kit's action orange
for (const ar of spec.arrows || []) {
  const A = meta.anchors[ar.from], B = meta.anchors[ar.to];
  if (!A || !B) { console.warn('arrow needs two anchors:', ar.from, ar.to); continue; }
  const ax = A.x + (ar.fdx || 0) * K, ay = A.y + (ar.fdy || 0) * K;
  const bx2 = B.x + (ar.tdx || 0) * K, by2 = B.y + (ar.tdy || 0) * K;
  const dx = bx2 - ax, dy = by2 - ay, L = Math.hypot(dx, dy) || 1;
  const ux = dx / L, uy = dy / L, head = 16 * K;
  const sx = bx2 - ux * head, sy = by2 - uy * head;
  const px = -uy, py = ux;
  layer += `<path d="M ${ax.toFixed(1)} ${ay.toFixed(1)} L ${sx.toFixed(1)} ${sy.toFixed(1)}" `
    + `fill="none" stroke="#ffffff" stroke-width="${(7 * K).toFixed(2)}" stroke-linecap="round"/>`;
  layer += `<path d="M ${ax.toFixed(1)} ${ay.toFixed(1)} L ${sx.toFixed(1)} ${sy.toFixed(1)}" `
    + `fill="none" stroke="#e0651a" stroke-width="${(4.5 * K).toFixed(2)}" stroke-linecap="round"/>`;
  layer += `<polygon points="${bx2.toFixed(1)},${by2.toFixed(1)} `
    + `${(sx + px * head * 0.45).toFixed(1)},${(sy + py * head * 0.45).toFixed(1)} `
    + `${(sx - px * head * 0.45).toFixed(1)},${(sy - py * head * 0.45).toFixed(1)}" `
    + `fill="#e0651a" stroke="#fff" stroke-width="${(1.4 * K).toFixed(2)}" stroke-linejoin="round"/>`;
}

const svg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" `
  + `viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">\n`
  + `<image x="0" y="0" width="${W}" height="${H}" xlink:href="data:image/png;base64,${png}"/>\n`
  + layer + `\n</svg>\n`;

fs.mkdirSync(path.dirname(path.resolve(outPath)), { recursive: true });
fs.writeFileSync(outPath, svg);
console.log('wrote', outPath, `(${(svg.length / 1024).toFixed(0)} KB)`);
