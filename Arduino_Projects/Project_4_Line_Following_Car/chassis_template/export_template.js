// export_template.js — 1:1 A4-landscape PDF of the chassis template + a PNG preview for the cards.
// Usage (from this folder): node export_template.js
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const html = path.resolve(__dirname, 'chassis_template_he.html');
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  try {
    const page = await browser.newPage();
    await page.goto('file:///' + html.split('\\').join('/'), { waitUntil: 'load' });
    await page.pdf({ path: path.resolve(__dirname, 'chassis_template_he.pdf'), format: 'A4', landscape: true, printBackground: true,
      margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
    await page.setViewport({ width: 1123, height: 794, deviceScaleFactor: 2 });   // 297 x 210 mm at 96 dpi
    await page.screenshot({ path: path.resolve(__dirname, '..', 'task_cards_he', 'assets', 'chassis_template_preview.png'), clip: { x: 0, y: 0, width: 1123, height: 794 } });
    console.log('wrote chassis_template_he.pdf + task_cards_he/assets/chassis_template_preview.png');
  } finally { await browser.close(); }
})().catch((e) => { console.error(e); process.exit(1); });
