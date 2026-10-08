// build_drive_support.js — everything Claude Code needs to support a student
// inside their project folder on the workshop Drive.
//
//   node build_drive_support.js              build into Arduino_Projects/_drive_support/
//   node build_drive_support.js --install    ...and copy into the Drive (I:\My Drive\Arduino_Projects)
//
// Claude Code loads CLAUDE.md from the working directory and every parent, so a
// student launched in  Arduino_Projects/Project_3_.../<nickname>/  gets:
//   Arduino_Projects/CLAUDE.md            the shared support guidelines (hand-written,
//                                         _drive_support/CLAUDE.md — this script never touches it)
//   Arduino_Projects/Project_3_.../CLAUDE.md   generated: hardware, sketches, card index, teacher gates
//   .../Project_3_.../claude_support/cards/      generated: every task card as plain text, teaching order
//   .../Project_3_.../claude_support/reference/  generated: the R cards as plain text
//
// The card text is extracted straight from the HE .dc.html sources (no browser),
// so re-running after any card edit keeps the Drive copy current. --install also
// makes sure each project's shared ino_files/ holds exactly the repo's sketches
// (it never touches a student's own ino_files/).

const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const SRC = path.join(ROOT, 'Arduino_Projects');
const OUT = path.join(SRC, '_drive_support');
const DRIVE = 'I:\\My Drive\\Arduino_Projects';
const INSTALL = process.argv.includes('--install');
const dirs = fs.readdirSync(SRC).filter((d) => /^Project_\d+_/.test(d)).sort((a, b) => Number(a.match(/\d+/)[0]) - Number(b.match(/\d+/)[0]));
const dirOf = (n) => dirs.find((d) => d.startsWith('Project_' + n + '_'));
// Projects 5-7 ship no reference cards of their own; their teacher sheets say "use project 4's".
const REF_FALLBACK = { 5: 4, 6: 4, 7: 4 };

// ---------------------------------------------------------------- shared data
// Teacher-sheet data (materials, which R cards each project uses) and the per-project
// hardware/skills summary are read from the scripts that already own them.
const tm = fs.readFileSync(path.join(ROOT, 'build_teacher_materials.js'), 'utf8');
const TEACHER = new Function('return ' + tm.match(/const PROJECTS = (\{[\s\S]*?\n\});/)[1])();

const SUMMARY = {
  1: ['Arduino Uno + לדים + כפתור', 'חיווט ברדבורד, קלט/פלט דיגיטלי, העלאה ראשונה, היכרות עם קלוד קוד'],
  2: ['ארדואינו + לדים + זמזם + כפתורים', 'תזמון, לוגיקת משחק'],
  3: ['ארדואינו + חיישן אולטרסוני', 'קריאת חיישן, לוגיקת סף'],
  4: ['שלדת פוליגל בעבודת יד + 4 מנועים + חיישני קו', 'הלחמה ראשונה, בניית שלדה, בקר מנועים, שליטה במנועים ובתנועה דרך קוד'],
  5: ['שלדת פרויקט 4 + ESP32 + עמוד שליטה בדפדפן הטלפון', 'ESP32 ראשון, שליטה מדף ווב (Wi-Fi)'],
  6: ['ESP32 + חיישן טמפרטורה ולחות + מסך OLED', 'חיישנים, מסך, נתונים חיים בדפדפן'],
  7: ['ESP32-CAM + שלדת המכונית', 'מימוש בשטח: הזרמת וידאו + נהיגה'],
  8: ['רחפן ESP32 בבנייה עצמית', 'פרויקט שיא: הלחמה מדויקת, חיישן ג׳יירו, עקרונות תעופה בסיסיים, פרוטוקול בטיחות'],
  9: ['ESP32-S3 + חיישן אופטי PMW3360 + מתגים + גלגלת + סוללת 18650', 'עכבר אישי: הלחמה, לוח כוח, יום הסוללה, Bluetooth'],
};

// ---------------------------------------------------------------- card text
const ent = (s) => s.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>')
  .replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&#x27;/g, "'").replace(/&#(\d+);/g, (_, n) => String.fromCharCode(n));

// HTML -> readable text. Block tags become line breaks, figures become "[איור: alt]",
// the dc checkbox overlays (<sc-if>) and all runtime markup are dropped.
function cardText(html) {
  let t = html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<helmet>[\s\S]*?<\/helmet>/gi, '')
    .replace(/<sc-if[\s\S]*?<\/sc-if>/gi, '')
    .replace(/<img[^>]*\balt="([^"]*)"[^>]*>/gi, (_, alt) => '\n[איור: ' + alt + ']\n')
    .replace(/<img[^>]*>/gi, '')
    .replace(/<span[^>]*>\s*\d+%\s*<\/span>/g, '')
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/<\/(p|div|h[1-6]|li|tr|pre|section|nav)>/gi, '\n')
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<[^>]+>/g, '');
  t = ent(t);
  const lines = t.split('\n').map((l) => l.replace(/\s+/g, ' ').trim()).filter(Boolean)
    .map((l) => l.replace(/^(\p{Extended_Pictographic}️?)(?=[^\s\p{Extended_Pictographic}])/u, '$1 '));
  // a numbered-step circle is its own line in the HTML — fold it into the step text
  const out = [];
  for (let i = 0; i < lines.length; i++) {
    if (/^\d{1,2}$/.test(lines[i]) && i + 1 < lines.length && !/^\d{1,2}$/.test(lines[i + 1])) { out.push(lines[i] + '. ' + lines[i + 1]); i++; }
    else out.push(lines[i]);
  }
  return out.join('\n');
}

const stripEmoji = (s) => s.replace(/^[\s\p{Extended_Pictographic}️‍]+/u, '').trim();
const h1Of = (html) => {
  const m = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/);
  return m ? stripEmoji(ent(m[1].replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ')) : '';
};
const stepOf = (html) => { const m = html.match(/שלב\s+(\d+)\s+מתוך\s+(\d+)/); return m ? m[1] + ' מתוך ' + m[2] : ''; };
const hasGate = (html) => /<!-- GATE:/.test(html);
const gateNoun = (html) => { const m = html.match(/עוברים קודם עם המורה על\s*<strong>([^<]+)<\/strong>/); return m ? m[1] : ''; };

// ---------------------------------------------------------------- card order (same walk as build_site.js)
function readNav(dir) {
  const p = path.join(dir, 'card_nav.js');
  if (!fs.existsSync(p)) return {};
  const s = fs.readFileSync(p, 'utf8');
  const m = s.match(/var\s+NAV\s*=\s*(\{[\s\S]*?\});/);
  try { return m ? JSON.parse(m[1]) : {}; } catch { return {}; }
}
const nextOf = (v) => { const n = v && v.next; return typeof n === 'string' ? n : (n && typeof n.d === 'string' ? n.d : null); };
const branchesOf = (v) => { const n = v && v.next; return (n && typeof n === 'object' && n.m) ? Object.values(n.m).filter((x) => typeof x === 'string') : []; };

function orderCards(files, nav) {
  const known = new Set(files), seen = new Set(), chains = [], alts = new Set();
  for (const f of files) {
    if (seen.has(f) || !nav[f] || nav[f].prev) continue;
    const chain = []; let cur = f;
    while (cur && known.has(cur) && !seen.has(cur)) { chain.push(cur); seen.add(cur); branchesOf(nav[cur]).forEach((b) => alts.add(b)); cur = nextOf(nav[cur]); }
    if (chain.length) chains.push(chain);
  }
  const loose = [...files.filter((f) => !seen.has(f) && alts.has(f)), ...files.filter((f) => !seen.has(f) && !alts.has(f))];
  return { chains, loose };
}

const tierOf = (f) => { const m = f.match(/T(\d)_/); return m ? Number(m[1]) : 0; };

// ---------------------------------------------------------------- sketches
// Each .ino opens with a comment banner; its first meaningful lines are the description.
function sketchBlurb(file) {
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/).slice(0, 25);
  const out = [];
  for (const raw of lines) {
    const l = raw.replace(/^\s*(\/\/|\/\*|\*\/|\*)\s?/, '').trim();
    if (!/^\s*(\/\/|\/\*|\*)/.test(raw) && raw.trim() !== '') break;   // past the banner
    if (!l || /^[=\-]{4,}$/.test(l) || /\.ino$/i.test(l) || /^(Tools settings|Library|Board):/i.test(l)) continue;
    if (/^Project \d+\b/.test(l) && !/step|שלב/i.test(l)) continue;   // the banner repeats the project name
    out.push(l.replace(/^WHAT THIS SKETCH DOES:\s*/i, ''));
    if (out.join(' ').length > 230) break;
  }
  const text = out.join(' ').replace(/\s+/g, ' ');
  return text.length <= 240 ? text : text.slice(0, 240).replace(/\s+\S*$/, '') + '…';
}

// ---------------------------------------------------------------- per project
function projectBlock(n, dir) {
  const t = TEACHER[String(n)];
  const cardsDir = path.join(SRC, dir, 'task_cards_he');
  const refDir = path.join(SRC, dir, 'reference_cards_he');
  const inoDir = path.join(SRC, dir, 'ino_files');
  const outDir = path.join(OUT, dir);
  const outCards = path.join(outDir, 'claude_support', 'cards');
  const outRef = path.join(outDir, 'claude_support', 'reference');
  fs.rmSync(path.join(outDir, 'claude_support'), { recursive: true, force: true });
  fs.mkdirSync(outCards, { recursive: true });
  fs.mkdirSync(outRef, { recursive: true });

  // cards, in teaching order
  const files = fs.readdirSync(cardsDir).filter((f) => f.endsWith('.dc.html')).sort();
  const nav = readNav(cardsDir);
  const { chains, loose } = orderCards(files, nav);
  const ordered = [...chains.flat(), ...loose];
  const index = { 1: [], 2: [], 3: [] };
  const gates = [];
  ordered.forEach((f, i) => {
    const html = fs.readFileSync(path.join(cardsDir, f), 'utf8');
    const stem = f.replace(/_he\.dc\.html$/, '');
    const num = String(i + 1).padStart(2, '0');
    const mdName = num + '_' + stem + '.md';
    const title = h1Of(html), step = stepOf(html), tier = tierOf(f) || 3;
    const gate = hasGate(html) ? gateNoun(html) : '';
    const head = '# ' + title + '\n\n' + 'פרויקט ' + n + ' · גרסה ' + tier + (step ? ' · שלב ' + step : '') +
      (gate ? '\n\n> ⛔ שער: לפני השלב הזה התלמיד עובר עם המורה על ' + gate + '. אם זה לא נעשה — מפנים למורה.' : '') +
      '\n\n---\n\n';
    fs.writeFileSync(path.join(outCards, mdName), head + cardText(html) + '\n', 'utf8');
    index[tier].push({ mdName, title, step, gate });
    if (gate) gates.push({ title, gate, step, tier });
  });

  // reference cards
  const refs = [];
  const refFrom = fs.existsSync(refDir) ? refDir
    : REF_FALLBACK[n] ? path.join(SRC, dirOf(REF_FALLBACK[n]), 'reference_cards_he') : null;
  const borrowed = Boolean(refFrom && refFrom !== refDir);
  if (refFrom && fs.existsSync(refFrom)) {
    for (const f of fs.readdirSync(refFrom).filter((x) => x.endsWith('.dc.html')).sort()) {
      const html = fs.readFileSync(path.join(refFrom, f), 'utf8');
      const stem = f.replace(/_he\.dc\.html$/, '');
      const title = h1Of(html);
      const safety = /safety|soldering|flight|battery/i.test(stem);
      fs.writeFileSync(path.join(outRef, stem + '.md'),
        '# ' + title + '\n\n' + (borrowed ? '> כרטיסיית עזר של פרויקט ' + REF_FALLBACK[n] + ' — משמשת גם בפרויקט הזה.\n\n' : '') + (safety ? '> כרטיסיית בטיחות — המורה מתדרך אותה. מותר להזכיר ממנה כלל במילים שלה; לא מתדרכים ולא מרחיבים.\n\n' : '') +
        '---\n\n' + cardText(html) + '\n', 'utf8');
      refs.push({ stem, title, safety });
    }
  }

  // sketches
  const sketches = fs.existsSync(inoDir)
    ? fs.readdirSync(inoDir).filter((d) => fs.existsSync(path.join(inoDir, d, d + '.ino'))).sort()
      .map((d) => ({ name: d, blurb: sketchBlurb(path.join(inoDir, d, d + '.ino')) }))
    : [];

  // the project CLAUDE.md
  const L = [];
  L.push('# פרויקט ' + n + ': ' + t.name + ' — הנחיות לקלוד קוד');
  L.push('');
  L.push('ההנחיות הכלליות ב-`../CLAUDE.md` חלות תמיד. כאן רק מה שמיוחד לפרויקט הזה.');
  L.push('');
  L.push('## הפרויקט בקצרה');
  L.push('');
  L.push('- **חומרה:** ' + SUMMARY[n][0]);
  L.push('- **מה לומדים:** ' + SUMMARY[n][1]);
  L.push('- **מעטפת הבטיחות (למידע בלבד — המורה מתדרך):** ' + t.envelope.replace(/<[^>]+>/g, ''));
  L.push('');
  L.push('## מה על השולחן');
  L.push('');
  for (const [qty, item] of t.materials) L.push('- ' + qty + ' × ' + item.replace(/<[^>]+>/g, ''));
  L.push('');
  L.push('## הסקיצות (`ino_files/`)');
  L.push('');
  L.push('גרסה 1 מעלה את הסקיצות הממוספרות כמו שהן, לפי הסדר שהכרטיסיות מכתיבות. `T2_*` הן נקודות הפתיחה של גרסה 2 — שם התלמיד משנה דבר אחד שהכרטיסייה מצביעה עליו.');
  L.push('');
  for (const s of sketches) L.push('- `' + s.name + '` — ' + s.blurb);
  L.push('');
  L.push('## הכרטיסיות (`claude_support/cards/`)');
  L.push('');
  L.push('קוראים את קובץ הכרטיסייה לפני שעונים על כל שאלה על שלב. הקבצים ממוספרים לפי סדר הלימוד.');
  for (const tier of [1, 2, 3]) {
    if (!index[tier].length) continue;
    L.push('');
    L.push('### גרסה ' + tier + (tier === 1 ? ' — בנייה מודרכת' : tier === 2 ? ' — עיצוב מודרך' : ' — עיצוב פתוח'));
    L.push('');
    for (const c of index[tier]) L.push('- `' + c.mdName + '` — ' + c.title + (c.gate ? '  ⛔ שער: ' + c.gate : ''));
  }
  L.push('');
  L.push('## כרטיסיות העזר (`claude_support/reference/`)');
  L.push('');
  if (borrowed) L.push('לפרויקט הזה אין כרטיסיות עזר משלו — אלה כרטיסיות העזר של פרויקט ' + REF_FALLBACK[n] + ', שמשמשות גם כאן.\n');
  for (const r of refs) L.push('- `' + r.stem + '.md` — ' + r.title + (r.safety ? ' (בטיחות — של המורה)' : ''));
  L.push('');
  L.push('## נקודות שמצריכות את המורה בפרויקט הזה');
  L.push('');
  L.push('- שלב 1 נעשה יחד עם המורה (לא ערוץ B).');
  for (const g of gates) L.push('- גרסה ' + g.tier + (g.step ? ', שלב ' + g.step.split(' ')[0] : '') + ' — "' + g.title + '": לפני השלב התלמיד עובר עם המורה על ' + g.gate + '.');
  L.push('- כל מה שהכרטיסייה מסמנת "קוראים למורה".');
  L.push('- בטיחות: ' + t.cards.replace(/<[^>]+>/g, '') + ' — התדריך של המורה, לא שלך.');
  L.push('');
  fs.writeFileSync(path.join(outDir, 'CLAUDE.md'), L.join('\n'), 'utf8');

  console.log('  P' + n + '  ' + ordered.length + ' cards (' + gates.length + ' gates), ' + refs.length + ' reference, ' + sketches.length + ' sketches');
  return { dir, sketches: sketches.map((s) => s.name) };
}

// ---------------------------------------------------------------- install
function copyDir(from, to) {
  fs.mkdirSync(to, { recursive: true });
  for (const e of fs.readdirSync(from, { withFileTypes: true })) {
    const a = path.join(from, e.name), b = path.join(to, e.name);
    if (e.isDirectory()) copyDir(a, b); else fs.copyFileSync(a, b);
  }
}

// Project-level Claude Code settings, so a student is never stopped by an "Allow?"
// prompt for the things the guidelines tell Claude to do (read the cards and the
// sketch, look around the folder) — while anything that changes the machine stays
// behind a prompt. Settings are read from the working directory's .claude/, so every
// project folder gets a copy (a student folder inherits it from the parent).
const SETTINGS = {
  permissions: {
    allow: ['Read', 'Glob', 'Grep', 'Edit', 'Write'],
    deny: ['Bash(rm *)', 'Bash(del *)', 'Bash(git *)', 'WebFetch', 'WebSearch'],
  },
};
function writeSettings(dir) {
  fs.mkdirSync(path.join(dir, '.claude'), { recursive: true });
  fs.writeFileSync(path.join(dir, '.claude', 'settings.json'), JSON.stringify(SETTINGS, null, 2) + '\n', 'utf8');
}

function install(projects) {
  if (!fs.existsSync(DRIVE)) { console.error('Drive not mounted: ' + DRIVE); process.exit(1); }
  fs.copyFileSync(path.join(OUT, 'CLAUDE.md'), path.join(DRIVE, 'CLAUDE.md'));
  writeSettings(DRIVE);
  console.log('  Drive/CLAUDE.md + .claude/settings.json');
  for (const { dir, sketches } of projects) {
    const dst = path.join(DRIVE, dir);
    if (!fs.existsSync(dst)) { console.log('  ! ' + dir + ' not on the Drive — skipped'); continue; }
    fs.copyFileSync(path.join(OUT, dir, 'CLAUDE.md'), path.join(dst, 'CLAUDE.md'));
    writeSettings(dst);
    fs.rmSync(path.join(dst, 'claude_support'), { recursive: true, force: true });
    copyDir(path.join(OUT, dir, 'claude_support'), path.join(dst, 'claude_support'));

    // shared ino_files/ = exactly the repo's sketches for this project
    const ino = path.join(dst, 'ino_files');
    fs.mkdirSync(ino, { recursive: true });
    const notes = [];
    for (const s of sketches) {
      const src = path.join(SRC, dir, 'ino_files', s, s + '.ino');
      const d = path.join(ino, s);
      fs.mkdirSync(d, { recursive: true });
      const tgt = path.join(d, s + '.ino');
      const same = (a, b) => fs.readFileSync(a, 'utf8').replace(/\r\n/g, '\n') === fs.readFileSync(b, 'utf8').replace(/\r\n/g, '\n');
      if (!fs.existsSync(tgt)) { fs.copyFileSync(src, tgt); notes.push('+' + s); }
      else if (!same(tgt, src)) notes.push('~' + s + ' (differs from repo — left alone)');
    }
    for (const d of fs.readdirSync(ino, { withFileTypes: true })) {
      if (!d.isDirectory() || sketches.includes(d.name)) continue;
      // a sketch that belongs to another project (a copy slip) — remove only if it is an
      // exact duplicate of that other project's repo file, so nothing unique is ever lost
      let dup = false;
      for (const p of projects) {
        const other = path.join(SRC, p.dir, 'ino_files', d.name, d.name + '.ino');
        const here = path.join(ino, d.name, d.name + '.ino');
        if (fs.existsSync(other) && fs.existsSync(here) && fs.readFileSync(other, 'utf8') === fs.readFileSync(here, 'utf8')) { dup = true; break; }
      }
      if (dup) { fs.rmSync(path.join(ino, d.name), { recursive: true, force: true }); notes.push('-' + d.name + ' (belonged to another project)'); }
      else notes.push('?' + d.name + ' (unknown sketch — left alone)');
    }
    console.log('  Drive/' + dir + (notes.length ? '   ino_files: ' + notes.join(', ') : ''));
  }
}

// ---------------------------------------------------------------- main
fs.mkdirSync(OUT, { recursive: true });
if (!fs.existsSync(path.join(OUT, 'CLAUDE.md'))) { console.error('missing hand-written ' + path.join(OUT, 'CLAUDE.md')); process.exit(1); }
console.log('building ' + path.relative(ROOT, OUT));
const built = dirs.map((d) => projectBlock(Number(d.match(/^Project_(\d+)_/)[1]), d));
if (INSTALL) { console.log('installing into ' + DRIVE); install(built); }
console.log('done');
