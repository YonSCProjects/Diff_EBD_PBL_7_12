// build_site.js — assemble the student-facing website from the Hebrew task cards.
//
//   node build_site.js            # build into site/
//   node build_site.js --projects 1,2,3
//
// Produces a self-contained static site you can drag onto Cloudflare Pages or Netlify:
//
//   site/index.html      Hebrew landing page, one tile per project
//   site/p4/index.html   that project's card list, in teaching order
//   site/p4/*.dc.html    the cards themselves, copied verbatim
//   site/vendor/         React, ReactDOM and Babel, so no card depends on unpkg
//
// Only task_cards_he ships. Reference cards R1-R7 are the teacher's — that was Yon's
// call on 2026-08-25 ("כרטיסיות R למינהן מיועדות למורה ולא לתלמיד") — so they stay out.
//
// The cards are copied byte-for-byte; the ONLY edit is repointing support.js's three CDN
// constants at site/vendor. A school network that blocks unpkg would otherwise render
// every card blank, because the dc runtime needs React and Babel to draw anything.

const fs = require('fs');
const path = require('path');
const https = require('https');

const ROOT = __dirname;
const SRC = path.join(ROOT, 'Arduino_Projects');
const OUT = path.join(ROOT, 'site');

const VENDOR = [
  ['react.production.min.js', 'https://unpkg.com/react@18.3.1/umd/react.production.min.js'],
  ['react-dom.production.min.js', 'https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js'],
  ['babel.min.js', 'https://unpkg.com/@babel/standalone@7.26.4/babel.min.js'],
];

const only = (() => {
  const i = process.argv.indexOf('--projects');
  return i > 0 ? new Set(process.argv[i + 1].split(',').map(Number)) : null;
})();

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
  .replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function get(url) {
  return new Promise((res, rej) => {
    https.get(url, (r) => {
      if (r.statusCode >= 300 && r.statusCode < 400 && r.headers.location) {
        return get(r.headers.location).then(res, rej);
      }
      if (r.statusCode !== 200) return rej(new Error(url + ' -> ' + r.statusCode));
      const c = [];
      r.on('data', (d) => c.push(d));
      r.on('end', () => res(Buffer.concat(c)));
    }).on('error', rej);
  });
}

// ---------------------------------------------------------------- discover projects
function discover() {
  return fs.readdirSync(SRC)
    .filter((d) => /^Project_\d+_/.test(d))
    .map((d) => {
      const n = Number(d.match(/^Project_(\d+)_/)[1]);
      const cards = path.join(SRC, d, 'task_cards_he');
      return { n, dir: d, cards, ok: fs.existsSync(cards) };
    })
    .filter((p) => p.ok && (!only || only.has(p.n)))
    .sort((a, b) => a.n - b.n);
}

// The eyebrow pill on every card reads "פרויקט 4 • מכונית עוקבת קו" — the project's own
// Hebrew name, authored by Yon. Take it from there rather than inventing one.
function projectName(cardsDir, files) {
  for (const f of files) {
    const s = fs.readFileSync(path.join(cardsDir, f), 'utf8');
    // the separator is · (U+00B7) on most projects and • (U+2022) on P3/P4 — accept either
    const m = s.match(/פרויקט\s*\d+\s*[·•]\s*([^<\n]{2,60}?)\s*(?:<|$)/m);
    if (m) return m[1].trim();
  }
  return null;
}

// card_nav.js is generated and holds both the prev/next chain and each card's Hebrew
// title. Walking the chain gives teaching order; sorting filenames would put M10 before M2.
function readNav(cardsDir) {
  const p = path.join(cardsDir, 'card_nav.js');
  if (!fs.existsSync(p)) return { nav: {}, lbl: {} };
  const s = fs.readFileSync(p, 'utf8');
  const grab = (name) => {
    const m = s.match(new RegExp('var\\s+' + name + '\\s*=\\s*(\\{[\\s\\S]*?\\});'));
    try { return m ? JSON.parse(m[1]) : {}; } catch { return {}; }
  };
  return { nav: grab('NAV'), lbl: grab('LBL') };
}

// A card's "next" is usually a filename, but Project 1 branches: on the pick-a-pattern card
// it is {k, m:{A,B,C}, d} — a choice with a default. Follow the default for the main line and
// surface the other branches separately, so no card becomes unreachable from the index.
function nextOf(v) {
  if (!v) return null;
  const n = v.next;
  if (typeof n === 'string') return n;
  if (n && typeof n === 'object') return typeof n.d === 'string' ? n.d : null;
  return null;
}

function branchesOf(v) {
  const n = v && v.next;
  if (!n || typeof n !== 'object' || !n.m) return [];
  return Object.values(n.m).filter((x) => typeof x === 'string');
}

function orderCards(files, nav) {
  const known = new Set(files);
  const seen = new Set();
  const chains = [];
  const alts = new Set();
  for (const f of files) {
    if (seen.has(f) || !nav[f] || nav[f].prev) continue;   // chain heads only
    const chain = [];
    let cur = f;
    while (cur && known.has(cur) && !seen.has(cur)) {
      chain.push(cur);
      seen.add(cur);
      branchesOf(nav[cur]).forEach((b) => alts.add(b));
      cur = nextOf(nav[cur]);
    }
    if (chain.length) chains.push(chain);
  }
  // branch alternatives first (they belong to a chain), then anything else, e.g. the T3 planner
  const loose = [...files.filter((f) => !seen.has(f) && alts.has(f)),
                 ...files.filter((f) => !seen.has(f) && !alts.has(f))];
  loose.forEach((f) => seen.add(f));
  return { chains, loose };
}

// ---------------------------------------------------------------- page templates
const SHELL = (title, body) => `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  *{box-sizing:border-box}
  body{margin:0;font-family:'Rubik',system-ui,sans-serif;background:oklch(0.972 0.008 85);
       color:oklch(0.28 0.012 260);-webkit-font-smoothing:antialiased;padding:40px 20px}
  .wrap{max-width:860px;margin:0 auto}
  .top{background:oklch(0.45 0.11 248);color:#fff;border-radius:22px;padding:32px 34px;margin-bottom:26px}
  h1{margin:0;font-size:29px;line-height:1.25;font-weight:700}
  .sub{margin-top:10px;font-size:16px;color:rgba(255,255,255,0.86);line-height:1.55}
  .back{display:inline-block;margin-bottom:18px;font-size:15px;color:oklch(0.45 0.11 248);text-decoration:none;font-weight:600}
  .back:hover{text-decoration:underline}
  .grid{display:grid;gap:14px}
  a.tile{display:block;background:#fff;border:1px solid oklch(0.92 0.006 85);border-radius:16px;
         padding:18px 20px;text-decoration:none;color:inherit;transition:border-color .12s,transform .12s}
  a.tile:hover{border-color:oklch(0.45 0.11 248);transform:translateY(-1px)}
  .num{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;
       border-radius:11px;background:oklch(0.94 0.03 248);color:oklch(0.45 0.11 248);
       font-weight:700;font-size:17px;margin-left:14px;flex:none}
  .row{display:flex;align-items:center}
  .name{font-size:18px;font-weight:700}
  .meta{font-size:14px;color:oklch(0.5 0.012 260);margin-top:3px}
  h2{font-size:17px;font-weight:700;margin:26px 0 12px;color:oklch(0.34 0.012 260)}
  .step{display:flex;align-items:center;gap:13px}
  .badge{flex:none;min-width:62px;font-size:13px;font-weight:600;color:oklch(0.45 0.11 248)}
  .foot{margin-top:34px;font-size:13.5px;color:oklch(0.55 0.012 260);text-align:center;line-height:1.7}
</style>
</head>
<body><div class="wrap">${body}</div></body>
</html>
`;

function indexPage(projects) {
  const tiles = projects.map((p) => `
    <a class="tile" href="p${p.n}/index.html">
      <div class="row">
        <span class="num">${p.n}</span>
        <div>
          <div class="name">${esc(p.name || ('פרויקט ' + p.n))}</div>
          <div class="meta">${p.count} כרטיסיות</div>
        </div>
      </div>
    </a>`).join('');
  return SHELL('הפרויקטים שלנו', `
    <div class="top">
      <h1>הפרויקטים שלנו</h1>
      <div class="sub">בוחרים פרויקט, ואז עוברים על הכרטיסיות לפי הסדר. אפשר לסמן ✓ בכל שלב שמסיימים.</div>
    </div>
    <div class="grid">${tiles}</div>
    <div class="foot">סדנת רובוטיקה</div>`);
}

function projectPage(p) {
  const link = (f) => {
    if (typeof f !== 'string') return '';
    // Standalone cards (the T3 planner) are absent from card_nav's label map, so fall back to
    // the card's own h1 rather than showing a filename to a student.
    const l = p.lbl[f] || { title: p.titles[f] };
    return `<a class="tile" href="${encodeURIComponent(f)}">
      <div class="step">
        <span class="badge">${esc(l.label || '')}</span>
        <span class="name">${esc(l.title || f.replace(/\.dc\.html$/, ''))}</span>
      </div>
    </a>`;
  };
  const parts = [];
  p.chains.forEach((chain, i) => {
    parts.push(`<h2>${p.chains.length > 1 ? 'מסלול ' + (i + 1) : 'הכרטיסיות'}</h2>`);
    parts.push('<div class="grid">' + chain.map(link).join('') + '</div>');
  });
  if (p.loose.length) {
    parts.push('<h2>נוסף</h2><div class="grid">' + p.loose.map(link).join('') + '</div>');
  }
  return SHELL(p.name || ('פרויקט ' + p.n), `
    <a class="back" href="../index.html">→ חזרה לכל הפרויקטים</a>
    <div class="top">
      <h1>${esc(p.name || ('פרויקט ' + p.n))}</h1>
      <div class="sub">פרויקט ${p.n} · ${p.count} כרטיסיות</div>
    </div>
    ${parts.join('\n')}`);
}

// ---------------------------------------------------------------- build
(async () => {
  const projects = discover();
  if (!projects.length) { console.error('no projects found'); process.exit(1); }

  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(OUT, { recursive: true });

  // vendor the runtime once
  const vdir = path.join(OUT, 'vendor');
  fs.mkdirSync(vdir, { recursive: true });
  const cache = path.join(ROOT, '.vendor-cache');
  fs.mkdirSync(cache, { recursive: true });
  for (const [name, url] of VENDOR) {
    const cached = path.join(cache, name);
    if (!fs.existsSync(cached)) {
      process.stdout.write('  downloading ' + name + ' ... ');
      fs.writeFileSync(cached, await get(url));
      console.log('ok');
    }
    fs.copyFileSync(cached, path.join(vdir, name));
  }
  console.log('vendor/ ready (react, react-dom, babel)');

  let totalCards = 0;
  for (const p of projects) {
    const files = fs.readdirSync(p.cards).filter((f) => f.endsWith('.dc.html')).sort();
    if (!files.length) continue;
    const dest = path.join(OUT, 'p' + p.n);
    fs.cpSync(p.cards, dest, { recursive: true });

    // repoint the runtime at our own copy — relative to the CARD's url, so ../vendor/
    const sp = path.join(dest, 'support.js');
    if (fs.existsSync(sp)) {
      let s = fs.readFileSync(sp, 'utf8');
      let hits = 0;
      for (const [name] of VENDOR) {
        const rx = new RegExp('"https://unpkg\\.com/[^"]*' + name.replace(/\./g, '\\.') + '"');
        if (rx.test(s)) { s = s.replace(rx, '"../vendor/' + name + '"'); hits++; }
      }
      fs.writeFileSync(sp, s);
      if (hits !== VENDOR.length) {
        console.log('  ! p' + p.n + ': repointed only ' + hits + '/' + VENDOR.length +
                    ' CDN urls — check support.js');
      }
    }

    // Two asset conventions exist: most cards use ./assets/, but Project 1's wiring figures
    // are referenced as ../images/. Copy those in too or they 404 on the site.
    const extra = new Set();
    for (const f of files) {
      const s = fs.readFileSync(path.join(dest, f), 'utf8');
      for (const m of s.matchAll(/src="\.\.\/images\/([^"]+)"/g)) extra.add(m[1]);
    }
    if (extra.size) {
      const imgDir = path.join(dest, 'images');
      fs.mkdirSync(imgDir, { recursive: true });
      let copied = 0, missing = [];
      for (const rel of extra) {
        const from = path.join(SRC, p.dir, 'images', rel);
        if (fs.existsSync(from)) {
          fs.mkdirSync(path.dirname(path.join(imgDir, rel)), { recursive: true });
          fs.copyFileSync(from, path.join(imgDir, rel));
          copied++;
        } else missing.push(rel);
      }
      // In the repo a card sits at Project_N/task_cards_he/, so ../images/ points at
      // Project_N/images/. On the site it sits at site/pN/, where ../images/ would escape
      // to site/images/ and 404. Repoint at the copy we just made beside it.
      for (const f of files) {
        const fp = path.join(dest, f);
        const s = fs.readFileSync(fp, 'utf8');
        if (s.includes('../images/')) {
          fs.writeFileSync(fp, s.split('"../images/').join('"./images/'));
        }
      }
      console.log('     + ' + copied + ' file(s) from ../images/ (paths repointed)' +
                  (missing.length ? '  MISSING: ' + missing.join(', ') : ''));
    }

    const { nav, lbl } = readNav(p.cards);
    const { chains, loose } = orderCards(files, nav);
    // h1 of each card, for anything card_nav does not label
    const titles = {};
    for (const f of files) {
      const m = fs.readFileSync(path.join(dest, f), 'utf8').match(/<h1[^>]*>([\s\S]*?)<\/h1>/);
      if (m) titles[f] = m[1].replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
    }
    Object.assign(p, { name: projectName(p.cards, files), count: files.length,
                       lbl, chains, loose, titles });
    fs.writeFileSync(path.join(dest, 'index.html'), projectPage(p));
    totalCards += files.length;
    console.log('  p' + p.n + '  ' + String(files.length).padStart(2) + ' cards  ' + (p.name || ''));
  }

  fs.writeFileSync(path.join(OUT, 'index.html'), indexPage(projects));
  // Netlify/Cloudflare serve .dc.html fine, but be explicit that this is not a SPA
  fs.writeFileSync(path.join(OUT, '_headers'),
    '/*\n  Cache-Control: public, max-age=3600\n/vendor/*\n  Cache-Control: public, max-age=31536000, immutable\n');

  const du = (d) => fs.readdirSync(d, { withFileTypes: true }).reduce((a, e) => {
    const f = path.join(d, e.name);
    return a + (e.isDirectory() ? du(f) : fs.statSync(f).size);
  }, 0);
  console.log('\nsite/  ' + projects.length + ' projects, ' + totalCards + ' cards, ' +
              (du(OUT) / 1048576).toFixed(1) + ' MB');
  console.log('preview:  npx serve site     (or: cd site && python -m http.server 8000)');
})();
