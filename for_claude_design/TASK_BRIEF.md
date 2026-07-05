# Task: redesign the Hebrew task cards of Projects 3 + 4 (same design system as Projects 1 + 2)

Look at the designs you made earlier in this project for the Hebrew task cards of **Project 1 (אותות אור)** and **Project 2 (משחק זמן תגובה)** — the `.dc.html` cards with the blue header band, progress bar, numbered step cards, skip-notices, and checkbox persistence. Apply the **same design system** to the attached Hebrew task cards of:

- **Project 3 — לא להתקרב יותר מדי** (proximity alarm): 12 cards, folder `project_3/`
- **Project 4 — מכונית עוקבת קו** (line-following car, first soldering project): 15 cards, folder `project_4/`

## Hard constraints

1. **The Hebrew text is FINAL — design only.** Every card just went through a professional Hebrew-editing pass and a three-reviewer pedagogical/visual review. Do not reword, shorten, merge, or "improve" any Hebrew sentence. Reflow into your components, but keep the wording exactly.
2. **Keep the card structure and meaning of every section:** header/milestone locator, "למה" intro, "מה עושים" checklist (with חלק א׳/ב׳ splits where present), wiring diagram section, "מה רואים אם הכול תקין", "סיימתם כש:", "תקועים?". Final milestones (P3 T1_M6, P3 T2_M5, P4 T1_M8, P4 T2_M6) get the celebration treatment like P1/P2.
3. **Project 3 wiring diagrams: use the real Fritzing breadboard images** included in `project_3/` (`w_p3_01…04_breadboard.svg`) — embed them as the wiring figure of the matching cards (T1_M1→01, T1_M3→02, T1_M4 and T2_M1→03, T3→04). **Do not replace them with stylized schematics** — we deliberately removed a stylized schematic from Project 1's T2_M2b in favor of the Fritzing image.
4. **Project 4 wiring diagrams: use the real breadboard images** included in `project_4/` — embed them as the wiring figure of the matching cards: `w_p4_01_driver_wiring` → T1_M4 **and** T2_M1 (full wiring map; the thick black wire is the common-ground — keep its caption emphasis), `w_p4_01_motors_to_driver` → T1_M5, `w_p4_05_button_tier3` → T3. Keep the ASCII wiring blocks as styled monospace panels (LTR) alongside the figures, like in P3.
5. **Soldering safety (Project 4) keeps maximum prominence:** the four-rules box on T1_M1 stays a strong red warning; every soldering-related "תקועים?" item keeps "קוראים למורה, תמיד" — never soften into self-help.
6. **Technical tokens stay LTR and monospace:** pin names (OUT1, GND, D5–D12), filenames (`03_distance_full_alarm.ino`), constants (`THRESHOLD_CM`, `BASE_SPEED`, `CORRECTION`, `LINE_IS_HIGH`, `true`/`false`).
7. **R-card references (R1…R6) keep the circled-badge treatment** like in P1/P2.
8. **Checkbox persistence** like P2: unique localStorage key per card (`tc_p3t1m1_checks`, `tc_p4t2m3_checks`, …).
9. **File naming per the P2 convention:** `P3_T1_M1_wire_sensor_he.dc.html`, `P4_T1_M1_meet_soldering_he.dc.html`, etc. One `.dc.html` per source card, using the shared `./support.js` runtime.

## Card lists

**Project 3 (V1 = שלב N מתוך 6, V2 = N מתוך 5, V3 = מתכנן):** T1_M1_wire_sensor, T1_M2_upload_distance_sketch, T1_M3_add_led_threshold, T1_M4_add_buzzer_full_alarm, T1_M5_test_real_objects, T1_M6_show_celebrate, T2_M1_startup, T2_M2_pick_threshold, T2_M3_pick_response_and_modify, T2_M4_test_and_tune, T2_M5_signature_alarm, T3_project_planner.

**Project 4 (V1 = שלב N מתוך 8, V2 = N מתוך 6, V3 = מתכנן):** T1_M1_meet_soldering, T1_M2_solder_motor_leads, T1_M3_assemble_chassis, T1_M4_wire_driver_and_sensors, T1_M5_drive_forward, T1_M6_sensor_test, T1_M7_line_follow_first_run, T1_M8_run_track_celebrate, T2_M1_startup, T2_M2_pick_speed, T2_M3_pick_correction_and_modify, T2_M4_design_build_track, T2_M5_test_and_tune, T2_M6_signature_run, T3_project_planner.
