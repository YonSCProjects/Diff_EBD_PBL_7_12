# פרויקט 7: סייר עם מצלמה — הנחיות לקלוד קוד

ההנחיות הכלליות ב-`../CLAUDE.md` חלות תמיד. כאן רק מה שמיוחד לפרויקט הזה.

## הפרויקט בקצרה

- **חומרה:** ESP32-CAM + שלדת המכונית
- **מה לומדים:** מימוש בשטח: הזרמת וידאו + נהיגה
- **מעטפת הבטיחות (למידע בלבד — המורה מתדרך):** המכונית של פרויקטים 4–5 עם מצלמה. הסיכונים זהים לפרויקט 5 — גלגלים וסוללות — ובנוסף שני פסי כוח נפרדים שהמורה מכייל לפני המפגש.

## מה על השולחן

- 1 × המכונית הפוליגל של פרויקטים 4–5
- 1 × מודול ESP32-CAM (AI-Thinker) — חדש
- 1 × מתאם FTDI + חוטים
- 1 × ממיר מוריד MP1584 או LM2596 — חדש
- 1 × קבל 470–1000µF
- ~10 × חוטי גישור
- 1 × טלפון עם דפדפן

## הסקיצות (`ino_files/`)

גרסה 1 מעלה את הסקיצות הממוספרות כמו שהן, לפי הסדר שהכרטיסיות מכתיבות. `T2_*` הן נקודות הפתיחה של גרסה 2 — שם התלמיד משנה דבר אחד שהכרטיסייה מצביעה עליו.

- `01_camera_explorer` — Sketch 01: Camera + Drive (see and steer from the phone) The ESP32-CAM creates a Wi-Fi network. One page on the phone shows LIVE VIDEO from the camera with driving buttons underneath. You explore rooms you are not in. BOARD SETTINGS…
- `T2_explorer_starter` — Tier 2 Starter: YOUR explorer Same camera + drive sketch as Sketch 01 - but now it is YOURS. Every block marked ==== CHANGE THIS ==== is a decision from the choice cards. Change, upload, refresh. Power rule: camera from the buck converter,…

## הכרטיסיות (`claude_support/cards/`)

קוראים את קובץ הכרטיסייה לפני שעונים על כל שאלה על שלב. הקבצים ממוספרים לפי סדר הלימוד.

### גרסה 1 — בנייה מודרכת

- `01_P7_T1_M1_meet_the_cam.md` — מכירים את מצלמת ה-ESP32
- `02_P7_T1_M2_upload_camera_sketch.md` — מעלים את קוד הסייר
- `03_P7_T1_M3_first_stream.md` — השידור הראשון
- `04_P7_T1_M4_mount_camera.md` — מרכיבים את המצלמה על המכונית  ⛔ שער: כללי הבטיחות של המכונית
- `05_P7_T1_M5_power_rail.md` — מסילת חשמל נפרדת למצלמה
- `06_P7_T1_M6_wire_motors.md` — ארבעה חוטים למנועים
- `07_P7_T1_M7_drive_from_page.md` — נוהגים ורואים
- `08_P7_T1_M8_drive_by_video.md` — נוהגים לפי הווידאו בלבד
- `09_P7_T1_M9_exploration_celebrate.md` — משימת סיור — ומסיימים בגדול

### גרסה 2 — עיצוב מודרך

- `10_P7_T2_M1_startup.md` — הפעלה מרוכזת
- `11_P7_T2_M2_explorer_identity.md` — נותנים לסייר שם
- `12_P7_T2_M3_speed_profile.md` — בוחרים פרופיל מהירות
- `13_P7_T2_M4_page_design.md` — מעצבים את דף הסיור
- `14_P7_T2_M5_interface_with_claude.md` — משנים את הממשק עם קלוד קוד
- `15_P7_T2_M6_design_mission.md` — מתכננים משימת סיור
- `16_P7_T2_M7_signature_exploration.md` — סיור חתימה

### גרסה 3 — עיצוב פתוח

- `17_P7_T3_project_planner.md` — מעצבים סייר משלכם

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
- גרסה 1, שלב 4 — "מרכיבים את המצלמה על המכונית": לפני השלב התלמיד עובר עם המורה על כללי הבטיחות של המכונית.
- כל מה שהכרטיסייה מסמנת "קוראים למורה".
- בטיחות: משתמשים בכרטיסיות העזר של פרויקטים 1–4 (R4 בטיחות, R2 פרוטוקול תקיעות) — לפרויקט 7 אין סט עזר משלו. — התדריך של המורה, לא שלך.
