// build_figure.js — one-shot pipeline for a wiring figure:
//   spec.json → .fzz (parts bundled) → Fritzing CLI export → pin coords →
//   composited wires/labels → <name>_breadboard.svg (+ preview PNG)
// Usage: node build_figure.js <spec.json> [--no-snap]
//
// spec = { name, out_dir, assets_dir?, instances[], wires[], labels[], margin? }
//   instance.snap = { pin: "VCC", to: "bb.pin10A", axis?: 'x'|'y', offset?: [dx, dy] px }  → after a first export the
//   instance is shifted so that its pin lands exactly on the target pin, then re-exported.
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const HERE = __dirname;
const REPO = path.resolve(HERE, '..', '..');
const FRITZING = (process.env.FRITZING_PATH || 'C:/Program Files/Fritzing') + '/Fritzing.exe';
const PX_PER_UNIT = 0.09; // export units are 1/1000 in; sketch px are 1/90 in

const specPath = path.resolve(process.argv[2]);
const noSnap = process.argv.includes('--no-snap');
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
const specDir = path.dirname(specPath);
const outDir = path.resolve(specDir, spec.out_dir || '.');
const work = path.join(outDir, 'fritzing');
fs.mkdirSync(work, { recursive: true });
const name = spec.name;

function run(cmd, args, opts = {}) {
  return execFileSync(cmd, args, { stdio: ['ignore', 'pipe', 'pipe'], encoding: 'utf8', ...opts });
}

function exportOnce(tag) {
  const tmpSpec = path.join(work, `${name}.spec.tmp.json`);
  fs.writeFileSync(tmpSpec, JSON.stringify(spec));
  const fzz = path.join(work, `${name}.fzz`);
  console.log(run('python', [path.join(HERE, 'make_fzz.py'), tmpSpec, fzz]).trim());
  const exp = path.join(work, `_export_${name}`);
  fs.rmSync(exp, { recursive: true, force: true });
  fs.mkdirSync(exp, { recursive: true });
  fs.copyFileSync(fzz, path.join(exp, `${name}.fzz`));
  try { run(FRITZING, ['-svg', exp], { timeout: 180000 }); } catch (e) { /* Fritzing returns non-zero on exit sometimes; check output */ }
  const bb = path.join(exp, `${name}_breadboard.svg`);
  if (!fs.existsSync(bb)) throw new Error('Fritzing export produced no breadboard SVG in ' + exp);
  const pinsJson = path.join(work, `${name}.pins.json`);
  console.log(run('node', [path.join(HERE, 'extract_pins.js'), bb, tmpSpec, pinsJson]).trim());
  fs.unlinkSync(tmpSpec);
  return { bb, pinsJson, pins: JSON.parse(fs.readFileSync(pinsJson, 'utf8')) };
}

let res = exportOnce('pass1');

// snapping pass
const snaps = spec.instances.filter((i) => i.snap);
if (snaps.length && !noSnap) {
  let moved = false;
  for (const ins of snaps) {
    const from = res.pins[ins.id].pins[ins.snap.pin];
    const [tid, tpin] = ins.snap.to.split('.');
    const to = res.pins[tid].pins[tpin];
    if (!from || !to) throw new Error('snap: missing pin for ' + ins.id);
    let dx = (to[0] - from[0]) * PX_PER_UNIT, dy = (to[1] - from[1]) * PX_PER_UNIT;
    if (ins.snap.axis === 'x') dy = 0;          // align only horizontally
    if (ins.snap.axis === 'y') dx = 0;          // align only vertically
    if (ins.snap.offset) { dx += ins.snap.offset[0] || 0; dy += ins.snap.offset[1] || 0; }   // extra shift in px (e.g. leg length)
    if (Math.abs(dx) > 0.05 || Math.abs(dy) > 0.05) {
      ins.x = Math.round((ins.x + dx) * 1000) / 1000; ins.y = Math.round((ins.y + dy) * 1000) / 1000; moved = true;
      console.log(`snap ${ins.id}.${ins.snap.pin} → ${ins.snap.to}: shifted by (${dx.toFixed(2)}, ${dy.toFixed(2)}) px → (${ins.x}, ${ins.y})`);
    }
  }
  if (moved) {
    // persist the snapped coordinates back into the spec so the .fzz is reproducible
    fs.writeFileSync(specPath, JSON.stringify(spec, null, 2) + '\n');
    res = exportOnce('pass2');
  }
}

const outSvg = path.join(outDir, `${name}_breadboard.svg`);
console.log(run('node', [path.join(HERE, 'compose.js'), res.bb, res.pinsJson, specPath, outSvg]).trim());
const png = path.join(work, `${name}_preview.png`);
console.log(run('node', [path.join(REPO, 'svg_to_png.js'), outSvg, png, String(spec.preview_scale || 2.5)]).trim());
if (spec.assets_dir) {
  const assets = path.resolve(specDir, spec.assets_dir);
  fs.mkdirSync(assets, { recursive: true });
  fs.copyFileSync(outSvg, path.join(assets, path.basename(outSvg)));
  console.log('copied to', path.join(assets, path.basename(outSvg)));
}
fs.rmSync(path.join(work, `_export_${name}`), { recursive: true, force: true });
