# Arduino Project 3 — Don't Get Too Close

*The third project in the Agourim differentiated Arduino workshop program.*
*Source file — teacher-facing. Student-facing task cards, reference cards, HTML tutorial, Claude Code tutorial-channel scaffold, and pre-written `.ino` files are generated from this document.*

**Version 0.1 — draft for review. 2026-06-30.**

---

## What the student builds

A **proximity alarm** on a breadboard with an Arduino Uno, an HC-SR04 ultrasonic distance sensor, one LED, and a piezo buzzer. The Arduino measures how far away the nearest object is, many times per second. When something comes closer than a chosen threshold distance, the Arduino sounds the alarm — lighting the LED, beeping the buzzer, or both.

At Tier 1 the student wires the sensor, uploads three pre-written sketches in turn (read distance → add a warning light → add the buzzer), and tests the finished alarm on real objects. At Tier 2 the student makes design choices — how close is "too close," and what the alarm does about it — and modifies the sketch with Claude Code's help. At Tier 3 the student designs a proximity alarm for a real use case they pick themselves (a desk-drawer alarm, a doorway alert, a pet-food-dish signal, or something they invent).

## Why this project is third

Three reasons, grounded in the program's design principles ([Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §4, §6.7):

1. **It reuses Projects 1–2's hardware skills and adds exactly one new component.** The alarm circuit is the LED + buzzer the student already knows from Projects 1 and 2, plus one genuinely new part: the HC-SR04 ultrasonic sensor. A student who completed Project 2 already knows how to wire an LED with a current-limiting resistor and drive a buzzer from a pin with `tone()`. The only new hardware is the four-pin sensor, wired in the first milestone. This keeps the hardware-learning load low so the project's real new content — **reading a sensor** and **threshold logic** — can be the focus.
2. **It is the first project where the code reacts continuously to the physical world.** Projects 1 and 2 were mostly event-driven (a button press starts something). Project 3's sketch runs in a loop that measures distance over and over and decides, every cycle, whether to sound the alarm. This is the student's first encounter with a sensor reading (`pulseIn()` timing the echo), with **threshold logic** (*"if the distance is less than 20 cm, sound the alarm"*), and with a program that is always watching, not just waiting for one event.
3. **It is the first project where the student sees a sensor "fail gracefully."** Sometimes the HC-SR04 returns a very large or jumpy number when there is nothing in front of it, or when the surface is soft or angled. The navigation cards address this explicitly as *"this is normal, not a bug"* — an honest, low-stakes first lesson that real sensors are imperfect, taught in a context where a weird reading costs nothing.

## Hardware per student

All hardware is assumed to be in the Agourim workshop kit. Project 3 reuses Projects 1–2's LED + buzzer and adds one new component (the HC-SR04 ultrasonic sensor). A second LED is needed only for the Tier 3 two-stage-alarm variant.

| Qty | Item | New / reused | Notes |
|-----|------|--------------|-------|
| 1 | Arduino Uno R3 (or compatible clone) | reused | Same board as Projects 1–2. |
| 1 | USB-A to USB-B cable | reused | For connecting to the Windows 11 workshop PC. |
| 1 | Full-size breadboard | reused | Same breadboard layout discipline as before. |
| **1** | **HC-SR04 ultrasonic distance sensor** | **NEW** | Four pins: VCC, Trig, Echo, GND. Runs on 5 V. The one new component of Project 3. ~$2. |
| 1 | 5 mm through-hole LED | reused | The alarm light. Any colour; red recommended for "alarm". |
| 1 | 220 Ω current-limiting resistor | reused | Colour-code: red-red-brown. For the LED. |
| 1 | Piezo buzzer (small, passive) | reused | The alarm sound. Reused from Project 2. Driven from a pin with `tone()`. |
| 2 | Extra 5 mm LED + 220 Ω resistor (Tier 3 two-stage alarm only) | reused / add-on | A second "getting close" warning LED (e.g. yellow) before the main red alarm. |
| ~8 | Jumper wires (M-M assortment) | reused | The sensor needs four of its own; budget a few extra. |
| 1 | Workshop PC (Windows 11) with Arduino IDE + Google Drive for Desktop | reused | Same setup as Projects 1–2. See Teacher Setup Checklist. |
| 1 | Per-student Project 3 folder on the shared Workshop Drive | new folder | Path: `G:\My Drive\Arduino_Projects\<student_nickname>\Project_3_Dont_Get_Too_Close\`. Created in the same together-ritual pattern as before. |

**Incremental cost vs. Project 2:** ~$2 per student (the HC-SR04 sensor). For 8 students, ~$16. Everything else is reused from the Projects 1–2 kit.

### Pin map (canonical for all sketches and wiring diagrams)

| Signal | Pin | Used at | Notes |
|--------|-----|---------|-------|
| HC-SR04 **Trig** (trigger output) | **D12** | T1·M1 onward | Arduino sends a short pulse out to start a measurement. |
| HC-SR04 **Echo** (echo input) | **D11** | T1·M1 onward | Arduino times how long the echo takes to come back. |
| HC-SR04 **VCC** | **5V** | T1·M1 onward | The sensor runs on 5 V, same as the board. |
| HC-SR04 **GND** | **GND** | T1·M1 onward | Common ground with the Arduino. |
| Alarm LED | **D9** | T1·M3 onward | Reuses the pin-9 LED convention from Projects 1–2. Through a 220 Ω resistor. |
| Buzzer | **D8** | T1·M4 onward | Driven with `tone()`. Reuses Project 2's pin-8 buzzer convention. |
| Second "warning" LED (Tier 3 two-stage only) | **D10** | T3 only | A yellow "getting close" LED that lights before the red alarm. Through its own 220 Ω resistor. |

**Why Trig/Echo are on D12/D11.** Pins D9 and D8 are already spoken for by the LED and buzzer (carried over from Projects 1–2 so the student's mental model stays stable). The sensor's two signal pins take the next free pair, D12 and D11, kept adjacent so the wiring reference reads cleanly. Neither needs PWM. D13 is deliberately avoided for Echo because the on-board LED tied to D13 can disturb a digital input.

## Session structure

A "session" at Agourim School is **one 45-minute class period**, of which approximately **30 minutes are actual work time** (see [Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §5.2). Project 3 is designed to fit **two 45-minute sessions** for a Tier 1 student working at a steady pace, with a third session available for students who want more time. As always, nothing pushes a student to finish on a schedule (Principle 5, Principle 9).

**Session 1 typical arc for a Tier 1 student** — Milestones 1 through 3. *Work Block 1:* set up the Project 3 folder and wire the HC-SR04 sensor (M1). *Work Block 2:* upload the distance sketch and watch the number change as a hand moves toward the sensor (M2), then add the LED and upload the "light up when close" sketch (M3). A Tier 1 student at the end of Session 1 can see a live distance reading and has a warning light that responds to their hand.

**Session 2 typical arc for a Tier 1 student** — Milestones 4 through 6. *Work Block 1:* add the buzzer and upload the full alarm sketch (M4). *Work Block 2:* test the alarm on real objects to find where it triggers (M5), then show it and celebrate (M6).

**Tier 2 students** typically spend Session 1 on Tier 2 Milestones 1–2 (start-up + threshold choice) and Session 2 on Milestones 3–5 (response choice + Claude Code Level 2 modification, test-and-tune, signature alarm). The Level 2 modification at Milestone 3 is the make-or-break step; the teacher rotates to it.

**Tier 3 students** spend Session 1 on the planning phase (PLAN + BUILD) and Session 2 on coding and testing (CODE + TEST + SHOW). Tier 3 at Project 3 is a natural draw for students who want their alarm to *do a real job* — guard a drawer, a doorway, a snack.

## Setup and Wait Protocol

*Prep before the students enter the room. Pre-session time target: ≤ 15 minutes.* The Project 3 setup is the Project 1–2 setup (see [Arduino_Project_1.md](../Project_1_Light_Signals/Arduino_Project_1.md)) with three differences:

1. **Add one HC-SR04 sensor to each parts tray** (but not pre-wired). The student wires its four pins from scratch at Milestone 1.
2. **Lay out one LED + 220 Ω resistor + one piezo buzzer** per station — the Project 1–2 alarm hardware. Do not pre-wire.
3. **Print one Project 3 poster per workstation** (`teacher_materials/project_3_poster_he.html`) and tape it where the student can write what their alarm guards at Milestone 6.

The "stuck" protocol is the same on every navigation card (re-read the step → check the wiring reference R1 → check the other reference cards → call the teacher). The Principle 8 direct-call convention from Projects 1–2 carries over unchanged.

**Backup task for wait time (Project 3):** *"sort the jumper wires by length, then by colour."* Quiet, tactile, requires no teacher attention, and tidies the station the sensor build will draw from. (Project 1 used resistor-sorting; each project improvises its own per the cross-project rule.)

---

## Tier 1 — Guided Build (6 milestones)

**Who this tier is for.** Students who want maximum support, and any student doing Project 3 for the first time who wants the clearest path. The tier is per-project — a student can have been Tier 2 on Project 2 and still choose Tier 1 here because the sensor and the idea of a threshold are new.

**Claude Code usage at Tier 1.** Channel A Level 1 throughout — every code milestone uploads a pre-written sketch, no editing. Channel B (conversational walk-through) is available but not required.

**Task card count.** Six milestones, six physical navigation cards. Each card has 3–5 checkboxes, a "done when" criterion, and the standard "stuck" protocol.

### Milestone 1 — Wire the HC-SR04 sensor

**What the student does.** Sets up their Project 3 folder on the Workshop Drive (the same together-ritual as every project's Milestone 1, abbreviated for a returning student). Then wires the four pins of the HC-SR04 sensor: **VCC → 5 V**, **GND → GND**, **Trig → pin 12**, **Echo → pin 11**. The sensor pushes into the breadboard so its two "eyes" face outward over the edge of the board, where a hand can move in front of them.

**Done when.** All four sensor pins are wired (VCC, GND, Trig→12, Echo→11) and the teacher has confirmed the wiring. *Nothing reads or beeps yet — the sketch comes at Milestone 2.*

**Why this milestone exists.** The single new-hardware milestone of Project 3, deliberately isolated so the student adds one component and confirms it before any code. It is also the together-milestone: the teacher stands beside the student for the folder-creation ritual, the first sensor plug-in, and the recognition line *"This is your folder, this is your project, Project 3 starts now."*

**Wiring reference.** Circuit 1 on reference card R1 (`w_p3_01_hcsr04`).

**Common stuck moment (teacher-facing).** The four pins are easy to swap. The most common errors are Trig and Echo reversed, or VCC and GND reversed. The reference card labels all four. Reversing VCC/GND will not damage a modern HC-SR04 for the few seconds it takes to notice, but the reading will fail — check the labels.

**Channel B note.** Channel B is NOT recommended at Milestone 1 (the teacher is present and speaking); it becomes available from Milestone 2 onward.

### Milestone 2 — Upload the distance sketch and watch the number change

**What the student does.** Opens the pre-written sketch `01_distance_to_serial.ino` from the project folder and clicks Upload. No code changes. The sketch measures the distance to the nearest object many times a second and prints it, in centimetres, to the **Serial Monitor**. The student opens the Serial Monitor (the magnifying-glass icon) and moves a hand slowly toward and away from the sensor, watching the number get smaller and larger.

**Done when.** The sketch uploads with a green "Done uploading" message, the Serial Monitor shows a distance in centimetres, and the number gets smaller as the student's hand gets closer.

**Why this milestone exists.** The visible win (Principle 4) and the physical-first moment (Principle 3): *the number changes as I move my hand* is engaging all by itself, before any alarm logic exists. It is also the first sensor reading the student has ever seen on screen.

**The "weird number" note (on the card).** Sometimes, with nothing in front of the sensor or a soft/angled surface, the number jumps to something very large or flickers. The card says plainly: **this is normal, not a bug.** The sensor hears no echo and reports "far away." Real sensors are not perfect, and that is fine.

**Sketch.** `01_distance_to_serial.ino` (Tier 1, output = Serial Monitor only). See R5.

### Milestone 3 — Add the LED and upload the "light up when close" sketch

**What the student does.** Wires one LED on **pin 9** through a 220 Ω resistor (long leg → resistor → pin 9, short leg → GND) — the same LED wiring as Projects 1–2. Then opens `02_distance_led_alarm.ino` and uploads it. This sketch does everything Milestone 2's did, plus: when the distance drops below **20 cm**, the LED turns on; when the object moves away, the LED turns off.

**Done when.** The LED is wired on pin 9 through its resistor, the sketch uploads, and the LED lights up when a hand comes within about 20 cm of the sensor and goes dark when the hand moves back.

**Why this milestone exists.** The first **threshold** the student sees in action: a number from the world crossing a line turns an output on. The LED is added and the threshold behaviour appears in one milestone because both pieces are already familiar (LED wiring from Project 1, the distance reading from Milestone 2) — the only new idea is the *if distance < 20 then light*.

**Wiring reference.** Circuit 2 on reference card R1 (`w_p3_02_hcsr04_led`).

**Sketch.** `02_distance_led_alarm.ino` (Tier 1, LED alarm at 20 cm). See R5.

### Milestone 4 — Add the buzzer and upload the full alarm sketch

**What the student does.** Wires the piezo buzzer (reused from Project 2): one leg to **pin 8**, the other leg to **GND**. Then opens `03_distance_full_alarm.ino` and uploads it. This sketch does everything Milestone 3's did, plus: when the distance drops below 20 cm, the buzzer beeps along with the LED. The student now has a complete proximity alarm — light *and* sound.

**Done when.** The buzzer is wired (pin 8 + GND), the sketch uploads, and bringing a hand within 20 cm now lights the LED *and* sounds the buzzer; both stop when the hand moves away.

**Why this milestone exists.** The payoff milestone — the alarm is now multi-sensory. The buzzer wiring is a one-minute recap of Project 2 (no new skill), so the milestone's weight is on *seeing the finished alarm work*, not on learning new hardware.

**Wiring reference.** Circuit 3 on reference card R1 (`w_p3_03_hcsr04_led_buzzer`).

**Common stuck moment (teacher-facing).** Same buzzer pitfalls as Project 2 — both legs in the same column (shorting it), or a leg to 5 V instead of pin 8. Drive the buzzer from pin 8, never straight from 5 V. See R4.

**Sketch.** `03_distance_full_alarm.ino` (Tier 1, LED + buzzer alarm at 20 cm). See R5.

### Milestone 5 — Test your alarm on real objects

**What the student does.** Tries the finished alarm against real things: a hand, a book sliding toward it, a wall as they carry the breadboard closer, a water bottle. The student notices roughly where the alarm starts (around 20 cm) and where it stops, and finds out which surfaces the sensor reads well (flat, hard, facing it) and which it reads poorly (soft, angled, fuzzy).

**Done when.** The student has triggered the alarm with at least two different real objects and can point to roughly how close an object has to be before the alarm goes off.

**Why this milestone exists.** Principle 6 movement (the student moves objects and themselves to test) and a grounded encounter with the sensor's real behaviour — the "fails gracefully" lesson made concrete. It also sets up the Tier 2/Tier 3 question *"is 20 cm the right distance for what I want to guard?"*

**Channel B note.** Channel B can answer "why does my sweater not set it off but my hand does?" conversationally — a curious student's first contact with how ultrasonic sensing works.

### Milestone 6 — Show your alarm and celebrate

**What the student does.** Decides what their alarm could *guard* — a pencil case, a corner of the desk, a doorway — and writes it on the **Project 3 poster** taped at their workstation (a row per student nickname, a column for "what my alarm guards"). Then shows the working alarm to the teacher, who celebrates by name and, with permission, photographs it for the portfolio.

**Done when.** The student has written what their alarm guards on the workstation poster and shown the working alarm to someone. The teacher celebrates and asks what they want to build next.

**Why this milestone exists.** The closing celebration and artifact milestone (Principle 4 + Principle 8). Naming what the alarm guards turns an abstract circuit into *the student's own thing that does a job* — the bridge to Tier 3's real-use-case design and a small rehearsal of it.

**Poster artifact.** `teacher_materials/project_3_poster.html` (+ `_he`). Printable; the teacher prints one per workstation.

---

## Tier 2 — Guided Design (5 milestones with two choice points)

**Who this tier is for.** Students who completed a Tier 1 project and want more control, or who arrived with some prior experience. Project 3's Tier 2 is where the student decides *how close is too close* and *what the alarm does about it*, then changes the code to match — Channel A Level 2 is the default interaction mode at Milestone 3.

**Claude Code usage at Tier 2.** Channel A Level 1 for the starter sketch; Channel A Level 2 for the modification at Milestone 3. Channel B available throughout.

**Task card count.** Five milestones (M1–M5). Unlike Project 2, there is **no conditional wiring card** — all hardware (sensor + LED + buzzer) is wired up front at Milestone 1, so the response-mode choice at Milestone 3 is a *code* choice, not a wiring choice. A single student's path is always five cards.

### Tier 2 Milestone 1 — Start-up

**What the student does.** Compressed version of Tier 1 Milestones 1–4: set up the folder, wire the HC-SR04 sensor (Trig 12, Echo 11, VCC 5 V, GND), wire the LED on pin 9 and the buzzer on pin 8, then upload the starter sketch `T2_alarm_starter.ino` and confirm the alarm works at its default 20 cm. The card then introduces the two choices coming up (threshold + response) and points to the reference cards.

**Done when.** The full alarm (sensor + LED + buzzer) is wired and working from the starter sketch at the default threshold, and the student has read the two choices coming up.

### Tier 2 Milestone 2 — Choice point A: pick your threshold distance

**What the student does.** Picks how close "too close" should be, based on what they imagine guarding:

- **5 cm — a tripwire.** The alarm fires only when something is almost touching the sensor. Good for guarding a single small object.
- **20 cm — a hand's reach.** The default. Good for "don't reach into my stuff."
- **50 cm — a zone.** The alarm fires when anything enters a wide area. Good for a doorway or a desk corner.

The student writes their choice (5 / 20 / 50 cm) on the card.

**Done when.** The student has picked a threshold and written it on the card.

**Why a choice here.** Principle 5 — the first design choice of the project, made after the student has already seen the basic alarm work, and tied directly to a real intention ("what do I want to guard?").

### Tier 2 Milestone 3 — Choice point B: pick your response + modify the sketch with Claude Code

**What the student does.** Picks what the alarm does when it fires:

- **Light only** (LED), **sound only** (buzzer), or **both**.
- **Steady** (on solid while the object is close) or **pulsing** (blinking/beeping on and off).

Then, following the Channel A Level 2 discipline (Principle 7), the student fills in (a) what they want / (b) what's currently happening / (c) what they've tried **on the card before prompting Claude Code**, and changes two things in `T2_alarm_starter.ino`:

1. The **threshold value** to match their Milestone 2 choice — a one-number change, e.g.:
   > *"How do I make the alarm turn on at 50 cm instead of 20 cm? Here's my code: [paste]."*
2. The **response** to match their choice — turning the LED or buzzer on/off, or making it pulse, e.g.:
   > *"I want the buzzer to beep on and off instead of staying on solid while something is close. Here's my code: [paste]. How do I make it pulse?"*

The student reads Claude's answer, makes the changes in the IDE, uploads, and tests.

**Done when.** The alarm fires at the student's chosen threshold with their chosen response, the change works when they test it, and they can say in one sentence what they changed.

**Why this milestone exists.** The student's substantive code modification for Project 3. The threshold change is a single, concrete number (cause-and-effect unmistakable); the response change is a slightly richer but still bounded edit. Together they are a real, satisfying Level 2 exercise.

**Comprehension check (on the card).** *"After Claude helped you, can you say in one sentence what number or line you changed?"*

### Tier 2 Milestone 4 — Upload, test, and tune your threshold

**What the student does.** Uploads the modified sketch, tests it against the real object or area they care about, and **tunes the threshold** until it feels right — if 50 cm is too jumpy in their corner, they try 40; if 5 cm misses their object, they try 8. Tuning the number is a second small Claude Code Level 2 interaction if the student wants help, or a direct one-number edit if they are comfortable.

**Done when.** The alarm fires where the student wants it to — not too early, not too late — against the real thing they are testing with.

**Why thresholds get their own tuning step.** Keeping the Milestone 3 change to "change the number once" honours Principle 1 (one new idea at a time); the open "make it feel right in my real spot" tuning belongs in this dedicated test-and-tune step. It also models the honest truth that sensor thresholds are found by trying, not calculated.

### Tier 2 Milestone 5 — Signature alarm: name it and show it

**What the student does.** Names their alarm (e.g. "Drawer Guard", "Keep Out", "Snack Defender"), writes the name and what it guards on the Tier 2 line of the workstation poster, and demonstrates it to a peer or the teacher.

**Done when.** The student has named their alarm, recorded it on the poster, and shown it to someone. The teacher celebrates and photographs it for the portfolio (with permission).

**Why this milestone exists.** Principle 5 fully expressed — the student's taste and intention define the alarm. Mirrors Projects 1–2's signature close-out.

---

## Tier 3 — Open Design (one-page project planner)

**Who this tier is for.** Students who completed Tier 2 of a prior project, arrived with prior experience, or explicitly ask for open design. Tier 3 at Project 3 is a strong draw because a proximity alarm has obvious *real jobs* a student can care about.

**Claude Code usage at Tier 3.** Channel A Level 3 — free dialogue, with the same (a)(b)(c) discipline applied to open-ended goals.

**Deliverable.** A single-page **project planner** (`T3_project_planner.html`) with five phases the student fills in:

- **PLAN** — pick a real use case: a **desk-drawer alarm** (beeps when the drawer opens), a **doorway alert** (signals when someone enters), a **pet-food-dish signal** (lights when something approaches), or **something the student invents**. Describe the spot it will guard and what should happen. Decide the threshold and the response. *Optional two-stage idea:* a yellow "getting close" LED on pin 10 before the red alarm — sketch the two zones on paper.
- **BUILD** — wire the circuit for the chosen alarm (add the second LED on pin 10 for a two-stage alarm). Take a photo when done. (Wiring reference: Circuit 4 on R1, `w_p3_04_two_stage`.)
- **CODE** — use Claude Code Level 3 to build or extend the sketch from the student's description. A genuinely interesting Level 3 problem lives here, e.g.: *"I want a drawer alarm that beeps only when the drawer opens, not the whole time something is near the sensor. Here's my code: [paste]. How do I make it alarm only on the change from near to far?"* Upload and test. Iterate.
- **TEST** — does it do the real job the student planned? Try it in the real spot. Iterate until the student is satisfied (the plan can change).
- **SHOW** — show the finished alarm doing its job to the teacher, a peer, or photograph it for the at-home portfolio.

**Wiring reference (two-stage variant).** Circuit 4 on reference card R1 (`w_p3_04_two_stage`).

---

## Claude Code integration — operational detail

**Channel A — Pair programmer.**

*Level 1 — Pre-written sketch upload.* The pre-written sketches for Project 3 are:

- `01_distance_to_serial.ino` — reads the HC-SR04 with `pulseIn()` and prints distance in cm to the Serial Monitor. Used at Tier 1 Milestone 2.
- `02_distance_led_alarm.ino` — adds an LED on pin 9 that lights when distance < 20 cm. Used at Tier 1 Milestone 3.
- `03_distance_full_alarm.ino` — adds the buzzer on pin 8 for a full light + sound alarm at 20 cm. Used at Tier 1 Milestone 4.
- `T2_alarm_starter.ino` — the Tier 2 starter: the full alarm with clearly-marked constants at the top (`THRESHOLD_CM`, `USE_LED`, `USE_BUZZER`, `PULSING`) so the Level 2 modification at Tier 2 Milestone 3 is a small, well-signposted edit.

*Level 2 — Modify with Claude Code's help.* The default expectation at Tier 2 Milestone 3 (and Milestone 4 tuning). The student fills in (a)(b)(c) on the card, pastes the current code with a scaffolded prompt, reads Claude's answer, makes the change, uploads, and tests. Comprehension check: *"After Claude helped you, can you say in one sentence what you changed?"*

*Level 3 — Free dialogue.* Used at Tier 3 to design a custom use-case alarm from the student's description — including the genuinely interesting "alarm only on the transition" drawer problem. No pre-written sketch.

**Channel B — Scaffolded tutorial.** Available at any tier and milestone. The student invokes it by saying: *"I'm on Project 3, Tier X, Milestone Y. Walk me through it."* The Channel B scaffold for Project 3 lives in `claude_code_channel_b_scaffold.md` (+ `_he`).

**Growth trajectory note.** Per [Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §6.13, a student who used Channel A Level 2 for the first time on Project 2 and now uses it confidently on Project 3 — and perhaps reaches Level 3 in Project 3's Tier 3 — is showing exactly the growth the two-channel design is meant to enable.

---

## Safety notes (Project 3 specific)

Project 3's safety envelope is as low as Projects 1–2's — still 5 V, no motors, no soldering, no batteries. The active risks are:

1. **Shorting 5 V to GND directly.** Same as before — usually a stray jumper, or the sensor's VCC and GND bridged. The fix is to remove the offending wire.
2. **An LED without its resistor.** The alarm LED needs its 220 Ω resistor in series. An LED on 5 V with no resistor burns out in seconds.
3. **The buzzer.** Drive the passive piezo buzzer from pin 8 with `tone()`; do **not** wire it directly across 5 V and GND. (Same rule as Project 2.)
4. **The sensor's pins.** Reversing Trig/Echo just stops it working; reversing VCC/GND briefly will not destroy a modern HC-SR04 but should be corrected as soon as the reading fails. There is no shock or heat risk.

**None of these are injury risks.** What the student is told: *"the Arduino and the sensor both run on 5 volts, which is too low to hurt you. Drive the buzzer from a pin, never straight from 5 volts. If something stops working, stop and call the teacher."* The long version is on the safety reminder reference card (R4).

---

## Teacher troubleshooting crib sheet (for the Teacher Troubleshooting artifact)

The most common failure modes in Project 3, in rough frequency order, with the fix:

1. **The Serial Monitor shows nothing / no distance.** Usual cause: the Serial Monitor is not open, or its baud rate doesn't match the sketch (9600). Fix: open the Serial Monitor (magnifying-glass icon) and set 9600 baud.

2. **The distance reads 0, or a huge/jumpy number all the time.** Usual causes: Trig and Echo swapped, or VCC/GND swapped, or a sensor pin not seated in the breadboard. Fix: check all four pins against R1 — VCC→5 V, GND→GND, Trig→12, Echo→11.

3. **The number jumps around even when wired correctly.** Often normal: soft, angled, or fuzzy surfaces scatter the echo, and an empty room gives a large "no echo" reading. The pre-written sketches read repeatedly so a single bad reading passes quickly. Tell the student this is expected; test against a flat, hard surface (a book, a hand, a wall) to see steady numbers.

4. **The LED never lights (Milestone 3).** Usual causes: LED on the wrong pin or backwards (short leg must go to GND), the resistor missing, or the distance never actually dropping below 20 cm because the sensor faces a wall. Fix: check the LED wiring against R1, then move a hand slowly toward the sensor's "eyes".

5. **The buzzer does not beep (Milestone 4).** Usual causes: buzzer leg in 5 V or a dead column instead of pin 8; or the Milestone-3 sketch is still uploaded (the buzzer sketch `03_...` was not actually uploaded). Fix: check the buzzer is on pin 8 + GND, then re-upload `03_distance_full_alarm.ino` and watch for "Done uploading".

6. **The alarm is always on / never on (threshold feels wrong).** Usual cause: the threshold value in the sketch doesn't match the real distance the student is testing at, or the sensor is pointed at a nearby wall so it always reads "close". Fix: confirm where the sensor points, then tune `THRESHOLD_CM` (Tier 2 Milestone 4).

7. **Upload errors ("Arduino not found", "avrdude: stk500_getsync()").** Same causes and fixes as Projects 1–2: wrong COM port, or the Serial Monitor / another IDE window holding the port. The Serial Monitor is open a lot in this project, so close it during upload if the IDE complains the port is busy.

---

## What this source file is not

This file is the **teacher-facing source of truth** for Project 3. It is not a student-facing document (students see the generated task cards, reference cards, tutorial, and Channel B scaffold), not a published curriculum artifact, and not a comprehensive Arduino tutorial. It covers only what Project 3 needs. If any content here conflicts with what a student sees at session time, the student-facing artifact wins and this source file is updated afterwards.

The narrative-level specification of Project 3 lives in [Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §6.7; this file carries the operational detail (milestone IDs, pin map, sketch lineup) that §6.7 deliberately leaves out, mirroring how Projects 1–2's source files relate to their §6 narratives.

---

*End of Arduino Project 3 — Don't Get Too Close source file. Ready for review.*
