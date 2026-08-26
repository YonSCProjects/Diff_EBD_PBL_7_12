---
name: wiring-figures-are-part-of-every-card-set
description: "Yon expects real Fritzing-quality circuit images in every project's wiring cards; ASCII maps alone are a gap he comes back for — don't defer figures to \"later\""
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 23475edf-dbb3-4a71-8074-6f8e659f8622
  modified: 2026-08-21T22:34:29.826Z
---

On 2026-08-21 Yon opened with "i see that you didn't create real images of the circuits for
p5-p7. please create them like you did in p1-p4" — the P5–P7 sets had shipped with ASCII
wiring maps and "Fritzing figures deferred" in the handoff. He also said: if the Fritzing
MCP isn't enough, "use any other high quality modeling tool" — quality of the image matters
more than which tool made it.

**Why:** the figures are what students (EBD, grades 7–12) actually wire from; the ASCII map
is a reference, not a picture. A card set without figures is not finished in Yon's eyes.

**How to apply:** treat the wiring figures as a mandatory step of the card-set process
(card_authoring_process.md step 2), not a deferral. Use [[reference_fritzing_kit]] — it
handles ESP32/CAM/L298N and other parts the Fritzing library lacks. When a hardware decision
changes (battery, motor count), regenerate the affected figures in the same pass as the text.
