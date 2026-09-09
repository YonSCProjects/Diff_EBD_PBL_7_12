/*
 * Project 9 — step 3: the first click.
 * Two silent switches on the breadboard become the LEFT and RIGHT buttons of a real
 * USB mouse. Plug the board in, upload, and pressing the switch clicks on screen.
 *
 * Tools settings that MUST be set (like the card says):
 *   Board:    "ESP32S3 Dev Module"
 *   USB Mode: "USB-OTG (TinyUSB)"     ← without this the computer sees no mouse
 * Libraries: none (USB HID is built into the ESP32 board package).
 *
 * Wiring: each switch between its GPIO and GND (internal pull-ups do the rest).
 *   LEFT  → GPIO 1        RIGHT → GPIO 2
 */

#include "USB.h"
#include "USBHIDMouse.h"

USBHIDMouse Mouse;

const int PIN_LEFT  = 1;
const int PIN_RIGHT = 2;
const unsigned long DEBOUNCE_MS = 8;

struct Btn {
  int pin;
  uint8_t hid;
  bool down = false;
  unsigned long last = 0;
};

Btn btns[] = { { PIN_LEFT, MOUSE_LEFT }, { PIN_RIGHT, MOUSE_RIGHT } };

void setup() {
  for (Btn &b : btns) pinMode(b.pin, INPUT_PULLUP);
  Mouse.begin();
  USB.begin();
}

void loop() {
  unsigned long now = millis();
  for (Btn &b : btns) {
    bool pressed = (digitalRead(b.pin) == LOW);
    if (pressed != b.down && now - b.last > DEBOUNCE_MS) {
      b.down = pressed;
      b.last = now;
      if (pressed) Mouse.press(b.hid);
      else         Mouse.release(b.hid);
    }
  }
  delay(1);
}
