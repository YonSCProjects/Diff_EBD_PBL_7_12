---
name: Fritzing MCP server
description: Project-scoped MCP server for generating Fritzing breadboard diagrams; configured via .mcp.json, source at C:\Fritzing mcp
type: reference
---

The project has a Fritzing MCP server configured in `.mcp.json` (project root):

- **Command:** `C:\Python314\python.exe -m fritzing_mcp`
- **CWD:** `C:\Fritzing mcp`
- **Source tree:** `C:\Fritzing mcp\fritzing_mcp\` (server.py, circuit_builder.py, parts.py, sketch.py, exporter.py, models.py)
- **Capabilities:** create/edit Fritzing sketches, add parts to breadboard, connect parts, export to SVG/PNG, generate BOM.

Use this MCP when generating breadboard illustrations — e.g., the 4 R1 wiring diagrams (single LED on pin 9, two LEDs on pins 9+10, LEDs+button with pull-down on pin 2, three LEDs on pins 9+10+11). Previously the image-slot placeholders in R1 cards pointed to external Wikimedia/SparkFun candidates that didn't perfectly match the pin assignments — this MCP lets us build exact-match diagrams.

Python dependencies (`mcp[cli]`, `pydantic>=2`, `lxml>=5`) were installed 2026-04-13 into the system Python 3.14 via `python -m pip install`.

**Also present:** `C:\Fritzing mcp\LED_Resistor_Series.fzz` — sample Fritzing sketch.

Image placeholders only exist in English cards (T1·M3, T1·M5, T1·M7, R1) — Hebrew cards were drafted without them. When adding real images, replace the `.living-placeholder` / `.image-slot` divs in the English cards with `<img>` tags, and mirror the structure into Hebrew cards.
