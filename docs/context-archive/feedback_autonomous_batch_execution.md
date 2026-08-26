---
name: Autonomous batch execution on reviewer passes
description: For large reviewer-driven batch fixes across many cards, Yon trusts judgment calls and prefers one end-to-end run over step-by-step confirmation
type: feedback
originSessionId: 3d210c3a-c0bd-44fd-9c8b-2b5b6675b02f
---
For large reviewer-driven batch fixes across many cards (both pedagogical-card-reviewer and visual-design-reviewer applied to a directory), Yon prefers a single end-to-end autonomous run over step-by-step confirmations. Exact instruction on 2026-04-13: *"run this task from beginning to end without asking any permissions from me. Make decisions yourself, I trust you. I'm going to rest and will review all changes later."*

**Why:** Yon's 18-card Project 1 Hebrew artifact family had dozens of HIGH + MEDIUM proposals across two reviewer dimensions. Asking per-proposal would have been hundreds of confirmations over hours. He explicitly wanted to review a single consolidated diff after the fact, not micromanage the batch.

**How to apply:**
- When given a "run from beginning to end" directive on a reviewer batch, dispatch reviewers in `summary` mode (directory-level, not per-card) to avoid 2N agent calls for N cards.
- Apply all HIGH proposals by default.
- Apply MEDIUM proposals when the judgment is clear; skip MEDIUM ones tagged by the reviewer as "flag for Yon's preference" or requiring visual/print-size confirmation and note them in the commit message under "Skipped."
- Prefer stylesheet-wide fixes over per-card duplication when the reviewer indicates the issue is family-wide.
- Commit the whole batch as ONE commit with a descriptive message listing what was done and what was skipped (Yon's review lens is the diff + commit log, not a per-card walk).
- Do NOT stop to ask about individual proposals. Decide and proceed.

**Counter-example — when to ask:** If a proposal would rename a file, delete content substantively, change a cited research claim, or touch master-document structure (vs. per-card polish), stop and confirm. The autonomous mandate covers reviewer batch fixes on HTML cards and stylesheet, not the master doc or overview.
