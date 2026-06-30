// ============================================================
// Project 3 - Don't Get Too Close (Proximity Alarm)
// Sketch 03: Full Alarm (light AND sound when something is close)
// ============================================================
//
// WHAT THIS SKETCH DOES:
//   Everything Sketch 02 did (measure distance, light the LED when
//   closer than 20 cm), PLUS: the buzzer now BEEPS at the same time.
//   You have a complete proximity alarm - light and sound together.
//
//   When the object moves away, both the LED and the buzzer turn off.
//
// Open the Serial Monitor at 9600 baud and bring your hand within
// about 20 cm of the sensor. The LED lights and the buzzer beeps.
// ============================================================


// ---- PIN NUMBERS (which Arduino pin each part is wired to) ----
const int TRIG_PIN   = 12;  // sensor: sends the ping out
const int ECHO_PIN   = 11;  // sensor: listens for the echo
const int LED_PIN    = 9;   // the alarm LIGHT, through a 220 ohm resistor
const int BUZZER_PIN = 8;   // the alarm SOUND (piezo buzzer)

// ---- THE THRESHOLD (how close is "too close") ----
const int THRESHOLD_CM = 20;  // closer than this many cm -> full alarm ON

// ---- THE BEEP (how high the buzzer tone is) ----
const int ALARM_TONE = 1000;  // 1000 Hz beep

// ---- COMMUNICATION SPEED (must match the Serial Monitor) ----
const long SERIAL_BAUD = 9600;


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
    return 999;  // no echo -> nothing close
  }
  return duration / 58;  // microseconds -> centimetres
}


// ============================================================
// setup() runs ONE time when the Arduino powers on or resets.
// ============================================================
void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  digitalWrite(LED_PIN, LOW);  // start with the alarm OFF
  noTone(BUZZER_PIN);          // make sure the buzzer is silent

  Serial.begin(SERIAL_BAUD);
  Serial.println("=================================");
  Serial.println("   DON'T GET TOO CLOSE");
  Serial.println("   Full alarm (light + sound) at 20 cm");
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
  Serial.print(" cm");

  // ---- THE THRESHOLD CHECK ----
  if (distanceCm < THRESHOLD_CM) {
    digitalWrite(LED_PIN, HIGH);          // too close -> light ON
    tone(BUZZER_PIN, ALARM_TONE);         //          -> buzzer BEEPS
    Serial.println("   --> TOO CLOSE! (alarm on)");
  } else {
    digitalWrite(LED_PIN, LOW);           // far enough -> light OFF
    noTone(BUZZER_PIN);                    //            -> buzzer silent
    Serial.println();
  }

  delay(100);  // small pause between checks
}
