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

### Pattern A2 — First-person plural inclusive framing for procedural meta-guidance

**Rule:** When stating **rules, disciplines, or procedural meta-guidance** (why a rule exists, what a discipline accomplishes, how a practice is meant to work), prefer first-person plural (עוזרים לנו, עבורנו, שלנו) over second-person plural (עוזר לכם, עבורכם, שלכם).

**Scope and exception:** This pattern applies to *procedural* meta-guidance only — rules, disciplines, the "why" behind a practice, explanations of workflow logic. It does **NOT** apply to *personal* orientation openers — the warm second-person framing that positions a specific milestone or project for a specific student (e.g., `זו אבן הדרך הראשונה שלכם בתוכנית הארדואינו` in the opening why-block of a first-milestone task card). In those personal-orientation contexts, second-person possessive (שלכם) adds warmth and ownership and should be kept. The rule of thumb: if the sentence could be spoken to any student in any workshop in exactly the same form, use first-person plural inclusive; if it's addressed to a specific student in a specific moment of their journey, second-person is appropriate.

**Why:** First-person plural in procedural meta-guidance creates a "we are in this together" inclusive tone — student, teacher, and Claude Code as co-participants in the same practice. But in personal orientation contexts (opening of a first-milestone card, recognition lines, direct teacher-to-student address), the second-person warmth is exactly what the moment needs. Don't strip warmth where warmth is the point.

**Examples:**

*Apply the rule (procedural meta-guidance):*
- `(א)(ב)(ג) זה לא אופציונלי. זה עוזר לכם לחשוב על הבעיה לפני שקלוד קוד עונה, וזה עוזר לקלוד קוד לתת לכם תשובה שימושית.`
- → `(א), (ב) ו-(ג) אינם סתם אופציות. הם עוזרים לנו לחשוב על הבעיה לפני שקלוד קוד עונה, ועוזרים לקלוד קוד להגיע לתשובה שתהיה שימושית עבורנו.`

*Do NOT apply the rule (personal orientation):*
- `זו אבן הדרך הראשונה שלכם בתוכנית הארדואינו.` — Yon kept `שלכם` here during T1_M1 review on 2026-04-12. The sentence is the opening of the why-block of a first-ever-milestone card, addressing a specific student at a specific moment. Stripping `שלכם` to `זו אבן הדרך הראשונה בתוכנית הארדואינו` was proposed and rejected: the reduced form is more "clinical" and loses the welcoming tone that belongs in this specific context.

### Pattern A5 — Permissive `אפשר ל-` for optional/backup tasks vs plural impersonal for primary instructions

**Rule:** For **optional, backup, or fallback tasks** (the "try this while you wait" alternatives), use the permissive construction `אפשר ל-` ("it is possible to / one may") rather than the plural impersonal verb (`מתחילים ל-`, `עושים את`). Primary instructions (the main task workflow) keep the plural impersonal form per pattern A1.

**Why:** The plural impersonal form (pattern A1) reads as "this is what we do here" — a shared practice the student is expected to follow. That register is correct for primary milestone instructions, but wrong for backup tasks, which the student is being *offered*, not *told*. `אפשר ל-` signals "this is available if you want it" — respecting student autonomy in the fallback context. Mixing A1 plural impersonal with backup tasks reads as "you must do the backup task" which contradicts the whole point of a backup task being an autonomous waiting activity.

**Examples:**

*Backup task — permissive form:*
- `מתחילים במשימת הגיבוי של מיון הנגדים שעל השולחן` → `אפשר להתחיל במשימת הגיבוי` (T1_M1 stuck-block revision, 2026-04-12)

*Primary task — plural impersonal (pattern A1 still applies):*
- `מחברים את הארדואינו למחשב` — primary instruction, stays plural impersonal
- `פותחים את Arduino IDE` — primary instruction, stays plural impersonal

**Interaction with pattern A1:** The reviewer agent should NOT flag `אפשר ל-` constructions as A1 violations. A1 and A5 cover different registers: A1 is for primary workflow instructions; A5 is for the offered alternatives.

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

**Why:** Literal translations from English produce Hebrew that reads as "translated" rather than native. A LED "lights up" naturally renders יאיר (shines) in Hebrew; ידלוק (burns/ignites) is technically correct but sounds archaic/combustion-related. Similarly, verbs with implicit force/violence connotations should be replaced with their gentler, task-appropriate counterparts when the physical action is delicate.

**Examples:**
- `הלד ידלוק חזק מאוד לשנייה-שתיים` → `הלד יאיר חזק מאוד לשנייה-שתיים`
- `נועצים את הלד בברדבורד` → `מכניסים את הלד לברדבורד` (T1_M3 review, 2026-04-12 — `נועצים` carries a forceful "staking/piercing" connotation that is alarming for EBD students handling delicate components; `מכניסים` is the standard Israeli maker-community verb for inserting components into a breadboard and matches the gentle physical action). The same logic applies to done-when state: `הלד נעוץ בברדבורד` → `הלד מוכנס לברדבורד`.
- Root-level preference extends to title/heading position: `מדליקים את הלד` → `מאירים את הלד` (T1_M4 review, 2026-04-12 — the ד.ל.ק root in `מדליקים` is the same family as the flagged `ידלוק`; א.ו.ר root in `מאירים` is the family of the preferred `יאיר`. When the English heading says "light up the LED," the Hebrew heading should use the א.ו.ר-root form to match body-text consistency).
- Extends to nif'al passive-action form: `לדים נדלקים` → `לדים מאירים` (T2_M2 + T1_M8 review, 2026-04-12 — `נדלקים` is a nif'al passive-action from the same ד.ל.ק root family, describing the LED-ignition event. `מאירים` is the hif'il participial from א.ו.ר and is the natural Hebrew verb for LED light-up events).
- State-descriptor `דולק`/`כבוי` present-tense adjective is NOT part of this pattern. `דולק` in the sentence "when LED 1 is on" is a state descriptor, not a verb action; it is the natural Israeli electronics vocabulary and should stay. Pattern B3 targets *verb actions* (future tense, present participle verbs for ignition/illumination events), not state descriptors. Keep `דולק`/`כבוי` for on/off states.
- Extends to verb choice (not just LED): `נועצים` is a forceful verb to avoid for delicate components; similar forceful or causative-chain verbs should prefer their direct-state alternatives. Example: `החזקת הכפתור לחוץ גורמת לתבנית לרוץ מהר יותר` → `כשהכפתור לחוץ — התבנית רצה מהר יותר` (T2_M4 review, 2026-04-12 — the causative chain `גורם ל-X לרוץ` is English "makes the pattern run" calqued into Hebrew; natural Hebrew uses the conditional-consequent form).

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
- "the file is under `ino_files/...`" (path navigation) → NOT `הקובץ נמצא תחת ino_files/...` → `הקובץ נמצא בתוך ino_files/...` (T1_M2 review, 2026-04-12 — `תחת` is a spatial "below/beneath" preposition in Hebrew; natural file-system navigation uses `בתוך` "inside")
- "first Upload click worked" (celebrating a procedural action) → NOT `הלחיצה הראשונה על Upload עבדה` → `ההעלאה הראשונה עבדה` (T1_M2 review, 2026-04-12 — English "click" is a noun-ified gesture; Hebrew celebrates the outcome, not the physical action)
- "legs land in different rows" (aviation/spatial metaphor for component placement) → NOT `הרגליים נוחתות בשורות שונות` → `כל רגל נמצאת בשורה שונה` (T1_M3 review, 2026-04-12 — "landing" is an English metaphor for component insertion that does not carry into Hebrew electronics vocabulary; describe the spatial outcome directly)
- "Notice something" / "Take a second to notice that" (English attention-drawing with placeholder object) → NOT `שמים לב לדבר` / `שווה לשים לב ש-` → `שמים לב:` or `כדאי לשים לב:` followed by the content as direct declarative (T1_M4, T1_M6 reviews, 2026-04-12 — Hebrew attention-drawing does not need an object noun filler; colon-predicate form reads cleanly).
- "the most common cause is that X" (English copula-relative-clause construction) → NOT `הסיבה הנפוצה ביותר היא ש...` → `הסיבה הנפוצה ביותר: ...` (T1_M8 review, 2026-04-12 — Hebrew prefers the colon-predicate over the English copula-relative-clause; the shorter form is also more scannable in stuck-block safety contexts).
- "you did this yourself" (celebrating with vague demonstrative) → NOT `ועשיתם את זה בעצמכם` → `ועשיתם אותה בעצמכם` (where the feminine pronoun back-references a specific feminine antecedent like `הנדסת חשמל`; T1_M8 celebration block, 2026-04-12 — `את זה` is a calque of English "this"; Hebrew prefers an internal-antecedent pronoun that closes the sentence's own referential loop).
- "it is normal to need help" (English infinitive-subject reassurance) → NOT `וזה נורמלי להזדקק לעזרה` → `מבקשים עזרה בלי לחשוש` (T1_M4 review, 2026-04-12 — the English infinitive-subject construction after `נורמלי` reads mechanically in Hebrew; the positive plural-impersonal form preserves the reassurance without the calque).
- "the button button" (English noun-noun compound with article) — `לוחצים על Upload` vs `לוחצים על כפתור ה-Upload` is a register choice, not a strict rule. For EBD students, explicit naming (`כפתור ה-Upload`) can aid recognition and reduce confusion; for literate contexts the compressed form (`לוחצים על Upload`) is tighter. T1_M6 review 2026-04-12 kept the explicit form for EBD clarity. Judgment call — use explicit naming when the student must identify a specific UI element.

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
- `חשוב לזכור את ההבדל` (trailing a bullet that already uses `<strong>` on both halves of the contrast) — closing-clause reminder that tells the student how important the information they just read is. If the bold markup and the reference card already encode the importance, the trailing reminder is instructive noise. Drop. (T1_M3 review, 2026-04-12 — first task-card example of this sub-type; watch for similar closers like "אל תשכחו", "חשוב להבין", "תזכרו ש-" in future drafts.)

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

## Category H — Professional/clinical register (for Ministry-facing documents)

Added 2026-04-12 based on Yon's DOCX edit of the Hebrew executive overview. This category applies specifically to professional/academic Hebrew — Ministry proposals, program descriptions, colleague-facing documents. For student-facing materials the simpler A1–A5 registers apply.

### Pattern H1 — Clinical-professional vocabulary for student experiences

**Rule:** In Ministry-facing prose, use psychological-clinical vocabulary (`הצפה`, `הימנעות`, `ויסות`) when describing student experiences. Informal emotional adjectives like `מפחידים` should be replaced with the clinical sequence — "overwhelm, fear, and avoidance."

**Why:** Clinical vocabulary signals professional awareness of the population's actual clinical profile. Ministry readers and special-education colleagues will recognize it immediately. Informal adjectives read as lay descriptions and weaken the document's authority.

**Examples:**
- `המגוון הרב והבחירה הפתוחה היו מציפים ומפחידים` → `המגוון הרב והבחירה הפתוחה מביאים להצפה, פחד והימנעות` (Hebrew overview edit, 2026-04-12)

### Pattern H2 — `קשיים` not `בעיות` for student challenges

**Rule:** Use `קשיים` ("difficulties") rather than `בעיות` ("problems") when describing student challenges or teacher experiences with the population.

**Why:** `קשיים` is warmer, more professional, and aligns with special-education discourse in Hebrew. `בעיות` has a stronger deficit-framing connotation and reads as informal. The shift parallels English editorial preferences for softer framing (Editorial Pattern 4, 5).

**Examples:**
- `שתי בעיות שנתקלתי בהן` → `שני קשיים איתם אני מתמודד` (Hebrew overview edit, 2026-04-12)

### Pattern H3 — `מענה` not `עזרה` in Ministry-facing prose

**Rule:** Use `מענה` ("response / provision") rather than `עזרה` ("help") when describing what the teacher provides to the student in formal educational contexts.

**Why:** `מענה` is the educational-system term used in Ministry documents about differentiated support; `עזרה` is colloquial. `מענה` also carries the connotation of a structured response to an identified need, which matches the differentiated-instruction framing. For student-facing materials `עזרה` remains fine (children understand it better).

**Examples:**
- `את העזרה שהוא צריך` → `את המענה לו הוא זקוק` (Hebrew overview edit, 2026-04-12)

### Pattern H4 — `אוטונומיה` not `סוכנות` for agency

**Rule:** Use `אוטונומיה` ("autonomy") rather than `סוכנות` ("agency") when describing student self-direction or empowerment.

**Why:** `סוכנות` is a direct calque of the English sociological term "agency"; it reads as translated and may not be familiar to all Ministry readers. `אוטונומיה` is the term used in mainstream Israeli educational discourse and directly maps to the program's framing (Principle 5: "structured autonomy").

**Examples:**
- `מכבדת את הסוכנות של התלמיד` → `מכבדת את האוטונומיה של התלמיד` (Hebrew overview edit, 2026-04-12, Principle 5)

### Pattern H5 — Prefer Hebraic roots over Anglicized roots where both exist

**Rule:** When a native Hebrew root and an Anglicized root both exist for the same concept, prefer the Hebraic root in professional/academic Hebrew.

**Why:** Native roots signal literacy in Hebrew's own lexicon rather than reliance on transliteration. `פיזי` is an Anglicism (from "physical"); `גשמי` is the native Hebrew root for "material / corporeal." Both mean the same thing; the Hebraic form reads as more polished.

**Examples:**
- `פיזי קודם, מופשט אחר כך` → `גשמי קודם, מופשט אחר כך` (Hebrew overview edit, Principle 3, 2026-04-12)

### Pattern H6 — `ישימה` not `ניתן ליישום` for feasibility

**Rule:** Prefer compact Hebrew adjectives (`ישימה`, `מעשית`, `בת-ביצוע`) over English-style relative-clause constructions (`ניתן ליישום`, `ניתנת להפעלה`) for feasibility claims.

**Why:** Hebrew prefers adjectival predicates where English uses "can be X'd." The adjectival form is shorter, more natural, and avoids the calque feel of the relative clause.

**Examples:**
- `חייבת להיות ישימה ולא שוחקת` (Hebrew overview Principle 9, 2026-04-12) — not `חייבת להיות ניתנת ליישום`

### Pattern H7 — Soft negation preference (PROMOTED from candidate to established)

**Rule:** Prefer positive reframes or soft negation (`אינה`, `אינו`, `אינם`) over bare negation (`לא`) in formal prose. Replace `אופציונלי` with `חיוני` where the sense is "essential" rather than merely "not optional."

**Why:** Soft negation and positive reframes read as more composed and more Hebrew-idiomatic. Bare negation with `לא` is direct but can feel like English-style contradiction.

**Examples:**
- `זה לא אופציונלי` → `אינם סתם אופציות` (R3 key-rule rewrite, 2026-04-11)
- `אינו אופציונלי עבור תלמידים עם קשיי למידה` → `הינו חיוני עבור תלמידים עם קשיי למידה` (Hebrew overview Principle 3, 2026-04-12)

**Promotion note:** This pattern had a single example in the "not yet established" section prior to 2026-04-12. The Hebrew overview edit provided a second reinforcing example (Principle 3's CRA description), which promotes it from candidate to established.

---

## Category C extensions — new calque sub-examples (added 2026-04-12)

### C1 sub-example — `גוש עבודה` → `מקטע עבודה`

**Rule:** Prefer `מקטע` (segment) over `גוש` (block) for work units in professional descriptions.

**Why:** `גוש` has a physical/chunky connotation suitable for student-facing materials; `מקטע` is more neutral/professional and fits Ministry-facing documents.

**Examples:**
- `גוש עבודה 1 / גוש עבודה 2` → `מקטע עבודה 1 / מקטע עבודה 2` (Hebrew overview session-structure table, 2026-04-12)

### C1 sub-example — `בין גושי עבודה` → `בין פרקי העבודה`

**Rule:** When referring to transitions between work segments in prose (not table headers), use `פרקים` (chapters/segments) rather than `גושים`.

**Why:** `פרקים` reads as more formal in running prose; `גושים` is better for visual/tabular contexts where chunkiness is intentional.

**Examples:**
- `הפסקת תנועה מובנית של 3 דקות בין גושי עבודה` → `הפסקת תנועה מובנית של 3 דקות בין פרקי העבודה` (Hebrew overview Principle 6, 2026-04-12)

### C1 sub-example — `אינו אופציונלי / ניתן למשא ומתן` → `קבוע`

**Rule:** For rules that are fixed and non-negotiable, prefer the compact declarative `קבוע` ("fixed") over the English-calque `לא ניתן למשא ומתן` ("non-negotiable, literally: not open to negotiation").

**Why:** `משא ומתן` in Israeli Hebrew is associated with commercial negotiations or diplomatic talks, not classroom ground rules. `קבוע` says the same thing more compactly and without the bazaar connotation.

**Examples:**
- `אלה אינם ניתנים למשא ומתן` → `כל אלה קבועים` (Hebrew overview Principle 6, established 2026-04-12)

### C1 sub-example — `לא ניתן לתזמון` → `לא אפשרי במסגרת זו`

(Placeholder — add when a second example appears.)

---

## Patterns observed but not yet established (single example only)

The following are candidate patterns that have appeared once but have not yet been reinforced by a second occurrence. The reviewer should flag drift from these as **low confidence** until a second example confirms them.

- **Replace "normal" / "not a disaster" with positive inclusion framing**: `לא אסון` and `חלק נורמלי מלמידה` were cut in favor of `חלק בלתי נפרד מלמידה`. Single example: R2 important-block rewrite.
- **`מדידה פשוטה` (simple) vs `מדידה קלה` (lightweight) — Yon prefers `פשוטה`** despite the minor "simplistic" connotation risk. Single example: Hebrew overview "איך נדע אם זה עובד" section, 2026-04-12. Note for future: if a Ministry reader flags `פשוטה` as reading simplistic, consider switching to `פשוטה ויעילה` or `מסגרת קלה` as alternatives.

---

## Category I — Cross-document terminology (propagated 2026-04-12)

### Pattern I1 — School name: `עגורים` (with ayin), not `אגורים` (with aleph)

**Rule:** The school's name in Hebrew is spelled `עגורים` (ayin-gimel-vav-resh-yud-mem), NOT `אגורים` (aleph-gimel...).

**Why:** Factual accuracy. The school is named after cranes (birds); the correct Hebrew spelling uses ayin. The aleph spelling was a transliteration artifact from the English "Agourim."

**Scope:** All Hebrew documents in the project. Propagated across 21 Hebrew files on 2026-04-12. See Editorial_Preferences_Log Pattern 15 for the cross-language equivalent.

### Pattern I2 — Navigation card (`כרטיסיית ניווט`), not task card (`כרטיסיית משימה`)

**Rule:** In all Hebrew student-facing materials and in all Ministry-facing framing, the student-facing cards are called `כרטיסיות ניווט` (navigation cards), not `כרטיסיות משימה` (task cards).

**Why:** "Navigation" emphasizes student agency and reframes the card as a map rather than an externally-imposed task. "Task" echoes a register that many EBD students have negative associations with. See Editorial_Preferences_Log Pattern 12 for the cross-language reasoning and the English equivalent "navigation card."

**Scope:** All 18 Hebrew student-facing files (14 task cards, 5 reference cards, tutorial, Channel B scaffold, Hebrew overview). Propagated 2026-04-12. English student-facing files to follow in the retroactive English pass.

---

## How to add a new pattern to this log

When Yon makes a new Hebrew edit that implies a pattern:

1. Check if the edit matches an existing pattern in this log. If yes, append the new example to that pattern.
2. If no existing pattern fits, add a new entry under the appropriate category.
3. Mark the pattern as **single-example / low confidence** until a second occurrence reinforces it.
4. Update `MEMORY.md` if the pattern introduces new terminology or new conventions that downstream agents need to know about.

The reviewer agent reads this file every time it runs, so keeping it up-to-date directly improves the agent's review quality.
