// 04_button_control.ino
// A push-button controls which of two LEDs is on.
//
// Used at Tier 1 Milestone 8 of Project 1 — the student's first INTERACTIVE
// Arduino sketch. Until now the Arduino has been the active element (blinking
// LEDs on its own). Now the student's input (button press) changes the
// Arduino's output (which LED is lit).
//
// This closes Project 1 with the student's first experience of the fundamental
// Arduino loop: read input --> decide --> write output. Every interactive
// project in the rest of the program is built on this pattern.
//
// Wiring:
//   - LED 1 (from Milestone 3): long leg --> 220 Ω resistor --> pin 9,
//     short leg --> GND
//   - LED 2 (from Milestone 5): long leg --> 220 Ω resistor --> pin 10,
//     short leg --> GND
//   - Button (from Milestone 7): one side --> Arduino 5V, other side --> pin 2
//     AND --> 10 kΩ pull-down resistor --> GND
//
// The 10 kΩ pull-down resistor is important: it holds pin 2 at 0 V (LOW) when
// the button is not pressed. When the button IS pressed, the 5 V rail connects
// to pin 2 directly and pin 2 reads HIGH. Without the pull-down, pin 2 would
// "float" when the button is not pressed and digitalRead() would return random
// values.
//
// Expected behaviour:
//   - Button NOT pressed: LED 1 (pin 9) is ON, LED 2 (pin 10) is OFF.
//   - Button pressed and held: LED 1 is OFF, LED 2 is ON.
//   - Release the button: back to LED 1 ON, LED 2 OFF.

const int LED_1 = 9;
const int LED_2 = 10;
const int BUTTON = 2;

void setup() {
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);
  pinMode(BUTTON, INPUT);
}

void loop() {
  int buttonState = digitalRead(BUTTON);

  if (buttonState == HIGH) {
    // Button is pressed: LED 2 on, LED 1 off.
    digitalWrite(LED_1, LOW);
    digitalWrite(LED_2, HIGH);
  } else {
    // Button not pressed: LED 1 on, LED 2 off.
    digitalWrite(LED_1, HIGH);
    digitalWrite(LED_2, LOW);
  }
}
