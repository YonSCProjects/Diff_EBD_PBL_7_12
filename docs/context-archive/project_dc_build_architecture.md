---
name: dc-build-architecture
description: "How the HE card builds render the .dc.html Claude-Design cards (render_cards_lib.js: JS+settle, break-tag, snapshot, scopeCss) after the classic retirement (commit cc4607c)"
metadata:
  node_type: memory
  type: project
  originSessionId: 4f98ca88-5db7-42fe-97d8-4266922384ce
---

**What.** 2026-07-05 commit `cc4607c`: the HE overview/bundle builds now source the `.dc.html` cards; classic HE task cards retired ([[project_review_console]] has the source-of-truth note). Yon's explicit call: "overview/bundle builds switch to sourcing the .dc.html cards, classic retired." All-in for all 4 projects — P1/P2 dc (his prior WIP) committed as canonical too (only `*.dc.html` + `support.js` + `assets/`; `uploads/`/`Claude_Design/`/`OldTaskCards/` left untracked).

**New shared module `render_cards_lib.js` (repo root)** — used by both `build_cards_only.js` and `build_overview_with_cards.js`:
- `resolveCardFile(dir, stem, suffix, projectKey)` — prefers the card's `.dc.html` twin, trying BOTH `${stem}${suffix}.dc.html` (P1, unprefixed) and `P${key}_${stem}${suffix}.dc.html` (P2/P3/P4 carry a `P<key>_` prefix — inconsistent naming!). Falls back to classic `${stem}${suffix}.html`, so EN builds and the still-classic **reference cards** (R0–R6 never converted) are unchanged.
- `renderCardPdf` — dc needs the React runtime: JS ON (old overview build did `setJavaScriptEnabled(false)` → would print raw `{{ }}`), `waitUntil:networkidle0` (Google Fonts), then `settleDc` polls rAF until no `{{` in innerText + stable innerHTML length (5s cap). Then `tagBreaks` sets `break-inside:avoid` on every leaf box (rounded+filled/bordered element with no box descendant) so A4 pagination won't slice a step card/callout/code panel. Nickname prompt pre-seeded + dialogs dismissed.
- `snapshotCardHtml` — for the self-contained merged HTML bundle, serializes the SETTLED dc `.tc-page` outerHTML (all inline-styled) + helmet `<style>`; classic path stays read-file/body+linked-CSS.
- `scopeCss(css, sel)` — **critical fix**: the classic ref stylesheet has global element rules (`h2{}` gives a black bg, `table{}`, `li{}`…) that BLEED onto the inline-styled dc `<h2>` etc. in the shared merged-HTML head. Each card's CSS is scoped to `.appendix-card--dc` / `.appendix-card--classic` (recurses @media/@supports/@layer; copies @font-face/@keyframes verbatim). PDF path is immune (each card = its own page) — bleed was HTML-bundle-only.

**Gotcha found + fixed:** P2's `task_cards_he/` was MISSING `support.js` (only P1 ever had it; the review console faked it via server fallback) → P2 dc cards rendered raw `{{` in the build until support.js was copied in. All 4 folders now have it.

**UPDATE 2026-07-06 (commit `b7bef77`) — reference cards ALSO converted to dc; the whole bundle is now uniformly dc.** All 25 HE reference cards (R0–R6 × P1–P4) rebuilt as STATIC dc (no support.js / no `<x-dc>` — just the dc skeleton: fonts head + `.tc-page`/`.tc-card`, header band with project chip + R-badge, NO progress bar, NO checkboxes, callouts/tables/mono-panels/figures). Classic HE reference cards retired. No build change needed — `resolveCardFile`'s first candidate `${stem}${suffix}.dc.html` finds the (unprefixed) ref dc cards automatically. Exemplar hand-authored = P1 `R2_stuck_protocol_he.dc.html`; other 24 via workflow `wf_5e1212a9` (verbatim gate 25/25). **Also added `inlineImages` to render_cards_lib.js**: the merged HTML bundle now embeds every `<img>` as a data URI so the self-contained bundle shows its figures (relative `../images`/`./assets` paths only resolve standalone — which is why the per-card PDF was always fine). New page counts: P1 51, P2 45, P3 56, P4 73; overview 78.

**Regenerated tracked bundles (superseded above):** Project_1 52pp, Project_2 45pp, Project_3 58pp, Project_4 76pp (= classic reference cards + dc task cards). Program overview (79pp) regenerated but is a **gitignored** output (`.gitignore` whitelists only `build_output/Project_N_Cards*.{html,pdf}`) — regenerate locally, don't commit. Rebuild: `node build_cards_only.js he <1-4>` and `node build_overview_with_cards.js he`. EN unchanged (still classic). Supersedes the old build-story caveat in [[feedback_build_output_must_reflect_changes]].
