// compose.js — draw Fritzing-style wires + callout labels onto an exported
// Fritzing breadboard SVG, anchored on real connector coordinates.
// Usage: node compose.js <export_breadboard.svg> <pins.json> <spec.json> <out.svg>
//
// spec.wires[]  = { from, to, color, width?, route?: 'direct'|'hv'|'vh', via?: [ref...],
//                   out?: ['up'|'down'|'left'|'right', len], in?: [dir, len] }
// spec.shapes[] = { a: ref, b?: ref, pad?, fill?, stroke?, strokeWidth?, rx?, dash? }  (rect spanning a..b)
// spec.labels[] = { ref|at, dx?, dy?, text, size?, anchor?, fill?, color?, stroke?, leader?: true, bold? }
// ref forms: "inst.PIN" | "inst.@c" (bbox anchor: @c @t @b @l @r @tl @tr @bl @br) | { ref, dx, dy } | [x, y]
const fs = require('fs');
const [, , svgPath, pinsPath, specPath, outPath] = process.argv;
const pins = JSON.parse(fs.readFileSync(pinsPath, 'utf8'));
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
let svg = fs.readFileSync(svgPath, 'utf8');

function resolve(r) {
  if (Array.isArray(r)) return r.slice();
  if (typeof r === 'object') { const p = resolve(r.ref); return [p[0] + (r.dx || 0), p[1] + (r.dy || 0)]; }
  const m = String(r).match(/^([^.]+)\.(.+)$/);
  if (!m) throw new Error('bad ref ' + r);
  const inst = pins[m[1]]; if (!inst) throw new Error('unknown instance ' + m[1]);
  if (m[2].startsWith('@')) {            // bbox anchors: @c @t @b @l @r @tl @tr @bl @br
    const [bx, by, bw, bh] = inst.bbox;
    const k = m[2].slice(1);
    const fx = k.includes('l') ? 0 : k.includes('r') ? 1 : 0.5;
    const fy = k.includes('t') ? 0 : k.includes('b') ? 1 : 0.5;
    return [bx + bw * fx, by + bh * fy];
  }
  const p = inst.pins[m[2]]; if (!p) throw new Error('unknown pin ' + r + ' (have: ' + Object.keys(inst.pins).filter((k) => !k.startsWith('c')).join(' ') + ')');
  return p.slice();
}
const DIR = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] };
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function wirePoints(w) {
  const a = resolve(w.from), b = resolve(w.to);
  const pts = [a];
  let cur = a;
  if (w.out) { const d = DIR[w.out[0]]; cur = [a[0] + d[0] * w.out[1], a[1] + d[1] * w.out[1]]; pts.push(cur); }
  const vias = (w.via || []).map(resolve);
  let end = b;
  let inPt = null;
  if (w.in) { const d = DIR[w.in[0]]; inPt = [b[0] + d[0] * w.in[1], b[1] + d[1] * w.in[1]]; end = inPt; }
  const targets = [...vias, end];
  for (const t of targets) {
    const route = w.route || 'direct';
    if (route === 'hv') pts.push([t[0], cur[1]]);
    else if (route === 'vh') pts.push([cur[0], t[1]]);
    pts.push(t); cur = t;
  }
  if (inPt) pts.push(b);
  // drop duplicate consecutive points
  return pts.filter((p, i) => i === 0 || Math.abs(p[0] - pts[i - 1][0]) > 0.01 || Math.abs(p[1] - pts[i - 1][1]) > 0.01);
}

function wireSvg(w) {
  const width = w.width || 30;
  const pts = wirePoints(w);
  const s = pts.map((p) => `${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');
  const [x1, y1] = pts[0], [x2, y2] = pts[pts.length - 1];
  return `<polyline points="${s}" fill="none" stroke="#222" stroke-opacity="0.30" stroke-linecap="round" stroke-linejoin="round" stroke-width="${width + 12}"/>` +
    `<polyline points="${s}" fill="none" stroke="${w.color}" stroke-linecap="round" stroke-linejoin="round" stroke-width="${width}"/>` +
    `<polyline points="${s}" fill="none" stroke="#fff" stroke-opacity="0.22" stroke-linecap="round" stroke-linejoin="round" stroke-width="${width * 0.3}"/>` +
    `<circle cx="${x1}" cy="${y1}" r="${width * 0.7}" fill="${w.color}" stroke="#222" stroke-opacity="0.5" stroke-width="4"/>` +
    `<circle cx="${x2}" cy="${y2}" r="${width * 0.7}" fill="${w.color}" stroke="#222" stroke-opacity="0.5" stroke-width="4"/>`;
}

function labelSvg(l) {
  const base = resolve(l.ref || l.at);
  const x = base[0] + (l.dx || 0), y = base[1] + (l.dy || 0);
  const size = l.size || 60;
  const text = String(l.text);
  const lines = text.split('\n');
  const wChar = size * 0.58;
  const w = Math.max(...lines.map((t) => t.length)) * wChar + size * 0.9;
  const h = lines.length * size * 1.2 + size * 0.5;
  const anchor = l.anchor || 'middle';
  const bx = anchor === 'start' ? x - size * 0.45 : anchor === 'end' ? x - w + size * 0.45 : x - w / 2;
  const by = y - h / 2;
  let s = '';
  if (l.leader) {
    s += `<line x1="${base[0]}" y1="${base[1]}" x2="${x}" y2="${y}" stroke="${l.stroke || '#333'}" stroke-width="8" stroke-dasharray="18 14" opacity="0.85"/>`;
    s += `<circle cx="${base[0]}" cy="${base[1]}" r="16" fill="none" stroke="${l.stroke || '#333'}" stroke-width="8"/>`;
  }
  if (l.fill !== 'none') s += `<rect x="${bx}" y="${by}" width="${w}" height="${h}" rx="${size * 0.35}" fill="${l.fill || '#ffffff'}" stroke="${l.stroke || '#333'}" stroke-width="${l.strokeWidth || 8}" opacity="0.96"/>`;
  lines.forEach((t, i) => {
    const ty = by + size * 0.5 + size * 1.2 * i + size * 0.85;
    s += `<text x="${x}" y="${ty}" font-family="Arial, Helvetica, sans-serif" font-size="${size}" font-weight="${l.bold === false ? 'normal' : 'bold'}" fill="${l.color || '#222'}" text-anchor="${anchor}">${esc(t)}</text>`;
  });
  return s;
}

function shapeSvg(sh) {
  // rect spanning two refs (+pad): a jumper cap over two header pins, a bracket around a pin group, ...
  const a = resolve(sh.a), b = resolve(sh.b || sh.a);
  const pad = sh.pad == null ? 50 : sh.pad;
  const x = Math.min(a[0], b[0]) - pad, y = Math.min(a[1], b[1]) - pad;
  const w = Math.abs(a[0] - b[0]) + 2 * pad, h = Math.abs(a[1] - b[1]) + 2 * pad;
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${sh.rx == null ? 18 : sh.rx}" fill="${sh.fill || 'none'}" stroke="${sh.stroke || '#222'}" stroke-width="${sh.strokeWidth || 10}"${sh.dash ? ` stroke-dasharray="${sh.dash}"` : ''}/>`;
}
const shapes = (spec.shapes || []).map(shapeSvg).join('\n');
const wires = (spec.wires || []).map(wireSvg).join('\n');
const labels = (spec.labels || []).map(labelSvg).join('\n');

// expand viewBox to include everything drawn (+ margin)
const vb = svg.match(/viewBox="([\d.\-]+) ([\d.\-]+) ([\d.\-]+) ([\d.\-]+)"/).slice(1).map(Number);
let [minX, minY, maxX, maxY] = [vb[0], vb[1], vb[0] + vb[2], vb[1] + vb[3]];
const touch = (x, y, pad) => { minX = Math.min(minX, x - pad); minY = Math.min(minY, y - pad); maxX = Math.max(maxX, x + pad); maxY = Math.max(maxY, y + pad); };
for (const w of spec.wires || []) for (const p of wirePoints(w)) touch(p[0], p[1], (w.width || 30) + 20);
for (const l of spec.labels || []) {
  const b = resolve(l.ref || l.at); const size = l.size || 60; const lines = String(l.text).split('\n');
  const w = Math.max(...lines.map((t) => t.length)) * size * 0.58 + size; const h = lines.length * size * 1.2 + size * 0.5;
  touch(b[0] + (l.dx || 0), b[1] + (l.dy || 0), Math.max(w, h) / 2 + 20);
}
const margin = spec.margin == null ? 100 : spec.margin;
minX -= margin; minY -= margin; maxX += margin; maxY += margin;
if (spec.extend) { minX += spec.extend[0] || 0; minY += spec.extend[1] || 0; maxX += spec.extend[2] || 0; maxY += spec.extend[3] || 0; }
const W = maxX - minX, H = maxY - minY;
svg = svg.replace(/viewBox="[^"]*"/, `viewBox="${minX.toFixed(1)} ${minY.toFixed(1)} ${W.toFixed(1)} ${H.toFixed(1)}"`)
  .replace(/width="[\d.]+in"/, `width="${(W / 1000).toFixed(3)}in"`)
  .replace(/height="[\d.]+in"/, `height="${(H / 1000).toFixed(3)}in"`);
// white backdrop so the figure prints cleanly inside the card frame
svg = svg.replace(/(<svg\b[^>]*>)/, `$1\n<rect x="${minX.toFixed(1)}" y="${minY.toFixed(1)}" width="${W.toFixed(1)}" height="${H.toFixed(1)}" fill="#ffffff"/>`);
svg = svg.replace(/<\/svg>\s*$/, `<g id="composited-shapes">
${shapes}
</g>
<g id="composited-wires">\n${wires}\n</g>\n<g id="composited-labels">\n${labels}\n</g>\n</svg>\n`);
fs.writeFileSync(outPath, svg);
console.log('wrote', outPath, '| wires', (spec.wires || []).length, '| labels', (spec.labels || []).length, '| viewBox', `${minX.toFixed(0)} ${minY.toFixed(0)} ${W.toFixed(0)} ${H.toFixed(0)}`);
