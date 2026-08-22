// ============================================================
// Project 8 - Tiny ESP32 Quadcopter
// Tier 2 Starter: YOUR drone
// ============================================================
//
// Same self-levelling flight sketch as Sketch 01 - but now it
// is YOURS. Every block marked  ==== CHANGE THIS ====  is a
// decision from the choice cards. Change, upload, put the drone
// on the level table, refresh the page, fly (tethered!).
//
// Everything below the CHANGE THIS blocks is the flight brain -
// leave it alone unless the teacher sits with you.
//
// Board: DOIT ESP32 DEVKIT V1. Props OFF for every bench test.
// ONLY FLY TETHERED. Eye protection on. One drone armed at a time.
// USB in = battery out; battery in = USB out - never both.
//
// BENCH CHECK - DISARMED, MOTORS OFF: while the drone is disarmed the
// page shows the four motor numbers in grey - what the motors WOULD get
// at about a third throttle. Nothing spins. Hold the drone by the two
// centre plates only, hair back, and tilt it: nose down -> FRONT up /
// BACK down; right side down -> RIGHT up / LEFT down; turned CCW ->
// RIGHT + LEFT up / FRONT + BACK down; still -> all four about equal.
// A live drone is never lifted, tilted or turned while ARMED.
//
// The teacher's phone is the second DISARM button: a DISARM that comes
// from any phone other than the pilot's LOCKS the drone - it refuses
// ARM until the battery has been out and in again. The page also counts
// MOTOR TIME (this ARM / total since the battery went in) beside the
// ARMED banner and shows the drone's network name.
// ============================================================

#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// ==== CHANGE THIS 1: your drone's identity ===================
// STATION = your station number (1..8). The teacher already set it when
//   the sketch was copied into your folder - leave that line as it is.
//   The Wi-Fi network is built from it: DRONE-01 .. DRONE-08, so every
//   drone in the room has its own name.
// DRONE_WIFI_PASS = the password on your station card: 8+ characters,
//   English letters / numbers / dashes. Not shared with anyone - any
//   phone that knows it is a second pilot.
// DRONE_DISPLAY_NAME = the name on the page. Hebrew is fine here,
//   exactly as written between the ordinary quotes - no special prefix.
const int   STATION            = 1;
const char  DRONE_WIFI_PASS[]  = "fly-drone-01";
const char* DRONE_DISPLAY_NAME = "הרחפן שלי";
// ============================================================

// ==== CHANGE THIS 2: stabilisation strength (pick ONE set) ===
// Careful  (זהיר):   KP = 1.5, KD = 0.10   - softer, may drift a little
// Balanced (מאוזן):  KP = 2.0, KD = 0.14   - the standard set
// Tuning after the first flight (one small step at a time!):
//   wobbles fast  -> KP down by 0.2     bounces after a push -> KD up by 0.02
//   leans, slow to fix -> KP up by 0.2  feels sluggish        -> KD down by 0.02
const float KP = 2.0;
const float KD = 0.14;
// ============================================================

// ==== CHANGE THIS 3: throttle ceiling (85 or 100 - never more) =
// 85  = careful (זהיר):  slider 100 % = 217 of 255; gentler, less lift margin on a heavy drone
// 100 = balanced (מאוזן): slider 100 % = the full 255 (the standard set)
// Whatever the ceiling, the throttle climbs at a fixed rate and can
// never jump - that is in the flight brain, not here.
const int MAX_THROTTLE_PERCENT = 100;
// ============================================================

// ==== CHANGE THIS 4: your page's colors ======================
const char* PAGE_BACKGROUND = "#10243e";   // page background
const char* ARM_COLOR       = "#2563eb";   // the ARM button
// DISARM stays RED on every drone in the room - do not change it.
// Color picking: search "html color picker" and copy the #code
// ============================================================

// ------------------------------------------------------------
// Below this line: the flight brain (do not change)
// ------------------------------------------------------------
static_assert(STATION >= 1 && STATION <= 8, "STATION must be 1..8");
static_assert(sizeof(DRONE_WIFI_PASS) >= 9, "Wi-Fi password must be at least 8 characters (WPA2 rule)");
static_assert(MAX_THROTTLE_PERCENT >= 50 && MAX_THROTTLE_PERCENT <= 100, "Throttle ceiling must be 50..100 % - talk to the teacher");

const float KYAW = 0.3;                     // yaw-rate damping (stops slow spinning on the spot)
const int   MAX_PWM = (255 * MAX_THROTTLE_PERCENT + 50) / 100;   // 100 % -> 255, 85 % -> 217

// Throttle climb rate (safety): each 4 ms step the throttle may rise by
// this many PWM counts (of 255) - 0 -> 255 in about half a second. Down is instant.
const int THR_RISE_STEP = 2;

// Per-motor test (the FRONT / RIGHT / BACK / LEFT buttons): one motor, fixed 2 s, ~25 %.
const int           SOLO_DUTY = 64;
const unsigned long SOLO_MS   = 2000;

// Preview: while DISARMED the sketch keeps working out what the four motors
// WOULD get at about a third throttle and the page shows those numbers in
// grey. They are never written to the motors - that is what makes the
// bench tilt checks possible with everything switched off.
const int PREVIEW_THR = 255 / 3;          // 85 of 255 - about a third of full power

// Motor pins. Seen from above, FRONT arm away from you. Opposite arms
// spin the same way: FRONT + BACK CW, RIGHT + LEFT CCW. If YOUR drone
// was built the other way round (FRONT + BACK CCW), set YAW_SIGN = -1.
const int MOTOR_FRONT = 25, MOTOR_RIGHT = 26, MOTOR_BACK = 14, MOTOR_LEFT = 27;
const int YAW_SIGN = 1;
const int LED = 2;

// Sensor (GY-521): flat on foam, chip UP, X arrow pointing at the FRONT arm.
//   roll > 0 = RIGHT side lower   pitch > 0 = NOSE lower   yawRate > 0 = turning CCW from above
const int SDA_PIN = 21, SCL_PIN = 22;

// Complementary filter: ALPHA = how much the gyro is trusted each step (98 %),
// the accelerometer supplies the rest so the angle never drifts (~0.2 s pull-back at 250 Hz).
const float ALPHA = 0.98f;

// PWM 20 kHz 8-bit. Core 3.x API; core 2.x fallback in #else.
const int PWM_FREQ = 20000, PWM_BITS = 8;
#if ESP_ARDUINO_VERSION_MAJOR >= 3
void pwmAttach(int pin)           { ledcAttach(pin, PWM_FREQ, PWM_BITS); }
void pwmWrite (int pin, int duty) { ledcWrite(pin, duty); }
#else
int  pwmChannel(int pin)          { return pin == MOTOR_FRONT ? 0 : pin == MOTOR_RIGHT ? 1 : pin == MOTOR_BACK ? 2 : 3; }
void pwmAttach(int pin)           { ledcSetup(pwmChannel(pin), PWM_FREQ, PWM_BITS); ledcAttachPin(pin, pwmChannel(pin)); }
void pwmWrite (int pin, int duty) { ledcWrite(pwmChannel(pin), duty); }
#endif

const unsigned long LOOP_US         = 4000;   // 250 Hz control loop
const unsigned long WATCHDOG_MS     = 600;    // no pilot message -> DISARM
const unsigned long SENSOR_PROBE_MS = 100;    // how often the I2C bus is asked "sensor still there?"
const int   SENSOR_FROZEN_STEPS     = 50;     // 50 identical readings in a row (200 ms) = sensor dead
const float TILT_CUTOFF_DEG         = 60;     // fell over -> DISARM
const float ARM_LEVEL_DEG           = 20;     // must be this level to ARM
const int   MAX_CORRECTION          = 60;
const int   MAX_YAW_CORRECTION      = 30;

WebServer        server(80);
Adafruit_MPU6050 mpu;
String           pageHtml;
char             wifiName[16];               // "DRONE-01" .. built from STATION at boot

bool  sensorOk = false, armed = false;
int   throttlePct = 0;                       // 0-100 from the pilot's slider
int   thrNow = 0;                            // 0..MAX_PWM, what the motors get - climbs slowly toward the slider
uint32_t pilotIP = 0;                        // the phone that pressed ARM - the only one the throttle listens to
bool  soloActive = false; int soloIndex = 0; unsigned long soloStartMs = 0;
bool  lockedOut = false;                     // a DISARM from a phone that is not the pilot's - only a power cycle clears it
unsigned long armedAtMs = 0, motorMsTot = 0; // the page's motor-time counter: this ARM, and the total since the battery went in
float roll = 0, pitch = 0;
float rollRate = 0, pitchRate = 0, yawRate = 0;
float gxOff = 0, gyOff = 0, gzOff = 0;
int   mFront = 0, mRight = 0, mBack = 0, mLeft = 0;   // last values sent to the motors
int   pFront = 0, pRight = 0, pBack = 0, pLeft = 0;   // grey preview numbers (disarmed - nothing is written)
unsigned long lastLoopUs = 0, lastCmdMs = 0, lastPrintMs = 0, lastProbeMs = 0;

// ---- motors ----
void writeMotors(int f, int r, int b, int l) {
  mFront = constrain(f, 0, MAX_PWM); mRight = constrain(r, 0, MAX_PWM);
  mBack  = constrain(b, 0, MAX_PWM); mLeft  = constrain(l, 0, MAX_PWM);
  pwmWrite(MOTOR_FRONT, mFront); pwmWrite(MOTOR_RIGHT, mRight);
  pwmWrite(MOTOR_BACK,  mBack);  pwmWrite(MOTOR_LEFT,  mLeft);
}
void motorsOff() { writeMotors(0, 0, 0, 0); }
void writeSolo() {                           // per-motor test: exactly one motor at SOLO_DUTY
  writeMotors(soloIndex == 0 ? SOLO_DUTY : 0, soloIndex == 1 ? SOLO_DUTY : 0,
              soloIndex == 2 ? SOLO_DUTY : 0, soloIndex == 3 ? SOLO_DUTY : 0);
}
void endSolo() { if (soloActive) { soloActive = false; motorsOff(); } }
// Every DISARM goes through here. Re-arming needs the slider on 0 and a
// fresh ARM press - nothing re-arms by itself. lock = true (a DISARM from
// a phone that is not the pilot's) goes one step further: ARM is refused
// until the battery has been out and in.
void disarm(const char* why, bool lock = false) {
  if (armed) motorMsTot += millis() - armedAtMs;   // stop the motor-time counter
  armed = false; throttlePct = 0; thrNow = 0; pilotIP = 0; soloActive = false;
  if (lock) lockedOut = true;
  motorsOff();
  Serial.print("DISARMED - "); Serial.println(why);
}

// ---- sensor: liveness ----
void sensorLost(const char* why) {           // sensor gone -> motors off, ARM refused until battery out/in
  if (!sensorOk) return;
  sensorOk = false;
  if (armed) disarm("sensor lost");
  Serial.print("SENSOR LOST - "); Serial.println(why);
}
void probeSensor() {                         // every 100 ms: one empty I2C transaction to the sensor's address
  if (!sensorOk || millis() - lastProbeMs < SENSOR_PROBE_MS) return;
  lastProbeMs = millis();
  Wire.beginTransmission(MPU6050_I2CADDR_DEFAULT);
  if (Wire.endTransmission() != 0) sensorLost("no answer on I2C - check VCC(3V3) GND SDA(21) SCL(22)");
}

// ---- sensor: gyro + accelerometer -> roll, pitch (complementary filter) ----
void readAttitude(float dt) {
  sensors_event_t a, g, t;
  mpu.getEvent(&a, &g, &t);
  // A live sensor never returns the same six numbers twice in a row for 200 ms.
  static float last[6]; static int sameCount = 0;
  float cur[6] = { a.acceleration.x, a.acceleration.y, a.acceleration.z, g.gyro.x, g.gyro.y, g.gyro.z };
  bool same = true;
  for (int i = 0; i < 6; i++) { if (cur[i] != last[i]) same = false; last[i] = cur[i]; }
  sameCount = same ? sameCount + 1 : 0;
  if (sameCount >= SENSOR_FROZEN_STEPS) { sameCount = 0; sensorLost("readings frozen"); return; }

  rollRate  = (g.gyro.x - gxOff) * RAD_TO_DEG;
  pitchRate = (g.gyro.y - gyOff) * RAD_TO_DEG;
  yawRate   = (g.gyro.z - gzOff) * RAD_TO_DEG;
  float rollAcc  = atan2(a.acceleration.y, a.acceleration.z) * RAD_TO_DEG;
  float pitchAcc = atan2(-a.acceleration.x,
                         sqrt(a.acceleration.y * a.acceleration.y + a.acceleration.z * a.acceleration.z)) * RAD_TO_DEG;
  roll  = ALPHA * (roll  + rollRate  * dt) + (1.0f - ALPHA) * rollAcc;   // 98 % gyro, 2 % accelerometer
  pitch = ALPHA * (pitch + pitchRate * dt) + (1.0f - ALPHA) * pitchAcc;
}

void calibrateGyro() {
  Serial.println("Calibrating gyro - keep the drone still and level (2 s)...");
  float sx = 0, sy = 0, sz = 0, az = 0; const int N = 500;
  for (int i = 0; i < N; i++) {
    sensors_event_t a, g, t;
    mpu.getEvent(&a, &g, &t);
    sx += g.gyro.x; sy += g.gyro.y; sz += g.gyro.z; az += a.acceleration.z;
    digitalWrite(LED, (i / 12) % 2);
    delay(4);
  }
  gxOff = sx / N; gyOff = sy / N; gzOff = sz / N;
  if (az / N < 5.0f) Serial.println("WARNING: sensor seems upside down (chip must face UP)");
  sensors_event_t a, g, t; mpu.getEvent(&a, &g, &t);
  roll  = atan2(a.acceleration.y, a.acceleration.z) * RAD_TO_DEG;
  pitch = atan2(-a.acceleration.x, sqrt(a.acceleration.y * a.acceleration.y + a.acceleration.z * a.acceleration.z)) * RAD_TO_DEG;
  Serial.print("Calibrated. Level reads roll "); Serial.print(roll, 1); Serial.print("  pitch "); Serial.println(pitch, 1);
  if (fabs(roll) > 5 || fabs(pitch) > 5) Serial.println("WARNING: the table is not level - the drone will lean that way");
}

// ---- control: PD + plus-mix ----
// Works out the four motor values for a given throttle from the tilt the
// sensor reports right now. Writes nothing - the caller decides whether
// they go to the motors (ARMED) or only to the page (DISARMED preview).
void computeMix(int thr, int &f, int &r, int &b, int &l) {
  // P and D only, no I-term: a CG offset shows up as a small steady lean the P term holds against.
  float rollCorr  = KP * roll  + KD * rollRate;      // + when the right side is low / dropping
  float pitchCorr = KP * pitch + KD * pitchRate;     // + when the nose is low / dropping
  float yawCorr   = KYAW * yawRate * YAW_SIGN;       // + when turning CCW
  rollCorr  = constrain(rollCorr,  -MAX_CORRECTION,     MAX_CORRECTION);
  pitchCorr = constrain(pitchCorr, -MAX_CORRECTION,     MAX_CORRECTION);
  yawCorr   = constrain(yawCorr,   -MAX_YAW_CORRECTION, MAX_YAW_CORRECTION);
  f = constrain((int)(thr + pitchCorr - yawCorr), 0, MAX_PWM);   // FRONT  (low side gets more)
  r = constrain((int)(thr + rollCorr  + yawCorr), 0, MAX_PWM);   // RIGHT
  b = constrain((int)(thr - pitchCorr - yawCorr), 0, MAX_PWM);   // BACK   (high side gets less)
  l = constrain((int)(thr - rollCorr  + yawCorr), 0, MAX_PWM);   // LEFT
}

// 250 times a second while ARMED - the only path that can put a non-zero value on a motor pin.
void runStabilizer() {
  int thrTarget = throttlePct * MAX_PWM / 100;
  if (thrTarget > thrNow) thrNow = min(thrNow + THR_RISE_STEP, thrTarget);   // up: limited
  else                    thrNow = thrTarget;                                // down: instant
  int thr = thrNow;
  if (thr == 0) { if (soloActive) writeSolo(); else motorsOff(); return; }
  int f, r, b, l;
  computeMix(thr, f, r, b, l);
  writeMotors(f, r, b, l);
}

// DISARMED: the same sums at a pretend third-throttle, for the page only.
void updatePreview() { computeMix(PREVIEW_THR, pFront, pRight, pBack, pLeft); }

// ---- the page (built once at boot so your colors and name go in) ----
void buildPage() {
  pageHtml = F(
    "<!DOCTYPE html><html lang='he' dir='rtl'><head>"
    "<meta charset='utf-8'>"
    "<meta name='viewport' content='width=device-width, initial-scale=1, user-scalable=no'>"
    "<title>%TITLE%</title>"
    "<style>"
    "body{margin:0;font-family:sans-serif;background:%BG%;color:#fff;display:flex;flex-direction:column;"
    "align-items:center;min-height:100vh;-webkit-user-select:none;user-select:none;touch-action:manipulation}"
    "h1{font-size:1.4rem;margin:14px 0 4px}"
    "p{margin:0 0 10px;color:#9fb6d4;font-size:0.85rem;text-align:center}"
    ".st{font-size:1.2rem;font-weight:700;padding:8px 22px;border-radius:14px;margin:6px 0 14px}"
    ".off{background:#334155}.on{background:#16a34a}"
    ".hd{display:flex;align-items:center;gap:12px}"
    "#tm{font-family:monospace;font-size:1rem;color:#9fb6d4;direction:ltr}"
    ".row{display:flex;gap:14px}"
    "button{border:none;border-radius:18px;font-size:1.6rem;font-weight:700;color:#fff;width:140px;height:90px}"
    "button:active{transform:translateY(3px)}"
    ".arm{background:%ARM%}.dis{background:#dc2626;box-shadow:0 4px 0 #7f1d1d}"
    ".thr{margin-top:22px;width:90vw;max-width:420px;text-align:center}"
    ".thr label{font-size:1.1rem}.thr b{font-size:1.6rem}"
    "input[type=range]{-webkit-appearance:none;width:100%;height:16px;border-radius:8px;background:#334155;margin:14px 0}"
    "input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:46px;height:46px;border-radius:50%;background:#fbbf24}"
    "input[type=range]:disabled{opacity:0.35}"
    ".att{margin-top:16px;font-size:1.05rem;direction:ltr}"
    ".mot{display:grid;grid-template-columns:repeat(4,64px);gap:8px;margin-top:10px;direction:ltr}"
    ".mot div{background:rgba(255,255,255,0.12);border-radius:10px;padding:6px 0;text-align:center;font-size:0.8rem;color:#9fb6d4}"
    ".mot b{display:block;font-size:1.2rem;color:#fff}"
    ".mot.prev div{opacity:0.45}"
    "#pl{color:#9fb6d4;font-size:0.8rem;margin-top:6px}"
    ".solo{display:grid;grid-template-columns:repeat(3,80px);grid-template-rows:repeat(3,44px);gap:6px;margin-top:14px;direction:ltr}"
    ".solo button{width:80px;height:44px;font-size:0.9rem;border-radius:10px;background:#475569;box-shadow:0 3px 0 #1e293b}"
    ".solo button:disabled{opacity:0.35;box-shadow:none}"
    ".solo .f{grid-column:2;grid-row:1}.solo .l{grid-column:1;grid-row:2}.solo .r{grid-column:3;grid-row:2}.solo .b{grid-column:2;grid-row:3}"
    ".info{color:#9fb6d4;font-size:0.8rem;margin-top:8px;text-align:center}"
    "#msg{color:#fbbf24;min-height:1.2em}"
    "</style></head><body>"
    "<h1>&#128641; %TITLE%</h1>"
    "<p>מחוון על 0 &larr; ARM &larr; מעלים לאט &larr; DISARM לעצירה</p>"
    "<div class='hd'><div id='st' class='st off'>כבוי &middot; DISARMED</div><div id='tm'>0:00 / 0:00</div></div>"
    "<div class='row'><button class='arm' id='arm'>ARM</button><button class='dis' id='dis'>DISARM</button></div>"
    "<div class='thr'><label>מצערת <b id='pv'>0%</b></label>"
    "<input type='range' id='sl' min='0' max='100' value='0'></div>"
    "<div class='att'>Roll <b id='r'>0.0</b>&deg; &nbsp; Pitch <b id='p'>0.0</b>&deg; &nbsp; Yaw <b id='y'>0</b>&deg;/s</div>"
    "<div class='mot' id='mot'><div>FRONT<b id='mf'>0</b></div><div>RIGHT<b id='mr'>0</b></div>"
    "<div>BACK<b id='mb'>0</b></div><div>LEFT<b id='ml'>0</b></div></div>"
    "<div id='pl'>תצוגה מקדימה &middot; המנועים כבויים</div>"
    "<div class='solo'><button class='f' data-n='0' disabled>FRONT</button><button class='l' data-n='3' disabled>LEFT</button>"
    "<button class='r' data-n='1' disabled>RIGHT</button><button class='b' data-n='2' disabled>BACK</button></div>"
    "<div class='info'>בדיקת מנוע בודד: 2 שניות ב-25 % &middot; רק כשחמוש והמחוון על 0<br>רשת: <span id='nt'>-</span> &middot; טלפונים מחוברים: <span id='ph'>0</span></div>"
    "<p id='msg'></p>"
    "<script>"
    "var armed=false,pilot=false,me=true,solo=false,seq=0;"
    "var sl=document.getElementById('sl'),pv=document.getElementById('pv'),msg=document.getElementById('msg');"
    "var solos=document.querySelectorAll('.solo button');"
    "function mmss(s){return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2)}"
    "function ask(u){var s=seq;return fetch(u).then(function(r){return r.text()}).catch(function(){return 'X'}).then(function(t){return s==seq?t:'X'})}"
    "function refresh(){var ok=armed&&me&&!solo&&sl.value=='0';for(var i=0;i<solos.length;i++)solos[i].disabled=!ok;"
    "sl.disabled=armed&&!me;if(armed&&!me)msg.textContent='מסך צפייה - DISARM בלבד'}"
    "function setArmed(now){if(armed&&!now){pilot=false;msg.textContent='כבוי - מחוון ל-0, ואז ARM מחדש'}armed=now;"
    "var st=document.getElementById('st');st.className='st '+(armed?'on':'off');"
    "st.innerHTML=armed?'חמוש &middot; ARMED':'כבוי &middot; DISARMED';refresh()}"
    "function show(s){if(s.charAt(0)!='A'&&s.charAt(0)!='D')return;setArmed(s.charAt(0)=='A');if(s.length>2)msg.textContent=s.substring(2)}"
    "function sendT(){ask('/t?v='+sl.value).then(show)}"
    "sl.addEventListener('input',function(){pv.textContent=sl.value+'%';refresh();sendT()});"
    "document.getElementById('arm').addEventListener('click',function(){"
    "if(sl.value!='0'){msg.textContent='מורידים את המחוון ל-0 לפני ARM';return}seq++;"
    "ask('/arm?v='+sl.value).then(function(s){if(s.charAt(0)=='A'&&s.length<=2){pilot=true;me=true;msg.textContent=''}show(s)})});"
    "document.getElementById('dis').addEventListener('click',function(){ask('/disarm').then(show)});"
    "for(var i=0;i<solos.length;i++)solos[i].addEventListener('click',function(){ask('/m?n='+this.getAttribute('data-n')).then(show)});"
    "setInterval(function(){if(pilot)sendT()},200);"
    "setInterval(function(){var s=seq;fetch('/data').then(function(r){return r.json()}).then(function(d){if(s!=seq)return;"
    "me=(d.me==1);solo=(d.solo==1);setArmed(d.armed==1);"
    "document.getElementById('r').textContent=d.roll.toFixed(1);document.getElementById('p').textContent=d.pitch.toFixed(1);"
    "document.getElementById('y').textContent=d.yaw.toFixed(0);"
    "document.getElementById('mf').textContent=d.f;document.getElementById('mr').textContent=d.r;"
    "document.getElementById('mb').textContent=d.b;document.getElementById('ml').textContent=d.l;"
    "document.getElementById('mot').className='mot'+(d.preview==1?' prev':'');"
    "document.getElementById('pl').style.display=d.preview==1?'block':'none';"
    "document.getElementById('ph').textContent=d.phones;"
    "document.getElementById('nt').textContent=d.net;"
    "document.getElementById('tm').textContent=mmss(d.as)+' / '+mmss(d.at);"
    "if(d.lock==1)msg.textContent='נעול - סוללה החוצה ופנימה';"
    "if(d.sensor==0)msg.textContent='החיישן אבד - בדקו את 4 החוטים, סוללה החוצה ופנימה'}).catch(function(){})},250);"
    "</script></body></html>");
  pageHtml.replace("%TITLE%", DRONE_DISPLAY_NAME);
  pageHtml.replace("%BG%",    PAGE_BACKGROUND);
  pageHtml.replace("%ARM%",   ARM_COLOR);
}

// ---- web handlers: reply "A"/"D" (+ ":reason", in Hebrew because the page shows it) ----
void handleRoot() { server.send(200, "text/html; charset=utf-8", pageHtml); }
void reply(const char* extra) { server.send(200, "text/plain", String(armed ? "A" : "D") + extra); }
uint32_t clientIP() { return (uint32_t)server.client().remoteIP(); }
bool fromPilot()    { return clientIP() == pilotIP; }
void handleArm() {
  if (lockedOut) { reply(":נעול - סוללה החוצה ופנימה"); return; }     // another phone disarmed: battery out and in first
  if (armed)                                                     { reply(":כבר חמוש");                 return; }
  if (!sensorOk)                                                 { reply(":החיישן לא עונה");          return; }
  if (throttlePct > 0 || server.arg("v").toInt() != 0)           { reply(":המחוון לא על 0");          return; }
  if (fabs(roll) > ARM_LEVEL_DEG || fabs(pitch) > ARM_LEVEL_DEG) { reply(":להניח על משטח ישר קודם"); return; }
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
  if (!armed)       { throttlePct = 0; reply(""); return; }       // nothing is stored while disarmed
  if (!fromPilot()) { reply(":מסך צפייה - DISARM בלבד"); return; } // not the pilot's phone: ignored
  int v = constrain(server.arg("v").toInt(), 0, 100);
  if (v > 0) endSolo();
  throttlePct = v;
  lastCmdMs = millis();                                          // the watchdog counts only the pilot
  reply("");
}
void handleSolo() {                                              // /m?n=0..3 : FRONT / RIGHT / BACK / LEFT
  if (!armed)                        { reply(":קודם ARM");               return; }
  if (!fromPilot())                  { reply(":מסך צפייה - DISARM בלבד"); return; }
  if (throttlePct > 0 || thrNow > 0) { reply(":המחוון לא על 0");         return; }
  if (soloActive)                    { reply(":מנוע אחד בכל פעם");       return; }
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

void haltFlicker() { while (true) { digitalWrite(LED, !digitalRead(LED)); delay(40); } }

void setup() {
  // FIRST THING: motor pins LOW so the MOSFET gates stay off while the board boots.
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
  Serial.println("===== PROJECT 8 - MY DRONE (Tier 2) =====");
  Serial.print("KP "); Serial.print(KP); Serial.print("  KD "); Serial.print(KD);
  Serial.print("  throttle ceiling "); Serial.print(MAX_THROTTLE_PERCENT); Serial.print(" % = ");
  Serial.print(MAX_PWM); Serial.println(" / 255");
  Serial.print("Motor pins: FRONT "); Serial.print(MOTOR_FRONT); Serial.print("  RIGHT "); Serial.print(MOTOR_RIGHT);
  Serial.print("  BACK ");            Serial.print(MOTOR_BACK);  Serial.print("  LEFT ");  Serial.print(MOTOR_LEFT);
  Serial.print("   I2C SDA ");        Serial.print(SDA_PIN);      Serial.print("  SCL ");   Serial.println(SCL_PIN);

  if (strlen(DRONE_WIFI_PASS) < 8) {
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
  mpu.setFilterBandwidth(MPU6050_BAND_44_HZ);
  Wire.setClock(400000);                                    // fast I2C, set after mpu.begin() which re-inits the bus
  delay(100);
  calibrateGyro();

  buildPage();
  snprintf(wifiName, sizeof(wifiName), "DRONE-%02d", STATION);
  WiFi.softAP(wifiName, DRONE_WIFI_PASS, 1, 0, 2);         // WPA2, channel 1, visible, at most 2 phones (pilot + teacher)
  Serial.print("Network:  "); Serial.println(wifiName);
  Serial.print("Password: "); Serial.println(DRONE_WIFI_PASS);
  Serial.print("Page:     http://"); Serial.println(WiFi.softAPIP());
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
  server.handleClient();
  probeSensor();

  unsigned long nowUs = micros();
  if (nowUs - lastLoopUs < LOOP_US) return;
  float dt = (nowUs - lastLoopUs) / 1000000.0f;
  lastLoopUs = nowUs;
  if (dt > 0.02f) dt = 0.02f;

  if (sensorOk) readAttitude(dt);

  if (armed && millis() - lastCmdMs > WATCHDOG_MS)                               disarm("no command for 600 ms - phone lost?");
  if (armed && (fabs(roll) > TILT_CUTOFF_DEG || fabs(pitch) > TILT_CUTOFF_DEG)) disarm("tilt over 60 deg - fell over?");
  if (soloActive && millis() - soloStartMs >= SOLO_MS)                           endSolo();

  if (armed) { runStabilizer(); }
  else       { motorsOff(); updatePreview(); }                                  // disarmed: motors off, preview numbers only

  if (!sensorOk)  digitalWrite(LED, (millis() / 40) % 2);                        // very fast flicker = sensor lost
  else            digitalWrite(LED, armed ? HIGH : ((millis() % 1000) < 100 ? HIGH : LOW));

  if (armed && millis() - lastPrintMs > 1000) {
    lastPrintMs = millis();
    Serial.print("slider "); Serial.print(throttlePct); Serial.print("%  motors "); Serial.print(thrNow);
    Serial.print("  roll "); Serial.print(roll, 1);
    Serial.print("  pitch "); Serial.print(pitch, 1); Serial.print("  F/R/B/L ");
    Serial.print(mFront); Serial.print('/'); Serial.print(mRight); Serial.print('/');
    Serial.print(mBack);  Serial.print('/'); Serial.println(mLeft);
  }
}
