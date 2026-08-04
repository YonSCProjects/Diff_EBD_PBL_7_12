// holes.js <img> — find breadboard hole rows/cols by darkness profile; print % positions
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
(async () => {
  const abs = path.resolve(process.argv[2]);
  const b64 = fs.readFileSync(abs).toString('base64');
  const tmp = path.join(path.dirname(abs), '__holes_tmp.html');
  fs.writeFileSync(tmp, `<img id="im" src="data:image/png;base64,${b64}">`);
  const b = await puppeteer.launch({ headless: 'new' });
  const pg = await b.newPage();
  await pg.goto('file:///' + tmp.replace(/\\/g, '/'), { waitUntil: 'load' });
  for (let i = 0; i < 40; i++) {
    const ok = await pg.evaluate(() => { const im = document.getElementById('im'); return im.complete && im.naturalWidth; });
    if (ok) break;
    await new Promise((r) => setTimeout(r, 200));
  }
  const out = await pg.evaluate(() => {
    const im = document.getElementById('im');
    const W = im.naturalWidth, H = im.naturalHeight;
    const c = document.createElement('canvas');
    c.width = W; c.height = H;
    const ctx = c.getContext('2d');
    ctx.drawImage(im, 0, 0);
    const d = ctx.getImageData(0, 0, W, H).data;
    const dark = (x, y) => { const i = (y * W + x) * 4; return (d[i] + d[i + 1] + d[i + 2]) / 3 < 110 ? 1 : 0; };
    // sample a clean vertical band on the right side of the board (no components)
    const x0 = Math.round(W * 0.72), x1 = Math.round(W * 0.94);
    const rowProfile = [];
    for (let y = 0; y < H; y++) { let s = 0; for (let x = x0; x < x1; x += 2) s += dark(x, y); rowProfile.push(s); }
    // sample a clean horizontal band for columns
    const y0 = Math.round(H * 0.60), y1 = Math.round(H * 0.78);
    const colProfile = [];
    for (let x = 0; x < W; x++) { let s = 0; for (let y = y0; y < y1; y += 2) s += dark(x, y); colProfile.push(s); }
    const peaks = (prof, minVal) => {
      const groups = []; let cur = null;
      prof.forEach((v, i) => {
        if (v >= minVal) { if (!cur) cur = { a: i, b: i }; else cur.b = i; }
        else if (cur) { groups.push((cur.a + cur.b) / 2); cur = null; }
      });
      if (cur) groups.push((cur.a + cur.b) / 2);
      return groups;
    };
    const rMax = Math.max(...rowProfile), cMax = Math.max(...colProfile);
    return {
      W, H,
      rows: peaks(rowProfile, rMax * 0.5).map((y) => +(y / H * 100).toFixed(2)),
      cols: peaks(colProfile, cMax * 0.5).map((x) => +(x / W * 100).toFixed(2)),
    };
  });
  await b.close();
  fs.unlinkSync(tmp);
  console.log('image', out.W + 'x' + out.H);
  console.log('hole ROWS (y%):', JSON.stringify(out.rows));
  console.log('hole COLS (x%): first', out.cols[0], 'last', out.cols[out.cols.length - 1], 'count', out.cols.length);
})();
