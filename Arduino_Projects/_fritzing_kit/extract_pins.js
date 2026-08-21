// extract_pins.js — read an exported Fritzing breadboard SVG and return the
// flattened (viewBox) coordinates of every connector of every part instance.
// Usage: node extract_pins.js <export_breadboard.svg> <spec.json> <out.json>
// NOTE: bendable-leg parts (LED, electrolytic cap) export their legs as anonymous paths, so only the
// body-side pin is reachable here; offset such parts by their leg length (snap.offset) when placing.
// Output: { "<instance id>": { "bbox":[x,y,w,h], "pins": { "<connector name>": [x,y], "c<N>": [x,y] } } }
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const HERE = __dirname;
const CORE = (process.env.FRITZING_PATH || 'C:/Program Files/Fritzing') + '/fritzing-parts/core';

function connectorNames(ins) {
  // connector id -> name, from the part's fzp
  let fzp;
  if (ins.part) {
    const d = path.join(HERE, 'parts', ins.part);
    fzp = path.join(d, fs.readdirSync(d).find((f) => f.startsWith('part.') && f.endsWith('.fzp')));
  } else fzp = path.join(CORE, ins.core + '.fzp');
  const txt = fs.readFileSync(fzp, 'utf8');
  const map = {};
  const re = /<connector\b([^>]*)>/g; let m;
  while ((m = re.exec(txt))) {
    const id = (m[1].match(/\bid="([^"]+)"/) || [])[1];
    const name = (m[1].match(/\bname="([^"]+)"/) || [])[1];
    if (id) map[id] = name || id;
  }
  return map;
}

(async () => {
  const [svgPath, specPath, outPath] = process.argv.slice(2);
  const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
  const byPartId = {};
  spec.instances.forEach((ins, i) => { byPartId[String((1001 + i) * 10)] = ins; });
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1600, height: 1200 });
    await page.goto('file:///' + path.resolve(svgPath).split('\\').join('/'), { waitUntil: 'load' });
    const raw = await page.evaluate(() => {
      const svg = document.querySelector('svg');
      const inv = svg.getScreenCTM().inverse();
      const toVb = (el) => {
        const b = el.getBBox();
        const p = svg.createSVGPoint(); p.x = b.x + b.width / 2; p.y = b.y + b.height / 2;
        const q = p.matrixTransform(el.getScreenCTM()).matrixTransform(inv);
        return [Math.round(q.x * 100) / 100, Math.round(q.y * 100) / 100];
      };
      const bboxVb = (el) => {
        const b = el.getBBox();
        const pts = [[b.x, b.y], [b.x + b.width, b.y + b.height]].map(([x, y]) => {
          const p = svg.createSVGPoint(); p.x = x; p.y = y;
          const q = p.matrixTransform(el.getScreenCTM()).matrixTransform(inv); return [q.x, q.y];
        });
        return [pts[0][0], pts[0][1], pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]].map((v) => Math.round(v * 100) / 100);
      };
      const out = {};
      document.querySelectorAll('g[partID]').forEach((g) => {
        const pid = g.getAttribute('partID');
        const pins = {};
        g.querySelectorAll('[id]').forEach((el) => {
          const id = el.id;
          let m;
          if ((m = id.match(/^(connector\d+)(pin|terminal|pad)$/))) {
            const key = m[1], kind = m[2];
            if (!pins[key] || kind === 'terminal') pins[key] = toVb(el);
          } else if ((m = id.match(/^(pin\d+[A-Z])$/))) {
            pins[m[1]] = toVb(el);
          }
        });
        out[pid] = { bbox: bboxVb(g), pins };
      });
      const vb = svg.getAttribute('viewBox').split(/\s+/).map(Number);
      return { out, vb };
    });
    const result = { _viewBox: raw.vb };
    for (const [pid, data] of Object.entries(raw.out)) {
      const ins = byPartId[pid];
      if (!ins) continue;
      const names = ins.part || ins.core ? connectorNames(ins) : {};
      const pins = {};
      const seen = {};
      for (const [cid, xy] of Object.entries(data.pins)) {
        pins[cid.replace(/^connector/, 'c')] = xy;     // c12
        let nm = names[cid] || cid;                     // OUT1 / pin10A
        if (pins[nm]) { seen[nm] = (seen[nm] || 1) + 1; nm = nm + '.' + seen[nm]; }
        pins[nm] = xy;
      }
      result[ins.id] = { bbox: data.bbox, pins };
    }
    fs.writeFileSync(outPath, JSON.stringify(result, null, 1));
    console.log('pins extracted for', Object.keys(result).filter((k) => k !== '_viewBox').join(', '));
  } finally { await browser.close(); }
})().catch((e) => { console.error(e); process.exit(1); });
