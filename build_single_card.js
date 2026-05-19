// Render one card HTML file to a single PDF.
// Usage: node build_single_card.js <path/to/card.html> [out.pdf]
//
// If out.pdf is omitted, the output is build_output/<basename>.pdf.

const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const src = process.argv[2];
if (!src) {
  console.error('Usage: node build_single_card.js <card.html> [out.pdf]');
  process.exit(1);
}
const srcAbs = path.resolve(src);
if (!fs.existsSync(srcAbs)) {
  console.error('Not found:', srcAbs);
  process.exit(1);
}

const OUT_DIR = path.join(__dirname, 'build_output');
if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR);
const outAbs = process.argv[3]
  ? path.resolve(process.argv[3])
  : path.join(OUT_DIR, path.basename(srcAbs, path.extname(srcAbs)) + '.pdf');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage();
    await page.setJavaScriptEnabled(false);
    await page.emulateMediaType('print');
    const url = 'file:///' + srcAbs.replace(/\\/g, '/');
    await page.goto(url, { waitUntil: 'load', timeout: 60000 });
    await page.pdf({
      path: outAbs,
      format: 'A4',
      printBackground: true,
      margin: { top: '10mm', right: '10mm', bottom: '10mm', left: '10mm' },
    });
  } finally {
    await browser.close();
  }
  const size = fs.statSync(outAbs).size;
  console.log('OK', outAbs, size, 'bytes');
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
