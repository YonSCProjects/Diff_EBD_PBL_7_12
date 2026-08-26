---
name: card-review-console
description: "In-browser review console for the Hebrew task cards (auto-discovers every project, P1-P8) — how Yon reports feedback and EXACTLY how to apply review_feedback/*.json when he says 'apply the feedback'"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4f98ca88-5db7-42fe-97d8-4266922384ce
  modified: 2026-08-03T20:53:39.814Z
---

**What.** Built + committed `a1cf4b3` (2026-07-05, pushed via this /save): a local review console so Yon can review all **55 Hebrew task cards** (P1–P4) and report wording/design corrections with zero location-typing. Files at repo root: `review_server.js` (dep-free node server, 127.0.0.1:8765, serves repo root; `GET /api/cards` manifest; `POST /api/save-feedback`), `review_console.html` (RTL UI: עיון/עריכה/הערה modes, in-place contenteditable fixes, numbered comment pins, per-card+global notes, done-tracking, multi-day localStorage persistence under `rvw:*`), `start_review.bat` (double-click launcher). Verified 27/27 E2E checks by puppeteer. Scope = task cards only (ref cards/posters excluded — extend the glob in `listCards()` to add them).

**SCOPE IS AUTOMATIC, NOT P1–P4 (verified 2026-08-25).** `listCards()` walks every
`Arduino_Projects/Project_*/task_cards_he/*.html` with no project filter, so the console lists
whatever exists at the time — 130 HE task cards across P1–P8 today, not the 55 it started with.
Nothing needs changing to review a new project's cards; they appear as soon as the files do.

**IT IS A WORDING TOOL — image feedback has no anchor.** `edits[]` bind to text blocks
(`beforeHTML`/`beforeText` + `cssPath`); there is no way to click a region of a figure. Feedback
about an illustration therefore goes in the free-form `cardNote` (per card) or `globalNotes`, and
lands as prose for judgment rather than a mechanical replacement. The cards do render their
figures in the console, so it is still the right place to *judge* them — just not to point at
them. Useful image notes name the figure (its filename or "the figure at step 4"), what is wrong,
and what it should show instead.

**THE APPLY CONTRACT — when Yon says "apply the feedback":**
1. Read the NEWEST `review_feedback/feedback_*.json` (a matching `.md` is the human-readable twin).
2. Per edit: `applyBy:"html"` → `beforeHTML` is a **byte-exact substring** of the source file → Edit it to `afterHTML` (if >1 occurrence, disambiguate with `contextBefore/After`; whitespace-collapse retry allowed EXCEPT when `preserveWhitespace:true`). `applyBy:"text"` (ALL dc-flavor cards, synthetic blocks, `structureChanged` edits) → locate `beforeText` near `cssPath` and hand-apply the wording change preserving every tag/attribute.
3. Verify each card's `sourceHash` (FNV-1a of file text) — mismatch = file changed since review → flag, don't blind-apply.
4. `comments[]` + `cardNote` + `globalNotes` are free-form requests → implement with judgment per [[feedback_autonomous_batch_execution]]; ambiguities listed in the commit summary, not asked per-item.
5. Rebuild bundles for touched CLASSIC projects (`node build_cards_only.js he 3|4`); **P1/P2 are dc now — no bundle build applies** (see below). One consolidated commit including the feedback json+md.

**THE APPLY CONTRACT NOW LIVES IN A SKILL:** `.claude/skills/apply-feedback/SKILL.md` (created 2026-08-03) — invoke via `/apply-feedback` or the plain phrases ("apply the feedback"/"apply changes"). It encodes everything below + hash verification, stale-cache skipping, comment-judgment precedents, W2 minimal-fix doctrine, rebuild+commit shape. Follow the skill; this memory is background.

**APPLY-LOOP GOTCHAS (learned 2026-07-08):** (1) The console saves the FULL localStorage state each time, so the NEWEST `feedback_*.json` is the cumulative superset — apply only that one. (2) `rvw:card:*` edits persist across days, so an edit already applied in a prior session re-exports as a **stale** edit — always verify each edit's `beforeText` is still present in the file (if the `afterText` is already there, it's a no-op; skip it). Tell Yon to hit **"איפוס הכל"** (reset-all) after an apply so old cached edits stop re-appearing. (3) A `comment` can request an **image swap** ("replace the image here with C:\...\x.png") — copy the file into the card's `assets/`, replace the target block (often an inline HTML mockup, not an `<img>`) with a framed `<img src="./assets/x.png">`; the bundle's `inlineImages` ([[dc-build-architecture]]) data-URIs it automatically. Always verify each card's `sourceHash` matches the current file before applying.

**RESOLVED 2026-07-05 (commit `cc4607c`) — dc is now the SINGLE canonical HE task-card source for all 4 projects.** All 55 classic `_he.html` task cards retired (deleted+committed); all 55 `.dc.html` now tracked; `support.js` in every `task_cards_he/`. So the console manifest now lists 55 dc cards only (the flavor filter's "classic" option shows nothing for HE task cards). **"Apply the feedback" now edits ONE file per card (the dc file)** — no classic twin to sync. dc rendered DOM ≠ source bytes (React), so wording fixes are text-mode: locate `beforeText` near `cssPath`, hand-apply preserving tags (the runtime injects `data-dc-tpl` attrs not present in source). Builds source dc via [[dc-build-architecture]]. Related: Yon's `improve_hebrew_gpt.js` (see [[project_gpt_hebrew_pass]]).

**Console internals (if it needs maintenance):** block scanner tags text blocks `data-rvw-b` (PRIMARY tags p/li/h1-6/td/figcaption…; leaf rule for div/span/strong with direct text; synthetic spans in mixed containers); pristine snapshots parent-side after neutralization (nickname prompt suppressed by pre-seeding `localStorage['agourim_card_nickname']='סוקר'`; `.nickname-indicator` removed pre-scan); plaintext-only editing, Enter blocked except pre-wrap blocks (`.prompt-template`), Esc reverts; dc settle-wait = rAF poll for no `{{` + stable innerHTML length (3s cap); tag-sequence mismatch ⇒ `structureChanged` ⇒ text-mode. Saved edits re-apply onto the DOM on revisit so review is WYSIWYG across sittings.
