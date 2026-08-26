---
name: project_step_figures_blender_rebuild
description: "2026-08-24 — every P4/P5/P7/P8 step figure rebuilt in Blender with ink outlines and auto-framing; what shipped, what is still open"
metadata: 
  node_type: memory
  type: project
  originSessionId: 23475edf-dbb3-4a71-8074-6f8e659f8622
  modified: 2026-08-24T14:41:57.739Z
---

2026-08-24. Yon asked for the step graphics of Projects 4, 5, 7 and 8 to be raised in quality,
pointing at a Claude Desktop carpentry-workshop chat and asking which of its **image** techniques
transferred (explicitly not its text or general design — those are already solved here).

**What transferred from that chat**, and is now the backbone of `_blender/`
(see [[reference_blender_pipeline]]):
- **Freestyle ink outlines.** The single biggest step change. Without a contour line every part
  dissolves into a neighbour of similar tone.
- **The painter's algorithm is provably wrong for interlocking geometry.** That diagnosis is why
  `Arduino_Projects/_illustration_kit/` is now retired for drawing — see
  [[reference_illustration_kit]].
- **Tone separation** — a mid-tone bench and a visible floor, so a near-white polygal plate has
  something to sit against.

**Shipped this session**
- P4: all 10 card figures plus the 7 M3 step figures re-rendered with ink, several rebuilt
  (`s_cut_plate` now shows the real template; `s_track` is one clean tape loop; the soldering
  iron is parked in its coil).
- P5: modelled from scratch — ESP32 DevKit on the car, 7 figures.
- P7: 8 figures — FTDI programmer, upload ritual, camera on its perch, two power rails, the
  barrier scene.
- P8: the whole quadcopter modelled (`p8_drone.py`) and 28 figures written.
- Infrastructure: `camera_fit` auto-framing, `shot_cards.js` (fails on any card image that did
  not load), `ribbon`/`capsule`/`sphere` primitives, `compose.js` gained wifi fans and numbered
  badges, callout type scaled up to about 8 pt at card size.

**Content bug found and fixed**: the P4 M3 card's summary strip said the motors are hot-glued
while its own step 4 says "screwed, not glued". The figure followed the wrong one. The figure now
shows two M3x30 per motor and the caption and alt text were corrected to match step 4.

**Yon's verdict on the rebuild (2026-08-25):** *"ok its better, we still need some
improvements."* Accepted as a real step up, not finished. He is reporting the remaining figure
problems through the review console ([[project_review_console]]) — which has no way to anchor a
comment to a figure, so they arrive as free-form `cardNote`/`globalNotes` prose naming the figure
and what is wrong with it. Framing, placement and part sizes are all parameters now, so
"too small", "cut off", "can't see X" and "wrong angle" are cheap to act on; re-rendering one
Cycles frame is about two minutes.

**Still open**
- `_blender/hand.py` — a hand is modelled and pose-checked but **not used in any figure**. Its
  flat and point poses read; the curled ones still read as a mitten with sticks. Finishing it is
  the next real lever on quality, since every card brief describes a hand doing something. If it
  is finished, put it in everywhere the briefs call for one, not in a couple of figures.
- P8's T2 figures reuse T1 scenes for the shared milestones (mount, pre-power, spin, thrust);
  that is deliberate, but a few could be given their own angle.
- Some bench scenes still frame loose — the accessories are genuinely as big as the subject
  (a 132 mm meter beside a 50 mm perfboard), and `_near()` anchors only buy so much.
