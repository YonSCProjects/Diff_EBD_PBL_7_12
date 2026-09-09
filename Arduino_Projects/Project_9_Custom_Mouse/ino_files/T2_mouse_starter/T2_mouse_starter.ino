/*
 * Project 9 — Tier 2 starter: YOUR mouse.
 * This is 06_bt_mouse with every personal decision pulled up into the TUNING BLOCK
 * below. In Tier 2 you change these numbers and mappings with Claude Code until the
 * mouse fits YOUR hand — that is the whole point of building your own.
 *
 * Tools settings:  Board "ESP32S3 Dev Module".
 * Libraries:       "PMW3360 Module" by SunjunKim, "ESP32-BLE-Mouse" by T-vK.
 */

// ═══════════════ TUNING BLOCK — everything you may change lives here ═══════════════

#define MOUSE_NAME      "P9-MOUSE"      // the name the computer sees when pairing

// the three speed levels the rear roller steps through (counts per inch)
const int CPI_LEVELS[3] = { 400, 800, 1600 };
const int START_LEVEL   = 1;            // 0 = slowest, 2 = fastest

// how the cursor responds
#define INVERT_X        false           // true flips left-right
#define INVERT_Y        false           // true flips up-down
#define BED_MODE        false           // true = extra smoothing for soft surfaces

// side buttons, base layer: MOUSE_BACK, MOUSE_FORWARD, MOUSE_MIDDLE,
//                           MOUSE_LEFT, MOUSE_RIGHT
#define S1_BASE         MOUSE_BACK
#define S2_BASE         MOUSE_FORWARD
#define S3_BASE         MOUSE_MIDDLE

// how long a button must be steady before it counts (raise if clicks double)
const unsigned long DEBOUNCE_MS = 8;

// ══════════════════════════ end of the tuning block ════════════════════════════════

#include <BleMouse.h>
#include <PMW3360.h>

BleMouse bleMouse(MOUSE_NAME, "Robotics Workshop", 100);
PMW3360 sensor;

const int PIN_CS = 10;
const int PIN_LEFT = 1, PIN_RIGHT = 2;
const int PIN_F_A = 4, PIN_F_B = 5, PIN_F_PUSH = 6;
const int PIN_R_A = 15, PIN_R_B = 16, PIN_R_PUSH = 17;
const int PIN_S[3] = { 7, 8, 9 };
const int PIN_LED[3] = { 39, 40, 41 };
const int PIN_LED_LAYER = 42;

int  level   = START_LEVEL;
bool layerOn = false;
bool dragLock = false;

struct Btn { int pin; bool down = false; unsigned long last = 0; };
Btn bLeft{PIN_LEFT}, bRight{PIN_RIGHT}, bMid{PIN_F_PUSH}, bLayer{PIN_R_PUSH};
Btn bSide[3] = { {PIN_S[0]}, {PIN_S[1]}, {PIN_S[2]} };
int lastFA = HIGH, lastRA = HIGH;
int smoothX = 0, smoothY = 0;

bool edge(Btn &b, unsigned long now) {
  bool p = (digitalRead(b.pin) == LOW);
  if (p != b.down && now - b.last > DEBOUNCE_MS) { b.down = p; b.last = now; return p; }
  return false;
}

void holdable(Btn &b, uint8_t hid, unsigned long now) {
  bool p = (digitalRead(b.pin) == LOW);
  if (p != b.down && now - b.last > DEBOUNCE_MS) {
    b.down = p; b.last = now;
    if (p) bleMouse.press(hid); else bleMouse.release(hid);
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
  bleMouse.begin();
  sensor.begin(PIN_CS);
  showLevel();
}

void loop() {
  unsigned long now = millis();

  if (edge(bLayer, now)) {
    layerOn = !layerOn;
    digitalWrite(PIN_LED_LAYER, layerOn ? HIGH : LOW);
  }

  if (bleMouse.isConnected()) {
    holdable(bLeft,  MOUSE_LEFT,  now);
    holdable(bRight, MOUSE_RIGHT, now);
    holdable(bMid,   MOUSE_MIDDLE, now);

    if (!layerOn) {
      holdable(bSide[0], S1_BASE, now);
      holdable(bSide[1], S2_BASE, now);
      holdable(bSide[2], S3_BASE, now);
    } else {
      if (edge(bSide[0], now)) {
        dragLock = !dragLock;
        if (dragLock) bleMouse.press(MOUSE_LEFT); else bleMouse.release(MOUSE_LEFT);
      }
      if (edge(bSide[1], now)) { bleMouse.click(MOUSE_LEFT); delay(30); bleMouse.click(MOUSE_LEFT); }
      if (edge(bSide[2], now)) { level = (level + 1) % 3; showLevel(); }
    }

    PMW3360_DATA d = sensor.readBurst();
    if (d.isOnSurface && d.isMotion) {
      int dx = INVERT_X ? d.dx : -d.dx;
      int dy = INVERT_Y ? d.dy : -d.dy;
      if (BED_MODE) {              // soften jumps from an uneven surface
        smoothX = (smoothX + dx) / 2;
        smoothY = (smoothY + dy) / 2;
        dx = smoothX; dy = smoothY;
      }
      bleMouse.move(constrain(dx, -127, 127), constrain(dy, -127, 127));
    }

    int fa = digitalRead(PIN_F_A);
    if (fa != lastFA && fa == LOW)
      bleMouse.move(0, 0, digitalRead(PIN_F_B) == HIGH ? 1 : -1);
    lastFA = fa;
  }

  int ra = digitalRead(PIN_R_A);
  if (ra != lastRA && ra == LOW) {
    level = constrain(level + (digitalRead(PIN_R_B) == HIGH ? 1 : -1), 0, 2);
    showLevel();
  }
  lastRA = ra;

  delay(1);
}
