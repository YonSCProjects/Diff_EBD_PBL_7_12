// T2_alternating_starter.ino
// Tier 2 starter sketch for the "alternating" pattern choice in Project 1.
//
// This is a Channel A Level 2 starter sketch — the student uploads it as-is
// first, then uses Claude Code to modify it to match their own design choices.
//
// Before asking Claude Code to help you change this sketch, first fill in
// three things on your task card:
//   (a) What I want to happen: [describe the behaviour you want]
//   (b) What's currently happening: [describe what the sketch does now]
//   (c) What I've tried: [what you've already looked at or considered]
// Then ask Claude Code. The (a)(b)(c) discipline is not optional — it is
// how Channel A Level 2 works in this program.
//
// Easy things to change (try one at a time, upload after each change):
//   - BLINK_DELAY_MS — change 500 to 250 for faster, or 1000 for slower
//   - LED_1 and LED_2 pin numbers — if you rewire to different pins
//   - Swap the HIGH and LOW in the loop to invert which LED is on first
//
// Wiring (same as Tier 1 Milestones 3 and 5):
//   - LED 1: long leg --> 220 Ω --> pin 9; short leg --> GND
//   - LED 2: long leg --> 220 Ω --> pin 10; short leg --> GND

const int LED_1 = 9;
const int LED_2 = 10;
const int BLINK_DELAY_MS = 500;

void setup() {
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);
}

void loop() {
  digitalWrite(LED_1, HIGH);
  digitalWrite(LED_2, LOW);
  delay(BLINK_DELAY_MS);

  digitalWrite(LED_1, LOW);
  digitalWrite(LED_2, HIGH);
  delay(BLINK_DELAY_MS);
}
