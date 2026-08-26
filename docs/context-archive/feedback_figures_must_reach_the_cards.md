---
name: feedback_figures_must_reach_the_cards
description: "A figure only counts when it renders in the card Yon opens — publish over the filename the card already embeds, then verify by screenshotting the card"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 23475edf-dbb3-4a71-8074-6f8e659f8622
  modified: 2026-08-24T05:22:17.192Z
---

Yon opened `P4_T1_M1_meet_soldering_he.dc.html` after a long stretch of figure work and said
"i dont see any improvement". He was right: ten Blender renders had been published as
`w_p4_r04_wiring.svg` while every card embeds `w_p4_s04_wiring.svg`. The renders were landing in
files nothing referenced, so the cards kept serving the old SVGs.

**Why:** work that does not reach the artefact the user opens has not been done, however good it
looks in a scratch folder. Grepping the cards for what they actually embed takes seconds and is
the difference between shipping and not.

**How to apply:**
- Before publishing any figure, `grep -o 'w_p4_s[0-9a-z_]*\.svg' <cards>` and target *those* names.
  `_blender/build_p4.sh` carries the publish map and a comment saying why.
- After publishing, **screenshot the card itself** (puppeteer on the `.dc.html`), not the SVG in
  isolation. That is what caught it.
- Then rebuild the bundle — see [[feedback_build_output_must_reflect_changes]].
- A new figure filename means a card edit too; there is no such thing as publishing a figure and
  being finished.

Related: [[reference_blender_pipeline]].
