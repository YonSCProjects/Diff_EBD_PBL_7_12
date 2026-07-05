# Project 4 wiring-diagram sources (hybrid pipeline)

The Fritzing parts library has no L298N driver, TCRT5000 line sensor, or
4xAA holder, so the P4 diagrams are **hybrid**: a real Fritzing export as
the base, plus labeled SVG module blocks and wires composited on top by
`inject_modules.js`.

## Files

| File | Role |
|---|---|
| `w_p4_01_motors_to_driver.fzz` | two real `gear-motor_2` parts, flanking; base for w_p4_01 |
| `base_ab.fzz` | Arduino + breadboard + GND→(−) rail wire (P1 `w1_single_led.fzz` stripped of LED/resistor/2 wires); base for w_p4_02 / 04 / full |
| `w_p4_03_signal_pins.fzz` | Arduino only (copy of P1 `w_arduino_only.fzz`); base for w_p4_03 |
| `w_p4_05_button_tier3.fzz` | pure Fritzing button + 10k pulldown on D2 (P1 `w3` stripped of LEDs); exported as-is, no compositing |
| `inject_modules.js` | compositor — module factories `l298n`, `sensor`, `battery`, `motor` + anchor-based Fritzing-style wires + viewBox expansion |
| `spec01/02/03/04/_full.json` | wire/module specs for w_p4_01, _02, _03, _04 and the full map (`w_p4_01_driver_wiring`, used by T1_M4 + T2_M1) |

## Regenerating

```
# export a base (via the Fritzing MCP): fritzing_export <fzz> <outdir> svg
node inject_modules.js <base_breadboard.svg> <out.svg> <specNN.json>
node svg_to_png.js <out.svg> <preview.png>   # visual check (repo root)
```

Key flat coordinates (both Arduino-bearing bases share them):
D5–D12 = x 2249.6 → 1489.6 step −100 at y=100 (D8 jumps to 1889.6);
5V = (1749.6, 2000), GND = (1949.6, 2000); breadboard rails:
(−) blue row y=755.556 (top), (+) red row y=2555.56 (bottom),
holes at x = 3240.56 + n·100.
