// embed_figures.js — insert dc-card figure blocks (same markup P4 uses) after a card's
// wiring <pre> box. Usage: node embed_figures.js <plan.json>
// plan = [{ card, pre: 1, figures: [{ file, title, caption, alt, width? }] }]
// Idempotent: a card already containing the figure's file name is skipped.
const fs = require('fs');
const path = require('path');

const plan = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const planDir = path.dirname(path.resolve(process.argv[2]));
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

function block(f) {
  return `
      <div style="border:1px solid oklch(0.93 0.006 85); border-radius:14px; overflow:hidden; background:oklch(0.985 0.004 85); margin-bottom:30px;">
        <div dir="ltr" style="padding:22px 18px 14px; display:flex; justify-content:center;">
          <img src="./assets/${f.file}" alt="${esc(f.alt || f.caption)}" style="width:${f.width || 640}px; max-width:100%; height:auto;" />
        </div>
        <div style="padding:11px 16px; background:#fff; border-top:1px solid oklch(0.94 0.006 85); font-size:13.5px; line-height:1.6; color:oklch(0.5 0.012 260);"><strong>${f.title}</strong> ${f.caption}</div>
      </div>
`;
}

for (const item of plan) {
  const file = path.resolve(planDir, item.card);
  let html = fs.readFileSync(file, 'utf8');
  const todo = item.figures.filter((f) => !html.includes(f.file));
  if (!todo.length) { console.log('skip (present):', path.basename(file)); continue; }
  // locate the n-th <pre> and the </div> that closes its box
  const re = /<pre[\s\S]*?<\/pre>/g; let m, n = 0, preEnd = -1;
  while ((m = re.exec(html))) { n++; if (n === (item.pre || 1)) { preEnd = m.index + m[0].length; break; } }
  if (preEnd < 0) throw new Error('no <pre> #' + item.pre + ' in ' + file);
  const closeIdx = html.indexOf('</div>', preEnd);
  if (closeIdx < 0) throw new Error('no closing div after pre in ' + file);
  const at = closeIdx + '</div>'.length;
  html = html.slice(0, at) + '\n' + todo.map(block).join('') + html.slice(at);
  fs.writeFileSync(file, html);
  console.log('embedded', todo.length, 'figure(s) in', path.basename(file));
}
