// ============================================================
// Project 2 - Reaction Time Game  (TIER 2: read & change the code)
// Starter B: BUZZER PATTERN FEEDBACK
// ============================================================
//
// This builds on sketch 02 (the buzzer game). Same GO light, same
// random wait, same buzzer beep, same "too early" rule.
//
// WHAT IS NEW HERE:
//   After you press the button, the Arduino looks at how fast you were
//   and plays a DIFFERENT buzzer pattern (pin 8) for each category:
//       FAST    -> ONE  short HIGH beep
//       MEDIUM  -> TWO  short beeps
//       SLOW    -> ONE  long  LOW  buzz
//   It also prints the same result to the Serial Monitor, so you can
//   match the sound you hear to the word on the screen.
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
const int LED_PIN    = 9;   // The "GO" light. Turns on when it is time to press.
const int BUTTON_PIN = 2;   // The button. Wired with an external pull-down resistor,
                            // so the pin reads HIGH when the button is pressed.
const int BUZZER_PIN = 8;   // The buzzer. Beeps at "GO" and plays the result pattern.

// ---- SOUND SETTINGS (for the buzzer) ----
const int  GO_TONE_HZ   = 1000;  // pitch of the "GO" beep, in Hertz
const int  GO_TONE_MS   = 100;   // how long the "GO" beep lasts, in ms

const int  FAST_TONE_HZ = 1800;  // FAST   pattern: one short HIGH beep, this pitch
const int  MED_TONE_HZ  = 1200;  // MEDIUM pattern: two short beeps, this pitch
const int  SLOW_TONE_HZ = 300;   // SLOW   pattern: one long LOW buzz, this pitch
const int  SHORT_BEEP_MS = 120;  // length of a short beep, in ms
const int  LONG_BUZZ_MS  = 500;  // length of the long slow buzz, in ms
const int  GAP_MS        = 120;  // silent gap between the two MEDIUM beeps, in ms

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
  pinMode(BUZZER_PIN, OUTPUT);  // The buzzer is something we control.

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
  Serial.println("   REACTION TIME GAME (buzzer patterns)");
  Serial.println("=================================");
  Serial.println("Wait for the LED to turn ON and BEEP,");
  Serial.println("then press the button as FAST as you can!");
  Serial.println("Listen: 1 high beep = fast, 2 beeps = medium, 1 low buzz = slow.");
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

  // ---- STEP 6: Decide the category, then play its buzzer pattern ----
  // We compare reactionTime to the thresholds at the top of the file.
  if (reactionTime < FAST_MS) {
    // FAST: one short HIGH beep.
    Serial.print("FAST! ");
    tone(BUZZER_PIN, FAST_TONE_HZ, SHORT_BEEP_MS);
    delay(SHORT_BEEP_MS);                 // let the beep finish

  } else if (reactionTime < MEDIUM_MS) {
    // MEDIUM: two short beeps with a small gap between them.
    Serial.print("MEDIUM. ");
    tone(BUZZER_PIN, MED_TONE_HZ, SHORT_BEEP_MS);
    delay(SHORT_BEEP_MS);                 // wait for the first beep to end
    delay(GAP_MS);                        // short silence
    tone(BUZZER_PIN, MED_TONE_HZ, SHORT_BEEP_MS);
    delay(SHORT_BEEP_MS);                 // let the second beep finish

  } else {
    // SLOW: one long LOW buzz.
    Serial.print("SLOW. ");
    tone(BUZZER_PIN, SLOW_TONE_HZ, LONG_BUZZ_MS);
    delay(LONG_BUZZ_MS);                  // let the long buzz finish
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

  // Wait until the player releases the button before the next round,
  // so a held-down button does not affect the next "too early" check.
  while (digitalRead(BUTTON_PIN) == HIGH) {
    // do nothing, just wait for release
  }

  // The loop() function ends here and automatically starts again
  // for the next round.
}
