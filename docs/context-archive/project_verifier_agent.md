---
name: Article verifier agent + hook
description: Project has a dedicated article-verifier subagent and a PostToolUse hook that auto-dispatches it when project markdown files change
type: project
originSessionId: 3d210c3a-c0bd-44fd-9c8b-2b5b6675b02f
---
The project has a citation-verification pipeline set up:

1. **Subagent** at `.claude/agents/article-verifier.md` — verifies that academic citations are real (authors, journal, year, DOI) using Crossref + WebSearch. Has three modes: `sweep` (all files), `incremental` (one file), `single` (one citation).
2. **PostToolUse hook** in `.claude/settings.json` — fires on Edit/Write/MultiEdit of any `*.md` file in the project root (excludes `.claude/`, `.git/`, `memory/`, and `Verification_Log.md` itself). Injects a system reminder telling the orchestrator to dispatch the verifier in incremental mode.
3. **Verification_Log.md** at project root — the single source of truth for what has been verified. Three tables: Verified / Partial-Corrected / Unverified-REMOVED.

**Why:** User's research standard is 100% verified citations only. Unverified articles must be removed and never used as a basis for analysis. Initial sweep on 2026-04-10 processed 78 unique citations: 66 verified, 12 corrected in place (mostly wrong journal names), 0 fabricated.

**How to apply:**
- When adding a new citation to any project doc, expect the hook to fire and either dispatch the verifier yourself or follow the system-reminder's instruction to do so.
- New subagents added to `.claude/agents/` are NOT discovered mid-session — they require a session restart before `subagent_type: article-verifier` works. In the meantime, dispatch via `general-purpose` with the verifier's instructions inlined.
- Never silently drop a citation. Unverified ones go into the "REMOVED" table of Verification_Log.md with the original text + search attempts, so we never re-check them.
- Crossref (`https://api.crossref.org/works?query.bibliographic=...`) is the fastest verification path — use it before falling back to WebSearch.
- **Year-disagreement convention:** when Crossref metadata and the publisher's own front matter/DOI slug disagree on publication year (common for late-2021/early-2022 papers that Crossref backdates), prefer the **publisher front matter and DOI slug** over Crossref. Example: Berrezueta-Guzmán & Robles-Bykbaev "Robotic Technologies in ADHD Care" — Crossref says 2022, IEEE Access and DOI `10.1109/access.2021.3137082` say 2021. Project uses 2021. When making a correction like this, propagate across ALL source files so the year is consistent everywhere, and note the disagreement in the Verification_Log row.
