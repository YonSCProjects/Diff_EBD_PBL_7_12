---
name: project_handoff_to_cowork
description: 2026-08-26 — the project is moving out of Claude Code to Claude Cowork; HANDOFF.md at the repo root is the authoritative brief and supersedes these memories
metadata: 
  node_type: memory
  type: project
  originSessionId: 23475edf-dbb3-4a71-8074-6f8e659f8622
  modified: 2026-08-28T21:23:38.436Z
---

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
