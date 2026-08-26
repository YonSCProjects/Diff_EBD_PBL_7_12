---
name: Channel C — spoken-companion mode
description: Third Claude Code channel (after A/B) — 100% voice-in/voice-out mode for students with severe reading/writing difficulty (severe ADHD + foreign-language home, or equivalent); pilot in Project 1
type: project
originSessionId: e680ace2-857b-49f5-9ebd-56985d6eee86
---
**The channel.** Principle 7 originally defined two Claude Code channels — A (pair programmer) and B (scaffolded tutorial reading the printed card aloud). **Channel C** adds a third mode: Claude Code *becomes* the navigation card rather than reading one. Student works voice-in/voice-out through headphones + mic; never reads, never types. The only visual anchor is a **picture-board** (zero text, Fritzing-rendered hardware target-state + T1·MN ID chip) per milestone.

**Why it exists.** Pilot for a specific student: passive-participation style (Principle 10), intelligent + technically capable, severe ADHD, foreign language at home → serious Hebrew reading/writing difficulty. If the pilot works, the pattern replicates to other students and other projects.

**Files (all Hebrew-primary, all in Project 1):**
- `Arduino_Projects/Project_1_Light_Signals/claude_code_channel_c_spoken_companion_he.md` — master prompt-pack loaded as Claude Code system instruction. Contains persona + 12 rules + per-milestone dialogue scripts M1–M8 (Tier 1 only in v1).
- `Arduino_Projects/Project_1_Light_Signals/task_cards_spoken/T1_M1_picture.html` … `T1_M8_picture.html` — 8 A4-landscape picture-boards (zero text, just ID chip + big image + progress dots).
- `Arduino_Projects/Project_1_Light_Signals/teacher_materials/channel_c_teacher_launch_card_he.html` — A5 teacher quarter-page: pre-session prep, what to expect during, what to do after.
- `Arduino_Projects/Project_1_Light_Signals/images/w_arduino_only_breadboard.svg` (+ _pcb, _schematic) — Fritzing-exported Arduino-only image, used by M1/M2 picture-boards (created by stripping all non-Arduino parts from Step1.fzz via jszip).

**Key design decisions made during v1 pilot build:**
- Tier 1 only (M1–M8). Tier 2 + T3 deferred to v2 if pilot succeeds.
- Hebrew-primary dialogue; technical terms (Arduino, LED, pin 9, GND, Upload, 220 Ω) stay in English.
- Cross-session state memory: Claude reads the session history and resumes from the last completed milestone when the student says *any* opening words (no trigger-phrase required). Only the very first session uses a scripted M1 opener.
- Teacher-alert mechanism: Claude tells the student *"take off the headphones and go to [teacher]"* — no audible Claude-to-teacher shouts (headphones make that impossible). Same pattern for 90-second silence threshold and 3-failed-attempt stuck protocol.
- M7 safety gate: wrong pull-down placement triggers immediate teacher-call, not 2 retry attempts (electrical-reset risk).
- Validation-and-reinforcement phrasing (תיקוף וחיזוק) follows the established Principle 10 script library.
- Movement break (Principle 6) is explicit Rule 12 — scripted after M4.

**Open items for v2 iteration** (after 2–3 pilot sessions):
- .ino file-name verification: scaffold instructs teacher to open `01_blink_L_fast`/`02_blink_external`/`03_blink_alternating`/`04_button_control` — confirm these match current `ino_files/` before first session.
- M4 "זה הרגע. זה קורה. בנית דבר שעובד." is three sentences, technically violating Rule 8 "one sentence" — reserved M4 exception, may need formalizing.
- Picture-board layout has large whitespace around the Fritzing SVG — acceptable for v1, could be tightened.

**How to apply.** When any other student presents with severe reading/writing difficulty + a capacity to work the hardware, consider offering Channel C. The scaffold is replicable: one scaffold .md per project + 8-12 picture-boards per project + the same teacher launch card with the project number swapped.
