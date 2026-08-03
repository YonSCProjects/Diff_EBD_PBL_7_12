# Card Editing Preferences Log

Learned patterns from **Yon's review-console edits** of the Hebrew (.dc.html) cards.
Maintained by the `/learn-changes` skill; used when authoring new cards (P5–P8) alongside
`dc_design_spec.md`, and when regenerating or sweeping existing cards.

Relationship to the other logs: `Hebrew_Translation_Preferences_Log.md` governs
translation/verb-form/register; `Editorial_Preferences_Log.md` governs the master-document
editorial voice. This log captures **how Yon edits the final student-facing cards**.
If a learned rule conflicts with either log, the conflict is surfaced to Yon, not resolved silently.

**Status ladder:** `TENTATIVE` (1–2 examples) → `FIRM` (3+ consistent, ≥2 cards, no strong
counterexamples) → `CONFIRMED` (Yon approved, or an approved sweep applied it program-wide).
Only FIRM/CONFIRMED rules are applied silently when authoring; TENTATIVE = "leaning".
A *strong* counterexample is a surviving instance in a card Yon marked **done**; instances in
cards he hasn't reviewed yet are weak counterexamples.

---

## Category T — Trimming / terseness

### T1 — Trim reassurance tails from stuck/help lines
**Rule:** In "תקועים?" boxes and help lines, the escalation is stated bare — "קוראים למורה." —
without appended reassurance or justification clauses ("לעזרה", "— זה חלק מהתהליך").

**Why (inferred):** The reassurance framing ("להיתקע זה חלק מהלמידה") already lives in R2 and
the program's stuck-protocol; repeating it on every card dilutes it. Shorter lines scan better
for the EBD population.

**Examples:**
- `תקועים? קוראים למורה לעזרה — זה חלק מהתהליך.` → `תקועים? קוראים למורה.` (P1 T1_M1, feedback 2026-07-08)

- `עדיין תקועים? קוראים למורה. זה השלב הראשון של חיווט + העלאה — מבקשים עזרה בלי לחשוש.` →
  `עדיין תקועים? קוראים למורה.` (P1 T1_M4, feedback 2026-08-04)

**Sharpened scope (from counterexample analysis, 2026-08-04):** trim only *reassurance / justification*
tails — "לעזרה", "זה חלק מהתהליך", "מבקשים עזרה בלי לחשוש". **Keep informational tails**, which Yon has
never touched: `קוראים למורה. בשביל זה יש את פרוטוקול…` (3×), `קוראים למורה ובוחרים יחד` (3×),
`קוראים למורה כשנתקעים שוב באותה בעיה` (2×), `קוראים למורה. גלגל שמתנדנד כנראה לא נדחף עד סוף הציר`,
and the diagnostic variants in P4 — those carry content, not comfort.

**Evidence:** 2 direct (2 cards), plus the same underlying preference already CONFIRMED in T3 and FIRM
in W2 — the "cut chrome and comfort, keep information" family.
**Counterexamples:** 13× `קוראים למורה לעזרה.` survive, all in cards Yon has not reviewed yet (weak).
**Protected carve-out:** the soldering escalation **"קוראים למורה, תמיד"** (9× across P4 + R6) and every
soldering-safety "קוראים למורה" line — locked motifs, NEVER trimmed.
**Status:** FIRM · **Sweep candidate:** the 13 `לעזרה` instances (pure reassurance, mechanical);
excludes every soldering/safety context and all informational tails above.

### T2 — Drop incidental "יחד עם המורה"
**Rule:** When teacher involvement is incidental to the action (creating a folder, routine steps),
drop "יחד עם המורה"; keep it only where teacher presence is the point (safety, soldering, first-time
setup rituals like opening Claude Code together).

**Why (inferred):** Autonomy-first framing — the students can do routine actions themselves;
reserving the teacher for moments that need the teacher keeps those moments meaningful.

**Examples:**
- `אם אין — יוצרים אותה יחד עם המורה.` → `אם אין — יוצרים אותה.` (P1 T1_M1, feedback 2026-07-05; restated by Yon in the card-note twice)

**Evidence:** 1 (+2 card-note restatements) · **Counterexamples:** ~18 instances across 10 files;
at least 5 are in P4 T1_M1 soldering context (protected — teacher presence IS the point there).
**Note (2026-07-13):** Yon's own uncommitted rework of T1_M1 reintroduces the phrase — most likely
an old-text-baseline artifact of that rework, not a reversal (pending his confirmation).
**Status:** TENTATIVE · **Sweep scope:** non-safety, non-soldering instances only, case-by-case.

---

## Category W — Wording clarity

### W1 — Explicit subject noun over bare-verb sentence openers (hints/sub-notes)
**Rule:** Hint lines don't open with a bare verb whose subject is implied from the previous
sentence; the subject noun is stated explicitly ("**קובץ** נמצא בתיקיית…" not "נמצא בתיקיית…").

**Why (inferred):** For students with reading difficulty, a sentence that names its subject is
parseable on its own; a verb-opener forces re-reading the previous sentence.

**Examples:**
- `נמצא בתיקיית פרויקט 1 שלכם, בתוך ino_files/…` → `קובץ נמצא בתיקיית פרויקט 1 שלכם, בתוך ino_files/…` (P1 T1_M2, feedback 2026-07-08)

**Evidence:** 1 · **Counterexamples:** not yet surveyed.
**Status:** TENTATIVE.

---

## Category V — Visuals

### V1 — Real screenshots/photos over drawn mockups for software UI and hardware
**Rule:** When a card shows a piece of real software UI (IDE toolbar, File Explorer) or real
hardware (the Arduino board), prefer an actual screenshot/photo supplied by Yon over a drawn
HTML/SVG mockup. Frame it in the standard diagram-frame (border, radius, soft shadow), store it
in the card's `assets/`, keep a Hebrew alt text. Fritzing breadboard diagrams are NOT mockups —
they stay.

**Why (inferred):** Students see the real thing on their own screens/desks; fidelity beats style.

**Examples:**
- Comment: "replace the image here with C:\Users\Yon\Downloads\upload.png" → the drawn IDE-toolbar
  mockup replaced by a real Arduino-IDE screenshot (P1 T1_M2, feedback 2026-07-08).
- Yon's own rework of P1 T1_M1 (2026-07-13, uncommitted WIP) replaces the elaborate inline-SVG
  Arduino Uno with a real board photo (`arduino_uno_r3_black_soft.png`) + a real IDE icon.

- Figure must actually show what the card teaches: T1_M5 ("מוסיפים לד שני") had been shipping the
  single-LED figure from T1_M3 plus a note apologizing for it ("בתרשים מופיע לד אחד לדוגמה"). On
  Yon's instruction (2026-08-04) it was replaced with the real two-LED render from
  `images/fritzing/w2_two_leds.fzz`, and the now-false apology sentence was dropped from the note.

**Evidence:** 3 (independent cards, consistent direction) · **Counterexamples:** none in edited cards.
**Status:** FIRM. Corollaries: (a) prefer the real render/photo over a stand-in; (b) never ship a
figure that contradicts its card — fix the figure, don't caption around it; (c) captions live in
**HTML, not baked into the image** (baked Hebrew captions blocked the X1 terminology sweep and had
to be cropped off three P1 PNGs).
**Procedure:** Yon supplies the image path; copy into `task_cards_he/assets/`; the bundle build
inlines it automatically (`inlineImages`).

---

### T3 — No standalone "how to use this card" intro line — CONFIRMED (swept 2026-08-03)
**Rule:** Cards do NOT carry the chrome line "עוברים על השלבים לפי הסדר. אפשר לסמן ✓ לכל שלב שמסיימים." between the header band and the first section. The checkboxes are self-explanatory.

**Why:** Yon removed it from T1_M1 (comment: "להוריד לגמרי את השורה הזאת") and then approved a program-wide sweep ("remove from all").

**Sweep record:** 2026-08-03 — removed from all 34 dc task cards that carried it (21 never had it). Two content-bearing near-variants kept pending his call: "השלב (הזה) מאחד כמה צעדים. עוברים אחד-אחד; אפשר לסמן ✓ לכל שלב." (P1×2 merged-step cards).
**Status:** CONFIRMED. New cards (P5–P8) must not include the line.

### W2 — Expected-boxes and figure captions state the observation, not the explanation
**Rule:** "מה רואים אם הכול תקין" and figure captions give the shortest observable fact ("הלד הירוק הקטן L ליד רגל 13 מהבהב."); background explanations and warm meta-framing are cut even when factually useful. **This governs NEW text being written — it is NOT a license to trim existing reviewed card content** (see sweep evaluation below).

**Why (explicit):** 2026-08-03 — Claude added a factory-Blink explanation + reused-board hedge to answer Yon's correctness question; Yon replaced it with the bare observation ("let's make it simple"). When a correctness issue is flagged, fix the claim minimally — don't add background.

**Examples:**
- `…מהבהב פעם בשנייה — לוח חדש מגיע מהמפעל עם קוד הבהוב מובנה. לוח שכבר השתמשו בו עשוי להתנהג אחרת, וזה בסדר.` → `…מהבהב.` (P1 T1_M1, direct instruction)
- Caption: `זה הלוח שלכם מהערכה — הלד הירוק L נמצא בשורת הלדים שליד רגל 13. כשהקוד רץ, הוא נדלק בירוק בדיוק כאן.` → `הלד L נמצא בשורת הלדים שליד רגל 13. כשהקוד רץ הוא נדלק באור ירוק.` (P1 T1_M1, feedback 2026-08-03 — warm framing "זה הלוח שלכם", the duplicate "הירוק", and "בדיוק כאן" all dropped)

**Evidence:** 2 · **Status:** FIRM (authoring-scope).
**Sweep evaluation (2026-08-03): REJECTED.** A scan flagged 39/55 cards with explanation-style tails in expected-boxes — but nearly all are original, reviewed content: protected catchphrases (`זה תקין, לא תקלה`, `ככה עובדים מהנדסים אמיתיים`), forward-pointers (`זה יקרה בשלב 2`), fails-gracefully reassurances. Mechanically trimming them would violate the protected-motifs guard. W2 applies to new authoring and to boxes Yon edits himself.

### W3 — Everyday verbs over formal register
**Rule:** Prefer the common verb over its formal synonym in instructions (מוצאים, not מאתרים).

**Why (inferred):** Reading accessibility — the everyday verb is recognized instantly by students with reading difficulty. Complements (does not conflict with) the plural-impersonal rule A1 in `Hebrew_Translation_Preferences_Log.md`.

**Examples:**
- `מאתרים על הלוח את הלד הירוק הקטן…` → `מוצאים על הלוח את…` (P1 T1_M1, feedback 2026-08-03)

**Evidence:** 1 · **Counterexamples:** 0 — no מאתרים/לאתר/איתור left anywhere.
**Status:** TENTATIVE (watch for more formal→everyday swaps: מבצעים→עושים, מתבוננים→מסתכלים…).

### W4 — Simple comparative descriptors over shape-jargon
**Rule:** Describe hardware by the simplest distinguishing feature ("הקצה הגדול יותר"), not by technical shape adjectives ("הקצה השטוח הרחב").

**Examples:**
- `…והקצה השטוח הרחב (USB-A) נכנס למחשב` → `…והקצה הגדול יותר (USB-A) נכנס למחשב` (P1 T1_M1, feedback 2026-08-03)

**Evidence:** 1 · **Status:** TENTATIVE.

### W5 — Section headers orient; tool names get a de-emphasized gloss
**Rule:** Part headers say where/what concretely ("מכינים את התיקיות **במחשב**"), and a first-appearance tool name may carry a short parenthetical explanation styled smaller + non-bold ("Arduino IDE <span small normal>(התוכנה שאיתה מתכנתים את הארדואינו)</span>").

**Examples:**
- `חלק א · מכינים את התיקיות` → `חלק א · מכינים את התיקיות במחשב` (P1 T1_M1, feedback 2026-08-03)
- `חלק ג · מגדירים את Arduino IDE` → `+ (התוכנה שאיתה מתכנתים את הארדואינו)`, gloss at 14px/400 per Yon's styling comment (P1 T1_M1, feedback 2026-08-03)

**Evidence:** 2 (one card) · **Status:** TENTATIVE.

### V2 — Teaching annotations span the FULL extent of what they mark
**Rule:** When an overlay marks a concept on a figure, it must cover that concept's full extent — a
**טור** highlight runs the whole column (both breadboard halves), a **שורה** highlight runs the whole
row (the board's full width). A partial marker teaches the wrong shape.

**Why (Yon, explicit):** "הסימנים שהוספת כדי שיראו מהו טור ומהי שורה מצוינים, רק בבקשה שנה שהסימון
של הטור יהיה לכל אורך הטור והסימון של השורה יהיה לכל אורך השורה" (comment, T1_M3, feedback 2026-08-04_0111).
The overlay's job is to teach an orientation — full length makes the vertical/horizontal contrast
unmistakable; a short stub reads as "this spot", not "this direction".

**How (procedure):** measure the figure's grid computationally rather than eyeballing percentages —
sample the image's darkness profile to find hole row/column centers (scratchpad `holes.js`), then
place the overlay on real coordinates. For `m3_breadboard.png`: hole rows at 41.2/44.5/47.5/50.5/53.6%
(top half) and 63.1/66.1/69.3/72.4/75.4% (bottom half), pitch ≈3.05%; board spans x≈33–97%.
Keep the band on a row clear of components.

**Evidence:** 1 (explicit instruction) · **Status:** FIRM (stated as a correction to a pattern Yon
had just praised) · Applies to any future figure annotation, in any project.

### V3 — When a figure changes, sweep the whole card for text that described the old one
**Rule:** Replacing a figure is not done until every sentence that referred to the old figure is
re-checked — including stuck boxes and side notes, not just the caption.

**Why:** After the T1_M5 two-LED figure landed, "רק **טור אחד** הצידה" was wrong in **two** places
(the info note under the figure and the "תקועים?" box). Yon caught both across two saves
(feedback 2026-08-04_0110 and _0120) — evidence that the whole card, not just the figure's
neighbourhood, has to be re-read.

**Examples:** `רק טור אחד הצידה` → `רק כמה טורים הצידה` (P1 T1_M5, ×2 locations).
**Evidence:** 2 (same card, two locations, two saves) · **Status:** FIRM as a procedure.

---

## Category X — Terminology (program-wide vocabulary)

### X1 — "רגל" is reserved for component legs; Arduino pins are "חיבור דיגיטלי N" — CONFIRMED (swept 2026-08-04)
**Rule:** One word, one concept. **Arduino pins** are `חיבור דיגיטלי 9` (power pins: `חיבור 5V`,
plural `חיבורים 9 ו-10`, table header `החיבור בארדואינו`, section title `מפת החיבורים`).
**רגל stays** for physical component legs only: `רגל ארוכה`/`רגל קצרה` of an LED, `רגלי החיישן`,
`רגל A`/`רגל B` of a button, `רגל אחת של הנגד`.

**Why (Yon, explicit):** "אני מציע שלא נקרא לכניסות של הארדואינו 'רגל' — נשאיר את הרגל לנגדים
וכאלה" (card note, T1_M3, feedback 2026-08-04_0025), then approved the program-wide sweep. Using
one word for two different things is exactly the ambiguity this student population can't afford.

**Gender consequence (mandatory):** חיבור is masculine where רגל was feminine — agreement flips
whenever the pin is the subject (`רגל דיגיטלית` → `חיבור דיגיטלי`, `הרגליים … הן` → `החיבורים … הם`,
`אחת`→`אחד`). Do NOT flip words whose subject is a component leg
(`חיבור דיגיטלי 9, והרגל הקצרה **מחוברת** ל-GND` is correct).

**Attribution:** keep the source's own suffix (`חיבור דיגיטלי 9 של הארדואינו`); never inject a new
one and never double it.

**Never touch:** English/LTR content (`pin 9`, `D9`), code blocks, `<pre>` ASCII wiring panels.

**Sweep record:** 2026-08-04 — 45 files (task + reference cards, P1–P4) swept by a 91-agent workflow
with an independent auditor per file; final audit: **313** `חיבור דיגיטלי N` instances, **0** pin-context
`רגל` leftovers, **0** over-reach, **61** component-leg usages preserved unchanged. Three P1 figure
images had the old terminology *baked in* as captions — those strips were cropped off and replaced
with HTML captions carrying the new wording (m3, m7; m5 was replaced outright, see V1).
**Status:** CONFIRMED — binding for all new authoring (P5–P8) and any regenerated card.

---

## Category P — Punctuation

### P2 — No comma before the conjunction ו' — CONFIRMED (rule stated by Yon)
**Rule:** Never place a comma before a vav-conjunction (`…מחכים שלוש שניות ומחברים בחזרה`, not
`…שלוש שניות, ומחברים`).

**Why (Yon, explicit):** "חוק חשוב, לא לשים פסיק לפני וו החיבור" (comment, T1_M2, feedback
2026-08-03_2357).

**Examples:**
- `מוציאים את כבל ה־USB, מחכים שלוש שניות, ומחברים בחזרה.` → `…מחכים שלוש שניות ומחברים בחזרה.`

**Status:** CONFIRMED as a writing rule (stated as law).
**Sweep status: NOT swept.** ~345 candidate `, ו…` sites exist across the dc cards, but many are
legitimate (comma closing a subordinate clause that happens to be followed by ו', list separators,
quoted/English content). A sweep would need per-instance judgment — offer it to Yon as a reviewed
batch rather than a blind replace.

### P1 — Minimal commas in short student-facing sentences
**Rule:** Short observable statements drop commas that Hebrew grammar does not require ("הלד הירוק הקטן L ליד רגל 13 מהבהב." — no commas; "כשהקוד רץ הוא נדלק" — no comma after the clause).

**Why (inferred):** Fewer visual stops = easier scanning for the EBD population; commas reserved for real ambiguity.

**Examples:**
- `הלד הירוק הקטן L, ליד רגל 13, מהבהב.` → `הלד הירוק הקטן L ליד רגל 13 מהבהב.` (P1 T1_M1, feedback 2026-08-03_2305)
- `כשהקוד רץ, הוא נדלק…` → `כשהקוד רץ הוא נדלק…` (P1 T1_M1 caption, feedback 2026-08-03)
- `רק כמה טורים הצידה, ודרך הנגד…` → `רק כמה טורים הצידה ודרך הנגד…` (P1 T1_M5, feedback 2026-08-04 — also P2)
- `אם הלד הראשון הפסיק להבהב בזמן חיווט השני, אולי הג'אמפר שלו התנתק` → `…בזמן חיווט השני אולי הג'אמפר שלו התנתק` (P1 T1_M5 stuck box, feedback 2026-08-04_0120 — comma before אולי, not a vav: the preference is broader than P2)

**Evidence:** 4 (2 cards) · **Status:** FIRM — apply when authoring; still do NOT sweep mechanically
(many existing commas legitimately close a subordinate clause; needs per-instance judgment, same as P2).

## Processed feedback ledger
| Date learned | Feedback files |
|---|---|
| 2026-08-04 (2nd run) | feedback_2026-08-04_0110 · _0111 · _0111_2 · _0113 · _0114 · _0120 |
| 2026-08-04 | feedback_2026-08-03_2351 · feedback_2026-08-03_2351_2 · feedback_2026-08-03_2357 · feedback_2026-08-04_0007 · feedback_2026-08-04_0025 |
| 2026-08-03 | feedback_2026-08-03_2232 · feedback_2026-08-03_2305 |
| 2026-07-13 | feedback_2026-07-05_2141 · feedback_2026-07-08_1726 · feedback_2026-07-08_1749 · feedback_2026-07-08_1749_2 · feedback_2026-07-08_1755 |

## Changelog
- **2026-08-04 (learn run 2)** — 2 new rules: **V2** (teaching annotations span the full extent of what
  they mark, + the measure-don't-eyeball procedure) and **V3** (a figure swap requires sweeping the whole
  card for text describing the old figure). **T1 → FIRM** with a sharpened scope from counterexample
  analysis: trim reassurance tails only, never informational ones (13 `לעזרה` sites remain as a clean
  sweep candidate; 9 soldering `תמיד` sites protected). **P1 → FIRM** (4 examples; sweep still deferred).
  Also applied a late-arriving edit from _0120 that the previous apply round predated.
- **2026-08-04** — **X1 terminology sweep CONFIRMED + executed**: Arduino pins רגל → חיבור דיגיטלי across
  45 files (313 instances; 0 leftovers, 0 over-reach, 61 component legs preserved), incl. gender-agreement
  flips and cropping three baked-in figure captions. **P2** (no comma before ו') recorded CONFIRMED as a
  writing rule, sweep deferred (needs per-instance judgment). **V1** promoted to FIRM with the T1_M5
  two-LED figure replacement + the "captions in HTML, not baked" corollary. Feedback ledger: 2026-08-04_0007/_0025.
- **2026-08-03 (learn run)** — 4 new rules: W3 everyday verbs (מאתרים→מוצאים), W4 simple descriptors,
  W5 header orientation + de-emphasized tool gloss, P1 minimal commas. W2 broadened to figure captions
  (+1 example) and scope-narrowed to authoring-only after a sweep evaluation REJECTED trimming existing
  boxes (39/55 flags were protected/original content). Ledger: 2026-08-03_2232 + _2305.
- **2026-08-03** — T3 added and CONFIRMED via approved sweep (intro chrome line removed from 34 cards);
  W2 added (FIRM, explicit "make it simple" instruction on expected-boxes). Feedback 2026-08-03_2232 applied
  (7 T1_M1 changes; T1_M2 entries were stale cache — Yon had not reset the console).
- **2026-07-13** — Log bootstrapped by /learn-changes creation: 4 seed rules (T1, T2, W1, V1) from the
  2026-07-05 + 2026-07-08 review rounds; V1 strengthened by Yon's own T1_M1 image rework.
