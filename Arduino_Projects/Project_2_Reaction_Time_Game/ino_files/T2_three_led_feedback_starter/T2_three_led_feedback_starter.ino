// ============================================================
// Project 2 - Reaction Time Game  (TIER 2: read & change the code)
// Starter A: THREE-LED FEEDBACK
// ============================================================
//
// This builds on sketch 02 (the buzzer game). Same GO light, same
// random wait, same buzzer beep, same "too early" rule.
//
// WHAT IS NEW HERE:
//   After you press the button, the Arduino looks at how fast you were
//   and lights ONE of three result LEDs to show your category:
//       FAST    -> GREEN  LED on pin 9  (this is also the GO light)
//       MEDIUM  -> YELLOW LED on pin 10
//       SLOW    -> RED    LED on pin 11
//   It also prints the same result to the Serial Monitor.
//
//   The GO light now stays on for ONLY a short window of time
//   (LED_ON_WINDOW). If you do not press before the light goes out,
//   you "missed it" and the round restarts.
//
// Open the Serial Monitor (magnifying glass, top-right of the IDE)
// and set the speed at the bottom to 9600 baud to read the messages.
//
// DO NOT press the button before the LED turns on. If you press
// too early, the round restarts and you get a "too early" message.
//
// ---- THINGS YOU WILL CHANGE LATER (look for these at the top) ----
//   LED_ON_WINDOW : how long the GO light stays on  (Hard mode = 500)
//   FAST_MS       : the FAST/MEDIUM cut-off          (you tune this)
//   MEDIUM_MS     : the MEDIUM/SLOW cut-off          (you tune this)
// ============================================================


// ============================================================
// CONSTANTS YOU CAN CHANGE  (these are the easy-to-find knobs)
// ============================================================

// ---- DIFFICULTY: how long the GO light stays on, in milliseconds ----
const unsigned long LED_ON_WINDOW = 2000;  // students change to 500 for Hard mode at T2_M3

// ---- CATEGORY THRESHOLDS: where FAST / MEDIUM / SLOW begin, in ms ----
const int FAST_MS   = 250;   // press faster than this  -> FAST    (students tune at T2_M4)
const int MEDIUM_MS = 450;   // press faster than this  -> MEDIUM  (students tune at T2_M4)
                             // anything slower (but in time) -> SLOW


// ============================================================
// PIN NUMBERS (which Arduino pin each part is wired to)
// ============================================================
const int LED_PIN    = 9;   // The "GO" light, AND the GREEN (FAST) result LED.
const int BUTTON_PIN = 2;   // The button. Wired with an external pull-down resistor,
                            // so the pin reads HIGH when the button is pressed.
const int BUZZER_PIN = 8;   // The buzzer. Beeps at the "GO" moment.
const int MED_LED    = 10;  // YELLOW result LED -> lights up for a MEDIUM time.
const int SLOW_LED   = 11;  // RED    result LED -> lights up for a SLOW time.

// ---- SOUND SETTINGS (for the buzzer) ----
const int  GO_TONE_HZ = 1000;  // pitch of the "GO" beep, in Hertz
const int  GO_TONE_MS = 100;   // how long the "GO" beep lasts, in ms

// ---- TIMING SETTINGS (how long the random wait can be) ----
const long MIN_WAIT_MS = 2000;  // shortest wait before "GO" = 2 seconds
const long MAX_WAIT_MS = 5000;  // longest  wait before "GO" = 5 seconds

// ---- HOW LONG THE RESULT LED STAYS LIT after a press, in ms ----
const int  RESULT_SHOW_MS = 1000;

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
  pinMode(LED_PIN, OUTPUT);     // GO light / GREEN result LED (we control it).
  pinMode(BUTTON_PIN, INPUT);   // The button (we read it).
  pinMode(BUZZER_PIN, OUTPUT);  // The buzzer (we control it).
  pinMode(MED_LED, OUTPUT);     // YELLOW result LED (we control it).
  pinMode(SLOW_LED, OUTPUT);    // RED result LED (we control it).

  // Make sure all the LEDs start OFF.
  digitalWrite(LED_PIN, LOW);
  digitalWrite(MED_LED, LOW);
  digitalWrite(SLOW_LED, LOW);

  // Start talking to the computer over the USB cable.
  Serial.begin(SERIAL_BAUD);

  // Give every game a different sequence of random waits.
  // analogRead(A0) reads electrical "noise" from an unconnected pin,
  // which gives us a different starting number each time.
  randomSeed(analogRead(A0));

  // Print a friendly welcome message.
  Serial.println("=================================");
  Serial.println("   REACTION TIME GAME (3-LED feedback)");
  Serial.println("=================================");
  Serial.println("Wait for the LED to turn ON and BEEP,");
  Serial.println("then press the button as FAST as you can!");
  Serial.println("GREEN = fast, YELLOW = medium, RED = slow.");
  Serial.println("Do NOT press before the light comes on.");
  Serial.println();
}


// ============================================================
// loop() runs OVER AND OVER, forever. Each pass = one round.
// ============================================================
void loop() {

  // ---- STEP 1: Get ready ----
  Serial.println("Get ready...");

  // Turn the result LEDs off at the start of each round.
  digitalWrite(MED_LED, LOW);
  digitalWrite(SLOW_LED, LOW);

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
  digitalWrite(LED_PIN, HIGH);                 // light up the "GO" signal (green)
  tone(BUZZER_PIN, GO_TONE_HZ, GO_TONE_MS);    // beep at the GO moment
  long startTime = millis();                   // remember the exact moment GO happened
  Serial.println("GO! Press the button!");

  // ---- STEP 4: Wait for a press, but ONLY for LED_ON_WINDOW ms ----
  // The light is on for at most LED_ON_WINDOW. Keep checking the button
  // until it is pressed OR the window runs out.
  bool pressedInTime = false;
  while (millis() - startTime < LED_ON_WINDOW) {
    if (digitalRead(BUTTON_PIN) == HIGH) {
      pressedInTime = true;
      break;  // got the press, stop waiting
    }
  }

  // ---- STEP 5: Measure the reaction time ----
  long reactionTime = millis() - startTime;  // how long the press took

  // Turn the GO light off now that the window is over.
  digitalWrite(LED_PIN, LOW);

  // If the player did NOT press in time, the round is a miss. Restart.
  if (!pressedInTime) {
    Serial.println(">> Too slow! The light went out. Try again.");
    Serial.println();
    return;  // start a fresh round next pass
  }

  // ---- STEP 6: Decide the category and light the matching LED ----
  // We compare reactionTime to the thresholds at the top of the file.
  if (reactionTime < FAST_MS) {
    // FAST: re-light the green LED (pin 9) as the result light.
    digitalWrite(LED_PIN, HIGH);
    Serial.print("FAST! ");
  } else if (reactionTime < MEDIUM_MS) {
    // MEDIUM: light the yellow LED (pin 10).
    digitalWrite(MED_LED, HIGH);
    Serial.print("MEDIUM. ");
  } else {
    // SLOW: light the red LED (pin 11).
    digitalWrite(SLOW_LED, HIGH);
    Serial.print("SLOW. ");
  }

  // Print the time next to the category word.
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

  // Keep the result LED lit for a moment so the player can see it.
  delay(RESULT_SHOW_MS);

  // Wait until the player releases the button before the next round,
  // so a held-down button does not affect the next "too early" check.
  while (digitalRead(BUTTON_PIN) == HIGH) {
    // do nothing, just wait for release
  }

  // The loop() function ends here and automatically starts again
  // for the next round.
}
