---
name: project-8-quadcopter-authored-2026-08-23
description: "Project 8 (tiny ESP32 quadcopter capstone) — locked hardware, the brief + firmware + figures, the two mandatory review passes, and the complete 28-card Hebrew set; what is still open"
metadata: 
  node_type: memory
  type: project
  originSessionId: 23475edf-dbb3-4a71-8074-6f8e659f8622
  modified: 2026-08-23T05:02:26.098Z
---

2026-08-22/23. Project 8 authored from **Yon's own updated plan**, not the old master-doc design:
`C:\RoboticsWorkshopTeachnPlay\arduinoQuadcopterProject\tiny-esp32-drone-tutorial-he.html`
(that folder also holds WIRING_DIAGRAM.txt, QuadCopterBuildInstructions.md, the AliExpress guide and
`TinyQuadcopter/MotorTest_FullPower.ino` — the pin source). Treat that tutorial as the source material.

**Locked hardware (Yon, this session).** FEICHAO 100 mm carbon frame (press-fit grommets, teacher
pre-screws the plates) · 4× 8520 coreless, **FRONT+BACK = CW, RIGHT+LEFT = CCW** (the tutorial's
adjacent-pairs assignment was wrong for a plus-flown frame and was corrected) · **65 mm** props,
1.0 mm bore · **ESP32 DevKit V1** (same board as P5/P6, not the tutorial's C3 SuperMini) · **one
MT3608** boosting the cell to 5.0 V for VIN only, motors run straight off the cell · **4× IRLB8721**
low-side MOSFETs on a hand-soldered perfboard (1N5819 flyback, 100 Ω gate, 10 kΩ pull-down, 220 µF
bulk) — no TB6612, no L9110S · **1S LiPo 1000 mAh PH2.0** + 1S USB charger · pins **FRONT 25,
RIGHT 26, BACK 14, LEFT 27**, I2C **SDA 21 / SCL 22**, LED 2.

**Honest numbers (this build, not the source's).** AUW ≈ 100 g (95 itemised + 5 build allowance);
4× 8520 + 65 mm ≈ 160–180 g bench thrust → **T/W 1.6–1.9, hover at roughly two thirds throttle**.
The master doc's "3.4:1" came from a ~50 g popsicle airframe and was corrected in §6.12. The gate is
restated in **slider terms** with an **inverted** thrust rig (props toward the scale on a tall post) —
an upright drone strapped to a block on the pan under-reads badly.

**Deliverables.** `Arduino_Projects/Project_8_Tiny_Quadcopter/`: `Arduino_Project_8.md` (the
per-project brief §6.12 calls for), `ino_files/` (00_motor_test, 01_flight, T2_flight_starter,
README), `images/` + `images/fritzing/gen_specs.py` (6 figures), `task_cards_he/` (28 cards),
`reference_cards_he/R1_flight_safety_he.dc.html`.

**Firmware safety (all three sketches).** Pins OUTPUT LOW before LEDC · WPA2 + per-station SSID
(`DRONE-` + a STATION constant) + max 2 clients + **pilot-IP lock** on /t and /arm with /disarm open
to every phone · **latched DISARM** (slider must return to 0 and ARM pressed again) · 600 ms watchdog
counting only the pilot · tilt cut-off 60° · throttle slew +2 counts / 4 ms, instant down · per-motor
2-second test buttons · motor-time counter · disarmed mix **preview** so the tilt checks never need a
live armed drone. Ceiling 100 % (Tier 2 may choose 85 %). NOT compile-tested — no ESP32 core on this
machine; static-checked both LEDC API branches.

**The two mandatory review passes ran** (safety protocol; technical accuracy): 44 findings, 3+3
blockers, adversarially verified by two lenses each → 38 confirmed → applied, plus a consistency pass
and a blocker re-verify. Highlights worth remembering: the **carbon plates conduct** (every board sits
on a full-footprint insulator; the plate sweep on ohms is now a step), an open AP let any phone in the
room arm the drone, two open pages fought over the throttle, and the emergency "pull the plug" rule is
**two-state** (props off → pull it; props on → DISARM/STOP, hands off until the props stop, teacher only)
because the PH2.0 plug sits under the propellers.

**Vocabulary decided from Yon's tutorial** (his words win, and Hebrew pattern E1 prefers the native
form): **מדחפים** (14× there, פרופלור 0×) and **מולטימטר** (9×) were swept across the whole set;
the board is **לוח המוספטים** (the card-set majority, Hebrew script rather than Latin).

**Card set (complete).** 28 Hebrew task cards + `reference_cards_he/R1_flight_safety_he.dc.html`,
each authored by one agent and verified/fixed by another; Tier 1 ×14, Tier 2 ×13 (the brief's 17
Tier-2 milestones fold seven "exactly T1·Mx" entries into their neighbours), Tier 3 planner.
`build_output/Project_8_Cards_he.{html,pdf}` = 138 pages. **Card vocabulary was swept to Yon's own
words** — מדחפים, מולטימטר, לוח המוספטים — and the brief's short safety line sits in every card footer.
**Cards run ~4–5 A4 pages each** (a comparable P7 card is 3): flagged for a pedagogical pass.

**Still open:** prop guards (Yon's decision); the teacher-phone DISARM lock and the green ARMED banner
(both implemented, both want a yes/no); reference cards R2/R3/R4 are cited but only R1 exists; the
sketches are not compile-tested; and the usual second pass (GPT Hebrew, reviewer trio, review console).
See [[reference_fritzing_kit]] for how the figures are built and
[[feedback_wiring_figures_not_optional]] for why they ship with every set.
