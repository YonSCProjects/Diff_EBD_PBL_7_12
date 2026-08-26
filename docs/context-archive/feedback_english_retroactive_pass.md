---
name: English retroactive pass is deferred but required
description: The English HTML task cards and reference cards for Project 1 need a visual polish pass (badge top-right, icons, inline R-ref circles, bold-fix CSS) — deferred during D.1 to prioritize Phase E, but Yon explicitly wants a complete English version alongside the Hebrew one
type: feedback
originSessionId: 3d210c3a-c0bd-44fd-9c8b-2b5b6675b02f
---
The full English retroactive pass for Project 1 HTML artifacts was deferred during Phase D.1 (2026-04-12) to move to Phase E faster. **Yon explicitly stated he wants a complete English version** — Hebrew is the workshop/local-peers language, but an English version is also needed.

**Why:** "at the end of the day I would like to have an english version of the project although at my workshop and among my locals pears we will use the Hebrew."

**How to apply:** After Phase E is complete (or during a natural pause), run the retroactive English pass on all Project 1 HTML artifacts:
1. Move `.card-id` badge from top-left to top-right for LTR English cards (CSS scoping: `[dir="ltr"] .card-id { right: 6mm; left: auto; }` or per-file inline style)
2. Add section icons (🏁, 🔌, 📋, 👀, ✅, 🪄, ⚠️, 💻) to English R1-R5 reference cards and English task cards — same icon placement as Hebrew
3. Add `.r-ref` inline circle spans wherever English cards reference R1-R5 in body text
4. Remove any parens around circled R-refs (E2 pattern)
5. Verify `.key` and callout blocks do NOT need the RTL bold-fix override (they're fine as-is for LTR English — the synthesized-bold issue is Hebrew-only)
6. English tutorial (`project_1_tutorial.html`) already has the Sketchbook workflow rewrite — no further fix needed there

**Scope:** 5 English reference cards (`reference_cards/R1-R5`) + 14 English task cards (`task_cards/T1_M1-M8, T2_M1-M5, T3`) + 1 English tutorial (already updated) = ~19 files total.

**When to remind Yon:** After Phase E is delivered, or when starting D.2 (Project 2), whichever comes first. The English pass is a visual-polish task that doesn't block any functional work, but it should be done before Yon shares the English version externally.
