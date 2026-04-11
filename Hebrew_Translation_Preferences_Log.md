# Hebrew Translation Preferences Log

This file captures the learned patterns for translating project content from English to Hebrew. It is the primary source of truth for the `hebrew-translation-reviewer` agent and for any future Hebrew drafting pass.

Each pattern has:
- A short **name** (for citation in reviewer proposals)
- A 1-line **rule**
- A **why** note (the motivation, often with a specific past incident)
- 1–3 **before → after** examples pulled from real edits on this project

Patterns are organized by category: verb form, phrasing, lexical choices, visual/markup, prose tightening, workflow.

**Evidence base:** All patterns below were extracted from Yon's edit requests during the 2026-04-11 Hebrew review pass of reference cards R1-R5 (`Arduino_Projects/Project_1_Light_Signals/reference_cards_he/`). The log is bootstrapped from a single session — patterns will get stronger evidence as more Hebrew content goes through review. Until then, a pattern with one past example should be treated as *suggestive*, not as established.

---

## Category A — Verb form and voice

### Pattern A1 — Plural impersonal verb form (לשון סתמית)

**Rule:** For instructional prose, use plural impersonal verbs (לוקחים, מחברים, מסתכלים, בודקים, מעלים, קוראים). NOT imperative masculine (קח, חבר, הסתכל), NOT imperative plural (קחו, חברו).

**Why:** Gender-neutral, non-commanding, matches a non-authoritarian pedagogical tone. Imperatives feel ordered; plural impersonal feels like shared practice — "this is what we do here." This is Yon's explicit preference for the Agourim student population where directive language can trigger oppositional responses.

**Examples:**
- `חבר את הלד לרגל 9` → `מחברים את הלד לרגל 9`
- `הסתכל על החיווט` → `מסתכלים על החיווט`

### Pattern A2 — First-person plural inclusive framing for meta-guidance

**Rule:** When stating reasons, rules, or meta-guidance (why a rule exists, what a discipline accomplishes), prefer first-person plural (עוזרים לנו, עבורנו, שלנו) over second-person plural (עוזר לכם, עבורכם, שלכם).

**Why:** Creates a "we are in this together" inclusive tone rather than a "teacher instructs student" tone. The "we" includes student, teacher, and Claude Code as co-participants in the same practice.

**Examples:**
- `(א)(ב)(ג) זה לא אופציונלי. זה עוזר לכם לחשוב על הבעיה לפני שקלוד קוד עונה, וזה עוזר לקלוד קוד לתת לכם תשובה שימושית.`
- → `(א), (ב) ו-(ג) אינם סתם אופציות. הם עוזרים לנו לחשוב על הבעיה לפני שקלוד קוד עונה, ועוזרים לקלוד קוד להגיע לתשובה שתהיה שימושית עבורנו.`

### Pattern A3 — Prefer hif'il when the action is causative/transitive

**Rule:** When the verb describes causing, projecting, or making-visible an action (read aloud, make shine, declare), use hif'il binyan, not kal.

**Why:** Precision. Kal יקרא = "will read" (silently, to self). Hif'il יקריא = "will read aloud / will make [someone] read" (to another). For the Channel B scenario where Claude Code narrates a task card to a student, יקריא is the correct verb.

**Examples:**
- `קלוד קוד יקרא את תוכן הכרטיסייה` → `קלוד קוד יקריא את תוכן הכרטיסייה`
- `שיקראו לכם את המשימה` → `שיקריאו לכם את המשימה`

### Pattern A4 — Distinguish נפעל passive from פעל active

**Rule:** Use the active form (לגעת, להתחבר) when the subject is performing the action; use the passive/reflexive נפעל form (להיגע, להתחבר) only when the subject is receiving the action.

**Why:** Easy confusion. להיגע = "to be touched" (receiving); לגעת = "to touch" (performing). Instructional text almost always wants the active.

**Examples:**
- `הן אף פעם לא צריכות להיגע ישירות אחת בשנייה` → `הן אף פעם לא צריכות לגעת ישירות אחת בשנייה`

---

## Category B — Lexical choices

### Pattern B1 — Adjectival form for "starter / initial / beginning"

**Rule:** Use the adjective התחלתי / התחלתיים for "initial / starter / beginning" when modifying a noun. Do NOT use the present-tense participle מתחיל / מתחילים in this role.

**Why:** מתחיל is a present-tense participle meaning "[he] is-beginning," which is ambiguous as a modifier — "code that is-beginning" reads strangely. The adjective התחלתי unambiguously means "initial / of-the-beginning."

**Examples:**
- `קובצי קוד מתחילים של גרסה 2` → `קובצי קוד התחלתיים של גרסה 2`
- `הקוד המתחיל` → `הקוד ההתחלתי`
- `אין קוד מתחיל` → `אין קוד התחלתי`

### Pattern B2 — Protocol and process nouns: prefer hif'il-derived gerund

**Rule:** For nouns naming a pedagogical state-of-being (stuckness, falling behind, catching up), prefer the hif'il-derived gerund (הִ...וּת form) over the kal action noun (ה-...-ה form).

**Why:** The hif'il gerund captures the state/condition more precisely than the kal action noun. "היתקעות" (being stuck) is a student condition; "תקיעה" (sticking/insertion) has mechanical non-pedagogical connotations.

**Examples:**
- `פרוטוקול התקיעה` → `פרוטוקול ההיתקעות`

### Pattern B3 — Prefer natural Hebrew verbs over English-derived verbs

**Rule:** For actions that have a natural Hebrew verb, prefer it over a literal translation from English.

**Why:** Literal translations from English produce Hebrew that reads as "translated" rather than native. A LED "lights up" naturally renders יאיר (shines) in Hebrew; ידלוק (burns/ignites) is technically correct but sounds archaic/combustion-related.

**Examples:**
- `הלד ידלוק חזק מאוד לשנייה-שתיים` → `הלד יאיר חזק מאוד לשנייה-שתיים`

### Pattern B4 — Unified vocabulary: גרסה for tier AND Claude Code level

**Rule:** Use `גרסה` as the single word for BOTH the student-work tier (גרסה 1/2/3 = Tier 1/2/3) AND the Claude Code Channel A level (גרסה 2/3 = Level 2/3). Do NOT split into רמה/גרסה.

**Why:** Simpler student vocabulary. The two axes are disambiguated by context (Channel A גרסה X = Claude Code level; project גרסה X = tier). Where both appear in the same sentence, phrase explicitly — e.g., `ערוץ A - בגרסה 3 - דיאלוג חופשי`.

**Examples:**
- `(רמה 2)` in a Channel A section header → `(גרסה 2)`
- `ערוץ A רמה 3` → `ערוץ A גרסה 3` (or phrased as `ערוץ A - בגרסה 3 - דיאלוג חופשי`)

---

## Category C — Phrasing and idioms

### Pattern C1 — Avoid word-for-word calques of English idioms

**Rule:** When the English source uses an idiom, compound construction, or verbal noun phrase, do NOT translate it word-for-word. Prefer the natural Hebrew phrasing even if it is structurally different.

**Why:** Direct translations from English produce awkward double-markers (e.g., redundant "too"), unnatural verb objects, and mechanical descriptions of things Hebrew would express implicitly.

**Examples:**
- "you will hear the teacher say X" → NOT `תשמעו את המורה אומר X` → `המורה יאמר X`
- "too low to harm" → NOT `נמוך מדי מכדי לפגוע` (double "too") → `נמוך מכדי לפגוע`
- "fix before uploading anything" → NOT `מתקנים לפני שמעלים שום דבר` → `קודם כל מתקנים את זה`
- "stop the clicks" → NOT `עוצרים את הלחיצות` → `עוצרים`

### Pattern C2 — Section titles: include the subject; trim connectives

**Rule:** Section titles should be standalone and scannable. Include the explicit noun subject; trim narrative connectives like "of / for / regarding."

**Why:** A title that reads as a fragment (e.g., `איזה לאיזו אבן דרך` — "which to which milestone") is confusing because the subject is omitted. Adding the explicit subject (`איזה קוד לאיזו אבן דרך` — "which code to which milestone") restores clarity.

**Examples:**
- `קובצי הקוד של גרסה 1 — איזה לאיזו אבן דרך` → `קובצי הקוד של גרסה 1 — איזה קוד לאיזו אבן דרך`

### Pattern C3 — Masculine default is acceptable when the specific referent is male

**Rule:** When the referent is a specific male teacher (Yon), use masculine verb/pronoun forms (`המורה יגיע`, `המורה יאמר`). Do NOT twist into awkward gender-neutral constructions for a specific known-male referent.

**Why:** Hebrew grammar requires gender. Awkward gender-neutral phrasings in contexts with a specific known referent are worse than using the grammatically-correct masculine form. This rule applies ONLY to project-specific materials referring to Yon directly; universal pedagogical writing for an unspecified teacher should use inclusive phrasing.

**Examples:**
- `המורה יגיע אליכם` (Yon is male — masculine is correct here)

---

## Category D — Prose tightening

### Pattern D1 — Cut filler, moralizing, and preachy add-ons

**Rule:** Remove filler phrases, rambling asides, moralizing qualifiers, and dramatic closers. Hebrew pedagogical writing is more concise than English; English padding does not translate.

**Why:** Hebrew readers (especially the Agourim student population) read shorter, more direct prose as *more* respectful, not less. Over-explanation reads as condescension or nagging.

**Examples of what to cut:**
- `עבודה שקטה, עבודה מועילה` — rhyming preachy add-on
- `(לא צריך כוס ולא דגל — פשוט קוראים)` — rambling aside about infrastructure
- `לא מאשימים אתכם בחיווט לא נכון` — moralizing qualifier
- `לחווט לא נכון זה חלק מלמידת ארדואינו, לא אסון` — dramatic closer with negation
- `מרימים יד או אומרים את השם של המורה. המורה יגיע אליכם` — mechanical description of how to call someone

### Pattern D2 — Prefer short aphorisms over long explanations

**Rule:** When restating an important idea at the close of a section, prefer a short memorable aphorism over a long explanatory clause.

**Why:** Easier to remember, more dignified, matches the rhythm of Hebrew pedagogical writing. Students are more likely to internalize a short phrase than a long sentence.

**Examples:**
- `תקיעה זאת לא כישלון — זה חלק נורמלי מלמידת ארדואינו, ולגלות במה בדיוק תקועים זה מידע שימושי לשלב הבא.` → `להיתקע זה לא להיכשל — זהו חלק בלתי נפרד מלמידה.`

### Pattern D3 — Prefer declarative statements over procedural descriptions

**Rule:** State the outcome directly rather than describing the action that leads to it.

**Why:** "עוצרים את הלחיצות" = "stop the clicks" — describes the physical action. "עוצרים" = "stop" — states the outcome. The outcome is what the reader needs to internalize; the action is implicit.

**Examples:**
- `עוצרים את הלחיצות. מסתכלים על החיווט.` → `עוצרים. מסתכלים על החיווט.`

---

## Category E — Visual / markup conventions

### Pattern E1 — Replace Latin-letter markers with Hebrew-native symbols

**Rule:** When a marker is meant to be read (a checkmark, a bullet, a status glyph), prefer Unicode symbols over Latin letters.

**Why:** Latin letters embedded in Hebrew running text are visually jarring and make the text feel less native. Unicode symbols are language-neutral and scan cleanly inside Hebrew RTL flow.

**Examples:**
- `מסמנים V בכרטיסייה` → `מסמנים ✓ בכרטיסייה`

### Pattern E2 — Reference card IDs: circled inline, no parentheses

**Rule:** When referencing another reference card by number (R1, R2, ...), wrap the ID in `<span class="r-ref">` which renders a small circle matching the top-corner badge style. Do NOT surround the circled ID with parentheses — the circle already acts as visual enclosure, and `(R2)` creates a paren-circle-paren stack that reads poorly.

**Why:** Visual coherence — the student sees the same circled "R2" glyph whether it appears in the corner badge or inline in body text.

**Examples:**
- `בודקים את כרטיסיית החיווט (R1)` → `בודקים את כרטיסיית החיווט <span class="r-ref">R1</span>` (no parens)
- `(ראו R3)` — OK to keep parens because they wrap the phrase `ראו R3`, not just the circle

### Pattern E3 — Card-ID top-corner badge: position opposite the heading

**Rule:** The card-ID corner badge sits in the physical corner opposite the heading. Hebrew RTL cards → top-**left** corner (heading flows from the right, badge in empty space on the left). English LTR cards → top-**right** corner.

**Why:** The badge should sit in visually-empty space, not collide with the heading. Empty-corner-opposite-heading is the consistent rule that produces this under both reading directions.

**Examples:**
- Hebrew `R1_wiring_reference_he.html`: `position: absolute; top: 6mm; left: 6mm;` ✓
- English `R1_wiring_reference.html` (pending backport): currently top-left, should move to top-right

### Pattern E4 — Arial-first font stack for Hebrew body text

**Rule:** Hebrew body text uses the font stack `Arial, 'Segoe UI', -apple-system, 'Noto Sans Hebrew', sans-serif`.

**Why:** Arial has more reliable Hebrew glyphs across Windows versions than Segoe UI. Segoe UI's bold Hebrew can fall back to synthesized bold (browser thickens regular glyphs), which looks visibly different from regular Hebrew.

### Pattern E5 — No monospace font on Hebrew text

**Rule:** Do NOT apply `font-family: monospace` (or Consolas, Courier New) to elements containing Hebrew text. Monospace is only for ASCII code/paths/filenames, which must be wrapped in `direction: ltr; unicode-bidi: isolate;` so they render LTR inside the RTL document.

**Why:** Monospace fonts do not have Hebrew glyphs, so applying them makes Hebrew fall back to a different font that looks visibly mismatched to the surrounding Arial text.

### Pattern E6 — No box-level `font-weight: bold` on `.key` or similar callout blocks

**Rule:** Callout boxes containing Hebrew text should NOT set `font-weight: bold` on the whole box. Individual `<strong>` tags inside the box still bold for emphasis; running text stays regular weight.

**Why:** Arial Bold for Hebrew on some Windows systems falls back to synthesized bold (browser thickens regular glyphs), which looks visibly different from regular Hebrew. Box-level bold amplifies this across the whole callout.

---

## Category F — Workflow

### Pattern F1 — Clean obvious fast-typing typos in user Hebrew without asking

**Rule:** When Yon provides Hebrew replacement text in a message, silently fix obvious typos (missing spaces, letter-swaps, double letters, unshifted punctuation) before inserting. Flag the cleaning briefly at the end of the response.

**Why:** Fast typing on phone/keyboard produces predictable errors. Asking about each one is noise and slows the review loop. The author has already moved on to the next idea.

**Examples observed this session:**
- `כשקשהלהתקדם` → `כשקשה להתקדם` (missing space)
- `שקלוטד` → `שקלוד` (inserted ט)
- `קןד` → `קוד` (ן instead of ו — shifted by one key)
- `(א)ת(ב) ו (ג)` → `(א), (ב) ו-(ג)` (normalized punctuation/connectives)

---

## Category G — Claude Code–specific terminology

### Pattern G1 — Channel / ערוץ

**Rule:** Claude Code's dual-channel roles are translated as ערוץ A (Channel A / pair programmer) and ערוץ B (Channel B / scaffolded tutorial). The Latin A and B are kept (do NOT translate to א and ב, which would collide with the metacognitive discipline markers).

**Why:** The (א)(ב)(ג) markers inside the Channel A Level 2 discipline already use Hebrew letters. Using A/B for the channel name keeps the two axes visually distinct.

### Pattern G2 — Metacognitive discipline markers (א)(ב)(ג)

**Rule:** The three-field Channel A Level 2 discipline uses the first three Hebrew letters in parentheses: `(א)`, `(ב)`, `(ג)`. When listing them together, separate with commas and use a hyphenated connective: `(א), (ב) ו-(ג)`.

**Why:** The (א)(ב)(ג) convention is established from the R3 reference card and must stay consistent across all subsequent Hebrew materials (H.3 task cards, H.5 HTML tutorial, H.6 Channel B scaffold).

---

## Patterns observed but not yet established (single example only)

The following are candidate patterns that have appeared once but have not yet been reinforced by a second occurrence. The reviewer should flag drift from these as **low confidence** until a second example confirms them.

- **Softer negation**: prefer `אינם סתם אופציות` over `זה לא אופציונלי` (declarative-positive with soft negation over bare negation). Single example: R3 key rule rewrite.
- **Replace "normal" / "not a disaster" with positive inclusion framing**: `לא אסון` and `חלק נורמלי מלמידה` were cut in favor of `חלק בלתי נפרד מלמידה`. Single example: R2 important-block rewrite.

---

## How to add a new pattern to this log

When Yon makes a new Hebrew edit that implies a pattern:

1. Check if the edit matches an existing pattern in this log. If yes, append the new example to that pattern.
2. If no existing pattern fits, add a new entry under the appropriate category.
3. Mark the pattern as **single-example / low confidence** until a second occurrence reinforces it.
4. Update `MEMORY.md` if the pattern introduces new terminology or new conventions that downstream agents need to know about.

The reviewer agent reads this file every time it runs, so keeping it up-to-date directly improves the agent's review quality.
