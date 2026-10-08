# פרויקט 6: תחנת מזג אוויר ב-ESP32 — הנחיות לקלוד קוד

ההנחיות הכלליות ב-`../CLAUDE.md` חלות תמיד. כאן רק מה שמיוחד לפרויקט הזה.

## הפרויקט בקצרה

- **חומרה:** ESP32 + חיישן טמפרטורה ולחות + מסך OLED
- **מה לומדים:** חיישנים, מסך, נתונים חיים בדפדפן
- **מעטפת הבטיחות (למידע בלבד — המורה מתדרך):** חזרה לשולחן ולמטריצה: אין מנועים, אין סוללות ואין הלחמה. מעטפת הבטיחות נמוכה כמו בפרויקטים 1–3, עם הבדל אחד — המודולים כאן עובדים על 3.3 וולט.

## מה על השולחן

- 1 × לוח ESP32 DevKit
- 1 × חיישן DHT22 — חדש
- 1 × מסך OLED SSD1306 בגודל 0.96" — חדש
- 1 × מטריצה + חוטי גישור
- 1 × כבל Micro-USB
- 1 × פלט אחד לבחירה — טייר 2 בלבד

## הסקיצות (`ino_files/`)

גרסה 1 מעלה את הסקיצות הממוספרות כמו שהן, לפי הסדר שהכרטיסיות מכתיבות. `T2_*` הן נקודות הפתיחה של גרסה 2 — שם התלמיד משנה דבר אחד שהכרטיסייה מצביעה עליו.

- `01_dht_serial` — Sketch 01: DHT22 to Serial (the sensor gives us numbers) Every 2 seconds it asks the DHT22 for the temperature and the humidity and prints both to the Serial Monitor. LIBRARY NEEDED (one-time, Library Manager): "DHT sensor library" by…
- `02_dht_oled` — Sketch 02: Readings on the OLED screen (your first I2C device) Same readings as Sketch 01 - now shown on the small screen attached to the ESP32. No computer needed once uploaded. LIBRARIES NEEDED (Library Manager): "Adafruit SSD1306" -…
- `03_weather_web` — Sketch 03: Weather page (screen + phone, live) The readings show on the OLED screen AND on a web page the ESP32 serves over its own Wi-Fi network. The page refreshes itself every 2 seconds - no app, no internet. HOW TO SEE IT (after…
- `T2_smart_device_starter` — Tier 2 Starter: YOUR smart device Same station as Sketch 03 - plus an OUTPUT that reacts when the humidity crosses a threshold you choose. Every block marked ==== CHANGE THIS ==== is a decision from the choice cards. Change, upload,…

## הכרטיסיות (`claude_support/cards/`)

קוראים את קובץ הכרטיסייה לפני שעונים על כל שאלה על שלב. הקבצים ממוספרים לפי סדר הלימוד.

### גרסה 1 — בנייה מודרכת

- `01_P6_T1_M1_toolchain_and_libraries.md` — מכינים את המחשב — ספריות ראשונות
- `02_P6_T1_M2_wire_dht22.md` — מחווטים את חיישן הלחות
- `03_P6_T1_M3_upload_sensor_serial.md` — החיישן נותן מספרים
- `04_P6_T1_M4_wire_oled_i2c.md` — מחברים מסך — שני חוטים לכל המידע
- `05_P6_T1_M5_upload_screen.md` — המספרים עולים על המסך
- `06_P6_T1_M6_upload_wifi_connect.md` — התחנה משדרת
- `07_P6_T1_M7_live_page.md` — הדף החי
- `08_P6_T1_M8_show_celebrate.md` — תחנת מזג אוויר משלכם — ומסיימים בגדול

### גרסה 2 — עיצוב מודרך

- `09_P6_T2_M1_startup.md` — הפעלה מרוכזת
- `10_P6_T2_M2_pick_output.md` — בוחרים מה קורה כשהלחות עולה
- `11_P6_T2_M3_set_threshold.md` — קובעים את סף ההתראה
- `12_P6_T2_M4_page_style_with_claude.md` — משפרים את הדף עם קלוד קוד
- `13_P6_T2_M5_station_identity.md` — נותנים לתחנה שם וצבע
- `14_P6_T2_M6_signature_station.md` — תחנת חתימה

### גרסה 3 — עיצוב פתוח

- `15_P6_T3_project_planner.md` — מעצבים מכשיר חכם משלכם

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
- כל מה שהכרטיסייה מסמנת "קוראים למורה".
- בטיחות: משתמשים בכרטיסיות העזר של פרויקטים 1–4 (R4 בטיחות, R2 פרוטוקול תקיעות) — לפרויקט 6 אין סט עזר משלו. — התדריך של המורה, לא שלך.
