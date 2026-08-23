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

const ANCHOR = /<div style="display:flex; align-items:center; gap:12px; margin:0 0 \d+px;">/;
const MARK = 'data-iso="step"';

// card file  ->  [ {svg, caption, alt}, ... ]
const MAP = {
  'Project_4_Line_Following_Car': {
    'P4_T1_M1_meet_soldering_he.dc.html': [{
      svg: 'w_p4_s01_soldering_station',
      caption: '<strong>עמדת ההלחמה מוכנה:</strong> מלחם על המעמד, ספוג לח, בדיל, משקפי מגן וכרטיס ארבעת הכללים — הכול במקום לפני שמדליקים.',
      alt: 'עמדת הלחמה מסודרת על שולחן: מחצלת עמידה בחום, מלחם מונח על מעמד עם ספוג לח לידו, גליל בדיל, משקפי מגן וכרטיס ובו ארבעת כללי הבטיחות.'
    }],
    'P4_T1_M2_solder_motor_leads_he.dc.html': [{
      svg: 'w_p4_s02_solder_motor_leads',
      caption: '<strong>מלחימים חוט לכל פד:</strong> אדום לפד העליון, שחור לתחתון, שלוש שניות על כל פד — והשרוול המתכווץ עולה על החיבור אחרי שהוא מתקרר.',
      alt: 'מנוע צהוב מונח על השולחן, שני פדי הנחושת שבקצה הגוף פונים אל הצופה. חוט אדום מולחם לפד העליון וחוט שחור לתחתון, המלחם מתקרב אל הפד ולידו שרוול מתכווץ.'
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
    html = html.replace(new RegExp(`[ ]*<div ${MARK}[\\s\\S]*?\\n      </div>\\n`, 'g'), '');
    const m = html.match(ANCHOR);
    const at = m ? m.index : -1;
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
