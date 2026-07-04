// review_server.js — tiny dependency-free local server for the card-review console.
//
// Serves the repo root over http://127.0.0.1:8765 so every card renders exactly
// as authored (per-project style.css, the P1 Claude-Design runtime, web fonts)
// and the review console can operate on same-origin iframes.
//
// Endpoints:
//   GET  /api/cards          -> JSON manifest of all Hebrew task cards (P1-P4)
//   POST /api/save-feedback  -> writes review_feedback/<baseName>.json + .md
//   GET  <anything else>     -> static file from the repo root
//
// Start:  node review_server.js       (or double-click start_review.bat)
// Stop :  Ctrl+C / close the window.

const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const PORT = 8765;
const HOST = '127.0.0.1';

const MIME = {
  '.html': 'text/html', '.htm': 'text/html', '.css': 'text/css',
  '.js': 'application/javascript', '.mjs': 'application/javascript',
  '.json': 'application/json', '.md': 'text/markdown', '.txt': 'text/plain',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.ico': 'image/x-icon',
  '.pdf': 'application/pdf', '.ino': 'text/plain',
  '.woff': 'font/woff', '.woff2': 'font/woff2', '.ttf': 'font/ttf',
};
const TEXTUAL = new Set(['.html', '.htm', '.css', '.js', '.mjs', '.json', '.md', '.txt', '.ino']);

// ---------------------------------------------------------------- manifest

function listCards() {
  const projectsDir = path.join(ROOT, 'Arduino_Projects');
  const cards = [];
  const projDirs = fs.readdirSync(projectsDir, { withFileTypes: true })
    .filter((d) => d.isDirectory() && /^Project_\d/.test(d.name))
    .map((d) => d.name)
    .sort();
  for (const proj of projDirs) {
    const dir = path.join(projectsDir, proj, 'task_cards_he');
    if (!fs.existsSync(dir)) continue;
    const files = fs.readdirSync(dir, { withFileTypes: true })
      .filter((d) => d.isFile() && d.name.toLowerCase().endsWith('.html'))
      .map((d) => d.name)
      .sort();
    const projNum = parseInt(proj.match(/^Project_(\d+)/)[1], 10);
    for (const f of files) {
      cards.push({
        file: `Arduino_Projects/${proj}/task_cards_he/${f}`,
        project: projNum,
        projectDir: proj,
        name: f.replace(/\.dc\.html$|\.html$/i, ''),
        flavor: f.toLowerCase().endsWith('.dc.html') ? 'dc' : 'classic',
      });
    }
  }
  return cards;
}

// ---------------------------------------------------------- save feedback

function saveFeedback(body) {
  const dir = path.join(ROOT, 'review_feedback');
  fs.mkdirSync(dir, { recursive: true });
  let base = String(body.baseName || 'feedback').replace(/[^A-Za-z0-9_\-]/g, '_');
  let candidate = base;
  let n = 2;
  while (fs.existsSync(path.join(dir, candidate + '.json')) ||
         fs.existsSync(path.join(dir, candidate + '.md'))) {
    candidate = `${base}_${n++}`;
  }
  const jsonPath = path.join(dir, candidate + '.json');
  const mdPath = path.join(dir, candidate + '.md');
  fs.writeFileSync(jsonPath, JSON.stringify(body.json, null, 2), 'utf8');
  fs.writeFileSync(mdPath, String(body.markdown || ''), 'utf8');
  return {
    json: path.relative(ROOT, jsonPath).replace(/\\/g, '/'),
    md: path.relative(ROOT, mdPath).replace(/\\/g, '/'),
  };
}

// ------------------------------------------------------------------ server

const server = http.createServer((req, res) => {
  const url = new URL(req.url, `http://${HOST}:${PORT}`);

  if (req.method === 'GET' && url.pathname === '/api/cards') {
    try {
      const cards = listCards();
      res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
      res.end(JSON.stringify({ cards }));
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: String(e.message || e) }));
    }
    return;
  }

  if (req.method === 'POST' && url.pathname === '/api/save-feedback') {
    let raw = '';
    req.on('data', (c) => { raw += c; if (raw.length > 30e6) req.destroy(); });
    req.on('end', () => {
      try {
        const body = JSON.parse(raw);
        const written = saveFeedback(body);
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ ok: true, written }));
      } catch (e) {
        res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({ ok: false, error: String(e.message || e) }));
      }
    });
    return;
  }

  // ---- static ----
  if (req.method !== 'GET') { res.writeHead(405); res.end(); return; }
  let rel = decodeURIComponent(url.pathname);
  if (rel === '/') rel = '/review_console.html';
  const full = path.normalize(path.join(ROOT, rel));
  if (!full.startsWith(path.normalize(ROOT + path.sep)) && full !== path.normalize(ROOT)) {
    res.writeHead(403); res.end('Forbidden'); return;
  }
  fs.stat(full, (err, st) => {
    if (err || !st.isFile()) {
      // dc-runtime fallback: some projects' task_cards_he reference ./support.js
      // but only Project 1 carries the file — serve P1's copy transparently.
      if (/\/task_cards_he\/support\.js$/i.test(rel.replace(/\\/g, '/'))) {
        const p1 = path.join(ROOT, 'Arduino_Projects', 'Project_1_Light_Signals', 'task_cards_he', 'support.js');
        if (fs.existsSync(p1)) {
          res.writeHead(200, { 'Content-Type': 'application/javascript; charset=utf-8', 'Cache-Control': 'no-store' });
          fs.createReadStream(p1).pipe(res);
          return;
        }
      }
      res.writeHead(404); res.end('Not found: ' + rel); return;
    }
    const ext = path.extname(full).toLowerCase();
    const mime = MIME[ext] || 'application/octet-stream';
    const type = TEXTUAL.has(ext) ? `${mime}; charset=utf-8` : mime;
    res.writeHead(200, { 'Content-Type': type, 'Cache-Control': 'no-store' });
    fs.createReadStream(full).pipe(res);
  });
});

server.on('error', (e) => {
  if (e.code === 'EADDRINUSE') {
    console.log(`Review server already running at http://${HOST}:${PORT}/ — opening that one is fine.`);
    process.exit(0);
  }
  throw e;
});

server.listen(PORT, HOST, () => {
  console.log('===========================================');
  console.log('  Card-review console is up.');
  console.log(`  Open:  http://${HOST}:${PORT}/review_console.html`);
  console.log('  Stop:  close this window (or Ctrl+C).');
  console.log('===========================================');
});
