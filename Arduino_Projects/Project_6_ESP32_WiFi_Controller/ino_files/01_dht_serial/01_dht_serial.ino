// ============================================================
// Project 6 - ESP32 Wi-Fi Controller (weather station)
// Sketch 01: DHT22 to Serial (the sensor gives us numbers)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   Every 2 seconds it asks the DHT22 for the temperature and
//   the humidity and prints both to the Serial Monitor.
//
// LIBRARY NEEDED (one-time, Library Manager):
//   "DHT sensor library" by Adafruit - installing it also
//   offers "Adafruit Unified Sensor": say yes to both.
//
// WIRING (DHT22 module, 3 pins):
//   +  (VCC)  -> 3V3 on the ESP32   (NOT 5V - the ESP32 is 3.3V)
//   out/DATA -> GPIO 4
//   -  (GND)  -> GND
//
// WHAT SUCCESS LOOKS LIKE (Serial Monitor, 115200):
//   Temp: 24.3 C   Humidity: 41.0 %
//   Breathe on the sensor - the humidity jumps within seconds.
// ============================================================

#include "DHT.h"

const int DHT_PIN = 4;          // the sensor's data wire
DHT dht(DHT_PIN, DHT22);

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  float humidity = dht.readHumidity();
  float temp     = dht.readTemperature();   // Celsius

  if (isnan(humidity) || isnan(temp)) {
    Serial.println("No reading - check the three sensor wires");
  } else {
    Serial.print("Temp: ");
    Serial.print(temp, 1);
    Serial.print(" C   Humidity: ");
    Serial.print(humidity, 1);
    Serial.println(" %");
  }
  delay(2000);   // the DHT22 needs 2 seconds between readings
}
