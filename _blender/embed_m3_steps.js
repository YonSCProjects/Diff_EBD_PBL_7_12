/* embed_m3_steps.js — put one figure INSIDE each numbered step of the chassis-assembly card.
 *
 *   node _blender/embed_m3_steps.js [--check]
 *
 * The other cards carry a single figure above the "what to do" list, which the shared
 * embed_steps.js handles. This card is different: it runs seven steps and each one gets its own
 * picture, so the figure has to sit with the step it illustrates rather than in a stack at the
 * top where the reader would have to hold seven images in their head.
 *
 * Idempotent — a re-run strips its own blocks (marked data-m3="step") before re-inserting, and
 * matches both LF and CRLF because these files are checked out with CRLF on Windows.
 */
const fs = require('fs');
const path = require('path');

const CARD = path.join(__dirname, '..', 'Arduino_Projects', 'Project_4_Line_Following_Car',
                       'task_cards_he', 'P4_T1_M3_assemble_chassis_he.dc.html');
const CHECK = process.argv.includes('--check');
const MARK = 'data-m3="step"';

// step number -> figure + its caption
const FIGS = {
  1: { svg: 'w_p4_m3_step1',
       cap: '<strong>מדפיסים ובודקים:</strong> התבנית מודבקת על הפוליגל בנייר דבק, ופס הביקורת שעליה נמדד בסרגל — חייב לצאת בדיוק <strong>5 ס״מ</strong>.',
       alt: 'לוח פוליגל על שולחן העבודה ועליו תבנית נייר מודבקת בארבע פינות בנייר דבק. סרגל שקוף מונח לאורך פס הביקורת המודפס, ולידו גליל נייר דבק.' },
  2: { svg: 'w_p4_m3_step2',
       cap: '<strong>חותכים על הקו:</strong> כמה העברות קלות ולא אחת חזקה. שני קווי הרוחב חוצים את תעלות הפוליגל והם הקשים יותר — וגם ארבע פינות האלכסון נחתכות.',
       alt: 'סכין חיתוך נעה לאורך קו המתאר השחור שעל התבנית. בתוך לוח הפוליגל נראות התעלות הפנימיות שקווי הרוחב חייבים לחצות.' },
  3: { svg: 'w_p4_m3_step3',
       cap: '<strong>מנקבים וקודחים:</strong> בחריצי האזיקונים שתי דקירות סכין לכל חריץ, ובסימוני הקדיחה קדח של <strong>3.5 מ״מ</strong>.',
       alt: 'הלוח החתוך על השולחן, מקדחה נטענת קודחת חור בסימון הקדיחה, ובצד נראים חריצי האזיקונים שנפתחו בדקירות סכין.' },
  4: { svg: 'w_p4_m3_step4',
       cap: '<strong>מדביקים בדבק חם:</strong> פס דבק חם לאורך גוף המנוע, מצמידים אותו לפינה שלו ולוחצים <strong>30 שניות</strong>. ככה ארבע פעמים.',
       alt: 'הלוח על השולחן ושלושה מנועים כבר מודבקים אליו. המנוע הרביעי מוחזק מעל פינתו ומתחתיו פס דבק חם, ואקדח הדבק החם מונח בצד.' },
  5: { svg: 'w_p4_m3_step5',
       cap: '<strong>גלגלים על הצירים:</strong> דוחפים כל גלגל עד הסוף — הגלגלים בחוץ, צמודים ללוח.',
       alt: 'השלדה עם ארבעת המנועים המודבקים. שלושה גלגלים כבר על הצירים והרביעי נדחף אל הציר שלו מבחוץ.' },
  6: { svg: 'w_p4_m3_step6',
       cap: '<strong>שלושה חלקים על הלוח:</strong> בית הסוללות בשני אזיקונים דרך החריצים והמתג פונה אחורה, ה-<span dir="ltr">L298N</span> מוברג, וה-<span dir="ltr">Uno</span> על סקוץ׳ באזור הירוק של התבנית.',
       alt: 'השלדה המתגלגלת ועליה בית הסוללות מהודק בשני אזיקונים, בקר המנועים מוברג ללוח ולוח הארדואינו מודבק בסקוץ׳ באזור המסומן.' },
  7: { svg: 'w_p4_m3_step7',
       cap: '<strong>שני חיישני הקו בחזית:</strong> לכל חיישן בורג <span dir="ltr">M3x20</span> עם <strong>שני אומים כמרווח</strong>, והחיישן מביט ברצפה.',
       alt: 'חזית הלוח מקרוב: חיישן קו מוברג מתחתיו בבורג שעליו שני אומים המשמשים מרווח, כך שהחיישן מרוחק מעט מהלוח ופונה כלפי מטה.' },
};

function figure(f) {
  return `
        <div ${MARK} style="flex:0 0 100%; margin:14px 0 2px; border:1px solid oklch(0.93 0.006 85); border-radius:12px; overflow:hidden; background:oklch(0.985 0.004 85);">
          <div dir="ltr" style="padding:14px 14px 8px; display:flex; justify-content:center;">
            <img src="./assets/${f.svg}.svg" alt="${f.alt}" style="width:100%; max-width:100%; height:auto;" />
          </div>
          <div style="padding:9px 14px; background:#fff; border-top:1px solid oklch(0.94 0.006 85); font-size:13px; line-height:1.55; color:oklch(0.5 0.012 260);">${f.cap}</div>
        </div>`;
}

let html = fs.readFileSync(CARD, 'utf8');
html = html.replace(new RegExp(`\\s*<div ${MARK}[\\s\\S]*?\\r?\\n        </div>`, 'g'), '');

let added = 0;
for (const [n, f] of Object.entries(FIGS)) {
  // find this step's numbered badge, then the end of the <p> that follows it
  const badge = new RegExp(`justify-content:center;">${n}</span>`);
  const m = html.match(badge);
  if (!m) { console.warn('step', n, '- no badge found'); continue; }
  const after = html.indexOf('</p>', m.index);
  if (after < 0) { console.warn('step', n, '- no paragraph after the badge'); continue; }
  const at = after + 4;
  html = html.slice(0, at) + figure(f) + html.slice(at);
  // The step is a flex row, so a figure appended after the <p> becomes a fourth flex item and
  // lays out BESIDE the text — which is why it could never reach even its declared width, and
  // why review kept asking for it "below the text and larger". Letting the row wrap lets the
  // 100%-basis figure drop onto its own line at the full width of the step card.
  const rowStart = html.lastIndexOf('<div style="display:flex; gap:13px; align-items:flex-start;', m.index);
  if (rowStart >= 0) {
    const head = html.slice(rowStart, rowStart + 120);
    if (!head.includes('flex-wrap')) {
      html = html.slice(0, rowStart) + head.replace('display:flex; gap:13px;', 'display:flex; flex-wrap:wrap; gap:13px;')
           + html.slice(rowStart + 120);
    }
  }
  added++;
}

if (!CHECK) fs.writeFileSync(CARD, html);
console.log(`${CHECK ? 'would insert' : 'inserted'} ${added} step figures`);
