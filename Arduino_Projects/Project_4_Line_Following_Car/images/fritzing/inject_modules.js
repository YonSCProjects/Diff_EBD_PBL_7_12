// inject_modules.js — composite labeled module blocks (L298N, line sensor, battery)
// + Fritzing-style wires onto an exported Fritzing breadboard SVG, expanding the
// canvas as needed.
//
// Usage: node inject_modules.js <in.svg|BLANK:w,h> <out.svg> <specJSON-file>
// spec = { modules: [{type:'l298n'|'sensor'|'battery', x, y, label?}],
//          wires:   [{from:[x,y]|'m<i>.<anchor>', to:..., color, width?, bend?[x,y]}],
//          margin?: number }
const fs = require('fs');

const [, , inPath, outPath, specPath] = process.argv;
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));

// ------------------------------------------------------------------ modules

function screwTerminal(x, y, w, h, poles, vertical) {
  // blue screw-terminal block with `poles` screws
  let s = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="#1f6fb2" stroke="#134a78" stroke-width="8"/>`;
  for (let i = 0; i < poles; i++) {
    const cx = vertical ? x + w / 2 : x + (w / (poles * 2)) * (2 * i + 1);
    const cy = vertical ? y + (h / (poles * 2)) * (2 * i + 1) : y + h / 2;
    s += `<circle cx="${cx}" cy="${cy}" r="${Math.min(w, h) * 0.16}" fill="#d7e4f0" stroke="#0d3350" stroke-width="6"/>`;
    s += `<line x1="${cx - 28}" y1="${cy}" x2="${cx + 28}" y2="${cy}" stroke="#0d3350" stroke-width="8"/>`;
  }
  return s;
}

const label = (x, y, text, size = 64, fill = '#ffffff', anchor = 'middle', bold = true) =>
  `<text x="${x}" y="${y}" font-family="Arial, sans-serif" font-size="${size}" font-weight="${bold ? 'bold' : 'normal'}" fill="${fill}" text-anchor="${anchor}">${text}</text>`;

function l298n(x, y) {
  // board 1700 x 1350
  const W = 1700, H = 1350;
  let s = `<g>`;
  s += `<rect x="${x}" y="${y}" width="${W}" height="${H}" rx="40" fill="#b03a2e" stroke="#7c241b" stroke-width="12"/>`;
  // mounting holes
  for (const [hx, hy] of [[x + 70, y + 70], [x + W - 70, y + 70], [x + 70, y + H - 70], [x + W - 70, y + H - 70]])
    s += `<circle cx="${hx}" cy="${hy}" r="34" fill="#fff" stroke="#7c241b" stroke-width="10"/>`;
  // heatsink (black, finned) top-center
  const hsX = x + W / 2 - 240, hsY = y + 90, hsW = 480, hsH = 460;
  s += `<rect x="${hsX}" y="${hsY}" width="${hsW}" height="${hsH}" fill="#1b1b1b" stroke="#000" stroke-width="8"/>`;
  for (let i = 1; i < 6; i++) s += `<line x1="${hsX + (hsW / 6) * i}" y1="${hsY}" x2="${hsX + (hsW / 6) * i}" y2="${hsY + hsH}" stroke="#3a3a3a" stroke-width="14"/>`;
  s += label(x + W / 2, y + 700, 'L298N', 110);
  // OUT1/OUT2 — left edge (two-pole vertical block)
  const tL = { x: x - 60, y: y + 280, w: 150, h: 420 };
  s += screwTerminal(tL.x, tL.y, tL.w, tL.h, 2, true);
  s += label(x + 130, y + 400, 'OUT1', 72, '#fff', 'start');
  s += label(x + 130, y + 610, 'OUT2', 72, '#fff', 'start');
  // OUT3/OUT4 — right edge
  const tR = { x: x + W - 90, y: y + 280, w: 150, h: 420 };
  s += screwTerminal(tR.x, tR.y, tR.w, tR.h, 2, true);
  s += label(x + W - 130, y + 400, 'OUT3', 72, '#fff', 'end');
  s += label(x + W - 130, y + 610, 'OUT4', 72, '#fff', 'end');
  // VIN / GND / 5V — bottom-left (three-pole horizontal)
  const tP = { x: x + 100, y: y + H - 90, w: 560, h: 150 };
  s += screwTerminal(tP.x, tP.y, tP.w, tP.h, 3, false);
  s += label(x + 195, y + H - 120, 'VIN', 54);
  s += label(x + 380, y + H - 120, 'GND', 54);
  s += label(x + 565, y + H - 120, '5V', 54);
  // ENA IN1 IN2 IN3 IN4 ENB — gold header pins bottom-right
  const names = ['ENA', 'IN1', 'IN2', 'IN3', 'IN4', 'ENB'];
  const hp = { x: x + W - 780, y: y + H - 40, gap: 120 };
  const headers = {};
  names.forEach((n, i) => {
    const px = hp.x + i * hp.gap;
    s += `<rect x="${px - 22}" y="${hp.y - 60}" width="44" height="110" fill="#caa64a" stroke="#8c6f22" stroke-width="8"/>`;
    s += label(px, hp.y - 84, n, 46, '#ffffff');
    headers[n] = [px, hp.y + 60];
  });
  s += `</g>`;
  return {
    svg: s,
    w: W, h: H, x, y,
    anchors: {
      OUT1: [tL.x + tL.w / 2, tL.y + tL.h * 0.25],
      OUT2: [tL.x + tL.w / 2, tL.y + tL.h * 0.75],
      OUT3: [tR.x + tR.w / 2, tR.y + tR.h * 0.25],
      OUT4: [tR.x + tR.w / 2, tR.y + tR.h * 0.75],
      VIN: [tP.x + tP.w / 6, tP.y + tP.h + 10],
      GND: [tP.x + tP.w / 2, tP.y + tP.h + 10],
      V5: [tP.x + (tP.w * 5) / 6, tP.y + tP.h + 10],
      ENA: headers['ENA'], IN1: headers['IN1'], IN2: headers['IN2'],
      IN3: headers['IN3'], IN4: headers['IN4'], ENB: headers['ENB'],
    },
  };
}

function sensor(x, y, name = 'Line sensor') {
  // small blue module 480 x 860, pins on top, eyes at bottom
  const W = 480, H = 860;
  let s = `<g>`;
  s += `<rect x="${x}" y="${y}" width="${W}" height="${H}" rx="30" fill="#1f4e9c" stroke="#12305f" stroke-width="10"/>`;
  const pinNames = ['VCC', 'GND', 'OUT'];
  const anchors = {};
  pinNames.forEach((n, i) => {
    const px = x + (W / 6) * (2 * i + 1);
    s += `<rect x="${px - 20}" y="${y - 90}" width="40" height="130" fill="#caa64a" stroke="#8c6f22" stroke-width="8"/>`;
    s += label(px, y + 110, n, 44);
    anchors[n] = [px, y - 90];
  });
  // sensor eyes (emitter light blue, receiver dark) at bottom, facing down
  s += `<circle cx="${x + W / 3}" cy="${y + H - 130}" r="80" fill="#78c0e8" stroke="#0d3350" stroke-width="10"/>`;
  s += `<circle cx="${x + (2 * W) / 3}" cy="${y + H - 130}" r="80" fill="#161616" stroke="#000" stroke-width="10"/>`;
  s += label(x + W / 2, y + H - 280, name, 44);
  s += `<rect x="${x + 60}" y="${y + 320}" width="${W - 120}" height="90" fill="#0f2a52"/>`; // ic hint
  s += `</g>`;
  return { svg: s, w: W, h: H, x, y, anchors };
}

function battery(x, y) {
  // 4xAA holder 1500 x 760, leads on the right
  const W = 1500, H = 760;
  let s = `<g>`;
  s += `<rect x="${x}" y="${y}" width="${W}" height="${H}" rx="40" fill="#242424" stroke="#000" stroke-width="12"/>`;
  for (let i = 0; i < 4; i++) {
    const cy = y + 95 + i * 150;
    s += `<rect x="${x + 90}" y="${cy}" width="${W - 320}" height="120" rx="55" fill="#4c8c4a" stroke="#2c5c2b" stroke-width="8"/>`;
    s += `<rect x="${x + 70}" y="${cy + 35}" width="34" height="50" fill="#cfcfcf"/>`;
    s += label(x + W / 2 - 60, cy + 82, 'AA', 52, '#e8f2e8');
  }
  s += label(x + W / 2, y + H - 32, '4 × AA', 66);
  const anchors = {
    PLUS: [x + W - 60, y + 200],
    MINUS: [x + W - 60, y + 420],
  };
  s += `<circle cx="${anchors.PLUS[0]}" cy="${anchors.PLUS[1]}" r="30" fill="#cc1414"/>`;
  s += label(anchors.PLUS[0] - 50, anchors.PLUS[1] + 20, '+', 80, '#ffffff', 'end');
  s += `<circle cx="${anchors.MINUS[0]}" cy="${anchors.MINUS[1]}" r="30" fill="#111"/><circle cx="${anchors.MINUS[0]}" cy="${anchors.MINUS[1]}" r="30" fill="none" stroke="#fff" stroke-width="8"/>`;
  s += label(anchors.MINUS[0] - 50, anchors.MINUS[1] + 22, '−', 80, '#ffffff', 'end');
  s += `</g>`;
  return { svg: s, w: W, h: H, x, y, anchors };
}

function motor(x, y, opt = 'MOTOR|right') {
  // yellow TT gear motor block 950 x 520; terminals ("T1"/"T2") on `side` edge
  const [name, side] = String(opt).split('|');
  const W = 950, H = 520;
  const tx = side === 'left' ? x : x + W;          // terminal edge x
  const capX = side === 'left' ? x : x + W - 200;  // silver can on terminal side
  let s = `<g>`;
  s += `<rect x="${x}" y="${y}" width="${W}" height="${H}" rx="46" fill="#f2c200" stroke="#8a6d00" stroke-width="12"/>`;
  s += `<rect x="${capX}" y="${y + 40}" width="200" height="${H - 80}" rx="26" fill="#9a9a9a" stroke="#5d5d5d" stroke-width="10"/>`;
  // axle hint on the opposite side
  const axX = side === 'left' ? x + W : x;
  s += `<rect x="${side === 'left' ? axX : axX - 70}" y="${y + H / 2 - 22}" width="70" height="44" fill="#d9d9d9" stroke="#7a7a7a" stroke-width="8"/>`;
  const lx = side === 'left' ? x + 200 + (W - 200) / 2 : x + (W - 200) / 2;
  s += label(lx, y + H / 2 + 22, name, 60, '#4a3800');
  // two copper solder tabs at the terminal edge
  const anchors = {};
  [['T1', y + 160], ['T2', y + 360]].forEach(([n, ty]) => {
    const tabX = side === 'left' ? tx - 60 : tx;
    s += `<rect x="${tabX}" y="${ty - 26}" width="60" height="52" fill="#c87533" stroke="#7c4716" stroke-width="8"/>`;
    anchors[n] = [side === 'left' ? tx - 60 : tx + 60, ty];
  });
  s += `</g>`;
  return { svg: s, w: W, h: H, x, y, anchors };
}

const FACTORY = { l298n, sensor, battery, motor };

// ------------------------------------------------------------------ compose

let svg, vb;
if (inPath.startsWith('BLANK:')) {
  const [w, h] = inPath.slice(6).split(',').map(Number);
  vb = [0, 0, w, h];
  svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}"></svg>`;
} else {
  svg = fs.readFileSync(inPath, 'utf8');
  const m = svg.match(/viewBox="([\d.\-]+) ([\d.\-]+) ([\d.\-]+) ([\d.\-]+)"/);
  vb = m.slice(1).map(Number);
}

const built = spec.modules.map((mo) => FACTORY[mo.type](mo.x, mo.y, mo.label));

function resolve(pt) {
  if (Array.isArray(pt)) return pt;
  const m = String(pt).match(/^m(\d+)\.(\w+)$/);
  if (!m) throw new Error('bad anchor ref: ' + pt);
  const a = built[Number(m[1])].anchors[m[2]];
  if (!a) throw new Error('unknown anchor ' + pt);
  return a;
}

function wireSvg(w) {
  const width = w.width || 28;
  const [x1, y1] = resolve(w.from);
  const [x2, y2] = resolve(w.to);
  const pts = w.bend ? `${x1},${y1} ${w.bend[0]},${w.bend[1]} ${x2},${y2}` : `${x1},${y1} ${x2},${y2}`;
  return `<polyline points="${pts}" fill="none" stroke="#2b2b2b" stroke-opacity="0.28" stroke-linecap="round" stroke-linejoin="round" stroke-width="${width + 14}"/>` +
    `<polyline points="${pts}" fill="none" stroke="${w.color}" stroke-linecap="round" stroke-linejoin="round" stroke-width="${width}"/>` +
    `<circle cx="${x1}" cy="${y1}" r="${width * 0.62}" fill="${w.color}"/>` +
    `<circle cx="${x2}" cy="${y2}" r="${width * 0.62}" fill="${w.color}"/>`;
}

const wiresSvg = (spec.wires || []).map(wireSvg).join('\n');
const modulesSvg = built.map((b) => b.svg).join('\n');

// expand viewBox to fit modules + wires (+ margin)
const margin = spec.margin ?? 120;
let [vx, vy, vw, vh] = vb;
let minX = vx, minY = vy, maxX = vx + vw, maxY = vy + vh;
for (const b of built) {
  minX = Math.min(minX, b.x - 120); minY = Math.min(minY, b.y - 160);
  maxX = Math.max(maxX, b.x + b.w + 120); maxY = Math.max(maxY, b.y + b.h + 120);
}
for (const w of spec.wires || []) {
  for (const pt of [resolve(w.from), resolve(w.to), ...(w.bend ? [w.bend] : [])]) {
    minX = Math.min(minX, pt[0] - 60); minY = Math.min(minY, pt[1] - 60);
    maxX = Math.max(maxX, pt[0] + 60); maxY = Math.max(maxY, pt[1] + 60);
  }
}
minX -= margin; minY -= margin; maxX += margin; maxY += margin;
const newVb = `${minX} ${minY} ${maxX - minX} ${maxY - minY}`;
svg = svg.replace(/viewBox="[^"]*"/, `viewBox="${newVb}"`);
// keep aspect: also fix width/height attrs if present (in inches units)
svg = svg.replace(/width="[\d.]+in"/, `width="${((maxX - minX) / 1000).toFixed(3)}in"`);
svg = svg.replace(/height="[\d.]+in"/, `height="${((maxY - minY) / 1000).toFixed(3)}in"`);

svg = svg.replace(/<\/svg>\s*$/, `<g id="composited-modules">\n${modulesSvg}\n${wiresSvg}\n</g>\n</svg>`);
fs.writeFileSync(outPath, svg);
console.log('wrote', outPath, 'modules:', built.length, 'wires:', (spec.wires || []).length, 'viewBox:', newVb);
