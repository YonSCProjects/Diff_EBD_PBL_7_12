// ============================================================
// Project 8 - Tiny ESP32 Quadcopter
// Sketch 00: Motor Test (slider -> all four motors, no sensor)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   The ESP32 creates a Wi-Fi network with your drone's name.
//   Your phone joins it, opens one page, and the page has two
//   big buttons (ARM / DISARM), one throttle slider, and four
//   small per-motor buttons (FRONT / RIGHT / BACK / LEFT).
//   The slider drives ALL FOUR motors at the same power.
//   A per-motor button spins ONE motor for 2 seconds at 25 %.
//   No gyro, no balancing - this is only "do my motors spin?".
//
// *** PROPELLERS OFF for this sketch. ***
//   The first run is with bare motors. Props go on only for
//   the bench thrust test, with the teacher, and only after
//   this sketch passed (all four spin, all four follow the
//   slider, nothing gets hot).
//
// USB in = battery out. Battery in = USB out. Never both.
//   Uploads happen on USB with the battery unplugged (the motors
//   cannot move - nothing feeds BAT+). Every motor run happens on
//   battery with the USB cable out.
//
// HOW TO USE (after uploading):
//   1. USB out. Battery in (the motors run from the battery).
//   2. Phone: Settings > Wi-Fi > your drone's network (DRONE-xx,
//      password on your station card).
//   3. Browser: 192.168.4.1
//   4. Slider on 0  ->  ARM  ->  press FRONT: only the FRONT motor
//      spins for 2 s. Then RIGHT, BACK, LEFT.
//   5. Slide up slowly: all four follow the slider  ->  DISARM.
//   The teacher's phone opens the same page: it shows everything
//   and its DISARM works, but only the phone that pressed ARM can
//   move the throttle or press a motor button.
//
// SAFETY BUILT INTO THE CODE (do not remove any of it):
//   - motor pins are driven LOW before PWM is switched on, so
//     the motors cannot twitch while the board boots
//   - the board always starts DISARMED
//   - the Wi-Fi network has a password and takes at most 2 phones
//     (pilot + teacher); the throttle listens only to the phone that
//     pressed ARM; DISARM works from every phone
//   - ARM is refused unless the slider is on 0
//   - DISARM is latched: after any DISARM (button or watchdog) the
//     motors stay off until the slider is back on 0 AND ARM is
//     pressed again - nothing re-arms by itself
//   - a DISARM that arrives from a phone that is NOT the pilot's (the
//     teacher's second stop button) also LOCKS the drone: it refuses
//     ARM until the battery has been out and in again
//   - the throttle can only CLIMB at a fixed rate (about half a
//     second from 0 to full) - a slider slam cannot slam the motors.
//     Going DOWN is never slowed: slider to 0, DISARM and the
//     watchdog cut power on the same step
//   - 100 % on the slider = full motor power (255 of 255)
//   - if the pilot's phone stops talking for 600 ms (page closed,
//     Wi-Fi lost, phone locked) the drone DISARMS by itself
//   - per-motor button: ONE motor, 2 s, 25 % power, only while
//     ARMED with the slider on 0; DISARM or the watchdog ends it early
//   - the page counts MOTOR TIME (this ARM / total since the battery
//     went in) beside the ARMED banner, and shows the drone's network
//     name, so the teacher can call "land" at 3:00 without a stopwatch
//
// LED ON THE BOARD (the small blue one):
//   short blink once a second = ready, disarmed
//   solid on                  = ARMED - motors can spin
// ============================================================

#include <WiFi.h>
#include <WebServer.h>

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

// ---- THROTTLE CEILING (100 % = the full 255) ----
const int MAX_THROTTLE_PERCENT = 100;
const int MAX_PWM = (255 * MAX_THROTTLE_PERCENT + 50) / 100;   // = 255
static_assert(MAX_THROTTLE_PERCENT >= 50 && MAX_THROTTLE_PERCENT <= 100, "Throttle ceiling must be 50..100 %");

// ---- THROTTLE CLIMB RATE (safety - do not change) ----
//   Each 4 ms step the throttle may rise by this many PWM counts
//   (of 255): 0 -> 255 takes about half a second. Down is instant.
const int THR_RISE_STEP = 2;

// ---- PER-MOTOR TEST (the FRONT / RIGHT / BACK / LEFT buttons) ----
const int           SOLO_DUTY = 64;       // ~25 % of 255 - spins a bare 8520, stays undramatic
const unsigned long SOLO_MS   = 2000;     // fixed 2 s run, then off by itself

// ---- MOTOR PINS (one MOSFET gate per motor - do not change) --------
//   Seen from above, the FRONT arm points away from you.
const int MOTOR_FRONT = 25;
const int MOTOR_RIGHT = 26;
const int MOTOR_BACK  = 14;
const int MOTOR_LEFT  = 27;
const int LED = 2;                        // blue LED on the DevKit

// ---- PWM (20 kHz: above hearing, smooth for coreless motors) -------
const int PWM_FREQ = 20000;
const int PWM_BITS = 8;                   // duty 0..255

// ESP32 Arduino core 3.x API: ledcAttach(pin, freq, bits) + ledcWrite(pin, duty).
// Core 2.x fallback (older IDE installs) uses numbered channels instead:
//   ledcSetup(ch, freq, bits); ledcAttachPin(pin, ch); ledcWrite(ch, duty);
// The #if below picks the right one automatically.
#if ESP_ARDUINO_VERSION_MAJOR >= 3
void pwmAttach(int pin)           { ledcAttach(pin, PWM_FREQ, PWM_BITS); }
void pwmWrite (int pin, int duty) { ledcWrite(pin, duty); }
#else
int  pwmChannel(int pin)          { return pin == MOTOR_FRONT ? 0 : pin == MOTOR_RIGHT ? 1 : pin == MOTOR_BACK ? 2 : 3; }
void pwmAttach(int pin)           { ledcSetup(pwmChannel(pin), PWM_FREQ, PWM_BITS); ledcAttachPin(pin, pwmChannel(pin)); }
void pwmWrite (int pin, int duty) { ledcWrite(pwmChannel(pin), duty); }
#endif

const unsigned long LOOP_US     = 4000;   // the motors are updated every 4 ms (same step as the flight sketch)
const unsigned long WATCHDOG_MS = 600;    // no pilot command for this long -> DISARM

WebServer server(80);
char      wifiName[16];                   // "DRONE-01" .. built from STATION at boot

bool          armed       = false;
int           throttlePct = 0;            // 0-100 from the pilot's slider (what the pilot ASKS for)
int           thrNow      = 0;            // 0..MAX_PWM, what the slider currently GIVES - climbs slowly toward the slider
int           duty        = 0;            // what the motors actually get right now (for the page)
uint32_t      pilotIP     = 0;            // the phone that pressed ARM - the only one the throttle listens to
bool          soloActive  = false; int soloIndex = 0; unsigned long soloStartMs = 0;   // per-motor test state
bool          lockedOut   = false;        // a DISARM from a phone that is not the pilot's - only a power cycle clears it
unsigned long armedAtMs   = 0;            // when the current ARM started (the page's motor-time counter)
unsigned long motorMsTot  = 0;            // motor time added up since the battery went in
unsigned long lastCmdMs   = 0;            // when the pilot's phone last talked to us
unsigned long lastStepUs  = 0;

// ---- motor helpers ----
void motorsOff() {
  duty = 0;
  pwmWrite(MOTOR_FRONT, 0); pwmWrite(MOTOR_RIGHT, 0);
  pwmWrite(MOTOR_BACK,  0); pwmWrite(MOTOR_LEFT,  0);
}

void motorsAll(int d) {
  duty = constrain(d, 0, MAX_PWM);
  pwmWrite(MOTOR_FRONT, duty); pwmWrite(MOTOR_RIGHT, duty);
  pwmWrite(MOTOR_BACK,  duty); pwmWrite(MOTOR_LEFT,  duty);
}

// The per-motor test: exactly one motor at SOLO_DUTY, the other three off.
void writeSolo() {
  duty = SOLO_DUTY;
  pwmWrite(MOTOR_FRONT, soloIndex == 0 ? SOLO_DUTY : 0); pwmWrite(MOTOR_RIGHT, soloIndex == 1 ? SOLO_DUTY : 0);
  pwmWrite(MOTOR_BACK,  soloIndex == 2 ? SOLO_DUTY : 0); pwmWrite(MOTOR_LEFT,  soloIndex == 3 ? SOLO_DUTY : 0);
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
  Serial.print("DISARMED - ");
  Serial.println(why);
}

// ---- the page the ESP32 serves to the phone ----
const char PAGE[] PROGMEM = R"rawliteral(
<!DOCTYPE html><html lang="he" dir="rtl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>בדיקת מנועים</title>
<style>
  body { margin:0; font-family:sans-serif; background:#10243e; color:#fff;
         display:flex; flex-direction:column; align-items:center; min-height:100vh;
         -webkit-user-select:none; user-select:none; touch-action:manipulation; }
  h1 { font-size:1.4rem; margin:14px 0 4px; }
  p  { margin:0 0 10px; color:#9fb6d4; font-size:0.85rem; text-align:center; }
  .st { font-size:1.2rem; font-weight:700; padding:8px 22px; border-radius:14px; margin:6px 0 14px; }
  .off { background:#334155; }  .on { background:#16a34a; }
  .hd { display:flex; align-items:center; gap:12px; }
  #tm { font-family:monospace; font-size:1rem; color:#9fb6d4; direction:ltr; }
  .row { display:flex; gap:14px; }
  button { border:none; border-radius:18px; font-size:1.6rem; font-weight:700; color:#fff;
           width:140px; height:90px; }
  button:active { transform:translateY(3px); }
  .arm { background:#2563eb; box-shadow:0 4px 0 #163a83; }
  .dis { background:#dc2626; box-shadow:0 4px 0 #7f1d1d; }
  .thr { margin-top:26px; width:90vw; max-width:420px; text-align:center; }
  .thr label { font-size:1.1rem; }  .thr b { font-size:1.6rem; }
  input[type=range] { -webkit-appearance:none; width:100%; height:16px; border-radius:8px;
                      background:#334155; margin:14px 0; }
  input[type=range]::-webkit-slider-thumb { -webkit-appearance:none; width:46px; height:46px;
                      border-radius:50%; background:#fbbf24; }
  input[type=range]:disabled { opacity:0.35; }
  .pwm { color:#9fb6d4; font-size:0.9rem; }
  .solo { display:grid; grid-template-columns:repeat(3,80px); grid-template-rows:repeat(3,44px); gap:6px; margin-top:18px; direction:ltr; }
  .solo button { width:80px; height:44px; font-size:0.9rem; border-radius:10px; background:#475569; box-shadow:0 3px 0 #1e293b; }
  .solo button:disabled { opacity:0.35; box-shadow:none; }
  .solo .f { grid-column:2; grid-row:1; }  .solo .l { grid-column:1; grid-row:2; }
  .solo .r { grid-column:3; grid-row:2; }  .solo .b { grid-column:2; grid-row:3; }
  .info { color:#9fb6d4; font-size:0.8rem; margin-top:8px; text-align:center; }
  #msg { color:#fbbf24; min-height:1.2em; }
</style></head><body>
<h1>&#128641; בדיקת מנועים</h1>
<p>מדחפים מפורקים! &middot; מחוון על 0 &larr; ARM &larr; מעלים לאט &larr; DISARM</p>
<div class="hd"><div id="st" class="st off">כבוי &middot; DISARMED</div><div id="tm">0:00 / 0:00</div></div>
<div class="row">
  <button class="arm" id="arm">ARM</button>
  <button class="dis" id="dis">DISARM</button>
</div>
<div class="thr">
  <label>מצערת <b id="pv">0%</b></label>
  <input type="range" id="sl" min="0" max="100" value="0">
  <div class="pwm">עוצמה למנועים: <span id="pwm">0</span> / <span id="max">255</span></div>
</div>
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
  setInterval(function(){ if (pilot) sendT(); }, 200);       // heartbeat: keeps the 600 ms watchdog fed - pilot page only
  setInterval(function(){                                    // live readout every 250 ms
    var s = seq;
    fetch('/data').then(function(r){ return r.json(); }).then(function(d){
      if (s != seq) return;                                  // asked before the last ARM press - stale
      me = (d.me == 1); solo = (d.solo == 1);
      setArmed(d.armed == 1);
      document.getElementById('pwm').textContent = d.duty;
      document.getElementById('max').textContent = d.max;
      document.getElementById('ph').textContent = d.phones;
      document.getElementById('nt').textContent = d.net;                             // must match the label on the frame
      document.getElementById('tm').textContent = mmss(d.as) + ' / ' + mmss(d.at);   // this ARM / since the battery went in
      if (d.lock == 1) msg.textContent = 'נעול - סוללה החוצה ופנימה';                     // another phone disarmed
    }).catch(function(){});
  }, 250);
</script>
</body></html>
)rawliteral";

// ---- web handlers ----
// Replies are "A" (armed) or "D" (disarmed), optionally followed by ":reason"
// (the reason is shown on the page, so it is in Hebrew).
void handleRoot() { server.send_P(200, "text/html; charset=utf-8", PAGE); }
void reply(const char* extra) { server.send(200, "text/plain", String(armed ? "A" : "D") + extra); }
uint32_t clientIP() { return (uint32_t)server.client().remoteIP(); }
bool fromPilot()    { return clientIP() == pilotIP; }

void handleArm() {
  if (armed)                                           { reply(":כבר חמוש");        return; }
  if (lockedOut)                                       { reply(":נעול - סוללה החוצה ופנימה"); return; }   // another phone disarmed: power cycle first
  if (throttlePct > 0 || server.arg("v").toInt() != 0) { reply(":המחוון לא על 0"); return; }   // slider not on 0 - refuse
  armed = true; thrNow = 0; lastCmdMs = millis(); armedAtMs = millis();
  pilotIP = clientIP();                                // this phone is the pilot until DISARM
  Serial.print("ARMED by "); Serial.print(server.client().remoteIP()); Serial.println(" - slider controls all four motors");
  reply("");
}

void handleDisarm() {                                  // open to EVERY phone - the teacher's too
  bool third = armed && !fromPilot();                  // not the pilot's phone = the teacher's stop button
  disarm(third ? "DISARM from another phone - locked until the battery is pulled" : "DISARM button", third);
  reply(third ? ":נעול - סוללה החוצה ופנימה" : "");
}

void handleThrottle() {
  if (!armed)       { throttlePct = 0; reply(""); return; }        // nothing is stored while disarmed (so ARM always starts from 0)
  if (!fromPilot()) { reply(":מסך צפייה - DISARM בלבד"); return; }  // not the pilot's phone: ignored
  int v = constrain(server.arg("v").toInt(), 0, 100);
  if (v > 0) endSolo();                                            // slider moved off 0 - a per-motor test ends first
  throttlePct = v;                                                 // the 4 ms step in loop() ramps the motors toward it
  lastCmdMs = millis();                                            // the watchdog counts only the pilot
  reply("");
}

void handleSolo() {                                                // /m?n=0..3 : FRONT / RIGHT / BACK / LEFT
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
  char buf[240];
  unsigned long armS = armed ? (millis() - armedAtMs) / 1000 : 0;                  // motor time of this ARM
  unsigned long totS = (motorMsTot + (armed ? millis() - armedAtMs : 0)) / 1000;   // and since the battery went in
  snprintf(buf, sizeof(buf),
           "{\"armed\":%d,\"duty\":%d,\"max\":%d,\"solo\":%d,\"phones\":%d,\"me\":%d,"
           "\"lock\":%d,\"as\":%lu,\"at\":%lu,\"net\":\"%s\"}",
           armed ? 1 : 0, duty, MAX_PWM, soloActive ? 1 : 0, (int)WiFi.softAPgetStationNum(),
           (!armed || fromPilot()) ? 1 : 0, lockedOut ? 1 : 0, armS, totS, wifiName);
  server.send(200, "application/json", buf);
}

void setup() {
  // FIRST THING, before anything else: motor pins LOW, so the
  // MOSFET gates are held off while the board starts up.
  pinMode(MOTOR_FRONT, OUTPUT); digitalWrite(MOTOR_FRONT, LOW);
  pinMode(MOTOR_RIGHT, OUTPUT); digitalWrite(MOTOR_RIGHT, LOW);
  pinMode(MOTOR_BACK,  OUTPUT); digitalWrite(MOTOR_BACK,  LOW);
  pinMode(MOTOR_LEFT,  OUTPUT); digitalWrite(MOTOR_LEFT,  LOW);
  pinMode(LED, OUTPUT);

  // Now switch the pins to PWM and write 0 to every one of them.
  pwmAttach(MOTOR_FRONT); pwmAttach(MOTOR_RIGHT);
  pwmAttach(MOTOR_BACK);  pwmAttach(MOTOR_LEFT);
  motorsOff();
  armed = false;                          // always boot DISARMED

  Serial.begin(115200);
  delay(300);
  Serial.println();
  Serial.println("===== PROJECT 8 - MOTOR TEST (props OFF!) =====");
  Serial.print("Throttle ceiling: "); Serial.print(MAX_THROTTLE_PERCENT);
  Serial.print(" % = "); Serial.print(MAX_PWM); Serial.println(" / 255");
  Serial.print("Motor pins:       FRONT "); Serial.print(MOTOR_FRONT); Serial.print("  RIGHT "); Serial.print(MOTOR_RIGHT);
  Serial.print("  BACK ");                  Serial.print(MOTOR_BACK);  Serial.print("  LEFT ");  Serial.println(MOTOR_LEFT);

  if (strlen(DRONE_WIFI_PASS) < 8) {      // the ESP32 silently fails to start an AP with a short password
    Serial.println("ERROR: Wi-Fi password must be 8+ characters. Halting.");
    while (true) { digitalWrite(LED, !digitalRead(LED)); delay(40); }
  }

  snprintf(wifiName, sizeof(wifiName), "DRONE-%02d", STATION);
  WiFi.softAP(wifiName, DRONE_WIFI_PASS, 1, 0, 2);   // WPA2, channel 1, visible, at most 2 phones (pilot + teacher)
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
  lastStepUs = micros();
}

void loop() {
  server.handleClient();

  // Watchdog: the pilot's page sends a throttle message every 200 ms while
  // armed. Three missed messages = phone is gone = stop the motors.
  if (armed && millis() - lastCmdMs > WATCHDOG_MS) disarm("no command for 600 ms - phone lost?");
  if (soloActive && millis() - soloStartMs >= SOLO_MS) endSolo();   // the 2 s per-motor test is over

  // Every 4 ms: move the motors toward the slider. UP by at most
  // THR_RISE_STEP counts per step, DOWN instantly.
  unsigned long nowUs = micros();
  if (nowUs - lastStepUs >= LOOP_US) {
    lastStepUs = nowUs;
    int thrTarget = armed ? throttlePct * MAX_PWM / 100 : 0;   // 100 % slider = MAX_PWM
    if (thrTarget > thrNow) thrNow = min(thrNow + THR_RISE_STEP, thrTarget);   // up: limited
    else                    thrNow = thrTarget;                                // down: instant
    if (!armed)          motorsOff();
    else if (soloActive) writeSolo();                           // per-motor test running: one motor only
    else                 motorsAll(thrNow);
  }

  // LED: solid when armed, short blink once a second when ready.
  digitalWrite(LED, armed ? HIGH : ((millis() % 1000) < 100 ? HIGH : LOW));
}
