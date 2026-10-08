# פרויקט 3: לא להתקרב יותר מדי — הנחיות לקלוד קוד

ההנחיות הכלליות ב-`../CLAUDE.md` חלות תמיד. כאן רק מה שמיוחד לפרויקט הזה.

## הפרויקט בקצרה

- **חומרה:** ארדואינו + חיישן אולטרסוני
- **מה לומדים:** קריאת חיישן, לוגיקת סף
- **מעטפת הבטיחות (למידע בלבד — המורה מתדרך):** מעטפת בטיחות זהה לפרויקטים 1–2 — 5 וולט, בלי הלחמה, מנועים או סוללות. הרכיב החדש הוא חיישן מרחק אולטרסוני.

## מה על השולחן

- 1 × ארדואינו Uno R3 + כבל USB
- 1 × מטריצה מלאה
- 1 × חיישן מרחק HC-SR04 — חדש
- 1 × נורית LED + נגד 220Ω
- 1 × זמזם פיאזו פסיבי
- 2 × נורית + נגד נוספים
- ~8 × חוטי גישור M-M

## הסקיצות (`ino_files/`)

גרסה 1 מעלה את הסקיצות הממוספרות כמו שהן, לפי הסדר שהכרטיסיות מכתיבות. `T2_*` הן נקודות הפתיחה של גרסה 2 — שם התלמיד משנה דבר אחד שהכרטיסייה מצביעה עליו.

- `01_distance_to_serial` — Sketch 01: Distance to Serial (read the sensor, print the number) 1. The HC-SR04 sensor measures how far away the nearest object is. 2. The Arduino prints that distance, in centimetres, to the screen. 3. The number updates many times every…
- `02_distance_led_alarm` — Sketch 02: Distance + LED Alarm (light up when something is close) Everything Sketch 01 did (measure distance and print it), PLUS: when the nearest object is CLOSER than 20 cm, the LED turns ON. When the object moves away again, the LED…
- `03_distance_full_alarm` — Sketch 03: Full Alarm (light AND sound when something is close) Everything Sketch 02 did (measure distance, light the LED when closer than 20 cm), PLUS: the buzzer now BEEPS at the same time. You have a complete proximity alarm - light and…
- `T2_alarm_starter` — Tier 2 STARTER: design your own alarm This is the full alarm, but with four easy settings at the top that YOU get to change. Start by changing just the numbers and true/false values in the "THINGS YOU CAN CHANGE" box - you do not have to…

## הכרטיסיות (`claude_support/cards/`)

קוראים את קובץ הכרטיסייה לפני שעונים על כל שאלה על שלב. הקבצים ממוספרים לפי סדר הלימוד.

### גרסה 1 — בנייה מודרכת

- `01_P3_T1_M1_wire_sensor.md` — מחווטים את חיישן המרחק
- `02_P3_T1_M2_upload_distance_sketch.md` — מעלים את קוד המרחק וצופים במספר משתנה
- `03_P3_T1_M3_add_led_threshold.md` — מוסיפים לד ומעלים קוד שמאיר אותו כשמתקרבים
- `04_P3_T1_M4_add_buzzer_full_alarm.md` — מוסיפים זמזם ומעלים את האזעקה המלאה
- `05_P3_T1_M5_test_real_objects.md` — בודקים את האזעקה על עצמים אמיתיים
- `06_P3_T1_M6_show_celebrate.md` — מציגים את האזעקה וחוגגים

### גרסה 2 — עיצוב מודרך

- `07_P3_T2_M1_startup.md` — התחלה — מקימים את האזעקה ובודקים שהיא עובדת
- `08_P3_T2_M2_pick_threshold.md` — בחירה א': בוחרים את מרחק הסף
- `09_P3_T2_M3_pick_response_and_modify.md` — בחירה ב': בוחרים את התגובה ומשנים את הקוד עם קלוד קוד
- `10_P3_T2_M4_test_and_tune.md` — מעלים, בודקים ומכווננים את הסף
- `11_P3_T2_M5_signature_alarm.md` — האזעקה החתומה — נותנים שם ומציגים

### גרסה 3 — עיצוב פתוח

- `12_P3_T3_project_planner.md` — מעצבים את אזעקת הקרבה שלכם

## כרטיסיות העזר (`claude_support/reference/`)

- `R0_breadboard_basics.md` — איך עובד ברדבורד
- `R1_wiring_reference.md` — תרשימי החיווט
- `R2_stuck_protocol.md` — תקועים? קודם מנסים את זה
- `R3_claude_code_prompts.md` — איך מדברים עם קלוד קוד
- `R4_safety_reminder.md` — תזכורת בטיחות (בטיחות — של המורה)
- `R5_sketch_index.md` — איזה קוד פותחים ומתי

## נקודות שמצריכות את המורה בפרויקט הזה

- שלב 1 נעשה יחד עם המורה (לא ערוץ B).
- כל מה שהכרטיסייה מסמנת "קוראים למורה".
- בטיחות: R4 (תזכורת בטיחות) · R1 (חיווט) · R2 (פרוטוקול תקיעות) — התדריך של המורה, לא שלך.
