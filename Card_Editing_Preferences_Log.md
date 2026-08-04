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
- `זה שלב החיווט הקשה ביותר בפרויקט 1. המורה מצפה לעזור בשלב זה — קוראים לו.` →
  `זה שלב החיווט הקשה ביותר בפרויקט 1. אם נתקעים קוראים למורה.` (P1 T1_M7, feedback 2026-08-04_1312 —
  4th instance; note the conditional framing "אם נתקעים" replacing the reassurance)
- `קוראים למורה — מעבר לקצב הזה הוא רגע שבו עדיף לא להיאבק לבד.` → `קוראים למורה.`
  (P1 T2_M1, feedback 2026-08-04_1442 — 5th instance)

**Status:** CONFIRMED · **Sweep executed 2026-08-04:** all 13 `קוראים למורה לעזרה.` → `קוראים למורה.`
across 13 cards (P1 T1_M2/M3/M6/M8; P3 T1_M2/M3/M4/M5, T2_M3; P4 T1_M5/M6/M7, T2_M3). Verified after:
0 leftovers, the 9 protected soldering `קוראים למורה, תמיד` lines untouched, and every informational
tail left in place. New cards must not reintroduce a reassurance tail.

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

### W3 — The plainer, more concrete word wins
**Rule:** Prefer the common verb over its formal synonym (מוצאים, not מאתרים), and the plainer noun
phrase over the terser one (שום דבר, not כלום).

**Why (inferred):** Reading accessibility — the everyday verb is recognized instantly by students with reading difficulty. Complements (does not conflict with) the plural-impersonal rule A1 in `Hebrew_Translation_Preferences_Log.md`.

**Examples:**
- `מאתרים על הלוח את הלד הירוק הקטן…` → `מוצאים על הלוח את…` (P1 T1_M1, feedback 2026-08-03)
- `עדיין לא קורה כלום חדש בלחיצה` → `עדיין לא קורה שום דבר חדש בלחיצה` (P1 T1_M7, feedback 2026-08-04_1312)
- `הם אמורים להתחלף לסירוגין` → `הם אמורים להידלק לסירוגין` (P1 T1_M6, same round) — also restores the
  program's LED-verb convention: a LED **נדלק/מאיר**; "מתחלף" describes the pair, not the component.

**Evidence:** 3 (3 cards) · **Counterexamples:** 0 — no מאתרים/לאתר/איתור left anywhere.
**Status:** FIRM (watch for more: מבצעים→עושים, מתבוננים→מסתכלים…).

### W6 — The header lede states what the card does — nothing else
**Rule:** The subtitle under the card title names the action only. Difficulty warnings, help offers and
encouragement do not belong there (they live in the warning box or the "תקועים?" box), and the lede is
**bold**.

**Why (Yon, explicit):** on T1_M7 he cut `שלב החיווט הקשה ביותר בפרויקט — אם לא בטוחים, קוראים למורה`
from the lede and commented "הדגש את הפונט". The difficulty warning already exists twice on that card
(the red warning box and the stuck box) — front-loading it in the lede greets the student with "this is
the hard one" before they have read a single step.

**Examples:**
- `מוסיפים כפתור לחיצה ונגד הורדה. שלב החיווט הקשה ביותר בפרויקט — אם לא בטוחים, קוראים למורה.`
  → `**מוסיפים כפתור לחיצה ונגד הורדה.**` (P1 T1_M7, feedback 2026-08-04_1312)

- `לחיצה על הכפתור מחליפה איזה לד דולק. זה הפרויקט האינטראקטיבי הראשון שלכם: קלט מהכפתור משנה את פלט הלדים.`
  → `לחיצה על הכפתור מחליפה את הלד הדולק.` (P1 T1_M8, feedback 2026-08-04_1435)
- `הפעלה מרוכזת: פותחים עמדת עבודה, מחווטים לד אחד…` → `פותחים עמדת עבודה, מחווטים לד אחד…`
  (P1 T2_M1, feedback 2026-08-04_1451 — a category label is chrome too)

**Evidence:** 3 (3 cards) · **Status:** FIRM. The de-duplication logic (say it where it belongs, once)
matches T1/T3/W2. Ledes carry the action, nothing else — no difficulty warning, no meta-framing,
no category label.

### W7 — No abstract concept-framing — the card teaches the action, not the pattern behind it
**Rule:** Cards don't name the computer-science abstraction a step illustrates. No "this is the basic
pattern of every interactive project", no קלט → החלטה → פלט diagram, no "input changes output" framing.
The student does the concrete thing; the concept is the teacher's material, not the card's.

**Why (Yon, 2026-08-04, T1_M8):** he cut `זה הפרויקט האינטראקטיבי הראשון שלכם: קלט מהכפתור משנה את פלט
הלדים` from the lede **and** deleted the whole קלט→החלטה→פלט chip box beneath the code ("הסר את השורה
הזאת ואת השורה שמתחתיה") — two separate removals of the same idea on one card. Naming an abstraction
adds vocabulary to learn on top of the task; the pattern is felt by doing it, not by being told.

**Examples:**
- lede: `…זה הפרויקט האינטראקטיבי הראשון שלכם: קלט מהכפתור משנה את פלט הלדים.` → removed
- the `התבנית הבסיסית של כל פרויקט אינטראקטיבי:` box with קלט/החלטה/פלט chips → removed entirely

**Evidence:** 2 removals on 1 card (one edit + one comment, same concept) · **Counterexamples:** 0 —
no קלט/פלט framing survives anywhere in the cards. **Status:** FIRM (the concept was eliminated, not
trimmed). Distinct from W2 (which is about explanation vs observation): W7 is about *abstraction* —
don't teach the category, teach the doing.

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

### V4 — First encounter with a part or a board feature gets a picture
**Rule:** The first time a card introduces a physical component (LED, resistor, pushbutton, buzzer,
sensor, motor driver…) or a breadboard feature (טור, שורה, החריץ המרכזי), the step carries a small
labelled illustration beside the text — not just words. Later mentions don't need it.

**Why (Yon, repeatedly):** "זו הפעם הראשונה שהתלמיד פוגש breadboard — בוא נוסיף לציור משהו שיבהיר מהי
שורה ומהו טור"; "הוסף איור של נגד 220 אום שרואים בו את הצבעים"; "להוסיף תמונה של כפתור לחיצה כמו זה
שמופיע למעלה באיור של fritzing"; "הוסף כאן איור של נגד 10 קילו אוהם עם הצבעים הנכונים שלו". A student
who has never held the part cannot match a name to an object from prose alone — and colour-coded parts
(resistors) are *only* identifiable visually.

**Examples (5, across 2 cards, all 2026-08-04):**
- P1 T1_M3 — טור/שורה overlays on the wiring figure (first breadboard); 220 Ω resistor with its bands.
- P1 T1_M7 — pushbutton drawing matching the Fritzing part; "החריץ המרכזי" overlay; 10 kΩ resistor
  with its bands (חום · שחור · כתום) under the "not the 220 Ω one" warning.

**How — best source first (learned the hard way 2026-08-04):**
1. **Extract the real part from the Fritzing SVG as vector.** `scratchpad/find_part.js` lists each
   `g[partID]` with its bbox; `extract_part.js <svg> <partID> <out.svg>` pulls one part into a
   tightly-cropped standalone SVG (defs carried along). Crisp at any size, and it is *literally* the
   component the student sees in the card's wiring figure. (P1 button = part `90000120` of
   `w3_leds_and_button_pulldown_breadboard.svg` → `assets/pushbutton.svg`.)
2. Only if the part isn't in a Fritzing figure, draw an inline SVG — and match the Fritzing look.
3. Never crop-and-enlarge the PNG figure: the part is ~50 px there and turns to mush.

**A drawn imitation can mislead:** Claude's hand-drawn pushbutton showed two top tabs and read as a
**2-leg** part; Yon caught it ("in this image only 2 legs are seen and this may be misleading") and asked
for the Fritzing one. Fidelity of the *part count / distinguishing features* matters more than style.
Label in Hebrew; never leave English chrome (a "4 legs" caption) in the drawing.

**Evidence:** 5 (2 cards, 4 separate explicit requests) · **Status:** FIRM.
**Counterexamples / sweep candidate:** only T1_M3 and T1_M7 currently carry component illustrations.
Parts introduced with no picture anywhere: **buzzer** (P2 T1_M4), **HC-SR04** (P3 T1_M1), **gear motors**
(P4 T1_M2), **L298N driver** (P4 T1_M4), **line sensors** (P4 T1_M3), plus the **soldering iron** (P4 T1_M1).
Yon simply hasn't reached those cards yet — offer the illustrations when he does, or as a batch.

### V5 — Multi-part technical lines are stacked rows, never one long chain
**Rule:** A line that strings several technical steps together with arrows or semicolons gets broken
into stacked rows (or bullets) — one relationship per row, colour-coded where it helps.

**Why (Yon, 3 times):** "הטקסט של השורה הזאת מצוין אבל בגלל החיצים הוא נראה קצת מבולגן ויכול להרתיע
תלמידים שקשה להם עם קריאה וריכוז" (T1_M2); "שורות טקסט כאלה שיש בהן חצים צריך לארגן בצורה שתהיה יותר
ברורה לעין. אולי להפריד את הרגל הארוכה והרגל הקצרה לשתי שורות" (T2_M1); "לכתוב את הטקסט הזה באופן ברור
יותר ויזואלית, לא כשורה אחת ארוכה" (T2_M2). A dense chain is a wall of symbols for a student with
reading difficulty; one relationship per row can be followed with a finger.

**Examples:**
- `בודקים שב־Tools → Board מופיע "Arduino Uno" ושב־Tools → Port מופיעה יציאת COM` → lead-in + two rows,
  each with the menu path in a mono chip (P1 T1_M2, feedback 2026-08-03_2357)
- `מחווטים לד אחד: רגל ארוכה (+) → נגד 220Ω → חיבור דיגיטלי 9, רגל קצרה (−) → GND` → two colour-coded
  rows, green long-leg / red short-leg (P1 T2_M1, feedback 2026-08-04_1442)
- T2_M2's one-paragraph "תקועים?" → four bullets (feedback 2026-08-04_1446)

**Evidence:** 3 (3 cards, all explicit) · **Status:** FIRM.

**Sweep evaluated 2026-08-04 → NO-OP (nothing to change).** The three "candidates" a grep had flagged
turned out to be **figure legends** — colour-keyed strips under the breadboard diagrams, where each entry
pairs a colour swatch with a 3-token chain (`9 → 220Ω → לד`). A legend is not prose: the compact chain is
the right form there, and stacking rows inside a horizontal legend would make it worse. The only prose
chains left are a **file path** (`Google Drive → My Drive → …`) and a **cycle**
(`לסירוגין → רדיפה → נשימה → חוזר`), where the arrow means "then" and reads correctly.

**Scope, sharpened by that check:** V5 governs **prose instructions and stuck/expected boxes** — lines the
student reads as a sentence. It does NOT apply to legends, file/menu paths, sequence-of-states lists, or
the English `<pre>` panels. *Lesson for future sweeps: look at the surrounding element before trusting a
text-pattern grep — the same characters mean different things in a legend and in a sentence.*

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

### X3 — Arduino pins carry the attribution: "חיבור דיגיטלי N של הארדואינו" — CONFIRMED (swept 2026-08-04)
**Rule:** Every Arduino pin reference names the board: `חיבור דיגיטלי 9 של הארדואינו` (and
`חיבור אנלוגי N של הארדואינו` if analog pins ever appear). Builds on X1 — X1 stopped calling pins "רגל",
X3 says whose connection it is.

**Why (Yon, explicit):** "כאן ובכל מקום אחר בכרטיסים כתוב 'חיבור דיגיטלי 9 של הארדואינו' במקום
'חיבור דיגיטלי 9'… ואם זה חיבור אנלוגי אז כתוב 'חיבור אנלוגי 9 של הארדואינו'" (T1_M8, feedback
2026-08-04_1435). A student wiring a breadboard has connections everywhere; naming the board removes
the ambiguity at every mention.

**Sweep record:** 2026-08-04 — **312** references: 272 in plain prose + **40 where the number sat inside
inline markup** (`חיבור דיגיטלי <strong>9</strong>`, `<code dir="ltr">2</code>`) that a plain-text pass
misses entirely — always run a second markup-aware pass. `<pre>` ASCII panels excluded (English layer).
Verified 0 bare refs, 0 doubled attributions.

**⚠ Sweep-script hazard (found here, applies to every future sweep):** a regex like
`(חיבור דיגיטלי \d+)(?! של הארדואינו)` **backtracks** — on already-attributed text `\d+` matches just the
`1` of `13`, the lookahead then sees `3 של…` and succeeds, producing `חיבור דיגיטלי 1 של הארדואינו3`.
Always anchor the number: `\d+(?!\d)`. This run was verified clean (all 2-digit pins intact), but the
scripts are **not** safe to re-run as written.

**Thinning sweep — approved and applied 2026-08-04.** The literal sweep left blocks repeating the
attribution (`לד 1 (חיבור דיגיטלי 9 של הארדואינו) דולק, לד 2 (חיבור דיגיטלי 10 של הארדואינו) כבוי`).
Yon approved thinning, so the standing form of X3 is now:

> **Keep the attribution on the FIRST pin mention in a block** (paragraph, caption, list item, table
> cell); later mentions in that same block are bare `חיבור דיגיטלי N`.

Applied: **101 repeats removed across 31 files, 254 first-mentions kept**; verified 0 blocks with a
doubled attribution. New cards must follow the first-mention-per-block form.

### X2 — Units are written with no space, using the symbol: "5V", "220Ω", "10kΩ" — CONFIRMED (swept 2026-08-04)
**Rule:** `5V`, `220Ω`, `10kΩ` — never `5 V`, `220 אוהם`, `10 קילו-אוהם`, `10 קΩ`. The number and its
unit symbol are one token, and the unit uses the Latin/symbol form even in Hebrew prose.

**Why (Yon, explicit):** "בכל מקום בכרטיסיות שכתוב 5 V צריך לשנות ל-5V" (comment, T1_M6, feedback
2026-08-04_1302). A split token reads as two things and can wrap across a line.

**Sweep record:** 2026-08-04 — 81 instances across 25 cards (all four projects, task + reference).
Verified 0 leftovers. New cards must write `5V`.

**Resistor units — RESOLVED 2026-08-04.** Yon: *"use the 10kΩ format"* → the same no-space symbol form
applies to resistance: **`220Ω`** and **`10kΩ`**. The seven prior variants (`220 אוהם` ×89, `220 Ω` ×20,
`220Ω` ×5, `10 קילו-אוהם` ×32, `10 קΩ` ×17, `10 kΩ` ×10, `10kΩ` ×1) are gone from Hebrew prose.

**Sweep record:** 2026-08-04 — 141 prose instances across 29 files; 0 prose leftovers.
**Deliberate carve-out — the LTR ASCII wiring panels keep `[220 Ω]` / `[10 kΩ]` (27 instances).**
Those `<pre>` diagrams are column-aligned — `│` and `▼` on following lines sit under the `┬` that
follows the value, so deleting a space would shift the connector and break the drawing:
```
Arduino pin 9  ───[220 Ω]───┬─── LED long leg
                           │
                           ▼
```
They are also the English/technical layer, where a space before the unit is the normal convention.
Any future unit sweep must exclude `<pre>` blocks the same way.

**Bidi note (verified by render, not assumed):** `10kΩ` inside RTL Hebrew displays correctly as
`10kΩ` — digits + `k` + `Ω` form one LTR run. No `dir="ltr"` wrapper or `&lrm;` is needed.

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

### P3 — Background explanations inside a step go in parentheses
**Rule:** When a step's sentence carries a "why this works" clause after the action, wrap it in
parentheses so the eye can skip it and still execute the step.

**Example:**
- `…ל-GND. זהו נגד ההורדה — הוא מחזיק את חיבור דיגיטלי 2 על 0 וולט כשהכפתור לא לחוץ.`
  → `…ל-GND. (זהו נגד ההורדה — הוא מחזיק את חיבור דיגיטלי 2 על 0 וולט כשהכפתור לא לחוץ).`
  (P1 T1_M7, feedback 2026-08-04_1312)

**Why (inferred):** same instinct as W2 — the action must stay findable; explanation is optional
reading, and parentheses mark it as such without deleting it.

**Evidence:** 1 · **Status:** TENTATIVE.

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

---

## Resolved conflicts

### 2026-08-04 — imperative "קראו" vs the plural-impersonal rule (A1) — RESOLVED, A1 HOLDS
Yon typed `אם נתקעים קראו למורה` (imperative) on T1_M7's stuck line; it was applied as
`אם נתקעים קוראים למורה.` and queried. **Yon confirmed: "you are correct, use 'קוראים'."**
A1 (plural impersonal, never imperative) stands with **no exception**. Precedent for future rounds:
an isolated imperative in Yon's own edit text is a typing slip — normalize it to the impersonal form
and say so, rather than treating it as a style change.

## Processed feedback ledger
| Date learned | Feedback files |
|---|---|
| 2026-08-04 (4th run) | feedback_2026-08-04_1429 · _1435 · _1442 · _1443 · _1446 · _1451 · _1451_2 · _1452 … _1452_9 (16 saves; _1452_9 is the superset) |
| 2026-08-04 (3rd run) | feedback_2026-08-04_1302 · _1312 · _1322 (_1322 = byte-identical re-save) |
| 2026-08-04 (2nd run) | feedback_2026-08-04_0110 · _0111 · _0111_2 · _0113 · _0114 · _0120 |
| 2026-08-04 | feedback_2026-08-03_2351 · feedback_2026-08-03_2351_2 · feedback_2026-08-03_2357 · feedback_2026-08-04_0007 · feedback_2026-08-04_0025 |
| 2026-08-03 | feedback_2026-08-03_2232 · feedback_2026-08-03_2305 |
| 2026-07-13 | feedback_2026-07-05_2141 · feedback_2026-07-08_1726 · feedback_2026-07-08_1749 · feedback_2026-07-08_1749_2 · feedback_2026-07-08_1755 |

## Changelog
- **2026-08-04 (approved sweeps)** — **X3 thinning applied**: attribution kept on the first pin mention
  per block, 101 repeats removed across 31 files (254 first-mentions kept, 0 doubled blocks remain).
  **V5 sweep evaluated → NO-OP**: the flagged "wiring chains" were figure legends (compact chain is
  correct there) and the remaining prose chains are a file path and a state sequence. V5's scope
  sharpened to prose/stuck-box lines only.
- **2026-08-04 (learn run 4)** — 3 new rules: **X3** (Arduino pins carry "של הארדואינו" — CONFIRMED,
  312 swept, incl. 40 refs hidden inside inline markup; documents the regex-backtracking hazard),
  **W7** (no abstract concept-framing — Yon deleted the קלט→החלטה→פלט box *and* its lede sentence),
  **V5** (multi-part technical lines become stacked rows — 3 explicit requests, FIRM). **W6 → FIRM**
  (3rd instance: category labels are chrome too). **T1** gained a 5th instance. **V4** gained the
  best-source procedure: extract the real part from the Fritzing SVG as vector (`find_part.js` /
  `extract_part.js`) — a hand-drawn imitation misled about leg count.
- **2026-08-04 (rulings + ohm sweep)** — Yon ruled on both open items: (1) **A1 holds, no exception** —
  his imperative `קראו` was a slip, normalize to `קוראים`; (2) **"use the 10kΩ format"** → X2 extended to
  resistance and swept: 141 prose instances across 29 files → `220Ω` / `10kΩ`, with the 27 `<pre>`
  ASCII-panel instances deliberately preserved (column alignment). Bidi verified by render.
- **2026-08-04 (learn run 3)** — 4 new rules: **V4** (first encounter with a part or board feature gets a
  labelled picture — 5 explicit requests, FIRM, with a clear sweep candidate: buzzer/HC-SR04/motors/L298N/
  line-sensors/soldering-iron have none), **W6** (header lede states the action only, bold), **P3**
  (background explanation inside a step goes in parentheses), **X2** (voltage written `5V`, CONFIRMED —
  81 sites swept). **W3 → FIRM** and broadened from "everyday verbs" to "the plainer, more concrete word"
  (+2 examples, incl. the LED-verb convention להידלק). **T1** gained a 4th example. Logged an **open
  conflict**: Yon's imperative `קראו` vs rule A1 — applied as impersonal, awaiting his ruling. Also
  surfaced: resistor-unit notation has 7 variants (220 אוהם/220 Ω/220Ω/10 קילו-אוהם/10 קΩ/10 kΩ/10kΩ) —
  needs his decision before any sweep.
- **2026-08-04 (T1 sweep)** — Yon approved the T1 sweep: 13 `קוראים למורה לעזרה.` → `קוראים למורה.`
  across 13 cards in P1/P3/P4. Verified 0 leftovers, 9 protected soldering `תמיד` lines intact,
  informational tails untouched. **T1 → CONFIRMED.**
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
