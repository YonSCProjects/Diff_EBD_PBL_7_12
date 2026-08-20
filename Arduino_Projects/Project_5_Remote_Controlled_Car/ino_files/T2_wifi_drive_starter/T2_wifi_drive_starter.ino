// ============================================================
// Project 5 - Remote-Controlled Car
// Tier 2 Starter: YOUR driving page
// ============================================================
//
// This is the same Wi-Fi drive sketch as Sketch 01 - but now
// it is YOURS. Every block marked  ==== CHANGE THIS ====  is
// a decision you make on the choice cards. Change, upload,
// refresh the page on the phone, feel the difference.
//
// After uploading: phone > Wi-Fi > your car's network,
// browser > 192.168.4.1. Hold to drive, release to stop.
// ============================================================

#include <WiFi.h>
#include <WebServer.h>

// ==== CHANGE THIS 1: your car's identity =====================
const char* CAR_WIFI_NAME    = "CAR-01";        // Wi-Fi name (English/numbers)
const char* CAR_DISPLAY_NAME = "המכונית שלי";   // the name on the page title
// ============================================================

// ==== CHANGE THIS 2: speed profile (pick ONE, 0-200 max!) ====
// Calm     (רגוע):    SPEED = 130, TURN_SPEED = 110
// Balanced (מאוזן):   SPEED = 170, TURN_SPEED = 150
// Sporty   (ספורטיבי): SPEED = 200, TURN_SPEED = 170
const int SPEED      = 170;
const int TURN_SPEED = 150;
// ============================================================

// ==== CHANGE THIS 3: your page's colors ======================
const char* PAGE_BACKGROUND = "#10243e";   // page background
const char* BUTTON_COLOR    = "#2563eb";   // driving buttons
// Color picking: search "html color picker" and copy the #code
// ============================================================

// ---- PIN NUMBERS (six pins in a row - do not change) --------
const int ENA = 32;  // left side speed  (PWM)
const int IN1 = 33;  // left side direction
const int IN2 = 25;  // left side direction
const int IN3 = 26;  // right side direction
const int IN4 = 27;  // right side direction
const int ENB = 14;  // right side speed (PWM)

WebServer server(80);

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

// ---- the driving page (your name and colors go in automatically) ----
String buildPage() {
  String p = F(
    "<!DOCTYPE html><html lang='he' dir='rtl'><head>"
    "<meta charset='utf-8'>"
    "<meta name='viewport' content='width=device-width, initial-scale=1, user-scalable=no'>"
    "<title>%TITLE%</title>"
    "<style>"
    "body{margin:0;font-family:sans-serif;background:%BG%;color:#fff;"
    "display:flex;flex-direction:column;align-items:center;min-height:100vh;"
    "-webkit-user-select:none;user-select:none;touch-action:manipulation}"
    "h1{font-size:1.4rem;margin:14px 0 4px}"
    "p{margin:0 0 10px;color:#cbd5e1;font-size:.85rem}"
    ".pad{display:grid;grid-template-columns:90px 90px 90px;grid-gap:12px;"
    "justify-content:center;margin-top:10px}"
    "button{border:none;border-radius:18px;font-size:2rem;color:#fff;"
    "background:%BTN%;height:90px}"
    "button:active{transform:translateY(3px)}"
    ".stop{background:#dc2626;font-size:1.3rem;font-weight:700}"
    ".ghost{visibility:hidden}"
    "</style></head><body>"
    "<h1>&#128663; %TITLE%</h1>"
    "<p>מחזיקים כפתור כדי לנסוע &middot; עוזבים &mdash; והמכונית עוצרת</p>"
    "<div class='pad'>"
    "<button class='ghost'></button><button id='f'>&#8679;</button><button class='ghost'></button>"
    "<button id='r'>&#8680;</button><button class='stop' id='s'>עצור</button><button id='l'>&#8678;</button>"
    "<button class='ghost'></button><button id='b'>&#8681;</button><button class='ghost'></button>"
    "</div>"
    "<script>"
    "function go(c){fetch('/go?d='+c).catch(function(){})}"
    "['f','b','l','r'].forEach(function(id){var el=document.getElementById(id);"
    "el.addEventListener('pointerdown',function(e){e.preventDefault();go(id)});"
    "el.addEventListener('pointerup',function(){go('s')});"
    "el.addEventListener('pointercancel',function(){go('s')});"
    "el.addEventListener('contextmenu',function(e){e.preventDefault()});});"
    "document.getElementById('s').addEventListener('pointerdown',function(){go('s')});"
    "</script></body></html>");
  p.replace("%TITLE%", CAR_DISPLAY_NAME);
  p.replace("%BG%", PAGE_BACKGROUND);
  p.replace("%BTN%", BUTTON_COLOR);
  return p;
}

void handleRoot() { server.send(200, "text/html; charset=utf-8", buildPage()); }

void handleGo() {
  String d = server.arg("d");
  if      (d == "f") setSides(true,  true,  SPEED, SPEED);
  else if (d == "b") setSides(false, false, SPEED, SPEED);
  else if (d == "l") setSides(false, true,  TURN_SPEED, TURN_SPEED);
  else if (d == "r") setSides(true,  false, TURN_SPEED, TURN_SPEED);
  else               stopCar();
  server.send(200, "text/plain", "ok");
}

void setup() {
  pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT); pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT); pinMode(ENB, OUTPUT);
  stopCar();

  Serial.begin(115200);
  WiFi.softAP(CAR_WIFI_NAME);
  Serial.print("Network: ");
  Serial.println(CAR_WIFI_NAME);
  Serial.print("Page:    http://");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleRoot);
  server.on("/go", handleGo);
  server.begin();
}

void loop() {
  server.handleClient();
}
