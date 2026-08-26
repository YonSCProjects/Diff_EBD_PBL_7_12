---
name: Fritzing canonical sketches — Project 1
description: Canonical .fzz sources for Project 1 wiring diagrams live in images/fritzing/; the project uses full-size RSR03MB102 breadboard, not the MCP default Half_breadboard_v2
type: reference
originSessionId: a20dca7b-3b4d-4454-a446-c6dad0d7f713
---

## Files (canonical sources)

`Arduino_Projects/Project_1_Light_Signals/images/fritzing/`
- `w0_empty_breadboard.fzz` — empty breadboard reference
- `w1_single_led.fzz` — one LED on pin 9
- `w2_two_leds.fzz` — two LEDs on pins 9 and 10
- `w3_leds_and_button_pulldown.fzz` — two LEDs + button + pull-down resistor
- `w4_three_leds_chasing.fzz` — three LEDs (no button) for chasing pattern
- `w5_three_leds_and_button_pulldown.fzz` — three LEDs + button + pull-down
- `w_arduino_only.fzz` — Arduino without breadboard

Exported SVGs land in `Arduino_Projects/Project_1_Light_Signals/images/w*_breadboard.svg` (also `_schematic.svg`, `_pcb.svg`).

## Breadboard part — full-size, NOT half

The workshop uses a full-size ~830-tie-point breadboard. All Project 1 sketches use **`Breadboard-RSR03MB102-ModuleID`** (Fritzing search title "RSR 03MB102 Breadboard"). This contradicts the global `fritzing_wiring_rules` MCP doc, which still says to use `Half_breadboard_v2`.

**Why:** The half-breadboard the MCP defaults to is visually different from the workshop's actual breadboard, which confused students.

**Why RSR03MB102 specifically:** Its pin-naming convention (`pin1A`..`pin63J`) is compatible with the half-breadboard's (`pin1A`..`pin30J`), so existing wires connecting to rows ≤30 keep working when the breadboard is swapped. The "Generic Bajillion Hole Breadboard" (`BreadboardModuleID`) uses incompatible naming (`A98`, `E99`) and would break wires.

## How to swap an existing half-breadboard sketch to full

1. Open the .fzz with Python's `zipfile` (or unzip + manual rezip)
2. Inside the .fz XML, replace `0152b316-ca6e-11ee-a6fa-8be78db221f8BreadboardModuleID` with `Breadboard-RSR03MB102-ModuleID`
3. Re-zip the .fzz
4. Export via `fritzing_export` — wires resolve fine because pin IDs are compatible

## Building from scratch

Don't hand-build with raw `fritzing_add_part` — the MCP primitives in `circuit_builder.py` were tuned for Half_breadboard_v2's coordinate system. For new sketches, easiest is to copy an existing .fzz from `images/fritzing/` and modify with the part-add/move/wire MCP tools, or rebuild after extending the helpers to support RSR03MB102 coordinates.
