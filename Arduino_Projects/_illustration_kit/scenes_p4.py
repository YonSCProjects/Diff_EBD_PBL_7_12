"""scenes_p4.py — one illustration per Project 4 step: what the student's hands actually do.

Run:  python build.py 4
Each scene() returns (filename, Scene, title). Millimetres and positions come from parts.py,
which is itself tied to the printed chassis template.
"""
from iso import Scene, iso, depth, cuboid, cyl_x, cyl_y, plate, shadow, wire, arrow, tag, poly, shade, render
import parts as P

RED, BLACK, ORANGE, GREEN, BLUE = P.RED, P.BLACK, P.ORANGE, P.GREEN, P.BLUE
HL = '#e0651a'          # action-arrow orange


# ---------------------------------------------------------------- helpers
def tape_strip(sc, x, y, w, d_, z):
    """Black electrical tape painted on the floor (after the floor, before the car)."""
    pts = [iso(x, y, z), iso(x + w, y, z), iso(x + w, y + d_, z), iso(x, y + d_, z)]
    sc.add(9400, poly(pts, '#15181c', None), 0)


def bench(sc, x0=0, y0=0, w=320, d=220):
    """A neutral bench surface so parts do not float."""
    cuboid(sc, x0, y0, -14, w, d, 4, '#d9cfbe', layer=0)


def floor(sc, z=-60, x0=-60, y0=0, w=500, d=250):
    cuboid(sc, x0, y0, z - 2, w, d, 2, '#f4f1ea', layer=0)


def car_on(sc, z, brain='uno', sensors=True, battery=True):
    """The finished car at height z (used by the on-the-floor scenes)."""
    P.chassis(sc, z=z)
    P.motors_all(sc, z=z, leads=False)
    P.wheels_all(sc, z=z)
    if brain == 'uno':
        P.arduino_uno(sc, z=z, label=False)
    elif brain == 'esp':
        P.esp32_devkit(sc, z=z, label=False)
    P.l298n(sc, z=z, label=False)
    if battery:
        P.battery_box(sc, z=z, label=False)
    if sensors:
        P.ir_sensor(sc, 'left', z=z)
        P.ir_sensor(sc, 'right', z=z)


# ---------------------------------------------------------------- M1 — the soldering station
def m1_soldering_station():
    sc = Scene()
    bench(sc)
    cuboid(sc, 30, 40, -10, 200, 140, 1.2, '#3f4a55', layer=1)                # heat mat
    cuboid(sc, 60, 60, -8.8, 46, 34, 6, '#6b7078', layer=3)                   # iron stand
    cyl_x(sc, 58, 77, 8, 66, 5.5, '#2f343b', layer=3)
    cyl_x(sc, 124, 77, 8, 16, 2.2, '#b9873a', layer=3)
    tag(sc, (100, 77, 14), 'מלחם על המעמד\nכשהוא לא ביד', dy=-26, size=6.4)
    cuboid(sc, 62, 104, -8.8, 30, 24, 5, '#8fc98f', layer=3)                  # sponge
    tag(sc, (77, 116, -3), 'ספוג לח', dx=-34, dy=12, size=6.0)
    cyl_y(sc, 175, 58, 6, 14, 15, '#c9ced4', layer=3)                         # solder reel
    tag(sc, (175, 65, 22), 'בדיל', dy=-20, size=6.0)
    cuboid(sc, 148, 132, -8.8, 46, 20, 9, '#2f6fb5', layer=3)                 # goggles
    tag(sc, (171, 142, 1), 'משקפי מגן —\nלפני שמדליקים', dx=48, dy=18, size=6.2)
    cuboid(sc, 236, 92, -8.8, 58, 44, 0.8, '#fff3e0', layer=3)                # rules card
    tag(sc, (265, 114, -8), 'ארבעת הכללים\nנאמרים בקול', dx=42, dy=-4, size=6.2)
    return 'w_p4_s01_soldering_station', sc, 'soldering station'


# ---------------------------------------------------------------- M2 — solder the motor leads
def m2_solder_motor_leads():
    sc = Scene()
    bench(sc, 20, 30, 270, 190)
    mx, my, mz = 70, 82, -10
    cuboid(sc, mx, my, mz, P.MOTOR_W, P.MOTOR_D, P.MOTOR_H, P.C_MOTOR, layer=3)
    cuboid(sc, mx + 46, my + 2.5, mz + 2.5, 24, P.MOTOR_D - 5, P.MOTOR_H - 5, P.C_GEAR, layer=3)
    # the two copper tabs on the can's end face
    for i in range(2):
        cuboid(sc, mx + 68, my + 6 + i * 9, mz + 8, 4, 5, 1.4, '#c87533', layer=3)
    wire(sc, [(210, 62, 6), (168, 76, 8), (mx + 72, my + 8.5, mz + 9)], RED, 1.6)
    wire(sc, [(210, 138, 6), (170, 118, 8), (mx + 72, my + 17.5, mz + 9)], BLACK, 1.6)
    cyl_x(sc, 152, 126, 30, 46, 4.6, '#2f343b', layer=5)                      # iron
    cyl_x(sc, 146, 126, 22, 10, 2.0, '#b9873a', layer=5)
    arrow(sc, (170, 116, 20), (148, 96, 6), HL, curve=6)
    tag(sc, (mx + 72, my + 13, mz + 9), '3 שניות על הפד,\nלא יותר', dx=58, dy=-28, size=6.2)
    cyl_x(sc, 56, 154, -6, 20, 2.6, '#1d2733', layer=3)                       # heat-shrink
    tag(sc, (66, 154, -3), 'שרוול מתכווץ —\nעולה על החיבור אחר כך', dx=-24, dy=22, size=6.0)
    return 'w_p4_s02_solder_motor_leads', sc, 'solder the motor leads'


# ---------------------------------------------------------------- M3a — cut the plate
def m3a_cut_plate():
    sc = Scene()
    cuboid(sc, 8, 20, -8, 285, 180, 8, '#dfe9f0', layer=0)                    # polygal sheet
    for yy in range(26, 196, 6):
        a = iso(10, yy, 0.02); b = iso(291, yy, 0.02)
        sc.add(depth(150, yy, 0),
               '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" style="stroke:#c3d3de;stroke-width:0.34"/>'
               % (a[0], a[1], b[0], b[1]), 0)
    cuboid(sc, 23.5, 35, 0, 250, 150, 0.5, '#fffdf7', layer=1)                # paper template
    zp = 0.55
    Pp = [(38.5, 35), (258.5, 35), (273.5, 50), (273.5, 170), (258.5, 185), (38.5, 185), (23.5, 170), (23.5, 50)]
    sc.add(9000, poly([iso(px, py, zp) for px, py in Pp], 'none', '#15181c', 1.1), 1)
    for (zx, zy, zw, zd, col, txt) in ((46, 86, 68, 54, '#1f7a44', 'המוח'),
                                       (116, 88.5, 43, 43, '#b03a3a', 'L298N'),
                                       (161, 79.5, 110, 61, '#b98a1f', '8×AA')):
        pts = [iso(zx, zy, zp), iso(zx + zw, zy, zp), iso(zx + zw, zy + zd, zp), iso(zx, zy + zd, zp)]
        sc.add(9010, poly(pts, 'none', col, 0.5, 'stroke-dasharray:2.4 1.8'), 1)
        cx, cy = iso(zx + zw / 2, zy + zd / 2, zp)
        sc.add(9011, '<text x="%.2f" y="%.2f" style="font-family:Rubik,Arial;font-size:5.2px;'
                     'font-weight:700;fill:%s;text-anchor:middle">%s</text>' % (cx, cy + 1.6, col, txt), 1)
    for (mx, my) in ((56.5, 35), (56.5, 162), (170.5, 35), (170.5, 162)):
        pts = [iso(mx, my, zp), iso(mx + 70, my, zp), iso(mx + 70, my + 23, zp), iso(mx, my + 23, zp)]
        sc.add(9012, poly(pts, 'none', '#3f6bb5', 0.45, 'stroke-dasharray:2 1.6'), 1)
    for (hx, hy) in (P.SENS_L, P.SENS_R):
        cx, cy = iso(hx, hy, zp)
        sc.add(9013, '<g><circle cx="%.2f" cy="%.2f" r="2.4" style="fill:none;stroke:#c0392b;stroke-width:0.6"/>'
                     '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" style="stroke:#c0392b;stroke-width:0.6"/>'
                     '<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f" style="stroke:#c0392b;stroke-width:0.6"/></g>'
               % (cx, cy, cx - 3.4, cy, cx + 3.4, cy, cx, cy - 2.4, cx, cy + 2.4), 1)
    for tx, ty in ((28, 40), (244, 40), (28, 166), (244, 166)):
        cuboid(sc, tx, ty, 0.5, 22, 13, 0.3, '#ffdf7a', layer=1)
    P.craft_knife(sc, 150, 27, 5)
    arrow(sc, (118, 33, 7), (236, 33, 7), HL)
    tag(sc, (176, 33, 7), 'חותכים על הקו השחור —\nכמה העברות קלות, לא אחת חזקה', dy=-32, size=6.6)
    tag(sc, (23.5, 170, 1), 'פינה קטומה\n15 מ״מ', dx=-48, dy=18, size=6.0)
    tag(sc, (262, 120, 1), 'התבנית מודבקת\nעל לוח הפוליגל', dx=56, dy=6, size=6.2)
    return 'w_p4_s03a_cut_plate', sc, 'cut the plate'


# ---------------------------------------------------------------- M3b — glue the motors
def m3b_glue_motors():
    """The plate is turned over and the motors are glued to what becomes the underside."""
    sc = Scene()
    plate(sc, z=0, thickness=P.PLATE_T, col=P.C_PLATE)
    z0 = P.PLATE_T

    def bead(mx, my):
        for gx in range(int(mx) + 6, int(mx + P.MOTOR_W) - 4, 10):
            cx, cy = iso(gx, my + P.MOTOR_D / 2, z0 + 0.4)
            sc.add(depth(gx, my, z0),
                   '<ellipse cx="%.2f" cy="%.2f" rx="3.6" ry="2.0" style="fill:#f7e3b8;'
                   'stroke:#d8bd82;stroke-width:0.35"/>' % (cx, cy), 2)

    for pos, side in (('front', 'left'), ('front', 'right'), ('rear', 'left')):
        mx = P.MOTOR_FX if pos == 'front' else P.MOTOR_RX
        my = P.PLATE_Y0 if side == 'left' else P.PLATE_Y1 - P.MOTOR_D
        bead(mx, my)
        cuboid(sc, mx, my, z0, P.MOTOR_W, P.MOTOR_D, P.MOTOR_H, P.C_MOTOR, layer=3)
        can_x = mx + P.MOTOR_W - 24 if pos == 'front' else mx
        cuboid(sc, can_x, my + 2.5, z0 + 2.5, 24, P.MOTOR_D - 5, P.MOTOR_H - 5, P.C_GEAR, layer=3)

    # the fourth motor coming down onto its fresh bead
    mx, my = P.MOTOR_RX, P.PLATE_Y1 - P.MOTOR_D
    bead(mx, my)
    lift = 46
    cuboid(sc, mx, my, z0 + lift, P.MOTOR_W, P.MOTOR_D, P.MOTOR_H, P.C_MOTOR, layer=5)
    cuboid(sc, mx, my + 2.5, z0 + lift + 2.5, 24, P.MOTOR_D - 5, P.MOTOR_H - 5, P.C_GEAR, layer=5)
    arrow(sc, (mx + 35, my + 11, z0 + lift - 6), (mx + 35, my + 11, z0 + 8), HL)
    P.glue_gun(sc, 206, 200, 20)
    tag(sc, (148, 108, z0), 'הפלטה הפוכה —\nמדביקים על הצד שיהיה למטה', dy=-36, size=7.0)
    tag(sc, (mx + 35, my + 11, z0 + 10), 'פס דבק חם לאורך הגוף,\nואז לוחצים 30 שניות', dx=62, dy=-10, size=6.2)
    tag(sc, (P.AXLE_F, P.PLATE_Y0 + 11, z0 + P.MOTOR_H), 'הצירים יוצאים החוצה\nושני מנועי הצד בקו אחד', dx=-34, dy=-26, size=6.0)
    return 'w_p4_s03b_glue_motors', sc, 'glue the motors'


# ---------------------------------------------------------------- M3c — rolling chassis
def m3c_wheels_on():
    sc = Scene()
    P.chassis(sc); P.motors_all(sc, leads=False); P.wheels_all(sc)
    arrow(sc, (P.AXLE_F, P.PLATE_Y1 + 66, -8), (P.AXLE_F, P.PLATE_Y1 + 18, -8), HL)
    tag(sc, (P.AXLE_F, P.PLATE_Y1 + 40, -8), 'דוחפים את הגלגל\nעד הסוף על הציר', dx=34, dy=22, size=6.2)
    tag(sc, (148, 108, P.PLATE_T), 'שלדה מתגלגלת —\nארבעה מנועים, ארבעה גלגלים', dy=-30, size=7.0)
    return 'w_p4_s03c_wheels_on', sc, 'rolling chassis'


# ---------------------------------------------------------------- M4 — the real wiring
def m4_wiring():
    sc = Scene()
    P.chassis(sc); P.motors_all(sc, leads=False); P.wheels_all(sc)
    P.arduino_uno(sc, label=False); P.l298n(sc, label=False); P.battery_box(sc, label=False)
    P.ir_sensor(sc, 'left'); P.ir_sensor(sc, 'right')
    zt = P.PLATE_T

    # each side's two motors gathered into one run up to its OUT terminal
    for sy, tx in ((P.PLATE_Y0 + 11, P.DRV_X - 1), (P.PLATE_Y1 - 11, P.DRV_X + P.DRV_W)):
        for k, col in enumerate((RED, BLACK)):
            wire(sc, [(P.MOTOR_FX + P.MOTOR_W, sy + k * 3, -12), (132, sy + k * 3, -12),
                      (132, sy + k * 3, zt + 3), (tx, P.DRV_Y + 8 + k * 5, zt + 6)], col, 1.5)
            wire(sc, [(P.MOTOR_RX, sy + k * 3, -12), (132, sy + k * 3, -12)], col, 1.5)
    # battery -> 12V / GND
    wire(sc, [(P.BAT_X, P.BAT_Y + 20, zt + 12), (P.DRV_X + 16, P.DRV_Y + P.DRV_D + 7, zt + 8),
              (P.DRV_X + 16, P.DRV_Y + P.DRV_D, zt + 6)], RED, 2.0)
    wire(sc, [(P.BAT_X, P.BAT_Y + 27, zt + 12), (P.DRV_X + 23, P.DRV_Y + P.DRV_D + 11, zt + 8),
              (P.DRV_X + 23, P.DRV_Y + P.DRV_D, zt + 6)], BLACK, 2.0)
    # six signal wires as a tidy ribbon along the front lane
    for i in range(6):
        col = GREEN if i in (0, 5) else ORANGE
        yy = 76 - i * 1.7
        wire(sc, [(P.DRV_X + 12 + i * 2.6, P.DRV_Y + 2, zt + 4), (P.DRV_X + 12 + i * 2.6, yy, zt + 6),
                  (P.BRAIN_X + 26 + i * 2.6, yy, zt + 6), (P.BRAIN_X + 26 + i * 2.6, P.BRAIN_Y + 4, zt + 4)], col, 1.0)
    # the common ground, thick, along the near side
    wire(sc, [(P.DRV_X + 30, P.DRV_Y + P.DRV_D, zt + 6), (P.DRV_X + 30, 152, zt + 9),
              (P.BRAIN_X + 46, 152, zt + 9), (P.BRAIN_X + 46, P.BRAIN_Y + P.BRAIN_D - 4, zt + 4)], BLACK, 2.4)
    # 5 V Y-splitter + the two sensor signal wires
    P.y_splitter(sc, label=False)
    for (sx, sy), col in ((P.SENS_L, ORANGE), (P.SENS_R, GREEN)):
        wire(sc, [(sx + 12, sy, -8), (sx + 12, sy, zt + 3), (P.BRAIN_X + 18, sy, zt + 5),
                  (P.BRAIN_X + 18, P.BRAIN_Y + 4, zt + 4)], col, 1.1)

    tag(sc, (P.DRV_X + 30, 152, zt + 9), '★ הארקה משותפת —\nהחוט שבלעדיו כלום לא זז', dx=8, dy=36, size=6.4)
    tag(sc, (92, 148, zt + 5), 'מפצל 5V בשרוול מתכווץ\nבמקום ברדבורד', dx=-70, dy=14, size=6.2)
    tag(sc, (P.BRAIN_X + 34, 74, zt + 6), 'שישה חוטי אות\nאל חיבורים 5–10', dx=-6, dy=-30, size=6.2)
    tag(sc, (P.BAT_X + 55, P.BAT_Y + 30, zt + 28), 'המתג כבוי\nכל זמן החיווט', dy=-26, size=6.4)
    tag(sc, (P.SENS_L[0] + 12, P.SENS_L[1], -8), 'חיישן שמאל ← 11', dx=-104, dy=-26, size=6.0)
    tag(sc, (P.SENS_R[0] + 12, P.SENS_R[1], -8), 'חיישן ימין ← 12', dx=-70, dy=6, size=6.0)
    tag(sc, (30, 110, -6), 'שני החיישנים מוברגים\nמתחת לחרטום', dx=-52, dy=34, size=6.2)
    return 'w_p4_s04_wiring', sc, 'wiring on the car'


# ---------------------------------------------------------------- M5 — wheels in the air
def m5_wheels_in_air():
    sc = Scene()
    cuboid(sc, 96, 74, -68, 108, 84, 44, '#d3b98c', layer=0)                  # the box
    car_on(sc, 0, brain='uno', sensors=False)
    for ax in (P.AXLE_F, P.AXLE_R):
        cx, cy = iso(ax, P.PLATE_Y1 + 6 + P.WHEEL_W / 2, -12)
        sc.over('<path d="M %.2f %.2f a 22 22 0 1 1 -7 -14" style="fill:none;stroke:%s;'
                'stroke-width:2;stroke-linecap:round"/>' % (cx + 26, cy - 11, HL))
    tag(sc, (148, 108, P.PLATE_T + 28), 'הגלגלים באוויר\nלפני שמעלים קוד', dy=-28, size=7.0)
    tag(sc, (150, 116, -46), 'קופסה מתחת לפלטה', dx=96, dy=26, size=6.2)
    return 'w_p4_s05_wheels_in_air', sc, 'wheels in the air'


# ---------------------------------------------------------------- M6 — sensor test
def m6_sensor_test():
    sc = Scene()
    floor(sc, -60)
    tape_strip(sc, -70, 102, 360, 19, -58)
    car_on(sc, -46, brain='uno')
    tag(sc, (-10, 111, -58), 'הקו השחור עובר\nמתחת לשני החיישנים', dx=-58, dy=14, size=6.4)
    P.laptop(sc, 292, 26, -58)                                                # the serial monitor
    tag(sc, (367, 26, 34), 'LINE  /  FLOOR\nבמסך הטורי', dy=-24, size=6.4)
    return 'w_p4_s06_sensor_test', sc, 'sensor test'


# ---------------------------------------------------------------- M7 — the track
def m7_track():
    import math
    sc = Scene()
    floor(sc, -60, x0=-30, y0=30, w=500, d=290)
    cx0, cy0, rx, ry = 300, 206, 196, 98
    pts = [iso(cx0 + rx * math.cos(2 * math.pi * i / 72), cy0 + ry * math.sin(2 * math.pi * i / 72), -58)
           for i in range(73)]
    d = 'M ' + ' L '.join('%.2f %.2f' % p for p in pts) + ' Z'
    sc.add(9500, '<path d="%s" style="fill:none;stroke:#15181c;stroke-width:14;stroke-linejoin:round"/>' % d, 0)
    car_on(sc, -46, brain='uno')
    tag(sc, (150, 300, -58), 'מסלול סרט שחור —\nפניות רחבות, בלי פינות חדות', dy=-26, size=6.6)
    return 'w_p4_s07_track', sc, 'the track'

# ---------------------------------------------------------------- M8 — the first line run
def m8_first_run():
    """The car actually following the tape for the first time: no laptop, no cable."""
    sc = Scene()
    floor(sc, -60, x0=-60, y0=0, w=480, d=250)
    tape_strip(sc, -50, 102, 420, 19, -58)
    car_on(sc, -46, brain='uno')
    arrow(sc, (P.PLATE_X0 - 8, 111, -54), (P.PLATE_X0 - 96, 111, -54), HL, w=3.0, head=7)
    tag(sc, (P.PLATE_X0 - 52, 111, -54), 'נוסעת לבד\nלאורך הקו', dy=-22, size=6.6)
    tag(sc, (330, 111, -58), 'שני החיישנים מעל הקו —\nהמכונית מתקנת את עצמה תוך כדי', dx=20, dy=22, size=6.4)
    return 'w_p4_s08_first_run', sc, 'the first line run'


SCENES = [m1_soldering_station, m2_solder_motor_leads, m3a_cut_plate, m3b_glue_motors,
          m3c_wheels_on, m4_wiring, m5_wheels_in_air, m6_sensor_test, m7_track, m8_first_run]
