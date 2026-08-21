// Render an SVG file to PNG so the exported Fritzing breadboard diagrams can be
// visually inspected. Usage: node svg_to_png.js <input.svg> <output.png>
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const svgPath = process.argv[2];
  const pngPath = process.argv[3];
  const scale = Number(process.argv[4]) || 1; // optional zoom for inspection
  if (!svgPath || !pngPath) {
    console.error('Usage: node svg_to_png.js <input.svg> <output.png>');
    process.exit(1);
  }
  const fileUrl = 'file:///' + path.resolve(svgPath).replace(/\\/g, '/');
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage();
    await page.setViewport({ width: 1400, height: 1000, deviceScaleFactor: scale });
    await page.goto(fileUrl, { waitUntil: 'load', timeout: 60000 });
    // Give the SVG a white backdrop (SVG documents have no <body>).
    await page.evaluate(() => {
      const s = document.querySelector('svg');
      if (s) { s.style.background = '#ffffff'; }
      if (document.documentElement) { document.documentElement.style.background = '#ffffff'; }
    });
    const el = await page.$('svg');
    if (el) {
      await el.screenshot({ path: pngPath });
    } else {
      await page.screenshot({ path: pngPath, fullPage: true });
    }
    console.log('wrote', pngPath);
  } finally {
    await browser.close();
  }
})().catch((e) => { console.error(e); process.exit(1); });
