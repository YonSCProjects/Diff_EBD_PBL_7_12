// ============================================================
// Project 5 - Remote-Controlled Car
// Sketch 01: Wi-Fi Drive (the car becomes its own network)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   The ESP32 creates a Wi-Fi network with your car's name.
//   Your phone joins that network, opens one web page, and the
//   buttons on that page drive the car. No app, no internet -
//   the car IS the network.
//
// HOW TO DRIVE (after uploading):
//   1. On the phone: Settings > Wi-Fi > connect to your car's
//      network (the CAR_WIFI_NAME below).
//   2. Open the browser and go to:  192.168.4.1
//   3. Hold a button to drive. Let go - the car stops.
//
// IMPORTANT - BEFORE UPLOADING:
//   Prop the car up so the wheels spin in the AIR for the
//   first test. Only then drive on the floor.
//
// IF ONE SIDE SPINS BACKWARD:
//   Normal, not a mistake. Swap that side's two wires at the
//   L298N outputs (OUT1 <-> OUT2 for left, OUT3 <-> OUT4 for
//   right) and test again.
// ============================================================

#include <WiFi.h>
#include <WebServer.h>

// ---- YOUR CAR'S NAME (English letters/numbers for the Wi-Fi) ----
const char* CAR_WIFI_NAME = "CAR-01";     // change 01 to your station number

// ---- SPEED (0-200 maximum! fresh batteries are strong) ----
const int SPEED      = 170;   // driving speed
const int TURN_SPEED = 150;   // pivot-turn speed

// ---- PIN NUMBERS (L298N driver: six pins in a row on the ESP32) ----
const int ENA = 32;  // left side speed  (PWM)
const int IN1 = 33;  // left side direction
const int IN2 = 25;  // left side direction
const int IN3 = 26;  // right side direction
const int IN4 = 27;  // right side direction
const int ENB = 14;  // right side speed (PWM)
// Each L298N channel drives BOTH motors of one side, wired in
// parallel - two motors that behave like one big motor.

WebServer server(80);

// ---- driving helpers ----
void stopCar() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void setSides(bool leftFwd, bool rightFwd, int leftSpd, int rightSpd) {
  digitalWrite(IN1, leftFwd ? HIGH : LOW);
  digitalWrite(IN2, leftFwd ? LOW  : HIGH);
  digitalWrite(IN3, rightFwd ? HIGH : LOW);
  digitalWrite(IN4, rightFwd ? LOW  : HIGH);
  analogWrite(ENA, leftSpd);
  analogWrite(ENB, rightSpd);
}

// ---- the driving page the ESP32 serves to the phone ----
const char PAGE[] PROGMEM = R"rawliteral(
<!DOCTYPE html><html lang="he" dir="rtl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
<title>המכונית שלי</title>
<style>
  body { margin:0; font-family:sans-serif; background:#10243e; color:#fff;
         display:flex; flex-direction:column; align-items:center; min-height:100vh;
         -webkit-user-select:none; user-select:none; touch-action:manipulation; }
  h1 { font-size:1.4rem; margin:14px 0 4px; }
  p  { margin:0 0 10px; color:#9fb6d4; font-size:0.85rem; }
  .pad { display:grid; grid-template-columns:90px 90px 90px; grid-gap:12px;
         justify-content:center; margin-top:10px; }
  button { border:none; border-radius:18px; font-size:2rem; color:#fff;
           background:#2563eb; height:90px; box-shadow:0 4px 0 #163a83; }
  button:active { transform:translateY(3px); box-shadow:0 1px 0 #163a83; }
  .stop { background:#dc2626; box-shadow:0 4px 0 #7f1d1d; font-size:1.3rem; font-weight:700; }
  .ghost { visibility:hidden; }
</style></head><body>
<h1>&#128663; המכונית שלי</h1>
<p>מחזיקים כפתור כדי לנסוע &middot; עוזבים &mdash; והמכונית עוצרת</p>
<div class="pad">
  <button class="ghost"></button>
  <button id="f">&#8679;</button>
  <button class="ghost"></button>
  <button id="r">&#8680;</button>
  <button class="stop" id="s">עצור</button>
  <button id="l">&#8678;</button>
  <button class="ghost"></button>
  <button id="b">&#8681;</button>
  <button class="ghost"></button>
</div>
<script>
  function go(c){ fetch('/go?d='+c).catch(function(){}); }
  ['f','b','l','r'].forEach(function(id){
    var el = document.getElementById(id);
    el.addEventListener('pointerdown', function(e){ e.preventDefault(); go(id); });
    el.addEventListener('pointerup',   function(){ go('s'); });
    el.addEventListener('pointercancel', function(){ go('s'); });
    el.addEventListener('contextmenu', function(e){ e.preventDefault(); });
  });
  document.getElementById('s').addEventListener('pointerdown', function(){ go('s'); });
</script>
</body></html>
)rawliteral";

void handleRoot() { server.send_P(200, "text/html; charset=utf-8", PAGE); }

void handleGo() {
  String d = server.arg("d");
  if      (d == "f") setSides(true,  true,  SPEED, SPEED);        // forward
  else if (d == "b") setSides(false, false, SPEED, SPEED);        // back
  else if (d == "l") setSides(false, true,  TURN_SPEED, TURN_SPEED); // pivot left
  else if (d == "r") setSides(true,  false, TURN_SPEED, TURN_SPEED); // pivot right
  else               stopCar();                                   // anything else = stop
  server.send(200, "text/plain", "ok");
}

void setup() {
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT); pinMode(ENB, OUTPUT);
  stopCar();

  Serial.begin(115200);
  WiFi.softAP(CAR_WIFI_NAME);            // the car becomes a Wi-Fi network
  Serial.print("Network: ");
  Serial.println(CAR_WIFI_NAME);
  Serial.print("Page:    http://");
  Serial.println(WiFi.softAPIP());       // this prints 192.168.4.1

  server.on("/", handleRoot);
  server.on("/go", handleGo);
  server.begin();
}

void loop() {
  server.handleClient();
}
