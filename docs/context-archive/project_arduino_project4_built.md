---
name: arduino-project-4-line-following-car-built
description: "Project 4 (line-following car, first soldering) full Hebrew artifact family built + committed 2eb45a2; pin map, R6 soldering card, stylesheet fixes, deferred items"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4f98ca88-5db7-42fe-97d8-4266922384ce
---

**What.** On 2026-07-02 the full **Hebrew** artifact family for **Project 4 — "מכונית עוקבת קו" / Line-Following Car** was built and committed `2eb45a2` on master (not yet pushed). Dir: `Arduino_Projects/Project_4_Line_Following_Car/`. D.4 work, same choices as P3 (straight-to-full-build, Hebrew-only). **First soldering project** of the program.

**Project 4 = line follower.** Two-motor chassis + **L298N** driver + 2 IR line sensors (TCRT5000-style) + 4×AA pack; car follows a black-tape line via crude proportional logic (sensor sees line → slow that side's motor). Tier 1 (8 cards): M1 together-milestone at the soldering station (4 safety rules + practice joints on scrap) → M2 solder motor leads → M3 sensors+chassis → M4 wire driver/sensors → M5 drive forward (prop car up first; backward wheel = swap OUT wires, normal) → M6 sensor test (LINE/FLOOR serial) → M7 first line-follow → M8 track+celebrate. Tier 2 (6 cards, 3 choices): speed (110/140/180) / correction (60/110) / track shape; Level-2 edit at M3. Tier 3: planner (complex track / speed build / reliability build / own idea; optional D2 button).

**Pin map (canonical):** L298N six pins in a row **D5–D10**: ENB=5 (right speed, PWM), IN4=6, IN3=7, IN2=8, IN1=9, ENA=10 (left speed, PWM). Motors: left→OUT1/2, right→OUT3/4. IR sensors: LEFT OUT=**D11**, RIGHT OUT=**D12** ("sensors live on 11–12" continuity with P3). Optional T3 button=D2 + 10kΩ pull-down. Power: battery→VIN/GND; **common ground L298N↔Arduino = the #1 pitfall** (highlighted everywhere); untethered via L298N 5V→Arduino 5V; **breadboard reused as the power hub** (5V/GND rails split to both sensors — the Uno has one 5V pin). Sketch constants: `BASE_SPEED`, `CORRECTION` (< BASE_SPEED), `LINE_IS_HIGH` (flip if car steers away from line).

**Sketches (4, NOT compile-tested):** `01_drive_forward`, `02_sensor_test`, `03_line_follow`, `T2_line_follow_starter`.

**New artifact: R6 soldering-basics reference card** (first project with 7 reference cards R0–R6). Soldering discipline: full 4-rule box only on T1_M1/R4/R6; other soldering cards = one-line reminder + r-refs; every soldering stuck-item routes to the teacher (R2 has a dedicated solder-exception box; R6 removed from R2's self-serve list to avoid contradiction). "חוט ההארקה המשותפת" is CORRECT Hebrew (adjective modifies הארקה = "common ground") — a reviewer flagged it wrongly; rejected.

**Build:** `node build_cards_only.js he 4` → `build_output/Project_4_Cards_he.{html,pdf}` (22 cards → 79pp). Build script has key `4`; `.gitignore` tracks `Project_4_Cards*`.

**Pipeline (3rd successful run of the P2/P3 process):** source MD + exemplar T1_M1 + sketches by hand → fan-out (23 agents) → guarded review (68 jobs, **116 findings, ~105 real** — guards held again) → 6 shared-stylesheet fixes by hand + guarded-apply (24 agents) → build → poster one-page verified by render (needed a manual second shave after the agent's fix: killed `min-height:277mm`, rows 37→32pt, tighter paddings) → one commit.

**Shared-stylesheet fixes (in P4's `task_cards/style.css` copy ONLY — P1/P2/P3 copies NOT yet updated, candidates for backport):**
1. `.warning > strong` scoping + `.warning ul li` white-card styling + inline per-item strong (safety-rule lists inside warnings).
2. `.celebration:not(.milestone-badge)` — the gold box no longer swallows the "milestone-badge celebration" locator line.
3. **`[dir="rtl"] .card-id { left: 5mm }`** — badge pinned physical top-LEFT on Hebrew cards per Pattern E3. The logical `inset-inline-end` was defeated by the element's own `direction:ltr` (logical props resolve against the ELEMENT's direction) — so P1/P2/P3 Hebrew cards currently render the badge top-RIGHT, violating E3. **Backport decision belongs to Yon** (changes the look of already-approved cards).
4. `.choice-preview strong` + `.key > strong` added to the RTL callout-header treatment; `.key > strong` display:block.
5. `p + .wiring-block/.code-block/pre` page-bonding (lead-in never strands at page bottom).

**Fritzing diagrams DONE (2026-07-05, commits `7a2f0f1` + `b88f6f0`, Yon chose "Hybrid: labeled block modules").** Seven SVGs in `images/`: w_p4_00 (P1 w0 copy)→R0; w_p4_01_motors_to_driver (2 real gear-motor_2 + L298N module)→R1#1+T1_M5; w_p4_02_power_and_common_ground→R1#2; w_p4_03_signal_pins (module above Arduino, near-vertical drops ENA..ENB→D10..D5; speed pins green, IN pins orange)→R1#3; w_p4_04_line_sensors→R1#4; w_p4_05_button_tier3 (pure Fritzing, stripped P1 w3)→R1#5+T3; w_p4_01_driver_wiring (full car map, thick black = common ground)→T1_M4+T2_M1. All placeholders replaced by `wiring-figure` embeds; bundle rebuilt (84pp). Regenerable: `images/fritzing/` holds the .fzz bases + `inject_modules.js` (l298n/sensor/battery/motor factories) + spec JSONs + README with all flat coords. T1_M3 still wants a real chassis photo (left as placeholder), same for T1_M6/T1_M7/T2_M4/R6 illustration slots.

**Deferred / open:**
- **English parallel** not built (Hebrew-only, same backlog as P1–P3).
- **Compile-test** the 4 sketches before session one (no arduino-cli in env).
- **Push** — `2eb45a2` local-only at build time.
- Teacher Phase-5 materials (setup checklist / troubleshooting sheet) not built — same scope cut as P2/P3 (the crib content lives in the source MD).
- Stylesheet backport question above.

**Next in program: Project 5 (Remote-Controlled Car)** — reuses P4's chassis, adds HC-05 Bluetooth / IR receiver (master doc §6.9).
