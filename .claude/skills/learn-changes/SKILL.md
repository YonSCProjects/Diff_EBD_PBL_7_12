---
name: learn-changes
description: Learn Yon's card-editing style from review-console feedback — extract before→after patterns from review_feedback/*.json, generalize them into authoring rules in Card_Editing_Preferences_Log.md, and propose (never auto-apply) program-wide sweeps.
---

# Learn Changes — turn review-console edits into card-authoring rules

Yon edits the Hebrew task/reference cards in the review console; every save writes a
`review_feedback/feedback_*.json` with exact before→after pairs. This skill ingests the
feedback that has not been learned yet, generalizes it into rules, and updates
**`Card_Editing_Preferences_Log.md`** (repo root) so that future card authoring
(P5–P8 and any regeneration) produces cards that already match his edited style.

Run it whenever Yon says "learn the changes" / "/learn-changes" — typically right after
an "apply the feedback" round, but it works standalone too.

## Procedure

### 1. Determine what's new
- Read `Card_Editing_Preferences_Log.md` → the **Processed feedback ledger** section
  lists every feedback file already learned.
- List `review_feedback/feedback_*.json` not in the ledger. If none → say so and stop.
- **Cumulative-superset semantics:** each console save exports the FULL localStorage
  state, so same-session saves overlap. Process the newest file of each batch, but the
  real dedup unit is the **edit**, not the file: an edit is *new* only if its
  `(card file, beforeText → afterText)` pair is not already cited as evidence in the log.

### 2. Extract and classify each new item
For every card entry in the new feedback:
- **edits[]** — each has `beforeText` / `afterText` (dc cards are text-mode). Classify:
  trimming (dropped words/clauses), word choice, register/tone, sentence structure,
  terminology, punctuation, reordering.
- **comments[]** — free-form requests. Classify: design change, image replacement
  (path like `C:\...\x.png` → the asset-swap procedure lives in the apply loop, but the
  *preference* it expresses — e.g. "real screenshots over drawn mockups" — is learnable),
  layout, content addition/removal.
- **cardNote / globalNotes** — often restate an edit; use as intent confirmation.
- **Stale edits:** if `beforeText` is absent from the current card and `afterText` is
  present, the edit was applied in an earlier round — do not double-count it as fresh
  evidence (it is usually already in the log).

### 3. Generalize into rules — with counterexample evidence
- Try to cluster each new edit under an EXISTING rule first (strengthen it: add the
  example, bump the evidence count).
- For a candidate NEW rule, before writing it: **grep all dc cards** for surviving
  instances of the "before" pattern. Record the counterexample count and where they are.
  A rule Yon applied once while leaving 13 identical instances untouched is a *narrow*
  or *tentative* rule — say so honestly. He edits card-by-card over days, so surviving
  instances in cards he hasn't reached yet are weak counterexamples; surviving instances
  in cards he marked **done** (`"done": true` in the feedback) are strong counterexamples
  and usually mean the rule's scope is narrower than it looks.
- **Confidence ladder:** `TENTATIVE` (1–2 examples) → `FIRM` (3+ consistent examples
  across ≥2 cards, no strong counterexamples) → `CONFIRMED` (Yon explicitly confirmed,
  or a sweep he approved was applied program-wide). Only FIRM/CONFIRMED rules may be
  used silently when authoring new cards; TENTATIVE rules are flagged as "leaning".

### 4. Protected motifs — never generalize over these
Locked program-level design decisions outrank any learned rule. A learned rule must
carve these out explicitly (check `review_feedback/gpt_p*_vetting_*.md` for the record):
- **"קוראים למורה, תמיד"** — the soldering-safety escalation (P4 + R6). A "trim after
  קוראים למורה" rule must NEVER touch the soldering variants.
- "זה נורמלי / זה תקין, לא תקלה" catchphrase; "סיימתם כש:" headers; "בלי פאניקה";
  "לא באותו טור, זה ייצור קצר"; "חיישנים אמיתיים אינם מושלמים וזה בסדר גמור";
  celebration blocks on final milestones; "זו לא העתקה — אתם מבינים מה שיניתם".
- The plural-impersonal verb form and other rules in `Hebrew_Translation_Preferences_Log.md`
  (this log complements it, doesn't override it). If a learned edit CONTRADICTS one of
  those patterns, surface the conflict to Yon instead of silently recording a rule.

### 5. Update the log
`Card_Editing_Preferences_Log.md` structure (keep it):
- Rules grouped by category, each with: **name** (T1, W2…), 1-line **rule**, **why**
  (inferred intent — phrase it as inference, not fact), **before → after examples**
  (real, cited with card + feedback date), **evidence count**, **counterexamples**
  (count + whether in done cards), **status** (TENTATIVE/FIRM/CONFIRMED), **sweep scope**
  (what a program-wide application would touch, minus protected carve-outs).
- **Processed feedback ledger** — append the newly ingested filenames + date.
- **Changelog** — one dated line per run summarizing what was learned.

### 6. Report to Yon — and propose, never auto-apply
End with a compact summary:
1. New rules learned / rules strengthened (with status changes).
2. Conflicts with existing preference logs, if any.
3. **Proposed sweeps table:** for each FIRM(+) rule, how many surviving instances a
   program-wide sweep would change, with the protected carve-outs listed. Apply a sweep
   ONLY when Yon explicitly approves it (then: batch-apply, rebuild affected bundles,
   one consolidated commit, and mark the rule CONFIRMED).
4. Remind him that "איפוס הכל" in the console clears stale cached edits.

### 7. Where the rules get used
- **Authoring new cards (P5–P8):** every authoring prompt must include
  `Card_Editing_Preferences_Log.md` alongside `dc_design_spec.md` (the spec's header
  points here). FIRM/CONFIRMED rules are applied silently; TENTATIVE rules are applied
  when they don't conflict with source text fidelity.
- The GPT Hebrew pass (`improve_hebrew_gpt.js`) and the reviewer agents may also cite
  this log; keep rule names stable so citations don't break.

## Notes
- Commit the updated log (and nothing else) at the end of a learning run:
  `Learn changes: <n> new rules, <m> strengthened (feedback_YYYY-MM-DD_*)`.
- This skill NEVER edits cards. Learning and sweeping are separate steps by design.
