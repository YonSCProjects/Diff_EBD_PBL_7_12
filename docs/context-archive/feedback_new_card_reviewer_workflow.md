---
name: New navigation card reviewer workflow
description: For any new student-facing card, run pedagogical + visual reviewers in parallel on EN, then hebrew reviewer on HE, applying high+medium confidence fixes before building
type: feedback
originSessionId: e680ace2-857b-49f5-9ebd-56985d6eee86
---
When creating a new navigation or reference card for the Arduino PBL program, Yon wants the full reviewer pipeline exercised — not a skip.

**Why**: Yon explicitly asked "now lets build a navigation card [...] all the content and design reviewer agents we have to get a very good and clear and easy to follow navigation card." The reviewers exist to produce a polished card on the first pass rather than catching issues after the PDF is printed or a student is confused in session.

**How to apply**:
1. Draft the EN card from an existing card (R4_safety_reminder.html is a good structural baseline for reference cards; T1_M5 is a good baseline for task cards).
2. Run `pedagogical-card-reviewer` and `visual-design-reviewer` **in parallel** on the EN draft — one message with both Agent calls.
3. Apply high-confidence and medium-confidence proposals; flag low-confidence ones for user judgment.
4. Create the HE translation mirroring the EN structure.
5. Run `hebrew-translation-reviewer` on the HE draft against the EN source.
6. Apply high + medium confidence HE fixes.
7. Register the new card filename in `build_overview_with_cards.js` `cardOrder` at the appropriate position (R0 first, T2_M2b between T2_M2 and T2_M3, etc.).
8. Rebuild both EN+HE overview PDFs via `node build_overview_with_cards.js en` then `he`.

**Reviewer fixes worth applying by default**: family consistency (palette, footer, h-sizes), page-break guards on callout boxes, replacing "mistakes to avoid" framing with "things to check if…" (Principle 8), real-image anchor over ASCII-only diagrams, orientation strip saying "come back to this — you do not need to memorise it."

**Reviewer GUARDS that suppress over-generation (proven on Project 3, 2026-06-30).** These reviewers over-generate badly when run naked — Project 2 got 271 findings / 33 real (87% noise). Project 3 ran the same 3 reviewers × 18 cards (56 jobs) as a Workflow but baked **hard guards** into every reviewer prompt and got **62 findings / ~50 real** — the noise mostly vanished. Reusable guard block for Projects 4–8 review workflows:
- "The V1/V2/V3 card-id is a VERSION/tier badge, NOT a checkmark — never propose changing it to ✓." (reviewers' #1 false positive)
- "These cards deliberately MIRROR the already-approved Project N-1 cards — do NOT propose stylistic rewrites of shared patterns; only flag what is genuinely wrong for THIS card."
- "The canonical pin map is FIXED: …"; "ASCII `wiring-block` + `living-placeholder` (no `<img>`) is intentional — Fritzing SVGs aren't generated yet, don't flag missing images."; any project-specific intentional quirk (e.g. P3's "a big distance reading like 999 is normal, not a bug").
- "HIGH/MEDIUM only, hard cap 5 findings/reviewer, empty array if clean."
Also force a **structured findings schema** ({severity, location, issue, fix}) so triage is mechanical, and run **generate → review → guarded-apply as three separate Workflows** (one agent per file in each) so you stay in the loop between phases. One Hebrew nuance the reviewers get BACKWARDS: a within-card "consistency" finding may point toward the *dispreferred* form — re-check against [[project_hebrew_reviewer_agent]] Pattern B3 (LED light-up = מאיר, not נדלק) before applying its direction.
