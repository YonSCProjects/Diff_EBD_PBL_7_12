# Arduino Project 4 — Line-Following Car

*The fourth project in the Agourim differentiated Arduino workshop program.*
*Source file — teacher-facing. Student-facing task cards, reference cards, Claude Code tutorial-channel scaffold, and pre-written `.ino` files are generated from this document.*

**Version 0.1 — draft for review. 2026-07-02.**

---

## What the student builds

A **line-following car**: a two-motor chassis with an Arduino Uno, an L298N motor-driver board, two infrared (IR) line sensors, and a battery pack. The car drives itself along a black-tape line on the floor: when one sensor drifts onto the line, that side's motor slows down and the car steers itself back. The student solders for the first time (motor leads and sensor leads), wires the driver board, uploads pre-written sketches, and watches their own machine drive itself.

At Tier 1 the student practices soldering on a scrap board, solders the motor and sensor leads, assembles and wires the car, uploads the drive-forward and line-following sketches, and runs the car on a straight track. At Tier 2 the student makes three design choices — forward speed, correction strength, and track shape — modifies the sketch with Claude Code's help, and builds their own tape track on the floor. At Tier 3 the student designs a complex track (turns, intersections), tunes the car for speed or reliability, and can add a start/stop button.

## Why this project is fourth

Three reasons, grounded in the program's design principles ([Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §4, §6.8):

1. **It is the first project where the student's build moves.** Projects 1–3 blinked, beeped, and sensed; Project 4 drives across the floor. This is the strongest Principle 6 (movement) project so far — the car moves and the student moves with it, laying tape, chasing the car, adjusting the track. The motivational pull of "my own robot drives itself" carries the heavier build.
2. **It introduces soldering as a first-class workshop discipline.** Wire connections under motor vibration must be permanent to be reliable, so the student solders the motor leads and the sensor leads. Soldering safety (eye protection on, hot iron on its stand, damp sponge, never touch the metal tip) is taught as a ritual at the first milestone, with the teacher present for every first joint — Principle 8's relational presence is not optional here.
3. **It introduces feedback control as an intuition, not an equation.** The line-following logic is a crude proportional controller: *"the sensor on one side sees the line → slow that side's motor."* No formal control vocabulary — just the felt experience that the car corrects itself, and that a bigger correction means sharper steering. This intuition is the conceptual bridge to every later robotics project.

## Hardware per student

All hardware is assumed to be in the Agourim workshop kit. Project 4 is the program's first big new-parts project (~$20 per student; see master doc §8). The soldering station (iron, stand, sponge, solder, eye protection) is **shared workshop equipment**, not per-student.

| Qty | Item | New / reused | Notes |
|-----|------|--------------|-------|
| 1 | Arduino Uno R3 (or compatible clone) | reused | Same board as Projects 1–3. |
| 1 | USB-A to USB-B cable | reused | For uploading; the car drives untethered on battery. |
| **1** | **Two-motor car chassis kit** | **NEW** | Frame, 2 wheels, caster wheel, screws, motor mounts. |
| **2** | **DC gear motors (TT motors)** | **NEW** | Usually included in the chassis kit. Leads are soldered at T1·M2. |
| **1** | **L298N dual H-bridge motor driver** | **NEW** | Drives both motors; takes battery power; 5V output can power the Arduino untethered. |
| **2** | **IR line-sensor modules (TCRT5000-style)** | **NEW** | Digital OUT per sensor. Mounted at the front, facing the floor. |
| **1** | **4×AA battery holder + rechargeable AAs** | **NEW** | ~5–6 V motor power, into the L298N. |
| 1 | Full-size breadboard | reused | The car's **power hub**: Arduino 5 V and GND feed the breadboard rails, and both sensors (and the common-ground wire) tap the rails. Same board as Projects 1–3, one new job. |
| ~10 | Jumper wires (M-F and M-M) | reused | Driver ↔ Arduino ↔ breadboard rails ↔ sensors. |
| 1 | Black electrical tape roll | shared | The track line on the floor. |
| 1 | Soldering station: iron + stand + damp sponge + solder + **eye protection** | shared | One station for the room; the teacher supervises every first joint. |
| 1 | Scrap practice board + scrap wire | shared | For T1·M1 soldering practice. |
| 1 | Per-student Project 4 folder on the shared Workshop Drive | new folder | Path: `G:\My Drive\Arduino_Projects\<student_nickname>\Project_4_Line_Following_Car\`. Created in the same together-ritual pattern as before. |

### Pin map (canonical for all sketches and wiring references)

Six driver pins in one contiguous block (D5–D10), two sensor pins (D11–D12) — easy to check at a glance.

| Signal | Pin | Notes |
|--------|-----|-------|
| **ENB** — right motor speed | **D5** | PWM. |
| **IN4** — right motor direction | **D6** | With IN3 sets right motor direction. |
| **IN3** — right motor direction | **D7** | |
| **IN2** — left motor direction | **D8** | With IN1 sets left motor direction. |
| **IN1** — left motor direction | **D9** | |
| **ENA** — left motor speed | **D10** | PWM. |
| **IR sensor LEFT — OUT** | **D11** | Digital read; continues Project 3's "sensors live on 11–12" pattern. |
| **IR sensor RIGHT — OUT** | **D12** | |
| Optional start/stop button (Tier 3 only) | **D2** | Program convention: the button lives on D2, 10 kΩ pull-down. |

**Motor wiring:** left motor → L298N OUT1/OUT2; right motor → OUT3/OUT4. **Power:** battery pack (+) → L298N VIN (12V terminal), battery (−) → L298N GND; **L298N GND ↔ Arduino GND (common ground — the #1 wiring pitfall)**; for untethered runs, L298N 5V output → Arduino 5V pin (onboard 5V-EN jumper in place). **The breadboard is the power hub:** Arduino 5 V → breadboard (+) rail, Arduino GND → breadboard (−) rail; both sensors take VCC from the (+) rail and GND from the (−) rail (the Uno has only one 5 V pin — the rails split it); OUT → D11 (left) / D12 (right). The L298N↔Arduino common-ground wire can also run through the (−) rail.

**Sensor polarity note (teacher-facing).** Most TCRT5000-style modules output **HIGH over black tape** (no reflection) and LOW over the bare floor. Some boards are inverted. The sketches expose this as a single constant `LINE_IS_HIGH` (default `true`); if a student's car steers *away* from the line, flip that constant — see the troubleshooting section.

## Session structure

A "session" is **one 45-minute class period** with ~30 minutes of work time ([Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §5.2). Project 4 is the biggest build so far and is designed for **three to four sessions** at Tier 1. Nothing pushes a student to finish on a schedule (Principle 5, Principle 9).

**Session 1 (typical Tier 1 arc)** — M1–M2: together-ritual + soldering practice on scrap, then soldering the motor leads. Soldering is slow on purpose; the win is *"I soldered, and my joints hold."*
**Session 2** — M3–M4: solder/attach the sensor leads, assemble the chassis, wire the L298N and the sensors.
**Session 3** — M5–M7: upload drive-forward and see the car move (the big win), sensor test over tape, upload line-following and first straight-line run.
**Session 4 (if needed)** — M8: track runs, tuning, celebration. Fast builders reach M8 in session 3.

**Tier 2 students** typically spend one session on start-up + the speed choice, one on the correction choice + Claude Code Level 2 modification, and one on track building + test-and-tune + signature run.

**Tier 3 students** spend a session on PLAN + BUILD and one or two on CODE + TEST + SHOW.

## Setup and Wait Protocol

*Prep before students enter. Pre-session time target: ≤ 15 minutes (plus one-time soldering-station setup).*

1. **Soldering station ready but OFF** until M1's safety ritual: iron on stand, damp sponge wet, solder coil, scrap board, **two pairs of eye protection** laid out visibly.
2. **Per-station parts tray:** chassis kit, 2 motors, L298N, 2 IR sensors, battery holder (batteries charged), jumpers. Do not pre-assemble; the teacher may pre-tin motor terminals for students who need a lighter first solder (per §6.8, Tier 1 latitude).
3. **Floor space:** a cleared 2–3 m strip with one straight black-tape line pre-laid for M7–M8; students lay their own tracks at Tier 2.
4. **Print one Project 4 poster per workstation** (`teacher_materials/project_4_poster_he.html`) — the student records their car's name and the tracks it completed.

The "stuck" protocol is unchanged (re-read the step → wiring reference R1 → other reference cards → call the teacher). **Soldering-specific rule: a student never troubleshoots at the soldering station alone — anything soldering-related is always "call the teacher."**

**Backup task for wait time (Project 4):** *"sketch your dream track on paper"* — quiet, tactile, previews the Tier 2 track-design choice, requires no teacher attention.

---

## Tier 1 — Guided Build (8 milestones)

**Who this tier is for.** Students who want maximum support, and any student doing Project 4 for the first time — this is the biggest build of the program so far, and Tier 1 is the clearest path through it. Eight milestones because the build is more involved (per §6.8); each is still one 15-minute-scale chunk.

**Claude Code usage at Tier 1.** Channel A Level 1 throughout — pre-written sketches, no editing. Channel B available from M2 onward, and particularly valuable here: the long build sequence feels smaller when walked through conversationally.

### Milestone 1 — Meet the soldering station (together-milestone)

**What the student does.** Sets up their Project 4 folder on the Workshop Drive (same together-ritual as every project; recognition line: *"This is your folder, this is your project, Project 4 starts now"*). Then, with the teacher beside them the whole time: puts on eye protection, learns the four safety rules (goggles on whenever the iron is on; hot iron lives on its stand; wipe the tip on the damp sponge; never touch the metal end), and practices 3–4 solder joints on the scrap board until one holds when tugged.

**Done when.** The student has made at least one solder joint on the scrap board that holds when gently tugged, and can say the four safety rules.

**Why this milestone exists.** Soldering is the program's first "real tool" moment and is intimidating for many students; the teacher's full presence (Principle 8) plus a no-stakes practice board turns fear into a win before anything that matters is soldered. Channel B is not used at M1 (the teacher is speaking).

### Milestone 2 — Solder the motor leads

**What the student does.** Solders two wires (red/black) to each motor's two terminals — four joints total, teacher nearby. Tug-tests each joint. Students who prefer a lighter first solder can work with pre-tinned terminals; the teacher decides together with the student.

**Done when.** Both motors have two soldered leads each, every joint passes a gentle tug test, and the teacher has checked them.

### Milestone 3 — Solder the sensor leads and mount everything on the chassis

**What the student does.** Prepares the two IR sensors (solders leads or attaches the M-F jumpers, per kit), then assembles the chassis: motors into their mounts, wheels on, caster on, battery holder in place, sensors mounted at the front **facing the floor**, about 1 cm above it, a few centimetres apart.

**Done when.** The chassis rolls when pushed by hand, both sensors point at the floor at the front, and nothing is loose.

### Milestone 4 — Wire the driver and the sensors

**What the student does.** Wires the electrical heart of the car: left motor → OUT1/OUT2, right motor → OUT3/OUT4; battery (+) → VIN, battery (−) → GND; **L298N GND ↔ Arduino GND (the common-ground wire — the card marks it with a warning)**; the six signal pins D5–D10 per the pin map; each sensor VCC → 5 V, GND → GND, OUT → D11 (left) / D12 (right).

**Done when.** Every wire matches the wiring reference R1 table, the common-ground wire is in place, and the teacher has confirmed the wiring. *Nothing moves yet — the sketch comes next.*

### Milestone 5 — Upload "drive forward" and watch it move

**What the student does.** **Props the car up so the wheels spin in the air** (the card says so explicitly — a car that leaps off the desk is the classic first-run surprise). Uploads `01_drive_forward.ino`. Wheels spin forward for 3 seconds, pause, repeat. Then puts the car on the floor for one real forward run.

**Done when.** Both wheels spin forward (swap a motor's two driver terminals if one spins backward — the card walks through this), and the car has driven forward on the floor.

**Why this milestone exists.** The project's biggest visible win (Principle 4 + 6): the student's own machine moves. The backward-wheel fix is deliberately part of the milestone — it is the most common assembly outcome and is a 30-second fix, not a failure.

### Milestone 6 — Test the sensors over the line

**What the student does.** Uploads `02_sensor_test.ino`, opens the Serial Monitor (9600), and holds the car over the pre-laid tape line: each sensor reads LINE over black tape and FLOOR over bare floor. The student slides the car left and right and watches the two readings flip — the same "the number changes as I move it" magic as Project 3, now with two eyes.

**Done when.** Both sensors flip between LINE and FLOOR as the car slides across the tape, matching which sensor is actually over the line.

### Milestone 7 — Upload line-following and run the straight track

**What the student does.** Uploads `03_line_follow.ino`, places the car at the start of the straight tape line (sensors straddling the line), switches on battery power, and lets go. The car follows the line, correcting itself as it drifts.

**Done when.** The car follows the full straight line start-to-finish without leaving it, at least once.

### Milestone 8 — Run your track and celebrate

**What the student does.** Runs the car on a line with a gentle curve (teacher adds a curve to the tape, or the student lays one). Names the car, writes the name and the completed track on the **Project 4 poster**, and shows a full run to the teacher. The teacher celebrates by name and photographs the car for the portfolio (with permission).

**Done when.** The car has completed a run witnessed by someone, its name is on the poster, and the teacher has celebrated.

---

## Tier 2 — Guided Design (6 milestones with three choice points)

**Who this tier is for.** Students who completed a Tier 1 project and want more control. Project 4's Tier 2 is a genuine *tuning* experience — the choices interact ("fast + sharp curve" fails; the student discovers why), and Channel A Level 2 is the default mode at the modification milestone.

**Claude Code usage at Tier 2.** Level 1 for the starter sketch; Level 2 for the speed/correction modifications; Channel B throughout.

### Tier 2 Milestone 1 — Start-up

Compressed rebuild/verify: folder, car assembled and wired (fresh build or verified carry-over from Tier 1), `T2_line_follow_starter.ino` uploaded, one clean run on the straight line. The card previews the three choices coming up (speed, correction, track). Done when the car follows the straight line from the starter sketch.

### Tier 2 Milestone 2 — Choice point A: pick your speed

Three options, written on the card: **איטי (slow)** — steady and safe on every curve; **בינוני (medium)** — the default balance; **מהיר (fast)** — exciting and risky on curves. The student writes their choice. Done when a speed is chosen and written.

### Tier 2 Milestone 3 — Choice point B: pick your correction + modify with Claude Code

Two options: **תיקון עדין (small correction)** — smooth on straights, may miss sharp curves; **תיקון חזק (strong correction)** — grips curves, wiggles on straights. Then the (א)(ב)(ג) discipline on the card, and a Level 2 session changing the two marked constants in the starter (`BASE_SPEED`, `CORRECTION`) to match both choices. Upload and test. Comprehension check: *"can you say in one sentence which numbers you changed?"* Done when the car runs with the student's chosen speed and correction and they can name the change.

### Tier 2 Milestone 4 — Design and build your track

The third choice: **ישר (straight)** / **עיקול עדין (gentle curve)** / **עיקול חד (sharp curve)** — then the student lays their own track on the floor with black tape. Corners must be curves, not right angles (the card shows why: the sensors lose a sharp corner). Done when the track is on the floor and its shape is written on the card.

### Tier 2 Milestone 5 — Test and tune

The student runs their car on their track and tunes: too slow → raise `BASE_SPEED`; flies off the curve → stronger `CORRECTION` or lower speed. Tuning is honest engineering iteration — usually two or three passes; if 15 minutes pass and it still isn't right, that's normal, continue next session. Done when the car completes the student's own track once, start to finish (a single clean run — matching every other completion bar in the program; the reliability chase belongs to Tier 3's optional reliability goal, not here).

### Tier 2 Milestone 6 — Signature run

The student names the car, writes name + track shape on the Tier 2 line of the poster, and demonstrates a full run to a peer or the teacher. Celebration block; photo with permission.

---

## Tier 3 — Open Design (one-page project planner)

**Who this tier is for.** Students who completed Tier 2 of a prior project or ask for open design. The natural draws: speed demons and track architects.

**Claude Code usage at Tier 3.** Channel A Level 3 — free dialogue with the (א)(ב)(ג) discipline.

**Deliverable.** A single-page **project planner** (`T3_project_planner.html`) with five phases:

- **PLAN** — pick a goal: a **complex track** (S-curves, a loop, an intersection — decide what the car should do at it), a **speed build** (fastest lap on a fixed track), or a **reliability build** (ten clean runs in a row). Optional: a **start/stop button** on D2 (10 kΩ pull-down, program convention). Sketch the track on paper.
- **BUILD** — lay the track; add the button if chosen (wiring reference: R1).
- **CODE** — Level 3 dialogue from the student's description (e.g., *"I want the car to stop for two seconds at the intersection and then continue straight. Here's my code: [paste]"*). Upload, test, iterate.
- **TEST** — against the goal they set (lap time / clean-run count / intersection behaviour). The plan may change.
- **SHOW** — a witnessed run; photo for the portfolio.

---

## Claude Code integration — operational detail

**Channel A — Pair programmer.**

*Level 1 — pre-written sketches:*

- `01_drive_forward.ino` — both motors forward at medium speed, 3 s on / 1 s pause, repeating. Used at T1·M5.
- `02_sensor_test.ino` — prints both IR sensors to the Serial Monitor as LINE / FLOOR. Used at T1·M6.
- `03_line_follow.ino` — the full line-follower: both-on-floor → forward; left sensor sees line → slow left motor; right sensor sees line → slow right motor; both see line → stop (end mark or lifted). Used at T1·M7–M8.
- `T2_line_follow_starter.ino` — same logic with the tuning constants at the top: `BASE_SPEED` (0–255), `CORRECTION` (how much the inner wheel slows), plus `LINE_IS_HIGH` for inverted sensor boards.

*Level 2 — modify with help.* Default at T2·M3 and the T2·M5 tuning loop. The student fills in (א)(ב)(ג) on the card, pastes the code, changes only the marked constants, uploads, tests.

*Level 3 — free dialogue.* Tier 3's custom goals; intersection behaviour is a genuinely interesting Level 3 problem.

**Channel B — Scaffolded tutorial.** Available at any tier from M2 onward. Invocation: *"אני בפרויקט 4, גרסה X, שלב Y. תעבור איתי על זה."* Scaffold lives in `claude_code_channel_b_scaffold_he.md`. Channel B is especially valuable in Project 4 (per §6.8): the long build reads smaller in conversation.

---

## Safety notes (Project 4 specific — first escalation of the program)

Projects 1–3 had a near-zero safety envelope. Project 4 adds two real (still small) risks, handled as first-class discipline:

1. **The soldering iron (≈350 °C).** The four rules, taught at M1 and enforced always: **eye protection on** whenever an iron is on at the station; the **iron lives on its stand** when not in the hand; clean the tip on the **damp sponge**, never fingers; **never touch the metal end** — it stays hot minutes after unplugging. A student never solders without the teacher at the station. Small burns are the realistic risk; the ritual makes them rare, and the sink is the first response for any touch.
2. **Motors and moving parts.** Fingers away from spinning wheels; prop the car up during bench tests; carry the car with the power switch off.
3. **Battery pack.** Rechargeable AAs are low-risk; never short the pack's leads; power off when not driving.

**What the student is told:** *"the electronics are still 5-volt safe, exactly like the last three projects. The two new things that deserve respect are the hot iron and the spinning wheels — the safety rules are on card R4, and for soldering the teacher is always with you."*

---

## Teacher troubleshooting crib sheet (for the Teacher Troubleshooting artifact)

1. **Nothing moves after upload.** Usual causes: battery switch off / batteries dead; or **no common ground** between L298N and Arduino. Fix: switch on, then check the GND↔GND jumper — the single most common Project 4 wiring miss.
2. **One wheel spins backward.** Normal assembly outcome, not a fault: swap that motor's two wires at the L298N output terminals (OUT1↔OUT2 or OUT3↔OUT4). The M5 card walks the student through it.
3. **Motors hum but the car doesn't move.** Low battery, or `BASE_SPEED` too low for carpet — raise it; run on smooth floor.
4. **The car steers *away* from the line.** The sensor board's polarity is inverted: flip `LINE_IS_HIGH` in the sketch (or the left/right sensor wires are swapped — check D11=left, D12=right).
5. **A sensor never changes its reading.** Height problem (must be ~1 cm above the floor), sunlight flooding the sensor (shade the track), or the sensor's onboard potentiometer needs a small turn. Verify with `02_sensor_test.ino`.
6. **The car wiggles violently on the straight.** `CORRECTION` too strong or speed too high — the Tier 2 tuning conversation, one constant at a time.
7. **The car loses sharp corners.** Physics, not failure: at high speed the sensors pass the line before the car can turn. Slow down, or make the corner a wider curve. (This is the speed-vs-track interaction Tier 2 is designed around.)
8. **A solder joint breaks mid-session.** Expected occasionally under vibration; back to the station, teacher present, re-flow the joint. Frame it as maintenance, not failure — real robots need maintenance.
9. **Upload errors.** Same as Projects 1–3 (COM port, busy Serial Monitor). One Project 4 twist: **unplug USB before untethered battery runs; never both power paths at once with the 5V jumper set** — the card sequences this.

---

## What this source file is not

This file is the **teacher-facing source of truth** for Project 4. It is not a student-facing document, not a published curriculum artifact, and not a soldering or motor-control tutorial. It covers only what Project 4 needs. If any content here conflicts with what a student sees at session time, the student-facing artifact wins and this source file is updated afterwards.

The narrative-level specification lives in [Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §6.8; this file carries the operational detail (milestone IDs, pin map, sketch lineup, safety ritual) that §6.8 deliberately leaves out.

---

*End of Arduino Project 4 — Line-Following Car source file. Ready for review.*
