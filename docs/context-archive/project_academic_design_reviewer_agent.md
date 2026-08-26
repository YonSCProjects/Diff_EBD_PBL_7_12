---
name: Academic design reviewer agent
description: academic-design-reviewer subagent reviews design of Arduino_PBL_Program.md (master) and the EN+HE overview docs — title pages, headings, tables, APA-7 references, pagination, cross-doc consistency
type: project
---

The `academic-design-reviewer` subagent (defined at `.claude/agents/academic-design-reviewer.md`) reviews academic-publication design quality of the program-level documents:

- `Arduino_PBL_Program.md` — master document (English)
- `Arduino_PBL_Program_Overview.md` — executive overview (English)
- `Arduino_PBL_Program_Overview_he.md` — executive overview (Hebrew, RTL)

Reviews title-page conventions, heading hierarchy, table/figure captioning + numbering, APA-7 reference formatting, in-text citation consistency, pagination/orphan-heading prevention, appendix labeling, cross-doc consistency (master↔overview, EN↔HE), and PDF/HTML/DOCX print-readiness via the `md-to-pdf.config.js` / `md-to-pdf-he.config.js` embedded CSS.

**Modes:** `scan` (single file), `summary` (all three), `config` (CSS-only), `crossdoc` (master↔overview or EN↔HE), `explain`.

Read-only — proposes changes, does not edit. Complementary to `editorial-coherence`, `hebrew-translation-reviewer`, `article-verifier`, `visual-design-reviewer`, `pedagogical-card-reviewer`, `overview-gap-checker` — does not duplicate their scope.

**How to apply:** invoke when finishing a draft of any of the three program documents, before generating PDFs for submission, or after substantive edits to the references list or appendix structure.
