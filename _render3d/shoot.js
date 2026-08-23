// shoot.js — serve the repo, open the WebGL scene in headless Chrome, save a PNG.
//   node _render3d/shoot.js out.png [view] [props] [w] [h] [ss]
const http = require('http');
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const ROOT = path.resolve(__dirname, '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
                '.json': 'application/json', '.png': 'image/png', '.hdr': 'application/octet-stream' };

function serve() {
  return new Promise(res => {
    const s = http.createServer((req, rp) => {
      const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
      if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) {
        rp.writeHead(404); return rp.end('nope');
      }
      rp.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' });
      fs.createReadStream(p).pipe(rp);
    });
    s.listen(0, '127.0.0.1', () => res(s));
  });
}

(async () => {
  const [out, view = 'hero', props = '0', w = '1600', h = '1200', ss = '2'] = process.argv.slice(2);
  const server = await serve();
  const port = server.address().port;
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--use-gl=angle', '--use-angle=default',
           '--enable-unsafe-swiftshader', '--disable-lcd-text'],
  });
  const page = await browser.newPage();
  page.on('pageerror', e => console.error('PAGE ERROR:', e.message));
  page.on('console', m => { if (m.type() === 'error') console.error('console:', m.text()); });
  await page.setViewport({ width: +w, height: +h, deviceScaleFactor: 1 });
  const url = `http://127.0.0.1:${port}/_render3d/scene.html?view=${view}&props=${props}&w=${w}&h=${h}&ss=${ss}`;
  await page.goto(url, { waitUntil: 'networkidle0' });
  await page.waitForFunction('window.__done === true', { timeout: 120000 });
  const el = await page.$('canvas');
  await el.screenshot({ path: out, omitBackground: true });
  await browser.close();
  server.close();
  console.log('wrote', out);
})().catch(e => { console.error(e); process.exit(1); });
