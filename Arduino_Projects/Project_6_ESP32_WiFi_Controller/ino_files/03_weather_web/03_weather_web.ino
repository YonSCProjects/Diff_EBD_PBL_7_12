// ============================================================
// Project 6 - ESP32 Wi-Fi Controller (weather station)
// Sketch 03: Weather page (screen + phone, live)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   The readings show on the OLED screen AND on a web page the
//   ESP32 serves over its own Wi-Fi network. The page refreshes
//   itself every 2 seconds - no app, no internet.
//
// HOW TO SEE IT (after uploading):
//   1. Phone: Settings > Wi-Fi > connect to WEATHER-01 (below)
//   2. Browser:  192.168.4.1
//   3. Breathe on the sensor and watch the humidity tile jump
//      on the phone - from across the room.
// ============================================================

#include "DHT.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <WebServer.h>

// ---- YOUR STATION'S NAME (English letters/numbers for the Wi-Fi) ----
const char* STATION_WIFI_NAME = "WEATHER-01";   // change 01 to your station number

const int DHT_PIN = 4;
DHT dht(DHT_PIN, DHT22);
Adafruit_SSD1306 display(128, 64, &Wire, -1);
WebServer server(80);

float lastTemp = 0, lastHum = 0;
bool  haveReading = false;
unsigned long lastRead = 0;

// ---- the weather page the ESP32 serves to the phone ----
const char PAGE[] PROGMEM = R"rawliteral(
<!DOCTYPE html><html lang="he" dir="rtl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>תחנת מזג האוויר שלי</title>
<style>
  body { margin:0; font-family:sans-serif; background:#0f2a3d; color:#fff;
         display:flex; flex-direction:column; align-items:center; min-height:100vh; }
  h1 { font-size:1.3rem; margin:18px 0 10px; }
  .tiles { display:grid; grid-template-columns:1fr 1fr; grid-gap:14px; width:92vw; max-width:520px; }
  .tile { background:#17415c; border-radius:18px; padding:18px 10px; text-align:center; }
  .label { font-size:.95rem; color:#a9c7dc; margin-bottom:6px; }
  .value { font-size:2.6rem; font-weight:700; }
  .unit  { font-size:1.1rem; color:#a9c7dc; }
  p { color:#a9c7dc; font-size:.85rem; margin-top:16px; }
</style></head><body>
<h1>&#127777; תחנת מזג האוויר שלי</h1>
<div class="tiles">
  <div class="tile"><div class="label">טמפרטורה</div>
    <div class="value"><span id="t">--</span><span class="unit"> °C</span></div></div>
  <div class="tile"><div class="label">לחות</div>
    <div class="value"><span id="h">--</span><span class="unit"> %</span></div></div>
</div>
<p>מתעדכן כל 2 שניות &middot; נושפים על החיישן ורואים את הלחות קופצת</p>
<script>
  function refresh(){
    fetch('/data').then(function(r){ return r.json(); }).then(function(d){
      document.getElementById('t').textContent = d.t;
      document.getElementById('h').textContent = d.h;
    }).catch(function(){});
  }
  refresh(); setInterval(refresh, 2000);
</script>
</body></html>
)rawliteral";

void handleRoot() { server.send_P(200, "text/html; charset=utf-8", PAGE); }

void handleData() {
  String json = "{\"t\":\"" + (haveReading ? String(lastTemp, 1) : "--") +
                "\",\"h\":\"" + (haveReading ? String(lastHum, 0) : "--") + "\"}";
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
    display.setCursor(0, 18);
    display.print(lastTemp, 1);
    display.println(" C");
    display.setCursor(0, 42);
    display.print(lastHum, 0);
    display.println(" %");
  } else {
    display.setCursor(0, 24);
    display.println("No reading -");
    display.println("check sensor wires");
  }
  display.display();
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("Screen not found - check SDA/SCL and the address");
  }
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.display();

  WiFi.softAP(STATION_WIFI_NAME);            // the station becomes a Wi-Fi network
  Serial.print("Network: ");
  Serial.println(STATION_WIFI_NAME);
  Serial.print("Page:    http://");
  Serial.println(WiFi.softAPIP());           // this prints 192.168.4.1

  server.on("/", handleRoot);
  server.on("/data", handleData);
  server.begin();
}

void loop() {
  server.handleClient();
  if (millis() - lastRead >= 2000) {         // read the sensor every 2 seconds
    lastRead = millis();
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    if (!isnan(h) && !isnan(t)) { lastHum = h; lastTemp = t; haveReading = true; }
    showOnScreen();
  }
}
