---
name: feedback_step_figures_from_card_text
description: "Build cards want one figure per numbered step, placed inside that step, and the step's own text is the authority on what the figure shows"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 23475edf-dbb3-4a71-8074-6f8e659f8622
  modified: 2026-08-24T05:22:32.774Z
---

For the chassis-assembly card Yon asked for "an explanatory image for each one of the 7 steps",
not a few figures covering the card loosely.

**Why:** a build card is a sequence of physical actions. One picture per action, sitting *with*
that action, means the student never has to hold several images in their head and map them back to
numbered text.

**How to apply:**
- One figure per numbered step, inserted **inside** the step block, right after its `<p>`.
  `_blender/embed_m3_steps.js` is the pattern — idempotent, CRLF-tolerant.
- **Read the step's own Hebrew and let it drive the figure.** Doing this on P4 M3 caught a real
  error: step 4 says the motors are marked through, drilled and *screwed* on with 2× M3×30, while
  every figure the project had ever carried showed them **hot-glued**. The artwork had been wrong
  in the flat SVGs and stayed wrong through the first Blender pass.
- Lift the callout wording from the step rather than inventing new phrasing; house style still
  applies (plural impersonal verbs, geresh ׳, no comma before a conjunctive ו).
- Fanning the callout authoring out one-agent-per-step works well and is fast.

Related: [[reference_blender_pipeline]], [[feedback_figures_must_reach_the_cards]].
