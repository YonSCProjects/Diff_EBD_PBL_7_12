// T2_breathing_starter.ino
// Tier 2 starter sketch for the "breathing" pattern choice in Project 1.
//
// One LED fades smoothly in and out using PWM (Pulse-Width Modulation), so
// it looks like it is "breathing" — slowly getting brighter, then slowly
// getting dimmer, repeatedly.
//
// PWM means the Arduino turns the LED on and off very fast — faster than the
// eye can see — and by changing the ratio of on-time to off-time it can make
// the LED look any brightness between fully off (0) and fully on (255).
//
// PWM only works on certain pins on the Arduino Uno — the ones marked with a
// tilde symbol (~) on the board: pins 3, 5, 6, 9, 10, and 11. Pin 9 is one
// of them, which is why this sketch uses pin 9.
//
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
//   - FADE_STEP_MS — change 10 to 5 for faster breathing, or 20 for slower
//   - LED_PIN — must stay on a PWM pin (3, 5, 6, 9, 10, or 11)
//   - Add a second breathing LED on a second PWM pin
//   - Pause at the brightest point by adding a delay() after the fade-in loop
//
// Wiring (same as Tier 1 Milestone 3):
//   - LED: long leg --> 220 Ω --> pin 9; short leg --> GND

const int LED_PIN = 9;
const int FADE_STEP_MS = 10;

void setup() {
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // Fade in: 0 (off) to 255 (full brightness)
  for (int brightness = 0; brightness <= 255; brightness++) {
    analogWrite(LED_PIN, brightness);
    delay(FADE_STEP_MS);
  }

  // Fade out: 255 back to 0
  for (int brightness = 255; brightness >= 0; brightness--) {
    analogWrite(LED_PIN, brightness);
    delay(FADE_STEP_MS);
  }
}
