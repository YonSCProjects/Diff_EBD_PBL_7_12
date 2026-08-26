---
name: reference_illustration_kit
description: Arduino_Projects/_illustration_kit/ draws every step illustration for P4/P5/P7/P8 — read its READMEs before drawing anything new
metadata: 
  node_type: memory
  type: reference
  originSessionId: 23475edf-dbb3-4a71-8074-6f8e659f8622
  modified: 2026-08-23T14:26:14.358Z
---

> **Superseded.** Every step figure for P4, P5, P7 and P8 is now a Blender render — see
> [[reference_blender_pipeline]]. This kit is kept only as the source of the millimetre
> geometry and the per-card briefs (`p8_facts_and_briefs.json`), which the Blender modules
> were ported from. Do not draw anything new with it: its painter's-algorithm depth sort is
> provably unable to give correct occlusion for interlocking geometry, which is what every
> depth bug in P5/P7/P8 turned out to be.

`Arduino_Projects/_illustration_kit/` is where every **step** illustration comes from — the picture
of what the student's hands actually do. It is separate from [[reference_fritzing_kit]], which draws
**wiring** figures from real Fritzing parts; both ship, they answer different questions.

- `iso.py` — the isometric engine. True 30° projection, painter's algorithm with explicit layers
  (0 under-plate far … 5 tools). Primitives: `cuboid`, `cyl_x/y/z`, `disc`, `ring_z`, `prism`,
  `blade`, `spin_arc`, `wire`, `arrow`, `tag`, `render` (auto-fits the viewBox).
- `parts.py` — the car: chassis, TT motors, wheels, Uno, ESP32, L298N, 8×AA box, IR sensors, tools.
  Its millimetres are tied to `Project_4_.../chassis_template/chassis_template_he.html`.
- `parts_p8.py` + `README_P8.md` — the quadcopter. Read the README before touching P8.
- `p8_facts_and_briefs.json` — agent-extracted authority for P8: pin map, rotation table, power tree,
  MOSFET channel lead-by-lead, and a per-card brief with Hebrew callouts.
- `scenes_p4.py` / `scenes_p5.py` / `scenes_p7.py` — one function per step, returning
  `(filename, Scene, title)`. `scenes_p8.py` still to be written.
- `build.py 4 5 7 8` renders into `<project>/images/` **and** `<project>/task_cards_he/assets/`.
- `embed_steps.js` inserts each figure into its card just above the "מה עושים" heading. Idempotent —
  it strips its own `data-iso="step"` block before re-inserting, so re-running never stacks copies.
- `shot.js <in.svg> <out.png> [width]` renders one SVG to PNG for eyeballing; `smoke_p8.py` renders
  parts on their own.

Two gotchas that cost time:
- Depth sorting is by world centroid, so a small overlay rect drawn on top of a bigger board sorts
  *behind* it. Use an explicit `sc.add(key + bump, poly(...), layer)` for anything lying on a surface.
- Bash heredocs in this environment eat backslashes — `\n` inside a Python string becomes a real
  newline and breaks the file. Use the Write/Edit tools for anything containing escapes.
