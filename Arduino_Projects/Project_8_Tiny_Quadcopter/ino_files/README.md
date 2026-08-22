# Project 8 — Tiny ESP32 Quadcopter: the sketches

Three sketches, uploaded in this order. Each lives in its own folder (`<name>/<name>.ino`) so the Arduino IDE opens it directly.

| Sketch | Tier | What it is for | Props |
|---|---|---|---|
| `00_motor_test/00_motor_test.ino` | 1 (and 2) | "Do my motors spin?" — phone page with ARM / DISARM, one throttle slider that drives **all four motors at the same power**, and **four per-motor buttons** (FRONT / RIGHT / BACK / LEFT) that spin **one** motor for **2 seconds at ~25 %**. No gyro, no balancing. First run with bare motors; later reused for the **bench thrust test** on the kitchen scale. | **OFF** for the first run. ON only for the thrust test, drone inverted on the thrust-test post, teacher present. |
| `01_flight/01_flight.ino` | 1 | The full pre-written flight brain: MPU6050 → complementary filter → PD on roll and pitch → **plus-mix** → four motors, 250 times a second. Same page as 00 (including the four per-motor buttons) plus a live roll / pitch / yaw-rate readout and the four motor numbers. Arm/disarm, 600 ms phone watchdog, 60° tilt cut-off, sensor-loss cut-off, gyro calibration at boot. | OFF for the bench checks. ON only for tethered flight after the thrust test passed. |
| `T2_flight_starter/T2_flight_starter.ino` | 2 | Exactly the same brain as 01, but the top of the file has four `==== CHANGE THIS ====` blocks from the choice cards: (1) identity — `STATION` number, Wi-Fi password, page name, (2) PD starting set — careful (זהיר) Kp 1.5 / Kd 0.10 or balanced (מאוזן) Kp 2.0 / Kd 0.14, (3) throttle ceiling **85 or 100 %**, (4) page colours. Nothing below the blocks needs touching. | Same as 01. |

Tier 3 starts from `01_flight.ino` (or the student's own `T2` copy) and extends it with Claude Code at Level 3 — BMP280 altitude hold, SD logging, flight modes. Those are not pre-written.

## Pins (same on all three sketches — do not change)

| Signal | DevKit V1 GPIO | Note |
|---|---|---|
| FRONT motor gate | 25 | X frame flown "diamond": one arm points forward = FRONT |
| RIGHT motor gate | 26 | |
| BACK motor gate | 14 | |
| LEFT motor gate | 27 | |
| MPU6050 SDA / SCL | 21 / 22 | GY-521 on the 3V3 pin, never 5 V |
| Blue LED | 2 | on the board |

PWM: LEDC 20 kHz, 8-bit (0–255). Stock throttle ceiling **100 % = duty 255** (`MAX_THROTTLE_PERCENT = 100`); a Tier 2 student may choose 85 % (= duty 217) instead. Motor pins are driven `OUTPUT LOW` **before** the PWM is attached, and every sketch boots DISARMED.

Sensor orientation the code assumes: GY-521 flat on foam tape, chip facing **up**, the **X arrow on the board pointing at the FRONT arm**. Then `roll > 0` means the right side is lower and `pitch > 0` means the nose is lower. If the bench checks (below) come out backwards, the sensor is mounted the wrong way round — fix the mounting, not the code.

Motor spin directions the code assumes for yaw damping: **FRONT + BACK clockwise, RIGHT + LEFT counter-clockwise** (opposite arms spin the same way). If a drone was built the other way round, set `YAW_SIGN = -1` in the flight sketch.

## Your drone's identity (the teacher sets it when copying the sketch)

At the top of all three sketches:

```cpp
const int  STATION           = 1;              // 1..8 -> the network is called DRONE-01 .. DRONE-08
const char DRONE_WIFI_PASS[] = "fly-drone-01"; // 8+ characters, a DIFFERENT one for every station
```

- **`STATION` gives every drone in the room its own network name.** A drone sitting on a workstation on USB is powered, so it broadcasts too — if two drones answered to `DRONE-01`, the teacher's emergency DISARM could land on the wrong one. The sketch refuses to compile with a station number outside 1–8.
- **The Wi-Fi network has a WPA2 password**, unlike the car projects — here the network *is* the control stick, so any phone that knows the name and the password is a second pilot. The password goes on the **station card and the teacher's sheet only**; the phone remembers it after the first join. Shorter than 8 characters and the sketch refuses to compile (and the ESP32 would silently fail to start the network).
- The soft-AP takes **at most 2 phones**: the pilot's and the teacher's. The page shows how many are connected (`טלפונים מחוברים`) — it should read **2** at the flight line.
- Tier 2's `DRONE_DISPLAY_NAME` is the name on the page. **Hebrew is fine, typed between the ordinary quotes — no `u8` prefix** (a `u8` prefix is what actually fails to compile on the core 3.x board package).

## Arduino IDE settings (one-time, same as Projects 5 and 6)

1. **Board**: Tools → Board → esp32 → **DOIT ESP32 DEVKIT V1**
   (the ESP32 core comes from Boards Manager: "esp32 by Espressif Systems"; version 3.x is what the code is written for — an older 2.x install still compiles, the sketch picks the old PWM calls automatically)
2. **Upload Speed**: Tools → Upload Speed → **115200** (slower than the default, far fewer failed uploads with cheap cables)
3. **Port**: Tools → Port → the COM port that appears when the board is plugged in (unplug / replug to see which one)
4. **Serial Monitor**: 115200 baud

## Libraries (Library Manager, Sketch → Include Library → Manage Libraries)

- **Adafruit MPU6050** — when it asks "install all dependencies?", say yes (that pulls in **Adafruit Unified Sensor** and **Adafruit BusIO**)
- **Adafruit Unified Sensor** — check it shows INSTALLED
- `WiFi`, `WebServer`, `Wire` — come with the ESP32 core, nothing to install

`00_motor_test` needs no libraries at all.

## The upload ritual (every time, every sketch)

1. **Props OFF.** Bare motor shafts.
2. **Battery OUT.** Unplug the PH2.0 plug. The board is powered by USB only while uploading.
3. USB cable in. Check Board / Port / Upload Speed (above).
4. Click **Upload** (→). If the console sits on `Connecting.....`, **hold the BOOT button** on the DevKit until the dots start moving, then let go.
5. Wait for `Hard resetting via RTS pin...`
6. Open the Serial Monitor (115200). You should see the sketch's banner with the throttle ceiling and the four motor pins — for 01 / T2 also `Calibrating gyro...` then `Calibrated.` — and then `Network: DRONE-01`, `Password: ...`, `Page: http://192.168.4.1`.
7. USB out. Put the drone on a **flat, level** surface. **Battery IN** — and do not touch it for 2 s while the blue LED flickers fast (gyro calibration; 00 has no calibration and is ready at once).
8. Blue LED does a short blink once a second = ready, disarmed.
9. Phone: Settings → Wi-Fi → **your drone's network (`DRONE-01` … `DRONE-08`), password on your station card**. If the phone warns "no internet", stay connected. Browser → `192.168.4.1`.
10. The teacher's phone joins the same network and opens the same page — it is the **second DISARM button**. The teacher's page never presses ARM and never touches the slider (the board ignores it anyway; see below).

**USB in = battery out; battery in = USB out — never both.** Program rule since Project 4, and R10 in the project doc. Uploads and the Serial Monitor happen on USB with the PH2.0 plug **out** (the motors cannot move — nothing feeds BAT+). **Every** motor run — bare-shaft test, thrust test, bench checks, flight — happens on battery with the USB cable **out**; once the battery is in, everything you need to see is on the phone page, so you never need the cable while motors can spin. Why: the battery plug is the drone's one arming authority, and that only works if it is the only plug.

## Props OFF / props ON — the rule

- **Sketch 00, first run: props OFF.** Slider on 0 → ARM → press **FRONT**, then **RIGHT**, **BACK**, **LEFT**: each button spins that one motor for 2 s at ~25 %, which is also the wiring check (the motor that spins must be the one named). Then slide up slowly: all four shafts spin, all four follow the slider, nothing hot after a minute at 50 %. DISARM, battery out.
- **Bench thrust test: the first time props go on.** The drone goes **upside-down on top of the thrust-test post** — props toward the scale pan — held by two rubber bands across the centre plates; post + drone on the scale, **tared to 0**. Eye protection for everyone, teacher present. Sketch 00 again: read the scale at slider **60 %**, **80 %** and **100 %**, then climb in 5 % steps and note **the slider % at which the reading first passes the drone's all-up weight — the hover point**. That is the gate:
  - **hover point ≤ 75 %** → *fly* (tethered, like every flight)
  - **hover point 75–85 %** → *tethered only, ≤ 30 cm*, weight ladder before the next session
  - **above 85 %, or never reached** → *no flight this session*, weight ladder first

  T/W (the 100 % reading ÷ the weight) is written down as a number, not used as the gate. The teacher records all of it. *Why inverted: upright, the props blow onto the pan and the scale reads 30–70 % low.*
- **Sketch 01 / T2 bench checks: props OFF again — and DISARMED.** Battery in, page open, **do not ARM**: while the drone is disarmed the page shows the four motor numbers in **grey**, which is what the motors *would* get at about a third throttle. Nothing spins. Hair tied back, sleeves up, hold the drone **by the two centre plates only** and move it:
  - tilt the nose down → FRONT goes up, BACK goes down
  - tilt the right side down → RIGHT goes up, LEFT goes down
  - turn it counter-clockwise (seen from above) → RIGHT + LEFT go up, FRONT + BACK go down
  - hold it still → all four settle to about the same number

  A live drone is never lifted, tilted or turned while ARMED.
- **Props ON for flight only after the thrust test passed and the bench checks passed** — and every practice flight is **tethered**, eye protection on, 3 m clear zone, one drone armed at a time.

## What the page does, and what the code does by itself

- **ARM** is refused unless the slider is on 0 (and for 01 / T2: the drone is within 20° of level and the sensor is answering). The page shows the reason in Hebrew. ARM is also refused if the drone is already armed.
- **One pilot.** The phone that pressed ARM owns the throttle and the per-motor buttons; the board ignores `/t` and `/m` from any other phone and tells it *"מסך צפייה - DISARM בלבד"*. **DISARM works from every phone** — that is what makes the teacher's phone a real second stop button.
- **DISARM** stops all four motors immediately, and it is **latched**: after *any* disarm (button, watchdog, tilt, sensor) the motors stay off until the slider is physically back on **0** *and* ARM is pressed again. Nothing re-arms by itself, and the board forgets who the pilot was. A DISARM that arrives from a phone that is **not** the pilot's — the teacher's second stop button — goes one step further and **locks** the drone: ARM is refused (the page says *נעול - סוללה החוצה ופנימה*) until the battery has been out and in again, so the teacher can walk in without waiting for the pilot to let go of the phone. DISARM is red on every drone; the Tier 2 colour block does not touch it.
- **Throttle climbs slowly, stops instantly.** The throttle may rise by only **2 PWM counts every 4 ms** (about half a second from 0 to full), so a slider slam — or a tap at the far end of the track — can only be a slow climb. Going *down* is never slowed: slider to 0, DISARM, the watchdog and the tilt cut-off all cut power on the same 4 ms step.
- **Watchdog.** While armed, the *pilot's* page sends the slider value every 200 ms. If the board hears nothing **from the pilot** for **600 ms** (page closed, phone locked, Wi-Fi dropped) it disarms itself. The teacher's page does not send a heartbeat, so it can never keep a lost drone alive.
- **Per-motor buttons** (all three sketches): accepted only while **ARMED with the slider on 0**, one motor at a time, a fixed **2 s** at ~25 % — a press is a timer, not a hold. DISARM, the watchdog, or moving the slider off 0 ends it early.
- 01 / T2: tilted more than **60°** → disarm (it fell over or hit the tether).
- 01 / T2: **the sensor stops answering** — the board pings it on the I2C bus every 100 ms, and also notices if the six readings freeze for 200 ms — → motors off, and ARM stays refused until the battery is out and in again. Without this the 60° cut-off would be blind exactly when the sensor wire shakes loose.
- Slider 100 % = motor duty **255 of 255** (or 217 if a Tier 2 student chose the 85 % ceiling). The PD corrections ride on top of the slider value and can only move the motors between 0 and that ceiling.
- The page also shows **how many phones are connected**. Two (pilot + teacher) is right; anything else, stop and find out why before ARM.
- The page shows the drone's **network name** (`רשת: DRONE-xx`) beside that count — it must match the tape label on the frame before anyone presses ARM — and a **motor-time counter** beside the ARMED banner: *this ARM / total since the battery went in*, counted while the drone is armed. That is the number the 3-minute "land" call is read from; it resets when the battery comes out.
- LED: fast flicker = calibrating (hold still) · short blink each second = ready · solid = armed · very fast flicker that never stops = MPU6050 not found or lost (check the four GY-521 wires; the Serial Monitor says the same).

## Tuning notes (Tier 2 card material)

Change one constant, one small step, one flight at a time:

| What you see | Change |
|---|---|
| wobbles fast / buzzes | Kp down by 0.2 |
| bounces after a push, slow to settle | Kd up by 0.02 |
| leans and is slow to come back | Kp up by 0.2 |
| feels sluggish, mushy | Kd down by 0.02 |
| slowly turns on the spot | leave KYAW; check the CW/CCW pairs and `YAW_SIGN` |
| will not lift by ~90 % of the slider | not a code problem — re-weigh, check the battery and the props. The answer is never a higher ceiling. |
