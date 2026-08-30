/* embed_steps.js — put one step illustration into every Hebrew build card of P4/P5/P7.
 *
 *   node embed_steps.js            # write
 *   node embed_steps.js --check    # report only
 *
 * The figure goes immediately BEFORE the "מה עושים" heading, so the student sees what the
 * step looks like before reading the steps. Re-running replaces the block instead of
 * stacking copies (the block carries a data-iso marker).
 */
const fs = require('fs'), path = require('path');

const ROOT = path.join(__dirname, '..');
const CHECK = process.argv.includes('--check');

const MARK = 'data-iso="step"';

// The figure goes just above the card's FIRST content section, i.e. immediately before the
// heading block that carries the first <h2>. Most cards call that section "מה עושים", but the
// flight and planner cards head straight into their own sections, so anchoring on the heading
// block rather than on its wording is what works across all four projects.
function anchorIndex(html) {
  const h2 = html.indexOf('<h2 ');
  if (h2 < 0) return -1;
  const openers = /<div style="display:flex; align-items:center; gap:1[02]px;[^"]*">/g;
  let best = -1, m;
  while ((m = openers.exec(html)) !== null) {
    if (m.index >= h2) break;
    best = m.index;
  }
  return best;
}

// card file  ->  [ {svg, caption, alt}, ... ]
const MAP = {
  'Project_4_Line_Following_Car': {
    // Both P4 soldering figures live on M2 since the soldering content moved off M1
    // (feedback_2026-08-30_1152). One key, two entries — a second key of the same name
    // would silently win and drop the station figure.
    'P4_T1_M2_solder_motor_leads_he.dc.html': [{
      svg: 'w_p4_s01_soldering_station',
      caption: '<strong>עמדת ההלחמה מוכנה:</strong> מלחם על המעמד, ספוג לח, בדיל וכרטיס שלושת הכללים — הכול במקום לפני שמדליקים.',
      alt: 'עמדת הלחמה מסודרת על שולחן: מחצלת עמידה בחום, מלחם מונח על מעמד עם ספוג לח לידו, גליל בדיל וכרטיס ובו שלושת כללי הבטיחות.'
    }, {
      svg: 'w_p4_s02_solder_motor_leads',
      caption: '<strong>מלחימים חוט לכל חיבור מתכת:</strong> אדום לחיבור העליון, שחור לתחתון, שלוש שניות על כל חיבור — והשרוול המתכווץ עולה על החיבור אחרי שהוא מתקרר.',
      alt: 'מנוע צהוב מונח על השולחן, שני חיבורי המתכת שבקצה הגוף פונים אל הצופה. חוט אדום מולחם לחיבור העליון וחוט שחור לתחתון, המלחם מתקרב אל החיבור ולידו שרוול מתכווץ.'
    }],
    'P4_T1_M3_assemble_chassis_he.dc.html': [
      {
        svg: 'w_p4_s03a_cut_plate',
        caption: '<strong>שלב א׳ — חותכים:</strong> התבנית מודבקת על הפוליגל, חותכים על הקו השחור בכמה העברות קלות ולא בהעברה אחת חזקה. ארבע הפינות נחתכות באלכסון של 15 מ״מ.',
        alt: 'לוח פוליגל עם תבנית נייר מודבקת עליו. על התבנית מסומן קו מתאר שחור עם ארבע פינות קטומות, מלבנים מקווקווים לאזורי המוח, הבקר והסוללות, וסימוני קדיחה לחיישנים. סכין חיתוך נעה לאורך הקו.'
      },
      {
        svg: 'w_p4_s03b_glue_motors',
        caption: '<strong>שלב ב׳ — מדביקים:</strong> הופכים את הפלטה ומדביקים את ארבעת המנועים על הצד שיהיה למטה. פס דבק חם לאורך גוף המנוע, ואז לוחצים 30 שניות.',
        alt: 'הפלטה הפוכה, ועליה ארבעה מנועים צהובים מודבקים בשתי שורות. תחת כל מנוע פס נקודות של דבק חם, מנוע רביעי יורד למקומו וחצי כתום מסמן את כיוון הלחיצה. אקדח דבק חם מונח בצד.'
      },
      {
        svg: 'w_p4_s03c_wheels_on',
        caption: '<strong>שלב ג׳ — גלגלים:</strong> דוחפים כל גלגל עד הסוף על הציר. בסוף השלב יש שלדה מתגלגלת — ארבעה מנועים וארבעה גלגלים.',
        alt: 'השלדה עומדת על ארבעה גלגלים שחורים עם חישוק לבן. חצי כתום מסמן דחיפה של הגלגל הקדמי עד סוף הציר.'
      }
    ],
    'P4_T1_M4_wire_driver_and_sensors_he.dc.html': [{
      svg: 'w_p4_s04_wiring',
      caption: '<strong>כך זה נראה על המכונית:</strong> שישה חוטי אות מהבקר אל חיבורים <strong>5–10</strong>, שני חיישני הקו מתחת לפלטה אל חיבורים <strong>11</strong> ו-<strong>12</strong>, והחוט השחור העבה הוא ★ <strong>ההארקה המשותפת</strong>. אין ברדבורד על המכונית.',
      alt: 'מבט על המכונית המורכבת מלמעלה באלכסון: הארדואינו על צד אחד של הפלטה, בקר המנועים L298N לידו ומחזיק הסוללות מאחור. שישה חוטי אות צבעוניים עוברים מהבקר אל הארדואינו, חוט שחור עבה מחבר בין ההארקות ושני חיישני הקו תלויים מתחת לחרטום.'
    }],
    'P4_T1_M5_drive_forward_he.dc.html': [{
      svg: 'w_p4_s05_wheels_in_air',
      caption: '<strong>לפני שמדליקים — הגלגלים באוויר:</strong> קופסה או ספר מתחת לפלטה, כך שארבעת הגלגלים מסתובבים חופשי והמכונית לא בורחת מהשולחן.',
      alt: 'המכונית מונחת על קופסה נמוכה שמרימה את הפלטה, וארבעת הגלגלים מסתובבים באוויר. שני עיגולים כתומים מסמנים את הגלגלים המסתובבים.'
    }],
    'P4_T1_M6_sensor_test_he.dc.html': [{
      svg: 'w_p4_s06_sensor_test',
      caption: '<strong>בודקים את החיישנים:</strong> מזיזים את המכונית מעל פס הסרט השחור וקוראים במסך הטורי — <span dir="ltr">LINE</span> כשהחיישן מעל הקו, <span dir="ltr">FLOOR</span> כשהוא מעל הרצפה.',
      alt: 'המכונית עומדת על הרצפה כשפס סרט שחור עובר מתחתיה, ולידה מחשב נייד פתוח שעליו נפתח המסך הטורי.'
    }],
    'P4_T1_M7_line_follow_first_run_he.dc.html': [{
      svg: 'w_p4_s08_first_run',
      caption: '<strong>הנסיעה הראשונה על הקו:</strong> בלי כבל ובלי יד — שני החיישנים מעל הסרט השחור והמכונית מתקנת את עצמה תוך כדי נסיעה.',
      alt: 'המכונית נוסעת לבדה לאורך פס סרט שחור על הרצפה, וחץ כתום מסמן את כיוון הנסיעה קדימה.'
    }],
    'P4_T1_M8_run_track_celebrate_he.dc.html': [{
      svg: 'w_p4_s07_track',
      caption: '<strong>המסלול המלא:</strong> לולאה סגורה של סרט שחור עם פניות רחבות ובלי פינות חדות — פנייה חדה מדי מוציאה את שני החיישנים מהקו בבת אחת.',
      alt: 'מסלול סגור בצורת אליפסה עשוי סרט שחור רחב על הרצפה, והמכונית עומדת על הקו בקצה העליון שלו.'
    }],
    'P4_T2_M4_design_build_track_he.dc.html': [{
      svg: 'w_p4_s07_track',
      caption: '<strong>לולאה סגורה:</strong> המסלול שלכם חייב להיסגר על עצמו ולהחזיק פניות רחבות — זה מה שמאפשר למכונית להשלים סיבוב שלם בלי לאבד את הקו.',
      alt: 'מסלול סגור בצורת אליפסה עשוי סרט שחור רחב על הרצפה, והמכונית עומדת על הקו בקצה העליון שלו.'
    }]
  },

  'Project_5_Remote_Controlled_Car': {
    'P5_T1_M1_prepare_esp32_he.dc.html': [{
      svg: 'w_p5_s01_meet_esp32',
      caption: '<strong>מכירים את ה-ESP32:</strong> שקע ה-USB פונה קדימה, ושישה החיבורים שבשורה המסומנת — <span dir="ltr">32 · 33 · 25 · 26 · 27 · 14</span> — הם אלה שילכו אל בקר המנועים.',
      alt: 'לוח ESP32 מונח על שולחן. שקע ה-USB בקצה אחד, וששת החיבורים 32, 33, 25, 26, 27 ו-14 מסומנים במסגרת ירוקה לאורך שורת הפינים.'
    }],
    'P5_T1_M2_swap_brain_he.dc.html': [{
      svg: 'w_p5_s02_swap_brain',
      caption: '<strong>אותה מכונית — מוח חדש:</strong> ה-Uno יורד מהמכונית, וה-ESP32 עולה על אותו פס סקוץ׳. המנועים, הבקר והסוללות נשארים בדיוק כפי שהם.',
      alt: 'המכונית מלמעלה באלכסון: לוח הארדואינו מורם מעליה, לוח ה-ESP32 יורד אל אותו פס סקוץ׳ שעל הפלטה, ובקר המנועים ומחזיק הסוללות נשארים במקומם.'
    }],
    'P5_T1_M3_rewire_driver_he.dc.html': [{
      svg: 'w_p5_s03_rewire',
      caption: '<strong>שישה חוטים בשורה:</strong> אותו סדר בשני הקצוות. בנוסף <span dir="ltr">5V</span> מהבקר אל <span dir="ltr">VIN</span> ו-<span dir="ltr">GND</span> אל <span dir="ltr">GND</span>. חיישני הקו נשארים מוברגים ולא מחוברים.',
      alt: 'המכונית מלמעלה באלכסון: שישה חוטי אות עוברים משורת החיבורים של בקר המנועים אל שישה חיבורים סמוכים על ה-ESP32, וזוג חוטי אדום ושחור מחברים בין הבקר ללוח.'
    }],
    'P5_T1_M4_upload_drive_he.dc.html': [{
      svg: 'w_p5_s04_upload',
      caption: '<strong>מעלים דרך USB:</strong> המתג כבוי, הגלגלים באוויר וכבל ה-USB מחובר רק לצורך ההעלאה.',
      alt: 'המכונית עומדת ליד מחשב נייד פתוח, וכבל USB עובר ממנה אל המחשב.'
    }],
    'P5_T1_M5_connect_phone_he.dc.html': [{
      svg: 'w_p5_s05_connect_phone',
      caption: '<strong>המכונית פותחת רשת משלה:</strong> מחפשים בטלפון את שם הרשת, מתחברים ופותחים את הכתובת <span dir="ltr">192.168.4.1</span>.',
      alt: 'המכונית על השולחן, גלי Wi-Fi יוצאים מלוח ה-ESP32 שעליה, ולידה טלפון מונח כשמסכו כלפי מעלה ומציג את שם הרשת ואת כתובת דף הנהיגה.'
    }],
    'P5_T1_M6_first_drive_he.dc.html': [{
      svg: 'w_p5_s06_first_drive',
      caption: '<strong>הנסיעה הראשונה:</strong> לוחצים ומחזיקים כדי לנסוע, משחררים והמכונית עוצרת — בלי כבל ובלי מגע.',
      alt: 'המכונית נוסעת על הרצפה, חץ כתום מסמן את הכיוון קדימה, ובצד מונח טלפון ובו כפתורי הנהיגה.'
    }],
    'P5_T1_M7_course_celebrate_he.dc.html': [{
      svg: 'w_p5_s07_course',
      caption: '<strong>מסלול סללום:</strong> מסדרים כמה קונוסים או בקבוקים במרווחים שווים, והמכונית עוברת ביניהם מבלי להפיל אף אחד.',
      alt: 'המכונית נוסעת על הרצפה בין ארבעה קונוסים כתומים המסודרים לסירוגין לשני צדי המסלול.'
    }]
  },

  'Project_7_Camera_Explorer': {
    'P7_T1_M1_meet_the_cam_he.dc.html': [{
      svg: 'w_p7_s01_ftdi_upload',
      caption: '<strong>המצלמה והמתכנת:</strong> <span dir="ltr">TX</span> אל <span dir="ltr">U0R</span> ו-<span dir="ltr">RX</span> אל <span dir="ltr">U0T</span> — החוטים מצטלבים בכוונה. החוט הצהוב בין <span dir="ltr">IO0</span> ל-<span dir="ltr">GND</span> הוא זה שמכניס את המצלמה למצב צריבה.',
      alt: 'לוח ESP32-CAM ומולו מתכנת FTDI אדום. ארבעה חוטים עוברים ביניהם, וחוט צהוב נוסף מחבר בין שני חיבורים בקצה לוח המצלמה.'
    }],
    'P7_T1_M2_upload_camera_sketch_he.dc.html': [{
      svg: 'w_p7_s02_upload_ritual',
      caption: '<strong>שלושת הצעדים, תמיד באותו סדר:</strong> מחברים את <span dir="ltr">IO0</span> אל <span dir="ltr">GND</span>, לוחצים <span dir="ltr">RST</span> ומעלים, ואז מוציאים את החוט הצהוב.',
      alt: 'לוח המצלמה על השולחן עם החוט הצהוב מחובר, ולידו שלושה כרטיסים ממוספרים המתארים את שלושת צעדי ההעלאה בזה אחר זה.'
    }],
    'P7_T1_M3_first_stream_he.dc.html': [{
      svg: 'w_p7_s03_first_stream',
      caption: '<strong>השידור הראשון:</strong> המצלמה פותחת רשת Wi-Fi משלה, מתחברים אליה מהטלפון ורואים את הווידאו החי בדפדפן.',
      alt: 'לוח המצלמה על השולחן וגלי Wi-Fi יוצאים ממנו, ולידו טלפון מונח כשמסכו כלפי מעלה ומציג חלון וידאו וכפתורים.'
    }],
    'P7_T1_M4_mount_camera_he.dc.html': [{
      svg: 'w_p7_s04_mount_camera',
      caption: '<strong>המצלמה על החרטום:</strong> העדשה פונה קדימה ומעט כלפי מטה, כדי שהיא תראה את הרצפה שלפני המכונית ולא את התקרה.',
      alt: 'החרטום של המכונית מלמעלה באלכסון: מדף המצלמה מסומן במלבן מקווקו על הפלטה, ולוח המצלמה יורד אליו כשחץ כתום מסמן את כיוון ההנחה.'
    }],
    'P7_T1_M5_power_rail_he.dc.html': [{
      svg: 'w_p7_s05_power_rails',
      caption: '<strong>שתי מסילות, מינוס אחד משותף:</strong> הבקר מקבל <span dir="ltr">12V</span> מהסוללה ישירות, והמצלמה מקבלת <span dir="ltr">5V</span> נקיים מהממיר. הקבל צמוד למצלמה והפס הלבן שלו פונה אל <span dir="ltr">GND</span>.',
      alt: 'המכונית מלמעלה באלכסון: מחזיק הסוללות מזין את בקר המנועים בקו ישיר, וקו שני עובר דרך ממיר מתח כחול קטן אל לוח המצלמה שבחרטום. קבל מונח צמוד למצלמה.'
    }],
    'P7_T1_M6_wire_motors_he.dc.html': [{
      svg: 'w_p7_s06_cam_to_driver',
      caption: '<strong>ארבעה חוטים בלבד:</strong> <span dir="ltr">14 · 15 · 13 · 12</span> מהמצלמה אל הבקר. הכובעונים על <span dir="ltr">ENA</span> ו-<span dir="ltr">ENB</span> נשארים במקומם.',
      alt: 'המכונית מלמעלה באלכסון: ארבעה חוטי אות עוברים מלוח המצלמה שבחרטום אל שורת החיבורים של בקר המנועים, ושני כובעונים שחורים יושבים על חיבורי ENA ו-ENB.'
    }],
    'P7_T1_M7_drive_from_page_he.dc.html': [{
      svg: 'w_p7_s07_drive_from_page',
      caption: '<strong>דף אחד, שני חצאים:</strong> הווידאו למעלה וכפתורי הנהיגה למטה — נוהגים ורואים באותו מסך.',
      alt: 'המכונית עם המצלמה נוסעת על הרצפה, וחץ כתום מסמן את כיוון הנסיעה. בצד מונח טלפון ובו חלון וידאו וכפתורי נהיגה.'
    }],
    'P7_T1_M8_drive_by_video_he.dc.html': [{
      svg: 'w_p7_s08_drive_by_video',
      caption: '<strong>נוהגים לפי המסך בלבד:</strong> המכונית עוברת מאחורי מחיצה, והנהג רואה רק את מה שהמצלמה רואה.',
      alt: 'המכונית עם המצלמה נוסעת על הרצפה ליד מחיצה גבוהה שחוסמת את המבט, ובצד מונח טלפון המציג את תמונת המצלמה.'
    }]
  },

  'Project_8_Tiny_Quadcopter': {
    'P8_T1_M1_meet_parts_contract_he.dc.html': [{
      svg: 'w_p8_s01_parts_contract',
      caption: '<strong>לפני שנוגעים במשהו:</strong> מחזיקים כל רכיב ואומרים את שמו, חותמים על חוזה הבטיחות ושוקלים את המסגרת בלי סוללה — בערך <strong>75 גרם</strong>. המדחף והסוללה נשארים אצל המורה.',
      alt: 'שולחן עבודה: מסגרת הפחמן מונחת על מאזני מטבח שמראים 75 גרם, מגש ובו ארבעה מנועים, לוח ESP32, חיישן וממיר מתח, לוח המוספטים, כרטיס חוזה הבטיחות ומשקפי מגן. בפינה נפרדת המורה מחזיק מדחף וסוללה.'
    }],
    'P8_T1_M2_press_fit_motors_he.dc.html': [{
      svg: 'w_p8_s02_press_fit_motors',
      caption: '<strong>לוחצים באגודל — בלי דבק ובלי כלים:</strong> כל מנוע נכנס דרך גומיית הזרוע כשהציר כלפי מעלה. אדום/כחול לזרועות <span dir="ltr">FRONT</span> ו-<span dir="ltr">BACK</span>, שחור/לבן ל-<span dir="ltr">RIGHT</span> ו-<span dir="ltr">LEFT</span>.',
      alt: 'מסגרת הרחפן מונחת שטוח עם סימון כתום על הזרוע הקדמית. אגודל לוחץ מנוע אחד כלפי מטה לתוך גומיית הטבעת שבקצה הזרוע, שלושת המנועים האחרים כבר במקומם וחוטיהם מובלים פנימה אל מרכז המסגרת.'
    }],
    'P8_T1_M3_meet_mosfet_board_he.dc.html': [{
      svg: 'w_p8_s03_meet_mosfet_board',
      caption: '<strong>מכירים את הלוח לפני שמחברים אותו:</strong> הלשונית של המוספט היא ה-<span dir="ltr">Drain</span>, טבעת הדיודה פונה אל <span dir="ltr">BAT+</span>, ובין <span dir="ltr">BAT+</span> ל-<span dir="ltr">GND</span> אין צפצוף. הלוח עדיין לא מחובר לכלום.',
      alt: 'לוח המוספטים מונח על השולחן ובו ארבעה ערוצים מסומנים M1 עד M4, ולידו מוספט בודד מוחזק כשהכיתוב פונה קדימה. מולטימטר עם שני מחושים נוגע בפסי BAT+ ו-GND ומראה OL.'
    }],
    'P8_T1_M4_mount_electronics_he.dc.html': [{
      svg: 'w_p8_s04_mount_electronics',
      caption: '<strong>כל לוח יושב על בידוד משלו:</strong> ה-<span dir="ltr">USB</span> פונה לזרוע האחורית, החץ <span dir="ltr">X</span> של החיישן מצביע על המנוע הקדמי, ורפידה <span dir="ltr">M1</span> נמצאת קרוב לזרוע הקדמית. תא הסוללה נשאר ריק.',
      alt: 'מבט מפורק של הרחפן: לוח ה-ESP32, החיישן וממיר המתח יורדים אל הלוחית העליונה כשכל אחד על רפידת קצף, ולוח המוספטים עולה אל צדה התחתון של הלוחית התחתונה. תא הסוללה מתחתיו ריק.'
    }],
    'P8_T1_M5_power_tree_he.dc.html': [{
      svg: 'w_p8_s05_power_tree',
      caption: '<strong>שישה חוטי חשמל וזהו:</strong> מהלוח אל <span dir="ltr">IN</span> של הממיר, מ-<span dir="ltr">OUT+</span> אל <span dir="ltr">VIN</span> של ה-<span dir="ltr">ESP32</span>, ומ-<span dir="ltr">3V3</span> אל החיישן. <strong>לא <span dir="ltr">VIN</span> ולא <span dir="ltr">5V</span></strong> — החיישן יושב רק על <span dir="ltr">3V3</span>.',
      alt: 'הרחפן מלמעלה באלכסון: שלושה זוגות חוטי אדום ושחור עוברים מלוח המוספטים אל ממיר המתח, מהממיר אל חיבורי VIN ו-GND של לוח ה-ESP32, ומחיבורי 3V3 ו-GND אל החיישן. בצד מונחת שקית חסינת אש סגורה.'
    }],
    'P8_T1_M6_motor_wiring_he.dc.html': [{
      svg: 'w_p8_s06_motor_wiring',
      caption: '<strong>כל מנוע לערוץ שלו:</strong> <span dir="ltr">FRONT</span> אל <span dir="ltr">M1</span>, <span dir="ltr">RIGHT</span> אל <span dir="ltr">M2</span>, <span dir="ltr">BACK</span> אל <span dir="ltr">M3</span> ו-<span dir="ltr">LEFT</span> אל <span dir="ltr">M4</span>. אדום או לבן הם הפלוס, והמולטימטר מצפצף על <strong>1–3 אוהם</strong>.',
      alt: 'הרחפן מלמעלה באלכסון כשלוח המוספטים שמתחת ללוחית פונה אל הצופה. שמונה חוטי מנוע מגיעים אל ארבעה זוגות רפידות מסומנות M1 עד M4, ומולטימטר במצב צפצוף נוגע בשתי רפידות של ערוץ אחד ומראה 2.1 אוהם.'
    }],
    'P8_T1_M7_signal_wiring_he.dc.html': [{
      svg: 'w_p8_s07_signal_wiring',
      caption: '<strong>ארבעה חוטי שער ושני חוטי חיישן:</strong> צהוב <span dir="ltr">25</span>, כתום <span dir="ltr">26</span>, ירוק <span dir="ltr">14</span> וכחול <span dir="ltr">27</span> אל <span dir="ltr">G1–G4</span>; לבן <span dir="ltr">21</span> ואפור <span dir="ltr">22</span> אל החיישן. כולם דקים מחוטי החשמל.',
      alt: 'הרחפן מלמעלה באלכסון: ארבעה חוטים דקים בצבעים שונים יוצאים משורת החיבורים הימנית של לוח ה-ESP32, עוברים מתחת ללוחית ומגיעים אל ארבע רפידות השער שעל לוח המוספטים. שני חוטים דקים נוספים מגיעים אל החיישן.'
    }],
    'P8_T1_M8_pre_power_check_he.dc.html': [{
      svg: 'w_p8_s08_pre_power_check',
      caption: '<strong>קודם מוכיחים ורק אז מדליקים:</strong> חלק א׳ — סורקים את הפחמן במולטימטר ובכל נקודה מקבלים <span dir="ltr">OL</span>. חלק ב׳ — המורה מחבר את הסוללה, הנורית נדלקת ואף מנוע לא זז.',
      alt: 'הרחפן המחווט מונח על השולחן. מולטימטר במצב אוהם נוגע בלוחית הפחמן ובלוח המוספטים ומראה OL, ומן הצד מגיעה סוללת ליתיום שהמורה מחבר. נורית קטנה נדלקת על לוח ה-ESP32.'
    }],
    'P8_T1_M9_upload_motor_test_he.dc.html': [{
      svg: 'w_p8_s09_upload_motor_test',
      caption: '<strong><span dir="ltr">USB</span> בפנים = סוללה בחוץ:</strong> הכבל מתחבר לשקע ה-<span dir="ltr">USB</span> של הלוח, בוחרים מהירות <span dir="ltr">115200</span> ומחזיקים את כפתור ה-<span dir="ltr">BOOT</span> בזמן ההעלאה. הסוללה מחכה בשקית.',
      alt: 'הרחפן מונח על השולחן בלי סוללה ובלי מדחפים, וכבל USB עובר ממנו אל מחשב נייד פתוח. בצד מונחת שקית חסינת אש סגורה ובתוכה הסוללה.'
    }],
    'P8_T1_M10_spin_no_props_he.dc.html': [{
      svg: 'w_p8_s10_spin_no_props',
      caption: '<strong>הפעם הראשונה שהמנועים מסתובבים:</strong> אין מדחף על אף מנוע, כבל ה-<span dir="ltr">USB</span> מנותק והמחוון על <strong>0</strong> לפני <span dir="ltr">ARM</span>. לוחצים <span dir="ltr">FRONT</span> — ורק המנוע הקדמי מסתובב.',
      alt: 'הרחפן על השולחן עם הסוללה מחוברת וארבעה צירים חשופים בלי מדחפים. חץ מעגלי מסמן שהמנוע הקדמי מסתובב, ולידו מונח טלפון ובו כפתור חמוש ומחוון מצערת.'
    }],
    'P8_T1_M11_thrust_test_he.dc.html': [{
      svg: 'w_p8_s11_thrust_test',
      caption: '<strong>המדחפים עולים בפעם הראשונה — כלפי המאזניים:</strong> הרחפן הפוך על ראש העמוד, שתי גומיות על הצלחות המרכזיות בלבד, מאפסים את המאזניים והידיים נשארות מאחורי קו הסרט.',
      alt: 'רחפן מהודק הפוך על ראש עמוד מוגבה מעל מאזני מטבח, ארבעת המדחפים מסתובבים מתחת ללוחית ומנשבים כלפי הצלחת. שתי גומיות חוצות את הלוחיות המרכזיות והמאזניים מראים 168 גרם.'
    }],
    'P8_T1_M12_upload_flight_he.dc.html': [{
      svg: 'w_p8_s12_upload_flight',
      caption: '<strong>בודקים את החיישן לפני שטסים:</strong> הרחפן חמוש והמחוון על <strong>30%</strong>, דוחפים זרוע אחת כלפי מטה <strong>בעיפרון ולא באצבע</strong> — והמספר של אותו מנוע יורד. עדיין בלי מדחפים.',
      alt: 'הרחפן על השולחן בלי מדחפים כשהסוללה מחוברת. עיפרון דוחף את הזרוע הקדמית כלפי מטה וחץ כתום מסמן את כיוון הדחיפה. בצד מונח טלפון ובו מחוון מצערת בשליש הדרך.'
    }],
    'P8_T1_M13_tethered_hover_he.dc.html': [{
      svg: 'w_p8_s13_tethered_hover',
      caption: '<strong>הריחוף הראשון — על החוט:</strong> מעלים את המחוון לאט, מחזיקים בגובה <strong>10–30 ס״מ</strong> והחוט נשאר רפוי. טלפון המורה פתוח על <span dir="ltr">DISARM</span> בלבד.',
      alt: 'הרחפן מרחף מעט מעל הרצפה בתוך מעגל מסומן בסרט, וחוט דיג רפוי יורד ממנו אל עוגן שטוח על הרצפה. מאחורי קו סרט צהוב מונחים טלפון ומשקפי מגן.'
    }],
    'P8_T1_M14_post_flight_celebrate_he.dc.html': [{
      svg: 'w_p8_s14_post_flight',
      caption: '<strong>טקס הסיום, תמיד באותו סדר:</strong> הטלפון יורד מהיד, הסוללה יוצאת ונכנסת לשקית חסינת האש, ארבעת המדחפים יורדים לקופסה — ורק אז בודקים בגב האצבע אם מנוע התחמם.',
      alt: 'הרחפן על השולחן וארבעה חצים כתומים מסמנים את הסרת המדחפים כלפי מעלה. בצד קופסת מדחפים פתוחה ובה ארבעה מדחפים, טלפון מונח עם המסך כלפי מטה וסוללה נכנסת לשקית חסינת אש.'
    }],

    'P8_T2_M1_startup_he.dc.html': [{
      svg: 'w_p8_t2_s01_startup',
      caption: '<strong>מתחילים משתי פעולות:</strong> המנועים נכנסים למסגרת בלחיצת אגודל בלבד, ולידם מסדרים <strong>ארבע ערימות זהות</strong> — אחת לכל ערוץ שתלחימו.',
      alt: 'מסגרת הרחפן עם שלושה מנועים במקומם ואגודל שלוחץ את הרביעי לתוך גומיית הזרוע. לצד המסגרת ארבע ערימות רכיבים זהות, כל אחת מסומנת M1 עד M4 ובה מוספט, שני נגדים ודיודה.'
    }],
    'P8_T2_M2_solder_channel_1_he.dc.html': [{
      svg: 'w_p8_t2_s02_solder_channel_1',
      caption: '<strong>ערוץ אחד, רגל אחר רגל:</strong> טבעת הדיודה פונה אל <span dir="ltr">BAT+</span>, הכיתוב של המוספט פונה לצד פד <span dir="ltr">G1</span>, מלחימים בכל חור שלישי ולא יותר מ-3 שניות על כל רגל.',
      alt: 'לוח מחוררים על מחצלת עבודה ועליו ערוץ אחד מולחם: מוספט שוכב שטוח, שני נגדים ודיודה. מלחם מונח על אחת ההלחמות ומשקפי מגן מונחים בצד.'
    }],
    'P8_T2_M3_check_channel_1_he.dc.html': [{
      svg: 'w_p8_t2_s03_check_channel_1',
      caption: '<strong>בודקים לפני שממשיכים:</strong> מחוש אדום על <span dir="ltr">M1−</span> ושחור על <span dir="ltr">BAT+</span> נותן <strong>0.2V–0.35V</strong>; מחליפים בין המחושים ומקבלים <span dir="ltr">OL</span>; ובין <span dir="ltr">BAT+</span> ל-<span dir="ltr">GND</span> אין צפצוף.',
      alt: 'הערוץ המולחם על לוח המחוררים ומולטימטר במצב דיודה. שני המחושים נוגעים ברפידת M1 מינוס ובפס BAT+, והתצוגה מראה 0.28 וולט.'
    }],
    'P8_T2_M4_solder_channels_2_4_he.dc.html': [{
      svg: 'w_p8_t2_s04_solder_channels_2_4',
      caption: '<strong>עוד שלושה ערוצים זהים:</strong> לפחות שני חורים ריקים בין מוספט למוספט, שרוול מתכווץ על ארבע הלשוניות, והרגל הארוכה של הקבל אל פס <span dir="ltr">BAT+</span> — קבל אחד לכל הלוח.',
      alt: 'לוח המחוררים עם ארבעה ערוצים מולחמים זה לצד זה, לשוניות המוספטים מכוסות בשרוול מתכווץ וקבל אלקטרוליטי אחד ניצב בקצה הלוח. מלחם נוגע באחת ההלחמות.'
    }],
    'P8_T2_M5_tune_mt3608_he.dc.html': [{
      svg: 'w_p8_t2_s05_tune_mt3608',
      caption: '<strong>מכוונים את הממיר לפני שהוא פוגש את ה-<span dir="ltr">ESP32</span>:</strong> המחוש האדום על <span dir="ltr">OUT+</span> והשחור על <span dir="ltr">OUT−</span>, מסובבים שלושה סיבובים לכיוון אחד ועוצרים בין <strong>4.95V ל-5.05V</strong>.',
      alt: 'ממיר מתח כחול מונח לבדו על השולחן, מברג קטן מסובב את הבורג הכחול שעליו וחץ מעגלי מסמן את כיוון הסיבוב. מולטימטר מחובר ליציאת הממיר ומראה 5.00 וולט, ולוח ה-ESP32 מונח הרחק בקצה השולחן.'
    }],
    'P8_T2_M6_mount_and_wire_he.dc.html': [{
      svg: 'w_p8_t2_s06_mount_and_wire',
      caption: '<strong>הרחפן השלם:</strong> כל לוח על רפידה משלו, החץ <span dir="ltr">X</span> מצביע על המנוע הקדמי, רפידה <span dir="ltr">M1</span> קרובה לזרוע הקדמית ושום מתכת לא נוגעת בפחמן. תא הסוללה עדיין ריק.',
      alt: 'הרחפן המורכב במלואו מלמעלה באלכסון: לוח ה-ESP32, החיישן וממיר המתח על הלוחית העליונה, לוח המוספטים מתחת לתחתונה, וכל חוטי החשמל, השער והחיישן מחוברים במקומם.'
    }],
    'P8_T2_M7_pre_power_check_he.dc.html': [{
      svg: 'w_p8_t2_s07_pre_power_check',
      caption: '<strong>מוכיחים שהרחפן בטוח ואז מדליקים:</strong> סורקים את לוח הפחמן ומקבלים <span dir="ltr">OL</span> בכל נקודה, המורה מחבר את הסוללה ומודדים <span dir="ltr">VIN</span> מול <span dir="ltr">GND</span> — <strong>4.9V–5.1V</strong>.',
      alt: 'הרחפן ללא מדחפים על השולחן עם הסוללה מחוברת. שני מחושי מולטימטר נוגעים בחיבורי VIN ו-GND של לוח ה-ESP32 והתצוגה מראה 4.98 וולט, ונורית קטנה דולקת על הלוח.'
    }],
    'P8_T2_M8_upload_and_spin_he.dc.html': [{
      svg: 'w_p8_t2_s08_upload_and_spin',
      caption: '<strong>מנתקים את הכבל ורק אז מסובבים:</strong> אין מדחף על אף מנוע, המחוון על <strong>0</strong>, לוחצים <span dir="ltr">ARM</span> ואז <span dir="ltr">FRONT</span> — ורק המנוע הקדמי מסתובב.',
      alt: 'הרחפן על השולחן בלי מדחפים כשהסוללה מחוברת וכבל ה-USB מנותק ומונח ליד המחשב הנייד. חץ מעגלי מסמן שהמנוע הקדמי מסתובב, ובצד טלפון עם כפתור חמוש.'
    }],
    'P8_T2_M9_thrust_test_he.dc.html': [{
      svg: 'w_p8_t2_s09_thrust_test',
      caption: '<strong>מודדים דחף ומחליטים לפי מספרים:</strong> הרחפן הפוך על ראש העמוד, שתי גומיות על הצלחות המרכזיות, חוט גיבוי רפוי של <strong>30 ס״מ</strong> והידיים מאחורי קו הסרט.',
      alt: 'רחפן מהודק הפוך על ראש עמוד מעל מאזני מטבח, ארבעת המדחפים מסתובבים ומנשבים כלפי הצלחת, וחוט גיבוי רפוי יורד מהרחפן אל בסיס העמוד.'
    }],
    'P8_T2_M10_choices_and_claude_he.dc.html': [{
      svg: 'w_p8_t2_s10_choices_and_claude',
      caption: '<strong>קודם המצב הבטוח, ואז הקוד:</strong> עוברים באצבע על ארבעת הצירים כדי לוודא שאין מדחף, הסוללה אצל המורה — ומשנים רק בתוך הבלוקים המסומנים בקוד ההתחלה.',
      alt: 'הרחפן על השולחן וארבעה עיגולים כתומים מסמנים את ארבעת הצירים החשופים בלי מדחפים. כבל USB עובר מהרחפן אל מחשב נייד פתוח, ובצד שקית חסינת אש סגורה ובה הסוללה.'
    }],
    'P8_T2_M11_tethered_hover_tuning_he.dc.html': [{
      svg: 'w_p8_t2_s11_tethered_hover_tuning',
      caption: '<strong>לולאת הכוונון:</strong> מחוון על <strong>0</strong>, לוחצים <span dir="ltr">ARM</span> ומעלים לאט, מרחפים <strong>10–30 ס״מ</strong> — ואז נוחתים, משנים <strong>קבוע אחד</strong> וטסים טיסה אחת.',
      alt: 'הרחפן מרחף מעט מעל הרצפה בתוך מעגל מסומן בסרט וחוט הדיג שוכב רפוי על הרצפה. מאחורי קו הסרט מונח טלפון עם דף הנהיגה, ולידו כרטיס רישום של הכוונונים.'
    }],
    'P8_T2_M12_flight_sequence_he.dc.html': [{
      svg: 'w_p8_t2_s12_flight_sequence',
      caption: '<strong>בוחרים רצף ומכריזים עליו למורה:</strong> קוראים בקול את רשימת הבדיקה של <span dir="ltr">R4</span>, הגובה נשאר <strong>10–30 ס״מ</strong> — ורצף ג׳ נטוס רק עם חוט מלא.',
      alt: 'מבט רחב על אזור הטיסה: מעגל מסומן בסרט על הרצפה ובתוכו שלושה סימוני נחיתה מסומנים א׳, ב׳ ו-ג׳. הרחפן טס נמוך מעליהם על חוט, ומאחורי קו הסרט מונח כרטיס רשימת הבדיקה.'
    }],
    'P8_T2_M13_signature_flight_he.dc.html': [{
      svg: 'w_p8_t2_s13_signature_flight',
      caption: '<strong>הטיסה שהכול היה בשבילה:</strong> החוט קשור בלולאה ובעוגן השטוח, מטיסים את הרצף שבחרתם פעם אחת, הצופה נשאר מאחורי קו הצופים — ובסוף הסוללה יוצאת ואז המדחפים יורדים.',
      alt: 'הרחפן מרחף מעל סימון ההמראה בתוך המעגל המסומן בסרט, חוט דיג מחבר אותו לעוגן שטוח על הרצפה. מאחורי קו הסרט עומדים טלפון ומשקפי מגן, ובצד שקית חסינת אש.'
    }],
    'P8_T3_project_planner_he.dc.html': [{
      svg: 'w_p8_t3_planner',
      caption: '<strong>מוסיפים רכיב אחד — במצב הבטוח:</strong> הסוללה בחוץ והמדחפים בקופסה, משתמשים רק בפינים הפנויים, ואז שוקלים שוב: <strong>יותר מ-3 גרם</strong> — חוזרים על מבחן הדחף.',
      alt: 'הרחפן על השולחן בלי סוללה ובלי מדחפים, ורכיב הרחבה חדש יורד אל הלוחית העליונה ומתחבר לשני חוטי החיישן הקיימים. בצד קופסת מדחפים פתוחה ומאזני מטבח שמראים 104 גרם.'
    }]
  }
};

function figure(svg, caption, alt) {
  return `      <div ${MARK} style="border:1px solid oklch(0.93 0.006 85); border-radius:14px; overflow:hidden; background:oklch(0.985 0.004 85); margin:0 0 26px;">
        <div dir="ltr" style="padding:20px 18px 12px; display:flex; justify-content:center;">
          <img src="./assets/${svg}.svg" alt="${alt}" style="width:620px; max-width:100%; height:auto;" />
        </div>
        <div style="padding:11px 16px; background:#fff; border-top:1px solid oklch(0.94 0.006 85); font-size:13.5px; line-height:1.6; color:oklch(0.5 0.012 260);">${caption}</div>
      </div>
`;
}

let written = 0, missing = [];
for (const [proj, cards] of Object.entries(MAP)) {
  const dir = path.join(ROOT, proj, 'task_cards_he');
  for (const [file, figs] of Object.entries(cards)) {
    const fp = path.join(dir, file);
    if (!fs.existsSync(fp)) { missing.push(file); continue; }
    for (const f of figs) {
      if (!fs.existsSync(path.join(dir, 'assets', f.svg + '.svg'))) missing.push(proj + '/' + f.svg);
    }
    let html = fs.readFileSync(fp, 'utf8');
    // drop any block this script wrote before, so re-running is idempotent
    // strip whatever this script wrote before, so re-running never stacks copies.
    // The cards are checked out with CRLF on Windows, so both endings have to match here —
    // a \n-only pattern silently fails and every run adds another figure.
    html = html.replace(
      new RegExp(`[ ]*<div ${MARK}[\\s\\S]*?\\r?\\n      </div>\\r?\\n(\\r?\\n)?`, 'g'), '');
    const at = anchorIndex(html);
    if (at < 0) { missing.push(file + ' (no anchor)'); continue; }
    const block = figs.map(f => figure(f.svg, f.caption, f.alt)).join('\n');
    html = html.slice(0, at - 6) + block + '\n' + html.slice(at - 6);
    if (!CHECK) fs.writeFileSync(fp, html);
    written++;
    console.log(`  ${figs.length === 1 ? ' ' : figs.length} ${file}`);
  }
}
console.log(`\n${CHECK ? 'would update' : 'updated'} ${written} cards`);
if (missing.length) console.log('MISSING:\n  ' + missing.join('\n  '));
