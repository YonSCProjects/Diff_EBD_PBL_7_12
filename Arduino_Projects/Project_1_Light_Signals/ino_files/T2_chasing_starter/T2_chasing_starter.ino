// T2_chasing_starter.ino
// Tier 2 starter sketch for the "chasing" pattern choice in Project 1.
//
// Three LEDs light up one at a time in sequence, like a chase light on a sign.
// This is a Channel A Level 2 starter sketch — the student uploads it as-is
// first, then uses Claude Code to modify it to match their own design choices.
//
// Before asking Claude Code to help you change this sketch, first fill in
// three things on your task card:
//   (a) What I want to happen: [describe the behaviour you want]
//   (b) What's currently happening: [describe what the sketch does now]
//   (c) What I've tried: [what you've already looked at or considered]
// Then ask Claude Code.
//
// Easy things to change (try one at a time):
//   - STEP_DELAY_MS — change 200 to 100 for a faster chase, or 400 for slower
//   - LED pin numbers
//   - Add a fourth or fifth LED by adding a new pin and a new step in loop()
//   - Reverse the direction of the chase
//
// Wiring: you need THREE LEDs for this pattern, not just two. Wire them to
// pins 9, 10, and 11, each with a 220 Ω current-limiting resistor, each with
// the short leg going to GND.

const int LED_1 = 9;
const int LED_2 = 10;
const int LED_3 = 11;
const int STEP_DELAY_MS = 200;

void setup() {
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);
  pinMode(LED_3, OUTPUT);
}

void loop() {
  // Step 1: LED 1 on, others off
  digitalWrite(LED_1, HIGH);
  digitalWrite(LED_2, LOW);
  digitalWrite(LED_3, LOW);
  delay(STEP_DELAY_MS);

  // Step 2: LED 2 on, others off
  digitalWrite(LED_1, LOW);
  digitalWrite(LED_2, HIGH);
  digitalWrite(LED_3, LOW);
  delay(STEP_DELAY_MS);

  // Step 3: LED 3 on, others off
  digitalWrite(LED_1, LOW);
  digitalWrite(LED_2, LOW);
  digitalWrite(LED_3, HIGH);
  delay(STEP_DELAY_MS);
}
