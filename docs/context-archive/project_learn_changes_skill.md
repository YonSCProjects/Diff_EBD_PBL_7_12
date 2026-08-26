---
name: learn-changes-skill
description: "The card-review loop skills: /apply-feedback + /learn-changes + Card_Editing_Preferences_Log.md — how Yon's console edits become applied changes and durable authoring rules"
metadata:
  node_type: memory
  type: project
  originSessionId: 4f98ca88-5db7-42fe-97d8-4266922384ce
  modified: 2026-08-04T12:30:14.351Z
---

**The loop (Yon's working rhythm, live since 2026-08-03):**
review in the console → **"apply changes"** (`/apply-feedback`) → **"learn the changes"** (`/learn-changes`)
→ approve sweeps as rules firm up → **"איפוס הכל"** in the console → repeat.

**Three artifacts (all in-repo, versioned):**
- **`.claude/skills/apply-feedback/SKILL.md`** — the apply contract: newest feedback file, FNV-1a
  `sourceHash` check, stale-cache detection, text-mode edit application (runtime injects `data-dc-tpl`
  attrs absent from source → match on text), comment-judgment precedents, rebuild + ONE commit.
- **`.claude/skills/learn-changes/SKILL.md`** — ingests unlearned feedback, dedups by
  (card, before→after), grep-based counterexample analysis, TENTATIVE→FIRM→CONFIRMED ladder,
  proposes sweeps but NEVER auto-applies, protected-motif guard.
- **`Card_Editing_Preferences_Log.md`** (repo root) — the rules. `dc_design_spec.md` points authors here.

**Rule state as of 2026-08-04, end of day** (read the log for full text/examples/sweep records):
**CONFIRMED (swept program-wide)** — T1 (no reassurance tail on stuck lines; 13), T3 (no "עוברים על
השלבים…" intro chrome; 34), X1 (pins = `חיבור דיגיטלי N`; `רגל` only for component legs; 313),
X2 (units no-space symbol form `5V` / `220Ω` / `10kΩ`; 81 + 141), X3 (pins carry `של הארדואינו`; 312,
then thinned to **first-mention-per-block**, 101 repeats removed), P2 (no comma before ו').
**FIRM** — W2 (observation not explanation), W3 (the plainer, more concrete word), W6 (header lede =
the action only, bold), W7 (**no abstract concept-framing** — Yon deleted the קלט→החלטה→פלט box *and*
its lede sentence), P1 (minimal commas), V1 (real figures; captions in HTML never baked into the image),
V2 (annotations span the full extent of what they mark), V3 (a figure swap → sweep the whole card),
V4 (**first encounter with a part gets a picture** — extract the real part from the Fritzing SVG as
vector), V5 (multi-part technical lines become stacked rows — **prose only**, not legends/paths/sequences).
**TENTATIVE** — T2, W1, W4, W5, P3.

**Sweep hazards learned (both cost real debugging):** (1) a lookahead guard like
`(חיבור דיגיטלי \d+)(?! של הארדואינו)` **backtracks** — `\d+` matches just the `1` of `13` and slips
through, corrupting two-digit pins on a re-run; always anchor with `\d+(?!\d)`. (2) A text-pattern grep
can't tell a legend from a sentence — **look at the surrounding element before sweeping** (the V5 sweep
turned out to be a no-op for exactly this reason). Also: `<pre>` ASCII panels are column-aligned and must
be excluded from every text sweep.

**Figure tooling now in-repo:** `tools/card_figures/` — `find_part.js` (list Fritzing parts + bboxes),
`extract_part.js` (pull one part into a standalone vector SVG — the preferred source for a component
illustration), `holes.js` (measure a breadboard's hole grid so overlays land on real coordinates).

**Hard-won gotchas:** (1) the console's **"איפוס הכל"** button did not exist until 2026-08-04 — I added
it (`review_console.html`, wipes all `rvw:*` after double confirm); before that every save re-exported
old edits. (2) Yon often keeps reviewing AFTER saying "apply" — always re-check for a newer
`feedback_*.json` before declaring a round done (one edit was nearly missed this way). (3) Figure
overlays: measure the image's hole grid computationally (scratchpad `holes.js` — darkness profile)
instead of eyeballing percentages.
