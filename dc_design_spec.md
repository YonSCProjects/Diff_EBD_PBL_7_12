# Claude-Design (.dc.html) Card Design Spec — Hebrew Arduino Task Cards

> **Companion log:** when AUTHORING NEW cards (P5–P8) — where the Hebrew is being written,
> not converted — also read **`Card_Editing_Preferences_Log.md`** (maintained by the
> `/learn-changes` skill from Yon's review-console edits). FIRM/CONFIRMED rules there are
> applied silently; TENTATIVE ones are "leanings". For CONVERSION of existing reviewed text,
> the Prime Directive below still wins: words are final.

Derived verbatim from the 8 exemplar cards:

1. `Arduino_Projects/Project_2_Reaction_Time_Game/task_cards_he/P2_T1_M1_wire_led_and_button_he.dc.html`
2. `Arduino_Projects/Project_2_Reaction_Time_Game/task_cards_he/P2_T2_M1_startup_he.dc.html`
3. `Arduino_Projects/Project_2_Reaction_Time_Game/task_cards_he/P2_T2_M3_pick_difficulty_and_modify_he.dc.html`
4. `Arduino_Projects/Project_2_Reaction_Time_Game/task_cards_he/P2_T1_M6_record_fastest_time_he.dc.html`
5. `Arduino_Projects/Project_2_Reaction_Time_Game/task_cards_he/P2_T3_project_planner_he.dc.html`
6. `Arduino_Projects/Project_1_Light_Signals/task_cards_he/T2_M2b_wire_third_led_he.dc.html`
7. `Arduino_Projects/Project_1_Light_Signals/task_cards_he/T1_M1_setup_workspace_he.dc.html`
8. `Arduino_Projects/Project_1_Light_Signals/task_cards_he/T3_project_planner_he.dc.html`

(plus one component — the dark serial-monitor/code panel — taken verbatim from sibling card
`P2_T1_M2_upload_wait_flash_measure_he.dc.html`, which is part of the same design system).

---

## 0. THE PRIME DIRECTIVE — words are FINAL

**The words of the target cards are FINAL. Authors reflow existing text into these
components but NEVER reword, shorten, merge, split, or "improve" sentences.**
Every Hebrew sentence, every `<strong>` emphasis choice, every pin number, every
resistor color sequence (e.g. `אדום · אדום · חום`) is authored content that has
passed pedagogical + Hebrew review. Your job is purely typographic: pour the
existing sentences into the exact component markup below. If a sentence doesn't
fit a component, pick a different component — do not touch the sentence.

---

## 1. Document skeleton

Every card is a single self-contained `.dc.html` file. Exact skeleton (verbatim
from `P2_T1_M1_wire_led_and_button_he.dc.html`):

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; }
  body { margin: 0; }
  @media print {
    .tc-page { background: #fff !important; padding: 0 !important; }
    .tc-card { box-shadow: none !important; border: 1px solid #e6e2d8 !important; }
  }
</style>
</helmet>
```

Then the page/card shells (verbatim — these two lines are IDENTICAL in all 8 cards):

```html
<div class="tc-page" dir="rtl" style="font-family:'Rubik',sans-serif; background:oklch(0.972 0.008 85); min-height:100vh; padding:40px 20px; display:flex; justify-content:center; color:oklch(0.28 0.012 260); -webkit-font-smoothing:antialiased;">
  <div class="tc-card" style="width:100%; max-width:760px; background:#fff; border-radius:22px; box-shadow:0 1px 2px rgba(40,35,20,0.04), 0 18px 50px -28px rgba(40,35,20,0.30); overflow:hidden;">

    <!-- header band here (section 2) -->

    <div style="padding:30px 34px 34px;">
      <!-- body content here (section 3) -->
    </div>

  </div>
</div>
```

Closing structure (verbatim):

```html
</x-dc>
<script type="text/x-dc" data-dc-script data-props="{&quot;$preview&quot;:{&quot;width&quot;:800,&quot;height&quot;:1180}}">
class Component extends DCLogic {
  state = { checked: {} };
  KEY = 'tc_p2t1m1_checks';
  componentDidMount() {
    try { const s = localStorage.getItem(this.KEY); if (s) this.setState({ checked: JSON.parse(s) }); } catch (e) {}
  }
  toggle(i) {
    this.setState(s => {
      const n = { ...s.checked, [i]: !s.checked[i] };
      try { localStorage.setItem(this.KEY, JSON.stringify(n)); } catch (e) {}
      return { checked: n };
    });
  }
  renderVals() {
    const v = {};
    for (let i = 1; i <= 14; i++) { v['check' + i] = !!this.state.checked[i]; v['toggle' + i] = () => this.toggle(i); }
    return v;
  }
}
</script>
</body>
</html>
```

Skeleton rules:

- `<script src="./support.js"></script>` in `<head>` — `support.js` must live in the
  same folder as the card (it already exists in P1 and P2 `task_cards_he/`).
- Content lives inside `<x-dc>…</x-dc>`; fonts/print CSS go in `<helmet>`.
- The logic script is `<script type="text/x-dc" data-dc-script data-props="…">`
  with the `$preview` sizing convention: always exactly
  `data-props="{&quot;$preview&quot;:{&quot;width&quot;:800,&quot;height&quot;:1180}}"` (HTML-escaped JSON, width 800, height 1180 — do not change).
- Template bindings in markup use `{{ name }}`; conditional rendering uses
  `<sc-if value="{{ boolName }}" hint-placeholder-val="{{ false }}">…</sc-if>`;
  hover/focus states use the DC attributes `style-hover="…"` / `style-focus="…"`.
- Change ONLY the `KEY` (localStorage key, section 7) per card. Keep the
  `renderVals()` loop bound at `14` (it over-provisions toggles; harmless).
  (The oldest card, `T1_M1`, inlines the key string and loops to 10 — the P2
  pattern above with a `KEY` field and bound 14 is the canonical one for new cards.)
- Font-link note: `T1_M1` loads only `JetBrains+Mono:wght@500`; all newer cards
  load `400;500;700`. Use `400;500;700` in new cards.

### 1.1 DCLogic extensions for interactive cards

**Choice cards + free-text fields** (verbatim from `P2_T2_M3`):

```js
class Component extends DCLogic {
  state = { checked: {}, diff: null, fa: '', fb: '', fc: '', understanding: '' };
  KEY = 'tc_p2t2m3_checks';
  DKEY = 'tc_p2t2m3_diff';
  FKEY = 'tc_p2t2m3_fields';
  componentDidMount() {
    try {
      const s = localStorage.getItem(this.KEY); if (s) this.setState({ checked: JSON.parse(s) });
      const d = localStorage.getItem(this.DKEY); if (d) this.setState({ diff: d });
      const f = localStorage.getItem(this.FKEY); if (f) { const o = JSON.parse(f); this.setState({ fa: o.fa || '', fb: o.fb || '', fc: o.fc || '', understanding: o.understanding || '' }); }
    } catch (e) {}
  }
  toggle(i) {
    this.setState(s => {
      const n = { ...s.checked, [i]: !s.checked[i] };
      try { localStorage.setItem(this.KEY, JSON.stringify(n)); } catch (e) {}
      return { checked: n };
    });
  }
  pickDiff(d) {
    try { localStorage.setItem(this.DKEY, d); } catch (e) {}
    this.setState({ diff: d });
  }
  setField(k, val) {
    this.setState(s => {
      const next = { fa: s.fa, fb: s.fb, fc: s.fc, understanding: s.understanding, [k]: val };
      try { localStorage.setItem(this.FKEY, JSON.stringify({ fa: next.fa, fb: next.fb, fc: next.fc, understanding: next.understanding })); } catch (e) {}
      return { [k]: val };
    });
  }
  renderVals() {
    const on = (d) => this.state.diff === d;
    const SEL = 'oklch(0.55 0.13 285)';
    const OFF = 'oklch(0.9 0.006 85)';
    const SELBG = 'oklch(0.975 0.02 285)';
    const OFFBG = 'oklch(0.99 0.003 85)';
    const v = {
      pickEasy: () => this.pickDiff('easy'), pickHard: () => this.pickDiff('hard'),
      selEasy: on('easy'), selHard: on('hard'),
      borderEasy: on('easy') ? SEL : OFF, borderHard: on('hard') ? SEL : OFF,
      bgEasy: on('easy') ? SELBG : OFFBG, bgHard: on('hard') ? SELBG : OFFBG,
      fa: this.state.fa, fb: this.state.fb, fc: this.state.fc, understanding: this.state.understanding,
      onA: (e) => this.setField('fa', e.target.value),
      onB: (e) => this.setField('fb', e.target.value),
      onC: (e) => this.setField('fc', e.target.value),
      onU: (e) => this.setField('understanding', e.target.value)
    };
    for (let i = 1; i <= 14; i++) { v['check' + i] = !!this.state.checked[i]; v['toggle' + i] = () => this.toggle(i); }
    return v;
  }
}
```

**Planner with numbered fields f1..fN** (from `P2_T3` / `T3`): same pattern, with

```js
for (let i = 1; i <= 6; i++) { v['f' + i] = this.state['f' + i]; v['on' + i] = (e) => this.setField('f' + i, e.target.value); }
```

and a `VKEY` for the chosen variant plus selected-tag colors:

```js
tag1: on('1') ? 'oklch(0.55 0.13 285)' : 'oklch(0.7 0.04 285)',
tag2: on('2') ? 'oklch(0.55 0.13 285)' : 'oklch(0.7 0.04 285)'
```

**Saveable numeric input** (from `P2_T1_M6`):

```js
onBest(e) {
  const v = e.target.value.replace(/[^0-9]/g, '').slice(0, 5);
  try { if (v) localStorage.setItem(this.BKEY, v); else localStorage.removeItem(this.BKEY); } catch (err) {}
  this.setState({ best: v, saved: !!v });
}
```

---

## 2. Header band anatomy

The header is the first child of `.tc-card`. Three variants (V1/V2 share one
skeleton; the planner V3 and final-milestone are distinct).

### 2.1 Track-1 / Track-2 header (V1 / V2) — verbatim from `P2_T1_M1`

```html
<div style="position:relative; background:oklch(0.45 0.11 248); color:#fff; padding:30px 34px 26px;">
  <div style="display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap;">
    <div style="display:inline-flex; align-items:center; gap:9px; background:rgba(255,255,255,0.14); border:1px solid rgba(255,255,255,0.22); padding:7px 14px; border-radius:999px; font-size:13.5px; font-weight:600;">
      <span style="width:8px; height:8px; border-radius:50%; background:oklch(0.78 0.16 90); display:inline-block;"></span>
      פרויקט 2 · משחק זמן תגובה
    </div>
    <div style="font-size:13px; font-weight:600; color:rgba(255,255,255,0.78);">מסלול 1 · כרטיסייה V1</div>
  </div>

  <h1 style="margin:18px 0 0; font-size:30px; line-height:1.22; font-weight:700; letter-spacing:-0.01em; max-width:30ch;">מחווטים את הלד והכפתור</h1>
  <p style="margin:12px 0 0; font-size:16px; line-height:1.55; color:rgba(255,255,255,0.85); max-width:56ch;">בונים מחדש את מעגל הבסיס מפרויקט 1 — לד וכפתור. <strong style="color:#fff;">זה הבסיס של משחק זמן התגובה</strong>: הלד נדלק, ואתם לוחצים מהר ככל האפשר.</p>

  <div style="margin-top:22px;">
    <div style="display:flex; align-items:center; justify-content:space-between; font-size:13px; font-weight:600; color:rgba(255,255,255,0.85); margin-bottom:8px;">
      <span>שלב 1 מתוך 6</span><span>17%</span>
    </div>
    <div style="height:8px; border-radius:999px; background:rgba(255,255,255,0.18); overflow:hidden;">
      <div style="height:100%; width:16.6%; border-radius:999px; background:oklch(0.78 0.16 90);"></div>
    </div>
  </div>
</div>
```

Anatomy, top to bottom:

| Part | Rules |
|---|---|
| **Project chip** (right in RTL) | pill `border-radius:999px`, translucent white `rgba(255,255,255,0.14)` bg + `rgba(255,255,255,0.22)` border, 13.5px/600, with an 8px yellow dot `oklch(0.78 0.16 90)`. Text: `פרויקט N · שם הפרויקט`. |
| **Track label** (left in RTL) | plain text 13px/600 `rgba(255,255,255,0.78)`. Track 1: `מסלול 1 · כרטיסייה V1`. Track 2: `מסלול 2 · כרטיסייה V2`. Choice-point card: `מסלול 2 · נקודת בחירה`. P1 creators-track: `מסלול יוצרים · אפשרות ב (רדיפה)`. P1 first card (before tracks split): just `כרטיסייה V1`. |
| **h1** | 30px/700, `line-height:1.22`, `letter-spacing:-0.01em`, `max-width:30ch`, `margin:18px 0 0`. White. |
| **Subtitle/lede** (optional — `T1_M1` omits it) | 16px, `line-height:1.55`, `rgba(255,255,255,0.85)`, `max-width:56ch` or `58ch`, `margin:12px 0 0`. Key phrase bolded with `<strong style="color:#fff;">…</strong>`. |
| **Progress row + bar** | wrapper `margin-top:22px`. Row: 13px/600 `rgba(255,255,255,0.85)`, `שלב N מתוך M` on one side, percent on the other, `margin-bottom:8px`. Bar: track 8px tall, `border-radius:999px`, bg `rgba(255,255,255,0.18)`, `overflow:hidden`; fill 100% height, `border-radius:999px`, **yellow `oklch(0.78 0.16 90)`**, `width:` = N/M as % (e.g. 16.6%, 20%, 60%, 12.5%, 100%). |

The V1 and V2 headers are structurally identical — only the track-label text
changes. Cards without linear progress (planner, wiring side-quests like
`T2_M2b`) omit the progress block entirely.

### 2.2 Final-milestone header — verbatim from `P2_T1_M6`

Gradient background + solid-yellow star chip; progress at 100%:

```html
<div style="position:relative; background:linear-gradient(135deg, oklch(0.45 0.11 248), oklch(0.42 0.13 285)); color:#fff; padding:30px 34px 26px;">
  <div style="display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap;">
    <div style="display:inline-flex; align-items:center; gap:9px; background:oklch(0.78 0.16 90); color:oklch(0.3 0.08 80); border:1px solid rgba(255,255,255,0.3); padding:7px 14px; border-radius:999px; font-size:13.5px; font-weight:700;">
      ⭐ השלב האחרון · פרויקט 2
    </div>
    <div style="font-size:13px; font-weight:600; color:rgba(255,255,255,0.78);">מסלול 1 · כרטיסייה V1</div>
  </div>
  ...h1 / lede (lede color rgba(255,255,255,0.88))...
  ...progress: <span>שלב 6 מתוך 6</span><span>100%</span> and fill width:100%...
</div>
```

### 2.3 Planner header (V3) — verbatim from `P2_T3`

Gradient runs purple→blue (reverse of final-milestone), chip alpha slightly
higher, track label `מתכנן פרויקט · V3`, **no progress block**:

```html
<div style="position:relative; background:linear-gradient(135deg, oklch(0.42 0.13 285), oklch(0.45 0.11 248)); color:#fff; padding:30px 34px 26px;">
  <div style="display:flex; align-items:center; justify-content:space-between; gap:14px; flex-wrap:wrap;">
    <div style="display:inline-flex; align-items:center; gap:9px; background:rgba(255,255,255,0.16); border:1px solid rgba(255,255,255,0.24); padding:7px 14px; border-radius:999px; font-size:13.5px; font-weight:600;">
      <span style="width:8px; height:8px; border-radius:50%; background:oklch(0.78 0.16 90); display:inline-block;"></span>
      פרויקט 2 · משחק זמן תגובה
    </div>
    <div style="font-size:13px; font-weight:600; color:rgba(255,255,255,0.78);">מתכנן פרויקט · V3</div>
  </div>

  <h1 style="margin:18px 0 0; font-size:30px; line-height:1.22; font-weight:700; letter-spacing:-0.01em; max-width:30ch;">מעצבים את משחק זמן התגובה שלכם</h1>
  <p style="margin:12px 0 0; font-size:16px; line-height:1.55; color:rgba(255,255,255,0.88); max-width:58ch;">מעצבים וריאציה משלכם — <strong style="color:#fff;">שני שחקנים זה מול זה, או משחק ניקוד על פני חמישה סבבים</strong> — ובונים אותה מאפס.</p>
</div>
```

---

## 3. Content components (body, inside `<div style="padding:30px 34px 34px;">`)

### 3.1 Intro line (first paragraph of body on step cards)

```html
<p style="margin:0 0 22px; font-size:16.5px; line-height:1.6; color:oklch(0.46 0.012 260);">עוברים על השלבים לפי הסדר. אפשר לסמן ✓ לכל שלב שמסיימים.</p>
```

(bottom margin varies 22–26px between cards; 22px is the common value.)

### 3.2 Section header — icon chip + h2

```html
<div style="display:flex; align-items:center; gap:12px; margin:0 0 16px;">
  <span style="display:inline-flex; align-items:center; justify-content:center; width:30px; height:30px; border-radius:9px; background:oklch(0.94 0.03 248); color:oklch(0.45 0.11 248); font-size:16px;">📋</span>
  <h2 style="margin:0; font-size:18px; font-weight:700; color:oklch(0.32 0.02 260);">מה עושים</h2>
</div>
```

- Bottom margin: `16px` before step lists, `14px` before diagrams/prompts, `8px`
  when a helper sentence follows, `12px` before prose.
- Icon-chip color coding by section role (30×30, radius 9):
  - **Blue** (default / doing / wiring / testing): bg `oklch(0.94 0.03 248)`, color `oklch(0.45 0.11 248)` — icons `📋 🔌 ✏️ 📝 🔍 📁 ⚙️ 💡`
  - **Purple** (Claude-Code / choices): bg `oklch(0.95 0.05 285)`, color `oklch(0.5 0.13 285)` — icons `💻 🔀`
  - **Yellow** (goal / show): bg `oklch(0.95 0.06 90)` color `oklch(0.5 0.12 75)` (🎯) or bg `oklch(0.96 0.06 90)` color `oklch(0.5 0.12 75)` (🎬)
- Optional trailing annotation inside the flex row (from `P2_T1_M2`):
  `<span style="font-size:13px; color:oklch(0.6 0.012 260); font-weight:500;">— לקריאה בלבד</span>`
- Optional helper sentence directly under the header:
  `<p style="margin:0 0 16px; font-size:14.5px; line-height:1.5; color:oklch(0.55 0.012 260);">…</p>`

### 3.3 Numbered step card with checkbox — THE core component

Steps live in a column wrapper:

```html
<div style="display:flex; flex-direction:column; gap:12px; margin-bottom:30px;">
  ...step cards...
</div>
```

Single step, verbatim (step 2 of `P2_T1_M1`). Three flex children: (1) the
checkbox bound to `toggleN`/`checkN`, (2) the number circle, (3) the text:

```html
<div style="display:flex; gap:13px; align-items:flex-start; background:oklch(0.985 0.004 85); border:1px solid oklch(0.92 0.006 85); border-radius:14px; padding:15px 16px;">
  <span onClick="{{ toggle2 }}" style="position:relative; flex:none; width:26px; height:26px; border-radius:7px; border:2px solid oklch(0.82 0.02 150); background:#fff; cursor:pointer; display:flex; align-items:center; justify-content:center; margin-top:2px;" style-hover="border-color:oklch(0.62 0.14 150)"><sc-if value="{{ check2 }}" hint-placeholder-val="{{ false }}"><span style="position:absolute; inset:-2px; border-radius:7px; background:oklch(0.62 0.14 150); display:flex; align-items:center; justify-content:center; color:#fff; font-size:16px; font-weight:800;">✓</span></sc-if></span>
  <span style="flex:none; width:30px; height:30px; border-radius:50%; background:oklch(0.45 0.11 248); color:#fff; font-weight:700; font-size:15px; display:flex; align-items:center; justify-content:center;">2</span>
  <p style="margin:0; font-size:16px; line-height:1.55; padding-top:3px;">מכניסים לד לברדבורד כך ש<strong>שתי הרגליים בטורים שונים</strong>. הרגל הארוכה (+), הקצרה (−).</p>
</div>
```

Rules:

- The `N` in `{{ toggleN }}` / `{{ checkN }}` and the visible circled number are
  independent — `{{ toggleN }}` indexes are unique across the WHOLE card (1..k in
  document order), while the visible number restarts per section (see `P2_T3`
  where step "1" of שלב 5 binds `toggle2`).
- Checkbox: 26×26, radius 7, border `2px solid oklch(0.82 0.02 150)`, hover
  border `oklch(0.62 0.14 150)`; checked overlay fills `inset:-2px` with green
  `oklch(0.62 0.14 150)` and a white 16px/800 `✓`. `T1_M1` additionally carries
  `user-select:none` and `title="סמן שסיימת"` — both are fine to include.
- Number circle: 30×30 filled blue `oklch(0.45 0.11 248)`, white 15px/700.
- Step text: 16px `line-height:1.55` `padding-top:3px`; emphasis via `<strong>`.
- **Two-paragraph step** (main line + small sub-hint), wrap text in a div:

```html
<div style="padding-top:3px;">
  <p style="margin:0; font-size:16px; line-height:1.55;">פותחים את תיקיית פרויקט 2 ויוצרים בתוכה תיקייה חדשה בשם <code dir="ltr" style="font-family:'JetBrains Mono',monospace; font-size:13px; background:oklch(0.96 0.01 248); color:oklch(0.42 0.1 248); border-radius:6px; padding:2px 7px; display:inline-block;">Project_2_Reaction_Time_Game</code></p>
  <p style="margin:6px 0 0; font-size:13.5px; line-height:1.5; color:oklch(0.55 0.012 260);">Google Drive → My Drive → Arduino_Projects → התיקייה עם הכינוי שלכם. פותחים בה את קלוד קוד יחד עם המורה.</p>
</div>
```

  When a step embeds a full-width illustration below its text (as `T1_M1` does),
  use `<div style="flex:1; min-width:0; padding-top:3px;">` and give the leading
  `<p>` `margin:0 0 13px`.
- **Checkbox-only step** (no number circle) — used for standalone confirmations
  (`P2_T3` build check): drop the number `<span>`, text at 15.5px.

#### 3.3.a Step-card WARNING variant (orange) — verbatim from `P2_T1_M1` step 6

The step everyone gets wrong is tinted orange: card bg/border and number-circle
change; checkbox border shifts to a warm tone (hover stays green):

```html
<div style="display:flex; gap:13px; align-items:flex-start; background:oklch(0.95 0.04 35); border:1px solid oklch(0.85 0.07 35); border-radius:14px; padding:15px 16px;">
  <span onClick="{{ toggle6 }}" style="position:relative; flex:none; width:26px; height:26px; border-radius:7px; border:2px solid oklch(0.78 0.08 35); background:#fff; cursor:pointer; display:flex; align-items:center; justify-content:center; margin-top:2px;" style-hover="border-color:oklch(0.62 0.14 150)"><sc-if value="{{ check6 }}" hint-placeholder-val="{{ false }}"><span style="position:absolute; inset:-2px; border-radius:7px; background:oklch(0.62 0.14 150); display:flex; align-items:center; justify-content:center; color:#fff; font-size:16px; font-weight:800;">✓</span></sc-if></span>
  <span style="flex:none; width:30px; height:30px; border-radius:50%; background:oklch(0.58 0.16 35); color:#fff; font-weight:700; font-size:15px; display:flex; align-items:center; justify-content:center;">6</span>
  <p style="margin:0; font-size:16px; line-height:1.55; padding-top:3px;">מרגל B מחברים <strong>גם</strong> דרך נגד <strong>10 קΩ</strong> (חום · שחור · כתום) ל-<strong>GND</strong> — זהו נגד ההורדה.</p>
</div>
```

There is also a **purple step variant** ("call the teacher" step, `T1_M1` step 5):
card `background:oklch(0.97 0.03 300); border:1px solid oklch(0.9 0.04 300)`,
checkbox border `oklch(0.78 0.05 300)`, number circle `oklch(0.52 0.12 300)`.

### 3.4 Warning / callout box (⚠️ orange) — verbatim from `P2_T1_M1`

Placed near the top of the body, BEFORE the diagram/steps. Note the heavier
`1.5px` border vs. normal cards:

```html
<div style="display:flex; gap:14px; align-items:flex-start; background:oklch(0.95 0.05 35); border:1.5px solid oklch(0.78 0.12 35); border-radius:16px; padding:18px 20px; margin-bottom:28px;">
  <span style="flex:none; font-size:24px; line-height:1;">⚠️</span>
  <div>
    <div style="font-weight:700; font-size:15.5px; margin-bottom:5px; color:oklch(0.48 0.15 32);">הטעות הנפוצה ביותר</div>
    <p style="margin:0; font-size:15.5px; line-height:1.6; color:oklch(0.42 0.08 32);">נגד ההורדה של 10 קΩ חייב להיות בין <strong>רגל 2 ל-GND</strong> — <strong>לא</strong> בין 5 V ל-GND. אם שמים אותו בין 5 V ל-GND, לחיצה על הכפתור יוצרת קצר ומאפסת את הארדואינו. עוקבים באצבע: מרגל 2 ל-GND? ✓</p>
  </div>
</div>
```

### 3.5 Skip-notice — verbatim from `T2_M2b`

Same ⚠️ skeleton as 3.4 with slightly softer border chroma
(`1.5px solid oklch(0.78 0.1 35)`), title text tells who may skip:

```html
<div style="display:flex; gap:14px; align-items:flex-start; background:oklch(0.95 0.05 35); border:1.5px solid oklch(0.78 0.1 35); border-radius:16px; padding:18px 20px; margin-bottom:28px;">
  <span style="flex:none; font-size:24px; line-height:1;">⚠️</span>
  <div>
    <div style="font-weight:700; font-size:15.5px; margin-bottom:5px; color:oklch(0.48 0.13 32);">אפשר לדלג אם בחרתם אפשרות א או ג</div>
    <p style="margin:0; font-size:15.5px; line-height:1.6; color:oklch(0.42 0.07 32);">לסירוגין (א) צריכה רק שני לדים, ונשימה (ג) רק לד אחד — החיווט שלכם כבר מוכן. עוברים ישר לשלב 3.</p>
  </div>
</div>
```

### 3.6 Purple info note (🧠 / 💡) — track-2 "you modify code" & planner intro

Verbatim from `P2_T2_M1` (with title):

```html
<div style="display:flex; gap:14px; align-items:flex-start; background:oklch(0.96 0.04 285); border:1px solid oklch(0.88 0.05 285); border-radius:16px; padding:18px 20px; margin-bottom:28px;">
  <span style="flex:none; font-size:22px; line-height:1;">🧠</span>
  <div>
    <div style="font-weight:700; font-size:15.5px; margin-bottom:4px; color:oklch(0.45 0.12 285);">במסלול הזה אתם משנים קוד בעצמכם</div>
    <p style="margin:0; font-size:15px; line-height:1.6; color:oklch(0.42 0.06 285);">מתארים מה אתם רוצים, שואלים את קלוד קוד, קוראים את התשובה, עורכים, ומעלים מחדש. זו לא העתקה — אתם מבינים מה שיניתם. את זה תתרגלו בשלב 3.</p>
  </div>
</div>
```

Titleless planner variant (verbatim from `P2_T3`, `padding:16px 20px`):

```html
<div style="display:flex; gap:14px; align-items:flex-start; background:oklch(0.96 0.04 285); border:1px solid oklch(0.88 0.05 285); border-radius:16px; padding:16px 20px; margin-bottom:28px;">
  <span style="flex:none; font-size:22px; line-height:1;">💡</span>
  <p style="margin:0; font-size:15px; line-height:1.6; color:oklch(0.42 0.06 285);">ממלאים את המתכנן, בונים, ומציגים. הכול נשמר במחשב הזה — אפשר לחזור ולערוך בכל רגע.</p>
</div>
```

### 3.7 "מה רואים אם הכול תקין" expected box (👀 yellow) — verbatim

Comes after the steps, first of the closing trio. Always icon 👀, yellow family:

```html
<div style="display:flex; gap:14px; align-items:flex-start; background:oklch(0.96 0.05 90); border:1px solid oklch(0.88 0.07 90); border-radius:16px; padding:18px 20px; margin-bottom:14px;">
  <span style="flex:none; font-size:22px; line-height:1;">👀</span>
  <div>
    <div style="font-weight:700; font-size:15.5px; margin-bottom:4px; color:oklch(0.42 0.07 75);">מה רואים אם הכול תקין</div>
    <p style="margin:0 0 6px; font-size:16px; line-height:1.55; color:oklch(0.4 0.03 75);">הלד מחובר לרגל 9 דרך הנגד, והכפתור יושב לרוחב החריץ המרכזי — צד אחד ל-5 V, השני לרגל 2 ודרך נגד ההורדה ל-GND.</p>
    <p style="margin:0; font-size:14px; line-height:1.5; color:oklch(0.5 0.03 75);"><strong>עדיין לא אמור להידלק שום דבר</strong> — עוד לא העלינו קוד. זה יקרה בשלב 2.</p>
  </div>
</div>
```

Second, smaller paragraph (14px, `oklch(0.5 0.03 75)`) is optional. If the card
uses only one paragraph, its margin is `0`. (`T2_M2b` titles this box
`מה אמורים לראות` — the title is content; keep whatever the source card says.)

### 3.8 "סיימתם כש…" done-when box (✅ green) — verbatim

Second of the closing trio. Title row + column of ✓ lines:

```html
<div style="background:oklch(0.96 0.04 150); border:1px solid oklch(0.86 0.06 150); border-radius:16px; padding:18px 20px; margin-bottom:14px;">
  <div style="display:flex; align-items:center; gap:10px; font-weight:700; font-size:15.5px; color:oklch(0.42 0.08 150); margin-bottom:12px;">
    <span style="font-size:20px;">✅</span>סיימתם כש…
  </div>
  <div style="display:flex; flex-direction:column; gap:9px;">
    <div style="display:flex; gap:10px; align-items:flex-start; font-size:15.5px; line-height:1.5; color:oklch(0.36 0.04 150);"><span style="flex:none; color:oklch(0.55 0.12 150); font-weight:700;">✓</span><span>הלד מחובר: רגל ארוכה דרך נגד 220 אוהם לרגל 9, קצרה ל-GND</span></div>
    <div style="display:flex; gap:10px; align-items:flex-start; font-size:15.5px; line-height:1.5; color:oklch(0.36 0.04 150);"><span style="flex:none; color:oklch(0.55 0.12 150); font-weight:700;">✓</span><span>המורה אישר שהחיווט נכון</span></div>
  </div>
</div>
```

Inline `<code>` inside a green ✓ line uses a translucent-white chip:
`background:rgba(255,255,255,0.65)` (see token table).

### 3.9 "תקועים?" stuck box (🪄 purple, dashed) — two variants

**Inline variant** (single flowing paragraph) — verbatim from `P2_T1_M1`:

```html
<div style="display:flex; align-items:flex-start; gap:14px; background:oklch(0.96 0.03 300); border:1px dashed oklch(0.78 0.07 300); border-radius:16px; padding:16px 20px;">
  <span style="flex:none; font-size:22px;">🪄</span>
  <div style="font-size:15.5px; line-height:1.55;"><strong style="color:oklch(0.45 0.12 300);">תקועים?</strong> &nbsp;כבר עשיתם חיווט דומה בפרויקט 1. אם הארדואינו מתאפס או נכבה — סביר מאוד שנגד ההורדה בצד הלא נכון. אם לא בטוחים, קוראים למורה.</div>
</div>
```

**Bulleted variant** (multiple tips) — verbatim from `P2_T2_M1`:

```html
<div style="background:oklch(0.96 0.03 300); border:1px dashed oklch(0.78 0.07 300); border-radius:16px; padding:16px 20px;">
  <div style="display:flex; align-items:center; gap:10px; font-weight:700; font-size:15.5px; color:oklch(0.45 0.12 300); margin-bottom:11px;">
    <span style="font-size:20px;">🪄</span>תקועים?
  </div>
  <div style="display:flex; flex-direction:column; gap:9px; font-size:15px; line-height:1.55; color:oklch(0.4 0.04 300);">
    <div style="display:flex; gap:9px;"><span style="flex:none; color:oklch(0.6 0.12 300);">●</span><span>השלב מאחד כמה צעדים. אם משהו לא ברור — מאטים ועושים צעד-צעד.</span></div>
    <div style="display:flex; gap:9px;"><span style="flex:none; color:oklch(0.6 0.12 300);">●</span><span>קוראים למורה — אפשר לקבל את הכרטיסים המפורטים של מסלול 1 לכל חלק.</span></div>
  </div>
</div>
```

The stuck box is the LAST element of a normal card (no bottom margin). When
something follows it (celebration), add `margin-bottom:22px`.

### 3.10 Celebration / final-milestone treatment — verbatim from `P2_T1_M6`

Gradient purple→blue block with big emoji, headline, paragraph, and skill chips.
Only on the final card of a track / planner:

```html
<div style="position:relative; overflow:hidden; background:linear-gradient(135deg, oklch(0.55 0.13 285), oklch(0.5 0.13 248)); color:#fff; border-radius:18px; padding:26px 26px 24px;">
  <div style="font-size:38px; line-height:1; margin-bottom:8px;">🎉</div>
  <div style="font-size:22px; font-weight:700; margin-bottom:10px;">השלמתם את פרויקט 2!</div>
  <p style="margin:0; font-size:15.5px; line-height:1.6; color:rgba(255,255,255,0.92); max-width:58ch;">בניתם משחק זמן תגובה אמיתי: לד, כפתור וזמזם, עם קוד שמודד כמה מהר אתם בעזרת <code dir="ltr" style="font-family:'JetBrains Mono',monospace; font-size:13px; background:rgba(255,255,255,0.16); border-radius:5px; padding:1px 6px;">millis()</code> ומדפיס את הזמן לצג הטורי. הזמן שלכם מופיע עכשיו על הפוסטר — בשבילכם ובשביל כל הקבוצה.</p>
  <div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:18px;">
    <span style="background:rgba(255,255,255,0.16); border:1px solid rgba(255,255,255,0.25); border-radius:999px; padding:6px 14px; font-size:13px; font-weight:600;">🔌 לד · כפתור · זמזם</span>
    <span style="background:rgba(255,255,255,0.16); border:1px solid rgba(255,255,255,0.25); border-radius:999px; padding:6px 14px; font-size:13px; font-weight:600;">⏱️ מדידת זמן עם millis()</span>
    <span style="background:rgba(255,255,255,0.16); border:1px solid rgba(255,255,255,0.25); border-radius:999px; padding:6px 14px; font-size:13px; font-weight:600;">🏆 לוח תוצאות כיתתי</span>
  </div>
</div>
```

Planner celebration (`P2_T3`, `T3`) is the same block with `padding:26px` and no
chips row.

### 3.11 Diagram frame with image + legend strip — verbatim from `P2_T1_M1`

Framed figure, image row is `dir="ltr"`, legend strip below with colored wire
swatches (16×4 rounded bars):

```html
<div style="border:1px solid oklch(0.93 0.006 85); border-radius:14px; overflow:hidden; background:oklch(0.985 0.004 85); margin-bottom:30px;">
  <div dir="ltr" style="padding:22px 18px 14px; display:flex; justify-content:center;">
    <img src="assets/w_p2_01_led_button_breadboard.svg" alt="תרשים ברדבורד — לד וכפתור עם נגד הורדה" style="width:600px; max-width:100%; height:auto;" />
  </div>
  <div dir="ltr" style="display:flex; gap:14px; justify-content:center; flex-wrap:wrap; padding:11px 12px; background:#fff; border-top:1px solid oklch(0.94 0.006 85); font-size:12px; font-weight:600;">
    <span style="display:inline-flex; align-items:center; gap:6px; color:oklch(0.5 0.15 28);"><span style="width:16px; height:4px; border-radius:2px; background:oklch(0.55 0.18 28);"></span>9 → 220Ω → לד</span>
    <span style="display:inline-flex; align-items:center; gap:6px; color:oklch(0.55 0.12 85);"><span style="width:16px; height:4px; border-radius:2px; background:oklch(0.65 0.14 85);"></span>כפתור B → רגל 2</span>
    <span style="display:inline-flex; align-items:center; gap:6px; color:oklch(0.4 0.012 260);"><span style="width:16px; height:4px; border-radius:2px; background:oklch(0.3 0.012 260);"></span>רגל 2 → 10kΩ → GND</span>
  </div>
</div>
```

Simpler legend-less variants that also occur:

- Blue-tinted frame (verbatim from `T2_M2b`; note descriptive Hebrew alt text):

```html
<div style="border:1px solid oklch(0.9 0.02 248); border-radius:14px; background:oklch(0.99 0.004 248); padding:16px; margin-bottom:30px; text-align:center;">
  <img src="../images/w4_three_leds_chasing_breadboard.svg" alt="תרשים ברדבורד: שלושה לדים במקביל — רגל 9 דרך נגד 220 אוהם ללד 1, רגל 10 דרך נגד 220 אוהם ללד 2, רגל 11 דרך נגד 220 אוהם ללד 3, כל הרגליות הקצרות ל-GND. בלי כפתור." style="display:block; max-width:100%; height:auto; margin:0 auto;">
</div>
```

- White frame + caption paragraph below (verbatim from `P2_T3`):

```html
<div style="border:1px solid oklch(0.93 0.006 85); border-radius:14px; background:#fff; padding:18px; margin-bottom:10px; text-align:center;"><img src="assets/w_p2_04_two_buttons_variant_breadboard.svg" alt="תרשים ברדבורד — שני כפתורים לשני שחקנים" style="width:600px; max-width:100%; height:auto;" /></div>
<p style="margin:0 0 20px; font-size:13.5px; line-height:1.6; color:oklch(0.55 0.012 260);"><strong>וריאציית שני השחקנים:</strong> כפתור שחקן 2 על רגל 3 עם נגד הורדה משלו ל-GND, לצד הכפתור הקיים על רגל 2. הלד והזמזם נשארים על רגליים 9 ו-8.</p>
```

- Photo frame with legend strip (from `T1_M1`, `arduino-usb-connection.png`):
  same pattern with 8×8 square swatches instead of wire bars.

### 3.12 Monospace LTR code / terminal panel — verbatim from `P2_T1_M2`

Dark panel with title bar; the whole panel is `dir="ltr"`; content in a `<pre>`
with per-line color spans. Use for serial-monitor output, terminal text, ASCII:

```html
<!-- serial monitor mock -->
<div dir="ltr" style="border-radius:14px; overflow:hidden; background:oklch(0.22 0.012 260); box-shadow:0 14px 36px -22px rgba(20,20,40,0.7); margin-bottom:30px;">
  <div style="display:flex; align-items:center; gap:8px; padding:10px 14px; background:oklch(0.27 0.015 260); border-bottom:1px solid oklch(0.32 0.015 260);">
    <span style="font-size:13px;">🔍</span>
    <span style="font-family:'JetBrains Mono',monospace; font-size:12px; color:oklch(0.7 0.01 260);">Serial Monitor — 9600 baud</span>
  </div>
  <pre style="margin:0; padding:16px 20px; font-family:'JetBrains Mono',monospace; font-size:13px; line-height:1.7; color:oklch(0.88 0.01 260); overflow-x:auto;"><span style="color:oklch(0.7 0.01 260);">Reaction Time Game — get ready…</span>
<span style="color:oklch(0.7 0.01 260);">Wait for the LED, then press FAST!</span>
<span style="color:oklch(0.82 0.13 90);">GO!</span>
<span style="color:oklch(0.78 0.15 145);">Your reaction time: 247 ms</span></pre>
</div>
```

Line-color roles: muted `oklch(0.7 0.01 260)`, highlight-yellow
`oklch(0.82 0.13 90)`, success-green `oklch(0.78 0.15 145)`, default
`oklch(0.88 0.01 260)`.

### 3.13 Inline `<code>` and `<kbd>` tokens

Every code/pin/filename/path token is JetBrains Mono and **always `dir="ltr"`**.
Variants seen in exemplars (all verbatim):

Primary (blue) inline code — file/folder names inside steps:

```html
<code dir="ltr" style="font-family:'JetBrains Mono',monospace; font-size:13px; background:oklch(0.96 0.01 248); color:oklch(0.42 0.1 248); border-radius:6px; padding:2px 7px; display:inline-block;">Project_2_Reaction_Time_Game</code>
```

Neutral (gray) inline code — menu paths, COM ports, placeholders:

```html
<span dir="ltr" style="font-family:'JetBrains Mono',monospace; font-size:13.5px; background:oklch(0.95 0.006 260); border-radius:6px; padding:2px 7px; display:inline-block;">Board → Arduino Uno</span>
```

Small neutral (in helper text / prompt lead-ins): `font-size:12.5px; background:oklch(0.95 0.006 260); border-radius:5px; padding:1px 6px;`

On tinted boxes (green done-when lines): `background:rgba(255,255,255,0.65); border-radius:5px; padding:1px 6px; font-size:13px;`
On the purple/gradient celebration: `background:rgba(255,255,255,0.16); border-radius:5px; padding:1px 6px; font-size:13px;`

Keyboard key (verbatim from `T1_M1`):

```html
<kbd style="font-family:'JetBrains Mono',monospace; font-size:13px; background:oklch(0.93 0.006 260); border:1px solid oklch(0.86 0.008 260); border-bottom-width:2px; border-radius:6px; padding:2px 7px; direction:ltr; display:inline-block;">Windows + E</kbd>
```

Bare LTR run inside Hebrew prose (no chip): `<span dir="ltr">Tools → Board = Arduino Uno</span>` or `<strong dir="ltr">USB-C</strong>`.

### 3.14 Choice cards (selectable, 2-up) — verbatim from `P2_T2_M3`

Clickable cards whose border/background/check-pill are DCLogic-bound. Wrapper:

```html
<div style="display:flex; gap:12px; margin-bottom:14px; flex-wrap:wrap;">
  <div onClick="{{ pickEasy }}" style="flex:1; min-width:200px; cursor:pointer; border:2px solid {{ borderEasy }}; background:{{ bgEasy }}; border-radius:14px; padding:16px 18px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
      <span style="font-size:18px;">🟢</span>
      <h3 style="margin:0; font-size:16px; font-weight:700; color:oklch(0.3 0.02 260);">קל</h3>
      <sc-if value="{{ selEasy }}" hint-placeholder-val="{{ false }}"><span style="margin-inline-start:auto; font-size:12.5px; font-weight:700; color:oklch(0.5 0.12 150); background:oklch(0.95 0.05 150); border-radius:999px; padding:3px 10px;">✓</span></sc-if>
    </div>
    <p style="margin:0; font-size:14.5px; line-height:1.5; color:oklch(0.45 0.012 260);">הלד נשאר דולק <strong>2 שניות</strong>. גם תגובה איטית נספרת. (זה מה שיש בקוד עכשיו.)</p>
  </div>
  <div onClick="{{ pickHard }}" style="flex:1; min-width:200px; cursor:pointer; border:2px solid {{ borderHard }}; background:{{ bgHard }}; border-radius:14px; padding:16px 18px;">
    ...same anatomy, 🔴 / קשה / selHard...
  </div>
</div>
```

Selection colors come from `renderVals()` (section 1.1): selected border
`oklch(0.55 0.13 285)`, unselected `oklch(0.9 0.006 85)`; selected bg
`oklch(0.975 0.02 285)`, unselected `oklch(0.99 0.003 85)`.

Planner flavor (`P2_T3`): `min-width:230px`, `border-radius:15px`, leading
emoji replaced by a bound-color numbered square tag
(`width:32px; height:32px; border-radius:9px; background:{{ tag1 }}; color:#fff; font-weight:800; font-size:16px;`),
check pill text `✓ נבחר` with `padding:3px 11px`.

**Non-interactive preview cards** (read-only "choices ahead", `P2_T2_M1`):

```html
<div style="background:oklch(0.97 0.025 285); border:1px solid oklch(0.9 0.04 285); border-radius:14px; padding:16px 18px;">
  <div style="font-weight:700; font-size:15.5px; color:oklch(0.42 0.1 285); margin-bottom:4px;">שלב 2 — איך המשחק נותן משוב</div>
  <p style="margin:0; font-size:15px; line-height:1.55; color:oklch(0.42 0.04 285);">שלושה לדים (מהיר/בינוני/איטי), תבנית זמזם, או הודעה עשירה בצג הטורי. בוחרים אחת.</p>
</div>
```

### 3.15 Planner field (label + hint + persisted textarea) — verbatim from `T3`

```html
<div style="background:oklch(0.985 0.004 85); border:1px solid oklch(0.92 0.006 85); border-radius:13px; padding:15px 16px;">
  <label style="display:block; font-size:14.5px; font-weight:700; color:oklch(0.34 0.012 260); margin-bottom:5px;">מה הפרויקט שלכם הולך להיות? <span style="font-weight:500; color:oklch(0.58 0.012 260);">(משפט או שניים)</span></label>
  <p style="margin:0 0 9px; font-size:12.5px; line-height:1.5; color:oklch(0.6 0.012 260);">דוגמה: "מנורת מצב רוח לשולחן שלי. שלושה לדים. הכפתור בוחר את מצב הרוח של הצבע — רגוע, אנרגטי, או ניטרלי."</p>
  <textarea value="{{ f1 }}" onInput="{{ on1 }}" rows="2" placeholder="כותבים כאן…" style="width:100%; resize:vertical; font-family:'Rubik',sans-serif; font-size:14.5px; line-height:1.5; color:oklch(0.3 0.012 260); background:#fff; border:1px solid oklch(0.88 0.006 85); border-radius:9px; padding:9px 11px; outline:none;" style-focus="border-color:oklch(0.6 0.1 248)"></textarea>
</div>
```

Fields stack in `<div style="display:flex; flex-direction:column; gap:14px; margin-bottom:30px;">`.

**Starred most-important field** (yellow) — verbatim from `T3`:

```html
<div style="background:oklch(0.96 0.04 90); border:1px solid oklch(0.88 0.06 90); border-radius:13px; padding:15px 16px;">
  <label style="display:block; font-size:14.5px; font-weight:700; color:oklch(0.42 0.08 75); margin-bottom:5px;">מה ההתנהגות? <span style="font-weight:600;">⭐ השדה הכי חשוב</span></label>
  <p style="margin:0 0 9px; font-size:12.5px; line-height:1.5; color:oklch(0.5 0.04 75);">…hint…</p>
  <textarea value="{{ f4 }}" onInput="{{ on4 }}" rows="3" placeholder="מתארים את ההתנהגות במילים שלכם…" style="width:100%; resize:vertical; font-family:'Rubik',sans-serif; font-size:14.5px; line-height:1.5; color:oklch(0.3 0.012 260); background:#fff; border:1px solid oklch(0.85 0.05 90); border-radius:9px; padding:9px 11px; outline:none;" style-focus="border-color:oklch(0.65 0.12 90)"></textarea>
</div>
```

(א)(ב)(ג) fields (`P2_T2_M3`) are the same component with purple labels
`color:oklch(0.4 0.06 285)` and 2-row textareas; a code-answer field uses
`font-family:'JetBrains Mono',monospace; font-size:13.5px; … direction:ltr;` on
the textarea (see "בדיקת הבנה" block, which wraps a title `🔎 בדיקת הבנה`
in `font-weight:700; font-size:15px; color:oklch(0.4 0.06 285)` inside a
neutral card `border-radius:14px; padding:16px 18px;`).

**Saveable numeric input row** (personal best, `P2_T1_M6`):

```html
<div dir="ltr" style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
  <input value="{{ best }}" onInput="{{ onBest }}" inputmode="numeric" placeholder="247" style="width:120px; font-family:'JetBrains Mono',monospace; font-size:22px; font-weight:700; text-align:center; color:oklch(0.4 0.09 75); background:#fff; border:2px solid oklch(0.82 0.08 90); border-radius:11px; padding:10px 8px; outline:none;" style-focus="border-color:oklch(0.65 0.14 90)" />
  <span style="font-family:'JetBrains Mono',monospace; font-size:18px; font-weight:600; color:oklch(0.5 0.06 75);">ms</span>
  <sc-if value="{{ saved }}" hint-placeholder-val="{{ false }}">
    <span style="display:inline-flex; align-items:center; gap:6px; font-size:13.5px; font-weight:600; color:oklch(0.5 0.12 150); background:oklch(0.95 0.05 150); border-radius:999px; padding:5px 12px;">✓ נשמר</span>
  </sc-if>
</div>
```

### 3.16 Prompt-template block (paste-into-Claude-Code) — verbatim from `P2_T2_M3`

Purple RTL panel; the paste placeholder is a mono span:

```html
<p style="margin:0 0 12px; font-size:15px; line-height:1.55; color:oklch(0.46 0.012 260);">מדביקים בחלון של קלוד קוד את הפנייה הזו, ובמקום <code dir="ltr" style="font-family:'JetBrains Mono',monospace; font-size:12.5px; background:oklch(0.95 0.006 260); border-radius:5px; padding:1px 6px;">[מדביקים כאן]</code> מדביקים את הקוד הנוכחי:</p>
<div dir="rtl" style="background:oklch(0.96 0.03 285); border:1px solid oklch(0.88 0.05 285); border-radius:13px; padding:16px 18px; margin-bottom:30px; font-size:15px; line-height:1.6; color:oklch(0.36 0.06 285);">
  הנה ההשהיה הנוכחית שלי. איך אפשר שהלד יישאר דולק רק 0.5 שנייה במקום 2 שניות? הנה הקוד שלי:<br><span style="font-family:'JetBrains Mono',monospace; font-size:13px; color:oklch(0.5 0.08 285);">[מדביקים כאן]</span>
</div>
```

### 3.17 Inline hint / summary strip (neutral)

Single-paragraph fact in a light card (verbatim from `P2_T2_M3`):

```html
<p style="margin:0 0 30px; font-size:14.5px; line-height:1.6; color:oklch(0.5 0.012 260); background:oklch(0.985 0.004 85); border:1px solid oklch(0.92 0.006 85); border-radius:12px; padding:13px 16px;">במשחק שלנו עוברים מ"קל" ל"קשה" — משנים את הזמן מ-2 שניות ל-0.5 שנייה. <strong>זו שורה אחת בקוד.</strong></p>
```

Plain de-emphasized footnote line (no card): `<p style="margin:0 0 30px; font-size:14px; line-height:1.55; color:oklch(0.55 0.012 260);">…</p>`

### 3.18 R-ref circled badge — DEFINED component (not present in exemplars)

The 8 exemplars never render R1/R2 reference-card markers; classic (non-.dc)
cards used circled badges. When a target card's text references a reference
card (`R1`, `R2`, `R6`…), render the token as this circled badge, consistent
with the section-icon-chip blue tokens:

```html
<span dir="ltr" style="display:inline-flex; align-items:center; justify-content:center; min-width:24px; height:24px; border-radius:999px; background:oklch(0.94 0.03 248); border:1.5px solid oklch(0.45 0.11 248); color:oklch(0.45 0.11 248); font-family:'JetBrains Mono',monospace; font-size:12.5px; font-weight:700; padding:0 6px; vertical-align:middle;">R1</span>
```

Use it inline in the sentence exactly where the source text says `R1` — the
surrounding words stay untouched. Do not invent R-refs the source doesn't have.

### 3.19 Tables

No `<table>` exists anywhere in the exemplar set — tabular facts are expressed
as done-when ✓ lists, legend strips, or step cards. Prefer those. If a target
card's FINAL text is irreducibly tabular, build it from the neutral-card tokens:
outer `border:1px solid oklch(0.92 0.006 85); border-radius:12px; overflow:hidden;`,
header row bg `oklch(0.985 0.004 85)` 14px/700 `oklch(0.34 0.012 260)`, body
cells 15px `oklch(0.4 0.012 260)`, row separators `1px solid oklch(0.93 0.006 85)`,
cell padding `9px 12px`; pin/number cells get `dir="ltr"` JetBrains Mono.

### 3.20 Micro-illustrations (optional, T1_M1 style)

`T1_M1` embeds hand-built inline mock UI (File Explorer windows, context menus,
a CSS keyboard, an inline-SVG Arduino board). These are bespoke; when needed,
follow its conventions: the whole illustration container is `dir="ltr"`,
neutral chrome colors from the token table, menus highlight the active item
with `background:oklch(0.5 0.13 248); color:#fff; font-weight:700;`, captions
back in `dir="rtl"` at 11.5px `oklch(0.55 0.012 260)`.

---

## 4. Design tokens

### 4.1 Color palette (oklch)

| Role | Token |
|---|---|
| Page background (warm paper) | `oklch(0.972 0.008 85)` |
| Card background | `#fff` |
| Body text (default) | `oklch(0.28 0.012 260)` |
| Heading text (h2) | `oklch(0.32 0.02 260)` |
| Secondary/intro text | `oklch(0.46 0.012 260)` |
| Muted text / helper | `oklch(0.55 0.012 260)`, lighter `oklch(0.6 0.012 260)` |
| **Brand blue** (header bg, number circles, section chips fg) | `oklch(0.45 0.11 248)` |
| Blue chip bg / code bg | `oklch(0.94 0.03 248)` / `oklch(0.96 0.01 248)` |
| Blue code fg | `oklch(0.42 0.1 248)` |
| Blue focus border | `oklch(0.6 0.1 248)` |
| Menu-highlight blue | `oklch(0.5 0.13 248)` |
| **Accent yellow** (progress fill, chip dot, star chip) | `oklch(0.78 0.16 90)` |
| Yellow box bg/border (expected box) | `oklch(0.96 0.05 90)` / `oklch(0.88 0.07 90)` |
| Yellow box title/body/small | `oklch(0.42 0.07 75)` / `oklch(0.4 0.03 75)` / `oklch(0.5 0.03 75)` |
| **Green** (checkbox checked, done-when) | `oklch(0.62 0.14 150)` |
| Checkbox idle border | `oklch(0.82 0.02 150)` |
| Green box bg/border | `oklch(0.96 0.04 150)` / `oklch(0.86 0.06 150)` |
| Green title / ✓ mark / body | `oklch(0.42 0.08 150)` / `oklch(0.55 0.12 150)` / `oklch(0.36 0.04 150)` |
| Green pill (✓ נבחר / ✓ נשמר) | fg `oklch(0.5 0.12 150)` on `oklch(0.95 0.05 150)` |
| **Warning orange** box bg / border | `oklch(0.95 0.05 35)` / `oklch(0.78 0.12 35)` (skip-notice `0.78 0.1 35`) |
| Orange title / body | `oklch(0.48 0.15 32)` / `oklch(0.42 0.08 32)` (skip: `0.48 0.13 32` / `0.42 0.07 32`) |
| Orange step-card bg/border/circle | `oklch(0.95 0.04 35)` / `oklch(0.85 0.07 35)` / `oklch(0.58 0.16 35)` |
| **Purple 285** (Claude-Code, choices, planner) box bg/border | `oklch(0.96 0.04 285)` / `oklch(0.88 0.05 285)` |
| Purple 285 title / body | `oklch(0.45 0.12 285)` / `oklch(0.42 0.06 285)` |
| Choice selected border/bg | `oklch(0.55 0.13 285)` / `oklch(0.975 0.02 285)`; unselected `oklch(0.9 0.006 85)` / `oklch(0.99 0.003 85)` |
| **Purple 300** (stuck box) bg / dashed border | `oklch(0.96 0.03 300)` / `oklch(0.78 0.07 300)` |
| Stuck title / body / bullet | `oklch(0.45 0.12 300)` / `oklch(0.4 0.04 300)` / `oklch(0.6 0.12 300)` |
| Celebration gradient | `linear-gradient(135deg, oklch(0.55 0.13 285), oklch(0.5 0.13 248))` |
| Final-header gradient | `linear-gradient(135deg, oklch(0.45 0.11 248), oklch(0.42 0.13 285))` |
| Planner-header gradient | `linear-gradient(135deg, oklch(0.42 0.13 285), oklch(0.45 0.11 248))` |
| Neutral card bg / border (steps, fields) | `oklch(0.985 0.004 85)` / `oklch(0.92 0.006 85)` |
| Frame border / divider | `oklch(0.93 0.006 85)` / `oklch(0.94 0.006 85)` |
| Neutral gray code chip | bg `oklch(0.95 0.006 260)` |
| Dark terminal bg / bar / border | `oklch(0.22 0.012 260)` / `oklch(0.27 0.015 260)` / `oklch(0.32 0.015 260)` |
| Terminal text default/muted/yellow/green | `oklch(0.88 0.01 260)` / `oklch(0.7 0.01 260)` / `oklch(0.82 0.13 90)` / `oklch(0.78 0.15 145)` |
| Card shadow | `0 1px 2px rgba(40,35,20,0.04), 0 18px 50px -28px rgba(40,35,20,0.30)` |
| Terminal shadow | `0 14px 36px -22px rgba(20,20,40,0.7)` |
| Print fallback border | `#e6e2d8` |

### 4.2 Radii

| Element | Radius |
|---|---|
| Card shell | 22px |
| Celebration block | 18px |
| Callout boxes (warning/expected/done/stuck/notes) | 16px |
| Planner choice card | 15px |
| Step cards, choice cards, diagram frames, terminal, "בדיקת הבנה" | 14px |
| Field cards, prompt panel | 13px |
| Hint strip | 12px |
| Saveable input | 11px |
| Illustration panels | 10px |
| Section icon chip, planner number tag, textarea | 9px |
| Checkbox | 7px |
| Inline code (blue) | 6px; (small/neutral/tinted) 5px |
| Pills / progress / chips / R-badge | 999px |
| Number circle | 50% |

### 4.3 Type scale (Rubik unless noted)

| Use | Size / weight |
|---|---|
| h1 | 30px / 700, lh 1.22, ls -0.01em |
| Celebration headline | 22px / 700; input numerals 22px mono 700 |
| h2 | 18px / 700 |
| Intro line | 16.5px |
| Step text, lede, expected body | 16px, lh 1.55 |
| Choice h3 | 16–16.5px / 700 |
| Box titles, done-when/stuck lines, celebration body | 15.5px |
| Note body, bullets, prompt panel, hint prose | 15px |
| Number circle | 15px / 700 |
| Field labels, helper sentences, choice body | 14.5px |
| Expected small print, footnotes | 14px |
| Sub-hints in steps, code textarea, ✓-pills | 13.5px |
| Chips (header, celebration), code inline, terminal pre | 13–13.5px |
| Track label, progress row | 13px / 600 |
| Small code / placeholder chips | 12.5px |
| Field hints | 12.5px |
| Legend strip | 12px / 600 |
| Illustration micro-text | 8.5–11.5px |

Line heights: prose 1.5–1.6; step text 1.55; terminal 1.7.

### 4.4 Spacing rhythm

- Card padding: header `30px 34px 26px`; body `30px 34px 34px`.
- Between major blocks: `margin-bottom:30px` (after step lists/diagrams/prompts),
  `28px` (after top callouts), `14px` between the closing trio boxes, `22px`
  between stuck box and celebration.
- Step list gap `12px`; field list gap `14px`; done-when/stuck line gap `9px`;
  legend gap `14px`; chips gap `10px`.
- Section header gap `12px`; step-card internal gap `13px` (14px in T1_M1).

### 4.5 JetBrains Mono / LTR rules

1. **Every** code, filename, folder, pin label, menu path, COM port, keyboard
   shortcut, unit (`ms`), and placeholder token is JetBrains Mono **and carries
   `dir="ltr"`** (attribute preferred; `direction:ltr` in style also occurs on
   `<kbd>`/textarea). No exceptions — even single words like `millis()`.
2. Multi-line code/terminal output goes in the dark LTR `<pre>` panel (3.12).
3. Containers whose content is inherently LTR (diagram image rows, legend
   strips, terminal panel, File-Explorer mocks, numeric input rows) get
   `dir="ltr"` on the container; Hebrew captions inside them switch back with
   `dir="rtl"`.
4. Hebrew text NEVER goes in JetBrains Mono, except tiny labels inside
   illustrations where the source did so.

### 4.6 RTL rules

- `dir="rtl"` once, on `.tc-page`. Everything inherits; do not repeat on children.
- Use logical properties where sides matter: `margin-inline-start:auto` pushes
  the ✓ pill to the far (left) edge of a choice card.
- Progress row order in markup = `שלב N מתוך M` first, percent second (renders
  right/left respectively under RTL).
- Mixed Hebrew-Latin hyphenation as in source: `ל-GND`, `ב-Arduino IDE` — copy
  exactly, never "fix".

---

## 5. Card composition order (canonical page flow)

1. Header band (V1/V2/V3/final).
2. Intro line (step cards only).
3. Top callout if any: warning (3.4) / skip-notice (3.5) / purple note (3.6).
4. Diagram section (`🔌 תרשים החיווט` header + frame) when the card wires hardware.
5. Work sections: `📋 מה עושים` + step list; or planner/choice sequence
   (`שלב 1 — …`, `שלב 2 — …`) mixing choice cards, fields, prompt blocks, steps.
6. Closing trio, always in this order, `margin-bottom:14px` between them:
   👀 expected → ✅ done-when → 🪄 stuck.
7. Celebration block — final-milestone / planner cards only (after stuck, which
   then gets `margin-bottom:22px`).

---

## 6. Conventions

### 6.1 localStorage KEY naming

Pattern: `tc_<project><track><milestone>_<what>` — all lowercase:

| Card | Keys |
|---|---|
| P2 T1 M1 | `tc_p2t1m1_checks` |
| P2 T2 M1 | `tc_p2t2m1_checks` |
| P2 T2 M3 | `tc_p2t2m3_checks`, `tc_p2t2m3_diff`, `tc_p2t2m3_fields` |
| P2 T1 M6 | `tc_p2t1m6_checks`, `tc_p2t1m6_best` |
| P2 T3 planner | `tc_p2t3_checks`, `tc_p2t3_variant`, `tc_p2t3_fields` |
| P1 T2 M2b | `tc_p1t2m2b_checks` |
| P1 T3 planner | `tc_p1t3_checks`, `tc_p1t3_fields` |
| P1 T1 M1 (legacy) | `tc_t1m1_checks` (no project prefix — legacy; new cards ALWAYS include the `pN` prefix) |

Suffixes: `_checks` (checkbox map), `_fields` (JSON of textareas), `_diff` /
`_variant` (choice id string), `_best` (numeric string). All reads/writes are
wrapped in `try { … } catch (e) {}`.

### 6.2 renderVals loop bound

Always `for (let i = 1; i <= 14; i++)` for `check`/`toggle` — a fixed
over-provisioned bound so authors never forget to raise it. Field loops use the
actual field count (`i <= 6`, `i <= 7`).

### 6.3 Image paths

- P2 cards: `assets/…` relative to the card folder (e.g.
  `assets/w_p2_01_led_button_breadboard.svg`,
  `assets/arduino-usb-connection.png` in P1's folder for photos).
- P1 Fritzing exports live one level up: `../images/w4_three_leds_chasing_breadboard.svg`.
- Fritzing SVG naming: `w_p2_NN_description_breadboard.svg` (P2) /
  `wN_description_breadboard.svg` (P1). Always give a full Hebrew `alt`
  describing the wiring. Diagram `<img>` width 600px, `max-width:100%; height:auto;`.

### 6.4 $preview

Every card: `data-props="{&quot;$preview&quot;:{&quot;width&quot;:800,&quot;height&quot;:1180}}"` — exact string, on the `data-dc-script` tag.

### 6.5 File naming

`P<proj>_T<track>_M<milestone>_<slug>_he.dc.html` (P2 style; P1 legacy files
omit the `P1_` prefix). Planners: `P<proj>_T3_project_planner_he.dc.html`.

---

## 7. Author checklist (before shipping a card)

- [ ] Text is byte-identical to the FINAL source wording (Hebrew, emphasis, punctuation, `·` separators, `קΩ`, `אוהם`, color sequences).
- [ ] Skeleton matches section 1 exactly (`support.js`, helmet fonts+print CSS, tc-page/tc-card lines verbatim).
- [ ] Header variant matches track (V1/V2/choice/final/V3) with correct chip text, track label, progress N/M and % width.
- [ ] Every step checkbox binds a unique `toggleN`/`checkN`; KEY follows `tc_pXtYmZ_checks`.
- [ ] Closing trio present and ordered 👀 → ✅ → 🪄 (step cards).
- [ ] All code/pin/path tokens are JetBrains Mono with `dir="ltr"`.
- [ ] Diagram frames wrap images with correct paths + Hebrew alt.
- [ ] `$preview` 800×1180; renderVals loop `<= 14`.
- [ ] Breadboard vocabulary: numbered strips = `טורים`, lettered = `שורות` (never swapped) — but remember: you never rewrite text anyway.
