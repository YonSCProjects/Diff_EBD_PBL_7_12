// ============================================================
// Project 2 - Reaction Time Game
// Sketch 02: Wait, Flash, Measure + BUZZER
// ============================================================
//
// This is the SAME game as sketch 01, with one new part: a buzzer.
//   - It BEEPS at the "GO" moment (when the LED turns on).
//   - It plays a short SUCCESS beep when you press the button.
//
// If you compare (diff) this file with sketch 01, the only new
// lines are the BUZZER_PIN, the tone() calls, and their comments.
//
// HOW THE GAME WORKS:
//   1. The Arduino waits a random amount of time (2 to 5 seconds).
//   2. Then the LED turns ON and the buzzer BEEPS. That is "GO!".
//   3. As fast as you can, press the button.
//   4. The Arduino measures how long it took you, in milliseconds.
//   5. It prints your time and remembers your best (fastest) time.
//
// Open the Serial Monitor (magnifying glass, top-right of the IDE)
// and set the speed at the bottom to 9600 baud to read the messages.
//
// DO NOT press the button before the LED turns on. If you press
// too early, the round restarts and you get a "too early" message.
// ============================================================


// ---- PIN NUMBERS (which Arduino pin each part is wired to) ----
const int LED_PIN    = 9;   // The "GO" light. Turns on when it is time to press.
const int BUTTON_PIN = 2;   // The button. Wired with an external pull-down resistor,
                            // so the pin reads HIGH when the button is pressed.
const int BUZZER_PIN = 8;   // NEW: The buzzer. Beeps at "GO" and on a successful press.

// ---- SOUND SETTINGS (for the buzzer) ----
const int  GO_TONE_HZ      = 1000;  // NEW: pitch of the "GO" beep, in Hertz
const int  GO_TONE_MS      = 100;   // NEW: how long the "GO" beep lasts, in ms
const int  SUCCESS_TONE_HZ = 1500;  // NEW: pitch of the success beep, in Hertz
const int  SUCCESS_TONE_MS = 150;   // NEW: how long the success beep lasts, in ms

// ---- TIMING SETTINGS (how long the random wait can be) ----
const long MIN_WAIT_MS = 2000;  // shortest wait before "GO" = 2 seconds
const long MAX_WAIT_MS = 5000;  // longest  wait before "GO" = 5 seconds

// ---- COMMUNICATION SPEED (must match the Serial Monitor) ----
const long SERIAL_BAUD = 9600;


// ---- MEMORY (variables that the program keeps between rounds) ----
long bestTime = -1;   // The best (fastest) reaction time so far, in ms.
                      // -1 means "no time recorded yet".


// ============================================================
// setup() runs ONE time when the Arduino powers on or resets.
// ============================================================
void setup() {
  // Set up the pins so the Arduino knows which is an output and which is an input.
  pinMode(LED_PIN, OUTPUT);     // The LED is something we control (turn on/off).
  pinMode(BUTTON_PIN, INPUT);   // The button is something we read.
  pinMode(BUZZER_PIN, OUTPUT);  // NEW: The buzzer is something we control.

  // Make sure the LED starts OFF.
  digitalWrite(LED_PIN, LOW);

  // Start talking to the computer over the USB cable.
  Serial.begin(SERIAL_BAUD);

  // Give every game a different sequence of random waits.
  // analogRead(A0) reads electrical "noise" from an unconnected pin,
  // which gives us a different starting number each time.
  randomSeed(analogRead(A0));

  // Print a friendly welcome message.
  Serial.println("=================================");
  Serial.println("   REACTION TIME GAME (with buzzer)");
  Serial.println("=================================");
  Serial.println("Wait for the LED to turn ON and BEEP,");
  Serial.println("then press the button as FAST as you can!");
  Serial.println("Do NOT press before the light comes on.");
  Serial.println();
}


// ============================================================
// loop() runs OVER AND OVER, forever. Each pass = one round.
// ============================================================
void loop() {

  // ---- STEP 1: Get ready ----
  Serial.println("Get ready...");

  // Pick a random wait time between MIN_WAIT_MS and MAX_WAIT_MS.
  // (random's second number is "up to but not including", so we add 1.)
  long waitTime = random(MIN_WAIT_MS, MAX_WAIT_MS + 1);

  // ---- STEP 2: Wait the random time, while watching for cheating ----
  // We use millis() so we can keep checking the button during the wait.
  long waitStart = millis();
  while (millis() - waitStart < waitTime) {

    // If the button is already pressed (HIGH) before the GO light,
    // that is jumping the gun. Restart the round.
    if (digitalRead(BUTTON_PIN) == HIGH) {
      Serial.println(">> Too early! Wait for the light. Try again.");
      Serial.println();

      // Wait until the player lets go of the button before restarting,
      // so the next round does not instantly see the press again.
      while (digitalRead(BUTTON_PIN) == HIGH) {
        // do nothing, just wait for release
      }

      return;  // leave loop() now; Arduino starts a fresh round next pass
    }
  }

  // ---- STEP 3: GO! Turn the LED on and start the stopwatch ----
  digitalWrite(LED_PIN, HIGH);                 // light up the "GO" signal
  tone(BUZZER_PIN, GO_TONE_HZ, GO_TONE_MS);    // NEW: beep at the GO moment
  long startTime = millis();                   // remember the exact moment GO happened
  Serial.println("GO! Press the button!");

  // ---- STEP 4: Wait for the player to press the button ----
  while (digitalRead(BUTTON_PIN) == LOW) {
    // keep looping (doing nothing) until the button reads HIGH (pressed)
  }

  // ---- STEP 5: Measure the reaction time ----
  long reactionTime = millis() - startTime;  // how long the press took

  // Turn the LED back off now that the round is done.
  digitalWrite(LED_PIN, LOW);

  // NEW: Play a short success beep to celebrate the press.
  tone(BUZZER_PIN, SUCCESS_TONE_HZ, SUCCESS_TONE_MS);

  // ---- STEP 6: Show the result ----
  Serial.print("Reaction time: ");
  Serial.print(reactionTime);
  Serial.println(" ms");

  // ---- STEP 7: Update and show the best time ----
  // If we have no best time yet, or this round was faster, save it.
  if (bestTime == -1 || reactionTime < bestTime) {
    bestTime = reactionTime;
    Serial.println("** New best time! **");
  }
  Serial.print("Best time so far: ");
  Serial.print(bestTime);
  Serial.println(" ms");
  Serial.println();

  // Wait until the player releases the button before the next round,
  // so a held-down button does not affect the next "too early" check.
  while (digitalRead(BUTTON_PIN) == HIGH) {
    // do nothing, just wait for release
  }

  // The loop() function ends here and automatically starts again
  // for the next round.
}
