/*
 * Project 9 — step 6: a whole basic mouse.
 * Clicks + optical sensor + the front scroll wheel (and its push = middle click).
 *
 * Tools settings:  Board "ESP32S3 Dev Module", USB Mode "USB-OTG (TinyUSB)".
 * Library:         "PMW3360 Module" by SunjunKim.
 *
 * New wiring in this step (J2, the 11 mm front encoder):
 *   A → GPIO 4 · B → GPIO 5 · PUSH → GPIO 6 · C(common) → GND
 */

#include "USB.h"
#include "USBHIDMouse.h"
#include <PMW3360.h>

USBHIDMouse Mouse;
PMW3360 sensor;

const int PIN_CS = 10;
const int CPI    = 800;

const int PIN_LEFT   = 1;
const int PIN_RIGHT  = 2;
const int PIN_F_A    = 4;
const int PIN_F_B    = 5;
const int PIN_F_PUSH = 6;

const unsigned long DEBOUNCE_MS = 8;

struct Btn { int pin; uint8_t hid; bool down = false; unsigned long last = 0; };
Btn btns[] = {
  { PIN_LEFT,   MOUSE_LEFT   },
  { PIN_RIGHT,  MOUSE_RIGHT  },
  { PIN_F_PUSH, MOUSE_MIDDLE },
};

int lastA = HIGH;

void setup() {
  for (Btn &b : btns) pinMode(b.pin, INPUT_PULLUP);
  pinMode(PIN_F_A, INPUT_PULLUP);
  pinMode(PIN_F_B, INPUT_PULLUP);
  Mouse.begin();
  USB.begin();
  sensor.begin(PIN_CS);
  sensor.setCPI(CPI);
}

void loop() {
  unsigned long now = millis();

  // clicks
  for (Btn &b : btns) {
    bool pressed = (digitalRead(b.pin) == LOW);
    if (pressed != b.down && now - b.last > DEBOUNCE_MS) {
      b.down = pressed; b.last = now;
      if (pressed) Mouse.press(b.hid); else Mouse.release(b.hid);
    }
  }

  // movement
  PMW3360_DATA d = sensor.readBurst();
  if (d.isOnSurface && d.isMotion) {
    Mouse.move(constrain(-d.dx, -127, 127), constrain(-d.dy, -127, 127));
  }

  // scroll: one detent of the wheel = one scroll step
  int a = digitalRead(PIN_F_A);
  if (a != lastA && a == LOW) {
    Mouse.move(0, 0, digitalRead(PIN_F_B) == HIGH ? 1 : -1);
  }
  lastA = a;

  delay(1);
}
