# Arduino Project 1 — Light Signals

*The first project in the Agourim differentiated Arduino workshop program.*
*Source file — teacher-facing. Student-facing task cards, reference cards, HTML tutorial, Claude Code tutorial-channel scaffold, and pre-written `.ino` files are generated from this document.*

**Version 0.1 — draft for review. 2026-04-11.**

---

## What the student builds

A small breadboard circuit with an Arduino Uno, two LEDs, a push-button, and current-limiting resistors. The LEDs blink in a pattern the student can see, modify, and control with the push-button. At Tier 1 the student uploads pre-written sketches and watches the hardware respond. At Tier 2 the student picks between different LED patterns and modifies a sketch to match their choice. At Tier 3 the student designs and programs their own "signature pattern" — anything from a mood light to an alarm signal to a two-player reaction cue.

## Why this project is first

Three reasons, grounded in the program's design principles ([Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §4):

1. **It produces a visible win almost immediately.** A blinking LED is instantly legible as success — the student plugs in the Arduino, clicks Upload, and a light starts blinking. Principle 4 (hyper-chunked milestones with visible wins) is the load-bearing reason this is Project 1 and not a more ambitious build.
2. **Nothing can go dangerously wrong.** No motors, no soldering, no batteries, no moving parts. The safety envelope is just "don't short the 5 V pin to GND, and don't poke the LED into the USB port." A student who has never touched electronics can succeed at Project 1 without acquiring a single safety discipline first. Those disciplines are introduced gradually across Projects 2–4.
3. **It is the student's first encounter with Claude Code.** Both Channel A (pre-written sketch upload — Level 1) and Channel B (conversational walk-through of the task cards) are introduced here at the lowest possible stakes. A student who finds the AI intimidating can complete every Tier 1 milestone at Channel A Level 1 without ever typing a word to Claude. A student who wants more can try Channel A Level 2 on the last Tier 1 milestone or move to Tier 2 on the next session.

## Hardware per student

All hardware is assumed to be in the Agourim workshop kit. This list is the student's workstation setup for Project 1. If any item is missing at session time, the teacher substitutes from the parts library or adjusts the task card wording live.

| Qty | Item | Notes |
|-----|------|-------|
| 1 | Arduino Uno R3 (or compatible clone) | The board has a built-in "L" LED on digital pin 13 that blinks from the factory sketch — Milestone 1 uses this as the first positive experience. |
| 1 | USB-A to USB-B cable | For connecting the Arduino Uno to the Windows 11 workshop PC. |
| 1 | Full-size breadboard (~830 tie points) | The student wires the external LEDs and button here. |
| 2–3 | 5 mm through-hole LEDs in different colours | Any colour is fine. At Tier 2/3 the student can pick the colours they like. |
| 2–3 | 220 Ω current-limiting resistors (one per LED) | Colour-code: red-red-brown. The resistor pack in the workshop has these in the first compartment. |
| 1 | Tactile push-button (4-pin, breadboard-friendly) | Added at Milestone 7, not before. |
| 1 | 10 kΩ pull-down resistor (for the button) | Colour-code: brown-black-orange. |
| ~15 | Jumper wires (M-M assortment) | For breadboard wiring. |
| 1 | Workshop PC (Windows 11) with Arduino IDE installed | Arduino IDE 2.x or later. Google Drive for Desktop installed and logged in to the shared robotics-workshop Google account, with the account's `My Drive` mounted at `G:\My Drive\`. See Teacher Setup Checklist. |
| 1 | Per-student Project 1 folder on the shared Workshop Drive | Path: `G:\My Drive\Arduino_Projects\<student_nickname>\Project_1_Light_Signals\`, where `<student_nickname>` is a nickname the student chose at their first workshop session (see §5.1 and §5.5 of the master document on the nickname architecture). Created at Milestone 1 in a together-ritual between the student and the teacher (see Milestone 1 below). This folder is the student's persistent workspace for Project 1 — their pre-written sketches, their modifications, their photos, and any notes they write all live here across sessions and across the whole year. |
| 1 | Claude Code launched pointed at the student's Project 1 folder | Invoked via the shared robotics-workshop Google account, with the student's Project 1 folder as the working directory. Claude Code can read and write the student's actual sketch files. See §5.5 of the master document for the dual-channel (pair programmer / scaffolded tutorial) operational detail. |

**Cohort kit for 8 students:** 8× each of the above (per-student columns). Plus the parts library stock: spare LEDs, spare resistors, spare jumper wires, and the "sort the resistor pack" backup-task bin (see *Setup and Wait Protocol* below).

## Session structure

A "session" at Agourim School is **one 45-minute class period**, of which approximately **30 minutes are actual work time** (the other 15 minutes are arrival, mini-huddle, movement break, clean-up, and close-out circle — see [Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §5.2). The two work blocks are 15 minutes each, which is the exact duration Principle 4's hyper-chunked milestone structure assumes.

Project 1 is designed to fit **two 45-minute sessions** for a Tier 1 student working at a steady pace, **three sessions** for a student who needs extra time on wiring or who has never used an Arduino before, and **one long or two short sessions** for a student who is fast or has prior Arduino experience. Nothing in the program pushes a student to finish on a particular schedule — the task cards and the teacher rotation adjust to the student, not the other way around (Principle 5, Principle 9 — see [Arduino_PBL_Program.md](../../Arduino_PBL_Program.md) §4).

**Session 1 typical arc for a Tier 1 student** — Milestones 1 through 4. *Work Block 1:* plug in the Arduino, see the factory blink (M1); upload the first sketch (M2); start wiring the first LED (M3). *Work Block 2:* finish wiring the first LED if not done in Block 1; upload the second sketch; confirm the external LED blinks (M4). A Tier 1 student at the end of Session 1 has a blinking external LED of their chosen colour on their own breadboard and has clicked Upload at least twice.

**Session 2 typical arc for a Tier 1 student** — Milestones 5 through 8. *Work Block 1:* wire the second LED (M5); upload the alternating-blink sketch (M6). *Work Block 2:* wire the push-button with the pull-down resistor (M7); upload the button-controlled sketch and celebrate (M8). A Tier 1 student at the end of Session 2 has a two-LED circuit with a button that switches which LED is on, and has taken a photo to show a family member at home (with their permission).

**Session 3 (if needed) for a Tier 1 student** — catching up any milestone that did not complete in Sessions 1 or 2. Milestone 7 (the push-button with pull-down resistor) is the most common "needs a third session" milestone because the pull-down wiring is the single hardest piece of Project 1 and several students will not finish it in the second work block of Session 2.

**Tier 2 students** typically spend Session 1 on Tier 2 Milestones 1–2 (start-up + pattern choice) and Session 2 on Tier 2 Milestones 3–5 (first Channel A Level 2 interaction, button behaviour choice, signature pattern show-off). Tier 2 students may finish in two 45-minute sessions if their Channel A Level 2 modification at Milestone 3 goes smoothly.

**Tier 3 students** typically spend Session 1 on the planning phase (PLAN + BUILD), Session 2 on the coding and testing phases (CODE + TEST + iteration), and Session 3 on the show-off phase — though Tier 3 at Project 1 is rare (see the Tier 3 section below).

## Setup and Wait Protocol

*Prep before the students enter the room. Pre-session time target: ≤ 15 minutes.*

### Teacher setup checklist (one-page version lives in the Teacher Setup Checklist artifact)

1. **Print and laminate the task cards for today's expected tiers.** Tier 1 cards are the default; add Tier 2/3 cards for students likely to reach them. Cards are in `Arduino_Projects/Project_1_Light_Signals/task_cards/`.
2. **Lay out each workstation** with: Arduino Uno, USB-B cable plugged into the PC, breadboard, one LED + one 220 Ω resistor in a small parts tray, and a set of ~15 jumper wires. *Do not pre-wire anything.* The student wires from scratch — that is the point of Milestones 3 onward.
3. **Open the Arduino IDE on each PC** and confirm the board type (Tools → Board → Arduino Uno) and the correct COM port (Tools → Port → COMx). Do a test compile-and-upload of `01_blink_L.ino` to confirm the IDE is talking to the board. *This is the highest-risk setup failure; check it before students arrive.*
4. **Verify the shared Workshop Drive state and prepare for each student's folder together-ritual.** For each student in today's session:
   - Confirm **Google Drive for Desktop** is running and logged into the shared robotics-workshop Google account, with the account's `My Drive` mounted at `G:\My Drive\`. If Drive for Desktop is not running, start it from the Windows Start menu and wait for the Drive to finish syncing before students arrive.
   - Open File Explorer and navigate to `G:\My Drive\Arduino_Projects\`. This is the top-level folder that holds every student's per-nickname subfolder for the whole robotics program.
   - **If the student has already worked in the robotics workshop on any earlier project**, their nickname subfolder already exists at `G:\My Drive\Arduino_Projects\<their_nickname>\`. Confirm it is visible and accessible.
   - **If this is the student's first time in the workshop ever**, the student's nickname subfolder does not exist yet and the student has not yet picked a nickname. Both of those happen at Milestone 1 in the together-ritual — you and the student pick a nickname together and create the folder together. **Do NOT pre-create a folder with a guess at the nickname.** The student chooses the nickname, not you.
   - **Do NOT pre-create the `Project_1_Light_Signals` subfolder for any student.** That folder is created in the one-minute together-ritual between you and the student at Milestone 1, and the ritual is a deliberate ownership moment (§5.5 of the master document — the Sciacca 2025 building-trusting-relationships anchor). The student watches the folder come into existence. Creating it ahead of time removes the ritual.
   - Open **Claude Code** on the workstation but **do not launch it into a working directory yet**. Claude Code is launched into the student's Project 1 folder during Milestone 1, after the folder is created together. A Claude Code session that was left open from a previous student's session with a different working directory should be closed and restarted fresh for the new student.
   - Confirm the student's workstation has Arduino IDE open with the correct Board (Arduino Uno) and Port (COMx) selected — see the setup check in the next paragraph.
   - Have your private nickname-to-real-name mapping sheet (the tracking sheet from §5.8 of the master document) ready to record a new nickname if this is the student's first workshop session. The mapping lives in your private notes, not on the shared Drive.
5. **Place the laminated reference cards** at each station: wiring reference, stuck-protocol reference, Claude Code prompt templates (Tier 2+ only), safety reminder.
6. **Place the backup-task bin** at each station: a small tray of ~30 mixed resistors from the workshop parts library. The backup task card reads: *"If you need to wait for the teacher and you've already tried the 'stuck' steps, sort these resistors by colour-code band value. Put them in order from smallest (1 Ω) to largest (1 MΩ)."* This is a quiet, tactile, mildly educational task that previews Project 3's sensor threshold work. Students who have already learned to read resistor colour codes from Project 3 or later can instead practice reading 4-band and 5-band codes side by side.
7. **Confirm the cool-down corner** is set up at the back of the workshop (§5.6 of the master document). Not Project 1-specific but always part of session setup.
8. **Review the tracking sheet** (§5.8 of the master document) for the expected students today and note any students whose last-session row had a red-card incident — those students need an intentional relational check-in during Arrival.

### The "stuck" protocol (same on every task card)

If a student gets stuck on any step, before calling the teacher they try in order:

1. **Re-read the step.** The task card's "what to do" section often answers its own question on the second reading.
2. **Check the wiring reference card** at the station. For hardware steps, ~60% of stuck moments are wiring errors the reference card catches.
3. **Check the stuck-protocol reference card** at the station. It lists the most common upload errors and wiring mistakes with short fixes ("Arduino not found → check COM port"; "LED doesn't light → flip the LED; long leg is +").
4. **Call the teacher** by raising a hand or saying the teacher's name. (No cup signalling, no flag — just the student's voice or hand. This is a deliberate Principle 8 choice — the call itself is a small relational moment.)
5. **If the teacher is busy** — work on the backup task (sort the resistor pack) until the teacher rotates to the workstation.

### Principle 8 note — the call itself is the intervention

The older LEGO-rover project in this repo used a traffic-light-cup system (red / yellow / green cups at each station) for non-verbal help signalling. The Arduino workshop program has deliberately dropped that system in favour of the student calling the teacher directly. The reason: the call is a small relational moment, and the teacher's walk-over is the trust-building exchange Principle 8 is built around. A cup system is more scalable but less personal; for an 8-student cohort with one teacher, the relational value of the direct call outweighs the efficiency of the cup system. If the cohort later grows beyond eight students or if the call system turns out not to scale, the cup system is documented in `Project_1_Start_Stop_Rover.md` and can be reintroduced.

---

## Tier 1 — Guided Build (8 milestones)

**Who this tier is for.** Students who need maximum support on their first Arduino project, students with high anxiety or coding-trauma histories, students who have not used an Arduino before, and students who simply want the clearest possible path through the project. A student can start at Tier 1 on Project 1 and move to Tier 2 on Project 2 — the tier is per-project, not a permanent label.

**Claude Code usage at Tier 1.** Channel A Level 1 throughout. Every milestone that involves code uses a pre-written `.ino` file the student opens and uploads. Channel B (the conversational tutorial-channel scaffold) is **available but not required** — a student who prefers to read the printed task card on their own does that; a student who prefers to hear the card walked through conversationally invokes Channel B. Neither path is privileged.

**Task card count.** Eight milestones, eight physical task cards. Each card has 3–5 checkboxes, a "done when" criterion, and the standard "stuck" protocol.

### Milestone 1 — Set up your workspace and plug in the Arduino (together-milestone)

**This is a together-milestone.** The teacher is at the student's side for this whole milestone. It is not a card the student works through alone. The teacher's presence for the full milestone is not optional — it is the student's first session of Project 1 and the point of the milestone is as much the relational moment as the technical setup. Budget approximately **5 minutes** for a student who has already worked in the workshop on an earlier project (they already have a nickname), and **up to 10 minutes** for a first-time-ever student who is picking their nickname at this moment.

**What the student does (with the teacher beside them):**

**Step 0 — Pick a nickname (only if this is your first time in the workshop ever).** If this is the student's first workshop session on any project, the teacher begins the ritual with the nickname question: *"What name do you want to use for your folder? It can be your real first name if you want, or any nickname you like — a character, an animal, a favourite word. It is going to be your folder's name for the whole year, so pick something you like seeing."* The student picks. The teacher writes the nickname next to the student's real name on the teacher's private tracking sheet (§5.8 of the master document). If the student already has a nickname from a previous project, skip Step 0 and go straight to Step 1.

1. **Open File Explorer** on the workshop PC (Windows key + E, or the folder icon on the taskbar).
2. **Navigate to the shared Workshop Drive:** `G:\My Drive\Arduino_Projects\`. This folder holds one subfolder per student nickname, including the student's own subfolder if they have worked in the workshop before.
3. **If this is the student's first workshop session ever:** together, create the student's own top-level nickname folder inside `Arduino_Projects`. The student types their chosen nickname as the folder name, or the teacher types it while the student watches, depending on the student's keyboard comfort. The nickname is now visible in the path as the student's own folder.
4. **If the student already has a nickname folder from a previous project:** the student opens their existing nickname folder (`G:\My Drive\Arduino_Projects\<their_nickname>\`) and sees their previous project folders already inside.
5. **Inside the nickname folder, create a new subfolder** called `Project_1_Light_Signals`. Same together-typing arrangement.
6. **Open Claude Code** and launch it with the new `Project_1_Light_Signals` folder as its working directory. The teacher walks the student through the exact invocation path on the workstation.
7. **Pick up the USB-B cable** and plug the Arduino Uno into the computer. Push the square end into the Arduino and the flat end into the PC's USB port.
8. **Look at the Arduino board** itself and find the small green "L" LED near pin 13 — the built-in LED that blinks from the factory sketch.
9. **Open the Arduino IDE** (the shortcut is on the desktop). The teacher confirms with the student that the Board menu shows "Arduino Uno" and the Port menu shows the correct COM port.

**The teacher's recognition line.** At the moment the folder is created and Claude Code is opened pointed at it, the teacher says to the student, short and direct:

> *"This is your folder, this is your project, Project 1 starts now."*

The exact words matter less than the recognition — the student has just watched their own folder come into existence in their own nickname subfolder, and an adult who knows them is welcoming them into it. The line is one breath, not a speech. If the student responds, the teacher listens; if the student doesn't respond, the teacher moves on. This is the small relational moment Principle 8 of the master document commits to, operationalised in one sentence.

**Done when.** The student has all five of these, together:
- Their own top-level nickname folder at `G:\My Drive\Arduino_Projects\<their_nickname>\` (created now or pre-existing from a previous project).
- Their own `Project_1_Light_Signals` subfolder inside it, newly created.
- Claude Code open and pointed at the Project 1 folder.
- The Arduino Uno plugged in via USB.
- The "L" LED on the Arduino blinking on/off about once per second from the factory sketch.

**Why this milestone exists.** It is the student's very first positive experience with the hardware **and** the student's literal moment of taking ownership of their Project 1 workspace. Three things happen at once: the student picks or confirms their nickname (identity + autonomy, Principle 5), the student sees their own folder come into existence on the Drive (ownership ritual, §5.5 of the master document), and the student sees the "L" LED blinking on the Arduino (first visible win, Principle 4). The blinking LED is **guaranteed not to fail** because the factory sketch is already installed on every Arduino Uno from the manufacturer — the student has done nothing except plug in a cable, and something blinks. And the folder creation is guaranteed not to fail because the teacher is beside the student the whole time, walking them through every click.

**Why this is a together-milestone and not a solo task card.** The Sciacca (2025) building-trusting-relationships sub-theme (§3.5 of the master document) is operationalised here — the teacher's presence during the student's first moment of taking ownership of their workspace is the small relational moment Principle 8 commits to. A student who goes through Milestone 1 alone and sees a folder appear on a screen misses the ritual's full weight. A student who goes through Milestone 1 beside the teacher, picks their own nickname, watches their folder come into existence, and hears the teacher's recognition line, gets the moment the program is designed to deliver.

**Student task card language (what actually appears on the printed card the student reads).**

> *Milestone 1 — Set up your workspace and plug in the Arduino*
>
> *The teacher will help you with this milestone — it is a together-milestone.*
>
> *What to do (with the teacher beside you):*
>
> - [ ] **First time in the workshop?** Pick a nickname for your folder. It can be any name you like — a character, an animal, your real first name, anything you want to see on the screen. Tell the teacher your nickname.
> - [ ] Open File Explorer (Windows key + E)
> - [ ] Go to `G:\My Drive\Arduino_Projects\`
> - [ ] Find your nickname folder, or create it together with the teacher
> - [ ] Inside your nickname folder, create a new folder called `Project_1_Light_Signals`
> - [ ] Open Claude Code with your new `Project_1_Light_Signals` folder
> - [ ] Plug in the Arduino with the USB cable
> - [ ] Look at the Arduino — you should see a small green light blinking near pin 13
> - [ ] Open the Arduino IDE
>
> *Done when:* You have your own nickname folder, your `Project_1_Light_Signals` folder inside it, Claude Code is open, the Arduino is plugged in, and the green light on the Arduino is blinking.
>
> *Stuck? Try this first:* This is a together-milestone — the teacher will walk you through it. If the teacher is with another student right now, wait at your workstation and work on sorting the resistor pack on your desk until the teacher comes to you.

**Channel A Level 1 note.** No sketch upload at this milestone. The factory sketch is already installed on the Arduino and the newly-created `Project_1_Light_Signals` folder is empty of sketches — that is normal. Sketches start appearing at Milestone 2, when the pre-written `01_blink_L_fast.ino` is copied into the folder.

**Channel B note.** Channel B is technically available at Milestone 1, but because the milestone is a together-milestone with the teacher present, a student using Channel B would be hearing instructions from Claude Code while the teacher is also speaking to them — which is confusing. Milestone 1 is the one milestone in Project 1 where Channel B is **not recommended**. Channel B becomes available and useful at Milestone 2 onward, once the student is working more independently.

**Research basis (teacher-facing).** *[Verification: Principle 4 — hyper-chunked milestones with visible wins. The LED blinking on the board is the first of many "something I did made the thing work" moments the super-target commits to (Arduino_PBL_Program.md §1, §4).]* *[Verification: Principle 5 — structured autonomy, not forced compliance. The student picking their own nickname is a Principle 5 autonomy moment at the earliest possible point in the program; the nickname is the student's chosen representation of themselves in the workshop's digital workspace for the entire year.]* *[Verification: Principle 8 — the teacher-student relationship is the multiplier. The together-milestone framing, the nickname question, and the recognition line are the direct operationalisation of Sciacca (2025)'s building-trusting-relationships sub-theme (§3.5), where all three of Sciacca's participant teachers described rapport and trust with students as the foundation on which PjBL works. The one-minute folder-creation ritual is a micro-relationship moment that costs one minute and returns real ownership plus a student-chosen nickname that carries across the entire year.]* *[Verification: Cibrian et al. (2022) — tangible feedback for ADHD self-regulation, via the non-human-mediator framing the master document's §3.6 establishes.]*

---

### Milestone 2 — Upload your first sketch

**What the student does.** Opens the pre-written sketch `01_blink_L_fast.ino` from the project folder. Clicks the Upload button (the right-arrow icon in the Arduino IDE toolbar). Watches the progress bar at the bottom of the IDE. When upload completes successfully, the "L" LED on the Arduino now blinks at a **faster** rate than the factory sketch — about three times per second instead of one.

**Done when.** The "L" LED is blinking faster than before, AND the Arduino IDE shows a green "Done uploading" message at the bottom.

**Why this milestone exists.** First Upload click. This is the moment the student learns that "code" is a thing they can change — a sketch in a file becomes behaviour on the hardware. The pre-written sketch is intentionally trivial (just a faster blink rate) so the student's first Upload click cannot fail in a confusing way. The difference between the factory blink and the new blink is visible immediately.

**Channel A Level 1 note.** The student opens `01_blink_L_fast.ino` with `File → Open` in the Arduino IDE, or by double-clicking the file in Windows Explorer. The sketch compiles in 3–5 seconds and uploads in another 3–5 seconds on a typical Arduino Uno.

**Channel B note.** Students using Channel B hear: *"Claude, I'm on Project 1, Tier 1, Milestone 2."* Claude walks them through opening the sketch, pressing Upload, and watching the LED.

**Research basis (teacher-facing).** *[Verification: Principle 2 — task-card-is-the-boss. The student is not being asked to write code; they are being asked to click Upload. The code is external scaffolding (Rosen, Boyle, Cariss & Forchelli 2014 on external cognitive scaffolds for students with learning disabilities) and the upload action is the student's entire agency here.]*

---

### Milestone 3 — Wire your first external LED

**What the student does.** Picks one LED from the parts tray and notices the legs are different lengths — the **long leg is positive (anode)** and the **short leg is negative (cathode)**. Plants the LED across two rows of the breadboard so the legs are in different rows (not shorted together). Connects the long leg (anode) to breadboard pin 9 via a 220 Ω resistor (picks a resistor with red-red-brown colour bands from the parts tray). Connects the short leg (cathode) to the Arduino's GND via a jumper wire.

**Done when.** The LED is in the breadboard with the long leg going through the resistor to the Arduino's pin 9, and the short leg going to the Arduino's GND. *The LED is not lit yet — the sketch for this wiring comes at Milestone 4.*

**Why this milestone exists.** First breadboard wiring. The student builds the physical circuit before running any code (Principle 3 — physical-first, then abstract). The wiring reference card at the station shows exactly this circuit with a labelled diagram; the student mirrors it.

**Common stuck moments (teacher-facing).** (a) LED in backwards — the long leg must go to pin 9 via the resistor, not to GND. If the student wires it backwards, the sketch at Milestone 4 will upload successfully but the LED will not light. The teacher rotates during or right after this milestone and checks. (b) Resistor not in series with the LED — if the resistor is not between pin 9 and the LED's long leg, the LED can draw too much current and burn out. Every wiring reference card shows the resistor in the correct position. (c) LED legs shorted to each other via the breadboard — the student puts both LED legs in the same horizontal row, which shorts them. The reference card shows the two legs in different rows.

**Channel A Level 1 note.** No sketch at this milestone. Pure hardware.

**Channel B note.** Channel B is particularly valuable here — a student who finds the wiring reference card overwhelming can invoke Claude with *"Walk me through wiring an LED to pin 9"* and get step-by-step conversational guidance. The teacher rotates to confirm the wiring is correct before the student moves to Milestone 4.

**Research basis (teacher-facing).** *[Verification: Principle 3 (physical-first / concrete-before-abstract) — Hwang & Taylor (2016)'s CRA sequence for students with disabilities in STEM. The student handles the physical LED and the physical resistor before any code about them exists in their world. Also [Verification: Israel et al. (2015) — scaffolded explicit instruction supports students with disabilities in computational-thinking contexts.]*]

---

### Milestone 4 — Upload the second sketch and light up the LED

**What the student does.** Opens `02_blink_external.ino` from the project folder. Clicks Upload. Watches the breadboard — the external LED they just wired now blinks on and off about once per second. If it does not blink, the student runs the **stuck protocol** (re-check wiring, reference card, Claude Code, call teacher).

**Done when.** The external LED on the breadboard is blinking. Student has achieved *something I wired lit up because of code I uploaded*.

**Why this milestone exists.** The closing of the hardware–software loop. Milestone 3 built the circuit without proving it works; Milestone 4 proves it works. This is the most important single moment in Project 1 — from here on the student knows they can make physical things happen by pressing Upload.

**Channel A Level 1 note.** Pre-written sketch. The student does not modify it.

**Channel B note.** If the LED doesn't light, Channel B walks the student through the debugging checklist (orientation, resistor position, pin number, USB connection). The Channel B scaffold for Milestone 4 specifically handles the "my LED is not blinking" case because that is the most common first-wiring failure mode.

**Teacher rotation checkpoint.** The teacher rotates to every Tier 1 student at Milestone 4. This is the project's first "does the student's circuit actually work" moment, and a quick confirmation from the teacher — *"yes, your LED is blinking, that's exactly right"* — is worth more at this moment than any task card. Principle 8 in action.

**Research basis (teacher-facing).** *[Verification: Principle 3 — physical-first; Principle 4 — visible win after a short cycle of work; Principle 8 — the teacher rotation check-in is the relational anchor for a potentially emotional moment (student's first successful upload on their own wiring).]*

---

### Milestone 5 — Add a second LED

**What the student does.** Picks a second LED of a **different colour** from the parts tray (if the first was red, pick green or yellow; any combination is fine). Wires it to pin 10 with its own 220 Ω resistor, mirroring the first LED's wiring but one row over. The student does not upload anything at this milestone — they only add hardware.

**Done when.** The second LED is wired in the breadboard next to the first LED, both legs in the correct orientation (long leg → resistor → pin 10, short leg → GND), and both LEDs ready for the next sketch.

**Why this milestone exists.** Reinforces the wiring pattern from Milestone 3 in a lower-stakes context — the student has already done this once, and now they're doing it again. Second wiring successes build confidence in the student's own hands. Principle 4 visible-win pattern plus a second data point for the student's self-belief.

**Claude Code notes.** Channel A Level 1 — no code change. Channel B can walk a student through the mirroring if they need it.

**Research basis (teacher-facing).** *[Verification: Principle 4 — "each milestone produces a tangible result" (Rosen et al. 2014 on scaffolded practice; Smith et al. 2020 on extrinsic support structuring outcomes for ADHD adolescents).]*

---

### Milestone 6 — Upload the alternating-blink sketch

**What the student does.** Opens `03_blink_alternating.ino`. Clicks Upload. Watches — the two LEDs now blink in an alternating pattern. When the first LED is on, the second LED is off, and vice versa. About once per second.

**Done when.** Both LEDs are blinking in alternation.

**Why this milestone exists.** First multi-output Arduino behaviour. The student now sees two independent things on the same Arduino controlled by the same sketch. This is the "code can do more than one thing at a time" moment.

**Channel A Level 1 note.** Pre-written sketch, no modification required. A Tier 1 student who is curious can now peek at the code in the IDE and see that two `digitalWrite()` calls exist — one for pin 9, one for pin 10, with a `delay()` between them. The student is not required to understand this, only to observe it if they want.

**Channel B note.** Channel B can explain the alternation mechanism conversationally if a student asks *"why are they alternating?"* — this is the first moment a Tier 1 student might voluntarily ask a conceptual question, and Channel B is the right place to answer it without the teacher having to stop rotation.

**Research basis (teacher-facing).** *[Verification: Principle 4 — visible win with an added dimension of complexity.]*

---

### Milestone 7 — Wire the push-button

**What the student does.** Adds the tactile push-button to the breadboard. The button straddles the centre gap of the breadboard so the four pins land in four different rows. Connects one side of the button to the Arduino's **5 V** rail via a jumper wire. Connects the other side of the button to **pin 2** (digital input) AND to **GND** via a 10 kΩ pull-down resistor (brown-black-orange colour bands). The pull-down resistor ensures pin 2 reads **LOW** when the button is not pressed and **HIGH** when the button is pressed.

**Done when.** The button is in the breadboard with 5 V on one side, pin 2 + 10 kΩ → GND on the other side. *The button does not do anything yet — the sketch at Milestone 8 tells the Arduino what to do when the button is pressed.*

**Why this milestone exists.** First digital-input wiring. The concept of "the Arduino reads something" is new at this milestone. Until now the Arduino has been the active element; now it is also a listener. The pull-down resistor is the trickiest single component to understand in Project 1, and the reference card handles it with a diagram rather than explanation.

**Common stuck moments (teacher-facing).** (a) The pull-down resistor is on the wrong side of the button — goes from 5 V to GND instead of from pin 2 to GND. This creates a short circuit when the button is pressed; the Arduino will brown-out. Every reference card shows the correct layout. (b) The button straddling is wrong — students sometimes put all four pins in the same row by laying the button flat. The button must span the breadboard centre gap. (c) Pin 2 is accidentally wired to GND directly without going through the resistor — this gives the student a constantly-LOW reading and the button appears broken.

**Teacher rotation checkpoint.** The teacher rotates to every student at Milestone 7 to visually check the pull-down wiring. This is the most common failure point in Project 1 and the one most likely to discourage a Tier 1 student if not caught quickly.

**Research basis (teacher-facing).** *[Verification: Principle 3 — physical-first; Principle 8 — teacher rotation as the relational safety net at the project's hardest wiring moment.]*

---

### Milestone 8 — Upload the button-controlled sketch

**What the student does.** Opens `04_button_control.ino`. Clicks Upload. Presses the button. When the button is not pressed, **one LED is on**. When the button is pressed and held, **the other LED is on**. Releasing the button returns to the first LED.

**Done when.** Pressing and releasing the button reliably switches which LED is lit.

**Why this milestone exists.** Project 1 closes with the student's first interactive Arduino behaviour. The student's *input* (button press) changes the Arduino's *output* (which LED is on). This is the foundation every subsequent project will build on — every interactive Arduino project is a loop of read-input-decide-write-output, and Milestone 8 is the student's first experience of that loop.

**Celebration.** At this milestone, the student has:
- Wired a breadboard from scratch.
- Uploaded four sketches.
- Built an interactive circuit with LEDs and a button.
- Completed the first project in the program.

The teacher's job at this milestone is to **celebrate visibly**. *"You made an Arduino circuit respond to a button. That's real electrical engineering, and you did it on your first project."* Take a photo for the student's portfolio (with their permission). Update the tracking sheet row (§5.8). Ask the student what they want to build on their next session — and listen to the answer, even if it means starting Project 3 out of order (§5.7 refusal-of-order protocol).

**Channel A Level 1 note.** Pre-written sketch. A Tier 2 student on their second session would use Channel A Level 2 at this milestone to modify the sketch so the button does something else (cycles through patterns, toggles instead of holds, etc.) — but Tier 1 closes with the pre-written version and the celebration.

**Research basis (teacher-facing).** *[Verification: Principle 4 — the closing visible win is the full interactive circuit; Principle 8 — the teacher celebration is the relational close-out; Principle 5 — asking the student what they want to build next is the autonomy signal that carries into Project 2 or wherever they decide to go next. Also [Verification: the Sciacca (2025) "zero percent head down rate during that PjBL week" quote from S.F. — engagement at Project 1 Milestone 8 is exactly the pattern the three-teacher case study reports practitioners seeing.]*]

---

## Tier 2 — Guided Design (5 milestones with choice points)

**Who this tier is for.** Students who have either (a) completed a Tier 1 project before and want more control, or (b) arrived with some prior Arduino experience and would be bored at Tier 1, or (c) simply want to design something more than copy it. A Tier 2 student at Project 1 is a student making genuine design decisions for the first time in the workshop.

**Claude Code usage at Tier 2.** Mix of Channel A Level 1 (starter sketches) and Channel A Level 2 (modify the starter sketch with Claude Code's help to match the student's chosen pattern). Channel B available throughout. The student's first Level 2 Claude Code interaction happens at Milestone 3 below.

**Task card count.** Five milestones, five task cards. Choice points explicit on each card.

### Tier 2 Milestone 1 — Start-up (combined Tier 1 Milestones 1–4)

**What the student does.** Exactly what Tier 1 Milestones 1–4 describe, compressed into a single card: plug in the Arduino, upload the starter sketch, wire the first LED, upload and confirm it lights. *A Tier 2 student moves through this in 15–20 minutes; a Tier 1 student took 4 cards and ~45 minutes. That is the whole point of the tier difference.*

**Done when.** One external LED wired to pin 9 and blinking from the starter sketch.

### Tier 2 Milestone 2 — Pick your pattern

**What the student does.** Looks at the **pattern choice card** and picks one of three patterns:

- **Pattern A — Alternating.** Two LEDs blinking in opposition (same as Tier 1 Milestone 6).
- **Pattern B — Chasing.** Three LEDs lighting up in sequence, like a chase light on a sign. Each LED lights for 200 ms then the next. The student wires a third LED for this option.
- **Pattern C — Breathing.** One LED fading smoothly in and out using PWM (pulse-width modulation on pin 9 or 10). The student adds a second LED only if they want a second breathing light.

The student picks one, wires any additional LEDs needed for their choice, and moves to Milestone 3.

**Done when.** The hardware is wired for the student's chosen pattern and the student has written their choice (A / B / C) on the task card.

**Why a choice here.** Principle 5 — autonomy at the first possible moment after the student has seen one thing work. Until now the student had no choices (Tier 1 is intentionally choice-free to maximize success); the first Tier 2 choice comes at Milestone 2 after they have already uploaded a sketch successfully.

### Tier 2 Milestone 3 — First Claude Code Level 2 interaction

**What the student does.** Opens the relevant starter sketch for their chosen pattern (`T2_alternating_starter.ino`, `T2_chasing_starter.ino`, or `T2_breathing_starter.ino`). Opens Claude Code in the browser tab.

Then, **following the Channel A Level 2 discipline** (Principle 7), the student fills in three things **on the task card before sending any prompt to Claude**:

- *(a) What I want to happen:* [the student writes the behaviour they want — for example, *"I want the two LEDs to alternate twice as fast, so about 2 times per second instead of 1 time per second"*]
- *(b) What's currently happening:* [the student writes the current behaviour — *"right now they alternate once per second"*]
- *(c) What I've tried:* [the student writes what they have already thought about or looked at — *"I looked at the delay() lines in the code"*]

The student then composes a prompt from these three pieces, pastes the current code, and sends the prompt to Claude Code. Claude responds with the specific line(s) to change. The student makes the change, clicks Upload, and tests.

**Done when.** The student has successfully modified the sketch with Claude Code's help and their LEDs are now behaving differently than they did with the starter sketch.

**Why this milestone exists.** It is the student's first experience of Channel A Level 2 — using Claude Code as a pair programmer rather than as a code dispenser. The "describe the problem first" discipline on the task card is non-negotiable because it is the specific mechanism Principle 7's evidence base (our inference from Morsink 2022's SDT framing) predicts is necessary to preserve student agency. A student who skips (a)(b)(c) and just pastes code into Claude saying *"make this faster"* is using Claude Code as an extrinsic reward machine — which is what Principle 7's design explicitly tries to avoid.

**Channel B note at Tier 2.** Channel B is still available at Tier 2 for students who want the conversational walk-through of the printed card, but Channel A Level 2 is the dominant interaction mode at this milestone.

**Research basis (teacher-facing).** *[Verification: Principle 7 three-level model; Morsink et al. 2022 self-determination theory framing (the program's design inference, not Morsink's own findings); Rosen 2014 on external cognitive scaffolds.]*

### Tier 2 Milestone 4 — Add the button, pick its behaviour

**What the student does.** Wires the push-button and the 10 kΩ pull-down resistor (same as Tier 1 Milestone 7). Then picks one of three button behaviours:

- **Behaviour A — Toggle.** Pressing the button toggles the pattern on/off. Press once = LEDs start; press again = LEDs stop.
- **Behaviour B — Cycle.** Pressing the button cycles through the three patterns (A → B → C → A again).
- **Behaviour C — Speed control.** Pressing the button speeds up the pattern by 50%; releasing brings it back to normal speed.

Student uses Claude Code Level 2 again to modify the sketch to match their chosen behaviour, following the same (a)(b)(c) discipline.

**Done when.** The button is wired, the sketch is modified, the button does what the student chose.

### Tier 2 Milestone 5 — Signature pattern and show-off

**What the student does.** Picks a "signature pattern" — a final combination of pattern + button behaviour + colours that the student wants to demonstrate. This is where the student's own taste enters the project for the first time. The student might say *"I want red and yellow, chasing pattern, and when I hold the button it gets faster"* — and then uses Claude Code Level 2 to generate the exact sketch for that combination.

**Done when.** The student shows their signature pattern to the teacher (or, if the student wants, to a peer at the next workstation). The teacher takes a photo for the student's portfolio and celebrates.

**Research basis (teacher-facing).** *[Verification: Principle 5 — fully-expressed autonomy at the Tier 2 close-out; Sciacca (2025) student agency and ownership sub-theme — "it gives them more ownership of their learning" (B.Q.), "by offering choices within the project, this boosted their sense of control" (M.G.).]*

---

## Tier 3 — Open Design (one-page project planner)

**Who this tier is for.** Students who have either completed Tier 2 of at least one prior project, or who arrive at Project 1 with prior Arduino experience, or who explicitly ask for open design. Tier 3 at Project 1 is rare — most students reach Tier 3 by Project 3 or 4 at the earliest. When it does happen, Tier 3 at Project 1 is usually the student designing a specific use case (a mood light for their bedroom, a signal light for their bike, a Morse-code sender, a two-LED "traffic light" with a button to cycle through states).

**Claude Code usage at Tier 3.** Channel A Level 3 — free dialogue. The student describes what they are trying to build, shows Claude Code any code they have written, and iterates. The discipline is the same as Level 2 ("(a) what I want, (b) what's happening, (c) what I've tried") but the student's "what I want" statements are open-ended and the student's iterations are driven by their own taste and judgment.

**Deliverable.** A single-page **project planner** (see `tier3_planner.html` when generated) with five phases the student fills in themselves:

- **PLAN** — what is the light pattern going to be? Sketch it on paper. What colours? What inputs (button, nothing, or multiple buttons)? What behaviour? Who is it for?
- **BUILD** — wire the LEDs, resistors, button(s) on the breadboard. Take a photo when done.
- **CODE** — use Claude Code Level 3 to generate the sketch from the student's description. Upload and test. Iterate.
- **TEST** — does it do what the student planned? If not, what is different? Iterate until the student is satisfied (not until it matches the plan — the plan can change, and often should).
- **SHOW** — show the finished project to the teacher, to a peer, or (with the student's permission) photograph it for the student's at-home portfolio.

The project planner is a single sheet because Tier 3 is about the student's own structure, not about following more cards.

---

## Claude Code integration — operational detail

**Channel A — Pair programmer.**

*Level 1 — Pre-written sketch upload.* The student opens a `.ino` file and clicks Upload. No code writing, no modification, no dialogue. The pre-written sketches for Project 1 are:

- `01_blink_L_fast.ino` — blinks the built-in L LED faster than the factory sketch. Used at Tier 1 Milestone 2.
- `02_blink_external.ino` — blinks the LED on pin 9. Used at Tier 1 Milestone 4.
- `03_blink_alternating.ino` — alternates pins 9 and 10. Used at Tier 1 Milestone 6.
- `04_button_control.ino` — button on pin 2 switches between pins 9 and 10. Used at Tier 1 Milestone 8.
- `T2_alternating_starter.ino`, `T2_chasing_starter.ino`, `T2_breathing_starter.ino` — Tier 2 starter sketches, one per pattern choice.

*Level 2 — Modify with Claude Code's help.* First introduced at Tier 2 Milestone 3. The student fills in (a)(b)(c) on the task card, sends a prompt to Claude Code including the current code, reads Claude's response, makes the change in the IDE, uploads, and tests. The task card's comprehension-check prompt at Level 2 is: *"After Claude helped you, can you explain in one sentence what changed?"*

*Level 3 — Free dialogue.* Used only at Tier 3. The student opens an open-ended conversation with Claude Code to design, refine, and iterate on their signature pattern. No pre-written sketch at Tier 3 — the student and Claude build the code together from the student's description.

**Channel B — Scaffolded tutorial.**

Channel B is available at any tier and any milestone. The student invokes it by saying to Claude Code: *"I'm on Project 1, Tier X, Milestone Y. Walk me through it."* Claude responds with the card's content in conversational form, asks a checkpoint question, and waits for the student to confirm the step is done before moving to the next.

The Channel B tutorial-channel scaffold for Project 1 lives in `claude_code_tutorial_scaffold.md` (generated separately). The scaffold is a short system prompt that primes Claude to deliver Project 1's content conversationally, plus per-milestone invocation templates the student can copy-paste if they prefer not to improvise.

**A Tier 1 student who uses Channel B** for every milestone never types a word of code to Claude Code. They hear the task cards walked through and confirm each step. This is a genuinely supported path through Project 1 for students who find printed instructions overwhelming.

**A Tier 3 student** typically does not use Channel B — they skip straight to Channel A Level 3 free dialogue — but Channel B is available if they want to return to it on a hard day.

---

## Safety notes (Project 1 specific)

Project 1 has the **lowest safety envelope of any project in the program**. No soldering, no moving parts, no batteries, no motors. The only active risks are:

1. **Shorting 5 V to GND directly.** If the student accidentally wires 5 V directly to GND (for example, via a jumper wire), the Arduino's onboard regulator briefly protects itself and then the board may reset or turn off. The fix is simply to remove the offending wire. No permanent damage to the board in almost all cases.
2. **Plugging the LED directly into 5 V without a resistor.** An LED at 5 V with no current-limiting resistor draws too much current, gets hot, and burns out in a few seconds. The wiring reference card and every task card mention the resistor explicitly. If a student reports *"my LED got really bright and then stopped working,"* that is the usual cause. Replace the LED and add the resistor.
3. **USB connector damage.** Plugging the USB cable in upside down or forcing it. The USB-B side of the cable has a clear orientation; the USB-A side on the PC is universal. If the student reports the cable won't go in, they are almost certainly trying the wrong orientation on the USB-B side.

**None of these are injury risks.** Project 1's safety discipline is primarily "don't burn out an LED or reset the board." Actual student-injury risks (soldering, LiPo batteries, propellers) come at Project 4 and Project 8 respectively.

**What the student is told about safety at Project 1.** Short version: *"the Arduino runs on 5 volts, which is too low to hurt you, but you can burn out an LED or confuse the board by wiring it wrong. If something stops working, stop pressing buttons and call the teacher — we'll figure out what happened."* The long version is on the safety reminder reference card.

---

## Teacher troubleshooting crib sheet (for the Teacher Troubleshooting artifact)

The most common failure modes in Project 1, in rough frequency order, with the fix:

1. **LED doesn't light at Milestone 4.** Usual cause: LED wired backwards (long leg to GND instead of pin 9). Fix: flip the LED. If that doesn't fix it, check that the resistor is actually in series with the LED and not just stuck in the breadboard unused. *[Verification: Berrezueta-Guzmán et al. 2021's non-human-mediator framing — the wiring reference card catches ~60% of these before the teacher needs to rotate.]*

2. **Arduino IDE shows "Arduino not found" or "no COM port" on Upload.** Usual cause: wrong COM port selected (Tools → Port → COMx). Fix: scroll through the available ports and pick the one that appeared when the Arduino was plugged in. If no new port appears, the USB cable may be a "charge-only" cable with no data lines; swap it for a proper data cable.

3. **Upload says "avrdude: stk500_getsync()" error.** Usual cause: the board is selected correctly but another program (Serial Monitor, or another instance of the IDE) has the COM port locked. Fix: close Serial Monitor, close any extra IDE windows, try Upload again.

4. **Button doesn't do anything at Milestone 8.** Usual cause: pull-down resistor on the wrong side (5 V → GND instead of pin 2 → GND). Fix: move the resistor so it is between pin 2 and GND, not between 5 V and GND. See the wiring reference card. *[Verification: Principle 3 physical-first + Principle 2 task-card-is-boss — the reference card catches most of these without teacher intervention.]*

5. **Both LEDs stay on all the time after Milestone 6.** Usual cause: one of the LEDs is wired to 5 V instead of to a pin. Fix: re-check the wiring against the reference card; both LEDs should go to pin 9 and pin 10, not to 5 V.

6. **Arduino resets or turns off repeatedly.** Usual cause: short circuit somewhere — usually a jumper wire bridging 5 V to GND accidentally, or a button wired without the pull-down resistor so pressing the button shorts 5 V to GND. Fix: disconnect the USB, check wiring, fix the short, reconnect.

7. **Student says "my sketch is the same as the reference but it doesn't work."** Usual cause: the student opened the sketch but did not click Upload, or the Upload silently failed. Fix: click Upload and watch for the green "Done uploading" message at the bottom of the IDE. If there is no green message, there is a compile error — read the red text.

8. **Student's LED lit up brightly for a moment then stopped.** Usual cause: LED wired without a current-limiting resistor, burned out. Fix: replace the LED from the parts library, add the 220 Ω resistor, re-wire, retry.

---

## What this source file is not

This file is the **teacher-facing source of truth** for Project 1. It is not:

- **A student-facing document.** Students see the task cards, reference cards, HTML tutorial, and Channel B tutorial-channel scaffold — all generated from this file. Students do not read this source file.
- **A published curriculum artifact.** This file is internal to the Agourim workshop production process and is the single document from which all Project 1 student-facing materials are generated. If any content here conflicts with what a student sees, the student-facing artifact wins at session time and this source file is updated afterwards.
- **A comprehensive Arduino tutorial.** It covers only what Project 1 needs. A student who wants to learn more about Arduino in general is pointed at external resources by the teacher during rotation check-ins.

The generated artifacts from this source file will live alongside it in `Arduino_Projects/Project_1_Light_Signals/` once Phase D.1 step (c) (artifact generation) is executed.

---

*End of Arduino Project 1 — Light Signals source file. Ready for review.*
