// Load every page of site/ with all non-localhost requests blocked, and report any that
// fail to render or reference a missing file. This is the school-network simulation: if a
// card needs unpkg or a file we forgot to copy, it shows up here rather than in a classroom.
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const BASE = 'http://127.0.0.1:8903';
const SITE = path.join(__dirname, 'site');

const pages = ['/index.html'];
for (const d of fs.readdirSync(SITE).filter((x) => /^p\d+$/.test(x))
                 .sort((a, b) => Number(a.slice(1)) - Number(b.slice(1)))) {
  pages.push('/' + d + '/index.html');
  for (const f of fs.readdirSync(path.join(SITE, d)).filter((x) => x.endsWith('.dc.html')).sort()) {
    pages.push('/' + d + '/' + encodeURIComponent(f));
  }
}

(async () => {
  const b = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const fails = [];
  let n = 0;
  for (const u of pages) {
    const p = await b.newPage();
    await p.setRequestInterception(true);
    const missing = [];
    p.on('request', (r) => {
      const x = r.url();
      if (x.startsWith(BASE) || x.startsWith('data:')) return r.continue();
      r.abort().catch(() => {});                       // simulate a blocked CDN
    });
    p.on('response', (r) => { if (r.status() === 404) missing.push(r.url().replace(BASE, '')); });
    p.on('dialog', (d) => d.dismiss().catch(() => {}));
    try {
      await p.goto(BASE + u, { waitUntil: 'networkidle0', timeout: 25000 });
      await new Promise((r) => setTimeout(r, 900));
      const s = await p.evaluate(() => ({
        c: document.body.innerText.trim().length,
        raw: (document.body.innerText.match(/\{\{/g) || []).length,
        br: Array.from(document.images).filter((i) => !i.complete || i.naturalWidth === 0).length,
      }));
      const bad = s.c < 250 || s.raw > 0 || s.br > 0 || missing.filter((m) => !/favicon/.test(m)).length;
      if (bad) fails.push({ u, ...s, missing: missing.filter((m) => !/favicon/.test(m)) });
    } catch (e) {
      fails.push({ u, err: e.message.slice(0, 60) });
    }
    await p.close();
    if (++n % 25 === 0) process.stdout.write('  ' + n + '/' + pages.length + '\n');
  }
  await b.close();
  console.log('\nchecked ' + pages.length + ' pages with the internet blocked');
  if (!fails.length) { console.log('ALL PASS'); process.exit(0); }
  console.log(fails.length + ' FAILED:');
  for (const f of fails) {
    console.log('  ' + f.u);
    if (f.err) console.log('      error: ' + f.err);
    else console.log('      text=' + f.c + ' raw=' + f.raw + ' brokenImg=' + f.br +
                     (f.missing.length ? ' 404: ' + f.missing.slice(0, 3).join(', ') : ''));
  }
  process.exit(1);
})();
