# `_fritzing_kit` — real-part wiring figures for Projects 4–7 (and onward)

Fritzing's core library has no ESP32 DevKit, ESP32-CAM, L298N module, TT gear motor, DHT22
module, SSD1306 OLED, FTDI programmer, buck module, TCRT5000 module or 8×AA box. This kit
renders those as **real Fritzing parts** (community `.fzpz` parts, bundled inside each
`.fzz`), exports through the Fritzing CLI, then composites wires and callout tags onto the
export at exact connector coordinates. Every figure stays a genuine `.fzz` Yon can open in
Fritzing, plus a composited SVG the cards embed.

## One command per figure

```
node Arduino_Projects/_fritzing_kit/build_figure.js <project>/images/fritzing/<name>.json
```

Pipeline: `make_fzz.py` (spec → `.fzz` with bundled parts) → `Fritzing.exe -svg` →
`extract_pins.js` (puppeteer: flattened coordinates of every connector, per instance) →
optional **snap** pass (re-export once with a part shifted so a pin lands on a target pin) →
`compose.js` (wires / shapes / labels) → `<name>_breadboard.svg` in `images/` + copy into
`task_cards_he/assets/` + `images/fritzing/<name>_preview.png`.

Projects 4, 6 and 7 generate their specs from `images/fritzing/gen_specs.py`
(run it, then build); Project 5 keeps hand-written JSON specs. `embed_figures.js <plan.json>`
inserts the dc-card figure block (same markup as P4) after a card's wiring `<pre>` box —
idempotent (`figure_plan_p5p6p7.json` is the plan used on 2026-08-22).

## Spec format (sketch px, 90 px = 1 in)

```json
{ "name": "w_p6_01_dht22", "out_dir": "..", "assets_dir": "../../task_cards_he/assets",
  "instances": [
    { "id": "bb",  "core": "breadboard2", "x": 0, "y": 330 },
    { "id": "esp", "part": "DOIT Esp32 DevKit v1 improved", "x": 20, "y": 110 },
    { "id": "dht", "part": "DHT22 temperature-humidity sensor", "x": 347, "y": 230,
      "snap": { "pin": "VCC", "to": "bb.pin40J", "axis": "x|y (optional)", "offset": [0, -30.8] } }
  ],
  "shapes": [ { "a": "drv.ENA", "b": "drv.+5V-J1", "pad": 42, "fill": "#1a1a1a" } ],
  "wires":  [ { "from": "esp.3V3", "to": "bb.pin12Y", "color": "#cc1414", "route": "vh", "width": 32,
                "out": ["right", 150], "via": [ { "ref": "esp.D4", "dx": 330 } ] } ],
  "labels": [ { "ref": "esp.D4", "dx": -210, "text": "4", "size": 56, "leader": false } ] }
```

* `part` = a directory under `parts/`; `core` = an fzp basename in `fritzing-parts/core`.
* Pin refs: `<id>.<connector name from the fzp>` (duplicates get `.2`, `.3`: `GND.2`), or
  `<id>.c<N>` (connector id), breadboard holes `bb.pin12Y`, bbox anchors `<id>.@c/@t/@b/@l/@r/@tl…`.
* Routes: `direct` (default), `vh` (vertical then horizontal), `hv`; `out` = stub leaving the
  pin; `via` = intermediate points (`[x,y]` or `{ref, dx, dy}`); units of dx/dy/out = export
  units (1000 per inch, i.e. 100 per breadboard pitch).
* `rotation`: degrees CW, pivot = the part's own origin → a 180° part occupies
  `(x-w, y-h)…(x, y)`; 90° CW occupies `(x-h, y)…(x, y+w)`.
* `preview_scale` (default 2.5) only affects the PNG preview.

## Gotchas learned (keep)

* **Bundled-part file names and moduleIds must not contain spaces**, and every breadboard
  SVG needs a `<g id="breadboard">` layer group — otherwise the Fritzing CLI silently drops the
  part. `normalize_parts.py` fixes both for everything under `parts/`.
* **Qt SVG, not a browser:** custom part SVGs must use solid fills and `style=` attributes —
  gradients in `<defs>` and `opacity=` render as white/opaque in the CLI export
  (the 8×AA box was redrawn for that reason).
* **Breadboard rail holes skip every 6th number** (no pin8/14/20/26/32/38/44/50/56/62 on W/X/Y/Z).
  Top rails: Z = blue (−, outermost), Y = red (+); bottom: X = blue (−), W = red (+, outermost).
* **Bendable-leg parts (LED, electrolytic cap)** export their legs as anonymous paths, so only the
  body-side pin is extractable; place them with `snap.offset` = leg length (LED: −30.8 px).
* `partID` in the export = `modelIndex × 10`; `make_fzz.py` assigns modelIndex 1001 + instance index.
* Label sizes: a full-map figure is ~10 000 units wide and prints at ~170 mm — tags need size ≥ 80
  (staggered in two columns at 100-unit pin pitch); narrow figures are fine at 50–60.
* Wire crossings that are topologically forced (TX↔RX on the FTDI figure; the two-lead battery
  feeding two loads; the ESP32 5V/GND pair) are left as clean right-angle crossings — don't fight them.

## Parts (community, CC-BY-SA; sources)

| dir | source |
|---|---|
| DOIT Esp32 DevKit v1 improved, ESP32-CAM_FRONT-fixed, L298N-DC-motor-driver-improved, DHT22 temperature-humidity sensor, OLED-128x64-I2C-Monochrome-Display-GND-VDD, FTDI Basic Programmer, Getriebemotor (TT motor), TCRT5000 line sensor | github.com/Design-n-Techie/Fritzing_Libraries |
| Mini560 buck module | github.com/RafaGS/Fritzing |
| 8xAA_box | drawn here (derived from Adafruit's 4xAA switchable pack); 110×61 mm closed box, OFF-ON switch, red/black leads |

Core parts used: `breadboard2` (RSR03MB102 full-size), `arduino_Uno_Rev3(fix)`, `LED-generic-5mm`,
`resistor`, `capacitor_electrolytic_small`, `servo`, `SparkFun-Electromechanical-BUZZER-PTH-NS-KIT`.
