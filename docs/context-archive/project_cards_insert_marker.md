---
name: Overview cards-insertion marker
description: build_overview_with_cards.js splits the overview markdown at the HTML comment <!-- INSERT_CARDS_HERE --> and interleaves the 19 Project 1 card PDFs at that point
type: project
---

`build_overview_with_cards.js` looks for the literal HTML comment `<!-- INSERT_CARDS_HERE -->` in the overview markdown. If present, it splits the markdown in two, renders each half to PDF via md-to-pdf, and merges as: **part1 + 19 card PDFs + part2**. If the marker is absent, card PDFs append at the end (legacy behavior).

**Why:** the user wants Appendix 1 (cards cover + 19 card pages) to physically precede Appendix 2 (budget) in the final PDF. The marker is placed after the cards-cover listing section and before the budget appendix.

**How to apply:** when editing the overview markdown structure, preserve the `<!-- INSERT_CARDS_HERE -->` marker at the desired physical card-insertion point. The marker currently sits between the "הכרטיסיות מצורפות בעמודים הבאים." line and the `# נספח 2 — תקציב` heading in the Hebrew overview.
