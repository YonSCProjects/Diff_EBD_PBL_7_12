# Task-Card Authoring Process (Hebrew `.dc.html` cards)

The end-to-end process for creating and polishing a Hebrew task card, assembled
from how Projects 1–4 were actually built. Follow it for every new card and for
Project 5–8 card sets. Hebrew cards are the **only** dev target (standing rule
since 2026-08-05); the English set is stale and must not be used as a source.

> **Quick map:** author from spec → wiring diagrams (Fritzing MCP) → verbatim
> gate → reviewer agents → GPT Hebrew pass → rebuild → Yon's review console →
> learn-changes.

## Background — where the `.dc.html` design came from (and why Claude Design is no longer a step)

The dc design language originated in **Claude Design** (claude.ai/design): the
P1/P2 Hebrew cards were redesigned there, and those cards are the exemplars the
whole system descends from. But Claude Design's Project 2 conversion **silently
reworded and condensed the card text** — violating the words-are-final rule —
which is the direct reason the `check_text.js` verbatim gate exists.

Since the P3/P4 rebuild (2026-07-05) the process is fully local: the design
language was extracted verbatim from the P1/P2 exemplars into
`dc_design_spec.md`, and Claude Code authors cards from that spec with the gate
enforcing zero rewording. **Do not route new cards through Claude Design.**
The DesignSync tool is not part of this process either — it only syncs files to
claude.ai/design *design-system* projects (it cannot message a Claude Design
chat project), and its auth is blocked in the VSCode environment (needs
`/design-login` from a plain terminal). Shelved idea: seed an "Agourim
task-card design system" project on claude.ai/design from `dc_design_spec.md`
so design sessions there could use the canonical component library.

---

## Step 1 — Author the card from the design spec

Write the card directly as a `.dc.html` file in the project's `task_cards_he/`
folder, using **`dc_design_spec.md`** (repo root) as the component library. The
spec was extracted verbatim from the approved P1/P2 exemplars and contains:

- document skeleton (`<x-dc>` / `<helmet>` / DCLogic script + `$preview`)
- header band variants (V1 / V2 / planner V3)
- step-cards with `{{ toggleN }}` / `<sc-if value="{{ checkN }}">` checkboxes
- warning / expected / done-when / stuck / celebration / skip-notice /
  diagram-frame / code-panel / choice-card / planner-field / R-ref-badge
  components
- oklch token table, RTL rules, LTR-mono rules for code

Conventions to keep (locked during the P3/P4 build):

- localStorage keys `tc_pNtMmK_checks` (planners: `tc_pNt3_checks`)
- header chip = the card's subtitle verbatim (e.g. "פרויקט 3 • לא להתקרב יותר מדי")
- images under `./assets/<name>` (copy from `../images/`)
- breadboard vocabulary: numbered strips (1–30) = "טורים", lettered strips
  (a–j) = "שורות"; LED legs go into different **טורים**, never שורות

**Do not re-extract the design system from old cards — the spec is the source.**

## Step 2 — Wiring diagrams (Fritzing MCP)

The breadboard diagrams the cards embed are generated with the project-scoped
**Fritzing MCP** (configured in `.mcp.json`; server source at
`C:\Fritzing mcp`). Workflow:

1. **Call the `fritzing_wiring_rules` tool FIRST**, before generating any
   circuit (standing global rule) — it returns the non-obvious conventions:
   LED polarity, breadboard layout, wire colors, Arduino SVG scaling.
2. **Don't hand-build sketches from scratch.** Copy a canonical `.fzz` from the
   project's `images/fritzing/` folder (P1 has `w0`–`w5` + `w_arduino_only`)
   and modify it with the MCP part/wire tools, then `fritzing_export` to SVG.
   Exports land in `images/w*_breadboard.svg`.
3. **Breadboard part:** use the full-size `Breadboard-RSR03MB102-ModuleID`
   ("RSR 03MB102"), NOT the MCP-default half breadboard — the workshop's real
   board is full-size and the half board confused students. RSR03MB102's pin
   naming is compatible with the half board's, so swapping it into an existing
   sketch keeps the wires.
4. **LED export bug:** the CLI silently DROPS any LED whose color property
   isn't `Red (633nm)` — set all LEDs Red (captions carry the pin numbers) or
   use per-colour parts.
5. **Parts the headless MCP can't snap+wire, or that Fritzing's library lacks**
   (ESP32 DevKit / ESP32-CAM / L298N / TT motor / DHT22 / OLED / FTDI / buck /
   TCRT5000 / 8×AA box): use **`Arduino_Projects/_fritzing_kit/`** (since
   2026-08-22, the pipeline behind every P4–P7 figure). It bundles real
   community `.fzpz` parts inside the `.fzz`, exports through the Fritzing CLI,
   extracts every connector's coordinates with puppeteer and composites
   Fritzing-style wires + callout tags at those exact points — one command per
   figure (`node _fritzing_kit/build_figure.js <spec.json>`), spec files in the
   project's `images/fritzing/` (or a `gen_specs.py` that writes them), and
   `embed_figures.js` drops the figure block into the cards. Read the kit's
   README for the spec format and the CLI gotchas (no spaces in bundled part
   names, `<g id="breadboard">` layer, no gradients in custom parts, rail holes
   skip every 6th number, bendable-leg offsets). The older P2 hand-compositing
   recipe and P4's `inject_modules.js` labeled blocks are superseded by it.
6. Cards reference the SVGs **by filename** from `./assets/` (copied from
   `../images/`), so overwriting an SVG auto-updates every card that uses it —
   just rebuild the bundle afterwards.

New Fritzing lessons (geometry, part quirks, conventions) get persisted to
`C:\Fritzing mcp\CLAUDE.md` or the MCP source — **with Yon's confirmation** —
so future sessions benefit.

## Step 3 — Verbatim-text gate (when converting existing text)

If the card's text already exists (a classic card, an approved draft), the
words are final. Enforce that mechanically:

```
node check_text.js <source.html> <card.dc.html>
```

Exit 0 = clean; otherwise it prints JSON with `missing[]` segments. It extracts
every text segment (>8 Hebrew / >15 Latin chars) from the source and fails
unless each appears whitespace-normalized in the dc file. On the P3/P4 rebuild
this gate ran three times per card (author, independent verifier, batch sweep)
and caught every silent rewording. For brand-new text this step is skipped —
the reviewers below are the quality gate instead.

## Step 4 — Reviewer-agent pipeline (with guards)

Run the reviewer subagents on the draft:

1. `pedagogical-card-reviewer` + `visual-design-reviewer` **in parallel**
2. then `hebrew-translation-reviewer` on the Hebrew text

**Always include the guard block in each reviewer prompt** — without it the
reviewers over-generate badly (Project 2: 271 findings, only 33 real; with
guards on Project 3: 62 findings, ~50 real):

- "The V1/V2/V3 card-id is a VERSION/tier badge, NOT a checkmark — never
  propose changing it to ✓."
- "These cards deliberately MIRROR the already-approved Project N-1 cards — do
  NOT propose stylistic rewrites of shared patterns; only flag what is
  genuinely wrong for THIS card."
- State the project's fixed facts: canonical pin map, intentional quirks
  (e.g. P3's "a big distance reading like 999 is normal, not a bug"),
  placeholder diagrams that are intentional.
- "HIGH/MEDIUM only, hard cap 5 findings per reviewer, empty array if clean."
- Force a structured findings schema: `{severity, location, issue, fix}`.

Apply high- and medium-confidence proposals; flag low-confidence ones for Yon.
One known reviewer inversion: a within-card "consistency" finding may point at
the *dispreferred* form — check against `Hebrew_Translation_Preferences_Log.md`
(e.g. LED lighting up = מאיר, not נדלק) before applying its direction.

## Step 5 — GPT Hebrew pass (ChatGPT second opinion)

**Manual trigger only — run when Yon asks; there is no hook.**

```
node improve_hebrew_gpt.js <card.dc.html> [more-cards...] [--out <file>] [--model <id>]
```

- Sends each card plus the full `Hebrew_Translation_Preferences_Log.md` to the
  OpenAI API (default model `gpt-5.5`; needs the `OPENAI_API_KEY` user env var).
- Returns **proposals only** (before/after pairs) — it never rewrites files, by
  design, to protect the fragile `.dc.html` markup (`{{ }}` tokens, `<sc-if>`,
  inline styles).

**Vet-and-apply (Claude's job):**

1. Check every proposal against `Hebrew_Translation_Preferences_Log.md` and the
   program's locked design decisions (catchphrases, deliberate warmth,
   P2-mirror phrasings, the "מקשיב להד" metaphor, etc.).
2. Markup safety: the Before-quote must exact-match the file and contain no
   markup.
3. Apply accepted proposals with Edit; if a phrase has a twin on another
   project's mirrored card, sync it there too (the exact-match check makes
   this safe).
4. Write a vetting record to `review_feedback/gpt_pN_vetting_<date>.md` —
   accepted / modified / rejected, with reasons. Precedents:
   `review_feedback/gpt_p3_vetting_2026-07-05.md` (74 proposals → ~60 accepted,
   14 rejected) and `gpt_p4_vetting_2026-07-05.md`.
5. Rejections that reveal a stable preference → propose adding it to the
   preferences log (with Yon's confirmation). The script reads the log from
   disk at runtime, so log updates flow into future runs automatically.

Status: P3+P4 have been through this pass (2026-07-05); **P1/P2 dc cards have
not yet** — still on the backlog.

## Step 6 — Rebuild

Every content change must end with `build_output/` regenerated:

- `node build_single_card.js <card>` for one card, or `node build_cards_only.js`
  for bundles (see `render_cards_lib.js` for the shared render pipeline).
- After **adding or renaming** a card: re-run `node build_card_nav.js` so the
  prev/next navigation stays correct, and register the filename in
  `build_overview_with_cards.js` `cardOrder` if the card belongs in the
  overview PDF.

## Step 7 — Yon's review round

1. Yon opens the review console (`start_review.bat`) and edits the cards in the
   browser; his changes export to `review_feedback/feedback_<date>.json` + `.md`.
2. "apply the feedback" / "apply changes" triggers the **apply-feedback** skill:
   read the newest JSON, verify hashes, detect stale cached edits, apply edits
   and comments with judgment, rebuild affected bundles, **one consolidated
   commit** (Yon prefers one end-to-end run over per-proposal confirmations).
3. After each apply round, run **/learn-changes** to distill the edits into
   generalized authoring rules in `Card_Editing_Preferences_Log.md` (sweeps
   only on approval).

---

## Key files

| File | Role |
|---|---|
| `dc_design_spec.md` | Component library / authoring source for all dc cards |
| `check_text.js` | Verbatim-text gate (source vs dc card) |
| `improve_hebrew_gpt.js` | GPT Hebrew pass — proposals only |
| `Hebrew_Translation_Preferences_Log.md` | Hebrew style rules; fed to GPT and used for vetting |
| `Card_Editing_Preferences_Log.md` | Yon's card-editing style, learned via /learn-changes |
| `render_cards_lib.js`, `build_single_card.js`, `build_cards_only.js` | Render/build pipeline |
| `build_card_nav.js` | Regenerates prev/next nav (re-run after add/rename) |
| `build_overview_with_cards.js` | Overview PDF with interleaved cards (`cardOrder`) |
| `start_review.bat`, `review_server.js` | Yon's in-browser review console |
| `review_feedback/` | Feedback exports + GPT vetting records |
| `Arduino_Projects/Project_N_*/images/fritzing/*.fzz` | Canonical Fritzing sketch sources — copy + modify, don't hand-build |
| `fix_wiring_svgs.js` | Post-processes exported SVGs: moves GND rail to the bottom (next to the Arduino's GND/5V pins) |
| `svg_to_png.js` | Rasterize exported/composited SVGs for visual QA |
| `Arduino_Projects/_fritzing_kit/` | Real-part figure pipeline for P4–P7+ (`build_figure.js`, `embed_figures.js`, bundled community parts, README with gotchas) |
| `Arduino_Projects/Project_4_Line_Following_Car/images/fritzing/inject_modules.js` | (superseded) Labeled-module + wire compositing for parts missing from the Fritzing library |
