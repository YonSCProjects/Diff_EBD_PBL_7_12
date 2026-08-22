// ============================================================
// Project 8 - Tiny ESP32 Quadcopter
// Sketch 01: Flight (self-levelling with the MPU6050)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   Same phone page as Sketch 00 (ARM / DISARM / throttle slider /
//   four per-motor test buttons), but now the drone keeps ITSELF
//   level. 250 times a second it:
//     1. reads the gyro + accelerometer (MPU6050),
//     2. blends them into a roll angle and a pitch angle
//        (the "complementary filter"),
//     3. works out how much to speed up the low side and slow
//        the high side (the "PD controller"),
//     4. writes four new speeds to the four motors.
//   The page also shows the live roll/pitch and the four motor
//   values, so you can test the brain on the bench, props OFF.
//
// ONLY FLY TETHERED. Eye protection on. One drone armed at a time.
//
// USB in = battery out. Battery in = USB out. Never both.
//   Uploads happen on USB with the battery unplugged (the motors
//   cannot move - nothing feeds BAT+). Every motor run happens on
//   battery with the USB cable out; everything you need to see is
//   on the phone page.
//
// HOW TO USE:
//   1. Put the drone on a flat, level table. USB out, battery in.
//      It calibrates its gyro for 2 s - DO NOT MOVE IT while the
//      blue LED flickers fast.
//   2. Phone > Wi-Fi > your drone's network (DRONE-xx, password on
//      your station card) > browser > 192.168.4.1
//   3. Slider on 0 -> ARM -> slide up slowly -> DISARM to stop.
//   The teacher's phone opens the same page: it shows everything
//   and its DISARM works, but only the phone that pressed ARM can
//   move the throttle.
//
// BENCH CHECK BEFORE THE FIRST FLIGHT - DISARMED, MOTORS OFF:
//   Props off (check by touch). Battery in, page open, DO NOT ARM.
//   While the drone is DISARMED the page shows the four motor numbers
//   in grey: what the motors WOULD get at about a third throttle.
//   Nothing spins. Hair tied back, sleeves up, hold the drone by the
//   two centre plates only (never by an arm), and move it:
//     tilt the nose DOWN        -> FRONT goes up, BACK goes down
//     tilt the RIGHT side DOWN  -> RIGHT goes up, LEFT goes down
//     turn it counter-clockwise (seen from above)
//                               -> RIGHT + LEFT go up, FRONT + BACK go down
//     hold it still             -> all four settle to about the same
//   If a check fails, the sensor is mounted the wrong way round
//   (see SENSOR ORIENTATION below) - fix that before flying.
//   A live drone is never lifted, tilted or turned while ARMED.
//
// SAFETY BUILT INTO THE CODE (do not remove any of it):
//   - motor pins LOW before PWM is switched on; always boots DISARMED
//   - the Wi-Fi network has a password and takes at most 2 phones
//     (pilot + teacher); the throttle listens only to the phone that
//     pressed ARM; DISARM works from every phone
//   - ARM refused unless the slider is on 0, the drone is level
//     (within 20 deg) and the sensor is working
//   - DISARM is latched: after any DISARM (button, watchdog, tilt,
//     sensor) the motors stay off until the slider is back on 0
//     AND ARM is pressed again - nothing re-arms by itself
//   - a DISARM that arrives from a phone that is NOT the pilot's (the
//     teacher's second stop button) also LOCKS the drone: it refuses
//     ARM until the battery has been out and in again
//   - the throttle can only CLIMB at a fixed rate (about half a
//     second from 0 to full) - a slider slam cannot slam the motors.
//     Going DOWN is never slowed: slider to 0, DISARM, the watchdog
//     and the tilt cut-off all cut power on the same step
//   - 100 % on the slider = full motor power (255 of 255)
//   - no message from the pilot's phone for 600 ms -> DISARM
//   - tilted more than 60 deg (it fell / crashed) -> DISARM
//   - the sensor stops answering, or its numbers freeze -> DISARM,
//     and ARM is refused until the battery is out and in again
//   - per-motor test button: ONE motor, 2 s, 25 % power, only while
//     ARMED with the slider on 0; DISARM or the watchdog ends it early
//   - the page counts MOTOR TIME (this ARM / total since the battery
//     went in) beside the ARMED banner, and shows the drone's network
//     name, so the teacher can call "land" at 3:00 without a stopwatch
//   - while DISARMED the page still shows what the motors WOULD do
//     (grey numbers), so the tilt checks never need an armed drone
//
// LED: fast flicker = calibrating (hold still)   solid = ARMED
//      short blink each second = ready, disarmed
//      very fast flicker that never stops = sensor not found / lost
// ============================================================

#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// ---- YOUR DRONE'S IDENTITY (the teacher sets these when copying the sketch) ----
//   STATION 1..8 -> the Wi-Fi network is called DRONE-01 .. DRONE-08.
//   Every drone in the room - on the bench on USB or at the flight
//   line - must have its own number, so a phone can never join the
//   wrong drone.
//   The password: 8+ characters, English letters / numbers / dashes,
//   a DIFFERENT one for every station. It goes on the station card
//   and on the teacher's sheet. Any phone that knows the name and the
//   password is a second pilot - so the password is not shared.
const int  STATION           = 1;
const char DRONE_WIFI_PASS[] = "fly-drone-01";
static_assert(STATION >= 1 && STATION <= 8, "STATION must be 1..8");
static_assert(sizeof(DRONE_WIFI_PASS) >= 9, "Wi-Fi password must be at least 8 characters (WPA2 rule)");

// ---- STABILISATION STRENGTH (the PD constants) ----
//   KP = how hard it pushes back per degree of tilt.
//   KD = how hard it brakes per degree-per-second of tilting speed.
//   Tier 2 starting sets:  careful (זהיר) KP 1.5 / KD 0.10
//                          balanced (מאוזן) KP 2.0 / KD 0.14
//   Wobbles fast -> lower KP.  Bounces after a push -> raise KD a little.
const float KP   = 2.0;
const float KD   = 0.14;
const float KYAW = 0.3;        // yaw-rate damping: stops it slowly spinning on the spot (0 = off)

// ---- THROTTLE CEILING (100 % = the full 255; Tier 2 may choose 85 for a careful build) ----
const int MAX_THROTTLE_PERCENT = 100;
const int MAX_PWM = (255 * MAX_THROTTLE_PERCENT + 50) / 100;   // = 255
static_assert(MAX_THROTTLE_PERCENT >= 50 && MAX_THROTTLE_PERCENT <= 100, "Throttle ceiling must be 50..100 %");

// ---- THROTTLE CLIMB RATE (safety - do not change) ----
//   Each 4 ms control step the throttle may rise by this many PWM
//   counts (of 255): 0 -> 255 takes about half a second. Down is instant.
const int THR_RISE_STEP = 2;

// ---- PER-MOTOR TEST (the FRONT / RIGHT / BACK / LEFT buttons) ----
const int           SOLO_DUTY = 64;       // ~25 % of 255 - spins a bare 8520, stays undramatic
const unsigned long SOLO_MS   = 2000;     // fixed 2 s run, then off by itself

// ---- PREVIEW (the DISARMED bench check) ----
//   While DISARMED the sketch keeps working out what the four motors
//   WOULD get at this pretend throttle, and the page shows those numbers
//   in grey. They are never written to the motors - that is the whole
//   point: the tilt checks are done with everything switched off.
const int PREVIEW_THR = 255 / 3;          // 85 of 255 - about a third of full power

// ---- MOTOR PINS (one MOSFET gate per motor - do not change) --------
// Seen from above, FRONT arm away from you. Opposite arms spin the
// same way: FRONT + BACK clockwise (CW), RIGHT + LEFT counter-clockwise
// (CCW). That is what stops the drone from spinning on the spot.
// If YOUR drone was built the other way round (FRONT + BACK CCW),
// set YAW_SIGN to -1.
const int MOTOR_FRONT = 25;
const int MOTOR_RIGHT = 26;
const int MOTOR_BACK  = 14;
const int MOTOR_LEFT  = 27;
const int YAW_SIGN    = 1;
const int LED         = 2;

// ---- SENSOR ORIENTATION (GY-521 board) ----
// Mounted flat on foam tape, chip facing UP, the X arrow printed on
// the board pointing at the FRONT arm (then the Y arrow points LEFT).
// Angle signs the whole sketch uses:
//   roll  > 0  = RIGHT side is lower       pitch > 0 = NOSE is lower
//   yawRate > 0 = turning counter-clockwise seen from above
const int SDA_PIN = 21, SCL_PIN = 22;

// ---- COMPLEMENTARY FILTER ----
//   ALPHA = how much the gyro is trusted each step (98 %); the
//   accelerometer supplies the other 2 % so the angle never drifts.
//   0.98 at 250 Hz = the accelerometer pulls the angle back over ~0.2 s.
const float ALPHA = 0.98f;

// ---- PWM (20 kHz, 8-bit). Core 3.x API; core 2.x fallback in #else ----
const int PWM_FREQ = 20000, PWM_BITS = 8;
#if ESP_ARDUINO_VERSION_MAJOR >= 3
void pwmAttach(int pin)           { ledcAttach(pin, PWM_FREQ, PWM_BITS); }
void pwmWrite (int pin, int duty) { ledcWrite(pin, duty); }
#else   // ledcSetup/ledcAttachPin/ledcWrite(channel) - numbered channels
int  pwmChannel(int pin)          { return pin == MOTOR_FRONT ? 0 : pin == MOTOR_RIGHT ? 1 : pin == MOTOR_BACK ? 2 : 3; }
void pwmAttach(int pin)           { ledcSetup(pwmChannel(pin), PWM_FREQ, PWM_BITS); ledcAttachPin(pin, pwmChannel(pin)); }
void pwmWrite (int pin, int duty) { ledcWrite(pwmChannel(pin), duty); }
#endif

// ---- timing + limits ----
const unsigned long LOOP_US      = 4000;   // 4 ms = 250 Hz control loop
const unsigned long WATCHDOG_MS  = 600;    // no pilot message for this long -> DISARM
const unsigned long SENSOR_PROBE_MS = 100; // how often the I2C bus is asked "sensor still there?"
const int   SENSOR_FROZEN_STEPS  = 50;     // 50 identical readings in a row (200 ms) = sensor dead
const float TILT_CUTOFF_DEG      = 60;     // more than this = it fell over -> DISARM
const float ARM_LEVEL_DEG        = 20;     // must be flatter than this to ARM
const int   MAX_CORRECTION       = 60;     // roll/pitch correction never exceeds this many PWM steps
const int   MAX_YAW_CORRECTION   = 30;

WebServer        server(80);
Adafruit_MPU6050 mpu;
char             wifiName[16];               // "DRONE-01" .. built from STATION at boot

bool  sensorOk = false, armed = false;
int   throttlePct = 0;                       // 0-100 from the pilot's slider (what the pilot ASKS for)
int   thrNow = 0;                            // 0..MAX_PWM, what the motors GET - climbs slowly toward the slider
uint32_t pilotIP = 0;                        // the phone that pressed ARM - the only one the throttle listens to
bool  soloActive = false; int soloIndex = 0; unsigned long soloStartMs = 0;   // per-motor test state
bool  lockedOut = false;                     // a DISARM from a phone that is not the pilot's - only a power cycle clears it
unsigned long armedAtMs = 0, motorMsTot = 0; // the page's motor-time counter: this ARM, and the total since the battery went in
float roll = 0, pitch = 0;                   // degrees, from the filter
float rollRate = 0, pitchRate = 0, yawRate = 0;   // deg/s, from the gyro
float gxOff = 0, gyOff = 0, gzOff = 0;       // gyro offsets found at boot
int   mFront = 0, mRight = 0, mBack = 0, mLeft = 0;   // last values sent to the motors
int   pFront = 0, pRight = 0, pBack = 0, pLeft = 0;   // grey preview numbers (disarmed - nothing is written)
unsigned long lastLoopUs = 0, lastCmdMs = 0, lastPrintMs = 0, lastProbeMs = 0;

// ------------------------------------------------------------ motors
void writeMotors(int f, int r, int b, int l) {
  mFront = constrain(f, 0, MAX_PWM); mRight = constrain(r, 0, MAX_PWM);
  mBack  = constrain(b, 0, MAX_PWM); mLeft  = constrain(l, 0, MAX_PWM);
  pwmWrite(MOTOR_FRONT, mFront); pwmWrite(MOTOR_RIGHT, mRight);
  pwmWrite(MOTOR_BACK,  mBack);  pwmWrite(MOTOR_LEFT,  mLeft);
}
void motorsOff() { writeMotors(0, 0, 0, 0); }

// The per-motor test: exactly one motor at SOLO_DUTY, the other three off.
void writeSolo() {
  writeMotors(soloIndex == 0 ? SOLO_DUTY : 0, soloIndex == 1 ? SOLO_DUTY : 0,
              soloIndex == 2 ? SOLO_DUTY : 0, soloIndex == 3 ? SOLO_DUTY : 0);
}
void endSolo() { if (soloActive) { soloActive = false; motorsOff(); } }

// Every DISARM goes through here: motors off, throttle and ramp back to
// zero, the pilot's phone forgotten. Re-arming needs the slider on 0
// and a fresh ARM press - nothing re-arms by itself.
// lock = true (a DISARM from a phone that is not the pilot's) goes one
// step further: ARM is refused until the battery has been out and in.
void disarm(const char* why, bool lock = false) {
  if (armed) motorMsTot += millis() - armedAtMs;   // stop the motor-time counter
  armed = false; throttlePct = 0; thrNow = 0; pilotIP = 0; soloActive = false;
  if (lock) lockedOut = true;
  motorsOff();
  Serial.print("DISARMED - "); Serial.println(why);
}

// ------------------------------------------------------------ sensor
// Called when the MPU6050 stops answering or its readings freeze.
// Motors off at once; ARM stays refused until the battery is out and in.
void sensorLost(const char* why) {
  if (!sensorOk) return;
  sensorOk = false;
  if (armed) disarm("sensor lost");
  Serial.print("SENSOR LOST - "); Serial.println(why);
}

// Every 100 ms: one empty I2C transaction to the sensor's address. The
// moment a VCC / GND / SDA / SCL wire comes off, it stops answering.
void probeSensor() {
  if (!sensorOk || millis() - lastProbeMs < SENSOR_PROBE_MS) return;
  lastProbeMs = millis();
  Wire.beginTransmission(MPU6050_I2CADDR_DEFAULT);
  if (Wire.endTransmission() != 0) sensorLost("no answer on I2C - check VCC(3V3) GND SDA(21) SCL(22)");
}

// Reads the MPU6050 and updates roll, pitch (degrees) and the three rates.
void readAttitude(float dt) {
  sensors_event_t a, g, t;
  mpu.getEvent(&a, &g, &t);                       // accel in m/s^2, gyro in rad/s

  // A live sensor never returns the same six numbers twice in a row
  // for 200 ms. If it does, it is dead (or the bus is stuck).
  static float last[6]; static int sameCount = 0;
  float cur[6] = { a.acceleration.x, a.acceleration.y, a.acceleration.z, g.gyro.x, g.gyro.y, g.gyro.z };
  bool same = true;
  for (int i = 0; i < 6; i++) { if (cur[i] != last[i]) same = false; last[i] = cur[i]; }
  sameCount = same ? sameCount + 1 : 0;
  if (sameCount >= SENSOR_FROZEN_STEPS) { sameCount = 0; sensorLost("readings frozen"); return; }

  rollRate  = (g.gyro.x - gxOff) * RAD_TO_DEG;    // + = right side going down
  pitchRate = (g.gyro.y - gyOff) * RAD_TO_DEG;    // + = nose going down
  yawRate   = (g.gyro.z - gzOff) * RAD_TO_DEG;    // + = turning CCW seen from above

  // The accelerometer "sees" which way gravity points -> a slow, noisy
  // but drift-free tilt angle.
  float rollAcc  = atan2(a.acceleration.y, a.acceleration.z) * RAD_TO_DEG;
  float pitchAcc = atan2(-a.acceleration.x,
                         sqrt(a.acceleration.y * a.acceleration.y +
                              a.acceleration.z * a.acceleration.z)) * RAD_TO_DEG;

  // Complementary filter: trust the gyro ALPHA (98 %) for the fast changes,
  // let the accelerometer pull the answer back the other 2 % so it never drifts.
  roll  = ALPHA * (roll  + rollRate  * dt) + (1.0f - ALPHA) * rollAcc;
  pitch = ALPHA * (pitch + pitchRate * dt) + (1.0f - ALPHA) * pitchAcc;
}

// Average the gyro for ~2 s while the drone is still. Whatever it reads
// now is its "zero" - that is why it must NOT move during this.
void calibrateGyro() {
  Serial.println("Calibrating gyro - keep the drone still and level (2 s)...");
  float sx = 0, sy = 0, sz = 0, az = 0; const int N = 500;
  for (int i = 0; i < N; i++) {
    sensors_event_t a, g, t;
    mpu.getEvent(&a, &g, &t);
    sx += g.gyro.x; sy += g.gyro.y; sz += g.gyro.z; az += a.acceleration.z;
    digitalWrite(LED, (i / 12) % 2);               // fast flicker = calibrating
    delay(4);
  }
  gxOff = sx / N; gyOff = sy / N; gzOff = sz / N;
  if (az / N < 5.0f) Serial.println("WARNING: sensor seems upside down (chip must face UP)");
  // Start the filter from the accelerometer's answer, so it does not begin at 0 on a sloped table.
  sensors_event_t a, g, t; mpu.getEvent(&a, &g, &t);
  roll  = atan2(a.acceleration.y, a.acceleration.z) * RAD_TO_DEG;
  pitch = atan2(-a.acceleration.x, sqrt(a.acceleration.y * a.acceleration.y + a.acceleration.z * a.acceleration.z)) * RAD_TO_DEG;
  Serial.print("Calibrated. Level reads roll "); Serial.print(roll, 1);
  Serial.print("  pitch "); Serial.println(pitch, 1);
  if (fabs(roll) > 5 || fabs(pitch) > 5) Serial.println("WARNING: the table is not level - the drone will lean that way");
}

// ------------------------------------------------------------ control
// The PD controller + plus-mix. Works out the four motor values for a
// given throttle from the tilt the sensor reports right now. It writes
// nothing: the caller decides whether the numbers go to the motors
// (ARMED) or only to the page as grey preview numbers (DISARMED).
void computeMix(int thr, int &f, int &r, int &b, int &l) {
  // P: push back in proportion to the tilt.  D: brake in proportion to
  // how fast it is tilting (taken straight from the gyro - much cleaner
  // than subtracting two noisy angles).
  // P and D only, no I-term: a CG offset shows up as a small steady lean
  // the P term holds against. Fine on a tether; an I-term would wind up
  // while the drone sits on the ground.
  float rollCorr  = KP * roll  + KD * rollRate;    // + when the right side is low / dropping
  float pitchCorr = KP * pitch + KD * pitchRate;   // + when the nose is low / dropping
  float yawCorr   = KYAW * yawRate * YAW_SIGN;     // + when turning CCW
  rollCorr  = constrain(rollCorr,  -MAX_CORRECTION,     MAX_CORRECTION);
  pitchCorr = constrain(pitchCorr, -MAX_CORRECTION,     MAX_CORRECTION);
  yawCorr   = constrain(yawCorr,   -MAX_YAW_CORRECTION, MAX_YAW_CORRECTION);

  // Mixing (plus-mix: X-shaped frame flown with one arm forward):
  //   low side gets MORE, high side gets LESS - by the same amount, so
  //   the total lift (and the height) barely changes.
  //   Yaw: slow the CW pair (FRONT+BACK), speed the CCW pair (RIGHT+LEFT)
  //   when the body turns CCW - their reaction torque turns it back.
  f = constrain((int)(thr + pitchCorr - yawCorr), 0, MAX_PWM);   // FRONT
  r = constrain((int)(thr + rollCorr  + yawCorr), 0, MAX_PWM);   // RIGHT
  b = constrain((int)(thr - pitchCorr - yawCorr), 0, MAX_PWM);   // BACK
  l = constrain((int)(thr - rollCorr  + yawCorr), 0, MAX_PWM);   // LEFT
}

// Runs 250 times a second while ARMED - the only path that can put a
// non-zero value on a motor pin.
void runStabilizer() {
  // Throttle ramp: the motors follow the slider UP by at most
  // THR_RISE_STEP counts per step, and DOWN instantly.
  int thrTarget = throttlePct * MAX_PWM / 100;      // 100 % slider = MAX_PWM
  if (thrTarget > thrNow) thrNow = min(thrNow + THR_RISE_STEP, thrTarget);   // up: limited
  else                    thrNow = thrTarget;                                // down: instant
  int thr = thrNow;
  if (thr == 0) {                                   // slider on 0 = all motors off, no twitching
    if (soloActive) writeSolo(); else motorsOff();  // (unless a per-motor test is running)
    return;
  }
  int f, r, b, l;
  computeMix(thr, f, r, b, l);
  writeMotors(f, r, b, l);
}

// DISARMED: the same sums at a pretend third-throttle, for the page only.
// Nothing in here touches a motor pin.
void updatePreview() { computeMix(PREVIEW_THR, pFront, pRight, pBack, pLeft); }

// ------------------------------------------------------------ web page
const char PAGE[] PROGMEM = R"rawliteral(
<!DOCTYPE html><html lang="he" dir="rtl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>הרחפן שלי</title>
<style>
  body { margin:0; font-family:sans-serif; background:#10243e; color:#fff; display:flex; flex-direction:column;
         align-items:center; min-height:100vh; -webkit-user-select:none; user-select:none; touch-action:manipulation; }
  h1 { font-size:1.4rem; margin:14px 0 4px; }   p { margin:0 0 10px; color:#9fb6d4; font-size:0.85rem; text-align:center; }
  .st { font-size:1.2rem; font-weight:700; padding:8px 22px; border-radius:14px; margin:6px 0 14px; }
  .off { background:#334155; }   .on { background:#16a34a; }   .row { display:flex; gap:14px; }
  .hd { display:flex; align-items:center; gap:12px; }
  #tm { font-family:monospace; font-size:1rem; color:#9fb6d4; direction:ltr; }
  button { border:none; border-radius:18px; font-size:1.6rem; font-weight:700; color:#fff; width:140px; height:90px; }
  button:active { transform:translateY(3px); }
  .arm { background:#2563eb; box-shadow:0 4px 0 #163a83; }   .dis { background:#dc2626; box-shadow:0 4px 0 #7f1d1d; }
  .thr { margin-top:22px; width:90vw; max-width:420px; text-align:center; }   .thr label { font-size:1.1rem; }   .thr b { font-size:1.6rem; }
  input[type=range] { -webkit-appearance:none; width:100%; height:16px; border-radius:8px; background:#334155; margin:14px 0; }
  input[type=range]::-webkit-slider-thumb { -webkit-appearance:none; width:46px; height:46px; border-radius:50%; background:#fbbf24; }
  input[type=range]:disabled { opacity:0.35; }
  .att { margin-top:16px; font-size:1.05rem; direction:ltr; }
  .mot { display:grid; grid-template-columns:repeat(4,64px); gap:8px; margin-top:10px; direction:ltr; }
  .mot div { background:#1e3a5f; border-radius:10px; padding:6px 0; text-align:center; font-size:0.8rem; color:#9fb6d4; }
  .mot b { display:block; font-size:1.2rem; color:#fff; }
  .mot.prev div { opacity:0.45; }
  #pl { color:#9fb6d4; font-size:0.8rem; margin-top:6px; }
  .solo { display:grid; grid-template-columns:repeat(3,80px); grid-template-rows:repeat(3,44px); gap:6px; margin-top:14px; direction:ltr; }
  .solo button { width:80px; height:44px; font-size:0.9rem; border-radius:10px; background:#475569; box-shadow:0 3px 0 #1e293b; }
  .solo button:disabled { opacity:0.35; box-shadow:none; }
  .solo .f { grid-column:2; grid-row:1; }  .solo .l { grid-column:1; grid-row:2; }
  .solo .r { grid-column:3; grid-row:2; }  .solo .b { grid-column:2; grid-row:3; }
  .info { color:#9fb6d4; font-size:0.8rem; margin-top:8px; text-align:center; }
  #msg { color:#fbbf24; min-height:1.2em; }
</style></head><body>
<h1>&#128641; הרחפן שלי</h1>
<p>מחוון על 0 &larr; ARM &larr; מעלים לאט &larr; DISARM לעצירה</p>
<div class="hd"><div id="st" class="st off">כבוי &middot; DISARMED</div><div id="tm">0:00 / 0:00</div></div>
<div class="row"><button class="arm" id="arm">ARM</button><button class="dis" id="dis">DISARM</button></div>
<div class="thr"><label>מצערת <b id="pv">0%</b></label><input type="range" id="sl" min="0" max="100" value="0"></div>
<div class="att">Roll <b id="r">0.0</b>&deg; &nbsp; Pitch <b id="p">0.0</b>&deg; &nbsp; Yaw <b id="y">0</b>&deg;/s</div>
<div class="mot" id="mot"><div>FRONT<b id="mf">0</b></div><div>RIGHT<b id="mr">0</b></div><div>BACK<b id="mb">0</b></div><div>LEFT<b id="ml">0</b></div></div>
<div id="pl">תצוגה מקדימה &middot; המנועים כבויים</div>
<div class="solo"><button class="f" data-n="0" disabled>FRONT</button><button class="l" data-n="3" disabled>LEFT</button><button class="r" data-n="1" disabled>RIGHT</button><button class="b" data-n="2" disabled>BACK</button></div>
<div class="info">בדיקת מנוע בודד: 2 שניות ב-25 % &middot; רק כשחמוש והמחוון על 0<br>רשת: <span id="nt">-</span> &middot; טלפונים מחוברים: <span id="ph">0</span></div>
<p id="msg"></p>
<script>
  var armed = false, pilot = false, me = true, solo = false, seq = 0;   // seq: answers from before the last ARM press are ignored
  var sl = document.getElementById('sl'), pv = document.getElementById('pv'), msg = document.getElementById('msg');
  var solos = document.querySelectorAll('.solo button');
  function mmss(s){ return Math.floor(s / 60) + ':' + ('0' + (s % 60)).slice(-2); }   // motor-time counter
  function ask(u){ var s = seq; return fetch(u).then(function(r){ return r.text(); }).catch(function(){ return 'X'; }).then(function(t){ return s == seq ? t : 'X'; }); }
  function refresh(){                                         // which controls this page may use right now
    var ok = armed && me && !solo && sl.value == '0';
    for (var i = 0; i < solos.length; i++) solos[i].disabled = !ok;
    sl.disabled = armed && !me;                               // another phone is the pilot: this page is DISARM-only
    if (armed && !me) msg.textContent = 'מסך צפייה - DISARM בלבד';
  }
  function setArmed(now){
    if (armed && !now) { pilot = false; msg.textContent = 'כבוי - מחוון ל-0, ואז ARM מחדש'; }   // latched: nothing re-arms by itself
    armed = now;
    var st = document.getElementById('st');
    st.className = 'st ' + (armed ? 'on' : 'off');
    st.innerHTML = armed ? 'חמוש &middot; ARMED' : 'כבוי &middot; DISARMED';
    refresh();
  }
  function show(s){                                           // "A"/"D" + optional ":reason"; anything else (failed/stale) is ignored
    if (s.charAt(0) != 'A' && s.charAt(0) != 'D') return;
    setArmed(s.charAt(0) == 'A'); if (s.length > 2) msg.textContent = s.substring(2);
  }
  function sendT(){ ask('/t?v=' + sl.value).then(show); }
  sl.addEventListener('input', function(){ pv.textContent = sl.value + '%'; refresh(); sendT(); });
  document.getElementById('arm').addEventListener('click', function(){
    if (sl.value != '0') { msg.textContent = 'מורידים את המחוון ל-0 לפני ARM'; return; }
    seq++;                                                    // from now on, only answers newer than this press count
    ask('/arm?v=' + sl.value).then(function(s){
      if (s.charAt(0) == 'A' && s.length <= 2) { pilot = true; me = true; msg.textContent = ''; }   // this page is the pilot now
      show(s);
    });
  });
  document.getElementById('dis').addEventListener('click', function(){ ask('/disarm').then(show); });
  for (var i = 0; i < solos.length; i++) solos[i].addEventListener('click', function(){ ask('/m?n=' + this.getAttribute('data-n')).then(show); });
  setInterval(function(){ if (pilot) sendT(); }, 200);       // heartbeat for the 600 ms watchdog - pilot page only
  setInterval(function(){                                    // live readout every 250 ms
    var s = seq;
    fetch('/data').then(function(r){ return r.json(); }).then(function(d){
      if (s != seq) return;                                  // asked before the last ARM press - stale
      me = (d.me == 1); solo = (d.solo == 1);
      setArmed(d.armed == 1);
      document.getElementById('r').textContent = d.roll.toFixed(1);  document.getElementById('p').textContent = d.pitch.toFixed(1);
      document.getElementById('y').textContent = d.yaw.toFixed(0);
      document.getElementById('mf').textContent = d.f;  document.getElementById('mr').textContent = d.r;
      document.getElementById('mb').textContent = d.b;  document.getElementById('ml').textContent = d.l;
      document.getElementById('mot').className = 'mot' + (d.preview == 1 ? ' prev' : '');   // grey while disarmed
      document.getElementById('pl').style.display = d.preview == 1 ? 'block' : 'none';
      document.getElementById('ph').textContent = d.phones;
      document.getElementById('nt').textContent = d.net;                             // must match the label on the frame
      document.getElementById('tm').textContent = mmss(d.as) + ' / ' + mmss(d.at);   // this ARM / since the battery went in
      if (d.lock == 1) msg.textContent = 'נעול - סוללה החוצה ופנימה';
      if (d.sensor == 0) msg.textContent = 'החיישן אבד - בדקו את 4 החוטים, סוללה החוצה ופנימה';
    }).catch(function(){});
  }, 250);
</script>
</body></html>
)rawliteral";

// ------------------------------------------------------------ web handlers
// Replies are "A" (armed) or "D" (disarmed), optionally followed by ":reason"
// (the reason is shown on the page, so it is in Hebrew).
void handleRoot()   { server.send_P(200, "text/html; charset=utf-8", PAGE); }
void reply(const char* extra) { server.send(200, "text/plain", String(armed ? "A" : "D") + extra); }
uint32_t clientIP() { return (uint32_t)server.client().remoteIP(); }
bool fromPilot()    { return clientIP() == pilotIP; }

void handleArm() {
  if (lockedOut) { reply(":נעול - סוללה החוצה ופנימה"); return; }         // another phone disarmed: battery out and in first
  if (armed)                                                     { reply(":כבר חמוש");                     return; }
  if (!sensorOk)                                                 { reply(":החיישן לא עונה");              return; }
  if (throttlePct > 0 || server.arg("v").toInt() != 0)           { reply(":המחוון לא על 0");              return; }
  if (fabs(roll) > ARM_LEVEL_DEG || fabs(pitch) > ARM_LEVEL_DEG) { reply(":להניח על משטח ישר קודם");     return; }
  armed = true; thrNow = 0; lastCmdMs = millis(); armedAtMs = millis();
  pilotIP = clientIP();                                          // this phone is the pilot until DISARM
  Serial.print("ARMED by "); Serial.println(server.client().remoteIP());
  reply("");
}
void handleDisarm() {                                            // open to EVERY phone - the teacher's too
  bool third = armed && !fromPilot();                            // not the pilot's phone = the teacher's stop button
  disarm(third ? "DISARM from another phone - locked until the battery is pulled" : "DISARM button", third);
  reply(third ? ":נעול - סוללה החוצה ופנימה" : "");
}
void handleThrottle() {
  if (!armed)      { throttlePct = 0; reply(""); return; }        // nothing is stored while disarmed (so ARM always starts from 0)
  if (!fromPilot()) { reply(":מסך צפייה - DISARM בלבד"); return; } // not the pilot's phone: ignored
  int v = constrain(server.arg("v").toInt(), 0, 100);
  if (v > 0) endSolo();                                          // slider moved off 0 - a per-motor test ends first
  throttlePct = v;
  lastCmdMs = millis();                                          // the watchdog counts only the pilot
  reply("");
}
void handleSolo() {                                              // /m?n=0..3 : FRONT / RIGHT / BACK / LEFT
  if (!armed)                      { reply(":קודם ARM");               return; }
  if (!fromPilot())                { reply(":מסך צפייה - DISARM בלבד"); return; }
  if (throttlePct > 0 || thrNow > 0) { reply(":המחוון לא על 0");       return; }
  if (soloActive)                  { reply(":מנוע אחד בכל פעם");       return; }
  const char* names[4] = { "FRONT", "RIGHT", "BACK", "LEFT" };
  const int   pins [4] = { MOTOR_FRONT, MOTOR_RIGHT, MOTOR_BACK, MOTOR_LEFT };
  soloIndex = constrain(server.arg("n").toInt(), 0, 3);
  soloActive = true; soloStartMs = millis(); lastCmdMs = millis();
  writeSolo();
  Serial.print("SOLO "); Serial.print(names[soloIndex]); Serial.print(" (GPIO "); Serial.print(pins[soloIndex]); Serial.println(") 2 s");
  reply("");
}
void handleData() {
  char buf[320];
  unsigned long armS = armed ? (millis() - armedAtMs) / 1000 : 0;                  // motor time of this ARM
  unsigned long totS = (motorMsTot + (armed ? millis() - armedAtMs : 0)) / 1000;   // and since the battery went in
  bool prev = !armed;                                          // disarmed -> the four numbers are the grey preview
  snprintf(buf, sizeof(buf),
           "{\"armed\":%d,\"roll\":%.1f,\"pitch\":%.1f,\"yaw\":%.0f,\"thr\":%d,\"f\":%d,\"r\":%d,\"b\":%d,\"l\":%d,"
           "\"max\":%d,\"preview\":%d,\"solo\":%d,\"phones\":%d,\"me\":%d,\"sensor\":%d,"
           "\"lock\":%d,\"as\":%lu,\"at\":%lu,\"net\":\"%s\"}",
           armed ? 1 : 0, roll, pitch, yawRate, thrNow,
           prev ? pFront : mFront, prev ? pRight : mRight, prev ? pBack : mBack, prev ? pLeft : mLeft,
           MAX_PWM, prev ? 1 : 0, soloActive ? 1 : 0, (int)WiFi.softAPgetStationNum(),
           (!armed || fromPilot()) ? 1 : 0, sensorOk ? 1 : 0, lockedOut ? 1 : 0, armS, totS, wifiName);
  server.send(200, "application/json", buf);
}

// ------------------------------------------------------------ setup / loop
void haltFlicker() { while (true) { digitalWrite(LED, !digitalRead(LED)); delay(40); } }   // very fast flicker forever

void setup() {
  // FIRST THING: motor pins LOW, so the MOSFET gates are held off while the board boots.
  pinMode(MOTOR_FRONT, OUTPUT); digitalWrite(MOTOR_FRONT, LOW);
  pinMode(MOTOR_RIGHT, OUTPUT); digitalWrite(MOTOR_RIGHT, LOW);
  pinMode(MOTOR_BACK,  OUTPUT); digitalWrite(MOTOR_BACK,  LOW);
  pinMode(MOTOR_LEFT,  OUTPUT); digitalWrite(MOTOR_LEFT,  LOW);
  pinMode(LED, OUTPUT);
  pwmAttach(MOTOR_FRONT); pwmAttach(MOTOR_RIGHT); pwmAttach(MOTOR_BACK); pwmAttach(MOTOR_LEFT);
  motorsOff();
  armed = false;                                            // always boot DISARMED

  Serial.begin(115200);
  delay(300);
  Serial.println();
  Serial.println("===== PROJECT 8 - FLIGHT =====");
  Serial.print("KP "); Serial.print(KP); Serial.print("  KD "); Serial.print(KD);
  Serial.print("  throttle ceiling "); Serial.print(MAX_THROTTLE_PERCENT); Serial.print(" % = ");
  Serial.print(MAX_PWM); Serial.println(" / 255");
  Serial.print("Motor pins: FRONT "); Serial.print(MOTOR_FRONT); Serial.print("  RIGHT "); Serial.print(MOTOR_RIGHT);
  Serial.print("  BACK ");            Serial.print(MOTOR_BACK);  Serial.print("  LEFT ");  Serial.print(MOTOR_LEFT);
  Serial.print("   I2C SDA ");        Serial.print(SDA_PIN);      Serial.print("  SCL ");   Serial.println(SCL_PIN);

  if (strlen(DRONE_WIFI_PASS) < 8) {                        // the ESP32 silently fails to start an AP with a short password
    Serial.println("ERROR: Wi-Fi password must be 8+ characters. Halting.");
    haltFlicker();
  }

  Wire.begin(SDA_PIN, SCL_PIN);
  sensorOk = mpu.begin();
  if (!sensorOk) {
    Serial.println("ERROR: MPU6050 not found - check VCC(3V3) GND SDA(21) SCL(22). Halting.");
    haltFlicker();
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_4_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_44_HZ);               // smooths motor vibration a little
  Wire.setClock(400000);                                    // fast I2C (set AFTER mpu.begin, which re-inits the bus) so one read takes < 1 ms
  delay(100);
  calibrateGyro();

  snprintf(wifiName, sizeof(wifiName), "DRONE-%02d", STATION);
  WiFi.softAP(wifiName, DRONE_WIFI_PASS, 1, 0, 2);         // WPA2, channel 1, visible, at most 2 phones (pilot + teacher)
  Serial.print("Network:  "); Serial.println(wifiName);
  Serial.print("Password: "); Serial.println(DRONE_WIFI_PASS);
  Serial.print("Page:     http://"); Serial.println(WiFi.softAPIP());   // 192.168.4.1
  server.on("/",       handleRoot);
  server.on("/arm",    handleArm);
  server.on("/disarm", handleDisarm);
  server.on("/t",      handleThrottle);
  server.on("/m",      handleSolo);
  server.on("/data",   handleData);
  server.begin();
  Serial.println("Ready - DISARMED. Slider on 0, then ARM.");
  lastLoopUs = micros();
}

void loop() {
  server.handleClient();                                    // phone messages, between control steps
  probeSensor();                                            // every 100 ms: is the sensor still on the bus?

  unsigned long nowUs = micros();
  if (nowUs - lastLoopUs < LOOP_US) return;                 // not yet time for the next 4 ms step
  float dt = (nowUs - lastLoopUs) / 1000000.0f;
  lastLoopUs = nowUs;
  if (dt > 0.02f) dt = 0.02f;                               // a slow web request passed - don't let one huge step upset the filter

  if (sensorOk) readAttitude(dt);

  if (armed && millis() - lastCmdMs > WATCHDOG_MS)                          disarm("no command for 600 ms - phone lost?");
  if (armed && (fabs(roll) > TILT_CUTOFF_DEG || fabs(pitch) > TILT_CUTOFF_DEG)) disarm("tilt over 60 deg - fell over?");
  if (soloActive && millis() - soloStartMs >= SOLO_MS)                      endSolo();   // the 2 s per-motor test is over

  if (armed) { runStabilizer(); }
  else       { motorsOff(); updatePreview(); }              // disarmed: motors off, preview numbers for the bench check

  // LED: solid = armed, short blink = ready, very fast flicker = sensor lost
  if (!sensorOk)  digitalWrite(LED, (millis() / 40) % 2);
  else            digitalWrite(LED, armed ? HIGH : ((millis() % 1000) < 100 ? HIGH : LOW));

  if (armed && millis() - lastPrintMs > 1000) {             // once a second while armed
    lastPrintMs = millis();
    Serial.print("slider "); Serial.print(throttlePct); Serial.print("%  motors "); Serial.print(thrNow);
    Serial.print("  roll "); Serial.print(roll, 1);
    Serial.print("  pitch "); Serial.print(pitch, 1); Serial.print("  F/R/B/L ");
    Serial.print(mFront); Serial.print('/'); Serial.print(mRight); Serial.print('/');
    Serial.print(mBack);  Serial.print('/'); Serial.println(mLeft);
  }
}
