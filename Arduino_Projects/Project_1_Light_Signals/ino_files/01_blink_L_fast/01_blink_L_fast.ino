// 01_blink_L_fast.ino
// Blinks the built-in "L" LED on the Arduino Uno faster than the factory sketch.
//
// Used at Tier 1 Milestone 2 of Project 1 — the student's first Upload click.
// No wiring required. The "L" LED is already on the Arduino board, connected
// internally to digital pin 13.
//
// Expected behaviour: the small green LED near pin 13 blinks about three times
// per second after upload. The factory sketch blinks once per second, so the
// student sees the LED blink faster than before — proof the upload worked.

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(150);
  digitalWrite(LED_BUILTIN, LOW);
  delay(150);
}
