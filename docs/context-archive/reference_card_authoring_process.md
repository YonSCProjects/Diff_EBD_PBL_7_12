---
name: card-authoring-process-doc
description: card_authoring_process.md at repo root documents the full 6-step task-card creation process (spec → check_text gate → reviewers → GPT Hebrew pass → rebuild → review console)
metadata: 
  node_type: memory
  type: reference
  originSessionId: 23475edf-dbb3-4a71-8074-6f8e659f8622
  modified: 2026-08-20T08:52:32.596Z
---

`card_authoring_process.md` (repo root, written 2026-08-20) is the single consolidated write-up of the Hebrew `.dc.html` task-card creation process. Read it instead of re-assembling the process from [[dc-redesign-p3-p4]], [[project-gpt-hebrew-pass]], and the reviewer-workflow memory. Covers: authoring from `dc_design_spec.md`, wiring diagrams via the Fritzing MCP (canonical .fzz sources, RSR03MB102 breadboard, LED-color bug, SVG compositing), the `check_text.js` verbatim gate, the guarded reviewer-agent pipeline, the `improve_hebrew_gpt.js` vet-and-apply pass, rebuild steps (incl. `build_card_nav.js`), Yon's review-console round + /learn-changes, and the Claude Design origin story (why it's no longer a step).
