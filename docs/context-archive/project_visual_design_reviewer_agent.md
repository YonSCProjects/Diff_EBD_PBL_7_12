---
name: Visual design reviewer agent
description: visual-design-reviewer subagent; expert in typography, page layout, tables, code blocks, icons, color/contrast, and print-ready quality for student-facing navigation cards, reference cards, and HTML tutorials
type: project
originSessionId: 3d210c3a-c0bd-44fd-9c8b-2b5b6675b02f
---
**What this is.** A read-only subagent at `.claude/agents/visual-design-reviewer.md` that reviews the visual and typographic design of student-facing HTML materials (navigation cards, reference cards, HTML tutorials) and the shared stylesheet. Reads CSS + HTML together. Read-only (Read, Grep, Glob, Bash), sonnet model, proposes rather than edits. Complements the `pedagogical-card-reviewer` which handles content/pedagogy.

**Why:** Yon explicitly asked for a SEPARATE agent for visual design (option C in the 2026-04-13 discussion), rather than expanding the pedagogical agent to include visual-design scope. The two skills — pedagogical design vs. visual/typographic design — are different specialties, and combining them would dilute both reviews. A separate agent also makes sense because visual design often requires stylesheet changes (affecting every card at once), which is a different scope of fix than pedagogical changes (which are usually per-card).

**How it works:**
1. Main agent dispatches `visual-design-reviewer` via the Agent tool with `subagent_type: visual-design-reviewer` and the target file path.
2. Agent reads the shared stylesheet (`task_cards/style.css` or linked CSS) AND the target HTML together — visual design cannot be evaluated from markup or CSS alone.
3. Agent walks through 10 design criteria (typography, page layout, tables, ASCII/code blocks, icons, visual hierarchy, color/contrast, print-ready quality, screen vs print parity, cross-card consistency).
4. Returns structured proposals with pattern citations, confidence levels, AND **"Scope of fix"** field (single card / multiple cards / stylesheet-wide) — Yon needs this extra field to decide whether a proposal is cheap or expensive.

**Four modes:**
- `scan` (default) — single-file deep review
- `summary` — directory-level roll-up of visual issues and drift between cards
- `css` — review the shared stylesheet itself, propose improvements affecting all cards
- `explain` — diagnostic for a specific visual concern + criterion

**Scope (what the reviewer checks):**
1. Typography — font stack appropriateness (Arial-first for Hebrew), font-size hierarchy, line height, bold/italic usage
2. Page layout and density — A4 portrait fit, print margins, section spacing, block alignment
3. Tables — width fit, column balance, cell padding, header distinction, RTL alignment
4. ASCII art, wiring diagrams, code blocks — fit without wrap, LTR isolation in RTL, filename prefix readability, legibility
5. Icons and symbols — emoji rendering at print size, grayscale fallback, Unicode consistency, icon placement, ✓ not V
6. Visual hierarchy — card-ID badge position, milestone-badge styling, h1 dominance, callout-box differentiation
7. Color and contrast — WCAG AA contrast ratios, grayscale printing fallback, Hebrew/English consistency
8. Print-ready quality — laminate-ready edges, printer-friendly (toner load), page-break behavior, watermarks/footers
9. Screen vs print parity — @media print rules, screen-hint hiding, link color rendering
10. Consistency across card family — drift between cards that should share visual signatures

**Out of scope (delegated to other agents):**
- Pedagogical content or structure → `pedagogical-card-reviewer`
- Hebrew grammar → `hebrew-translation-reviewer`
- English voice/style → `editorial-coherence`
- Citation accuracy → `article-verifier`
- Factual content corrections → flag as human-review
- Alternative template structures (template is established)
- Icon-system rewrites (unless an icon is actively broken)

**Key files the agent reads every invocation:**
- The target HTML file
- The shared stylesheet (`task_cards/style.css`)
- `Hebrew_Translation_Preferences_Log.md` Category E (visual/markup conventions E1–E6) for constraints to respect

**Established constraints the agent respects (not re-litigates):**
- Icon system: 🏁 milestone, 🔌 wiring, 📋 what to do, 👀 expected, ✅ done when, 🪄 stuck, ⚠️ warning, 💻 code, 🎉 celebration
- Pattern E4 Arial-first Hebrew font stack
- Pattern E5 no monospace on Hebrew text (only on LTR-isolated code/paths/filenames)
- Pattern E6 no box-level bold on callout classes under `[dir="rtl"]`
- Pattern E1 ✓ not V for checkmarks
- Pattern E3 card-ID badge top-left for Hebrew, top-right for English

**Philosophy (from the agent definition):** "The best visual design is invisible. The student notices the content, not the form. The worst visual design is anything that distracts, obscures, or gets in the way of what the card is trying to teach."

**When to dispatch:**
- When a new card is created (after pedagogical review) — visual design pass before print
- Before a batch of cards is laminated — one `summary` pass across the directory catches drift
- When Yon wants to modify the shared stylesheet — use `css` mode for a review of the stylesheet itself
- When printed cards look off (cramped, wrapped tables, illegible code blocks) — `scan` on the problem card

**When NOT to dispatch:**
- On Markdown source files (no CSS, no visual rendering) — visual design lives in HTML + CSS
- On the master document or overview — those use the `md-to-pdf` pipeline with its own config (a separate concern)
- On teacher-facing materials (setup checklists, troubleshooting crib sheets) — different visual requirements

**Activation status:** Agent created 2026-04-13; requires Claude Code restart to activate (same as the other custom subagents).
