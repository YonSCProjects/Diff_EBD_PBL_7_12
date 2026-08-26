---
name: Build-output files must reflect every content change
description: Yon works from the build_output PDFs, not the source MDs or source HTMLs — stale build outputs = invisible work. Every content change must propagate to build_output before the task is considered done.
type: feedback
originSessionId: e680ace2-857b-49f5-9ebd-56985d6eee86
---
**Rule.** Every content change must end with its affected `build_output/` artifact(s) regenerated. A task is not done until `build_output/` reflects the change.

**Why:** Yon's working view of the project is the `build_output/` folder — that's what goes to the PSGA, to the teachers, and to his own reading queue. If I edit `Arduino_Principles.md` or a navigation card and report "done" without rebuilding, Yon opens the PDF and sees stale content. It caused a recovery cycle on 2026-04-18 when I updated `Arduino_Principles.md` but not the overview MDs that the PDFs are actually built from.

**How to apply.** Before declaring any content change done, map the edited file(s) to the build outputs they affect, then rebuild:

| Source file(s) edited | Build output(s) that must be regenerated | Build command |
|---|---|---|
| `Arduino_PBL_Program.md` | `build_output/Arduino_PBL_Program.{pdf,html}` | `npx md-to-pdf --config-file md-to-pdf.config.js Arduino_PBL_Program.md` (+ `--as-html`), then `mv` into `build_output/` |
| `Arduino_PBL_Program_Overview.md` | `build_output/Arduino_PBL_Program_Overview.{pdf,html,docx}` | `node build_overview_with_cards.js en` |
| `Arduino_PBL_Program_Overview_he.md` | `build_output/Arduino_PBL_Program_Overview_he.{pdf,html,docx}` | `node build_overview_with_cards.js he` |
| Any file in `Arduino_Projects/Project_1_Light_Signals/reference_cards/` or `task_cards/` (EN + HE) | `build_output/Arduino_PBL_Program_Overview.pdf` AND `..._he.pdf` (cards are embedded in the appendix via puppeteer) | both `build_overview_with_cards.js` runs |
| `Arduino_Projects/Project_1_Light_Signals/Arduino_Project_1.md` | `build_output/Arduino_Project_1.{pdf,html}` | `npx md-to-pdf --config-file md-to-pdf.config.js Arduino_Projects/Project_1_Light_Signals/Arduino_Project_1.md` (then `mv`) |
| `Arduino_Principles.md` | **None directly.** Principles live inside `Arduino_PBL_Program.md` (§4) and the overviews, so if Principle text changes *meaningfully* in the source doc, the three built docs that restate the principles must also be updated and rebuilt. |
| Anything under `teacher_materials/` | No `build_output/` counterpart — those HTMLs are printed directly from their source location. Still worth verifying they print correctly. |

**Critical caveat.** `Arduino_Principles.md` is a **source-of-truth** document but is **not itself** a build-output source. The three documents that restate the principles each carry their own copy:
- `Arduino_PBL_Program.md` §4 (master document, full depth)
- `Arduino_PBL_Program_Overview.md` (executive summary, compact)
- `Arduino_PBL_Program_Overview_he.md` (Hebrew executive summary)

When adding/modifying a principle in `Arduino_Principles.md`, **also** update the three documents that restate principles. Grep for indicators like "nine principles" / "תשעה עקרונות" / "Principle 9" before calling the task done.

**Pre-declaration checklist:**
1. List every file I edited in this task.
2. Cross-reference against the table above.
3. If any row applies, run the build command.
4. Verify the page count of the output PDF changed appropriately (principle additions should add pages).
5. Then declare done.
