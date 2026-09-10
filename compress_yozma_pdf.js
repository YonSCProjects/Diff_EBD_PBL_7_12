// Prints build_output/Arduino_Yozma_Tnufa_he.html (prose + 130-card appendix,
// self-contained) to a single PDF in ONE Chromium pass, replacing the pdf-lib
// merge of 130 per-card PDFs. One pass embeds each font once instead of once
// per card — the difference between a ~155 MB and a portal-uploadable file.
// Page setup mirrors md-to-pdf-he.config.js (A4, 25/20 mm margins, page-number
// footer hidden on the title page).
const path = require('path');
const puppeteer = require('puppeteer');

const ROOT = __dirname;
const SRC = path.join(ROOT, 'build_output', 'Arduino_Yozma_Tnufa_he.html');
const OUT = path.join(ROOT, 'build_output', 'Arduino_Yozma_Tnufa_he.pdf');

(async () => {
  const browser = await puppeteer.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await browser.newPage();
  page.setDefaultTimeout(600000);
  console.log('loading merged HTML...');
  await page.goto('file:///' + SRC.replace(/\\/g, '/'), { waitUntil: 'networkidle0', timeout: 600000 });
  await new Promise((r) => setTimeout(r, 3000));
  console.log('printing to PDF (single pass)...');
  await page.pdf({
    path: OUT,
    format: 'A4',
    margin: { top: '25mm', right: '20mm', bottom: '25mm', left: '20mm' },
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `
      <div style="width: 100%; font-size: 9pt; color: #999; text-align: center; padding: 0 20mm;" id="footer-content">
        <span class="pageNumber"></span> / <span class="totalPages"></span>
      </div>
      <script>
        (function(){
          var pn = document.querySelector('.pageNumber');
          var fc = document.getElementById('footer-content');
          if (pn && fc && pn.textContent.trim() === '1') { fc.style.visibility = 'hidden'; }
        })();
      </script>
    `,
    timeout: 600000,
  });
  await browser.close();
  const size = require('fs').statSync(OUT).size;
  console.log('Done: ' + OUT + ' (' + Math.round(size / 1024 / 1024 * 10) / 10 + ' MB)');
})().catch((e) => { console.error(e); process.exit(1); });
