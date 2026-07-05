// render_cards_lib.js — shared card-rendering helpers for the build scripts.
//
// Handles BOTH card flavors:
//   • classic  (*.html)     — static HTML + external CSS (card.js just adds an
//                             interactive, print-hidden checkbox layer).
//   • Claude-Design (*.dc.html) — <x-dc> + support.js React runtime + web fonts;
//                             the visible markup only exists AFTER the runtime
//                             resolves its {{ }} templates, so we must run JS and
//                             wait for it to settle before capturing.
//
// Exports:
//   resolveCardFile(dir, stemName, suffix)  -> actual filename, preferring the
//                                              .dc.html twin for HE task cards.
//   renderCardPdf(browser, fullPath)        -> A4 PDF Buffer (settled).
//   snapshotCardHtml(browser, fullPath)     -> { body, styles } post-render HTML
//                                              for the self-contained merged bundle.

const fs = require('fs');
const path = require('path');

const isDcPath = (p) => /\.dc\.html$/i.test(p);

const PDF_OPTS = {
  format: 'A4',
  printBackground: true,
  margin: { top: '10mm', right: '10mm', bottom: '10mm', left: '10mm' },
};

// Google Fonts used by the dc cards — inlined once into the merged HTML head.
const DC_FONTS_LINK =
  '<link rel="preconnect" href="https://fonts.googleapis.com">' +
  '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>' +
  '<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">';

// Prefer the `.dc.html` twin when it exists (HE task cards were redesigned into
// the dc design system; their classic twins are retired). Falls back to classic
// so EN builds and reference cards keep working unchanged. dc task cards are named
// inconsistently — P1 has no project prefix, P2/P3/P4 carry a `P<key>_` prefix —
// so both candidates are tried. `projectKey` is optional (only task cards use it).
function resolveCardFile(dir, stemName, suffix, projectKey) {
  const candidates = [`${stemName}${suffix}.dc.html`];
  if (projectKey) candidates.push(`P${projectKey}_${stemName}${suffix}.dc.html`);
  for (const c of candidates) {
    if (fs.existsSync(path.join(dir, c))) return c;
  }
  return `${stemName}${suffix}.html`;
}

async function preparePage(browser, fullPath) {
  const page = await browser.newPage();
  page.on('dialog', (d) => d.dismiss().catch(() => {}));
  // Neutralize the classic card.js nickname prompt (no-op for dc cards).
  await page.evaluateOnNewDocument(() => {
    try { localStorage.setItem('agourim_card_nickname', 'סוקר'); } catch (e) {}
  });
  await page.emulateMediaType('print');
  const isDc = isDcPath(fullPath);
  const url = 'file:///' + fullPath.replace(/\\/g, '/');
  await page.goto(url, { waitUntil: isDc ? 'networkidle0' : 'load', timeout: 90000 });
  try { await page.evaluate(() => document.fonts && document.fonts.ready); } catch (e) {}
  if (isDc) { await settleDc(page); await tagBreaks(page); }
  return page;
}

// The dc cards style every element inline (no class hooks on the step cards or
// callout boxes), and carry no print page-break rules — so a naive A4 print can
// slice through a step card. Tag every "leaf" box (a rounded, filled/bordered
// element that contains no other such box — i.e. an individual step card, callout,
// code panel or diagram frame) with break-inside:avoid so it stays whole. Boxes
// taller than a page are ignored by the engine, so this only ever helps.
async function tagBreaks(page) {
  try {
    await page.evaluate(() => {
      const card = document.querySelector('.tc-card');
      if (!card) return;
      const isBox = (el) => {
        const s = getComputedStyle(el);
        const r = parseFloat(s.borderTopLeftRadius) || 0;
        const bg = s.backgroundColor;
        const filled = bg && bg !== 'transparent' && bg !== 'rgba(0, 0, 0, 0)';
        const bordered = (parseFloat(s.borderTopWidth) || 0) > 0;
        return r >= 8 && (filled || bordered);
      };
      const boxes = [...card.querySelectorAll('*')].filter(isBox);
      const set = new Set(boxes);
      for (const el of boxes) {
        if (el.classList.contains('tc-card')) continue;
        const hasBoxChild = [...el.querySelectorAll('*')].some((d) => set.has(d));
        if (!hasBoxChild) { el.style.breakInside = 'avoid'; el.style.pageBreakInside = 'avoid'; }
      }
    });
  } catch (e) { /* best-effort */ }
}

// Wait until the dc runtime has replaced every {{ }} template and the DOM size
// has stopped changing (or a hard 5s cap). Mirrors the review console's settle.
async function settleDc(page) {
  try {
    await page.evaluate(() => new Promise((resolve) => {
      const start = performance.now();
      let lastLen = -1, stable = 0;
      const tick = () => {
        const txt = document.body ? document.body.innerText : '';
        const html = document.body ? document.body.innerHTML : '';
        const hasTpl = txt.indexOf('{{') !== -1;
        if (!hasTpl && html.length === lastLen) stable++; else stable = 0;
        lastLen = html.length;
        if ((!hasTpl && stable >= 3) || performance.now() - start > 5000) { resolve(); return; }
        requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }));
  } catch (e) { /* settle best-effort */ }
}

async function renderCardPdf(browser, fullPath) {
  const page = await preparePage(browser, fullPath);
  try {
    return await page.pdf(PDF_OPTS);
  } finally {
    await page.close();
  }
}

// Return the post-render card markup for the merged, self-contained HTML bundle.
// dc cards style every element inline, so the settled `.tc-page` subtree is fully
// self-contained once the web-font link is present in the document head.
async function snapshotCardHtml(browser, fullPath) {
  const isDc = isDcPath(fullPath);
  if (!isDc) {
    // Classic: no JS needed — inline the linked CSS + per-card <style>, take body.
    const html = fs.readFileSync(fullPath, 'utf8');
    const dir = path.dirname(fullPath);
    let styles = '';
    for (const m of html.matchAll(/<link rel="stylesheet" href="([^"]+)">/g)) {
      const cssPath = path.resolve(dir, m[1]);
      if (fs.existsSync(cssPath)) styles += `<style>${fs.readFileSync(cssPath, 'utf8')}</style>`;
    }
    styles += [...html.matchAll(/<style>[\s\S]*?<\/style>/g)].map((m) => m[0]).join('\n');
    const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/);
    const dirMatch = html.match(/<html[^>]*\sdir="([^"]+)"/);
    const langMatch = html.match(/<html[^>]*\slang="([^"]+)"/);
    return {
      body: bodyMatch ? bodyMatch[1] : '',
      styles,
      dir: dirMatch ? dirMatch[1] : '',
      lang: langMatch ? langMatch[1] : '',
      fonts: false,
    };
  }
  // dc: run the runtime, then serialize the rendered card + its helmet <style>.
  const page = await preparePage(browser, fullPath);
  try {
    const snap = await page.evaluate(() => {
      const card = document.querySelector('.tc-page') || document.body;
      const styleEls = [...document.querySelectorAll('style')].map((s) => s.outerHTML).join('\n');
      return { html: card ? card.outerHTML : '', styles: styleEls };
    });
    return { body: snap.html, styles: snap.styles, dir: 'rtl', lang: 'he', fonts: true };
  } finally {
    await page.close();
  }
}

// Prefix every selector in a classic stylesheet with `scope` so its global
// element rules (h2 {}, table {}, li {} …) can't bleed onto the inline-styled dc
// cards sharing the merged bundle. @media/@supports/@layer blocks are recursed
// into; @font-face/@keyframes/@page and the like are copied verbatim.
function scopeCss(css, scope) {
  css = css.replace(/\/\*[\s\S]*?\*\//g, '');
  let i = 0;
  const n = css.length;

  function readBlockBody() { // assumes css[i] is just past the opening '{'
    let body = '', depth = 1;
    while (i < n && depth > 0) {
      const ch = css[i];
      if (ch === '{') depth++;
      else if (ch === '}') { depth--; if (depth === 0) { i++; break; } }
      body += ch; i++;
    }
    return body;
  }

  function parse(atTopOfNested) {
    let out = '';
    while (i < n) {
      let prelude = '';
      while (i < n && css[i] !== '{' && css[i] !== '}') { prelude += css[i]; i++; }
      if (i >= n) { out += prelude; break; }
      if (css[i] === '}') { i++; if (atTopOfNested) return out; else continue; }
      i++; // consume '{'
      const sel = prelude.trim();
      if (sel.startsWith('@')) {
        const at = sel.split(/[\s({]/)[0].toLowerCase();
        if (at === '@media' || at === '@supports' || at === '@layer') {
          out += `${sel}{${parse(true)}}`;
        } else {
          out += `${sel}{${readBlockBody()}}`; // @font-face, @keyframes, @page…
        }
      } else {
        const body = readBlockBody();
        const scoped = sel.split(',').map((s) => {
          s = s.trim();
          if (!s) return s;
          if (s === 'html' || s === 'body' || s === ':root') return scope;
          return `${scope} ${s}`;
        }).join(', ');
        out += `${scoped}{${body}}`;
      }
    }
    return out;
  }
  return parse(false);
}

module.exports = { resolveCardFile, renderCardPdf, snapshotCardHtml, isDcPath, PDF_OPTS, DC_FONTS_LINK, scopeCss };
