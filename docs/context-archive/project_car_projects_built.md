---
name: car-projects-built-2026-08-20
description: "P4 adjusted + P5 (14 cards) + P7 (17 cards) built on the polygal 4WD platform with ESP32 web control; template, sketches, pin maps, deferrals"
metadata:
  type: project
---

2026-08-20, commits 2403459..8fada5d: the full car arc built per Yon's decisions
(polygal 8-10mm hand-cut chassis 25x15cm, 4WD TT motors, ESP32
replaces Uno in P5 with soft-AP web driving page, ESP32-CAM in P7).

**Chassis template:** Arduino_Projects/Project_4_Line_Following_Car/chassis_template/
chassis_template_he.{html,pdf} — 1:1 A4 landscape, self-jigging drill marks (mark
through component's own holes), sensors 26mm apart at nose, brain zone Uno<->ESP32,
camera perch, 50mm calibration bar. mm-true SVG; ALL text middle-anchored (RTL SVG
start-anchor spills left — hazard).

**P4 adjusted** (9 cards, wf_339688f3): T1_M3 rewritten to polygal fabrication;
T1_M2 4 motors/8 joints; T1_M4 side pairs parallel. Sketches PWM<=200 documented.

**P5 built** (14 cards, wf_58e9e059): pin map "six in a row" 32,33,25,26,27,14 ->
ENA,IN1,IN2,IN3,IN4,ENB; L298N 5V->VIN. Sketches: 00_esp32_test, 01_wifi_drive
(soft-AP + RTL hold-to-drive page at 192.168.4.1), T2_wifi_drive_starter (CHANGE
THIS: identity/speed רגוע130 מאוזן170 ספורטיבי200/colors). localStorage tc_p5*.

**P7 built** (17 cards, wf_50317b9e): AI-Thinker ESP32-CAM; only 4 free pins ->
IN1=14,IN2=15(L),IN3=13,IN4=12(R), ENA/ENB caps ON, PWM on INs; FTDI upload ritual
(IO0-GND jumper + RST, remove after); TWO POWER RAILS: battery->L298N (motors) +
battery->buck 5V->CAM + 470-1000uF cap stripe-to-GND, common ground (brownout
lesson); MJPEG stream :81. Sketches 01_camera_explorer, T2_explorer_starter.

**Registration done:** build_card_nav.js (P5+P7), build_cards_only.js (PROJECTS,
stems, arg whitelist — NOTE the arg whitelist is a separate hardcoded list that
silently defaults to P1!), .gitignore bundle whitelists. Bundles committed.

**Authoring hazard learned (candidate for the prefs log H-series):** the dc
renderer DROPS whitespace-only text nodes between <span>s inside <pre> — newlines
must live inside span text or use div-per-line. Hit ~6 cards, fixed by verifiers.
Also: "ודא" starts with root-vav — NOT a P2 comma-before-conjunction target (a
verifier over-trimmed it once; restored).

**Deferred:** P5/P7 reference-card sets (R-set; P4's partially serve); Fritzing/
composited wiring figures (ASCII maps used, P2/P3 precedent); sketch compile tests
(workshop machine, esp arduino-esp32 API drift risk on the CAM sketch); overview
appendix scope for P5/P7 (build_overview_with_cards.js covers P1-P2 only);
GPT Hebrew pass + review-console round on the new sets; P6 sensor question
(BMP280 vs DHT22) still open; P6+P8 card sets not started.

**P6 built too** (15 cards, wf_31eb2077, commit 018b6c7): DHT22 (Yon's call; one-wire,
GPIO4) + SSD1306 OLED as THE I2C device (SDA21/SCL22 @0x3C); modules on 3.3V via
breadboard power rails (single 3V3 pin); soft-AP page WEATHER-01 with live tiles
(/data JSON every 2s); T2 output LED26 (220Ω) / buzzer27 / servo via Claude Code,
HUMIDITY_THRESHOLD alert (room 35-55%, breath 70-90%). First Library-Manager installs
(DHT sensor library + Adafruit Unified Sensor; Adafruit SSD1306 + GFX). Sketches:
01_dht_serial, 02_dht_oled, 03_weather_web, T2_smart_device_starter.

**2026-08-22 — battery decision + real figures.** Yon: "lets do 4 motors and use aa batteries"
→ **8×AA box with switch (12V)** replaces 2×18650 everywhere (P4/P5/P7 cards, sketch comments,
chassis template battery zone now 110×61 mm at x 161–271 / brain 46–114 / L298N 116–159,
master doc + both overviews incl. budget: consumables $89/$76, year-1 $1,734–1,808, year-2
$463–562). Speed constants were NOT rescaled (comments say ≤200, 160 gentler with fresh
alkaline) — Yon may retune on the workshop machine. Real Fritzing-style figures now exist for
P4 (4 regenerated), P5 (3), P6 (5), P7 (4) via [[reference_fritzing_kit]]; embedded in 12
P5–P7 cards; all four bundles + 3 docs rebuilt. Still open: P4 R1 body text still says
"the left motor" (singular) in places; P5/P6/P7 R-sets; GPT Hebrew pass on the new captions.
