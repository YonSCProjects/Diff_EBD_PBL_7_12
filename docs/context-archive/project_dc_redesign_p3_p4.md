---
name: dc-redesign-p3-p4
description: "P3+P4 Hebrew task cards rebuilt as .dc.html locally (commit ae31f60) — the verbatim-text gate, the promoted design spec + checker, and the P5-P8 replay recipe"
metadata:
  node_type: memory
  type: project
  originSessionId: 4f98ca88-5db7-42fe-97d8-4266922384ce
---

**What.** 2026-07-05, commit `ae31f60`: all 27 P3+P4 Hebrew task cards rebuilt in the Claude-Design `.dc.html` design system **locally by Claude Code** (Yon asked to "apply the P1/P2 design language, don't change the words" — the DesignSync/Claude-Design hand-off was NOT used; see [[reference-designsync]]). Files: `P3_*_he.dc.html` (12) and `P4_*_he.dc.html` (15) in each project's `task_cards_he/`, plus per-folder `support.js` and `assets/` (wiring SVGs, P2 convention). Classic `_he.html` cards left in place — P3/P4 now carry BOTH flavors (unlike P1/P2 where classic was deleted, uncommitted WIP). Flavor-map + apply-to-both-files rule recorded in [[card-review-console]].

**The verbatim guarantee (reusable doctrine).** Claude Design's own P2 conversion silently reworded/condensed text. To enforce Yon's words-are-final rule mechanically: `check_text.js` (repo root since this commit) extracts every text segment (>8 Hebrew / >15 Latin chars) from the classic card and fails unless each appears whitespace-normalized in the dc file (+alt attrs; emoji/arrows stripped; inline tags fused). Gate ran 3× per card — author agent, independent verifier agent, final batch sweep — **27/27 clean, 0 rewordings, 0 repair rounds**. Usage: `node check_text.js <classic.html> <dc.html>` (exit 0 = clean; JSON with `missing[]`).

**The design spec (durable authoring source).** `dc_design_spec.md` (repo root, ~57KB) — full component library extracted verbatim from 8 P1/P2 exemplars: document skeleton (`<x-dc>`/`<helmet>`/DCLogic script + `$preview`), header band variants (V1/V2/planner V3), step-cards with `{{ toggleN }}`/`<sc-if value="{{ checkN }}">` checkboxes, warning/expected/done-when/stuck/celebration/skip-notice/diagram-frame/code-panel/choice-card/planner-field/R-ref-badge components, oklch token table, RTL + LTR-mono rules. **For P5–P8: author dc cards directly from this spec + check_text.js gate — no need to re-extract.**

**Conventions locked:** localStorage keys `tc_p3t1m1_checks` … `tc_p4t3_checks` (planners `tc_pNt3_checks`); header chip = classic subtitle verbatim (e.g. "פרויקט 3 • לא להתקרב יותר מדי"); classic milestone-badge line appears verbatim as header locator; images `./assets/<name>` (copy from `../images/`); renderVals loop to 20; celebrations on P3 T1_M6/T2_M5, P4 T1_M8/T2_M6; P4 soldering four-rules box = strong red variant, "קוראים למורה, תמיד" untouched.

**Build record:** workflow `wf_ae9aacd8-044`, 55 agents (1 spec extractor, 27 authors, 27 independent verifiers), ~5.6M subagent tokens, 0 errors. Headless render QA via scratchpad `shot.js` (puppeteer full-page screenshot; dialogs dismissed for card.js prompt; NODE_PATH must point at repo node_modules when scripts run from outside the repo).

**Open:** delete classic P3/P4 cards? (Yon's call — classic still feeds `build_cards_only.js` PDF bundles); the for_claude_design.zip hand-off is now moot for P3/P4 design (may still be wanted for Claude Design's own archive).
