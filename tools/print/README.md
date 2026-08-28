# tools/print — printable task-card PDFs

    node tools/print/build_print_pdf.js build_output/Project_1_Cards_he.html \
         build_output/Project_1_Task_Cards_he_print.pdf

Add `--all` to include the six reference cards; by default it prints task cards only, since the
R cards are the teacher's (rule C7).

Three rules, in the order they are allowed to win:

1. **Every שלב starts a new page.** Each card carries one "שלב N מתוך M" in its header band, so a
   card is a stage and a stage owns its sheet from the top.
2. **Nothing is cut mid-section.** Every atomic block — step row, callout, diagram frame,
   done-when box, planner field — gets `break-inside: avoid`, and every heading is bound to the
   block it introduces so a title is never stranded at the foot of a page.
3. **As little white as possible.** Rule 1 puts the slack at the end of each stage, where the next
   stage cannot reclaim it. Two things claw it back without touching a letter of type: the
   vertical rhythm is tightened for paper (margins and body padding down about a third — screen
   spacing reads as slack in print), and a stage that overruns its last sheet by a little is
   scaled down just enough to save it.

`Project_N_Cards_he.zooms.json` holds the per-stage shrink for that bundle, worked out by
measuring the rendered PDF rather than predicting from card height — the break rules push content
forward, so a stage's sheet count cannot be derived from how tall it is. The script picks the file
up automatically. Shrinks are floored at 90%, which keeps 16 px body type above 14 px.

Delete the .zooms.json (or pass `--zooms=` a different file) to build with no shrinking at all.
Fonts are embedded as data: URIs, so this builds and prints identically with no network.
