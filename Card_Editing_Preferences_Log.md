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

**Evidence:** 1 · **Counterexamples:** 13× `קוראים למורה לעזרה` survive in not-yet-reviewed cards (weak).
**Protected carve-out:** the soldering escalation **"קוראים למורה, תמיד"** (8×, P4 + R6) and every
soldering-safety "קוראים למורה" line — these are locked design motifs and are NEVER trimmed.
**Status:** TENTATIVE · **Sweep scope (if confirmed):** the 13 `לעזרה` instances + trailing
justification clauses in stuck boxes, excluding all soldering/safety contexts.

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

**Evidence:** 2 (independent cards, consistent direction) · **Counterexamples:** none in edited cards.
**Status:** TENTATIVE (strong direction — one more consistent instance ⇒ FIRM).
**Procedure:** Yon supplies the image path; copy into `task_cards_he/assets/`; the bundle build
inlines it automatically (`inlineImages`).

---

## Processed feedback ledger
| Date learned | Feedback files |
|---|---|
| 2026-07-13 | feedback_2026-07-05_2141 · feedback_2026-07-08_1726 · feedback_2026-07-08_1749 · feedback_2026-07-08_1749_2 · feedback_2026-07-08_1755 |

## Changelog
- **2026-07-13** — Log bootstrapped by /learn-changes creation: 4 seed rules (T1, T2, W1, V1) from the
  2026-07-05 + 2026-07-08 review rounds; V1 strengthened by Yon's own T1_M1 image rework.
