---
name: apply-feedback
description: Apply Yon's review-console feedback to the dc cards — read the newest review_feedback/*.json, verify hashes, detect stale cached edits, apply edits + comments with judgment, rebuild affected bundles, one consolidated commit. Trigger phrases; "apply the feedback", "apply changes", "apply feedback".
---

# Apply Feedback — the review-console apply contract

Yon reviews Hebrew cards in the review console (`start_review.bat`) and saves feedback to
`review_feedback/feedback_*.json`. This skill applies a saved round to the card sources.
It is the other half of `/learn-changes` (which should usually run right after).

## Procedure (distilled from the applied rounds — follow all of it)

### 1. Pick the round
- Newest `review_feedback/feedback_*.json` by mtime. Same-sitting saves are cumulative
  supersets — the newest contains everything; earlier same-batch files are just history.
- Read `stats` for scale. Cards are in `cards[]`; untouched cards in `notReviewed`.

### 2. Per card: verify BEFORE touching
- Compute FNV-1a of the current file and compare to the card's `sourceHash`:
  `node -e "const fs=require('fs');let s=fs.readFileSync('<F>','utf8');let h=0x811c9dc5;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=(h*0x01000193)>>>0;}console.log(h.toString(16).padStart(8,'0'))"`
- **Hash matches** → apply normally.
- **Hash differs** → check each edit for staleness: if `beforeText` is ABSENT and
  `afterText` (or its effect) is PRESENT, the edit was applied in an earlier round and is
  re-exporting from unreset console cache → **skip it, count it, tell Yon**. If an edit is
  neither applicable nor stale (real drift), flag that card for manual review — never
  blind-apply onto changed content.

### 3. Apply edits (all dc cards = text-mode)
- Locate `beforeText` near the `cssPath`/`contextBefore`/`contextAfter`; hand-apply the
  wording change preserving every existing tag and attribute. The runtime injects
  `data-dc-tpl` attributes that do NOT exist in the source — match on text, keep the
  source's actual inline markup (`<strong>`, `<code dir="ltr">`…).
- Whitespace: normalize sensibly (feedback sometimes carries doubled spaces / moved
  spaces around tags); never let that change wording.
- Never touch anything outside the matched span; never "improve" neighboring text.

### 4. Comments = requests, applied with judgment
- **A comment and an edit on the same block:** the stronger/later instruction wins
  (precedent: an edit trimmed a line, the comment said "להוריד לגמרי" → the line was
  removed entirely).
- **Image replacement** ("replace the image here with C:\...\x.png"): copy the file into
  that card's `task_cards_he/assets/`, replace the target block (often an inline HTML
  mockup, not an `<img>`) with a framed `<img src="./assets/x.png">` + Hebrew alt, styled
  like the card's other figures. Extension must match the bytes (Chromium rejects JPEG
  bytes under a .png name over file://) — convert if needed.
- **Styling requests** ("smaller, not bold") — implement with inline style consistent
  with the dc tokens.
- **Correctness questions** ("לבדוק את זה — למה ש…?") — verify the fact, then fix the
  claim MINIMALLY. Do not add background explanations (rule W2 in
  `Card_Editing_Preferences_Log.md`); Yon rejected an explanatory fix in favor of the
  bare corrected observation.
- Ambiguities: resolve by judgment, list them in the commit message / report — don't
  ask per-item (Yon's autonomous-batch preference).

### 5. Guards
- Protected motifs (soldering "קוראים למורה, תמיד", "זה תקין לא תקלה", "סיימתם כש:",
  celebrations…) — a feedback edit CAN change them (Yon's word is law on his own cards),
  but never extend such a change beyond the exact span he edited.
- Wording comes only from Yon's `afterText` or his explicit comment — never invent.

### 6. Verify, rebuild, commit
- Render each changed card headlessly (puppeteer: JS on, dismiss dialogs, wait for the
  dc runtime to settle — no raw `{{`, images load) and eyeball the screenshot.
- Rebuild the affected projects' bundles: `node build_cards_only.js he <N>` — and the
  overview `node build_overview_with_cards.js he` (gitignored output, still required:
  Yon works from build_output/).
- ONE consolidated commit: changed cards + rebuilt tracked bundles + the feedback
  `.json`+`.md` records. Message: `Apply review feedback (feedback_YYYY-MM-DD_HHMM): <scope>`
  with a body listing edits applied / stale-skipped / comments and how each was resolved.

### 7. Close the loop
- Remind Yon: click **"איפוס הכל"** in the console so applied edits stop re-exporting.
- Suggest running **/learn-changes** to fold the round into the rules log.
