---
name: arduino-project-2-reaction-time-game-built
description: "Project 2 full student-facing artifact family built and committed (Phase D.2); pin map, build invocation, and two deferred follow-ups"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4d0de021-d16a-417d-8e86-30ad5107e3d9
---

**What.** On 2026-06-08 the full Project 2 artifact family was built and committed (`110aa19` on master, 61 files, not yet pushed). This is the D.2 work that [[project_arduino_pbl_program]] listed as deferred. Scope delivered = the user-approved "all phases 1–4" (everything except Phase-5 teacher setup/troubleshooting sheets).

**Project 2 = Reaction-Time Game / משחק זמן תגובה.** Arduino waits random 2–5 s → LED on → press button fast → `millis()` measures reaction → reports it. Dir: `Arduino_Projects/Project_2_Reaction_Time_Game/`.

**Built (HE source-of-truth + EN parallel):**
- 13 task cards: Tier 1 M1–M6 (V1), Tier 2 M1/M2/M2b-conditional/M3/M4/M5 (V2), Tier 3 planner (V3).
- Reference cards R0–R5: R0/R2/R3/R4 adapted from P1, R1 (wiring) + R5 (sketch index) new.
- 5 `.ino`: `01_wait_flash_measure`, `02_wait_flash_measure_buzzer`, + 3 Tier-2 starters (`T2_three_led_feedback_starter`, `T2_buzzer_pattern_starter`, `T2_serial_readout_starter`). Tier-2 starters expose `LED_ON_WINDOW` (2000→500 for Hard at T2_M3) and `FAST_MS`/`MEDIUM_MS` (tuned at T2_M4).
- Channel B scaffold (HE+EN), printable workstation poster (HE+EN), `Arduino_Project_2.md` source-of-truth.

**Pin map (canonical):** go-LED/fast = D9, buzzer = D8, button1 = D2, medium/slow LEDs (Tier-2 3-LED mode) = D10/D11, button2 (Tier-3 two-player) = D3.

**Build:** `node build_cards_only.js 2 he` / `... 2 en` — both build scripts are now parametrised per project key (project 1 stays the default; arg order-agnostic). Outputs `build_output/Project_2_Cards{,_he}.{html,pdf}` (19 cards → 55 pages HE, 62 EN). `.gitignore` has matching `!build_output/Project_2_Cards*` exceptions.

**Process that worked (reuse for Projects 3–8):** scaffold + gold-standard exemplar card by hand → fan-out Workflow (one agent per milestone, HE+EN, mirroring the exemplar + the P1 twin + the source-MD section) → review Workflow (hebrew + pedagogical + visual reviewers) → **guarded apply** Workflow. The reviewers OVER-GENERATE badly (271 findings, 132 "high"; only 33 were real — 87% rejected). The guard that mattered: never change `V1/V2/V3` card-ids (reviewers wrongly flag "V"→"✓"), never contradict the actual P1 card, reject scope-creep. See [[feedback_autonomous_batch_execution]] and [[feedback_new_card_reviewer_workflow]].

**Fritzing wiring diagrams (partly done — important tooling finding):**
- **w_p2_01 (LED + button): DONE, real Fritzing render, P1-quality.** Pipeline that works: copy a P1 canonical `.fzz` (used w3) → `remove_part` the extra LED + its dangling breadboard wires → `export` SVG → run `fix_wiring_svgs.js <path>` (its P1 coordinate patterns MATCH because the file derives from a P1 canonical) → verify by rendering. I can now self-verify renders: `node svg_to_png.js <in.svg> <out.png>` (root, untracked) rasterizes an SVG so Read can view it.
- **w_p2_02/03/04 (buzzer + 2nd button): RESOLVED 2026-07-01 via SVG compositing — real Fritzing diagrams now shipped** (committed; cards auto-updated since they ref SVGs by filename; HE bundle rebuilt to 55pp). The "GUI needed" conclusion below is SUPERSEDED: place the part with `add_part`, export, extract flattened leg coords with puppeteer, inject Fritzing-style wires onto the SVG. Full recipe in [[reference_fritzing_svg_compositing]]. w02/w03 (1 new part = buzzer) came out clean; w04 (2 buttons, 6 wires, mismatched button styles) is busy-but-functional. Original blocker for reference: adding a NEW part (buzzer, 2nd button) cannot be wired cleanly via the MCP: `add_part` places at raw x,y and returns `connections:[]` (no breadboard snap); `connect_parts` to a non-snapped part renders the wire in the WRONG place (rule #9 — wire geometry needs `register_part_position()`, a `circuit_builder` helper NOT exposed as an MCP tool). SVG-injection workaround also fails because the exported SVG's connector coords are local/transform-relative across multiple embedded view layers (a `connector0pin` at a plausible coord turned out to be a PCB-view DIL28 footprint). **Conclusion for Projects 3-8: adding new breadboard parts needs the Fritzing GUI (drag-to-snap, ~30s/part), then export + post-process.** Don't burn time grinding new-part placement via MCP. `images/fritzing/w_p2_02_led_button_buzzer.fzz` has a buzzer pre-placed (unwired) as a GUI starting point. See [[reference_fritzing_canonical_steps]], [[reference_fritzing_led_color_bug]].
2. **Program-wide stylesheet suggestions — NOT applied (to preserve P1 parity).** Reviewers flagged, in the *shared* style.css: `.section-icon` has no rule (icon spacing relies on browser default); `.card-id` uses physical `left:5mm` not logical `inset-inline-end` (so EN badge sits top-left, not top-right — same as P1, part of the deferred English-polish pass [[feedback_english_retroactive_pass]]); `.milestone-badge` 16pt bold competes with h1. All three affect the already-approved P1 look too — Yon should decide program-wide.
