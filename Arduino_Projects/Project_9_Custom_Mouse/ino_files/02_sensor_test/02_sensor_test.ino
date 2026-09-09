/*
 * Project 9 — step 5: the cursor moves.
 * The PMW3360 optical sensor — the mouse's eye — drives the cursor for the first time.
 *
 * Tools settings:  Board "ESP32S3 Dev Module", USB Mode "USB-OTG (TinyUSB)".
 * Library:         "PMW3360 Module" by SunjunKim  (Library Manager). It carries the
 *                  sensor's firmware blob and uploads it at begin().
 *
 * Wiring (J1, harness under 40 mm — these are the S3's default SPI pins):
 *   CS → GPIO 10 · MOSI → GPIO 11 · SCK → GPIO 12 · MISO → GPIO 13
 *   MOTION → GPIO 14 (unused here) · VCC → 3V3 · GND → GND
 */

#include "USB.h"
#include "USBHIDMouse.h"
#include <PMW3360.h>

USBHIDMouse Mouse;
PMW3360 sensor;

const int PIN_CS = 10;
const int CPI    = 800;   // a gentle starting speed

void setup() {
  Serial.begin(115200);
  Mouse.begin();
  USB.begin();

  if (!sensor.begin(PIN_CS)) {
    // the sensor did not answer — the card's stuck box says what to check
    while (true) {
      Serial.println("PMW3360 not found - check the 7 wires of J1");
      delay(1000);
    }
  }
  sensor.setCPI(CPI);
}

void loop() {
  PMW3360_DATA d = sensor.readBurst();
  if (d.isOnSurface && d.isMotion) {
    // the sensor reports movement mirrored relative to a hand-held mouse
    Mouse.move(constrain(-d.dx, -127, 127), constrain(-d.dy, -127, 127));
  }
  delay(2);
}
