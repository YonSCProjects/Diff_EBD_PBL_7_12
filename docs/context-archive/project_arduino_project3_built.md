---
name: arduino-project-3-dont-get-too-close-built
description: "Project 3 (proximity alarm) full Hebrew artifact family built + committed 66b55d0; pin map, build invocation, deferred items"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4f98ca88-5db7-42fe-97d8-4266922384ce
---

**What.** On 2026-06-30/07-01 the full **Hebrew** student-facing artifact family for **Project 3 — "לא להתקרב יותר מדי" / Don't Get Too Close** (proximity alarm) was built and committed `66b55d0` on master (not yet pushed). Dir: `Arduino_Projects/Project_3_Dont_Get_Too_Close/`. This is the D.3 work. Built per Yon's choices: **"go straight to full build"** + **Hebrew-only** (English parallel deferred, like [[feedback_english_retroactive_pass]]).

**Project 3 = proximity alarm.** HC-SR04 ultrasonic sensor measures distance many times/sec; below a threshold it triggers LED + buzzer. Tier 1 (6 cards): wire sensor → upload distance-to-Serial & watch number → add LED+threshold → add buzzer (full alarm) → test on real objects → show & celebrate. Tier 2 (5 cards): startup → pick threshold (5/20/50cm) → pick response (light/sound/both, steady/pulsing) + Claude Code Level-2 edit → test & tune → signature alarm. Tier 3: planner (drawer/doorway/pet-dish/invent use case). **Only NEW component is the HC-SR04** — LED + buzzer reused from P1/P2 (one-new-part discipline held).

**Pin map (canonical):** HC-SR04 Trig=**D12**, Echo=**D11**, VCC=5V, GND=GND; alarm LED=**D9** (220Ω); buzzer=**D8** (`tone()`); 2nd "warning" LED (Tier-3 two-stage)=**D10**; default threshold **20 cm**.

**Sketches (4):** `01_distance_to_serial`, `02_distance_led_alarm`, `03_distance_full_alarm`, `T2_alarm_starter` (flags `THRESHOLD_CM`/`USE_LED`/`USE_BUZZER`/`PULSING` at top for the Level-2 edit). Raw `pulseIn()` w/ 30ms timeout, no library; **duration==0 → returns 999** so "big number = nothing close = normal, not a bug" (the master-doc teaching point) is literally true on screen. **NOT compile-tested** — no arduino-cli in build env; Yon should compile-test before sessions (same caveat as P1/P2).

**Build:** `node build_cards_only.js he 3` → `build_output/Project_3_Cards_he.{html,pdf}` (18 cards → 64-page PDF). Build script now has project key `3` (PROJECTS + CARD_STEMS); `.gitignore` has `!build_output/Project_3_Cards*`. Both committed.

**Process (reused P2 pipeline, see [[project_arduino_project2_built]]):** wrote source MD + hand-built T1_M1 exemplar + 4 sketches → fan-out Workflow (19 agents, one per HE artifact, mirroring exemplar + P2 twin + source) → review Workflow (56 jobs: hebrew + pedagogical + visual per card) → guarded-apply Workflow (19 agents). **The guards in the review prompt WORKED this time** — 62 findings, ~50 real (vs P2's 87% noise). Key guard text: V1/V2/V3 are version badges not checkmarks; P2-mirrored patterns are pre-approved; pins fixed; ASCII+living-placeholder wiring is intentional (no Fritzing yet); "999 is normal" is intentional.

**Real fixes applied:** (a) **shared stylesheet gaps** — added global `h3` sub-divider, `table` styling, `.key` callout (was an orphan class → unstyled), `.field-optional`; (b) **Hebrew Pattern B3** — LED light-up = **מאיר** (not נדלק/מדליק), whole-alarm activation = **מגיב/מופעל**; "אזעקה נדלקת" left as idiomatic; (c) gender/smichut (אזעקת המלאה→האזעקה המלאה, ארבעה הגדרות→ארבע הגדרות מסומנות, כבית→נכבית, השתניתם→שיניתם); (d) pedagogy — T1_M3 split into חלק א/ב like T1_M4, observable done-when, sensor-seating + VCC/GND safety, time-expectation notes, bounded tuning loop.

**Deferred / open:**
- **Fritzing wiring diagrams** w_p3_01..04 — HC-SR04 is a NEW part; per [[project_arduino_project2_built]] the MCP can't snap+wire new parts → needs Fritzing GUI. Cards currently use ASCII `wiring-block` + `living-placeholder` (print-hidden authoring scaffold). 4 circuits speced in R1: 01 sensor, 02 +LED, 03 +buzzer(full), 04 two-stage(+pin10 LED).
- **English parallel** not built (Hebrew-only per Yon). Same status as P1/P2 English backlog.
- **Channel B scaffold** has a few internal "הלד נדלק" (vs preferred מאיר) — acceptable in a system-prompt scaffold, not fixed.
- **Push** — `66b55d0` committed AND pushed to origin/master (via /save, 2026-07-01).
- Teacher materials (Phase-5 setup checklist + troubleshooting sheet) not built — same scope cut as P2 ("phases 1-4").
