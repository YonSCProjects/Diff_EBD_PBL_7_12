# פרויקט 5: מכונית נשלטת מרחוק — הנחיות לקלוד קוד

ההנחיות הכלליות ב-`../CLAUDE.md` חלות תמיד. כאן רק מה שמיוחד לפרויקט הזה.

## הפרויקט בקצרה

- **חומרה:** שלדת פרויקט 4 + ESP32 + עמוד שליטה בדפדפן הטלפון
- **מה לומדים:** ESP32 ראשון, שליטה מדף ווב (Wi-Fi)
- **מעטפת הבטיחות (למידע בלבד — המורה מתדרך):** אותה מכונית של פרויקט 4 עם מוח חדש. אין רכיבי כוח חדשים ואין הלחמה חדשה — הסיכונים הם אלה של פרויקט 4: גלגלים מסתובבים ובית סוללות.

## מה על השולחן

- 1 × המכונית של פרויקט 4, שלמה
- 1 × לוח ESP32 DevKit — חדש
- 1 × כבל Micro-USB
- ~8 × חוטי גישור לחיווט מחדש
- 1 × טלפון עם דפדפן

## הסקיצות (`ino_files/`)

גרסה 1 מעלה את הסקיצות הממוספרות כמו שהן, לפי הסדר שהכרטיסיות מכתיבות. `T2_*` הן נקודות הפתיחה של גרסה 2 — שם התלמיד משנה דבר אחד שהכרטיסייה מצביעה עליו.

- `00_esp32_test` — Sketch 00: ESP32 Test (is the computer ready?) Blinks the small blue LED that is already ON the ESP32 board, once per second, and prints a counting message. Nothing is wired yet - this is a handshake with the board. BEFORE UPLOADING -…
- `01_wifi_drive` — Sketch 01: Wi-Fi Drive (the car becomes its own network) The ESP32 creates a Wi-Fi network with your car's name. Your phone joins that network, opens one web page, and the buttons on that page drive the car. No app, no internet - the car…
- `T2_wifi_drive_starter` — Tier 2 Starter: YOUR driving page This is the same Wi-Fi drive sketch as Sketch 01 - but now it is YOURS. Every block marked ==== CHANGE THIS ==== is a decision you make on the choice cards. Change, upload, refresh the page on the phone,…

## הכרטיסיות (`claude_support/cards/`)

קוראים את קובץ הכרטיסייה לפני שעונים על כל שאלה על שלב. הקבצים ממוספרים לפי סדר הלימוד.

### גרסה 1 — בנייה מודרכת

- `01_P5_T1_M1_prepare_esp32.md` — מכינים את המחשב ל-ESP32
- `02_P5_T1_M2_swap_brain.md` — מחליפים את המוח של המכונית  ⛔ שער: כללי הבטיחות של המכונית
- `03_P5_T1_M3_rewire_driver.md` — מחווטים את הבקר אל ה-ESP32
- `04_P5_T1_M4_upload_drive.md` — מעלים את קוד הנהיגה
- `05_P5_T1_M5_connect_phone.md` — מתחברים מהטלפון
- `06_P5_T1_M6_first_drive.md` — הנסיעה הראשונה  ⛔ שער: תדריך הנהיגה הראשונה
- `07_P5_T1_M7_course_celebrate.md` — מסלול מכשולים — ומסיימים בגדול

### גרסה 2 — עיצוב מודרך

- `08_P5_T2_M1_startup.md` — הפעלה מרוכזת
- `09_P5_T2_M2_car_identity.md` — נותנים למכונית שם
- `10_P5_T2_M3_speed_profile.md` — בוחרים פרופיל מהירות
- `11_P5_T2_M4_page_design.md` — מעצבים את דף הנהיגה
- `12_P5_T2_M5_layout_with_claude.md` — משנים את הפריסה עם קלוד קוד
- `13_P5_T2_M6_signature_drive.md` — נסיעת חתימה

### גרסה 3 — עיצוב פתוח

- `14_P5_T3_project_planner.md` — מעצבים מצב נהיגה משלכם

## כרטיסיות העזר (`claude_support/reference/`)

לפרויקט הזה אין כרטיסיות עזר משלו — אלה כרטיסיות העזר של פרויקט 4, שמשמשות גם כאן.

- `R0_breadboard_basics.md` — איך עובד ברדבורד
- `R1_wiring_reference.md` — תרשימי החיווט
- `R2_stuck_protocol.md` — תקועים? קודם מנסים את זה
- `R3_claude_code_prompts.md` — איך מדברים עם קלוד קוד
- `R4_safety_reminder.md` — תזכורת בטיחות (בטיחות — של המורה)
- `R5_sketch_index.md` — איזה קוד פותחים ומתי
- `R6_soldering_basics.md` — יסודות ההלחמה (בטיחות — של המורה)

## נקודות שמצריכות את המורה בפרויקט הזה

- שלב 1 נעשה יחד עם המורה (לא ערוץ B).
- גרסה 1, שלב 2 — "מחליפים את המוח של המכונית": לפני השלב התלמיד עובר עם המורה על כללי הבטיחות של המכונית.
- גרסה 1, שלב 6 — "הנסיעה הראשונה": לפני השלב התלמיד עובר עם המורה על תדריך הנהיגה הראשונה.
- כל מה שהכרטיסייה מסמנת "קוראים למורה".
- בטיחות: משתמשים בכרטיסיות העזר של פרויקט 4 (R4 בטיחות, R2 פרוטוקול תקיעות) — לפרויקט 5 אין סט עזר משלו. — התדריך של המורה, לא שלך.
