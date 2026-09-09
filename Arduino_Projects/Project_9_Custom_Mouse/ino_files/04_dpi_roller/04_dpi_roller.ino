/*
 * Project 9 — step 7: the speed roller.
 * The small rear roller changes the mouse speed LIVE, and three LEDs show the level.
 * This is the project's signature feature.
 *
 * Tools settings:  Board "ESP32S3 Dev Module", USB Mode "USB-OTG (TinyUSB)".
 * Library:         "PMW3360 Module" by SunjunKim.
 *
 * New wiring in this step:
 *   J3 (9 mm rear roller):  A → GPIO 15 · B → GPIO 16 · PUSH → GPIO 17 · C → GND
 *   J6 (LEDs, each through 330 ohm to GND):
 *   DPI1 → GPIO 39 · DPI2 → GPIO 40 · DPI3 → GPIO 41
 */

#include "USB.h"
#include "USBHIDMouse.h"
#include <PMW3360.h>

USBHIDMouse Mouse;
PMW3360 sensor;

const int PIN_CS = 10;

const int PIN_LEFT   = 1;
const int PIN_RIGHT  = 2;
const int PIN_F_A    = 4;
const int PIN_F_B    = 5;
const int PIN_F_PUSH = 6;
const int PIN_R_A    = 15;
const int PIN_R_B    = 16;
const int PIN_LED[3] = { 39, 40, 41 };

// the three speed levels; T2 tunes these to the student's hand
const int CPI_LEVELS[3] = { 400, 800, 1600 };
int level = 1;                                   // start in the middle

const unsigned long DEBOUNCE_MS = 8;
struct Btn { int pin; uint8_t hid; bool down = false; unsigned long last = 0; };
Btn btns[] = {
  { PIN_LEFT,   MOUSE_LEFT   },
  { PIN_RIGHT,  MOUSE_RIGHT  },
  { PIN_F_PUSH, MOUSE_MIDDLE },
};

int lastFA = HIGH, lastRA = HIGH;

void showLevel() {
  for (int i = 0; i < 3; i++) digitalWrite(PIN_LED[i], i == level ? HIGH : LOW);
  sensor.setCPI(CPI_LEVELS[level]);
}

void setup() {
  for (Btn &b : btns) pinMode(b.pin, INPUT_PULLUP);
  for (int p : { PIN_F_A, PIN_F_B, PIN_R_A, PIN_R_B }) pinMode(p, INPUT_PULLUP);
  for (int i = 0; i < 3; i++) pinMode(PIN_LED[i], OUTPUT);
  Mouse.begin();
  USB.begin();
  sensor.begin(PIN_CS);
  showLevel();
}

void loop() {
  unsigned long now = millis();

  for (Btn &b : btns) {
    bool pressed = (digitalRead(b.pin) == LOW);
    if (pressed != b.down && now - b.last > DEBOUNCE_MS) {
      b.down = pressed; b.last = now;
      if (pressed) Mouse.press(b.hid); else Mouse.release(b.hid);
    }
  }

  PMW3360_DATA d = sensor.readBurst();
  if (d.isOnSurface && d.isMotion) {
    Mouse.move(constrain(-d.dx, -127, 127), constrain(-d.dy, -127, 127));
  }

  int fa = digitalRead(PIN_F_A);
  if (fa != lastFA && fa == LOW) {
    Mouse.move(0, 0, digitalRead(PIN_F_B) == HIGH ? 1 : -1);
  }
  lastFA = fa;

  // rear roller: each detent moves one speed level up or down
  int ra = digitalRead(PIN_R_A);
  if (ra != lastRA && ra == LOW) {
    level += (digitalRead(PIN_R_B) == HIGH) ? 1 : -1;
    level = constrain(level, 0, 2);
    showLevel();
  }
  lastRA = ra;

  delay(1);
}
