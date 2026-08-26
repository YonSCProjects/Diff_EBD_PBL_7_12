---
name: Fritzing LED color export bug
description: Fritzing CLI silently drops LEDs whose color property isn't "Red (633nm)"; Yellow/Green LEDs vanish from the SVG export
type: reference
originSessionId: e680ace2-857b-49f5-9ebd-56985d6eee86
---
**Symptom**: A `.fzz` sketch with multiple LEDs — e.g., LED1=Red, LED2=Yellow, LED3=Green — renders only LED1 in the exported SVG. Wiring, resistors, and pin connections are correct; the non-Red LED bodies are just missing.

**Root cause**: Fritzing's core part `C:\Program Files\Fritzing\fritzing-parts\core\LED-generic-5mm.fzp` (moduleId `5mmColorLEDModuleID`) defines only `Red (633nm)` as the valid color property value. Non-matching values (`Yellow`, `Green`, etc.) cause the CLI exporter to silently skip the part. The SVG ends up with only the LEDs that match the default color.

**Fix applied for Project 1 w2/w3/w4/w5**: Patched the `.fzz` XML via jszip to replace `value="Yellow"` and `value="Green"` with `value="Red (633nm)"`. Trade-off: all LEDs render the same red color in the breadboard image — colour differentiation is lost. Acceptable because card captions and wiring diagrams state pin numbers explicitly; students pick their own colours in practice.

**How to apply**: When generating a .fzz with multiple LEDs in the Project 1 Arduino PBL workflow, set **all** LED color properties to `Red (633nm)`. To genuinely render distinct colours, use per-colour Fritzing parts (e.g., `LED-green-5mm.fzp`) rather than the generic `5mmColorLEDModuleID`. To check an exported SVG for missing LEDs, grep for `partID="[0-9]+"` and confirm the unique count matches expected parts+wires.

**Candidate for global Fritzing MCP rules** (`C:\Fritzing mcp\CLAUDE.md`): not persisted there yet — ask Yon before appending globally.
