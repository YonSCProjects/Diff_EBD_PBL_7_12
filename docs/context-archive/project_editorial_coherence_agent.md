---
name: Editorial-coherence agent + preferences log
description: editorial-coherence subagent that learns Yon's editorial voice from past edit requests and proposes consistent revisions to other parts of the text; paired with Editorial_Preferences_Log.md as its knowledge source
type: project
originSessionId: 3d210c3a-c0bd-44fd-9c8b-2b5b6675b02f
---
The project has a dedicated **editorial voice coherence** pipeline set up alongside the article-verifier:

1. **Subagent** at `.claude/agents/editorial-coherence.md` — learns Yon's editorial preferences (tone softening, inclusive framing, terminology choices, audience specificity, empowering-rather-than-accusatory register) and, when asked, scans a target file for places that drift from the established voice. Returns proposed revisions (before/after + rationale + confidence) for human review. Has three modes: `learn` (update pattern library from recent edits), `scan` (propose revisions for a file or section), `explain` (diagnostic only).
   - Tools: Read, Grep, Glob, Bash (read-only for git log/diff)
   - Model: sonnet
   - **Does NOT modify files directly** — it proposes, the human approves, the main agent applies.
2. **Editorial_Preferences_Log.md** at the project root — the primary knowledge source for the agent. Maintained by the main Claude Code agent as working memory. Captures editorial patterns with a short name, a 1-line rule, a "why" note, and 1–3 before/after examples. Started 2026-04-10 during Phase C drafting of the Arduino PBL master document.
3. **Git history** — secondary knowledge source. The agent can run `git log --follow -p -- <file>` to see the full change history of a target file and infer patterns from the diffs alone if the preferences log is missing or sparse.

**Why:** Yon is iteratively editing the Arduino PBL master document (~30–50 pages) section by section. Every time Yon requests a voice/tone change (e.g. "curriculum → program," "soften absolute claims to 'many of them'," "label examples as illustrative not exhaustive," "no Ministry-specific naming," "forward-looking endings not accusatory absolutes"), that preference should propagate consistently to the rest of the document. Manually propagating is tedious and error-prone; the editorial-coherence agent automates the "scan for drift and propose revisions" step.

**How to apply:**
- When Yon requests a voice/tone change that is likely to recur elsewhere in the document, update `Editorial_Preferences_Log.md` with a new pattern or reinforce an existing one BEFORE drafting the next section. The log is the shared memory between sessions.
- When a section is drafted and ready for review, consider dispatching the `editorial-coherence` agent in `scan` mode to check it against the established voice, BEFORE showing it to Yon. This catches drift early.
- If the subagent is not yet discoverable (see session-restart caveat below), dispatch via `general-purpose` with the agent's system prompt inlined.
- NEVER apply the agent to §9 Honest Limitations or similar transparency sections. Pattern 8 in the preferences log explicitly excludes limitations/caveats passages — those should be direct and blunt, not softened.
- The agent proposes, the human approves, the main agent applies. Do not have the agent make direct edits.

**Session-restart caveat:** New subagents added to `.claude/agents/` during a session are NOT discoverable as `subagent_type: editorial-coherence` until the session is restarted. During the creation session itself, dispatch via `subagent_type: general-purpose` with the agent's instructions inlined. From the next session onward, the native subagent type works.

**Patterns captured in the preferences log as of 2026-04-10 (Phase C drafting of §1):**
1. Terminology: "program" not "curriculum"
2. Audience: "potential evaluating and funding organizations" not "Israeli Ministry of Education"
3. Inclusive framing: label examples as illustrative not exhaustive
4. Softened claims: "many of them" / "most of these students" / "often" over universal claims
5. Soft, forward-looking endings, not accusatory absolutes
6. Terseness: when the point is made, stop (no "as opposed to X" tails)
7. Structural mismatch language, not student-failure language ("did not meet their needs" not "did not survive")
8. Honest limitations are NOT softened — the exception where Pattern 4 and Pattern 5 do not apply
