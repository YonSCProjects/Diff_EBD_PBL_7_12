# Arduino Project 2 — Reaction-Time Game

*The second project in the Agourim differentiated Arduino workshop program.*
*Source file — teacher-facing. Student-facing task cards, reference cards, HTML tutorial, Claude Code tutorial-channel scaffold, and pre-written `.ino` files are generated from this document.*

**Version 0.1 — draft for review. 2026-06-08.**

---

## What the student builds

A small reflex game on a breadboard with an Arduino Uno, one LED, one push-button, and a piezo buzzer. The Arduino waits a random number of seconds, then turns on the LED (and, after the buzzer is added, beeps); the player has to press the button as fast as they can. The Arduino uses `millis()` to measure the time between the LED turning on and the button being pressed, and reports the result — on the Serial Monitor at Tier 1, and via the student's chosen feedback mode (three fast/medium/slow LEDs, a buzzer pattern, or a Serial readout) at Tier 2. At Tier 1 the student wires the circuit, uploads two pre-written sketches, plays the game, and records their fastest time. At Tier 2 the student makes two design choices (feedback mode + difficulty) and modifies the sketch with Claude Code's help — their first substantive code change. At Tier 3 the student designs a two-player head-to-head variant or a multi-round scored game.

## Why this project is second

Three reasons, grounded in the program's design principles ([Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §4, §6.6):

1. **It reuses Project 1's hardware skills and adds exactly one new component.** The reaction game's circuit is Project 1's LED-plus-button circuit, plus a piezo buzzer. A student who completed Project 1 already knows how to wire an LED with a current-limiting resistor and a push-button with a pull-down resistor. The only genuinely new piece of hardware is the buzzer, which is wired in a single milestone (T1·M4). This keeps the hardware-learning load low so the project's real new content — `millis()` timing and the first code modification — can be the focus.
2. **It is the first project where the student modifies code.** Project 1 was Channel A Level 1 throughout (upload pre-written sketches, no editing). Project 2 is where Channel A Level 2 becomes the default expectation at Tier 2: the student describes a change they want, asks Claude Code for help, reads the answer, makes the edit, and tests. The reaction game is an ideal first modification target because the change is small and concrete ("make the LED stay on for 0.5 seconds instead of 2 seconds") and the result is immediately visible and playable.
3. **It introduces the idea that the Arduino can do more than one thing at once.** The game runs a timer *and* watches for a button press at the same time. This is the student's first encounter with `millis()`-based timing (measuring elapsed time without freezing the program in a `delay()`), a simple game state (waiting → ready → measuring → finished), and event-reactive behaviour. These are the conceptual stepping stones to every later project.

## Hardware per student

All hardware is assumed to be in the Agourim workshop kit. Project 2 reuses Project 1's core circuit and adds one new component (a piezo buzzer). A second push-button is needed only for the Tier 3 two-player variant.

| Qty | Item | New / reused | Notes |
|-----|------|--------------|-------|
| 1 | Arduino Uno R3 (or compatible clone) | reused | Same board as Project 1. |
| 1 | USB-A to USB-B cable | reused | For connecting to the Windows 11 workshop PC. |
| 1 | Full-size breadboard | reused | Same breadboard layout discipline as Project 1. |
| 1 | 5 mm through-hole LED | reused | The "go" LED — turns on to start the reaction window. Any colour. At Tier 2's three-LED mode this is the **fast** indicator. |
| 1 | 220 Ω current-limiting resistor | reused | Colour-code: red-red-brown. One per LED. |
| 1 | Tactile push-button (4-pin) | reused | The player's button. |
| 1 | 10 kΩ pull-down resistor (for button 1) | reused | Colour-code: brown-black-orange. |
| **1** | **Piezo buzzer (small, passive)** | **NEW** | Driven from a digital pin with `tone()`. One leg to the pin, one leg to GND. ~$1. |
| 2 | Extra 5 mm LEDs (Tier 2 three-LED mode only) | reused / add-on | The **medium** and **slow** indicators. Different colours recommended (e.g. yellow + red). |
| 2 | Extra 220 Ω resistors (Tier 2 three-LED mode only) | reused | One per extra LED. |
| **1** | **Second tactile push-button (Tier 3 only)** | **NEW** | Player 2's button for the head-to-head variant. ~$1. |
| **1** | **Second 10 kΩ pull-down resistor (Tier 3 only)** | **NEW** | For the second button. |
| ~15 | Jumper wires (M-M assortment) | reused | For breadboard wiring. |
| 1 | Workshop PC (Windows 11) with Arduino IDE + Google Drive for Desktop | reused | Same setup as Project 1. See Teacher Setup Checklist. |
| 1 | Per-student Project 2 folder on the shared Workshop Drive | new folder | Path: `G:\My Drive\Arduino_Projects\<student_nickname>\Project_2_Reaction_Time_Game\`. Created in the same together-ritual pattern as Project 1's Milestone 1. |

**Incremental cost vs. Project 1:** ~$2–3 per student (piezo buzzer + second button + second pull-down resistor). For 8 students, ~$16–24. Everything else is reused from Project 1's kit.

### Pin map (canonical for all sketches and wiring diagrams)

| Signal | Pin | Used at | Notes |
|--------|-----|---------|-------|
| "Go" LED (and **fast** indicator at Tier 2) | **D9** | T1·M1 onward | PWM-capable; reuses Project 1's pin-9 convention. |
| Buzzer | **D8** | T1·M4 onward | Driven with `tone()`. Off the PWM pins to avoid confusion. |
| Button 1 (player) | **D2** | T1·M1 onward | Standard interrupt-capable input pin; 10 kΩ pull-down to GND. |
| **Medium** indicator LED (Tier 2 three-LED mode) | **D10** | T2·M2b | Added only if the student picks the three-LED feedback mode. |
| **Slow** indicator LED (Tier 2 three-LED mode) | **D11** | T2·M2b | Added only if the student picks the three-LED feedback mode. |
| Button 2 (player 2) | **D3** | T3 only | For the two-player head-to-head variant; 10 kΩ pull-down to GND. |

## Session structure

A "session" at Agourim School is **one 45-minute class period**, of which approximately **30 minutes are actual work time** (see [Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §5.2). Project 2 is designed to fit **two 45-minute sessions** for a Tier 1 student working at a steady pace, with a third session available for students who want more time. As always, nothing pushes a student to finish on a schedule (Principle 5, Principle 9).

**Session 1 typical arc for a Tier 1 student** — Milestones 1 through 3. *Work Block 1:* set up the Project 2 folder and wire the LED + button (M1). *Work Block 2:* upload the "wait, flash, measure" sketch (M2) and play the game five times (M3). A Tier 1 student at the end of Session 1 has a working reaction-time game and has seen their reaction time printed on the Serial Monitor.

**Session 2 typical arc for a Tier 1 student** — Milestones 4 through 6. *Work Block 1:* add the buzzer (M4) and upload the buzzer-feedback sketch (M5). *Work Block 2:* play with the buzzer feedback and record the fastest time on the workstation poster (M6), then celebrate.

**Tier 2 students** typically spend Session 1 on Tier 2 Milestones 1–2 (start-up + feedback-mode choice, plus the conditional wiring card M2b if they chose three LEDs) and Session 2 on Milestones 3–5 (difficulty choice + Claude Code Level 2 modification, test-and-tune, signature game). The Level 2 modification at Milestone 3 is the make-or-break step; the teacher rotates to it.

**Tier 3 students** spend Session 1 on the planning phase (PLAN + BUILD) and Session 2 on coding and testing (CODE + TEST + SHOW). Tier 3 at Project 2 is more common than at Project 1, because a student who enjoyed Project 1 and wants to compete often arrives wanting the two-player game.

## Setup and Wait Protocol

*Prep before the students enter the room. Pre-session time target: ≤ 15 minutes.* The Project 2 setup is identical to Project 1's (see [Arduino_Project_1.md](../Project_1_Light_Signals/Arduino_Project_1.md)) with three differences:

1. **Add the buzzer to each parts tray** (but not pre-wired). The student wires it from scratch at Milestone 4.
2. **Lay out a "go" LED + 220 Ω resistor + one push-button + one 10 kΩ pull-down resistor** per station — the Project 1 circuit subset. Do not pre-wire.
3. **Print one Project 2 poster per workstation** (`teacher_materials/project_2_poster_he.html`) and tape it where the student can write their fastest time at Milestone 6.

The "stuck" protocol is the same on every task card (re-read the step → check the wiring reference R1 → check the other reference cards → call the teacher). The Principle 8 direct-call convention from Project 1 carries over unchanged.

---

## Tier 1 — Guided Build (6 milestones)

**Who this tier is for.** Students who want maximum support, and any student doing Project 2 for the first time who wants the clearest path. The tier is per-project — a student can have been Tier 2 on Project 1 and still choose Tier 1 here because the buzzer and the timing concept are new.

**Claude Code usage at Tier 1.** Channel A Level 1 throughout — every code milestone uploads a pre-written sketch, no editing. Channel B (conversational walk-through) is available but not required.

**Task card count.** Six milestones, six physical task cards. Each card has 3–5 checkboxes, a "done when" criterion, and the standard "stuck" protocol.

### Milestone 1 — Wire the LED and button

**What the student does.** Sets up their Project 2 folder on the Workshop Drive (the same together-ritual as Project 1's Milestone 1, abbreviated for a returning student). Then wires the Project 1 circuit subset: one LED on **pin 9** through a 220 Ω resistor (long leg → resistor → pin 9, short leg → GND), and one push-button on **pin 2** with a 10 kΩ pull-down resistor to GND and the other side to 5 V. This is a direct recapitulation of Project 1's LED wiring (Project 1 M3) and button wiring (Project 1 M7).

**Done when.** The LED is wired to pin 9 through its resistor, the button is wired to pin 2 with its pull-down resistor, and the teacher has confirmed the wiring. *Nothing lights up or beeps yet — the sketch comes at Milestone 2.*

**Why this milestone exists.** It rebuilds the foundation circuit so the student has a known-good base before the new timing concept arrives. A student who did Project 1 will recognise this wiring and gain a quick confidence win; a student who is shaky on the pull-down resistor gets a second, lower-stakes pass at it.

**Wiring reference.** Circuit 1 on reference card R1 (`w_p2_01_led_button`).

**Channel B note.** Channel B is useful here for a student who wants the button wiring walked through again.

### Milestone 2 — Upload the "wait, flash, measure" sketch

**What the student does.** Opens the pre-written sketch `01_wait_flash_measure.ino` from the project folder. Clicks Upload. No code changes. The sketch waits a random 2–5 seconds, turns on the LED, waits for the button press, measures the elapsed time with `millis()`, and prints the reaction time (in milliseconds) to the **Serial Monitor**. The student opens the Serial Monitor (the magnifying-glass icon in the Arduino IDE) to see the readout.

**Done when.** The sketch uploads with a green "Done uploading" message, and opening the Serial Monitor shows the game's instructions and a reaction time after the first press.

**Why this milestone exists.** First `millis()` sketch and the student's first use of the Serial Monitor as an output device. The sketch is pre-written so the first encounter with timing code cannot fail in a confusing way.

**Sketch.** `01_wait_flash_measure.ino` (Tier 1, feedback = Serial Monitor). See R5.

### Milestone 3 — Play the game five times

**What the student does.** Plays the reaction game five times. Each round: wait for the LED, press the button as fast as possible, read the reaction time on the Serial Monitor. The student notices their times vary and tries to beat their own best.

**Done when.** The student has played five rounds and can point to their fastest time on the Serial Monitor.

**Why this milestone exists.** The visible win (Principle 4) and the Principle 6 movement moment — reacting physically fast *is* the activity, and the competitive pull is the engagement engine. The student experiences the full game loop working before any new hardware or code is added.

**Channel B note.** Channel B can explain "why is the wait time different each round?" conversationally — the first place a curious student meets the idea of a random number.

### Milestone 4 — Add the buzzer

**What the student does.** Wires the piezo buzzer into the existing breadboard: one leg to **pin 8**, the other leg to **GND**. The buzzer is the only new component in Project 2. No resistor is needed for a small passive piezo buzzer driven from a digital pin.

**Done when.** The buzzer is wired (pin 8 + GND) and the teacher has confirmed it. *The buzzer does not beep yet — the sketch that drives it comes at Milestone 5.*

**Why this milestone exists.** The single new-hardware milestone of Project 2, deliberately isolated so the student adds one component and confirms it before changing the code.

**Wiring reference.** Circuit 2 on reference card R1 (`w_p2_02_led_button_buzzer`).

**Common stuck moment (teacher-facing).** A passive piezo buzzer has no polarity to worry about in this use, but students sometimes put both legs in the same breadboard column (shorting it) or run a leg to 5 V instead of a pin. The reference card shows pin 8 + GND.

### Milestone 5 — Upload the updated sketch with buzzer feedback

**What the student does.** Opens the second pre-written sketch `02_wait_flash_measure_buzzer.ino` and uploads it. No code changes. This sketch does everything the first one did, plus: it beeps the buzzer at the "go" moment (so the student can react to sound as well as light), and plays a short success tone when the button is pressed.

**Done when.** The sketch uploads, and playing a round now produces a beep at the "go" moment and a tone on the press, in addition to the Serial Monitor readout.

**Why this milestone exists.** The student's second upload of the project and the payoff for adding the buzzer — the game is now multi-sensory. Still Level 1 (no editing), but the student can see in the IDE that the new sketch has `tone()` lines the old one didn't.

**Sketch.** `02_wait_flash_measure_buzzer.ino` (Tier 1, feedback = Serial Monitor + buzzer). See R5.

### Milestone 6 — Write your fastest time on the Project 2 poster

**What the student does.** Looks back over their rounds, finds their fastest reaction time, and writes it on the **Project 2 poster** taped at their workstation. The poster has a row per student nickname and a column for the fastest time.

**Done when.** The student's fastest time is written on the workstation poster, and the teacher has celebrated.

**Why this milestone exists.** The closing celebration and artifact milestone (Principle 4 + Principle 6). The poster makes the student's achievement visible and persistent, and turns the workstation into a friendly leaderboard the cohort can rally around. The teacher celebrates the same way as Project 1's Milestone 8 — visibly, by name, with a portfolio photo if the student agrees, and by asking what they want to build next.

**Poster artifact.** `teacher_materials/project_2_poster.html` (+ `_he`). Printable; the teacher prints one per workstation.

---

## Tier 2 — Guided Design (5 milestones with two choice points)

**Who this tier is for.** Students who completed a Tier 1 project and want more control, or who arrived with some prior experience. Project 2's Tier 2 is, for many students, their **first experience of modifying code** — Channel A Level 2 is the default interaction mode here.

**Claude Code usage at Tier 2.** Channel A Level 1 for the starter sketches; Channel A Level 2 for the modification at Milestone 3. Channel B available throughout.

**Task card count.** Five milestones (M1, M2, M3, M4, M5), plus one **conditional** card (M2b) that only fires for students who pick the three-LED feedback mode. A single student's path is always five cards.

### Tier 2 Milestone 1 — Start-up

**What the student does.** Compressed version of Tier 1 Milestones 1–3: set up the folder, wire the LED + button, upload the starter sketch, play a round to confirm the game works. Then the card introduces the two choice points coming up (feedback mode + difficulty) and points to the reference cards.

**Done when.** The reaction game is wired and running from the starter sketch, and the student has read the two choices coming up.

### Tier 2 Milestone 2 — Choice point A: pick your feedback mode

**What the student does.** Picks one of three feedback modes for how the game reports the result:

- **Mode A — Three LEDs (fast / medium / slow).** Three LEDs light up by category: fast → green (pin 9), medium → yellow (pin 10), slow → red (pin 11). Requires wiring two extra LEDs (the conditional card **M2b**).
- **Mode B — Buzzer pattern.** The buzzer plays a different pattern for fast / medium / slow (e.g. one high beep, two beeps, one low buzz). No extra wiring beyond the buzzer.
- **Mode C — Serial Monitor readout.** A richer Serial Monitor message (e.g. "FAST! 210 ms" with a category word). No extra wiring.

The student writes their choice (A / B / C) on the card.

**Done when.** The student has picked a feedback mode and written it on the card.

**Why a choice here.** Principle 5 — the first design choice of the project, made after the student has already seen the basic game work.

### Tier 2 Milestone 2b — Wire the extra LEDs *(conditional — only if Mode A was chosen)*

**What the student does.** Only if the student picked **Mode A (three LEDs)**: wire two more LEDs — medium on **pin 10** and slow on **pin 11**, each with its own 220 Ω resistor, mirroring the pin-9 LED. Students who picked Mode B or Mode C skip this card entirely and go straight to Milestone 3.

**Done when.** The two extra LEDs are wired (pin 10 + pin 11, each through a resistor to GND) and the teacher has confirmed.

**Wiring reference.** Circuit 3 on reference card R1 (`w_p2_03_three_leds_button_buzzer`).

**Note.** This mirrors Project 1's conditional T2·M2b ("wire the third LED") pattern exactly.

### Tier 2 Milestone 3 — Choice point B: pick difficulty + modify the sketch with Claude Code

**What the student does.** Picks the difficulty:

- **Easy** — the LED stays on for 2 seconds, so slower reactions still count.
- **Hard** — the LED stays on for only 0.5 seconds, so only fast reactions count.

Then, following the Channel A Level 2 discipline (Principle 7), the student fills in (a) what they want / (b) what's currently happening / (c) what they've tried **on the card before prompting Claude Code**, and uses the master document's verbatim prompt scaffold:

> *"Here's my current delay. How do I make the LED stay on for only 0.5 seconds instead of 2 seconds? Here's my code: [paste]."*

The student reads Claude's answer, makes the one-line change in the IDE, uploads, and tests. This is the substantive code modification that defines Project 2.

**Done when.** The student has changed the LED-on window to match their chosen difficulty, the change works when they play, and they can say in one sentence what line they changed.

**Why this milestone exists.** The student's first real code modification. The change is deliberately a single, concrete number so the modification is achievable and the cause-and-effect is unmistakable.

**Comprehension check (on the card).** *"After Claude helped you, can you say in one sentence which line you changed?"*

### Tier 2 Milestone 4 — Upload, test, and tune your variant

**What the student does.** Uploads the modified sketch (with their feedback mode and difficulty), plays five rounds, and — if they chose Mode A or B — tunes the fast/medium/slow thresholds so the categories feel right for them (e.g. "fast = under 250 ms"). Threshold tuning is a second small Claude Code Level 2 interaction if the student wants help.

**Done when.** The student's variant runs the way they want: the right feedback mode, the right difficulty, and (for Mode A/B) thresholds that feel fair.

**Why thresholds live here.** Keeping the difficulty change (M3) to a single concept (the 0.5s vs 2s window) honours Principle 1; the more open "make the categories feel right" tuning belongs in this dedicated test-and-tune step.

### Tier 2 Milestone 5 — Signature game: name it and share

**What the student does.** Names their variant (e.g. "Lightning Round", "Owl Mode"), writes the name and their fastest time on the Tier 2 line of the workstation poster, and plays a round head-to-head against a peer or the teacher.

**Done when.** The student has named their variant, recorded it, and shown it to someone. The teacher celebrates and photographs it for the portfolio (with permission).

**Why this milestone exists.** Principle 5 fully expressed — the student's taste and identity enter the project. Mirrors Project 1's signature-pattern close-out.

---

## Tier 3 — Open Design (one-page project planner)

**Who this tier is for.** Students who completed Tier 2 of a prior project, arrived with prior experience, or explicitly ask for open design. Tier 3 at Project 2 is more common than at Project 1, because the two-player competition is a natural draw.

**Claude Code usage at Tier 3.** Channel A Level 3 — free dialogue, with the same (a)(b)(c) discipline applied to open-ended goals.

**Deliverable.** A single-page **project planner** (`T3_project_planner.html`) with five phases the student fills in:

- **PLAN** — which variant? Two choices are offered: (1) a **two-player head-to-head** game with a second button (pin 3) and a way to show who won, or (2) a **multi-round scored** game that keeps score across 5 rounds. Sketch the game flow on paper. What feedback? What hardware?
- **BUILD** — wire the circuit for the chosen variant (the two-player variant needs the second button + pull-down on pin 3). Take a photo when done.
- **CODE** — use Claude Code Level 3 to build the sketch from the student's description. Upload and test. Iterate.
- **TEST** — does it do what the student planned? Iterate until the student is satisfied (the plan can change).
- **SHOW** — show the finished game to the teacher, a peer, or photograph it for the at-home portfolio.

**Wiring reference (two-player variant).** Circuit 4 on reference card R1 (`w_p2_04_two_buttons_variant`).

---

## Claude Code integration — operational detail

**Channel A — Pair programmer.**

*Level 1 — Pre-written sketch upload.* The pre-written sketches for Project 2 are:

- `01_wait_flash_measure.ino` — the Tier 1 game: random wait, LED on, measure reaction with `millis()`, print to Serial Monitor. Used at Tier 1 Milestone 2.
- `02_wait_flash_measure_buzzer.ino` — adds `tone()` buzzer feedback to the game. Used at Tier 1 Milestone 5.
- `T2_three_led_feedback_starter.ino` — Tier 2 starter for Mode A (three fast/medium/slow LEDs).
- `T2_buzzer_pattern_starter.ino` — Tier 2 starter for Mode B (distinct buzzer patterns per category).
- `T2_serial_readout_starter.ino` — Tier 2 starter for Mode C (rich Serial Monitor readout with category word).

*Level 2 — Modify with Claude Code's help.* First introduced (as the default expectation) at Tier 2 Milestone 3. The student fills in (a)(b)(c) on the card, pastes the current code with the master-doc scaffold, reads Claude's answer, makes the change, uploads, and tests. The comprehension check is: *"After Claude helped you, can you explain in one sentence which line changed?"*

*Level 3 — Free dialogue.* Used at Tier 3 to design the two-player or multi-round variant from the student's description. No pre-written sketch.

**Channel B — Scaffolded tutorial.** Available at any tier and milestone. The student invokes it by saying: *"I'm on Project 2, Tier X, Milestone Y. Walk me through it."* The Channel B scaffold for Project 2 lives in `claude_code_channel_b_scaffold.md` (+ `_he`).

**Growth trajectory note.** Per [Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §6.13, a student who used Channel B throughout Project 1, uses Channel B + Channel A Level 1 in Project 2 Tier 1, and reaches Channel A Level 2 in Project 2 Tier 2 is showing exactly the growth the two-channel design is meant to enable.

---

## Safety notes (Project 2 specific)

Project 2's safety envelope is nearly as low as Project 1's — still 5 V, no motors, no soldering, no batteries. The active risks are:

1. **Shorting 5 V to GND directly.** Same as Project 1 — usually a stray jumper or a button wired without its pull-down resistor. The fix is to remove the offending wire.
2. **An LED without its resistor.** Every LED (the go LED and the Tier 2 indicator LEDs) needs a 220 Ω resistor in series. An LED on 5 V with no resistor burns out in seconds.
3. **The buzzer.** A small passive piezo buzzer is safe driven from a digital pin with `tone()`. Do **not** connect the buzzer directly across 5 V and GND — drive it from pin 8 so the Arduino controls it. A buzzer wired directly to 5 V will sound continuously and can draw more current than intended.

**None of these are injury risks.** What the student is told: *"the Arduino runs on 5 volts, which is too low to hurt you. The buzzer is safe — but always drive it from a pin, never straight from 5 volts. If something stops working, stop and call the teacher."* The long version is on the safety reminder reference card (R4).

---

## Teacher troubleshooting crib sheet (for the Teacher Troubleshooting artifact)

The most common failure modes in Project 2, in rough frequency order, with the fix:

1. **The game seems to do nothing after upload.** Usual cause: the Serial Monitor is not open, so the student can't see the game's prompts and result. Fix: open the Serial Monitor (magnifying-glass icon) and set the baud rate to match the sketch (9600). The game prints its instructions there.

2. **The button press is not detected.** Usual cause: pull-down resistor on the wrong side (5 V → GND instead of pin 2 → GND), exactly as in Project 1's Milestone 7. Fix: move the resistor so it is between pin 2 and GND. See R1.

3. **The buzzer does not beep at Milestone 5.** Usual causes: (a) buzzer leg in 5 V or a dead column instead of pin 8; (b) the old (Milestone 2) sketch is still uploaded — the buzzer sketch (`02_...`) was not actually uploaded. Fix: check the buzzer is on pin 8 + GND, then re-upload `02_wait_flash_measure_buzzer.ino` and watch for "Done uploading".

4. **The buzzer sounds continuously / never stops.** Usual cause: the buzzer is wired directly across 5 V and GND instead of from pin 8. Fix: move the driven leg to pin 8.

5. **Reaction times look impossibly small (e.g. 0–20 ms) or the round ends instantly.** Usual cause: button bounce or a floating input — often the pull-down resistor is missing, so pin 2 reads HIGH before the LED even turns on. Fix: confirm the 10 kΩ pull-down is in place. The pre-written sketch also ignores presses that arrive before the "go" moment (jump-the-gun guard).

6. **Three-LED mode (Tier 2) lights the wrong LED or none.** Usual cause: the medium/slow LEDs are not on pins 10/11, or the thresholds in the sketch don't match how the student plays. Fix: check pins 10/11 against R1, then tune thresholds at Milestone 4.

7. **`millis()` rollover worry.** Not a real issue for this project — `millis()` rolls over after ~49 days of continuous running. A workshop session is far shorter, so the starter sketches do not need rollover handling. Mentioned only so the teacher can reassure a student who read about it online.

8. **Upload errors ("Arduino not found", "avrdude: stk500_getsync()").** Same causes and fixes as Project 1: wrong COM port, or the Serial Monitor / another IDE window holding the port. Note: with this project the Serial Monitor is open a lot, and it must be **closed during upload** if the IDE complains the port is busy.

---

## What this source file is not

This file is the **teacher-facing source of truth** for Project 2. It is not a student-facing document (students see the generated task cards, reference cards, tutorial, and Channel B scaffold), not a published curriculum artifact, and not a comprehensive Arduino tutorial. It covers only what Project 2 needs. If any content here conflicts with what a student sees at session time, the student-facing artifact wins and this source file is updated afterwards.

The narrative-level specification of Project 2 lives in [Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §6.6; this file carries the operational detail (milestone IDs, pin map, sketch lineup) that §6.6 deliberately leaves out, mirroring how Project 1's Appendix 1 carries milestone IDs while §6.6 gives the narrative.

---

*End of Arduino Project 2 — Reaction-Time Game source file. Ready for review.*
