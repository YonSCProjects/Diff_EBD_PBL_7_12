---
name: fritzing-svg-compositing-unblocks-new-part-wiring
description: "Proven technique to add buzzer / 2nd-button / any new-part wires to a Fritzing breadboard diagram headlessly by compositing wires onto the exported SVG — reverses the old \"GUI needed\" conclusion"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4f98ca88-5db7-42fe-97d8-4266922384ce
---

**The blocker (reconfirmed 2026-07-01).** The headless Fritzing MCP genuinely CANNOT snap+wire a NEW breadboard part (buzzer, 2nd button). `add_part` places at raw x,y (no breadboard-pin alignment); `connect_parts` to the part's own connectors renders the wire in the WRONG place (wiring-rules #9 — the wire needs `register_part_position()`, not exposed as an MCP tool). Wiring via breadboard pins only "connects" visually if the wire ends at the exact hole the floating leg sits in. The old finding [[project_arduino_project2_built]] concluded "new parts need the Fritzing GUI." **That is now bypassable via SVG compositing.**

**The technique (proven on P2 w_p2_02/03/04, 2026-07-01).** Render the parts natively with Fritzing, then draw the missing jumper wires directly onto the exported breadboard SVG at exact coordinates:

1. **Place the new part** with `fritzing_add_part` (raw coords are fine — it renders visually, just unwired). Position it clear of other parts. Use the real moduleId if known (e.g. buzzer `SparkFun-Electromechanical-BUZZER-PTH-NS-KIT`); the generic `pushbutton` = a *round* 2-connector button (looks different from the tactile 4-pin `20A9BBEE34_ST`, which is NOT addable by name).
2. **Export** the breadboard SVG via `fritzing_export`.
3. **Extract flattened SVG-viewBox coords** of the part legs + Arduino pins with a puppeteer script: `pt = bboxCenter; pt.matrixTransform(el.getScreenCTM()).matrixTransform(svg.getScreenCTM().inverse())`. Arduino pins are direct `<circle id="connectorNpin">` already at flattened coords. New-part legs need a group-walk: find the part `<g>` by a signature (buzzer = ancestor of a `circle[fill="#ED1C24"]` piezo) then read its `connector0pin`/`connector1pin`; for several 2-pin parts, enumerate every tightest `<g>` that has connector0pin+connector1pin but not connector2pin and identify by x-position.
4. **Inject Fritzing-style wires** as `<polyline>` before `</svg>`: colored core + soft dark casing (`#2b2b2b` opacity .28, +14 width) + small endpoint dots, `stroke-linecap="round"`. Native wire widths ≈ 22 (signal) / 44 (power) in that viewBox.
5. **Rasterize to PNG** (repo `svg_to_png.js`) and VIEW it to verify; iterate on coords.
6. **Copy the composited SVG over the target `images/…_breadboard.svg`.** Cards reference SVGs **by filename**, so they auto-update — no card edits. Rebuild the bundle (`node build_cards_only.js he <N>`).

**Reference facts.** Arduino Uno flattened pins (this export scale): D2=`connector63pin`, D3=`connector64pin`, D8=`connector51pin`, D9=`connector52pin`, GND=`connector89pin`, 5V=`connector87pin`. Wire colours: orange `#f28a00` (digital signal), green `#25cc35` (signal), red `#cc1414` (5V), black `#000000` (GND). The SparkFun buzzer's two legs are the SAME column (vertical, ~0.7in apart, bridge the gap): route D8→top leg, GND→bottom leg. LED-colour export bug still applies (all LEDs render red — see [[reference_fritzing_led_color_bug]]).

**Caveats.** (a) Composited wires live in the SVG ONLY, not the `.fzz` — a plain re-export won't reproduce them; save BOTH the `.fzz` (parts placed) and the composited SVG. (b) 2-button circuits (w_p2_04) come out **busy** (6 crossing wires, mismatched button styles) — clean for 1 new part (buzzer), messy for 2. (c) Helper scripts (`extract_coords.js`, `extract_all.js`, `inject_wires.js`) were written in the session scratchpad — recreate from this recipe, or promote them to the repo for reuse.

**Reusable for:** Project 3's deferred HC-SR04 living-placeholder diagrams (same new-part blocker — [[project_arduino_project3_built]]) and Projects 4–8. See [[reference_fritzing_canonical_steps]] for the copy+export base pipeline.

**Extension — hybrid labeled-module compositing (proven on P4, 2026-07-05).** When a part doesn't exist in the library AT ALL (L298N, TCRT5000, 4xAA holder), draw it as a labeled SVG block and composite it + its wires onto the Fritzing export. Tool promoted to the repo: `Arduino_Projects/Project_4_Line_Following_Car/images/fritzing/inject_modules.js` (usage `node inject_modules.js <base.svg|BLANK:w,h> <out.svg> <spec.json>`; factories `l298n`/`sensor`/`battery`/`motor` with named wire anchors like `m0.OUT1`, `m0.ENB`, `m1.PLUS`; auto-expands viewBox, negative coords fine). Layout trick that renders cleanest: put the L298N ABOVE the Arduino at x=750,y=−1620 → its ENA..ENB header pins land almost exactly over D10..D5 (near-vertical wire drops). Rail facts for the P1-derived Arduino+breadboard base: (−) blue row y=755.556 (top), (+) red row y=2555.56 (bottom), holes x=3240.56+n·100; D5..D12 at y=100, x 2249.6→1489.6 step −100 with D8 at 1889.6. `extract_ids.js` pattern needs `NODE_PATH=<repo>/node_modules` when run from the scratchpad.
