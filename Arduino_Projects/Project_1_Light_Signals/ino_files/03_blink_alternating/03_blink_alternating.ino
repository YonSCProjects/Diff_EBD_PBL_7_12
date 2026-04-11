// 03_blink_alternating.ino
// Blinks two external LEDs in alternation — when one is on, the other is off.
//
// Used at Tier 1 Milestone 6 of Project 1 — the student's first multi-output
// sketch. Shows that a single Arduino can control two independent things at
// the same time.
//
// Wiring (from Tier 1 Milestones 3 and 5):
//   - LED 1 long leg (anode) --> 220 Ω resistor --> Arduino pin 9
//   - LED 1 short leg (cathode) --> Arduino GND
//   - LED 2 long leg (anode) --> 220 Ω resistor --> Arduino pin 10
//   - LED 2 short leg (cathode) --> Arduino GND
//
// Expected behaviour: LED 1 on, LED 2 off, for half a second; then LED 1 off,
// LED 2 on, for half a second; repeat forever.

const int LED_1 = 9;
const int LED_2 = 10;

void setup() {
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);
}

void loop() {
  digitalWrite(LED_1, HIGH);
  digitalWrite(LED_2, LOW);
  delay(500);

  digitalWrite(LED_1, LOW);
  digitalWrite(LED_2, HIGH);
  delay(500);
}
