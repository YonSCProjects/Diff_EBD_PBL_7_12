---
name: fritzing-kit-real-part-figures
description: "Arduino_Projects/_fritzing_kit = the figure pipeline for P4-P7+ (real community Fritzing parts bundled in .fzz, CLI export, puppeteer pin coords, composited wires); supersedes P2 hand-compositing and P4 inject_modules"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 23475edf-dbb3-4a71-8074-6f8e659f8622
  modified: 2026-08-21T21:55:43.056Z
---

Since 2026-08-22 every wiring figure in P4–P7 is produced by
`Arduino_Projects/_fritzing_kit/build_figure.js <spec.json>` (README in the kit has the spec
format and the gotchas). Parts the core library lacks (ESP32 DevKit V1, ESP32-CAM, L298N,
TT motor "Getriebemotor", DHT22, SSD1306 OLED, FTDI, Mini560 buck, TCRT5000, my own 8xAA box)
live in `_fritzing_kit/parts/` and are bundled INSIDE each `.fzz` (so Yon can open them in
Fritzing). Specs: P4/P6/P7 `images/fritzing/gen_specs.py`, P5 hand-written JSONs.
`embed_figures.js` inserts the P4-style figure block after a card's wiring `<pre>`.

**Why:** Fritzing MCP alone could not draw ESP32/CAM/L298N circuits at all; Yon asked for
real images "like P1-P4", so this is the high-quality route (figures look native).

**How to apply:** new figure = write a spec (or extend gen_specs.py) → build → LOOK at
`images/fritzing/<name>_preview.png` (crop with PIL if needed) → embed → rebuild the bundle.
Hard-won rules live in the kit README (no spaces in bundled part names, `<g id="breadboard">`,
no gradients/opacity in custom parts, rail holes skip every 6th number, LED leg offset,
forced crossings to leave alone). Check crossings on paper first: with all endpoints on the
region boundary, interleaved chord pairs (1-3 / 2-4) always cross — move a part instead of
fighting the route. See [[reference_fritzing_svg_compositing]] (older recipe, superseded).

**2026-08-23 — extended for Project 8.** `draw_p8_parts.py` in the kit draws the parts nobody
publishes: `mosfet_board_4ch` (the 7x5 cm perfboard with four IRLB8721 low-side channels, pads
BAT+/GND/M1-4/G1-4), `motor_8520_cw` + `motor_8520_ccw` (lead colours encode rotation),
`lipo_1s_1000` (PH2.0 pouch) and `mt3608_module`. Re-run it then `normalize_parts.py`. Custom part
SVGs must use SOLID fills and `style=` attributes only — gradients in `<defs>` and `opacity=` render
white/opaque through the Fritzing CLI's Qt SVG renderer (the 8xAA box had to be redrawn for that).
