// 02_blink_external.ino
// Blinks the external LED wired to digital pin 9.
//
// Used at Tier 1 Milestone 4 of Project 1 — the student's first external LED
// lights up because of code they uploaded.
//
// Wiring (from Tier 1 Milestone 3):
//   - LED long leg (anode) --> 220 Ω resistor --> Arduino pin 9
//   - LED short leg (cathode) --> Arduino GND
//
// Expected behaviour: the external LED on the breadboard blinks on and off
// about once per second. This is the "something I wired lit up because of code
// I uploaded" moment — the Principle 4 visible win that Project 1 is built
// around.

const int LED_PIN = 9;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  delay(500);
}
