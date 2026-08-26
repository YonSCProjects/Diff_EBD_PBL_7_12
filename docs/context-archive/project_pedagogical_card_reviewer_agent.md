---
name: Pedagogical card reviewer agent
description: pedagogical-card-reviewer subagent; expert in applying the program's 9 design principles and EBD-appropriate simplicity/clarity criteria to student-facing navigation cards and reference cards
type: project
originSessionId: 3d210c3a-c0bd-44fd-9c8b-2b5b6675b02f
---
**What this is.** A read-only subagent at `.claude/agents/pedagogical-card-reviewer.md` that reviews student-facing navigation cards and reference cards against the program's 9 research-grounded design principles plus established simplicity/clarity criteria for the EBD student population at Agourim School. Read-only (Read, Grep, Glob, Bash), sonnet model, proposes rather than edits, modeled on the same structured-proposal pattern as `editorial-coherence` and `hebrew-translation-reviewer`.

**Why:** Yon asked for a pedagogical expert agent whose specialty is making navigation cards "as simple, clear, and easy to follow as possible" while ensuring they embody all 9 design principles. The other reviewer agents are linguistic (Hebrew translation) and editorial (English voice); neither is competent to judge whether a card's *pedagogical design* serves a student with a difficult school history. This agent fills that gap.

**How it works:**
1. Main agent dispatches `pedagogical-card-reviewer` via the Agent tool with `subagent_type: pedagogical-card-reviewer` and the target card file path.
2. Agent reads `Arduino_Principles.md` (canonical 9 principles with evidence) and the target card.
3. Agent walks through the 9 principles one-by-one plus additional simplicity/clarity criteria (reading load, visual hierarchy, concreteness, emotional register, stuck-protocol quality).
4. Returns structured proposals with pattern citations and confidence levels — ordered by confidence (high first).
5. Main agent presents high/medium-confidence proposals to Yon; applies approved changes.

**Three modes:**
- `scan` (default) — single-card deep review with structured proposals
- `summary` — directory-level roll-up identifying the most common issues and cards needing the most attention (abbreviated proposals)
- `explain` — diagnostic: given a passage + principle number, explain match or violation

**Scope (what the reviewer checks):**
- All 9 principles (predictable routine, navigation card traces path, physical-first, 15-min milestones, structured autonomy, movement, Claude Code dual-channel, relationship is multiplier, teacher sustainability)
- Simplicity/clarity criteria: reading load, sentence length, visual hierarchy, icon consistency, concreteness, emotional register, stuck-protocol quality
- For Tier 1 cards: Channel A Level 1 indication; together-milestone pattern on M1
- For Tier 2 cards: Channel A Level 2 + (א)(ב)(ג) discipline references
- For Tier 3 planners: Channel A Level 3 + free dialogue framing

**Out of scope (explicitly delegated to other agents):**
- Hebrew grammatical corrections → `hebrew-translation-reviewer`
- English style/voice issues → `editorial-coherence`
- Citation accuracy → `article-verifier`
- Content factual corrections (wrong pin numbers, wrong resistor values) → flag as human-review, don't propose specific fix
- Structural reorganization of the card template (template is established)
- Visual design changes beyond established icon/emphasis conventions

**Key files the agent reads every invocation:**
- `Arduino_Principles.md` — primary source of truth (9 principles with design rules)
- `Arduino_PBL_Program.md` §5.2 (7-phase session structure) and §5.3 (card template) — operational context
- `Hebrew_Translation_Preferences_Log.md` — for Hebrew cards, to avoid duplicating that reviewer's work
- `Editorial_Preferences_Log.md` — for English cards, to avoid duplicating the editorial-coherence reviewer

**When to dispatch:**
- After drafting any new navigation card or reference card (Hebrew or English), before asking Yon to review
- On a whole-directory audit of `task_cards_he/` when Yon wants to know which cards need the most attention
- When a principle's interpretation is contested — the `explain` mode returns a diagnostic without proposing changes

**When NOT to dispatch:**
- On teacher-facing documents (setup checklists, troubleshooting crib sheets) — different audience, different criteria
- On the master document or overview — those are not navigation cards
- On the per-project Markdown source files — those are drafts; the HTML cards generated from them are the agent's target
- When Yon has already reviewed the card and explicitly approved it without pedagogical concerns

**Philosophy (from the agent definition):** "The best card is one a stuck student can pick up, read, and get unstuck from without anyone nearby. The worst card is one the student cannot use without the teacher decoding it."

**Honest caveat:** The agent is as good as the canonical principles document it reads. If `Arduino_Principles.md` drifts from the master document's §4 principles (as it did briefly between 2026-04-12 when Yon renamed Principles 2 and 8 in the overview but the canonical document still had the old names), the agent's reviews will reflect whichever version it reads. On 2026-04-13 the canonical document was updated to match the new Principle 2 ("navigation card traces the path") and Principle 8 ("the relationship is the multiplier") names, and all `task card` → `navigation card` references were propagated globally across the 20-section document. Future renamings must be propagated to the canonical document *before* dispatching the agent.
