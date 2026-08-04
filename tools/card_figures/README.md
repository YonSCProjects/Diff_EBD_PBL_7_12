# Card-figure tools

Small helpers for the Hebrew card figures. Run from the repo root
(`NODE_PATH` already resolves; puppeteer comes from the repo's node_modules).

| script | what it does |
|---|---|
| `find_part.js <fritzing.svg>` | lists every `g[partID]` with its bounding box — use it to identify which part is the button/LED/resistor |
| `extract_part.js <fritzing.svg> <partID> <out.svg> [pad]` | pulls one part into a tightly-cropped standalone SVG (vector, crisp at any size). This is the **preferred** source for a component illustration — see rule V4 in `Card_Editing_Preferences_Log.md` |
| `holes.js <breadboard.png>` | finds the breadboard hole rows/columns by darkness profile and prints them as percentages — use it to place figure overlays (טור / שורה / החריץ) on real coordinates instead of eyeballing (rule V2) |

Measured once for `Project_1/task_cards_he/assets/m3_breadboard.png`:
rows at 41.2 / 44.5 / 47.5 / 50.5 / 53.6 % (top half) and 63.1 / 66.1 / 69.3 / 72.4 / 75.4 % (bottom half),
pitch ≈ 3.05 %, board spans x ≈ 33–97 %.
