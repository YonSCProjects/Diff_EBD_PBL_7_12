# Project 9 — The Personal Mouse (עכבר אישי)

*Ninth project of the programme, and its first fully personal one: a computer mouse designed
around one student's own hand, built from the parts already ordered for it.*
*Source material — the teacher's design folder at `C:\RoboticsWorkshopTeachnPlay\Mouse project`
(plan, wiring guides, visual build guide, BOM, order checklist, three Hebrew mini-tutorials).
The Hebrew navigation cards are generated from this document.*

**Version 1.0 — authored 2026-09-07 from the design folder; technical-accuracy and safety
review passes run during authoring. Sketches not compile-tested (no ESP32 core on the
authoring machine) — same standing caveat as Project 8.**

## Read this first — locked hardware decisions

Ground truth is the **February 2026 order** (`Order_Tracking_Checklist.md`) — what was
actually bought outranks every earlier plan page:

- **MCU: ESP32-S3 DevKitC-1 N8R2, 44-pin** — the board the wiring guides assume; one was
  bought. (Four ESP32-S3 *Mini* boards with expansion boards were also bought — spares, and
  the future 2.4 GHz dongle. They are not the build board.)
- **Sensor: PixArt PMW3360DM-T2QU module with LM19 lens** — SPI, 3.3V. The mouse's eye.
- **Rollers: two Kailh mouse encoders** — 11 mm front (scroll + middle-click push), 9 mm
  rear (the speed roller; its push toggles the side-button function layer). Never generic
  EC11 — the docs are explicit that EC11 fails under continuous scrolling.
- **Main clicks: Kailh GM 8.0 switches — these are the ones bought, and they are clicky,
  not silent.** The plan wanted GM 2.0 Silent; the order says GM 8.0. The cards describe
  the real switches and never promise quiet clicks. (Foam dampening or a GM 2.0 reorder is
  a future option, documented in the folder.)
- **Side buttons: 3× 6×6×5 mm tactile switches.** Rear-roller push toggles their layer.
- **Battery: protected NCR18650B 3400 mAh** in a spring holder (protected cells run ~68 mm —
  the holder must take that). **TP4056 USB-C module with DW01A+8205A protection** charges it.
  **SS12F15 slide switch** is the main power switch.
- **Indicator LEDs: 5 mm LEDs from workshop stock + 330Ω from the bought THT resistor kit.**
  The order contains only 0603 SMD LEDs and SMD resistors — hand-soldering 0603 is not a
  student task in this workshop. The SMD parts wait for a future PCB revision. 3× DPI level
  + 1× layer.
- **Boost: MT3608 from workshop stock (Project 8 spares), pre-tuned to 5.0V** — see
  correction 2 below. None was bought for this project; the workshop has them.
- **PTFE film (bought, 3 sheets)** for glide rails — the mouse must work on a mattress.
  Shell, wheels and fastening hardware were *not* bought yet; the shell is a Tier-2 design
  activity and a planner extension, not a Tier-1 build step.

## Corrections to the source folder (deliberate, evidence-based)

1. **The control-pin map was re-assigned.** The folder's map (buttons on GPIO 25–26, sides
   on 32–34, LEDs on 27–29) is classic-ESP32 numbering that is invalid on an S3: GPIO 22–25
   do not exist, 26–32 are the flash pins, 19/20 are the native USB pair that USB-HID needs,
   0/3/45/46 are straps. The sensor pins were **kept exactly** (CS 10, MOSI 11, SCK 12,
   MISO 13, MOTION 14 — they are the S3's default SPI pins). Everything else moved to valid
   free pins — the full map is below and in `ino_files/pins.h`.
2. **AMS1117-3.3 removed from the battery path.** Its ~1.1V dropout needs ≥4.4V in; a
   Li-ion spends most of its life at 4.2–3.4V, so the planned battery→LDO rail browns out.
   The folder's own boost-converter tutorial teaches exactly this flaw *for this mouse*.
   The build uses the Project 8 power pattern instead: **battery → TP4056 (load on OUT± for
   load-sharing) → slide switch → MT3608 boost pre-tuned to 5.0V → the DevKit's 5V pin**;
   the sensor and every 3.3V peripheral feed from the DevKit's 3V3 output. The bought
   AMS1117 modules stay in the drawer, with this note as the reason.
3. **Wireless in the cards is Bluetooth.** The 2.4 GHz dongle mode needs a second board
   flashed as a receiver — real, but an extension: the spare S3 Minis make it a natural
   Tier-3 planner project, not a core milestone.
4. **Tier 1 wires on a breadboard with jumpers, not JST harnesses.** The folder's 8-harness
   JST architecture belongs to the final shell build; its own simplified guide (Dec 2025)
   already walks this back for beginners. Crimping comes later; the electronics come first.
5. **Rear-roller push = layer toggle** (the plan overview's and BOM's definition). The
   firmware plan's alternative meanings (favourite-DPI toggle, long-press modes) are Tier-2
   material for the student to choose with Claude Code.

## Pin map (final — ESP32-S3 DevKitC-1)

| function | GPIO | | function | GPIO |
|---|---|---|---|---|
| PMW3360 CS | 10 | | Rear roller A | 15 |
| PMW3360 MOSI | 11 | | Rear roller B | 16 |
| PMW3360 SCK | 12 | | Rear roller push (layer) | 17 |
| PMW3360 MISO | 13 | | Side S1 / S2 / S3 | 7 / 8 / 9 |
| PMW3360 MOTION | 14 | | LED DPI 1 / 2 / 3 | 39 / 40 / 41 |
| Left / Right click | 1 / 2 | | LED layer | 42 |
| Front encoder A / B | 4 / 5 | | Front encoder push (middle) | 6 |

All buttons and encoder contacts switch to GND with internal pull-ups. LEDs through 330Ω.
Free for the future: 18, 21, 38, 47.

## Safety (the short line every card's footer carries)

**מלחימים רק כשהמורה ליד, לא נוגעים בקצה המתכת של המלחם — והסוללה נכנסת אחרונה, אחרי שהמורה בדק.**

Full rules live on reference card R1 (`reference_cards_he/R1_battery_soldering_safety_he.dc.html`,
the Project 8 pattern — task-card footers cite R1): the three soldering rules (identical
to Projects 4 and 8), plus the 18650 rules — only the protected cell, never below 3.0V,
charge only on the protected TP4056, polarity checked by the teacher before first
insertion, stored at half charge, and a battery that is hot, swollen or dented goes to
the teacher immediately. No propellers, no goggles — the hazards here are one hot iron
and one lithium cell.

## Tier 1 — building the mouse (12 milestones)

### Milestone 1 — Meet the parts (together milestone)
**Goal.** Every part of the future mouse in the student's hand; the safety agreement.
**Steps.** (1) Tray tour, part by part, naming each aloud: the S3 board, the sensor with
its lens ("the eye"), the two rollers (spin them — feel the detents), a GM 8.0 switch
(click it), the tactile side buttons, the 18650 and its holder — the teacher shows the
battery, hands over everything else. (2) Spin each encoder and count clicks per turn.
(3) Read the three soldering rules + the battery rules from R1 aloud with the teacher.
(4) Sign the safety agreement; the battery stays with the teacher until Milestone 10.
**Expected result.** A tray of named parts and a signed agreement; nothing is wired.
**Done when.** The student can point at any part and name it; the agreement is signed.
**Stuck.** קוראים למורה.

### Milestone 2 — The board is alive
**Goal.** The ESP32-S3 blinks; the project folder exists.
**Steps.** (1) Press the S3 board into the breadboard across the centre channel (like the
ESP32 in Projects 5–6). (2) USB-C cable to the computer. (3) Open `00_hello_blink` in the
Arduino IDE, board "ESP32S3 Dev Module", upload. If upload will not start: hold BOOT, tap
RESET, release, retry — this is the S3 ritual, it appears on the card. (4) Onboard RGB
blinks green-blue-orange. (5) Only after the blink: create the project folder in Drive
and point Claude Code at it (hardware first, folders second — the programme rule).
**Expected result.** The little onboard LED cycles three colours.
**Done when.** Blink runs, folder exists, Claude Code works in it.
**Stuck.** קוראים למורה.

### Milestone 3 — The first click  *(figure: w_p9_01)*
**Goal.** The board becomes a real USB mouse with two clicking switches.
**Steps.** (1) Two GM 8.0 switches on the breadboard; each: one leg to its GPIO (left 1,
right 2), the other to GND. (2) IDE: USB Mode = "USB-OTG (TinyUSB)" — the setting that
turns the board into a device. (3) Upload `01_click_test`. (4) The computer now lists a
new mouse; pressing the left switch clicks whatever the cursor is on. (5) Note the serial
port may vanish while the sketch runs — normal for a board that became a mouse;
BOOT+RESET brings upload mode back.
**Expected result.** Clicking a bare switch on a breadboard clicks on screen.
**Done when.** Both switches click; the student has clicked something real with them.
**Stuck.** קוראים למורה.

### Milestone 4 — The eye  *(figure: w_p9_02)*
**Goal.** The PMW3360 wired — the most delicate wiring of the project.
**Steps.** (1) Sensor module into the breadboard, lens down, over the board's edge so the
lens sees the desk. (2) Seven jumpers, checked one by one against the figure: VCC→3V3,
GND→GND, MOSI→11, MISO→13, SCK→12, CS→10, MOTION→14. Short and tidy — this is an SPI bus.
(3) Nothing uploads yet; wiring is checked against the figure, wire by wire, before power.
**Expected result.** Seven wires matching the figure exactly; teacher check.
**Done when.** Every wire traced with a finger against the figure; teacher approved.
**Stuck.** קוראים למורה.

### Milestone 5 — The cursor moves
**Goal.** The sensor drives the cursor — the mouse's magic moment.
**Steps.** (1) Claude Code installs the "PMW3360 Module" library (SunjunKim). (2) Upload
`02_sensor_test`. (3) Slide the breadboard over a mousepad: the cursor follows. (4) Try
the mattress/blanket surface — the reason this mouse exists — and see how it behaves.
(5) If the cursor is dead: the card's stuck box points to the J1 wires and the library.
**Expected result.** Moving the board moves the cursor, even on fabric.
**Done when.** Cursor follows on both a pad and a soft surface.
**Stuck.** בודקים את שבעת החוטים מול האיור, חוט אחרי חוט. לא זז — קוראים למורה.

### Milestone 6 — The scroll wheel  *(figure: w_p9_03)*
**Goal.** Front 11 mm roller scrolls; its push is the middle click.
**Steps.** (1) Front encoder into the breadboard: A→4, B→5, push→6, common→GND.
(2) Upload `03_basic_mouse`. (3) Turn the shaft with a finger — a page scrolls; push —
middle click. (4) The whole basic mouse now works: clicks, cursor, scroll.
**Expected result.** A page scrolls one step per detent, both directions.
**Done when.** Scroll both ways + middle click work alongside clicks and cursor.
**Stuck.** קוראים למורה.

### Milestone 7 — The speed roller  *(figure: w_p9_04)*
**Goal.** The project's signature: the rear 9 mm roller changes cursor speed live, three
LEDs show the level.
**Steps.** (1) Rear encoder: A→15, B→16, push→17, common→GND. (2) Three 5 mm LEDs: long
leg via 330Ω to 39/40/41, short legs to GND. (3) Upload `04_dpi_roller`. (4) Turn the
rear roller: the cursor speed steps 400→800→1600 and the lit LED moves with it. (5) Find
the speed that fits your hand today — it becomes your default in Tier 2.
**Expected result.** Speed changes while moving the cursor; LEDs track the level.
**Done when.** All three levels reachable both ways; each level's LED lights alone.
**Stuck.** לד לא מאיר — בודקים את כיוון הרגליים שלו. קוראים למורה.

### Milestone 8 — Side buttons and the layer  *(figure: w_p9_05)*
**Goal.** The full wired mouse: three thumb buttons plus the function layer.
**Steps.** (1) Three tactile switches: S1→7, S2→8, S3→9, other legs GND. (2) Layer LED:
long leg via 330Ω→42. (3) Upload `05_full_wired`. (4) Base layer: S1=back, S2=forward,
S3=middle. (5) Push the rear roller: the layer LED lights and the same buttons become
drag-lock, double-click and speed-step. Push again — back.
**Expected result.** Seven buttons, two rollers, four LEDs — everything answers.
**Done when.** Every control does its job in both layers; the layer LED tells the truth.
**Stuck.** קוראים למורה.

### Milestone 9 — Soldering the power board (together milestone)  *(figure: w_p9_06)*
**Goal.** The battery board: TP4056, holder, switch and boost soldered to perfboard.
**Steps.** (1) Say the three soldering rules aloud; iron on when the teacher is beside
you. (2) Solder in this order, testing after each: battery holder leads → TP4056 B±;
TP4056 OUT+ → switch → MT3608 IN+; TP4056 OUT− → MT3608 IN−; MT3608 OUT± → a JST tail
for the S3's 5V/GND. (3) Heat-shrink every joint. (4) The teacher checks the MT3608 is
pre-tuned to 5.0V with the multimeter — before anything connects to the S3. NO battery
in the holder yet.
**Expected result.** One tidy power board, joints shiny, output measuring 5.0V (teacher,
with a bench supply on the input).
**Done when.** Teacher measured 5.0V at the output tail; polarity double-checked.
**Stuck.** בהלחמה — קוראים למורה, תמיד.

### Milestone 10 — Battery day (together milestone)
**Goal.** The battery goes in for the first time; charging works.
**Steps.** (1) The teacher hands over the 18650 and checks polarity against the holder
markings together with the student. (2) Cell into the holder, switch OFF. (3) USB-C into
the TP4056: red LED = charging, blue/green = full. (4) Switch ON: the S3's power LED
lights from the battery — no computer cable. (5) Switch OFF when done; the battery rules
from R1 are read once more.
**Expected result.** The board runs from its own battery; the charger's LEDs behave.
**Done when.** Power-on from battery works; charge LED seen; polarity teacher-verified.
**Stuck.** הסוללה חמה, נפוחה או נראית פגועה — מפסיקים ומוסרים למורה מיד.

### Milestone 11 — The cable comes off
**Goal.** Bluetooth: the mouse works with no wire at all.
**Steps.** (1) Claude Code installs "ESP32-BLE-Mouse" (T-vK). (2) Upload `06_bt_mouse`
(over USB), then unplug. (3) Switch ON — the mouse advertises as "P9-MOUSE". (4) Pair
from the computer's Bluetooth settings. (5) Everything from Milestone 8, now wireless,
running on the battery.
**Expected result.** Cursor, clicks, both rollers, layers — with the cable in a drawer.
**Done when.** Paired and fully working wirelessly for a whole test round.
**Stuck.** לא מוצאים "P9-MOUSE" — מכבים ומדליקים את המתג ומרעננים את החיפוש. קוראים למורה.

### Milestone 12 — The mattress test (final milestone)
**Goal.** The reason this mouse exists, proven: full function on a soft surface.
**Steps.** (1) The test matrix, checked live: cursor / left / right / scroll / middle /
speed roller + LEDs / three side buttons / layer — first on the desk, then on the
mattress-like surface. (2) Battery topped up on the TP4056. (3) The build photographed
for the project folder. (4) Celebrate — this mouse did not exist a month ago.
**Expected result.** Every row of the matrix passes on both surfaces.
**Done when.** The full matrix ✓ on fabric; photo saved; the smile happened.
**Stuck.** שורה שלא עוברת — חוזרים לכרטיסייה של אותו רכיב. קוראים למורה.

## Tier 2 — making it yours (6 milestones)

1. **Startup** — wake the mouse, run the short matrix, open `T2_mouse_starter` with its
   TUNING BLOCK in Claude Code.
2. **Choice א׳ — your speeds.** Tune `CPI_LEVELS` and the starting level to the student's
   hand with Claude Code; test each change on the fabric surface.
3. **Choice ב׳ — your buttons.** Remap `S1_BASE/S2_BASE/S3_BASE` and decide what the layer
   does; rename the Bluetooth name (`MOUSE_NAME`) to the mouse's real name.
4. **Choice ג׳ — bed mode.** Turn on `BED_MODE`, feel the smoothing, tune it; decide
   whether inverting an axis helps this hand.
5. **The shell begins.** Choose concept A/B/C from the design folder, mock the shape in
   cardboard/foam around the real parts, mark where every control falls under the fingers.
   (3D printing happens with the teacher, outside the cards — recorded honestly.)
6. **The signature demo** — name the mouse, demonstrate every personalized behaviour, and
   show one thing no store-bought mouse of theirs does.

## Tier 3 — planner

The standard planner card: design your own extension. Seeded ideas: the 2.4 GHz dongle on
a spare S3 Mini; a scroll-wheel click-and-a-half; a profile per app; the printed shell.

## Reference cards

R1 — battery + soldering safety (the only R card, P8-style; task-card footers cite it,
and the T1·M1 contract card reads its rules aloud).

## Open items (recorded, not blocking)

- Sketches not compile-tested (no ESP32 core here) — first upload session is the test.
- Step figures (Blender) not yet modelled for the mouse — wiring figures ship now, the
  step-figure pass follows the P8 pattern later.
- Shell CAD, wheels, JST harnesses, 2.4 GHz dongle: future phases, seeded in T2/T3.
- GM 2.0 Silent switches, if quiet clicks return as a requirement: drop-in swap.
