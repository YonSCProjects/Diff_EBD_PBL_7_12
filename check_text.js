// check_text.js <classic.html> <dc.html> — verify every content text segment of the
// classic card appears verbatim (whitespace-normalized) in the dc redesign.
// Exit 0 = all present; exit 1 = missing segments (printed as JSON).
const fs = require('fs');

const INLINE = /<\/?(strong|em|b|i|u|a|code|span|small|sub|sup|abbr|mark)\b[^>]*>/gi;

function decode(s) {
  return s
    .replace(/&nbsp;/g, ' ')
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&rarr;/g, '→')
    .replace(/&larr;/g, '←')
    .replace(/&harr;/g, '↔')
    .replace(/&times;/g, '×')
    .replace(/&middot;/g, '·')
    .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
    .replace(/&amp;/g, '&');
}

function norm(s) {
  return decode(s)
    .replace(/\{\{[^}]*\}\}/g, ' ')
    .replace(/[ ‏‎]/g, ' ')
    .replace(/[“”„]/g, '"')
    .replace(/[‘’]/g, "'")
    .replace(/[—–]/g, '-')
    .replace(/…/g, '...')
    .replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{FE0F}\u{200D}\u{2190}-\u{21FF}]/gu, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function textOf(html) {
  return html
    .replace(/<!--[\s\S]*?-->/g, ' ')
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<title[\s\S]*?<\/title>/gi, ' ')
    .replace(INLINE, '')
    .replace(/<[^>]+>/g, '\n');
}

const [classicPath, dcPath] = process.argv.slice(2);
const classic = textOf(fs.readFileSync(classicPath, 'utf8'));
const dcRaw = fs.readFileSync(dcPath, 'utf8');
const dc = norm(textOf(dcRaw));
// alt attributes carry content too
const dcAlts = norm([...dcRaw.matchAll(/alt="([^"]*)"/g)].map((m) => m[1]).join(' '));
const dcAll = dc + ' ' + dcAlts;

const segs = classic
  .split('\n')
  .map(norm)
  .filter((s) => {
    if (s.length < 8) return false;
    const hasHebrew = /[֐-׿]/.test(s);
    return hasHebrew ? s.length >= 8 : s.length >= 15;
  });

const seen = new Set();
const missing = [];
for (const s of segs) {
  if (seen.has(s)) continue;
  seen.add(s);
  if (!dcAll.includes(s)) missing.push(s);
}

console.log(JSON.stringify({ classic: classicPath, dc: dcPath, total: seen.size, missingCount: missing.length, missing }, null, 1));
process.exit(missing.length ? 1 : 0);
