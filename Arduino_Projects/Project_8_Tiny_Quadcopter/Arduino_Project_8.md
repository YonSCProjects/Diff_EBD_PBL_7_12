# Arduino Project 8 — Tiny ESP32 Quadcopter

*The eighth and final project in the Agourim differentiated Arduino workshop program — the apex capstone.*
*Source file — teacher-facing. Student-facing task cards (Hebrew `.dc.html`), reference cards, Claude Code tutorial-channel scaffold, safety cards, and pre-written `.ino` files are generated from this document.*

**Version 0.2 — 2026-08-22, after the two mandatory review passes (safety-protocol pass; technical-accuracy pass). The confirmed findings of both passes are applied in this version; the reviewers' numbers are kept in the *Technical review record* near the end of the file. The sketches in `ino_files/` were changed to the same policy on the same day.**

---

## Read this first — locked hardware decisions and where this file overrides the sources

This file is built from Yon's updated drone tutorial (`tiny-esp32-drone-tutorial-he.html`, the MOSFET build) and from [Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §6.12 and §5.6. Where the sources disagree with each other, the **locked decisions of 2026-08-22** win, and this file is the single operational source of truth for Project 8. The decisions that differ from the master document's §6.12 narrative are:

| Topic | Master doc §6.12 says | Locked decision (this file) |
|-------|-----------------------|------------------------------|
| Brain | "an ESP32 at the center" | **ESP32 DevKit V1 (30-pin DOIT)** — the same board as Projects 5 and 6, not the ESP32-C3 SuperMini of the tutorial. |
| Motor drive | 2× TB6612FNG | **4× IRLB8721 logic-level N-MOSFETs** as low-side switches on a small perfboard (the tutorial's Task 3 circuit). No TB6612, no L9110S. |
| Boosters | 2× MT3608 (ESP32 rail + motor rail) | **1× MT3608**, battery → IN, OUT pre-tuned to **5.0 V** → DevKit **VIN**. **Motors run directly from the 1S battery** — no booster on the motor rail. |
| Battery | ~300–500 mAh | **1S LiPo 3.7 V 1000 mAh, PH2.0 (JST-PH) connector**, 1S USB charger, charged by the teacher in the fireproof bag. |
| Propeller guards | "mandatory for practice flights" | **Not yet decided / not in the kit.** Until guards arrive, every practice flight is **tethered** (fishing line to a fixed anchor), eye protection for everyone in the room, 3 m clear zone, one drone armed at a time, props fitted in the Safe state as the last act before the battery goes in. 65 mm props are kept rather than §6.12's "55 mm during the learning phase" alternative — the thrust table has no margin to give up. *When guards arrive, they go on for every practice flight.* The dated deviation note at the top of the Safety Protocol says the same thing in one paragraph. |
| Throttle ceiling | (tutorial: 70 % = 178/255 for an 86 g drone) | **100 % = 255/255** (`MAX_THROTTLE_PERCENT = 100`) in the stock sketches, with a **firmware slew limiter**: the throttle may climb only **+2 counts per 4 ms step** (~0.5 s from 0 to full) and drops instantly. The technical review of 2026-08-22 showed that at an 85 % cap the hover point of a ~100 g build sits at 70–90 % of the slider and the PD controller runs out of headroom; the cap protected no hardware (the motors are on the battery, the IRLB8721 is rated 62 A). The beginner envelope is now the **slider-based hover-point gate** (Hardware section) plus the Tier 2 ceiling choice — **85 % (careful) / 100 % (balanced)**. |
| Frame | FEICHAO 100 mm carbon kit | Same — **FEICHAO/JMT hollow-cup carbon frame, 100 mm wheelbase (AliExpress 32950607425)**, two 1.5 mm plates (teacher pre-screws them), rubber grommets: the 8.5 mm motors **press-fit** through (no glue, no screws), rubber motor caps = landing feet, battery O-rings. ~9 g. The tutorial's popsicle-stick frame (its Task 1) is replaced. **The carbon plates conduct electricity** — every board sits on a full-footprint insulator (Hardware section). |
| Bench thrust-test gate | "T/W ≥ 2.0 : 1 before the first hover attempt" (written for a 42–45 g popsicle airframe) | **Restated in what the student reads on the scale** (technical review 2026-08-22): the drone is tested **inverted on a post**, and the gate is the **hover point** — the slider % at which the scale reading first passes the AUW. **≤ 75 % = fly, tethered** (≈ thrust at 100 % ≥ 1.5 × AUW — the master doc's 2.0 intent for this heavier build); **75–85 % = tethered only, ≤ 30 cm, weight ladder before the next session**; **above 85 % or never = no flight, weight ladder**. T/W is still computed and logged, as a number, not as the gate. |
| Wi-Fi | open soft-AP, "program convention from Projects 5–7" | **WPA2 password per station** (8+ characters, on the teacher's sheet and the pilot's station card), **at most two clients** (pilot + teacher), SSID **`DRONE-<station>`** from a `STATION` constant the teacher sets (1–8) when copying the sketch, and a **pilot lock**: throttle is accepted only from the phone that pressed ARM; DISARM from any phone. Unlike the car projects, the drone's network has a password because *the network is the control stick*. |

Everything else in §6.12 (the three tiers, the safety escalation, the Claude Code levels, the evidence caveat) stands.

---

## What the student builds

A **tiny quadcopter** that fits on the palm of one hand: a 100 mm carbon frame, four 8.5×20 mm coreless motors with 65 mm propellers, an ESP32 DevKit V1 at the center, an MPU6050 inertial sensor (GY-521) that tells the ESP32 which way is down, a hand-built four-channel MOSFET board that switches the motors, a small MT3608 boost module that feeds the ESP32 a clean 5 V from the 3.7 V battery, and a 1S LiPo battery. The drone broadcasts its own Wi-Fi network (`DRONE-<station>`, with a password — unlike the car projects, because here the network *is* the control stick); the student's phone joins it, opens one page at `192.168.4.1`, and that page has an **ARM / DISARM** pair, a **throttle slider**, and four **per-motor test buttons** for the bench. The full flight firmware fuses gyroscope and accelerometer with a complementary filter and runs a PD controller that keeps the drone level while the student controls height.

At **Tier 1** the student assembles a partly pre-built kit (frame plates pre-screwed, MOSFET board pre-soldered, MT3608 pre-tuned), does all the wiring, runs every test, uploads two pre-written sketches — a **motor-test sketch** (slider → motors, no sensor) and the **full flight sketch** — and flies a tethered first hover. At **Tier 2** the student builds everything including the MOSFET board (four soldered channels), tunes the MT3608 with a multimeter, chooses PID starting values, a tether/zone option and a flight-test sequence, and edits a starter sketch with Claude Code. At **Tier 3** the student plans and builds an extension (altitude hold, logging, flight modes, battery monitor) with Claude Code Level 3.

## Why this is the capstone

1. **It needs every skill from Projects 1–7 and cannot be shortcut.** Breadboard and pull-down logic (P1), timing and state (P2), a sensor feeding a decision (P3), soldering and motor drivers and battery power (P4), ESP32 + soft-AP web page + PWM (P5), I2C sensors and Library Manager (P6), multi-subsystem integration and separate power rails (P7). Project 8 adds three new things on top: **sensor fusion** (the complementary filter), **closed-loop control** (PD tuning), and a **flight safety protocol** as a first-class discipline.
2. **It is the one project in the program where the hardware can hurt someone.** Four propellers at ~40,000 RPM cut fingers and scratch eyes; a LiPo battery can burn. Projects 1–7 built the habits (eye protection, power-off discipline, battery discipline, "call the teacher") that the Full Flight Safety Protocol in this file depends on. A student who has internalised "goggles on when the iron is on" (P4) already knows the shape of "goggles on when a motor can spin."
3. **It is the empowering experience the super-target names.** A thing the student built with their own hands leaves the ground. Principle 4 is served by 14–17 visible checkpoints; Principle 3 by the fact that the student touches, presses, solders, measures, and weighs everything before any flight code runs; Principle 9 by the heavy teacher pre-build at Tier 1, so the teacher's session time goes to rotation and safety, not kit prep.

**Evidence honesty (from §6.12):** there is no verified research on flight-based STEM for this population. Project 8 is an inferential extension from the ground-robotics and makerspace-for-EBD literature, piloted under the safety discipline below. This file does not claim otherwise.

---

## Hardware per student

Project 8 is the program's most expensive and heaviest-prep project (~$35–45 per student in parts; master doc §8). The soldering station, multimeters, kitchen scale, charger, fireproof bag, and sand bucket are **shared workshop equipment**.

### Bill of materials (per drone) with weight budget

| Qty | Item | Weight (g) | New / reused | Notes |
|-----|------|-----------:|--------------|-------|
| 1 | **FEICHAO/JMT 100 mm hollow-cup carbon frame kit** (2× 1.5 mm plates, standoffs + screws, 4 rubber motor grommets, 4 rubber motor caps = landing feet, battery O-rings) | 9 | NEW | Teacher pre-screws the two plates. Motors press-fit through the grommets — no glue, no screws anywhere in the build. Frame max prop 65 mm (5.7 mm tip clearance). |
| 4 | **8520 coreless motors** (8.5×20 mm), 2 CW + 2 CCW, ~70 mm leads | 20 (4×5) | NEW | Verify the set is 2+2. Convention used here: **CW motors (red/blue leads) → FRONT and BACK; CCW motors (black/white leads) → RIGHT and LEFT** (see "Rotation pairs" below). |
| 4 (+8 spare) | **65 mm propellers, 1.0 mm bore**, 2 CW + 2 CCW | 4 (4×1) | NEW | 1.0 mm bore is the 8520 shaft size — standard 1.5 mm whoop props do not fit. Students will break props; keep a spares box on the teacher's desk. |
| 1 | **ESP32 DevKit V1** (30-pin DOIT, with headers) | 10 | reused (P5/P6 board) | Board type "DOIT ESP32 DEVKIT V1". |
| 1 | **MT3608 boost module** (the common 36×17 mm module) | 2 | NEW (P7 used a buck) | **Pre-tuned by the teacher to 5.00 V** and locked with a drop of nail polish. Feeds DevKit VIN only. |
| 1 | **MPU6050 / GY-521** IMU | 2 | NEW | Runs from the DevKit **3V3** pin (program rule: one 3.3 V sensor rail). The module carries its own 3.3 V regulator and onboard pull-ups to that rail. I2C address 0x68. |
| 1 | **MOSFET board** — perfboard ~4×5 cm, 4× **IRLB8721** (TO-220), 4× **1N5819** Schottky, 4× **100 Ω**, 4× **10 kΩ** (¼ W), 1× **220 µF / 6.3 V low-ESR** electrolytic, bare copper rails | 18 (board 5 + 4 TO-220 8 + parts 5) | NEW | Tier 1: pre-soldered by the teacher. Tier 2: student-soldered. The four tabs are heat-shrunk and the solder side faces an insulating sheet, never the carbon plate. Counterfeit IRLB8721s are common — the teacher runs the 5-minute check (Setup section). |
| 1 | **1S LiPo 3.7 V 1000 mAh, PH2.0 connector** (25C+) | 24 | NEW | Lives in the fireproof bag on the teacher's desk. One battery out of the bag at a time in the whole room (battery-custody rule). |
| — | Wires: 22–24 AWG silicone red/black (battery pigtail, board → MT3608), 26 AWG (MT3608 → VIN/GND), 28–30 AWG signal (gates, I2C, 3V3); **PH2.0 mating pigtail**; 10 female crimp pins + 1-way housings (DevKit side: VIN, 2× GND, 3V3, 21, 22, 25, 26, 14, 27) or 5 F-F jumpers cut in half; foam tape (MPU); **full-footprint foam double-sided tape 2–3 mm + a 0.5–1 mm plastic / Kapton shim under every board** (the carbon plates conduct); 2× nylon standoffs or spacers (DevKit); 2× 2.5 mm zip ties; heat-shrink; 1 mm braided cord (tether loop); 2 mm foam/EVA pad (battery bay) | 6 | — | Short wires = less weight and less resistance. Power wires in red/black only. Insulation is not a place to save grams. |
| | **Itemised subtotal** | **95** | | |
| | Build allowance (solder, heat-shrink, tape, strain relief, tether loop, board insulation) | +5 | | |
| | **Planning AUW (all-up weight, with battery)** | **≈ 100 g** (105 g with margin; 110 g worst case) | | *The kitchen scale at T1·M11 / T2·M13 is the truth — the student writes the real number on the card.* |

**Shared equipment for the room:** soldering station (from P4), 2× multimeters, digital kitchen scale (**1 g resolution, ≥ 1 kg, no auto-power-off within 2 minutes, any "hold" averaging mode off**), a **thrust-test post** (a rigid 4×4 cm wooden block 15 cm tall glued to a wide low base, or a sand-filled 0.5 L bottle; ≥ 300 g in total, ≤ 45 mm across at the top) with **two rubber bands** and a 30 cm backup line (thrust test — the drone sits **inverted** on the post), 1S USB LiPo charger (TP4056-type, 4.20 V cutoff), **two fireproof LiPo bags — one labelled STORAGE (zipped, R3 custody) and one labelled CHARGING (holds one cell, on the tile)**, **sand bucket** (≥ 5 L dry sand, with a scoop), ceramic tile or fireproof mat under the charging spot, **safety glasses for every person in the room** (not just the pilot), floor tape (flight circle + spectator line + lift-off mark), **fishing line 0.35–0.40 mm nylon monofilament (≥ 6 kg rating)** for tethers, a **flat tether anchor, 2–3 kg and ≤ 10 cm tall** (a 2.5 kg barbell plate lying flat, a flat sandbag, or the 2 L sand bottle laid on its side — never upright: the drone hovers at 10–30 cm, inside the height of a standing bottle), a spares box (props, motors, MOSFETs, diodes, **one pre-tuned spare MT3608** (marked 5.0 V like the rest — troubleshooting items 2 and 15 send a build to it), **one spare FEICHAO frame kit per four drones** — grommets, motor caps, battery O-rings — and spare PH2.0 pigtails), a phone or tablet per flying drone.

**Shared tools and bench consumables (non-flying, so not in the weight table):** hot-glue gun + sticks, #00 Phillips screwdriver (the frame's M2 screws), flush cutters + wire strippers (P4 kit), a JST/Dupont pin-release tool, clear nail polish (MT3608 pot lock), a silver paint marker + a fine permanent marker (module marking, board labels, the FRONT arrow), 2–3 mm foam double-sided tape stock, Kapton tape or thin plastic sheet for shims (an old loyalty card works), 1 mm braided cord for tether loops, cloth tape.

### Thrust, weight, and the T/W gate — the numbers the teacher needs

**Units first.** Every percentage on a task card is a **slider** percentage unless it is written "duty". With the stock ceiling at 100 %, slider 100 % = duty 255 = full motor power, so **slider 80 % = duty 204** and **slider 60 % = duty 153**; the Tier 2 "careful" ceiling of 85 % (duty 217) shortens the slider, and a hover point measured with the motor-test sketch moves up by ~17 % of itself on that shorter slider (65 % → 76 %).

**Free-air bench figures (percent of full throttle, not slider).** Four 8520 motors with 65 mm props at 3.7–4.2 V produce roughly **40–45 g each on a fresh battery** (bench, decision file) — **160–180 g** total at duty 255; a tired battery or 2-blade props push it toward 140 g, 4-blade props toward 200 g. The student never sees those numbers directly: at slider 100 % the cell, the PH2.0 plug and the pigtail sag ~0.35 V under 6–7 A (×~0.88), so a 140–180 g bench set **reads about 125–160 g on the scale** — and only on the inverted rig of T1·M11 (a drone blowing down onto the scale pan reads 30–70 % low, which is why the upright rig of the first draft was scrapped).

| Scale reading at slider 100 % (inverted rig, tared) | AUW 90 g | AUW 100 g | AUW 110 g |
|----------------------------------------------------:|:--------:|:---------:|:---------:|
| 110 g (tired battery / weak motors) | T/W 1.22 · hover ~87 % | 1.10 · ~94 % | 1.00 · never |
| 125 g (a 140 g bench set) | 1.39 · ~80 % | 1.25 · ~86 % | 1.14 · ~92 % |
| 140 g (a 160 g bench set — the realistic first build) | 1.56 · ~74 % | **1.40 · ~80 %** | 1.27 · ~85 % |
| 160 g (a 180 g bench set / 4-blade props) | 1.78 · ~68 % | 1.60 · ~73 % | 1.45 · ~78 % |

*Hover slider % = 100 × (AUW / T₁₀₀)^(2/3): thrust on a brushed motor rises a little faster than linearly with duty, between `W/T` (linear) and `√(W/T)` (quadratic); the table uses the middle exponent. The realistic first build — 160 g bench motors, AUW 100 g — lands at T/W 1.40 with hover at ~80 % of the slider: flyable on a tether, nowhere near the 3.4 : 1 the master doc's narrative assumed for an 8520 build (that figure came from a 42–45 g popsicle airframe).*

**Why the gate is the hover point and why the "fly" line sits at 75 %.** The PD corrections ride on top of the slider value and each motor is constrained to 0–255; `MAX_CORRECTION` is 60 counts. A hover point at slider 75 % (duty 191) leaves 64 counts of headroom — the controller never clips. At 85 % (duty 217) only 38 counts remain: the drone loses height while it levels, which is tolerable on a tether at 30 cm and not above it. Above 85 % the stabiliser has nothing to work with. The hover point is also the one quantity the student observes directly on the scale, and it does not depend on which ceiling the flight sketch later uses.

**The gate (T1·M11 / T2·M13), in what the student reads:** the student records the AUW, the scale reading at slider 60 / 80 / 100 %, and **the slider % at which the reading first passed the AUW — the hover point**. T/W = reading at 100 % ÷ AUW is written down as a number, not used as the gate.
- **Hover point ≤ 75 % → "fly" (tethered, as every practice flight is).** Equivalent to thrust at 100 % ≥ 1.5 × AUW — the master doc's "2.0" intent carried over to a heavier airframe.
- **Hover point 75–85 % → "tethered only, ≤ 30 cm, weight ladder before the next session."** (≈ thrust ≥ 1.25 × AUW.)
- **Hover point above 85 %, or never reached at slider 100 % → no flight this session; weight ladder.**

**Technical review 2026-08-22 — result on the cap.** The first draft capped the duty at 85 % (217/255) "to keep a beginner envelope". At that cap the hover point of a 100 g build sits at 70–90 % of the *shorter* slider and the controller has 22–45 of its 60 counts; the cap protected no hardware (motors on the battery, IRLB8721 rated 62 A, cell 25 C). The stock ceiling is therefore **100 %**, and the beginner envelope is provided by three things that do not cost headroom: the **slew limiter** in every sketch (throttle climbs at most +2 counts per 4 ms step, ~0.5 s from 0 to full; down is instant, so DISARM, landing and the watchdog are never delayed — a slip of the thumb is a slow climb, never a jump), the **hover-point gate** above, and the **Tier 2 ceiling choice** (85 % careful / 100 % balanced, T2·M14 Choice C). The full numbers are in the *Technical review record*.

> **Weight ladder (ordered by payoff per effort):** (1) **the cell** — a 1S 750 mAh (−6 g) or a genuine 35 C+ 600 mAh (−8 to −9 g), PH2.0: the 3-minute rule in R8 uses ~250 mAh per flight (3 min × ~5 A hover draw = 42 % of a 600 mAh cell), so the 1000 mAh cell's only benefit is ~0.1 V less sag near full throttle — **a kit decision for Yon against locked decision 6; the BOM keeps 1000 mAh until he decides**; (2) 4-blade 65 mm props — +10–15 % thrust at a higher current (the 1000 mAh cell has the headroom), the cheapest way to move a failing build across the gate; (3) trim the perfboard to the minimum outline and lay the TO-220s flat — −2 to −3 g; (4) shortest possible wires, no intermediate connectors — −2 g; (5) last resort: I-PAK (TO-251) logic-level MOSFETs, ~0.5 g each, −6 g, only after verifying R_DS(on) at 3.3 V. **Insulation is not a place to save grams.** The DevKit and MT3608 are fixed by decision.

### Rotation pairs (a correction to the tutorial — read before sorting motors)

The frame is square (an X); it is **flown "plus-style"**: one arm points forward and the four motors are named **FRONT / RIGHT / BACK / LEFT**, exactly as the folder's `MotorTest_FullPower.ino` names them. In that orientation the **opposite arms must spin the same way** so that a pitch or roll correction does not also twist the drone (yaw): **FRONT and BACK = CW; RIGHT and LEFT = CCW.** Props follow the motor: CW prop on a CW motor. *(The tutorial's "Front + Right CW, Back + Left CCW" is the X-configuration rule applied to a plus layout — with that arrangement every pitch correction would also spin the drone. The cards use this file's pairing.)* Brushed motors reverse with polarity — the tutorial's claim that coreless motors ignore polarity is incorrect. If a motor spins the wrong way, swap its two wires at the board; that is the fix, not a new motor.

### Pin map (canonical for all sketches, wiring references, and figures)

The four motor gates are **four pins in a row** on the right-hand header of the DevKit (USB at the bottom): 14 · 27 · 26 · 25. I2C is on the program's standard 21/22 (same as P6).

| Signal | DevKit pin | Wire colour | Notes |
|--------|-----------:|-------------|-------|
| **G1 — FRONT motor gate** (CW) | **GPIO 25** | yellow | LEDC PWM, 20 kHz, 8-bit. Non-strapping. |
| **G2 — RIGHT motor gate** (CCW) | **GPIO 26** | orange | idem |
| **G3 — BACK motor gate** (CW) | **GPIO 14** | green | Non-strapping, but GPIO 14 can emit a millisecond-scale pulse at reset — a tiny BACK-motor twitch at power-up (no props) is normal. If it bothers, GPIO 33 is the free alternative; the sketches expose the pin as a constant. |
| **G4 — LEFT motor gate** (CCW) | **GPIO 27** | blue | idem |
| MPU6050 SDA | **GPIO 21** | white | I2C data |
| MPU6050 SCL | **GPIO 22** | grey | I2C clock |
| MPU6050 VCC | **3V3** | red (thin) | **3V3 — not VIN, not 5 V.** The rule keeps everything the ESP32 touches on one 3.3 V rail (ESP32 pins are not 5 V tolerant); the GY-521 itself has its own regulator and would survive 5 V. |
| MPU6050 GND | **GND (left header, next to 3V3)** | black (thin) | The DevKit has exactly two GND pins — one per side. Left GND = sensor. |
| MT3608 OUT+ | **VIN** | red | 5.0 V in. |
| MT3608 OUT− | **GND (right header, next to VIN)** | black | Right GND = power return. The MOSFET board's ground reaches the DevKit through the MT3608's common IN−/OUT− copper. |
| Status LED (onboard blue) | GPIO 2 | — | Used by the sketches only: fast flicker = calibrating, short blink = ready/disarmed, solid = armed, endless fast flicker = MPU6050 not found (at boot) or lost (in flight — the drone has disarmed itself and refuses ARM until it is rebooted). |
| *Tier 3 only:* battery sense | GPIO 34 (input-only ADC) | — | 100 k / 100 k divider from BAT+, **with a 100 nF–1 µF ceramic from the pin to GND at the DevKit pin** (the 50 k source impedance is too high for the ESP32 ADC without it). |
| *Tier 3 only:* BMP280 / second I2C device | shares 21/22 | — | |
| **Never use for motors or wiring** | 0, 5, 12, 15 (strapping; 2 is strapping too — onboard LED only), 6–11 (flash), 34–39 as outputs | | |

### Power tree

```
                     1S LiPo 3.7 V 1000 mAh  (PH2.0 plug — CHECK POLARITY with the meter)
                      red (+)                          black (−)
                        │                                 │
                        ▼                                 ▼
   ┌──────────────────── MOSFET BOARD (perfboard ~4×5 cm) ─────────────────────┐
   │  BAT+ rail ═══╦═══════╦═══════╦═══════╦═══════ 220 µF (+ leg)  ● BAT+ →MT3608 IN+
   │              M1+     M2+     M3+     M4+        (motor "+" pads)           │
   │             ►|D1    ►|D2    ►|D3    ►|D4        1N5819, band toward BAT+  │
   │              M1−     M2−     M3−     M4−        (motor "−" pads = Drains)   │
   │              Q1      Q2      Q3      Q4         IRLB8721, Source on GND    │
   │   G1 ─100Ω─┤ G2 ─100Ω─┤ G3 ─100Ω─┤ G4 ─100Ω─┤  gates; 10 kΩ each to GND   │
   │  GND rail ═══╩═══════╩═══════╩═══════╩═══════ 220 µF (− leg)   ● GND →MT3608 IN−
   └────────────────────────────────────────────────────────────────────────────┘
                        │ 22–24 AWG                              │
                        ▼                                        ▼
                 ┌──── MT3608 boost, pre-tuned 5.00 V (nail-polish lock) ────┐
                 │  IN+   IN−                             OUT+    OUT−       │
                 └────────────────────────────────────────┬───────┬──────────┘
                                                      red │       │ black  (26 AWG)
                                                          ▼       ▼
                                       ESP32 DevKit V1:  VIN     GND (right header)
                                                          │
                     3V3 ──► MPU6050 VCC        GND (left header) ──► MPU6050 GND
                     GPIO 21 ──► SDA             GPIO 22 ──► SCL
                     GPIO 25 ──► G1 FRONT (CW)   GPIO 26 ──► G2 RIGHT (CCW)
                     GPIO 14 ──► G3 BACK  (CW)   GPIO 27 ──► G4 LEFT  (CCW)

   Motors run on raw battery voltage (3.7–4.2 V) through their MOSFETs.
   Only the ESP32 sees the 5.0 V rail. Only the MPU6050 sees 3.3 V.
   One ground. Star point = the MOSFET board's GND rail.
   Connection count: battery 2 + board→MT3608 2 + MT3608→DevKit 2 + DevKit→MPU 4 + gates 4 + motors 8 = 22.
```

**Why the MT3608 is there at all.** The DevKit's onboard AMS1117 regulator needs ≥ ~4.5 V on VIN to make a clean 3.3 V; a 3.7 V cell (sagging to ~3.3 V under motor load) cannot run it, and feeding the battery into the 3V3 pin bypasses the regulator with an unregulated, sagging voltage — the ESP32 would brown-out and reboot every time the motors spool. The MT3608 holds 5.0 V as long as the battery stays above ~2.5 V, which decouples the brain from the motors' sag. **The brownout detector stays enabled** in every sketch (the folder's `MotorTest_FullPower.ino` disabled it — that hack belonged to the old single-rail build and is not copied).

**USB and battery are never connected at the same time.** Program rule since P4: *USB in = battery out; battery in = USB out.* Uploads happen on USB with the battery unplugged (the motors cannot move — the board has no BAT+); every motor run happens on battery with USB unplugged. The DevKit V1 tolerates both in principle, but the rule removes a whole class of "why is it doing that" moments and keeps the drone's arming authority in one place: the battery plug.

### The MOSFET channel — exactly what each of the four channels is

```
  BAT+ rail ─────────┬────────────────────────┐
                     │                        │  cathode (the BAND) — toward BAT+
                 [ MOTOR ]                 ──┤◄──   1N5819 Schottky (flyback)
                     │                        │  anode — toward the Drain
                     └───────────┬────────────┘
                                 │  ← motor "−" pad (M−)
                              D  │  Drain  (also the metal TAB of the TO-220!)
  GPIO ──[100 Ω]──► G ─────────┤├   IRLB8721 — legs G · D · S left→right,
                   │          S  │           label facing you, legs down
                [10 kΩ]          │  Source
                   │             │
  GND rail ────────┴─────────────┴─────────────────────────────
```

- **IRLB8721 pinout:** hold it with the printed label facing you and the legs pointing down: **left = Gate, middle = Drain, right = Source**. The **metal tab is Drain** — electrically the motor's "−" wire. Therefore the **four tabs must never touch each other** (it would join all four motors into one), and no tab may touch the BAT+ or GND rail. Leave ≥ 2 empty holes between MOSFETs; **heat-shrink the four tabs** (unconditional — a conductive carbon plate sits 1 mm away). No heatsink is needed: R_DS(on) ≈ 20–25 mΩ at the ESP32's 3.3 V gate drive → ~0.1 W at 2 A and ~0.16 W at the 8520's 2.5 A stall. A MOSFET that gets *hot* is a counterfeit (see Setup).
- **Flyback diode orientation:** band (cathode) to **BAT+** / the motor's "+" side; anode to the Drain / motor "−" side. *Why:* a motor is a coil; when the MOSFET switches off 20,000 times a second, the coil's current has nowhere to go and the Drain voltage spikes until something breaks down. The diode gives that current a loop (motor − → diode → motor +) and clamps the spike at ~0.3 V. **Reversed, the diode is a dead short across the battery through the MOSFET the moment the gate goes high — it smokes.** Must be Schottky (1N5819), not a 1N4007: a slow diode cannot follow 20 kHz. The diode's average current is the motor current × (1 − duty) — ≤ 0.75 A at any operating point — so the 1 A 1N5819 is sufficient; a 1N5822 (3 A) is the drop-in upgrade if a motor is ever stalled for long.
- **10 kΩ gate pull-down:** ties the gate to 0 V whenever the ESP32 is *not* actively driving it — during the ~1 s of boot when GPIOs float, during a reset, and if the gate wire ever falls off. A floating logic-level gate drifts to 1–2 V from leakage and static and **half-turns the motor on**. This is the hardware half of boot safety; the software half is *every motor pin is set `OUTPUT LOW` before LEDC is attached* in every sketch.
- **100 Ω gate resistor:** the gate is a ~1.5 nF capacitor; charging it straight from a GPIO would spike the pin above its 40 mA rating and ring. 3.3 V / 100 Ω = 33 mA peak, gone in a microsecond.
- **220 µF bulk capacitor** across BAT+/GND (long leg = +, stripe = −): a local energy reservoir for the moment all four motors switch on together, so the battery leads' inductance does not dip the rail. One per board, not one per channel.
- **Power path:** BAT+ rail → motor → Drain → Source → GND rail. The 22–24 AWG battery pigtail and the two rails carry up to ~6–8 A in bursts — bare copper wire or doubled resistor-leg offcuts for the rails, solder flooded along them.
- **The carbon plates conduct.** Not as well as copper, but well enough: the resin surface is patchy and every drilled hole and cut edge is bare fibre (a plate reads ohms to a few hundred ohms edge to edge; the kit's metal standoffs join the two plates, so insulating one plate is not enough). This board's bare rails, its four Drain tabs, the DevKit's 30 protruding header-pin tips and the MT3608's solder joints are all 1 mm from that plate. **Every board on this drone sits on its own full-footprint insulating layer between its solder side and the plate, and nothing metal touches carbon anywhere in the build** — a pin tip joining VIN to GND or two tabs joined through the plate is a LiPo short. The check is in M4 and M8: meter on Ω, one probe on a cut edge or a screw hole (the glossy face can read open on a plate that shorts at a hole), the other on every pad and pin in turn — OL everywhere.

**Suggested perfboard layout (4×5 cm, single-sided, 2.54 mm pitch):**

```
 ┌──────────────────────────────────────────────────────────────┐
 │ ● BAT+ (pigtail red)     ● BAT+ → MT3608 IN+      ▬ 220 µF   │
 │ ════════════════ BAT+ rail (bare copper) ═══════════════════ │
 │   M1+ M1−        M2+ M2−        M3+ M3−        M4+ M4−       │  ← motor pads
 │   ►|  │          ►|  │          ►|  │          ►|  │          │  ← 1N5819, band up (to BAT+)
 │   [Q1 G D S]     [Q2 G D S]     [Q3 G D S]     [Q4 G D S]    │  ← ≥2 empty holes between
 │   100Ω  10k      100Ω  10k      100Ω  10k      100Ω  10k     │
 │   ● G1           ● G2           ● G3           ● G4          │  ← gate pads (to GPIO)
 │ ════════════════ GND rail (bare copper) ════════════════════ │
 │ ● GND (pigtail black)    ● GND → MT3608 IN−                  │
 └──────────────────────────────────────────────────────────────┘
   Channel map:  M1/G1 = FRONT (GPIO 25)   M2/G2 = RIGHT (GPIO 26)
                 M3/G3 = BACK  (GPIO 14)   M4/G4 = LEFT  (GPIO 27)
   Label the board with a marker: M1–M4, G1–G4, BAT+, GND, and an arrow "FRONT".
```

### What the teacher pre-builds (before the project starts; one-time, ~40 min per Tier 1 kit)

1. **Frame:** screw the two carbon plates to the standoffs; press the four rubber grommets into the arm rings; leave the motors, caps and O-rings loose in the tray. Mark "FRONT" on one arm with a paint pen. **Measure the plate once** — meter on Ω, probes on two cut edges or screw holes — and write the reading on the tray: a carbon plate reads ohms to a few hundred ohms (an FR4 carbon-look plate reads OL); either way the insulation goes on, and the reading is the "why" the student is shown. **Cover the board-landing area of both plates with an insulating layer** (Kapton, two layers of electrical tape, or a 0.5–1 mm plastic shim glued with double-sided tape) and cloth tape on the two plate edges the battery O-rings cross. **Fit the tether loop** (Tier 1 kits): a 10 mm loop of 1 mm braided cord through two adjacent holes on the bottom plate's centreline, knotted on the *top* face, hanging ~10 mm clear below the plate — the fishing line is girth-hitched onto it at every flight. Route the PH2.0 pigtail so the plug exits at the frame's side, between two arms.
2. **MT3608 tuned to 5.00 V and locked.** Modules ship at either end of the 25-turn pot, and the pot's sense is not the same on every batch — **do not assume a direction; trust the meter.** Meter on OUT+/OUT−, battery on IN+/IN− (storage charge), nothing else connected. Turn **3 full turns one way** and watch: if the reading moves toward 5.0 V keep going; if it moves away, or does not move at all (you are at the pass-through end, where OUT ≈ IN — a boost module cannot output less than its input; that floor is not a broken module), turn the other way. Slow down in the last half-volt, stop at **4.95–5.05 V**, battery off and on again — still 5.0 V; confirm it holds with a DevKit connected as load; a drop of nail polish on the pot. Write "5.0 V ✓ + date" on the module with a silver marker. **A DevKit must never be connected to an MT3608 that has not read in that window on two power-ups** — a module at the wrong end of its pot outputs 20 V+. Teacher numbers: MT3608 input 2–24 V, output up to 28 V, rated 2 A output (a DevKit at ~250 mA on 5 V draws ~0.4 A from the cell, far inside the envelope).
3. **MOSFET board (Tier 1 kits):** all four channels, the 220 µF cap, the rails, the PH2.0 pigtail soldered to BAT+/GND (polarity checked with the meter against the actual battery — JST-PH polarity on micro-drone batteries is **not** standardised), labels M1–M4 / G1–G4, the four TO-220s laid flat with **heat-shrink on the tabs** and heat-shrink over the two spare BAT+/GND pads once their wires are on. Multimeter-checked (procedure in T1·M3). Tier 2 kits get the bare perfboard and loose parts; the teacher still solders the **battery pigtail** at Tier 2 — it is the one joint that carries the full current.
4. **MOSFET counterfeit check (every MOSFET, 1 min each):** gate tied to 3.3 V, push ~1 A Drain→Source (a motor and a battery), measure V_DS: genuine ≈ 20–50 mV; a relabelled standard-gate part reads 100 mV+ and warms up. Do not use IRF520 / IRFZ44N / IRF540 look-alikes (10 V gate parts).
5. **Batteries** at storage charge (3.8 V), in the **STORAGE** fireproof bag, labelled B1…Bn. The second bag (**CHARGING**, one cell at a time) and the charger on the tile at the teacher's desk, ≥ 1 m from the storage bag. On a flight day the flight batteries are brought to **4.1–4.2 V during the building block**, before any flight slot — a cell at the 3.8 V storage floor barely clears checklist item 4 for one slot.
6. **Motors sorted** into a CW bag (red/blue leads → FRONT/BACK) and a CCW bag (black/white → RIGHT/LEFT); **props sorted** CW/CCW in two labelled boxes kept on the teacher's desk (props are handed out only at the flight line).
7. **Flight zone** laid out once per room (Safety Protocol section): 3 m circle, spectator line, lift-off mark, flat anchor, tether; the thrust-test post at the bench-test station.
8. **Sketches** copied to each student folder at the milestone that needs them: `00_motor_test.ino`, `01_flight.ino`, `T2_flight_starter.ino`. **In each copy the teacher sets `STATION` (1–8)** so the drone's network is `DRONE-<station>`, and the station's Wi-Fi password (8+ English letters/digits) is written on the **teacher's sheet** and on the **pilot's station card** — a phone types it once and remembers it. A tape label with the name goes on the top plate.
9. **DevKit pin tips.** With pre-soldered male headers the 30 pin tips stand 2–3 mm below the PCB. Either clip them flush (60 seconds per kit, ~0.5 g saved) or plan for the full-footprint 3 mm foam pad / nylon standoffs at M4 — say which on the card; the student must not guess whether the tape is supposed to reach.

---

## Session structure

A "session" is **one 45-minute class period** with ~30 minutes of work time in two 15-minute blocks ([Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §5.2). Project 8 is the longest project in the program by design. Nothing pushes a student to finish on a schedule (Principle 5, Principle 9); a milestone that spills into the next session is normal and the card says so.

**Tier 1 — seven sessions (typical).**
- S1 — M1 (safety contract + meet the parts, together) · M2 (press-fit the motors).
- S2 — M3 (meet the MOSFET board + multimeter) · M4 (mount the electronics, MPU flat and arrow forward).
- S3 — M5 (power tree) · M6 (motors to channels).
- S4 — M7 (signal wires) · M8 (multimeter pre-power check + first power-up).
- S5 — M9 (toolchain + libraries + upload motor-test) · M10 (spin the motors, no props, from the phone).
- S6 — M11 (props on, bench thrust test, the gate) · M12 (upload the flight sketch, sensor check).
- S7 — M13 (tethered first hover) · M14 (post-flight ritual + celebration). *Flight slots are short on purpose: one student's flight is ~5 minutes including the checklist; the rest of the class is building or spectating behind the line.*

**Tier 2 — nine to eleven sessions.** Two extra sessions for soldering the four channels (T2·M3–M5) and one for MT3608 tuning + the choice points; the flight-test sequence (T2·M16) often takes its own session.

**Tier 3 — Tier 2 plus three to five sessions** on the planner's PLAN / BUILD / CODE / TEST / SHOW.

**Flight days are declared days.** A session with any flying is declared a "flight day" at the mini-huddle: goggles for everyone from the start (hair back, sleeves up), the zone is clear, the battery bags are on the teacher's desk, and only the teacher hands out batteries and props. At the same huddle the teacher **names today's head-counter and one fallback out loud, by name** (fire procedure step 1), and declares the four flight-day rules: **the soldering station is switched off and unplugged at the huddle and stays cold for the whole flight block — soldering resumes only after the last battery is bagged** (a tip stays hot for minutes after unplugging, so "off during the slot" is not a rule that can be kept); **no charge is started or left running while any drone is live** — charging belongs to building time; **while a drone is live at the line, no USB cable is plugged into any drone** — a drone on USB broadcasts its network too, and two networks with the teacher's DISARM phone on the wrong one is the failure R6 exists to prevent: the teacher calls *"flight slot"* before handing out the battery and workstations pause uploads until *"clear"* (~5 minutes); and **every phone except the pilot's and the teacher's is in a bag** during flight slots — any phone that knows the drone's name and password is a second pilot. Building and flying in the same session is fine — building happens at the workstations, flying at the flight line, never both by the same student at the same moment.

## Setup and Wait Protocol

*Prep before the students enter. Pre-session time target: ≤ 15 minutes (plus the one-time pre-build above).*

### Teacher setup checklist (one-page version lives in the Teacher Setup Checklist artifact)

1. **Print and laminate the task cards for today's expected tiers**, the wiring reference (R1: pin map + power tree + channel map), the MOSFET-channel reference (R2), the safety-contract card (R3), and the pre-flight checklist (R4). Cards are in `Arduino_Projects/Project_8_Tiny_Quadcopter/task_cards_he/`.
2. **Per-station parts tray** according to the student's next milestone (the tray grows across sessions: frame + motors → board → DevKit/MPU/MT3608 → wires). **No battery and no props in any tray, ever.** Batteries are in the bag on the teacher's desk; props are in the two CW/CCW boxes on the teacher's desk.
3. **Multimeters** at two stations, set to continuity; a spare 9 V in each.
4. **Soldering station** (Tier 2 sessions only) ready but OFF until the student's ritual — iron on stand, damp sponge wet, eye protection laid out (P4 discipline). On a declared flight day it is off and unplugged for the whole flight block (see Session structure).
5. **Flight-day additions:** goggles count ≥ people in the room (and the hair-back / sleeves-up glance before every ARM); zone tape intact, lift-off mark ~40 cm from the anchor X; the flat anchor on the X with the 1.2 m tether bowlined on and the drone-end loop ready for the girth hitch; sand bucket and both fireproof bags at the teacher's desk within five steps of the zone; charger unplugged during flight slots; kitchen scale + thrust-test post + two rubber bands + the 30 cm backup line at the bench-test station (outside the circle); the pilot's station card with the drone's name and password; the teacher's phone charged, with the station passwords on the teacher's sheet; a prompt on the sheet: *name today's head-counter and fallback at the huddle*.
6. **Workshop PC(s):** Arduino IDE with the ESP32 core installed, board "DOIT ESP32 DEVKIT V1", libraries *Adafruit MPU6050* + *Adafruit Unified Sensor* installed (Library Manager). Test-compile `01_flight.ino` once on the machine before students arrive — this is the highest-risk setup failure.
7. **Shared Workshop Drive** — Google Drive for Desktop running, `G:\My Drive\Arduino_Projects\<nickname>\` visible for each expected student. Do not pre-create `Project_8_Tiny_Quadcopter` — it is created in the together-ritual at M1.
8. **Cool-down corner** set up (§5.6). **Review the tracking sheet** (§5.8) — on a flight day, note which students are on their first flight; their slot gets the full medical-alert / freeze attention.

### The "stuck" protocol (same on every task card)

If a student gets stuck on any step, before calling the teacher they try in order:

1. **Re-read the step.** The task card's "what to do" section often answers its own question on the second reading.
2. **Check the wiring reference card** at the station. For hardware steps, ~60% of stuck moments are wiring errors the reference card catches.
3. **Check the stuck-protocol reference card** at the station. It lists the most common upload errors and wiring mistakes with short fixes.
4. **Call the teacher** by raising a hand or saying the teacher's name. (No cup signalling, no flag — just the student's voice or hand. This is a deliberate Principle 8 choice — the call itself is a small relational moment.)
5. **If the teacher is busy** — wait at the workstation until the teacher rotates over.

**Project 8 additions to the stuck protocol (printed in red on every card):**
- **Anything with a battery connected, a prop fitted, or the soldering iron on is always "call the teacher" — never self-troubleshoot a powered drone.**
- **If anything smells hot, smokes, or a motor moves when nobody told it to — first ask: is a prop on?** **PROPS OFF (every build step): pull the battery plug first, then call.** Pulling the plug is the one action a student may take on a powered *props-off* drone without asking. **PROPS ON (M11 bench, M13 flight line): you never touch the drone** — contract rule 6: slider to 0, DISARM, say STOP; hands stay behind the line until every prop has stopped; only the teacher touches the drone, and only after the props stop. *Why: the battery plug sits under the propellers.*
- **Backup task for wait time:** *"Draw your drone from above and label FRONT, the four motors with CW/CCW, and where each wire goes."* Quiet, tactile, previews the wiring milestones, needs no teacher attention.

---
## Tier 1 — Guided Build (14 milestones)

**Who this tier is for.** Every student doing Project 8 for the first time who wants the clearest path, and every student for whom the soldering of sixteen-plus joints on a power board would be the wrong place to spend their confidence. Tier 1 gets the MOSFET board pre-soldered and the MT3608 pre-tuned; the student still does **all** the wiring, **all** the measuring, **all** the tests, and the flight. Fourteen milestones because the build is the largest in the program (§6.12 says 12–15); each is still one 15-minute-scale chunk, and each ends in something the student can see, measure, or hold.

**Claude Code usage at Tier 1.** Channel A Level 1 throughout — two pre-written sketches (`00_motor_test.ino`, `01_flight.ino`), no editing. Channel B available from M2 onward and particularly valuable on this long sequence; not used at M1 (the teacher is speaking) and not used at M13 (the flight line is a no-screens-except-the-controller place).

**Three rituals that repeat.** *Battery custody:* the student never takes a battery; the teacher hands one over at the moment a milestone needs it and takes it back when the milestone ends. *Props last, off first:* props are fitted only at M11 and M13, at the bench-test station / flight line, **in the Safe state (battery out) as the last thing before the battery goes in**, and they come off **first, right after the battery comes out** — the two four-word rituals are **ON: props → battery → ARM** and **OFF: DISARM → battery → props**. *Goggles:* on for everyone in the room from the first moment any motor can spin (M10 onward), with hair tied back and sleeves pushed up — and on for the multimeter/solder work before that by habit.

---

### Milestone 1 — Meet the parts and sign the safety contract (together-milestone)

**Goal.** The student knows every part by name and touch, has their Project 8 folder, and has agreed to the six flight rules before anything is built.

**Steps.**
1. Folder ritual, same as every project: `G:\My Drive\Arduino_Projects\<nickname>\Project_8_Tiny_Quadcopter\`, Claude Code opened on it. Recognition line: *"This is your folder, this is your project — Project 8, the last one, starts now."*
2. Parts tray walk-through with the teacher, each part picked up and named: frame (two plates, grommets, caps, O-rings), the four motors (two colour-pairs — CW and CCW), the DevKit (the same brain as the car and the weather station), the MPU6050 ("it feels which way is down"), the MT3608 ("makes 5 V for the brain"), the MOSFET board ("four electronic switches, one per motor"). The teacher shows — does not hand over — a battery and a prop, and names the two things in the room that can hurt.
3. The **safety contract card (R3)**: the teacher reads the six rules aloud, the student reads them back in their own words, both sign. The six rules: **goggles on whenever a motor can spin · props on last, off first · one battery out of the bag = one drone alive, and the teacher hands it out · nobody inside the circle when a drone is armed · always on the tether · anyone says "STOP" → slider to zero, DISARM, hands off.** The card glosses rule 2 in one line: *last = the last thing before the battery goes in; first = right after the battery comes out.* A student who is reliably non-speaking under pressure agrees a **READY signal** with the teacher here (a thumbs-up held for two seconds, a hand on the tape line, the green side of a signal card — chosen with the student) and it is written on the contract card; it is the student's answer to "Ready?" at the flight line.
4. The student puts on their goggles and adjusts the strap — they will live in the student's tray for the whole project.
5. Weigh the empty frame and the tray's parts on the kitchen scale (~75 g without battery) — the first number in the weight log on the card.

**Expected result.** A signed contract card in the tray, a folder on the Drive, and a student who can point at each part when the teacher names it.

**Done when.** The folder exists, Claude Code is open on it, the contract is signed by both, the student can say the six rules in their own words, and the weight log has its first line.

**Stuck / teacher notes.**
- A student who will not sign is not refused the project — the teacher asks what rule is the problem and talks it through (§5.7 refusal-as-information). No signature, no flight day; building can start.
- The contract card is the single most important artifact of Project 8: every later "STOP" or "props off" is a reference back to it, not a new rule.

*[Verification: Principle 8 — the together-milestone; Sciacca (2025) trusting relationships. Principle 3 — every part is in the hand before it is in a diagram.]*

---

### Milestone 2 — Press-fit the four motors into the frame

**Goal.** Four motors seated in the frame's rubber grommets, the right rotation on the right arm, leads routed to the center.

**Steps.**
1. Find the "FRONT" arm (the teacher's paint mark). Lay the frame flat with FRONT away from you.
2. Take the two **CW motors (red/blue leads)**. Push one, shaft up, down through the **FRONT** grommet until the motor's shoulder sits on the rubber; same for **BACK**. Firm thumb pressure, no tools, no glue.
3. Take the two **CCW motors (black/white leads)** → **RIGHT** and **LEFT** grommets, the same way. (Right and left are the drone's right and left when FRONT points away from you.)
4. Press a rubber motor cap onto the bottom of each motor — these are the landing feet.
5. Route each motor's two leads along the arm toward the center plate and tuck them under the plate edge; nothing may hang near a prop circle.
6. Spin each shaft with a fingertip: free, no grinding.

**Expected result.** A frame with four motors and four feet that stands level on the table; all eight leads end at the center.

**Done when.** FRONT and BACK carry red/blue motors, RIGHT and LEFT carry black/white motors, all four are fully seated, all four shafts spin freely, and the student has written "F=CW B=CW R=CCW L=CCW" on the card.

**Stuck.**
- Motor will not go in: the grommet is tilted — push it out, re-seat it square, try again. Never hammer, never glue.
- Motor wobbles in the grommet: wrong grommet size or a torn grommet — swap from the spare frame kit in the spares box.
- Which is right, which is left? Hold the frame with FRONT pointing away from you; your right hand is the drone's right.

---

### Milestone 3 — Meet the MOSFET board (pre-soldered) and check it with the multimeter

**Goal.** The student can read the pre-built board — which pad is which — and proves with a multimeter that it has no shorts before it is ever connected to anything.

**Steps.**
1. Hold one spare **IRLB8721** label-up, legs down: say **"Gate – Drain – Source, left to right"**; touch the metal tab — *"the tab is Drain; the four tabs on the board must never touch."*
2. On the board, find and point to: **BAT+ rail, GND rail, M1+…M4+, M1−…M4−, G1…G4, the 220 µF capacitor (stripe = −), the four diodes (band toward BAT+)**. Card R2 has the same picture.
3. Multimeter to **continuity (beep)**. Probe **BAT+ rail ↔ GND rail: no beep** (a beep = a short — stop, call the teacher).
4. Probe **tab-to-tab** for every pair of MOSFETs: **no beep**.
5. Multimeter to **Ω (20 k range)**. Probe **each G pad ↔ GND rail: about 10 kΩ** (that is the pull-down). Then **each M− pad ↔ GND: OL / very high** (the MOSFET is off when its gate is at 0 V).
6. Write the four G-to-GND readings on the card.

**Expected result.** No beeps where there must be none; four readings near 10 k.

**Done when.** BAT+↔GND no beep, no tab-to-tab beep, four gate readings between 9 and 11 kΩ, and the student can name G-D-S and say which pin the tab is.

**Stuck.**
- Meter shows "1" or "OL" on the gate check: wrong range — set the dial to 20 k (or auto), make sure a probe is on copper, not solder mask.
- Meter beeps BAT+↔GND: do not connect anything; call the teacher (a solder bridge, a reversed diode, or a reversed capacitor).

*[Verification: Principle 3 — the "invisible" switch is made concrete by a meter reading before a volt touches it; P1's pull-down comes back as the same idea on a bigger switch.]*

---

### Milestone 4 — Mount the electronics on the frame (MPU flat, arrow forward)

**Goal.** DevKit, MPU6050, MT3608 and the MOSFET board fixed to the frame in the positions the wiring expects — **every board on its own insulator, because the black plate conducts electricity like a wire** (the teacher shows the tray's plate reading from the pre-build).

**Steps.**
1. **Tether loop** (already fitted on a Tier 1 kit — check it; Tier 2 fits it now, while the bottom plate is still bare): a 10 mm loop of 1 mm braided cord through two adjacent holes on the bottom plate's centreline, knotted on the top face, hanging ~10 mm clear below the plate and clear of the battery bay. The tether will be girth-hitched to this loop at every flight; it sits under the centre of gravity.
2. **DevKit** on the top plate, centered, **USB connector toward the BACK arm** (so the cable never crosses the FRONT), on a **full-footprint 3 mm foam-tape pad** laid on the plate's insulating layer so the header-pin tips sink into the foam (or on the two nylon standoffs, if the kit uses them). Press 10 s. *A pin tip touching the plate joins VIN or 3V3 to GND through the carbon.*
3. **MPU6050** on a square of **foam tape that covers its whole footprint** (not a centre dot) on the top plate, directly in front of the DevKit, chip side up, **board flat to the plate** (check by eye from the side), and the silk-screen **X arrow pointing at the FRONT motor**. Press gently — do not crush the foam.
4. **MT3608** on the top plate beside the DevKit, pot screw reachable, on full-footprint foam tape on the same insulating layer.
5. **MOSFET board** under the bottom plate, the four TO-220s laid flat with their **tabs heat-shrunk**, labelled side readable, **M1 pad nearest the FRONT arm**; an **insulating sheet (Kapton, or a plastic card trimmed to the board outline) between the perfboard's solder side and the carbon plate**, then full-footprint 1–2 mm foam double-sided tape (not corner dots); a small 2.5 mm zip tie through the plate slots goes *on top of* that layer, never instead of it. No glue or thick tape on the MOSFETs — the foam pad only.
6. **Battery bay:** the cell sits **under the board** on a **2 mm foam/EVA pad that covers the whole component side**, held **only by the two frame O-rings** through the plate slots (never a zip tie, never tape on the cell), its lead routed out with slack to the side where the plug exits; cloth tape on the two plate edges the O-rings cross. The pouch may touch only smooth faces — nothing sharp, no solder spike, no clipped lead, no tab top, no plate edge. The bay stays empty and reachable: a battery must slide in and out by hand, without tools.

**Expected result.** A drone-shaped object with every board in place and on its insulator, the FRONT arrow on the MPU matching the FRONT arm, a tether loop under the centre.

**Done when.** The teacher confirms: MPU flat and arrow → FRONT, DevKit USB → BACK, MOSFET board M1 → FRONT, **no metal touches carbon — every board on its own insulating pad**, the tether loop hangs clear of the battery bay and outside every prop circle, a finger run over the bay with the battery out finds nothing sharp and nothing metal, nothing inside any prop circle. **Plate check:** meter on Ω (2 M or auto), black probe on a bare plate edge or a screw hole (not the glossy face): BAT+ pad, GND pad, VIN pin, 3V3 pin, each M− pad and each G pad in turn → **OL**. Anything that shows a number = lift that board, add a shim, remount.

**Stuck.**
- MPU foam pad looks tilted: peel and redo — a tilted sensor means a drone that always leans.
- Not sure which way the arrow points: the GY-521 prints "X" with an arrow near the chip; if the arrow is unreadable, the teacher marks it with a paint dot.
- The meter shows a number from a pad to the plate: a pin tip or a tab is through the foam, or the board's solder side is on bare carbon — lift, add the sheet, remount, re-measure.
- Why foam and not plain tape? The card's one-liner: *"motor vibration through hard tape makes the sensor see shaking instead of tilt — and the foam keeps the pins off the carbon."*

---

### Milestone 5 — Power-tree wiring

**Goal.** Battery pigtail → board; board → MT3608; MT3608 → DevKit; DevKit 3V3/GND → MPU. No battery connected yet.

**Steps.**
1. The **PH2.0 pigtail** is already soldered to the board's **BAT+ / GND** pads (teacher). Identify it; red = BAT+.
2. **Board → MT3608:** a red 22–24 AWG wire from the board's second **BAT+** pad to **MT3608 IN+**; black from the board's second **GND** pad to **MT3608 IN−**. (Strip 3 mm, tin, solder — the P4 ritual; teacher nearby; or pre-tinned pads for a lighter solder.)
3. **MT3608 → DevKit:** red from **OUT+** to the DevKit **VIN** pin; black from **OUT−** to the **GND pin next to VIN** (right header). Use female Dupont ends on the DevKit side, or solder to the header pins.
4. **DevKit → MPU6050:** thin red from **3V3** to MPU **VCC**; thin black from the **GND next to 3V3** (left header) to MPU **GND**. The card says it in red: **3V3, not VIN, not 5 V.** *(Teacher's why, not the card's: everything the ESP32 touches stays on one 3.3 V rail so no 5 V can ever reach a GPIO; the sensor module itself has its own regulator and would not be harmed.)*
5. Tidy: power wires away from the prop circles, one small zip tie or a dab of hot glue per wire as strain relief (not on the MOSFET board).

**Expected result.** Six power wires in place, red to +, black to −, every one matching the R1 power tree.

**Done when.** The student ticks the six lines on the card's power-wiring list and the teacher has eyeballed polarity at the MT3608 and the DevKit.

**Stuck.**
- Which GND? Two GND pins on the DevKit: the one **next to VIN** is for the MT3608; the one **next to 3V3** is for the MPU.
- The MT3608's IN/OUT labels are tiny: IN is the side with the big coil next to it on most modules — the teacher's silver marker has already marked "IN" / "OUT 5.0 V ✓".

---

### Milestone 6 — Motor wiring to the four channels

**Goal.** Each motor's two leads on its own channel, FRONT on M1, RIGHT on M2, BACK on M3, LEFT on M4.

**Steps.**
1. Trim each motor's leads so they reach their pads with ~1 cm spare (shorter = lighter), strip 2 mm, tin.
2. **FRONT motor → M1:** red (or the lighter of the pair) to **M1+**, blue/black to **M1−**.
3. **RIGHT motor → M2:** "+" lead to **M2+**, "−" lead to **M2−**. **BACK → M3**, **LEFT → M4** the same way. (8520 convention: red/white = +, blue/black = −. If a motor later spins the wrong way, swapping its two wires is the fix.)
4. Solder each (teacher nearby), heat-shrink any bare lead that could touch a neighbour.
5. **Continuity check:** meter on continuity, probe **M1+ ↔ M1−**: a beep or a few ohms (that is the motor winding). Repeat M2–M4. Then **M1+ ↔ M2−: no beep** (channels are independent).

**Expected result.** Eight joints, four motor windings readable through their pads.

**Done when.** All four M+↔M− checks read the motor (beep / 1–3 Ω), no cross-channel beep, and the student has written which motor sits on which channel.

**Stuck.**
- Lead too short after trimming: splice a 2 cm extension with heat-shrink — call the teacher.
- No beep on one motor: a cold joint or a broken hair-thin lead at the motor — reflow, or swap the motor from spares.

---

### Milestone 7 — Signal wiring (gates + I2C)

**Goal.** Four gate wires and two I2C wires from the DevKit to their pads — the six thin wires that carry information rather than power.

**Steps.**
1. Four thin signal wires in four colours, ~8 cm: **yellow GPIO 25 → G1 (FRONT)**, **orange GPIO 26 → G2 (RIGHT)**, **green GPIO 14 → G3 (BACK)**, **blue GPIO 27 → G4 (LEFT)**. The four GPIOs are **four pins in a row** on the right header: 14 · 27 · 26 · 25.
2. **White GPIO 21 → MPU SDA**, **grey GPIO 22 → MPU SCL**.
3. Female Dupont on the DevKit side (or solder), solder on the board/MPU side. Route the gate wires under the plate, away from the motor leads.
4. Meter on Ω: **each GPIO pin ↔ GND: ~10 kΩ** — the same pull-down reading as M3, now seen from the brain's side (proves the gate wire is connected).
5. Count with the card: **22 connections** in the whole drone — power 6, motors 8, gates 4, I2C 2, battery 2.

**Expected result.** A fully wired drone with no battery, that the meter says is sane.

**Done when.** The four gate readings are ~10 k from the DevKit pins, SDA/SCL go to 21/22, the card's 22-line checklist is fully ticked, and the teacher has signed the card's "wiring checked" box.

**Stuck.**
- A gate reads OL from the DevKit pin: the wire is on the wrong header pin (count from VIN: VIN, GND, 13, 12, **14**, **27**, **26**, **25**) or the Dupont is not seated.
- SDA/SCL swapped is harmless to the hardware — M12's sensor check will show "MPU not found" and the fix is a swap.

---

### Milestone 8 — Multimeter pre-power check and first power-up (together-milestone)

**Goal.** Prove the drone is safe to power, then power it — and see the DevKit's LED with the right voltages, no props, nothing moving, nothing warm.

**Steps.**
1. **Before any battery:** continuity **pigtail red ↔ pigtail black: no beep.** Tab-to-tab: no beep. **Plate sweep:** meter on Ω, one probe on a plate screw head or a drilled-hole edge (not the glossy face), the other on BAT+, GND, VIN, 3V3, each M− pad and each gate pad in turn: **OL everywhere** — *the black plate conducts like a wire; a board touching it is a short.* Goggles on, hair back, sleeves up (habit — the motors could theoretically move from here on).
2. The teacher brings **one battery**, meter on DC V: **battery plug: 3.7–4.2 V, red positive**. If the meter reads negative, the battery's connector is reverse-wired — it goes back in the bag with a red label; never "just flip it".
3. USB **not** connected. Drone flat on the table. The teacher plugs the battery in **while the student watches the motors**: the DevKit's red power LED lights; **no motor moves** (a ≤ 0.1 s twitch of the BACK motor is normal; a motor that keeps turning = pull the plug).
4. Meter on DC V: **DevKit VIN ↔ GND: 4.9–5.1 V**; **MPU VCC ↔ GND: 3.2–3.4 V**; **board BAT+ ↔ GND: battery voltage**.
5. Back of a finger on the MT3608, the DevKit's regulator, each MOSFET: **cool or faintly warm**, never hot. Wait 30 s, touch again.
6. The teacher unplugs the battery and takes it back. The three readings go on the card.

**Expected result.** A drone that powers up quietly with 5.0 V on the brain and 3.3 V on the sensor.

**Done when.** No-beep checks passed, LED on, no motor motion, VIN 4.9–5.1 V, MPU 3.2–3.4 V, nothing hot, the readings are on the card, and the battery is back with the teacher.

**Stuck.**
- No LED: MT3608 wires reversed or not on OUT; or the MT3608 is not the tuned one — check the silver "5.0 V ✓" mark.
- A motor spins at plug-in: **pull the plug.** The gate wire is on the wrong pin, the G pad reads OL (missing pull-down) — back to M7's meter check — or a Drain tab is touching the carbon plate (the plate sweep in step 1).
- Anything hot, any smell: pull the plug; a reversed diode or reversed capacitor — teacher.
- A number (not OL) on the plate sweep, or the drone gets warm and reboots when the motors spool later: a pad or a pin is touching the plate — unstick the board, add the insulating pad (M4), re-check.

*[Verification: Principle 3 + the program's power-off discipline (§5.6): test with a multimeter before first power-up. The teacher's presence is the relational anchor for the first powered moment (Principle 8).]*

---

### Milestone 9 — Toolchain, libraries, and upload the MOTOR-TEST sketch

**Goal.** The workshop PC talks to the DevKit, the two libraries are installed, and `00_motor_test.ino` is on the drone.

**Steps.**
1. **Battery out** (it is — with the teacher). Plug the USB cable into the DevKit. Arduino IDE: **Tools → Board → ESP32 Arduino → "DOIT ESP32 DEVKIT V1"**; **Tools → Port → the new COM port**; **Tools → Upload Speed → 115200** (fewer failed uploads on cheap cables).
2. **Tools → Manage Libraries** (or the Library Manager sidebar): search **"Adafruit MPU6050" → Install** (accept "install all dependencies"); check **"Adafruit Unified Sensor"** is installed too. (Same ritual as P6's DHT/SSD1306 installs.)
3. Copy `00_motor_test.ino` from the teacher's folder into your Project 8 folder; **File → Open** it. Read its header: it says what it does and that **props must be off**. The teacher has already set your station number in it (`STATION`), so the drone's network will be **DRONE-<your station>** — the name on the tape label on your frame.
4. Click **Upload**. Wait for *"Hard resetting via RTS pin…"*. If the IDE sits on "Connecting…", hold the DevKit's **BOOT** button until the dots move. *(On a flight day: uploads pause while a drone is live at the line — the teacher's "flight slot" / "clear" — because a drone on USB broadcasts its network too.)*
5. Open the Serial Monitor at 115200: the sketch prints its banner — its name, the throttle ceiling (`Throttle ceiling: 100 % = 255 / 255`) and the four motor pins — and then `Network: DRONE-xx`, `Password: …` and `Page: http://192.168.4.1`. Write the network name on the card (the password is on your station card).

**Expected result.** A successful upload and a Serial banner with your drone's own name.

**Done when.** "Done uploading" in the IDE, the banner in the Serial Monitor, both libraries shown as installed, the network name written on the card and matching the label on the frame.

**Stuck.**
- No COM port: charge-only USB cable (swap), or the CP2102 driver — the Teacher Setup Checklist covers the driver once per PC.
- Compile error mentioning `ledcAttach`: the ESP32 core is older than 3.x — update "esp32 by Espressif" in Boards Manager (the sketches target core 3.x).
- Upload "Connecting…" forever: hold BOOT; if still stuck, unplug/replug USB and retry.

---

### Milestone 10 — Spin the motors WITHOUT props, from the phone slider

**Goal.** Each motor answers its own button, all four answer the slider — the project's first *"my motors spin when I move the slider"* win. No props.

**Steps.**
1. **Goggles on, hair tied back, sleeves up — everyone at the station.** Confirm by touch: **no props on any motor.** USB out. Drone flat on the table, **hands off** — with no props there is no lift, so nothing needs holding (the physics point M11 then measures).
2. The teacher hands over one battery; the student plugs it in (teacher watching the motors). LED on, no motor moving.
3. Phone: **Settings → Wi-Fi → DRONE-xx** (the name on your drone's label; **password on your station card** — typed once, the phone remembers it; if the phone warns "no internet", stay connected); browser → **192.168.4.1**. The motor-test page appears: an **ARM / DISARM** pair, a throttle slider **0–100 %** (100 % = full motor power; **the motors follow the slider *up* slowly — about half a second from 0 to full — and *down* instantly**), and four **per-motor test buttons FRONT / RIGHT / BACK / LEFT** that work only while ARMED and the slider is at 0.
4. Slider at 0. Press **ARM** (the grey banner turns green and reads *חמוש · ARMED*; the blue LED goes solid). Press **FRONT**: the FRONT motor — and only it — spins for 2 s at a low fixed speed (~25 % power), then stops by itself; the page's motor number shows the test power for those 2 s and snaps back to 0 — that is normal, not a fault. Then RIGHT, BACK, LEFT. Write a ✓ next to each on the card. *A button that spins a different arm than its name = two gate wires swapped at the header.* A second press during a run is ignored; DISARM ends a run at once.
5. Slider: slowly up to ~30 % — all four spin; to ~50 % — louder; hold a minute — nothing hot; back to 0. The pitch of the sound rises and falls with the slider.
6. The teacher says **"STOP"** once, as a rehearsal: the student zeros the slider and presses **DISARM**. Then the second half of the drill: **after any DISARM the drone stays down until the slider is at 0 and a fresh ARM press arrives — nothing re-arms by itself.** The teacher unplugs the battery and takes it back. Touch test: motors and MOSFETs warm at most.

**Expected result.** Four motors, each individually addressable, all four following the slider — without a single propeller in the room.

**Done when.** All four per-motor ✓s, the slider test done, the STOP rehearsal done, DISARM pressed, battery back with the teacher, and the card's line "what did the slider do to the sound?" answered.

**Stuck.**
- A button spins the **wrong** motor: two gate wires are swapped at the DevKit — note which, fix at the header, re-test. (Do not change the sketch.)
- A button does nothing: the page is not ARMED, the slider is not at 0, or another motor's 2 s run is still going — wait, slider to 0, try again.
- One motor never spins: its gate wire, its joint at the M pads, or a fake MOSFET — the M7 meter check from the DevKit pin finds the first two.
- The page does not load: forget other `DRONE-xx` networks on the phone, turn mobile data off, re-join, reload. The network asks for a password: it is on your station card.
- **ARM is refused although the slider shows 0:** press DISARM once, then ARM (the page says why in Hebrew — *המחוון לא על 0*).
- The page says **מסך צפייה - DISARM בלבד** ("viewing screen — DISARM only"): this phone is not the one that pressed ARM — the drone takes the slider only from the pilot's phone; any phone may DISARM.
- The page disarms by itself after a moment: the phone's screen went to sleep or the browser went to the background — the 600 ms watchdog did its job. Keep the page in front; slider to 0, re-ARM.
- The DevKit reboots when the slider goes up (the blue LED restarts its calibration flicker and the page drops): the 220 µF cap is not on the rails, or the MT3608 IN wires are long and thin — teacher.

*[Verification: §6.12 — "the beginner motor-test firmware step is crucial — it gives the student a success milestone before the PID-tuned hover attempt." Principle 4.]*

---

### Milestone 11 — Props on, bench thrust test on the kitchen scale, and the T/W gate (together-milestone, flight-day rules)

**Goal.** With propellers fitted for the first time, measure how hard the drone pulls upward and decide — with numbers — whether it may fly.

**Steps.**
1. **Flight-day rules from here:** goggles on **everyone in the room**, hair back, sleeves up; the soldering iron is off and cold; the bench-test station is outside the flight circle; the teacher hands out the **four props** (2 CW + 2 CCW) at the station, nowhere else. **Battery not yet connected.** Printed in red on this card instead of the generic rule: **with props on you never touch the drone — slider to 0, DISARM, say STOP; only the teacher touches it, after every prop has stopped.**
2. **Fit the props:** **CW props on FRONT and BACK, CCW props on RIGHT and LEFT** (R1 shows the blade shapes; the CW/CCW boxes are labelled). Press each prop straight down onto the 1.0 mm shaft until it seats; tug-test — a prop that pulls off easily goes back in the box and a spare is used.
3. **Weigh:** drone + (the teacher's) battery on the scale → **AUW** in grams, written on the card. **Then the rig (teacher's hands):** the drone goes **upside-down on top of the thrust-test post** — props toward the scale pan, exhaust toward the ceiling — held by **two rubber bands across the centre plates** (not across arms or motors), the battery in its O-rings (check it cannot drop out of the bay inverted), the prop plane **≥ 65 mm (one prop diameter) above the pan**, the post top no wider than ~45 mm so it does not reach under the prop discs. A **30 cm backup line** from the post's base to the frame's tether loop, slack — a lanyard, not a load path (the circle tether stays at the anchor; it cannot reach the bench). Post + drone on the scale, **tare to 0** with everything in place. The teacher tug-tests the bands in all four directions. *Why inverted: upright, the props blow straight down onto the pan and the scale reads 30–70 % low; inverted, thrust presses the drone onto the post and the number is real. The motor-test sketch has no sensor, so upside-down changes nothing in the code.*
4. The teacher plugs in the battery; phone → DRONE-xx → motor-test page → ARM. Everyone's hands are behind the line the tape marks on the bench (≥ 50 cm from the props) from battery-in to battery-out.
5. **Direction check (one motor at a time):** press FRONT — the scale reading goes **positive** (the prop blows air at the pan = it is lifting). Then RIGHT, BACK, LEFT. A reading that stays **near zero or goes negative** = that motor is spinning backwards → note it on the card. *(At the buttons' ~25 % power one motor is only 5–10 g — read the sign, not the size; if a sign is unclear, check by elimination: all four on the slider at 40 %, then compare with three.)* **The fix is a solder job, not a bench job:** after step 6 — **DISARM → battery out (teacher) → props off, all four, into the boxes** — the drone goes back to the workstation, the teacher unsolders that motor's two leads and swaps them at its M pads, **M6's M+↔M− continuity check** is re-run on that channel, and then back at the bench: props on again (tug each), post, bands, tare, battery from the teacher, re-run the check for that motor.
6. **Thrust, three readings and the hover point:** slider to **60 %** — wait a second for the motors to climb and the scale to settle, read and write; to **80 %** — read and write; to **100 %** (= full motor power) — read and write. Then back to 50 % and up in **5 % steps**, watching the scale: **the slider % at which the reading first passes the AUW is the hover point** — write it. Slider to 0, **DISARM**, battery out (teacher). Reading at 100 % ÷ AUW = **T/W** (written as a number; the gate is the hover point).

**Expected result.** AUW, three thrust numbers, a hover point and a ratio on the card; every motor lifting, not pushing.

**Done when.** AUW, the three thrusts and the hover point are written, all four motors lift (positive readings), and the teacher has written the decision line from the Hardware section's gate: **hover point ≤ 75 % → "fly"** (tethered, like every flight) — *or* **75–85 % → "tethered only, ≤ 30 cm, weight ladder before the next session"** — *or* **above 85 % / never → "weight ladder first, no flight this session"**. **The battery is back with the teacher and the props come off before the drone leaves the station** (M12 needs USB; no USB with props on).

**Stuck.**
- Scale jumps around: the post is too light (≥ 300 g) or tipping — a wider base; the backup line is taut — give it slack; the scale's "hold" mode is on — off.
- Thrust much lower than the table: **props too close to the post or the pan** (≥ 65 mm — the first suspect), air recirculating (move the rig to the table edge, away from walls), tired battery (measure it — below 3.8 V, swap), a prop slipping on its shaft (tug-test), or one motor backwards dragging the total down (the per-motor check finds it).
- The drone comes loose from the bands: **slider to 0, DISARM** — the M10 STOP drill; nobody's hand until the props stop; the teacher re-bands with the battery out.
- Hover point above 85 %: the weight ladder in the Hardware section — the teacher decides which rung; the student re-weighs next session. This is engineering, not failure — the card says so. The answer is never more throttle.

*[Verification: §6.12 — "the discipline of pre-flight validation: the drone must pass a bench thrust test before it is allowed to fly." Principle 3 (the number comes from a scale the student reads), Principle 4 (a measurable checkpoint that is not a flight).]*

---

### Milestone 12 — Upload the FULL flight sketch and check the sensor

**Goal.** `01_flight.ino` on the drone; the sensor visibly reporting tilt on the phone page.

**Steps.**
1. **Props off** (they came off at the end of M11 — confirm by touch). Battery out. USB in.
2. Copy `01_flight.ino` into your folder, open it, read the header (what ARM does, the watchdog, the slow throttle climb, the sensor-loss stop), **Upload** (the teacher has set your `STATION` in this copy too). Serial Monitor: **"Calibrating gyro…"** then **"Calibrated."**, **"Network: DRONE-xx"**, **"Page: http://192.168.4.1"**.
3. **USB out.** The teacher hands over the battery; plug in with the drone flat and still on the table — the blue LED **flickers fast for 2 s (gyro calibration); a drone that is moved during those 2 s flies crooked** (the card says: plug in, hands off, count to three). Short blink once a second = ready, disarmed.
4. Phone → DRONE-xx (password on the station card) → 192.168.4.1: the flight page — **ARM / DISARM**, the slider, live **ROLL / PITCH** in degrees, **yaw rate**, the **four motor numbers** (shown grey, labelled *preview — motors off*, while DISARMED: what the brain *would* send), and the four per-motor test buttons. Do **not** ARM yet.
5. Tilt the drone nose-down by hand: **PITCH goes positive** (nose low) and returns to ~0 when flat. Tilt the right side down: **ROLL goes positive**. Flat is ~0 on both. *(If the signs come out backwards, the sensor is mounted the wrong way round — fix the mounting at M4, not the code.)*
6. **Logic check of the brain, DISARMED, motors off** — hair back, sleeves up, the drone lifted **by the two centre plates only**, fingers under the bottom plate, never over an arm, shafts pointing away from faces: **nose down → FRONT's grey number goes up, BACK's goes down; right side down → RIGHT up, LEFT down; turn it counter-clockwise → RIGHT + LEFT up, FRONT + BACK down; hold still → all four settle to about the same number.** Put it down flat.
7. **One short armed check, drone flat on the table, hands off** (goggles on; no props — confirm by touch; the teacher beside the student; the second and last bench ARM after M10): slider 0 → ARM → slider ~30 % — all four spin and settle to about the same number; nudge one arm edge up 2–3 cm **with a pencil**, not a finger — that motor's number drops, the opposite one rises. Slider 0, DISARM. Battery out, back to the teacher. *A live drone is touched only by a still hand on the centre plate; it is never lifted, tilted or turned while armed.*

**Expected result.** Live tilt numbers that follow the student's hands, and (grey) motor numbers that push the low side up.

**Done when.** Upload done, ROLL/PITCH within ±2° when flat and moving in the right direction when tilted, the four preview checks of step 6 pass, the armed check of step 7 done, DISARM pressed, and the battery is back with the teacher.

**Stuck.**
- LED flickers fast and never stops / Serial says "MPU6050 not found": SDA/SCL swapped (swap at the header), MPU VCC not on 3V3, or the GND-next-to-3V3 wire — M7's list.
- The page says **"sensor lost"** and the LED flickers endlessly mid-check: an I2C wire shook loose — the drone disarmed itself and will not ARM again until it is rebooted (battery out, wire fixed, battery in).
- PITCH reads ±5° while flat: the drone was moved during calibration, or the foam pad is tilted (M4) — unplug, set flat, replug, hands off.
- ARM is refused: the slider is not at 0, the drone is more than 20° from level, or the sensor is not answering — the page says which, in Hebrew. **ARM refused while the slider shows 0: press DISARM once, then ARM.**
- Pitch and roll seem swapped or sign-reversed: the MPU's arrow is not toward FRONT — re-mount (M4).
- The check moves the **wrong** motor's number: impossible (that is the code); the wrong **motor** physically speeding up at step 7 = gate wires swapped (M10's per-motor buttons / M7's meter check).

---

### Milestone 13 — Tethered first hover (together-milestone; the flight line)

**Goal.** The drone leaves the floor on a tether, hovers at 10–30 cm for a few seconds, and lands on command. The student's own flight.

**Steps.**
1. **Pre-flight checklist R4 aloud, teacher and student, the eleven items in R7's order, no paraphrase** (the list is in the Safety Protocol section): everyone goggled, hair back, sleeves up, iron cold · circle and line clear, every other phone in a bag, no drone on USB · drone on the bench, battery out, props off · battery ≥ 3.8 V on the meter · wiring tucked, MPU flat, motors seated, bay pad in, cell undented · **props on now, from the teacher's box, with the battery still out** (CW F/B, CCW R/L — tug each) · tether girth-hitched to the frame loop, both knots inspected, anchor on the X · both phones ready (Wi-Fi on, mobile data off, stale DRONE-xx networks forgotten, screen-sleep off). Printed in red on this card: **with props on you never touch the drone — slider to 0, DISARM, say STOP; only the teacher touches it, after every prop has stopped.**
2. The student places the drone on the **lift-off mark** (~40 cm from the anchor X, so the slack line lies flat on the floor and the drone never hovers over the anchor), FRONT away from the spectator line; the teacher plugs the battery in; hands off until the blue LED stops flickering (~2 s); **both walk out of the circle** and stand behind the spectator line. **Only now the phones join:** at the line both phones join **DRONE-xx** (a phone that remembers the network re-joins by itself in 10–30 s — wait at the line, do not re-enter the circle), reload 192.168.4.1, **DISARMED** on both, slider at 0, and the page's network line (**רשת: DRONE-xx**) matches the label on the frame. *The drone's Wi-Fi is born when the battery goes in and dies when it comes out — every battery means a fresh join, and the wait is part of the slot.* The teacher's page is for **DISARM only** — never ARM, never the slider on it. Then: *"Ready?"* — in words, or the READY signal from the contract card — *"Clear."* — **ARM** (pilot's phone).
3. Slider up *slowly* — the sketch backs this up (the motors can only climb at a fixed rate, ~0.5 s from 0 to full) but does not replace it: the student still flies the thing. At ~30–40 % the motors sing; at ~50–70 % the feet get light; a little more and the drone lifts. **Hold at 10–30 cm** — the tether stays slack. Breathe. Count five.
4. Slider **down slowly** until the feet touch; slider to **0**; **DISARM**. If the drone tilts, drifts toward the line, or anything feels wrong: **slider to 0 → DISARM** — a 20 cm drop on rubber feet is nothing. **After DISARM, before anyone crosses the tape, the pilot's phone goes face-down on the floor behind the line (or into the teacher's hand)** — a phone in a hand is a drone that can wake up.
5. Second and third hover if the student wants them, same sequence — slider at 0, a fresh ARM press each time. **≤ 3 minutes total motor time on this battery: the page's motor-time counter says where you are (the teacher's page shows it too); the teacher calls "land" at 3:00.**

**Expected result.** Feet off the floor, a level hover, a landing on command.

**Done when.** The drone lifted off under the student's slider, stayed roughly level for ≥ 3 s, landed on the slider, DISARM was pressed and the phone put down — witnessed by the teacher. One clean hover is the bar; no duration, no precision.

**Stuck.**
- Lifts one side first / flips at lift-off: **slider to 0, DISARM** — a prop on the wrong motor (CW on a CCW arm) or one motor reversed (M11's direction check would have caught it — re-run it). Never "give it more throttle to see".
- Rocks back and forth faster and faster: **DISARM** — the controller is too aggressive for this build; the teacher lowers `KP` by 0.2 in the sketch (a Tier 2 skill the teacher does for a Tier 1 student) and re-uploads next slot.
- Slowly turns (yaws) while hovering: one rotation pair is wrong (F/B must match, R/L must match) or the build is paired the other way round (`YAW_SIGN = -1` in the sketch — teacher) — note it; flyable on a tether.
- Will not lift by ~90 % of the slider: too heavy today (battery voltage, prop slip) — back to the M11 numbers, never to more throttle.
- The phone shows DRONE-xx joined but the page will not load: forget other DRONE-xx networks, mobile data off, re-join, reload (the M10 Stuck line — more frequent at the line, because every battery is a fresh join). The network shows "full": a third phone got in first — at most two clients; find it, disconnect it, re-join.
- The banner turns green (ARMED) by itself, or the pilot's phone shows *מסך צפייה - DISARM בלבד*: another phone pressed ARM — **DISARM, say STOP**, find the phone; slider 0 on the pilot's phone, then the pilot's own ARM.
- The page disarms mid-hover and the drone drops: the phone screen slept or the page went to the background — the 600 ms watchdog. A 20 cm drop is fine; keep the page in front and the screen awake; slider at 0, re-ARM.
- The student freezes or spikes: the teacher says "slider down, DISARM" once, calmly, and if the student does not move, the teacher's phone (joined to the same network, page open) presses DISARM — **a DISARM from the teacher's phone latches the drone down until the battery is pulled**, so it cannot be re-armed by a thumb on the pilot's phone while the teacher walks in. The teacher still says "phone down" once and, if there is no response, takes the phone from the student's hand before walking in (the latch is the first layer, the phone is the second). Then the medical-alert protocol. The flight is tried again another session; nothing is said about it at the close-out circle except what the student wants said.

*[Verification: §5.6 — tethered first flight mandatory; one at a time; medical-alert protocol. Principle 8 — the teacher beside the student for the whole slot. Principle 5 — the student decides when to lift and when to land.]*

---

### Milestone 14 — Post-flight ritual and celebration

**Goal.** The drone made safe in the right order, the battery back in the bag, the flight logged — and the moment marked.

**Steps.**
1. Page shows **DISARMED**, slider at 0. **The pilot's phone leaves the pilot's hands** — into the teacher's hand or face-down on the floor behind the line. Only then the teacher enters the circle and **unplugs the battery** (the student may do it with the teacher beside them). *Phone down, battery first: a phone in a hand is a drone that can wake up; a drone without a battery cannot arm.*
2. **Props off** — all four — into the teacher's box, before the drone leaves the circle. Unhitch the tether from the frame loop.
3. Back of a finger: motors, MOSFETs, MT3608 — warm is fine, hot is a note on the card for the teacher.
4. Battery to the teacher: meter reading written on the card's flight log (before / after), then into the **STORAGE bag** (≥ 3.5 V) or, below 3.5 V, a 15-minute top-up in the CHARGING bag as the last act of the session — never while another drone is live (LiPo section).
5. Flight log line: date, AUW, hover point and T/W, battery before/after, motor time from the page's counter, hovers flown, one sentence from the student ("what it felt like" / "what I'd change").
6. Celebrate: a photo of the student with their drone (permission), the tracking-sheet row, and the question for the next session: *"Tier 2, a second flight, or an extension from the Tier 3 list?"*

**Expected result.** A safe drone on the bench, a battery in the bag, a logged flight.

**Done when.** Battery in the bag, props in the box, log written, photo (optional) taken — and the teacher has said the sentence: *"You built a thing that flies. Nobody gave you that; you made it."*

**Stuck.**
- Nothing technical can go wrong here. The only failure is skipping the order: **DISARM → phone down → battery out → props off.** The card prints the words in that order, large, beside the ON order **props → battery → ARM**.

*[Verification: Principle 4 — the closing visible win; Principle 8 — the celebration is the relational close-out; §5.6 battery discipline.]*

---
## Tier 2 — Guided Design (17 milestones with four choice points)

**Who this tier is for.** Students who completed Tier 1 of Project 8 (a second pass with their own hands on the soldering iron and the tuning constants) or who arrive from a Tier 2 completion on Projects 6 or 7 and want the full build. Tier 2 is the **full assembly** of §6.12: the student builds the MOSFET board channel by channel, tunes the MT3608 with a multimeter, does all the wiring and all the tests, and makes four real decisions — PID starting values, the tether/zone option (standing in for the prop-guard choice while guards are pending), the throttle ceiling and identity, and the flight-test sequence.

**Claude Code usage at Tier 2.** Level 1 for `00_motor_test.ino`; **Level 2** at T2·M14 on `T2_flight_starter.ino` (the `==== CHANGE THIS ====` blocks, P5/P7 convention) with the (a)(b)(c) discipline; Channel B throughout; not at the soldering station or the flight line.

**Where Tier 2 differs from Tier 1, in one line each.** The student solders the board (T2·M3–M5) and tunes the MT3608 (T2·M6) instead of receiving them; the teacher still solders the battery pigtail; every test is the student's own; the flight sketch is the student's edited starter, not the stock file.

### Tier 2 Milestone 1 — Start-up, contract, parts, identify everything

As T1·M1 (folder ritual, contract signed, parts named, empty-frame weight) **plus** the bare perfboard and the loose channel parts in the tray: the student sorts them into four channel piles (1 MOSFET, 1 diode, 1× 100 Ω, 1× 10 kΩ each) plus the capacitor, and reads every resistor with the meter (100 Ω brown-black-brown; 10 kΩ brown-black-orange). **Done when** the contract is signed, four piles are sorted and meter-verified, and the card's parts list is ticked.

### Tier 2 Milestone 2 — Press-fit the motors

Exactly T1·M2. **Done when** F/B carry CW motors, R/L carry CCW motors, all seated, all spinning free.

### Tier 2 Milestone 3 — Solder channel 1 (together-milestone at the soldering station)

**Goal.** One complete MOSFET channel on the perfboard, built in the order that makes checking easy.

**Steps.** (1) Goggles; the P4 four rules said aloud; iron on. (2) Lay the **BAT+ rail** and the **GND rail** first: two bare copper wires across the board, soldered at every third hole. (3) **Q1**: label toward the gate-pad side, legs **G-D-S**, one leg tacked, straightened, then the other two, ≤ 3 s per leg; clip the legs. **Leave ≥ 2 holes** for Q2. (4) **D1** between M1+ (on the BAT+ rail) and M1− (the Drain leg): **band toward BAT+**. (5) **100 Ω** from the G1 pad to the Gate leg; **10 kΩ** from the Gate leg to the GND rail; Source leg bent onto the GND rail and soldered. (6) Mark "M1 / G1 / FRONT" beside the pads with a marker.

**Done when** the channel matches card R2 picture-for-picture, the teacher has looked at the diode band and the G-D-S order, and every joint passes a gentle tug.

**Stuck.** Diode band the wrong way — desolder, flip (the teacher does the desoldering). Legs bridged with solder — wick or a clean reflow. A leg pulled out of the plastic — spare MOSFET.

### Tier 2 Milestone 4 — Multimeter-check channel 1

T1·M3's procedure on one channel, done by the student: BAT+↔GND no beep; G1↔GND ≈ 10 kΩ; M1−↔GND OL; tab↔GND no beep; tab↔BAT+ no beep; **diode test mode**: red probe on M1− (anode side), black on BAT+ → ~0.2–0.35 V; reversed → OL. **Done when** the five readings are on the card and none is wrong. *Channel 1 is checked before channel 2 exists, so a mistake is found once, not four times.*

### Tier 2 Milestone 5 — Solder channels 2–4, the capacitor, and check everything

Repeat T2·M3 for Q2/D2 (M2, RIGHT), Q3/D3 (M3, BACK), Q4/D4 (M4, LEFT), **≥ 2 empty holes between MOSFETs**; then the **220 µF** across the rails (long leg → BAT+, stripe → GND); then the two extra **BAT+ / GND pads for the MT3608**. The teacher solders the **PH2.0 pigtail** (the full-current joint). Full T1·M3 meter check on all four channels **plus tab-to-tab for all six pairs**. **Done when** every reading is on the card, no beep where there must be none, and the four gate readings are 9–11 kΩ. *Typically one full session plus a bit.*

### Tier 2 Milestone 6 — Tune the MT3608 to 5.0 V with the multimeter (together-milestone)

**Steps.** (1) The MT3608 on the bench, **not connected to the DevKit**; meter on DC V on OUT+/OUT−. (2) The teacher connects a battery to IN+/IN− through the test leads. (3) Read the output. Fresh modules show ≈ battery voltage; turn the pot **counter-clockwise** 10–15 full turns until the reading starts to climb, then slowly to **5.00 V (4.95–5.05)**. If the first reading is already high (10–20 V) — keep turning CCW until it drops. (4) Battery off, on again: still 5.0 V. (5) A drop of nail polish on the pot; "5.0 V ✓ + today's date" on the module. (6) The teacher reads it once more before it goes on the frame.

**Done when** the module reads 4.95–5.05 V on two power-ups and is locked and marked. *The card repeats the one rule in red: the DevKit never meets an unchecked MT3608.*

### Tier 2 Milestone 7 — Mount the electronics (MPU flat, arrow forward)

T1·M4 exactly, including the teacher's check of the MPU's arrow. **Done when** the teacher signs the "arrow → FRONT, board flat" line.

### Tier 2 Milestone 8 — Power-tree wiring

T1·M5 with the student soldering every joint. **Done when** the six lines are ticked and polarity is eyeballed at both ends.

### Tier 2 Milestone 9 — Motor wiring to the four channels

T1·M6. **Done when** four windings read through their pads and no channel cross-beeps.

### Tier 2 Milestone 10 — Signal wiring (gates + I2C)

T1·M7. **Done when** the 22-line list is ticked and the four gates read ~10 k from the DevKit pins.

### Tier 2 Milestone 11 — Multimeter pre-power check and first power-up

T1·M8, teacher beside. **Done when** no-beep checks pass, LED on, no motor motion, VIN 4.9–5.1 V, MPU 3.2–3.4 V, nothing hot, battery back with the teacher.

### Tier 2 Milestone 12 — Toolchain, motor-test upload, spin without props

T1·M9 + T1·M10 on one card (a Tier 2 student has done ESP32 uploads on P5/P6/P7). **Done when** each motor answers its own button, all four follow the slider, DISARM pressed, battery returned.

### Tier 2 Milestone 13 — Props on, bench thrust test, weigh, compute the gate

T1·M11 exactly — the inverted post, the same three readings — with the student doing the arithmetic on the card: AUW, the scale reading at **slider 60 / 80 / 100 %** (the same three points as T1·M11; the slider-to-duty conversion lives once, in the Hardware section), the **hover point** (the slider % at which the reading first passed the AUW), and **T/W** = reading at 100 % ÷ AUW, written as a number. **Done when** the hover point and the ratio are written, the per-motor direction check is clean (positive = lifting), and the card carries the teacher's decision line from the Hardware section's gate: **≤ 75 % → "fly" (tethered)** / **75–85 % → "tethered only, ≤ 30 cm, weight ladder"** / **above 85 % or never → "weight ladder first, no flight this session"**. Props off, battery back.

### Tier 2 Milestone 14 — The choice points and the Claude Code Level 2 edit (props off, USB in)

**Goal.** Turn `T2_flight_starter.ino` into the student's own flight sketch by deciding four things and changing only the marked blocks.

**Choice A — PD starting set (pick one; both are reasonable):**
- **Option 1 — "Careful" (זהיר):** `KP = 1.5`, `KD = 0.10`. Softer — levels gently, may drift a little, least likely to oscillate. *Pick this if unsure, or if the bench test put the hover point above 75 % of the slider (a heavy build has less room for big corrections).*
- **Option 2 — "Balanced" (מאוזן):** `KP = 2.0`, `KD = 0.14`. The standard set — the same numbers the stock `01_flight.ino` flies with; catches tilt faster, may rock on a very light build. *Pick this if the hover point came out at or below 75 % of the slider and the build is tidy.*
- *(Units: KP in PWM counts per degree of tilt; KD in PWM counts per degree-per-second of gyro rate. These are engineering starting points, not values verified on this exact airframe — the first tethered hover is the verification, and the tuning loop at T2·M15 is the real work.)*

**Choice B — Tether length / zone (the stand-in for the prop-guard choice while guards are pending):**
- **Short tether (0.8 m), hover only:** the drone may lift and hover; no sideways intent. *Pick this for a first flight.*
- **Full tether (1.2 m), hover + small moves:** the drone may hover and drift to a target mark inside the circle. *Pick this after one clean hover session.*
- *When guards arrive, this choice becomes "guards on for every practice flight" and the tether length stays a zone decision.*

**Choice C — Identity and ceiling:** the network name is not one of the choices — it is built at boot from the teacher-set `STATION` constant (`"DRONE-" + STATION`) and that line stays as the teacher wrote it. What the student sets is `DRONE_WIFI_PASS` (**at least 8 English letters/digits**; the sketch refuses to compile with a shorter one, and the new password goes on the pilot's station card and the teacher's sheet), `DRONE_DISPLAY_NAME` (the page title, Hebrew allowed), page colours; and `MAX_THROTTLE_PERCENT` — **85 (careful) or 100 (balanced), never above 100** (the sketch refuses to compile above 100). **85 %** (duty 217) shortens the slider for a nervous pilot on a light, strong build — the hover point then sits ~17 % higher on that shorter slider; **100 %** (duty 255) is the stock setting and the one that leaves the PD controller its full 64 counts of headroom, which is what a build with a hover point near 75 % needs. The card says why: the ceiling shapes the slider, it is not a power limit — the real envelope is the slew limiter, the hover-point gate and the tether.

**Choice D is made at T2·M16** (flight-test sequence) — not here.

**The edit.** The (a)(b)(c) discipline on the card — *(a) what I want:* e.g. "soft PID, DRONE-03, title 'הרחפן של נועה', short tether"; *(b) what is currently in the starter:* the default values; *(c) what I looked at:* the four `CHANGE THIS` blocks — then the Level 2 prompt with the sketch pasted, Claude's answer, the change in the IDE (**only inside the marked blocks**), **Verify**, **Upload** (battery out, props off). Serial banner shows the new name. Comprehension check on the card: *"say in one sentence which numbers you changed and what each one does."*

**Done when** the student's starter compiles and uploads with their four choices written on the card, and they can say the one sentence.

**Stuck.** Claude proposes changes outside the blocks — the card says: only the blocks; ask Claude to restate the change as "replace line X with Y". A Hebrew display name needs nothing special — type it between the ordinary quotes exactly as the starter already does, and do **not** add a `u8` prefix (on the core 3.x package that prefix is what actually fails to compile). Hebrew belongs only in `DRONE_DISPLAY_NAME`; `STATION` stays the teacher's number and `DRONE_WIFI_PASS` stays English letters and digits. If the compile fails right after this edit, the Hebrew is not the cause: the editor draws that line right-to-left, so a pasted name easily loses a quote or the `;` — check that the line still has one `"` at each end of the name and a `;` at the end, and retype them if unsure.

### Tier 2 Milestone 15 — Tethered first hover and the tuning loop

T1·M13's flight sequence with the student's own sketch and tether choice. Then **one constant at a time, one small step, one flight**: wobbles fast / buzzes → `KP` −0.2; leans and is slow to come back → `KP` +0.2; bounces after a push, slow to settle → `KD` +0.02; feels sluggish, mushy → `KD` −0.02; slowly turns on the spot → leave `KYAW`, check the CW/CCW pairs and `YAW_SIGN`. Each change = DISARM → battery out (teacher) → props off → USB → edit → upload → props on at the line → checklist → fly. **Two or three passes is normal; fifteen minutes of tuning without a clean hover is also normal — continue next session.** **Done when** the drone hovers for ≥ 5 s without growing oscillation and the final `KP`/`KD` are written on the card.

### Tier 2 Milestone 16 — Choice D: the flight-test sequence, then fly it

Pick one (all tethered, all inside the circle, all with the R4 checklist before each battery):
- **Sequence 1 — Three hovers:** three separate 5-second hovers, land between each, one battery.
- **Sequence 2 — Hover and hold:** one hover held for 15 s, a peer counting aloud behind the line.
- **Sequence 3 — Hover to a mark:** (full tether only) lift, drift to a tape mark 50 cm away, land on it.
- *Untethered options from the master document (short untethered hover / flight to a target) are **suspended** until propeller guards are in the kit. The card carries that sentence verbatim.*

**Done when** the chosen sequence is completed once, witnessed, and logged (battery before/after, what happened).

### Tier 2 Milestone 17 — Signature flight, post-flight ritual, celebration

The student names the drone (poster line), demonstrates their sequence once more for a peer or the teacher, then T1·M14's ritual in order: **DISARM → battery out → props off → log → bag**. Photo with permission. The teacher's sentence. **Done when** the log has its line and the battery is in the bag.

*[Verification: Principle 5 — four genuine decisions whose consequences the student feels on the tether; Principle 7 — Level 2 on the starter with the (a)(b)(c) discipline; §6.12 Tier 2 choice points, with the prop-guard choice transformed into the tether/zone choice per the locked decision.]*

---

## Tier 3 — Open Design (one-page project planner)

**Who this tier is for.** Students who completed Tier 2 of Project 8 (the only sensible entry — Tier 3 extends a flying, tuned drone) or who arrive with real flight-controller experience. Tier 3 on Project 8 is genuinely advanced; §6.12 says so and this file does not soften it.

**Claude Code usage at Tier 3.** Channel A **Level 3** — free dialogue with the (a)(b)(c) discipline, the student's tuned `T2_flight_starter.ino` as the base. Every extension changes the flight sketch, so **every new upload repeats the full test ladder**: motor-test page → props-off behaviour check → bench thrust (if weight changed) → tethered hover. The planner prints the ladder.

**Deliverable.** A single-page **project planner** (`T3_project_planner_he.dc.html`) with five phases:

- **PLAN** — pick **one** extension (a second only after the first flies):
  1. **Battery monitor + low-battery auto-land** — a 100 k/100 k divider from BAT+ to GPIO 34 **with a 100 nF ceramic from the pin to GND at the DevKit** (without it the 50 kΩ source impedance and the motors' 20 kHz ripple make the reading wander); the page shows volts; below 3.5 V the sketch ramps the throttle down over 3 s and disarms. Two things to plan for: the reading **collapses under throttle** because the cell sags, so the threshold must be checked against a reading taken while armed, not idle — hence a hold time (stay below 3.5 V for ~1 s) before the auto-land fires; and the per-drone calibration comes free, from the multimeter reading the student already takes at T1·M8. *(The most useful extension for the whole room — it removes the "how long has this battery been out" guesswork.)*
  2. **Altitude hold** — a **BMP280** barometer on the same I2C bus (21/22, address 0x76); a slow P loop on pressure-altitude adds/subtracts a few PWM counts to hold height. Honest note on the card: barometric hold at 20 cm indoors is noisy; the goal is "holds within ±10 cm for 10 s".
  3. **Flight modes** — a mode button on the page: *manual* (Tier 2 behaviour), *auto-level only*, *auto-hover* (altitude hold on). Clean state machine (P5's skill).
  4. **Flight data logger** — pitch, roll, throttle, four motor values and (if fitted) battery volts, 20 times a second, streamed to the page and downloadable as CSV (no SD card needed — the ESP32 has RAM for a 60 s buffer). The student graphs a hover afterwards.
  5. **Status LED** — a WS2812 pixel (GPIO 33) beside the onboard blue one: green disarmed, red armed, blinking red low battery. Tiny code, big visibility for the teacher across the room.
  6. **Yaw from the phone** — a left/right pair on the page that biases the CW pair against the CCW pair; the drone turns on the spot on the tether.
  7. **Enhanced filter** — the stock loop already runs at 250 Hz, so this one is about the filter itself: tune the complementary filter's `ALPHA` (0.98 in the stock sketch), add a gyro low-pass, or push the loop above 250 Hz and see whether anything improves; measure the difference as "seconds of stable hover before a correction".
  Write: the use case, what changes on the page, what changes in the hardware (weight!), what the test is.
- **BUILD** — add the hardware (weigh again; re-run the thrust test if AUW changed by > 3 g). Wiring reference R1 lists the free pins (33, 34, 32, 23, 19, 18).
- **CODE** — Level 3 dialogue from the student's description with the starter pasted; Claude generates the change; the student reads it, uploads, tests on the **motor-test ladder** first.
- **TEST** — against the goal the student wrote (volts shown / height held / CSV downloaded / LED matches state). The plan may change.
- **SHOW** — a witnessed tethered flight with the extension working; log and photo.

---

## Claude Code integration — operational detail

**Channel A — Pair programmer.**

*Level 1 — pre-written sketches (Tier 1; Tier 2 for the motor test):*

- `00_motor_test.ino` — **Motor test, no sensor.** Sets the four motor pins `OUTPUT LOW` *before* the PWM is attached (LEDC 20 kHz, 8-bit; core 3.x `ledcAttach`/`ledcWrite(pin, duty)`, core 2.x calls picked automatically); boots DISARMED; **WPA2 soft-AP** named `"DRONE-" + STATION` (the teacher sets `STATION` 1–8 when copying the sketch) with `DRONE_WIFI_PASS` (8+ characters; the sketch halts with the fast LED flicker and a Serial error rather than start an open AP) and **at most two clients**; page at `192.168.4.1` with **ARM / DISARM**, one throttle slider **0–100 %** (`MAX_THROTTLE_PERCENT = 100` → `MAX_PWM = 255`) driving all four motors at the same power, and **four per-motor test buttons (FRONT / RIGHT / BACK / LEFT)** that run one motor for **2 s at a fixed ~25 % duty** and are accepted only while ARMED with the slider at 0 and no other test running (any DISARM or watchdog trip ends the run at once). **Throttle slew limiter:** the duty may rise only +2 counts per 4 ms step (~0.5 s from 0 to full) and falls instantly. ARM refused unless the slider is at 0, with the reason printed in Hebrew; **throttle is accepted only from the phone that pressed ARM**, DISARM from any phone, and a DISARM from another phone **latches** the drone until the battery is pulled. The phone sends a heartbeat every 200 ms and a **600 ms watchdog** disarms if it hears nothing from the *pilot* (page closed, phone locked, Wi-Fi dropped); the page then says so and asks for the slider to go back to 0 before a fresh ARM — it never moves the slider by itself, because putting it back on 0 is the student's act. The page also shows the drone's **network name** (`רשת: DRONE-xx` — it must match the label on the frame), the connected-phone count and the same **motor-time counter** as the flight sketch. Brownout detector **enabled**. Serial banner at 115200 with the pin map, the ceiling and the network name. Used at T1·M9–M11, T2·M12–M13.
- `01_flight.ino` — **Full flight.** Same boot-safety, same AP/page pattern plus live **ROLL / PITCH** in degrees, **yaw rate**, and the **four motor numbers**; `Wire.begin(21, 22)`; Adafruit MPU6050; **gyro calibration at boot** (the blue LED flickers fast for ~2 s — drone still and level); ARM refused unless the slider is at 0, the drone is within **20°** of level, and the sensor answers; **complementary filter** (gyro-integrated angle corrected by the accelerometer) at **250 Hz**; **PD on angle** with D from the gyro rate (`KP = 2.0`, `KD = 0.14`); **yaw-rate damping** `KYAW = 0.3` (`YAW_SIGN = ±1` for the CW/CCW pairing) on the CW pair vs the CCW pair; **plus mixer** (a square frame flown with one arm forward — the comment in the sketches says the same): `rollCorr = KP·roll + KD·rollRate` (+ when the right side is low), `pitchCorr = KP·pitch + KD·pitchRate` (+ when the nose is low), `yawCorr = KYAW·yawRate·YAW_SIGN`; the corrections ride on top of the **slew-limited** throttle (+2 counts per 4 ms up, instant down, reset to 0 on every disarm) and each motor is constrained **0–255**, with `MAX_CORRECTION` 60 counts; **auto-disarm** above **60°** of tilt (crash / tether snag), on a sensor that stops answering (the drone then refuses ARM until it is rebooted), and on the 600 ms watchdog, which counts **only the pilot's messages**. Same AP hardening as the motor-test sketch (WPA2, `"DRONE-" + STATION`, two clients, pilot-IP lock, latched DISARM) and the same **four per-motor 2 s test buttons**; while DISARMED the page shows the four motor numbers **greyed and labelled *preview — motors off*** (the mixer is computed but nothing is written to a pin), which is what the M12 logic check reads; a **motor-time counter** (since ARM and cumulative) sits beside the ARMED banner on both phones. Blue LED: fast flicker = calibrating, short blink = ready, solid = armed, endless fast flicker = MPU6050 not found or lost. Used at T1·M12–M13.
- `T2_flight_starter.ino` — `01_flight.ino` with four `==== CHANGE THIS ====` blocks at the top: **1 identity** (`STATION` — the teacher's number, from which the network name `"DRONE-" + STATION` is built — `DRONE_WIFI_PASS`, with a compile-time check that refuses fewer than 8 characters, and `DRONE_DISPLAY_NAME`), **2 stabilisation strength** (careful 1.5/0.10 · balanced 2.0/0.14 written as comments; `KP`/`KD` to fill), **3 throttle ceiling** (`MAX_THROTTLE_PERCENT` 85 or 100 — a `static_assert` refuses anything above 100), **4 page colours** (DISARM stays red whatever the student picks). Pins, `KYAW`, the slew limiter, the pilot lock, the watchdog and the tilt cut-off are below the blocks and commented "do not change".

All three sketches live in `ino_files/<name>/<name>.ino` (authored 2026-08-22 alongside this file; `ino_files/README.md` carries the upload ritual, the IDE settings, and the props-off bench checks in the sketches' own words). They target **arduino-esp32 core 3.x** and fall back to the core-2.x PWM calls automatically. They are compile-tested on the workshop machine before any card references them (the P5/P7 memory notes an API-drift risk).

*Level 2 — modify with help.* Default at T2·M14 and the T2·M15 tuning loop. The student fills in (a)(b)(c) on the card, pastes the starter, changes only the marked blocks, uploads (battery out, props off), tests on the ladder. Comprehension check: *"which numbers did you change, and what does each do?"*

*Level 3 — free dialogue.* Tier 3's extensions. A well-structured Level 3 prompt for Project 8 always includes the pin map, the statement "brushed motors on low-side MOSFETs, LEDC 20 kHz 8-bit, pins set OUTPUT LOW before attach", and the safety invariants (ceiling, watchdog, tilt cut-off) as things that must not change — the planner prints this prompt skeleton.

**Channel B — Scaffolded tutorial.** Available at any tier from M2 onward, **except** at the soldering station and the flight line (no screens there but the controller phone). Invocation: *"I'm on Project 8, Tier X, Milestone Y. Walk me through it."* The scaffold lives in `claude_code_channel_b_scaffold_he.md`. On Project 8's long sequences Channel B is especially valuable (§6.12) — and it carries the safety lines verbatim from the cards; it never improvises a safety rule.

---
## FULL FLIGHT SAFETY PROTOCOL (first-class, non-negotiable)

> **Deviation from §5.6 — propeller guards pending (2026-08-22, Yon).** §5.6 and §6.12 call propeller guards mandatory for practice flights. Guards are **not in the kit** on this date and the choice of guard has not been made, so Project 8 flies under the compensating controls written into this protocol: every practice flight **tethered** (R5), the **3 m circle** and spectator line (R4), **goggles, hair back, sleeves up for everyone in the room** (R1), **props in the teacher's boxes** and fitted only at the bench or the line, in the Safe state (R2), **one battery out of the bag at a time** (R3), and the **hover-point gate** at M11. §6.12's alternative of 55 mm props "during the learning phase" is deliberately **not** used — the thrust table has no margin to give up. **The deviation sunsets the day guards arrive:** from then on guards go on for every practice flight and the tether stays. The override table at the top of this file says the same in one row; §5.6 in the master document needs a one-line amendment to record it — that edit is Yon's, outside this file.

This section is the protocol §5.6 and §6.12 point to. It is written to be **enforced by one teacher managing 3–8 students**, which is why almost every rule is built on *custody* (the teacher physically holds the one thing that makes a drone dangerous) rather than on watching everyone at once. Every rule carries its *why*, because a rule a student understands is a rule a student keeps when the teacher's back is turned. The student-facing version (six rules, contract card R3) is in T1·M1; this is the teacher's complete version.

### The two things that can hurt, named plainly

1. **Propellers.** Four 65 mm props at up to ~40,000 RPM. They cut skin, they scratch a cornea, and a prop that leaves a shaft travels across a room. *A prop cannot hurt anyone while it is in the box on the teacher's desk.*
2. **The LiPo battery.** A 1S 1000 mAh cell that is punctured, crushed, shorted, over-charged, or charged while damaged can vent flame. *A battery cannot start a fire while it is in the fireproof bag at storage charge.*

Everything below follows from keeping those two objects in custody except for the minutes they are needed.

### Definitions the whole room uses

- **Armed** = the flight page shows the green ARMED banner (*חמוש · ARMED*) and the motors will follow the slider *right now*. An armed drone can start its motors at any moment. Armed is a software state; it only exists while a battery is plugged in.
- **Disarmed** = the page shows DISARMED; the motors will not follow the slider. Still a drone with a battery in it — still treated as "can start": DISARM is a state, not a lock. It stays down until the slider is back at 0 and a **fresh ARM press** arrives; nothing re-arms by itself. *(One exception in the other direction: a DISARM pressed from any phone other than the one that armed — the teacher's — **latches** the drone until the battery is pulled.)*
- **Safe** = **battery unplugged**. The only state in which hands touch props, wiring, or motors. **Props go on in the Safe state** — the last thing done before the battery goes in — and they come off first, right after the battery comes out. *(The one narrow exception: at M10 and M12 a prop-less live drone may be touched by a still hand on its centre plates for the bench checks — never by an arm, never near a shaft.)* **In an emergency the same definition decides who reaches in:** with **props off**, pulling the battery plug is the first move and any student may do it; with **props on**, nobody's hands go near the drone — DISARM on the phone (or say **STOP**), wait until every propeller has stopped, and only then does the **teacher** unplug it.
- **Live** = a drone with a battery plugged in, armed or not.
- **Flight circle** = the 3 m diameter tape circle. **Spectator line** = the tape line 2.5 m from the circle's centre (1 m outside the circle). **Flight line** = the spot on the spectator line where the pilot and the teacher stand.
- **Flight day** = any session in which any motor will spin with a prop fitted. Declared at the mini-huddle.

### The rules (each with its why)

**R1 — Personal protection for every person in the room whenever any motor can spin (from T1·M10 onward, and on every flight day from the first minute): goggles on, long hair tied back, sleeves pushed up, no dangling cords, lanyards or bracelets over the drone.**
*Why:* a prop fragment or a drone that yaws into a wall throws pieces in any direction; the spectator 3 m away is as exposed as the pilot. "Everyone" includes the teacher (modelling, not exception — §5.6) and any visitor; a visitor without goggles means no flying until they have a pair. Hair and sleeves are in the same rule because a bare 1 mm motor shaft is exposed at *every* props-off milestone — a spinning shaft grabs hair or a cuff before anyone feels it; the motor stalls, the hair does not come back.
*Enforced by:* the goggles count at setup (pairs ≥ people), the mini-huddle declaration, and a hair-back / sleeves-up glance before every ARM. No exceptions, no "just for a second".

**R2 — Props go on last and come off first. Props live in the teacher's two boxes (CW / CCW) and are handed out only at the bench-test station or the flight line, at item 6 of the pre-flight checklist with the battery still out; they come off before the drone leaves that spot, and always before USB, before any wiring, and before the drone goes in a tray.**
*Why:* a drone without props cannot cut anyone, whatever the firmware does; every build, upload and test milestone therefore happens prop-less. The M11 thrust test and the M13 flight are the only two places props exist.
*Enforced by:* custody of the boxes; the two four-word rituals printed on the cards (**ON: props → battery → ARM**; **OFF: DISARM → battery → props**); the teacher's eye at the two stations where props are allowed — including the M11 motor-reversal fix, the one repair that sends a props-on drone back to the workstation (props off first, always; the swap is a solder job at the M pads, not a bench job).

**R3 — One battery out of the bag at a time, handed out by the teacher, taken back by the teacher. That is the one-armed-drone rule in physical form.**
*Why:* a room with one live battery has at most one drone that can move; the teacher always knows where it is; nobody can arm a second drone behind the teacher's back because there is nothing to arm it with. The master doc's "only one student arms at any moment" is true by construction, not by supervision.
*Enforced by:* the STORAGE fireproof bag stays on the teacher's desk, zipped; batteries are labelled; the teacher's hand is the only hand that opens the bag. *The network half of the same idea:* on a flight day **every phone except the pilot's and the teacher's is in a bag** — the drone's Wi-Fi has a password, but any phone that knows the drone's name and password is a second pilot. *Exception for Tier 2/3 students with a demonstrated record:* the student may plug the battery in at the circle **with the teacher beside them** — the teacher still carried it there.

**R4 — Nobody inside the flight circle while a drone is live. Pilot and teacher walk out together before ARM; the teacher walks in only after DISARM, the pilot's "slider is zero", and the pilot's phone has left the pilot's hands — into the teacher's hand or face-down on the floor behind the line.**
*Why:* a 1.2 m tether and a 1.5 m circle radius mean the drone cannot reach anyone outside the circle; inside it, a drone that pitches over at ankle height can reach a face that bends down to look. And a phone in a hand is a drone that can wake up: DISARM is a state, not a lock, until the battery is out.
*Enforced by:* the tape; the sequence on card R4; the rule that the student may not ARM until the teacher says "clear" from the line.

**R5 — Every practice flight is tethered until propeller guards are in the kit (and when guards arrive, they go on for every practice flight — the tether stays).**
*Why:* the tether is the physical cap on where the drone can go: not over the spectator line, not into a window, not at head height. It replaces the protection the guards would give to the people in the room, not to fingers — which is why R2 and R4 still apply.
*Tether spec:* **nylon monofilament fishing line, 0.35–0.40 mm (≥ 6 kg breaking strain)**; length **1.2 m** from the anchor knot to the drone (0.8 m for the Tier 2 "short tether" choice); **girth-hitched to the frame's tether loop** — the 10 mm loop of 1 mm braided cord fitted through the bottom plate at M4, under the centre of gravity, so a taut line pulls straight down, not sideways. (The frame has no "centre ring"; the loop *is* the attachment, and reference card R1 draws it. One verb everywhere: *hitch* and *unhitch*.) The anchor is **flat, ≤ 10 cm tall, 2–3 kg** — a 2.5 kg barbell plate lying flat with the bowline through its centre hole, a flat sandbag, or the 2 L sand bottle **laid on its side** — never upright, never furniture: the drone hovers at 10–30 cm, so an upright bottle stands inside the hover band where a prop can strike it. The drone lifts off from a taped mark **~40 cm from the anchor X**, so the slack line lies flat on the floor and the drone never hovers over the anchor. The line carries a fixed bowline at each end; the teacher inspects **both** knots — the bowline at the anchor and the girth hitch at the drone — at every checklist. The card's one-liner: *"the tether is a fence, not a leash — fly low so it stays slack; if it goes tight, the drone tilts, so throttle down."*

**R6 — "STOP" is a word anyone in the room may say. When it is said: the pilot's slider goes to zero, DISARM is pressed, everyone's hands go still, and the teacher decides what happens next. The teacher's own phone is joined to the flying drone's network with the page open, as a second DISARM button — DISARM only: never ARM, never the slider on it.**
*The drone accepts throttle only from the phone that pressed ARM (any phone may DISARM), and a DISARM that arrives from any other phone latches the drone down until the battery is pulled — so the teacher may walk in without waiting for the student to let go of their phone.*
*Why:* with one teacher and eight students, the teacher cannot see every hazard; a peer who sees a tether fraying or a student entering the circle needs a sanctioned way to halt the room without arguing about it. A word that everyone may say and nobody may ignore is the cheapest emergency stop there is.
*Enforced by:* practice — the word is rehearsed once at T1·M10 (motors spinning, no props: the teacher says "STOP", the student zeros the slider and disarms); it is never used for a joke; saying it wrongly costs nothing. *Third fallback, needing no network at all:* lock the pilot's phone or switch its Wi-Fi off — the 600 ms watchdog disarms the drone within a second (a 20–30 cm drop, which this protocol already accepts).

**R7 — Pre-flight checklist (card R4) read aloud by the teacher with the student, every battery, every flight, no skipping because "we did it five minutes ago".**
The eleven items, in order:
1. Everyone in the room: **goggles on, hair back, sleeves up**.
2. The flight circle is empty; the spectator line is clear of bags and chairs; the soldering iron is off, unplugged and cold on its stand.
3. The drone is on the bench, **battery out**, props **off** — start from Safe.
4. Battery voltage on the meter: **≥ 3.8 V** (below: back to the bag; a different battery).
5. Wiring tucked, nothing inside a prop circle, MPU board flat, motors seated (push each), the battery-bay foam pad in place, the cell undented.
6. **Props on now**, battery still out — CW on FRONT/BACK, CCW on RIGHT/LEFT; tug each.
7. Tether **girth-hitched to the frame loop**, both knots inspected, the flat anchor on the X.
8. Both phones *ready* — Wi-Fi on, mobile data off, stale `DRONE-xx` profiles forgotten, screen-sleep off, browser open. They cannot join yet: the drone's network does not exist until the battery is in.
9. Drone on the **lift-off mark** (~40 cm from the anchor X), FRONT away from the line, tether slack; **battery plugged in** (teacher, or student-with-teacher per R3); **hands off** until the blue LED stops flickering (~2 s of gyro calibration); both walk out to the line.
10. At the line: **both phones join `DRONE-xx`** (password on the pilot's station card; a phone that remembers the network re-joins by itself in 10–30 s — wait at the line, do not re-enter the circle), reload `192.168.4.1`, **DISARMED** on both, slider at 0, and the page's network line (**רשת: DRONE-xx**) matches the label on the frame.
11. The teacher asks: *"Ready?"* The student answers **in words, or with the READY signal agreed with the teacher at T1·M1 and written on the contract card**. Then the teacher says *"Clear."* Only then: **ARM**, on the pilot's phone.
*Why this order:* the drone's Wi-Fi is born when the battery goes in and dies when it comes out, so the phones can only join after item 9 — every battery means a fresh join, and the wait is part of the slot. Props go on at item 6 while the drone is still Safe, before the tether and long before the battery.
*Why a spoken checklist:* §5.6 names these items; speaking them makes the student the co-owner of the procedure rather than its subject, and it is the moment the teacher reads the student's state (item 11 is the medical-alert gate). The gate keeps its full force whatever form the answer takes: silence, hesitation, a half-signal, "I don't know", or a signal the teacher has to ask for twice is a **no** for that slot.

**R8 — Flight envelope: height ≤ 30 cm for a first hover (≤ 1 m ever, indoors on the tether); one battery = one flight block (the hovers the student planned, or the T2·M16 sequence), and in any case the teacher calls "land" at 3:00 of motor time on the page's counter; the throttle ceiling is the one the sketch ships with — 100 % with the firmware slew limiter, or the Tier 2 choice of 85 % (careful) / 100 % (balanced) — and no other value is ever typed in; the pilot stands at the flight line, not closer.**
*Why:* a 30 cm drop on rubber feet breaks nothing. The motor-time limit is about the cell and the motors, not the 5 V rail (the MT3608 holds 5 V down to a ~2.5 V cell): a 1S LiPo pulled under load below ~3.5 V is a cell that puffs, and 8520 coreless motors get hot on a long run. The beginner envelope is no longer a duty cap — a cap ate the PD controller's headroom and protected no hardware — but three things that cost no headroom: the **slew limiter** (the throttle can only rise, ~0.5 s from 0 to full; down and DISARM are instant), the **hover-point gate** at M11, and the tether.
*Enforced by:* the motor-time counter on the page (the teacher's phone shows it too); the ~5-minute flight slot; and item 4 of R7, which re-meters any battery handed out a second time and sends it back to the bag below 3.8 V.

**R9 — Post-flight order, always: DISARM → phone down → battery out → props off → battery measured and bagged. Then, and only then, the drone goes back to the workstation.**
*Why:* the phone is the only thing that can still arm a live drone, so it goes face-down on the floor or into the teacher's hand before anyone crosses the tape; the battery is the arming authority, so it leaves first; the props are the injury, so they leave second; a drone on a workstation tray with a prop on it is a rule R2 violation waiting for the next session.

**R10 — Build-station rules that carry over from Projects 4–7 and apply unchanged:** never modify wiring on a live drone; USB in = battery out; a **props-off** drone with a motor turning on its own means *pull the plug first, ask second* — **with props on, nobody's hand goes near the drone: DISARM, say STOP, and wait until every prop has stopped, because the battery plug sits under the propellers**; soldering only with the teacher at the station, and the iron is off whenever the teacher is not at it (one teacher, one hazard at a time); eye protection at the bench for clipping and soldering.

### LiPo handling, charging, storage, and the fire procedure

- **Storage:** in the fireproof bag, at storage charge (**3.8 V**, 3.75–3.85), labelled, on the teacher's desk during sessions and in a locked metal cabinet between sessions. Never in a student's tray, bag, or pocket.
- **Inspection before every use (teacher, 5 seconds):** not puffy, no dents, no exposed foil, leads intact, connector clean, voltage ≥ 3.8 V. **A puffy, dented, or reverse-reading battery is retired on the spot:** red tape, into the sand bucket (on the sand, not buried), then out of the building at the end of the session to a saltwater discharge and e-waste (§5.6). It is never flown "one more time".
- **Charging:** only the teacher; only the **1S USB charger (TP4056-type, 4.20 V cutoff)**; only **inside the open fireproof bag on the ceramic tile**, on the teacher's desk, **only during a session with the teacher in the room**; never overnight, never unattended, never two batteries on one charger lead. Charge current ≤ 1 A. Unplug at the green LED. A battery that is warm to the touch while charging is unplugged and watched for 10 minutes on the tile.
- **After flight:** measure, log, bag. A battery below 3.5 V after a flight is charged before it is stored, or stored only after a partial charge to 3.8 V — a LiPo left flat is a LiPo that puffs.
- **Never:** water on a LiPo; a LiPo in a pocket with keys; a LiPo on a metal table; a LiPo plugged into anything but its drone or its charger; a LiPo with bare leads.

**Fire / venting procedure (printed on the wall by the charging tile and on card R3's back):**
1. **Say "FIRE" and "OUT"** — students leave the room by the normal route and wait in the corridor at the school's assembly point. The **head-counter named out loud at today's mini-huddle** counts heads against the attendance list on the teacher's clipboard and reports the number to the first adult who arrives — not back into the room. If the head-counter is today's pilot, is in the cool-down corner, or is absent, **the fallback named at the same huddle takes it**. The teacher does not fight a fire with students in the room. *Enforced by:* the huddle naming, the prompt on the setup checklist, and the clipboard leaving the room with the students.
2. **If the battery is in the bag:** zip it (if safe in one motion) and leave it on the tile. The bag is designed to contain a 1S cell.
3. **If the battery is in a drone on the floor:** **do not pick it up.** Pour the **sand bucket** over it — sand smothers and absorbs; the drone is lost, that is fine.
4. **Never water** — not on the battery, not on the drone (the program's §5.6 rule; water spreads burning electrolyte and shorts whatever is left).
5. **Ventilate** (the smoke is irritant); call the school's emergency number; re-enter only when the cell has stopped hissing and cooled for 15 minutes; then the remains go into the sand bucket and out of the building.
6. **Log it** (§5.8 incident line) — and debrief the students at the next session in plain words: what happened, what the bag/sand did, what did not happen because of the rules.

### Medical-alert / freeze protocol (from §5.6, operationalised)

A first flight is an adrenaline moment for every student in this population. The protocol:
- **Before:** item 10 of the checklist is the gate. A student who cannot answer "ready?" in words, or who says "I don't know", is not flown that slot — *"we'll build instead, and the drone will wait for you"*. No negotiation, no pressure, no loss of face: the card has a box "flight postponed by me" the student ticks themselves.
- **During:** if the student freezes, spikes, shakes, goes rigid, takes their hands off the phone, or loses the agreed READY/stop signal with the drone live: the teacher says, once, calmly, *"slider down — DISARM"*. If nothing happens within two seconds, the teacher presses DISARM on the teacher's phone — **that latches the drone: it cannot be re-armed until the battery is out**, so the teacher may walk in as soon as the props stop, without waiting for the phone — pulls the battery, and puts the drone down. *(For a student who flies on an agreed signal rather than on speech, silence is not by itself the trigger; the indicators are the physical ones and the loss of the agreed signal. The teacher's DISARM is the unconditional fallback in every case.)* Then the student is walked to the cool-down corner (§5.6); the teacher stays with them or hands the room to the backup task; nothing is said to the room beyond "we're done flying for now".
- **After:** the attempt is logged as a postponed flight, not a failed one. The next try is in a later session, and the student chooses whether a peer stands beside them at the line. Never push a student to complete a first flight when they are not ready — §5.6 verbatim.
- **Physical injury (a cut from a prop, a burn):** battery out of the nearest live drone first (the teacher), then first aid per the school's procedure; the incident line in §5.8; the drone in question is not flown again that day.

### Flight-zone marking (one-time, ~15 minutes)

- Choose an **indoor corner or gym corner** with ≥ 4 × 4 m free, no glass within 3 m of the circle's edge, no ceiling fixtures below 2.5 m, a non-slippery floor. Open windows closed (draughts).
- Tape a **3 m diameter circle**; mark its centre with an X; place the **anchor** on the X.
- Tape the **spectator line**: a straight line or arc **2.5 m from the centre** on the side facing the room, with a 60 cm **flight-line** box on it for pilot + teacher. Chairs for spectators behind it.
- The **bench-test station** (kitchen scale + the thrust-test post + two rubber bands) sits **outside** the circle, at a table edge away from walls (recirculating air makes the scale read low), with its own tape line 50 cm in front of it ("hands behind this line while the props turn").
- A laminated sign at the circle: the six contract rules, the STOP word, the two rituals — **ON: props → battery → ARM** and **OFF: DISARM → phone down → battery out → props off** — and the props-on line in red: *with props on you never touch the drone; only the teacher, and only after every prop has stopped.*

### What the student is told about safety (the short version on every card's footer)

*"This is the one project where the hardware can hurt you — the props and the battery. That is why the teacher holds both, why you wear goggles whenever a motor can spin, why the drone is always on a line, and why anyone can say STOP. Every other rule is the same as the last seven projects."*

---

## Teacher troubleshooting crib sheet (for the Teacher Troubleshooting artifact)

Before anything else on a drone that browned out, smoked, or blew a fuse of a battery: **put the meter on ohms, probe on a bare plate edge or a screw hole, and sweep BAT+, GND, VIN, 3V3, every M− and every G pad — all must read OL.** The carbon plates conduct like a wire, so a board that has slipped off its insulating pad (or a DevKit pin tip that has pushed through the foam) is a short that mimics half the faults below.

In rough frequency order, with the fix. Anything in the first six is "pull the battery first" — **props off**. **With props on** (M11 bench, M13 flight line) the order is **DISARM → wait until every prop has stopped → then the plug**, and only the teacher's hand: the plug sits under the propellers. A prop that keeps turning *after* DISARM is a hardware fault (items 1 and 3), not a firmware one — the drone is banded to the post or on its tether, so waiting is safe; cover it with the prop box or a folded thick cloth if it must be stopped sooner.

1. **A motor spins the moment the battery goes in.** A gate without a pull-down (G pad reads OL to GND), a gate wire on a strapping pin, or a MOSFET soldered D-G-S instead of G-D-S. Meter from the DevKit pin to GND: must read ~10 k. *Never fix on a live drone.*
2. **ESP32 LED never lights.** MT3608 wires on IN instead of OUT (or reversed); an untuned MT3608 (silver mark missing); pigtail polarity reversed at the board (check the battery plug with the meter — red must read positive).
3. **ESP32 reboots when the slider rises** (page drops, LED blinks). Missing/reversed 220 µF; long thin MT3608 input wires; a tired battery below 3.6 V; a MOSFET half-on (fake) dragging the rail. Fix the rail first, then check the MOSFET's V_DS under load.
4. **One motor never spins.** In order: gate wire on the wrong header pin (count from VIN: VIN, GND, 13, 12, **14**, **27**, **26**, **25**); cold joint at M+/M−; hair-thin lead broken at the motor; fake MOSFET (warm, V_DS > 100 mV). The per-motor buttons on the motor-test page isolate it in 10 s.
5. **A button spins the wrong motor.** Two gate wires swapped at the header — swap them back, not the sketch.
6. **A diode or MOSFET smoked.** Diode reversed (band must face BAT+) or 1N4007 instead of 1N5819; a tab touching a rail; **a bare tab, a solder spike or a DevKit pin tip touching the carbon plate — the plates conduct, so a board resting straight on one is a short**; M+ and M− swapped so the diode sits across the battery. Replace the part and re-run the T1·M3 meter check before any battery.
7. **"MPU6050 not found".** SDA/SCL swapped (21 = SDA, 22 = SCL); the GND-next-to-3V3 wire missing; the VCC wire not on 3V3 at all (on a GPIO, on GND, or pulled out of its crimp); a cold joint or a broken hair-thin wire at the MPU header; AD0 pulled high (a scanner then shows 0x69, not 0x68). An I2C scanner sketch shows 0x68 when the wiring is right. *A VCC wire that landed on VIN or 5 V is **not** the cause and has **not** damaged anything — the GY-521 carries its own 3.3 V regulator. Move it to 3V3 (the program rule: one sensor rail) and keep looking; never replace the sensor for this.*
8. **Drone flips on lift-off.** A prop on the wrong rotation (CW on a CCW arm); a motor reversed (re-run the per-motor check on the inverted rig — **a near-zero or negative reading is the backwards motor**, since a correct motor now presses the drone onto the post; swap its two leads at the M pads and re-run M6's continuity check); MPU arrow not toward FRONT; a channel on the wrong arm (M1 must be FRONT).
9. **Drone slowly yaws while hovering.** Rotation pairs wrong (FRONT/BACK must match, RIGHT/LEFT must match); the build is paired the other way round (`YAW_SIGN = -1`); one prop damaged. Flyable on the tether; fix the pairing before the next flight day.
10. **Rocks faster and faster (oscillation).** `KP` too high for this build — −0.2; if it bounces after a push and is slow to settle, `KD` +0.02. One constant per upload.
11. **Leans and never levels.** Calibrated while tilted (replug flat, hands off 3 s); MPU foam pad tilted; `KP` too low (+0.2).
12. **Will not lift by ~90 % of the slider.** Weight (re-weigh), battery < 3.8 V, a prop slipping on its shaft, a motor backwards dragging the total. The answer is never a higher ceiling.
13. **Page will not load / Wi-Fi drops.** The phone auto-switches to mobile data — turn it off; forget stale `DRONE-xx` profiles; the phone is > 10 m away; two drones broadcasting the same name — **a drone on USB broadcasts too**, so check the workstations and not only the charger desk, and check that no two stations were given the same `STATION` number. If the network shows **"full"**, a third phone joined first: at most two clients — find it, disconnect it, re-join.
14. **Watchdog keeps disarming mid-hover.** The page's 200 ms slider updates are not reaching the drone — phone sleep / screen-off, a second app in front, the phone auto-switching to mobile data. Keep the page in the foreground and the screen awake; the 600 ms watchdog is doing its job.
15. **MT3608 reads 5.0 V unloaded but the DevKit browns out.** A module with a weak inductor or a counterfeit MT3608 — swap from spares; or the IN wires are 30 AWG (must be ≥ 24).
16. **Prop will not press onto the shaft / falls off.** Wrong bore (must be 1.0 mm; 1.5 mm whoop props are the usual mistake); a bent shaft from a crash (replace the motor).
17. **Battery reads negative on the meter.** Reverse-wired PH2.0 from the supplier — red tape, retire it or re-pin it (teacher, with the pin-release tool); never "just flip the plug".
18. **Upload errors.** Same family as P5–P7: wrong board (must be DOIT ESP32 DEVKIT V1), charge-only cable, hold BOOT during "Connecting…", Serial Monitor holding the port, core < 3.x for `ledcAttach`.
19. **ARM is refused although the page shows the slider at 0.** The board is still holding an older slider value: press **DISARM once, then ARM**. The page prints the reason in Hebrew (*המחוון לא על 0* / *להניח על משטח ישר* / *החיישן לא עונה*) — read it before troubleshooting anything else.
20. **The drone will not re-ARM after the teacher pressed DISARM.** That is the latch working as designed: a DISARM from any phone other than the one that ARMed keeps the drone down until the battery is pulled. Battery out, battery in, fresh ARM from the pilot's phone.
21. **The pilot's page says "teacher view — DISARM only", or the drone pulses about five times a second and will not lift.** Throttle is accepted only from the phone that pressed ARM. If the message appears on the *pilot's* phone, another phone armed first — DISARM, say STOP, find it. If the drone pulses, the sketch on that drone is older than the pilot-lock version (two pages fighting over one slider) — re-upload the current sketch; until then, one phone only.
22. **A per-motor test button does nothing.** The page is not ARMED, the slider is not at 0, or another motor's 2-second run is still going. A button that spins the *wrong* arm is two gate wires swapped at the header (item 5) — never a sketch edit.

---

## Technical review record — 2026-08-22

*Reviewer record, not card content — the Hebrew card-generation pass skips this section. It exists so the next editor does not re-derive the numbers.*

- **Throttle ceiling and hover margin** (the one item the locked decisions asked this review to settle). At the first draft's 85 % cap (duty 217) the hover point of a ~100 g build sits at 70–90 % of the shortened slider, leaving the PD controller 22–45 of its 60 `MAX_CORRECTION` counts, and the cap protected no hardware. **Result: ceiling 100 % (`MAX_PWM = 255`) plus a firmware slew limiter of +2 counts per 4 ms (~0.5 s from 0 to full, instant down); the beginner envelope moves to the hover-point gate and the Tier 2 ceiling choice (85 % careful / 100 % balanced).**
- **IRLB8721 — verified correct, no change.** V_GS(th) 1.35–2.35 V; R_DS(on) 16 mΩ max at V_GS 4.5 V, ~20–30 mΩ typical at the ESP32's 3.3 V drive (a genuine max-threshold part 50–80 mΩ). Conduction 0.10 W at 2 A, 0.16 W at the 8520's 2.5 A stall, 0.24 W worst case; switching ~0.04–0.08 W at 20 kHz through the 100 Ω gate resistor (33 mA peak for < 1 µs, ~10 mA at the 2.3 V Miller plateau, ~0.5 µs edges). TO-220 in free air 62 K/W → +6–20 K. **No heatsink is correct; a MOSFET that gets hot is a counterfeit.**
- **1N5819 flyback — verified correct, no change.** Average diode current = motor current × (1 − duty): hover (D 0.75, 1.2 A) 0.30 A; worst realistic (D 0.5, 1.5 A) 0.75 A → 0.34 W and about +25 K in DO-41; stall (D 0.85, 2.5 A) 0.38 A; peak 2.5 A against the part's 25 A I_FSM. **1 A / 40 V is sufficient; 1N5822 (3 A) is the drop-in upgrade if a motor is ever stalled for long.**
- **10 kΩ gate pull-down — verified.** Holds the gate at ~0.6 V against GPIO 14's ~45 kΩ internal pull-up at reset; RC ≈ 11 µs.
- **MT3608 and the 5 V rail — verified.** The ESP32's 3.3 V rail draws 0.15 A average with 0.4 A Wi-Fi transmit peaks → 0.25 A average / 0.66 A peak from a 3.5 V cell, 0.77 A at 3.0 V: inside the module's 2 A rating. The AMS1117 dissipates 0.26 W average / 0.68 W peak, the same as it does on USB. Feeding the cell into the 3V3 pin would exceed the ESP32's 3.6 V absolute maximum at 4.2 V and back-drive the AMS1117 — the file's reason for the booster is correct.
- **Brownout detector — verified, stays ENABLED.** The folder's old `MotorTest_FullPower.ino` disabled it because that build ran an ESP32-C3 straight off the cell. Here the MT3608 holds 5 V down to a 2.5 V cell, so the trip never comes from motor sag, and disabling it would let a real brownout run the CPU on garbage with the gates live.
- **Pins — verified.** 25 / 26 / 14 / 27 are non-strapping (strapping = 0, 2, 5, 12, 15); the right-hand header order VIN · GND · 13 · 12 · 14 · 27 · 26 · 25 is correct; both GND pins are correct; GPIO 34 is on ADC1, the ADC that still works with Wi-Fi on.
- **PH2.0 is the weak link — a teacher item, not a card item.** ~25 mΩ contact resistance → ~0.17 V and ~1.2 W at the 7 A bursts, ~0.5 W at hover. The plug may be warm after a full-throttle bench run. **The student's two-state rule stays absolute** (*props off: hot or smelling = pull the plug, call the teacher; props on: DISARM, hands off until every prop has stopped, then call — the plug sits under the propellers*); it is the **teacher** who checks the pigtail and plug for discoloration or a loosened shell at the pre-build and after any full-throttle test, and spare PH2.0 pigtails are in the spares box.
- **Thrust rig — changed.** The upright rig of the first draft under-reads by 30–70 % (the prop wash lands on the pan). The build is tested **inverted on a post**; the geometry and the sign convention are in the Hardware section and T1·M11.
- **Weights — changed.** Motors 4 × 5 g, MT3608 2 g, MOSFET board 18 g → itemised 95 g, planning AUW ≈ 100 g (105 g with margin, 110 g worst case). The T/W table carries an AUW 110 g column so the worst case is readable off the grid.
- **Still open for Yon:** the cell size (locked decision 6 keeps 1000 mAh; rung 1 of the weight ladder states the 7–9 g cost of that choice) and the propeller guards (the dated deviation note at the top of the Safety Protocol).

---

## What this source file is not

This file is the **teacher-facing source of truth** for Project 8. It is not:

- **A student-facing document.** Students see the Hebrew task cards, the reference cards (R1 wiring, R2 MOSFET channel, R3 safety contract, R4 pre-flight checklist), the Channel B scaffold, and the three `.ino` files — all generated from this file. Students do not read this file.
- **A published curriculum artifact.** It is internal to the Agourim production process; if a student-facing artifact and this file disagree at session time, the artifact wins and this file is updated afterwards.
- **A drone-building or control-theory tutorial.** It covers only what Project 8 needs; the complementary filter and PD controller are specified to the level the sketches implement and the cards explain, no further.
- **A substitute for the two review passes.** §6.12 requires a dedicated safety-protocol review (unambiguous, enforceable by one teacher with 3–8 students, every rule with its why) and a technical-accuracy review (thrust table, BOM, wiring) **before any implementation**. **Both passes were run on 2026-08-22 and their confirmed findings are applied in this version;** the technical pass's numbers are in the *Technical review record* above. The two places where this file knowingly departs from its sources — the re-based thrust gate (hover point on an inverted rig, instead of §6.12's T/W ≥ 2.0) and the *Rotation pairs* correction — carry that pass's signature, and what is still open is listed at the end of the record.

The narrative-level specification lives in [Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §6.12 and §5.6; this file carries the operational detail (milestone IDs, pin map, power tree, channel design, sketch lineup, flight protocol) that the master document deliberately leaves out. The generated artifacts will live alongside it in `Arduino_Projects/Project_8_Tiny_Quadcopter/` (`task_cards_he/`, `reference_cards_he/`, `ino_files/`, `images/`, `teacher_materials/`) once Phase D.8 is executed.

---

*End of Arduino Project 8 — Tiny ESP32 Quadcopter source file. Version 0.2 — both review passes applied 2026-08-22; the open items are listed at the end of the Technical review record.*
