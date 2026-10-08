# פרויקט 4: מכונית עוקבת קו — הנחיות לקלוד קוד

ההנחיות הכלליות ב-`../CLAUDE.md` חלות תמיד. כאן רק מה שמיוחד לפרויקט הזה.

## הפרויקט בקצרה

- **חומרה:** שלדת פוליגל בעבודת יד + 4 מנועים + חיישני קו
- **מה לומדים:** הלחמה ראשונה, בניית שלדה, בקר מנועים, שליטה במנועים ובתנועה דרך קוד
- **מעטפת הבטיחות (למידע בלבד — המורה מתדרך):** ההסלמה הראשונה בתוכנית. החשמל עדיין 5 וולט ובטוח — מה שחדש הוא חום ותנועה: מלחם חם, גלגלים מסתובבים ובית סוללות. זה הפרויקט הראשון עם הלחמה.

## מה על השולחן

- 1 × לוחית שלדה מפוליגל, חתוכה מהתבנית
- 4 × מנועי TT + 4 גלגלים 65 מ"מ
- 1 × בקר מנועים L298N
- 2 × חיישני קו IR (מסוג TCRT5000)
- 1 × בית סוללות 8×AA עם מתג + סוללות
- 1 × ארדואינו Uno R3 + כבל USB
- 1 × מטריצה
- ~10 × חוטי גישור M-M ו-M-F
- — × חומרת M3 ואזיקוני פלסטיק
- 1 × גליל איזולירבנד שחור

## הסקיצות (`ino_files/`)

גרסה 1 מעלה את הסקיצות הממוספרות כמו שהן, לפי הסדר שהכרטיסיות מכתיבות. `T2_*` הן נקודות הפתיחה של גרסה 2 — שם התלמיד משנה דבר אחד שהכרטיסייה מצביעה עליו.

- `01_drive_forward` — Sketch 01: Drive Forward (first motor test) Both wheels spin FORWARD at medium speed for 3 seconds, pause for 1 second, and repeat. Forever. IMPORTANT - BEFORE UPLOADING: Prop the car up so the wheels spin in the AIR and the car cannot…
- `02_sensor_test` — Sketch 02: Sensor Test (see what the car's "eyes" see) Reads the two IR line sensors many times a second and prints what each one sees to the Serial Monitor: LEFT: FLOOR RIGHT: LINE TRY IT: Open the Serial Monitor (magnifying glass,…
- `03_line_follow` — Sketch 03: Line Follow (the car drives itself!) HOW IT WORKS - the whole idea in three lines: Both sensors see the floor -> the line is between them -> drive forward. LEFT sensor sees the line -> the car drifted right -> slow the LEFT…
- `T2_line_follow_starter` — Tier 2 STARTER: tune your own car This is the full line-follower, with the settings YOU tune marked at the top. Change only the numbers in the "THINGS YOU CAN CHANGE" box - you do not have to touch anything below it. BASE_SPEED - how fast…

## הכרטיסיות (`claude_support/cards/`)

קוראים את קובץ הכרטיסייה לפני שעונים על כל שאלה על שלב. הקבצים ממוספרים לפי סדר הלימוד.

### גרסה 1 — בנייה מודרכת

- `01_P4_T1_M2_solder_motor_leads.md` — מלחימים את חוטי המנועים  ⛔ שער: הדרכת ההלחמה
- `02_P4_T1_M3_assemble_chassis.md` — בונים את השלדה מפוליגל
- `03_P4_T1_M4_wire_driver_and_sensors.md` — מחווטים את בקר המנועים ואת החיישנים
- `04_P4_T1_M5_drive_forward.md` — מעלים "נסיעה קדימה" ורואים את המכונית זזה  ⛔ שער: תדריך המנועים והסוללה
- `05_P4_T1_M6_sensor_test.md` — בודקים את עיני המכונית מעל הקו
- `06_P4_T1_M7_line_follow_first_run.md` — מעלים את קוד עוקב הקו — והמכונית נוסעת לבד
- `07_P4_T1_M8_run_track_celebrate.md` — מריצים מסלול וחוגגים

### גרסה 2 — עיצוב מודרך

- `08_P4_T2_M1_startup.md` — התחלה — מקימים את המכונית ונוסעים על הקו הישר
- `09_P4_T2_M2_pick_speed.md` — בחירה א': בוחרים את המהירות
- `10_P4_T2_M3_pick_correction_and_modify.md` — בחירה ב': בוחרים את חוזק התיקון ומשנים את הקוד עם קלוד קוד
- `11_P4_T2_M4_design_build_track.md` — בחירה ג': מעצבים ובונים את המסלול שלכם
- `12_P4_T2_M5_test_and_tune.md` — מריצים, בודקים ומכווננים
- `13_P4_T2_M6_signature_run.md` — הריצה החתומה — נותנים שם ומציגים

### גרסה 3 — עיצוב פתוח

- `14_P4_T3_project_planner.md` — מעצבים אתגר משלכם למכונית

## כרטיסיות העזר (`claude_support/reference/`)

- `R0_breadboard_basics.md` — איך עובד ברדבורד
- `R1_wiring_reference.md` — תרשימי החיווט
- `R2_stuck_protocol.md` — תקועים? קודם מנסים את זה
- `R3_claude_code_prompts.md` — איך מדברים עם קלוד קוד
- `R4_safety_reminder.md` — תזכורת בטיחות (בטיחות — של המורה)
- `R5_sketch_index.md` — איזה קוד פותחים ומתי
- `R6_soldering_basics.md` — יסודות ההלחמה (בטיחות — של המורה)

## נקודות שמצריכות את המורה בפרויקט הזה

- שלב 1 נעשה יחד עם המורה (לא ערוץ B).
- גרסה 1, שלב 1 — "מלחימים את חוטי המנועים": לפני השלב התלמיד עובר עם המורה על הדרכת ההלחמה.
- גרסה 1, שלב 4 — "מעלים "נסיעה קדימה" ורואים את המכונית זזה": לפני השלב התלמיד עובר עם המורה על תדריך המנועים והסוללה.
- כל מה שהכרטיסייה מסמנת "קוראים למורה".
- בטיחות: R4 (תזכורת בטיחות) · R6 (מדריך הלחמה) · R1 (חיווט) · R2 (פרוטוקול תקיעות) — התדריך של המורה, לא שלך.
