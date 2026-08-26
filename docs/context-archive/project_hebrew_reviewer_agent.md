---
name: Hebrew translation reviewer agent
description: hebrew-translation-reviewer subagent + Hebrew_Translation_Preferences_Log.md; learns Yon's Hebrew translation preferences from past edits and proposes consistent revisions on new Hebrew translations
type: project
originSessionId: 3d210c3a-c0bd-44fd-9c8b-2b5b6675b02f
---
**What this is.** A read-only subagent at `.claude/agents/hebrew-translation-reviewer.md` that reviews Hebrew translations of project materials against a preferences log at `Hebrew_Translation_Preferences_Log.md` (project root). Modeled on the existing `editorial-coherence` agent: proposes revisions rather than editing files, reads git history as secondary evidence, returns structured before/after proposals with confidence levels.

**Why:** During the 2026-04-11 Hebrew parity pass of reference cards R1-R5, Yon made many linguistic corrections that reveal a coherent set of preferences (plural impersonal verb form, first-person plural inclusive framing, hif'il-over-kal for causative actions, adjective-over-participle for "starter/initial," unified vocabulary `גרסה` for both tier and Claude Code level, pruned English calques, tight prose, circled inline R-references, no monospace on Hebrew, no box-level bold on callouts). Rather than re-asking the same corrections on H.3 (Tier 1 task cards), H.4 (Tier 2 + Tier 3 planner), H.5 (HTML tutorial), H.6 (Channel B scaffold), and the retroactive English-to-Hebrew passes for Projects 2-8, the reviewer agent should catch these drifts automatically during drafting. Yon explicitly asked for this: *"let's add to our agents team an agent that will review the Hebrew translation and will try to identify wrong or not ideal word selections and other issues that are common to translation to Hebrew."*

**How it works:**
1. Main agent drafts a new Hebrew translation (task card, tutorial section, etc.).
2. Main agent dispatches the `hebrew-translation-reviewer` subagent via the Agent tool with `subagent_type: hebrew-translation-reviewer` and the target file path in the prompt.
3. Reviewer reads `Hebrew_Translation_Preferences_Log.md`, the target file, and optionally the git history of neighboring Hebrew files. Returns a structured proposal list (before/after pairs, pattern citations, confidence levels).
4. Main agent presents high/medium-confidence proposals to Yon for approval; applies approved changes; logs new patterns back to the preferences log if Yon introduces something novel.

**Scope (what the reviewer checks):** verb form (A1 plural impersonal, A2 first-person plural inclusive, A3 hif'il-over-kal for causative, A4 active-over-passive), lexical choices (B1 adjective-over-participle, B2 hif'il-gerund over kal action noun, B3 natural-Hebrew verbs, B4 unified `גרסה`), phrasing (C1 anti-calque, C2 section titles with explicit subjects, C3 masculine default for specific male referent), prose tightening (D1 cut filler/moralizing, D2 aphorisms over explanations, D3 declarative over procedural), visual/markup (E1 Unicode over Latin markers, E2 circled R-refs no parens, E3 badge corner opposite heading, E4 Arial-first font stack, E5 no monospace on Hebrew, E6 no box-level bold on callouts), workflow (F1 silently fix fast-typing typos), Claude Code terminology (G1 channel names Latin A/B, G2 metacognitive markers (א)(ב)(ג)).

**Out of scope (what the reviewer does NOT check):** general Hebrew grammar unrelated to the preferences log, content accuracy, research claims, citation formats, structural reorganization, style in sections Yon explicitly exempted, typos that Yon would catch on re-read (those go in a separate "Mechanical issues" output section, not in the style proposals).

**Evidence base caveat:** The preferences log was bootstrapped from a single review pass (R1-R5 reference cards, 2026-04-11). Most patterns have 1-2 examples, not 3+. The reviewer is instructed to cap confidence at "medium" for patterns with 1-2 examples and at "low" for patterns in the "not yet established" section. Confidence will grow as more Hebrew content passes through review.

**Key files:**
- `.claude/agents/hebrew-translation-reviewer.md` — agent definition (frontmatter: name, description, tools: Read/Grep/Glob/Bash, model: sonnet)
- `Hebrew_Translation_Preferences_Log.md` (project root) — primary source of truth for patterns. Seven categories (A verb form, B lexical, C phrasing, D prose tightening, E visual/markup, F workflow, G Claude Code terminology). Structured entries with pattern ID, rule, why, examples.

**When to dispatch:**
- After drafting any new Hebrew content (task card, reference card, tutorial section, Channel B scaffold) and before asking Yon to review it.
- After applying a batch of user-requested Hebrew edits, to catch consistency drift across the affected section.
- On `learn` mode when Yon says "the preferences log feels out of date" — reviewer reports newly-observed patterns for main-agent evaluation but does not modify the log itself.

**When NOT to dispatch:**
- On files that contain no Hebrew.
- On files where the Hebrew was translated in the same session and Yon already approved it without asking for review.
- As a replacement for Yon's own review — the reviewer flags drift; Yon has the final word.
