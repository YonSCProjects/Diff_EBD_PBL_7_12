// ============================================================
// Project 3 - Don't Get Too Close (Proximity Alarm)
// Tier 2 STARTER: design your own alarm
// ============================================================
//
// This is the full alarm, but with four easy settings at the top that
// YOU get to change. Start by changing just the numbers and true/false
// values in the "THINGS YOU CAN CHANGE" box - you do not have to touch
// anything below it.
//
//   THRESHOLD_CM - how close is "too close"?  Try 5, 20, or 50.
//   USE_LED      - should the LED light up?    true or false
//   USE_BUZZER   - should the buzzer beep?      true or false
//   PULSING      - false = stays on solid.      true = blinks / beeps on-off
//
// Ask Claude Code to help you change these, then upload and test.
// Open the Serial Monitor at 9600 baud to see the distance.
// ============================================================


// ====== THINGS YOU CAN CHANGE (this is your design) ======
const int  THRESHOLD_CM = 20;     // how close is "too close", in cm (try 5 / 20 / 50)
const bool USE_LED      = true;   // light the LED when too close?
const bool USE_BUZZER   = true;   // beep the buzzer when too close?
const bool PULSING      = false;  // false = on solid, true = blink/beep on and off
// =========================================================


// ---- PIN NUMBERS (you do not need to change these) ----
const int TRIG_PIN   = 12;  // sensor: sends the ping out
const int ECHO_PIN   = 11;  // sensor: listens for the echo
const int LED_PIN    = 9;   // the alarm light, through a 220 ohm resistor
const int BUZZER_PIN = 8;   // the alarm sound (piezo buzzer)

const int  ALARM_TONE  = 1000;  // buzzer beep, in Hz
const int  PULSE_MS    = 250;   // when PULSING: how long each on/off lasts, in ms
const long SERIAL_BAUD = 9600;  // must match the Serial Monitor


// ============================================================
// readDistanceCm() - ping once and return the distance in centimetres.
// Returns 999 when no echo comes back (nothing is close enough).
// ============================================================
long readDistanceCm() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000UL);

  if (duration == 0) {
    return 999;
  }
  return duration / 58;
}


// ---- small helpers so the loop stays easy to read ----
void alarmOn() {
  if (USE_LED)    digitalWrite(LED_PIN, HIGH);
  if (USE_BUZZER) tone(BUZZER_PIN, ALARM_TONE);
}

void alarmOff() {
  if (USE_LED)    digitalWrite(LED_PIN, LOW);
  if (USE_BUZZER) noTone(BUZZER_PIN);
}


// ============================================================
// setup() runs ONE time when the Arduino powers on or resets.
// ============================================================
void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  alarmOff();

  Serial.begin(SERIAL_BAUD);
  Serial.println("=================================");
  Serial.println("   DON'T GET TOO CLOSE - your alarm");
  Serial.println("=================================");
  Serial.println();
}


// ============================================================
// loop() runs OVER AND OVER, forever. Each pass = one check.
// ============================================================
void loop() {
  long distanceCm = readDistanceCm();

  Serial.print("Distance: ");
  Serial.print(distanceCm);
  Serial.println(" cm");

  bool tooClose = (distanceCm < THRESHOLD_CM);

  if (tooClose && PULSING) {
    // Blink / beep on and off: on for PULSE_MS, off for PULSE_MS, repeating.
    bool onNow = (millis() / PULSE_MS) % 2 == 0;
    if (onNow) {
      alarmOn();
    } else {
      alarmOff();
    }
  } else if (tooClose) {
    alarmOn();        // too close, not pulsing -> steady alarm
  } else {
    alarmOff();       // far enough -> everything off
  }

  delay(50);  // short pause so pulsing looks smooth
}
