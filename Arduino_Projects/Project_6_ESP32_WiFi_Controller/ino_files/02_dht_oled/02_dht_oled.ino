// ============================================================
// Project 6 - ESP32 Wi-Fi Controller (weather station)
// Sketch 02: Readings on the OLED screen (your first I2C device)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   Same readings as Sketch 01 - now shown on the small screen
//   attached to the ESP32. No computer needed once uploaded.
//
// LIBRARIES NEEDED (Library Manager):
//   "Adafruit SSD1306" - installing it also offers
//   "Adafruit GFX Library": say yes to both.
//
// I2C WIRING (the screen, 4 pins) - two wires carry everything:
//   VCC -> 3V3        GND -> GND
//   SDA -> GPIO 21    SCL -> GPIO 22
//   The screen answers to address 0x3C (printed on most modules).
//
// WHAT SUCCESS LOOKS LIKE:
//   The screen shows two big lines:  24.3 C  /  41 %
// ============================================================

#include "DHT.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const int DHT_PIN = 4;
DHT dht(DHT_PIN, DHT22);

Adafruit_SSD1306 display(128, 64, &Wire, -1);   // 128x64 pixels, I2C

void setup() {
  Serial.begin(115200);
  dht.begin();

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {   // the screen's I2C address
    Serial.println("Screen not found - check SDA/SCL and the address");
    while (true) delay(1000);
  }
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(2);
  display.setCursor(0, 20);
  display.println("Hello!");
  display.display();
  delay(1000);
}

void loop() {
  float humidity = dht.readHumidity();
  float temp     = dht.readTemperature();

  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("Weather station");

  if (isnan(humidity) || isnan(temp)) {
    display.setTextSize(1);
    display.setCursor(0, 24);
    display.println("No reading -");
    display.println("check sensor wires");
  } else {
    display.setTextSize(2);
    display.setCursor(0, 18);
    display.print(temp, 1);
    display.println(" C");
    display.setCursor(0, 42);
    display.print(humidity, 0);
    display.println(" %");
  }
  display.display();
  delay(2000);
}
