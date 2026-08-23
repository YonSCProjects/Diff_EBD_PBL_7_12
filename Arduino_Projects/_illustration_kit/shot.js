// _shot.js <in.svg> <out.png> [widthPx]  — render one SVG to PNG for eyeballing
const fs = require('fs'), puppeteer = require('puppeteer');
const f = process.argv[2], out = process.argv[3], W = parseInt(process.argv[4] || '1000', 10);
const svg = fs.readFileSync(f, 'utf8')
  .replace(/<\?xml[^>]*>/, '')
  .replace(/<svg /, `<svg style="width:${W}px;height:auto" `);
(async () => {
  const b = await puppeteer.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.setViewport({ width: W + 24, height: 800 });
  await p.setContent(`<body style="margin:12px;background:#fff">${svg}</body>`);
  await new Promise(r => setTimeout(r, 350));
  await p.screenshot({ path: out, fullPage: true });
  await b.close();
  console.log('ok');
})();
