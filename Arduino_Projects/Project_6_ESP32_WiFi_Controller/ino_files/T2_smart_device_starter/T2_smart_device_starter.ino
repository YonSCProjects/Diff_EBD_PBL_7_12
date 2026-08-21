// ============================================================
// Project 6 - ESP32 Wi-Fi Controller (weather station)
// Tier 2 Starter: YOUR smart device
// ============================================================
//
// Same station as Sketch 03 - plus an OUTPUT that reacts when
// the humidity crosses a threshold you choose. Every block
// marked  ==== CHANGE THIS ====  is a decision from the choice
// cards. Change, upload, refresh the page on the phone.
//
// Breathe on the sensor: humidity climbs past your threshold,
// the output switches on, the screen and the page say ALERT.
// ============================================================

#include "DHT.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <WebServer.h>

// ==== CHANGE THIS 1: your station's identity =================
const char* STATION_WIFI_NAME    = "WEATHER-01";        // Wi-Fi name (English/numbers)
const char* STATION_DISPLAY_NAME = "תחנת מזג האוויר שלי"; // the name on the page
// ============================================================

// ==== CHANGE THIS 2: your output and its threshold ===========
// Output: LED (with 220 ohm) or active buzzer - both are simple
// on/off outputs on one pin. (Servo "gauge" = the Claude Code card.)
const int   OUTPUT_PIN         = 26;    // LED on 26, or buzzer on 27
const float HUMIDITY_THRESHOLD = 60.0;  // % - above this, the output turns ON
// Typical room: 35-55%. A breath on the sensor reaches 70-90%.
// ============================================================

// ==== CHANGE THIS 3: your page's colors ======================
const char* PAGE_BACKGROUND = "#0f2a3d";   // page background
const char* TILE_COLOR      = "#17415c";   // the reading tiles
// ============================================================

const int DHT_PIN = 4;
DHT dht(DHT_PIN, DHT22);
Adafruit_SSD1306 display(128, 64, &Wire, -1);
WebServer server(80);

float lastTemp = 0, lastHum = 0;
bool  haveReading = false, alertOn = false;
unsigned long lastRead = 0;

String buildPage() {
  String p = F(
    "<!DOCTYPE html><html lang='he' dir='rtl'><head>"
    "<meta charset='utf-8'>"
    "<meta name='viewport' content='width=device-width, initial-scale=1'>"
    "<title>%TITLE%</title>"
    "<style>"
    "body{margin:0;font-family:sans-serif;background:%BG%;color:#fff;"
    "display:flex;flex-direction:column;align-items:center;min-height:100vh}"
    "h1{font-size:1.3rem;margin:18px 0 10px}"
    ".tiles{display:grid;grid-template-columns:1fr 1fr;grid-gap:14px;width:92vw;max-width:520px}"
    ".tile{background:%TILE%;border-radius:18px;padding:18px 10px;text-align:center}"
    ".label{font-size:.95rem;color:#cfe3ef;margin-bottom:6px}"
    ".value{font-size:2.6rem;font-weight:700}"
    ".unit{font-size:1.1rem;color:#cfe3ef}"
    ".alert{margin-top:16px;width:92vw;max-width:520px;border-radius:18px;padding:16px;"
    "text-align:center;font-size:1.2rem;font-weight:700;background:#1f5a3a}"
    ".alert.on{background:#b91c1c}"
    "p{color:#cfe3ef;font-size:.85rem;margin-top:14px}"
    "</style></head><body>"
    "<h1>&#127777; %TITLE%</h1>"
    "<div class='tiles'>"
    "<div class='tile'><div class='label'>טמפרטורה</div>"
    "<div class='value'><span id='t'>--</span><span class='unit'> &deg;C</span></div></div>"
    "<div class='tile'><div class='label'>לחות</div>"
    "<div class='value'><span id='h'>--</span><span class='unit'> %</span></div></div>"
    "</div>"
    "<div class='alert' id='a'>הכול רגיל</div>"
    "<p>סף ההתראה: %THR%% לחות &middot; מתעדכן כל 2 שניות</p>"
    "<script>"
    "function refresh(){fetch('/data').then(function(r){return r.json()}).then(function(d){"
    "document.getElementById('t').textContent=d.t;"
    "document.getElementById('h').textContent=d.h;"
    "var a=document.getElementById('a');"
    "a.textContent=d.alert?'התראה! לחות גבוהה':'הכול רגיל';"
    "a.className=d.alert?'alert on':'alert';}).catch(function(){});}"
    "refresh();setInterval(refresh,2000);"
    "</script></body></html>");
  p.replace("%TITLE%", STATION_DISPLAY_NAME);
  p.replace("%BG%", PAGE_BACKGROUND);
  p.replace("%TILE%", TILE_COLOR);
  p.replace("%THR%", String(HUMIDITY_THRESHOLD, 0));
  return p;
}

void handleRoot() { server.send(200, "text/html; charset=utf-8", buildPage()); }

void handleData() {
  String json = "{\"t\":\"" + (haveReading ? String(lastTemp, 1) : "--") +
                "\",\"h\":\"" + (haveReading ? String(lastHum, 0) : "--") +
                "\",\"alert\":" + (alertOn ? "true" : "false") + "}";
  server.send(200, "application/json", json);
}

void showOnScreen() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.print(STATION_WIFI_NAME);
  display.println("  192.168.4.1");
  if (haveReading) {
    display.setTextSize(2);
    display.setCursor(0, 16);
    display.print(lastTemp, 1);
    display.println(" C");
    display.setCursor(0, 38);
    display.print(lastHum, 0);
    display.println(" %");
    display.setTextSize(1);
    display.setCursor(70, 46);
    display.println(alertOn ? "ALERT!" : "ok");
  } else {
    display.setCursor(0, 24);
    display.println("No reading -");
    display.println("check sensor wires");
  }
  display.display();
}

void setup() {
  pinMode(OUTPUT_PIN, OUTPUT);
  digitalWrite(OUTPUT_PIN, LOW);
  Serial.begin(115200);
  dht.begin();
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("Screen not found - check SDA/SCL and the address");
  }
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.display();

  WiFi.softAP(STATION_WIFI_NAME);
  Serial.print("Network: ");
  Serial.println(STATION_WIFI_NAME);
  Serial.print("Page:    http://");
  Serial.println(WiFi.softAPIP());

  server.on("/", handleRoot);
  server.on("/data", handleData);
  server.begin();
}

void loop() {
  server.handleClient();
  if (millis() - lastRead >= 2000) {
    lastRead = millis();
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    if (!isnan(h) && !isnan(t)) { lastHum = h; lastTemp = t; haveReading = true; }
    alertOn = haveReading && (lastHum >= HUMIDITY_THRESHOLD);
    digitalWrite(OUTPUT_PIN, alertOn ? HIGH : LOW);   // the output follows the alert
    showOnScreen();
  }
}
