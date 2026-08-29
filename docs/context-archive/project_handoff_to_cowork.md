---
name: project_handoff_to_cowork
description: the Cowork round trip, 2026-08-26 to 2026-08-29 — what it changed and what it left; the project is back in Claude Code
metadata: 
  node_type: memory
  type: project
  originSessionId: 23475edf-dbb3-4a71-8074-6f8e659f8622
  modified: 2026-08-28T21:23:38.436Z
---

> **CLOSED 2026-08-29 — the project came back.** Yon worked in Cowork for three days and
> returned to Claude Code. The return leg is `HANDOFF_COWORK_TO_CLAUDE_CODE.md` at the repo root:
> it covers toolchain setup, what commits `76377a3` and after changed, and the traps of that
> phase. **Read both handoff files; they are complementary, not versions of each other.** What
> follows is the outbound record, kept for the reasoning.

2026-08-26. Yon moved this project out of Claude Code to **Claude Cowork**, because the work is
now dominated by design and 3-D modelling.

**`HANDOFF.md` at the repo root is the authority.** 628 lines, written from a seven-way survey of
the repo plus an adversarial completeness pass — not from memory. It covers the project in one
page, the five things that bite, environment setup and every machine-specific path, the three
figure pipelines, the Hebrew and card conventions, the review loop, per-project state, ranked
open work, and eleven ways to break things silently. **Where anything in this memory folder
disagrees with HANDOFF.md, HANDOFF.md wins.**

**The memory folder is now archived in-repo** at `docs/context-archive/` (53 files). It had to
be: this directory's key encodes the absolute path of the project folder, so **moving or renaming
the folder orphans the memory even on the same machine.** Worth remembering as a general fact
about how this memory works, not just for this move.

**What the new environment may not be able to do** (the answer Yon asked for, recorded because
it shapes what work is possible there):
- The outputs travel — all 96 figure SVGs and 18 card bundles are committed, so cards render and
  print anywhere. It is *regeneration* that needs a local toolchain.
- Three hard local dependencies: **Blender** (~2–2.5 min a frame on CPU, 70 min for a full P8
  pass), **Fritzing** desktop plus its un-vendored `fritzing-parts/core`, and the **review
  console** (a local server on 127.0.0.1:8765 — the heartbeat of Yon's whole feedback loop).
- The irony worth naming: the move is *for* the design and modelling emphasis, and the modelling
  is exactly the part that needs a local Blender install.
- Degrade but survive: the two skills and seven agents (their procedures are written out in the
  repo), the hooks (Claude Code-only), automatic memory recall.
- Fine: all textual work, the Hebrew conventions, the four preference logs, git.
- Suggested split if Blender cannot run there: author and review in the new environment, keep a
  local machine for render passes. `--compose-only` re-labels a figure in about a second without
  Blender; only geometry changes need a full render.

**Concurrent work.** Commit `76377a3` (2026-08-26) came from a *different* session working in the
same repo, and it reworked much of `_blender/`: `cadparts.py` + `wrl.py` (real components read
from KiCad's published VRML), `pcb.py` (boards with generated silkscreen), `quality.py` (world
lighting and layered materials), a `fonts/` directory and a rewritten `compose.js`. HANDOFF.md
was updated to point at `_blender/README.md` as the authority on the current pipeline. Expect
this repo to have more than one session in it.

Related: [[reference_blender_pipeline]], [[project_step_figures_blender_rebuild]],
[[project_review_console]], [[reference_github]].


## What the Cowork phase actually produced (2026-08-29)

- **The "look like toys" verdict had one cause, and it was not geometry or shading.**
  `quality.apply()` installed a light silhouette-only ink line and then `render.py` called the
  legacy `lib.outlines()` four lines later. Freestyle keeps exactly **one lineset per view
  layer**, so the second call wiped the first — every figure had a 2.4 px black outline on
  silhouette *and* crease *and* material boundary, over correctly rendered CAD geometry. Two
  rounds of work chased the wrong cause first. Now guarded by `_quality_owns_ink` in
  `render.py`; ink is 0.80 px, silhouette and border only, set in `quality.ink()`.
  **If you add any Freestyle call to the render path, check that guard.**
- 32 P4/P5/P7 step figures re-rendered with CAD parts from KiCad's VRML library; 14 wiring
  figures polished with the new `_fritzing_kit/polish_for_print.js`.
- The wide wiring diagrams are still unreadable — labels land at 3–5 px on a card because the
  *sketch layout* is spread out, not because of padding. Fixing it needs the parts moved in the
  `.fzz` and a re-run of `build_figure.js`, which needs Fritzing installed. **Fritzing and its
  core parts library are present on Yon's machine**, so this is work for Claude Code.

## Decision: print PDFs wait (2026-08-29)

Projects 1–3 have `Project_N_Task_Cards_he_print.pdf` via `tools/print/`; P4–P8 do not. Yon:
**"we will do the pdfs at the end when all 8 projects are ready. no need to waste printing
materials before."** Do not offer them again until all eight card sets are finished.
