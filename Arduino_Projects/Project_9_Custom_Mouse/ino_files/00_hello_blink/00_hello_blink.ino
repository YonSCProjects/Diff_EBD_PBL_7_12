/*
 * Project 9 — step 2: the ESP32-S3 is alive.
 * Blinks the small RGB LED that is already on the DevKit board — no wiring yet.
 *
 * Board: "ESP32S3 Dev Module" (Tools → Board → esp32).
 * This sketch needs no special USB mode and no libraries.
 */

#ifndef RGB_BUILTIN
#define RGB_BUILTIN 48   // the DevKitC-1 onboard RGB LED lives on GPIO 48
#endif

void setup() {
}

void loop() {
  rgbLedWrite(RGB_BUILTIN, 0, 32, 0);   // green
  delay(400);
  rgbLedWrite(RGB_BUILTIN, 0, 0, 32);   // blue
  delay(400);
  rgbLedWrite(RGB_BUILTIN, 32, 8, 0);   // orange
  delay(400);
  rgbLedWrite(RGB_BUILTIN, 0, 0, 0);    // off
  delay(400);
}
