/*
 * Project 9 — step 8: the whole mouse, wired.
 * Everything together: clicks, sensor, both rollers, three side buttons, four LEDs.
 * Pushing the rear roller toggles a FUNCTION LAYER for the side buttons; the yellow
 * layer LED shows which layer is active.
 *
 * Tools settings:  Board "ESP32S3 Dev Module", USB Mode "USB-OTG (TinyUSB)".
 * Library:         "PMW3360 Module" by SunjunKim.
 *
 * New wiring in this step:
 *   J5 (side buttons to GND):  S1 → GPIO 7 · S2 → GPIO 8 · S3 → GPIO 9
 *   J6 adds the layer LED:     LAYER → GPIO 42 (through 330 ohm)
 *
 * Side buttons, base layer:   S1 = Back · S2 = Forward · S3 = middle click
 * Side buttons, layer ON:     S1 = drag lock · S2 = double click · S3 = speed level
 * (T2 changes these mappings with Claude Code — that is the point of this mouse.)
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
const int PIN_R_PUSH = 17;
const int PIN_S[3]   = { 7, 8, 9 };
const int PIN_LED[3] = { 39, 40, 41 };
const int PIN_LED_LAYER = 42;

const int CPI_LEVELS[3] = { 400, 800, 1600 };
int  level    = 1;
bool layerOn  = false;
bool dragLock = false;

const unsigned long DEBOUNCE_MS = 8;
struct Btn { int pin; bool down = false; unsigned long last = 0; };
Btn bLeft{PIN_LEFT}, bRight{PIN_RIGHT}, bMid{PIN_F_PUSH}, bLayer{PIN_R_PUSH};
Btn bSide[3] = { {PIN_S[0]}, {PIN_S[1]}, {PIN_S[2]} };

int lastFA = HIGH, lastRA = HIGH;

bool edge(Btn &b, unsigned long now) {           // true once on each new press
  bool pressed = (digitalRead(b.pin) == LOW);
  if (pressed != b.down && now - b.last > DEBOUNCE_MS) {
    b.down = pressed; b.last = now;
    return pressed;
  }
  return false;
}

void holdable(Btn &b, uint8_t hid, unsigned long now) {   // press-and-hold buttons
  bool pressed = (digitalRead(b.pin) == LOW);
  if (pressed != b.down && now - b.last > DEBOUNCE_MS) {
    b.down = pressed; b.last = now;
    if (pressed) Mouse.press(hid); else Mouse.release(hid);
  }
}

void showLevel() {
  for (int i = 0; i < 3; i++) digitalWrite(PIN_LED[i], i == level ? HIGH : LOW);
  sensor.setCPI(CPI_LEVELS[level]);
}

void setup() {
  for (Btn *b : { &bLeft, &bRight, &bMid, &bLayer, &bSide[0], &bSide[1], &bSide[2] })
    pinMode(b->pin, INPUT_PULLUP);
  for (int p : { PIN_F_A, PIN_F_B, PIN_R_A, PIN_R_B }) pinMode(p, INPUT_PULLUP);
  for (int i = 0; i < 3; i++) pinMode(PIN_LED[i], OUTPUT);
  pinMode(PIN_LED_LAYER, OUTPUT);
  Mouse.begin();
  USB.begin();
  sensor.begin(PIN_CS);
  showLevel();
}

void loop() {
  unsigned long now = millis();

  holdable(bLeft,  MOUSE_LEFT,  now);
  holdable(bRight, MOUSE_RIGHT, now);
  holdable(bMid,   MOUSE_MIDDLE, now);

  // rear roller push toggles the function layer
  if (edge(bLayer, now)) {
    layerOn = !layerOn;
    digitalWrite(PIN_LED_LAYER, layerOn ? HIGH : LOW);
  }

  // side buttons — meaning depends on the layer
  if (!layerOn) {
    holdable(bSide[0], MOUSE_BACKWARD, now);
    holdable(bSide[1], MOUSE_FORWARD,  now);
    holdable(bSide[2], MOUSE_MIDDLE,   now);
  } else {
    if (edge(bSide[0], now)) {                    // drag lock: left button stays down
      dragLock = !dragLock;
      if (dragLock) Mouse.press(MOUSE_LEFT); else Mouse.release(MOUSE_LEFT);
    }
    if (edge(bSide[1], now)) {                    // double click
      Mouse.click(MOUSE_LEFT); delay(30); Mouse.click(MOUSE_LEFT);
    }
    if (edge(bSide[2], now)) {                    // next speed level
      level = (level + 1) % 3;
      showLevel();
    }
    bSide[0].down = digitalRead(bSide[0].pin) == LOW;
  }

  PMW3360_DATA d = sensor.readBurst();
  if (d.isOnSurface && d.isMotion) {
    Mouse.move(constrain(-d.dx, -127, 127), constrain(-d.dy, -127, 127));
  }

  int fa = digitalRead(PIN_F_A);
  if (fa != lastFA && fa == LOW)
    Mouse.move(0, 0, digitalRead(PIN_F_B) == HIGH ? 1 : -1);
  lastFA = fa;

  int ra = digitalRead(PIN_R_A);
  if (ra != lastRA && ra == LOW) {
    level = constrain(level + (digitalRead(PIN_R_B) == HIGH ? 1 : -1), 0, 2);
    showLevel();
  }
  lastRA = ra;

  delay(1);
}
