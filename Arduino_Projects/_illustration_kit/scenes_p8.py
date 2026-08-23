"""scenes_p8.py — one illustration per Project 8 step: what the student's hands actually do.

Run:  python build.py 8
Each scene() returns (filename, Scene, title).

Every technical detail here is checked against _illustration_kit/p8_facts_and_briefs.json, which
was extracted from Arduino_Project_8.md, the .ino files and all 28 Hebrew cards. The ones that
are easy to draw wrongly:
  - opposite arms spin the SAME way: FRONT+BACK = CW, RIGHT+LEFT = CCW
  - CW motors carry RED(+)/BLUE(-) leads, CCW motors WHITE(+)/BLACK(-)
  - the MOSFET board hangs UNDER the bottom plate; the LiPo hangs under that, on two O-rings
  - the DevKit's micro-USB faces the BACK arm; the MPU6050's X arrow points at the FRONT motor
  - props go on at the very last step, and every practice flight is on the tether
"""
import math
from iso import (Scene, iso, depth, cuboid, cyl_x, cyl_y, cyl_z, disc, ring_z, prism, blade,
                 spin_arc, wire, arrow, tag, poly, shade)
import parts_p8 as P

RED, BLACK, ORANGE, GREEN, BLUE, YELLOW = P.RED, P.BLACK, P.ORANGE, P.GREEN, P.BLUE, P.YELLOW
WHITE_W, GREY_W, HL = P.WHITE_W, P.GREY_W, P.HL
CX, CY = P.CTR_X, P.CTR_Y
ZD, ZM, ZB = P.Z_DECK, P.Z_MOSFET, P.Z_BAT


# ---------------------------------------------------------------- shared helpers
def bench_for_drone(sc, props=False, pad=26):
    """A bench just big enough for the machine, so the auto-fit viewBox does not waste space."""
    r = (P.PROP_R if props else P.ARM_R + P.RING_RO) + pad
    P.bench(sc, CX - r, CY - r, 2 * r, 2 * r)


def loose_motor(sc, x, y, z, spin='cw', layer=3, lift=0.0):
    """One 8520 lying where it was left, leads showing which pair it belongs to."""
    cyl_z(sc, x, y, z + lift, P.MOTOR_H, P.MOTOR_R, P.C_CAN, cap_col=P.C_BELL, layer=layer)
    cyl_z(sc, x, y, z + lift + P.MOTOR_H, P.SHAFT_H, P.SHAFT_R, '#9aa0a6', layer=layer)
    for i, col in enumerate(P.LEAD_COL[spin]):
        off = (i - 0.5) * 2.4
        wire(sc, [(x + P.MOTOR_R, y + off, z + lift + 6), (x + 16, y + off + 3, z + lift + 1)],
             col, 0.9, layer=layer + 1)


def loose_prop(sc, x, y, z, cw=True, layer=3):
    col = P.C_PROP_CW if cw else P.C_PROP_CCW
    cyl_z(sc, x, y, z, 3.2, P.PROP_HUB, '#1f2329', layer=layer, hole=0.6)
    for a in (0, 180):
        blade(sc, x, y, z + 2.4, a + (18 if cw else -18), P.PROP_HUB, P.PROP_R, col, cw=cw, layer=layer)


def gate_wires(sc, z=0.0, layer=4, only=None):
    """The four PWM wires: DevKit right header -> the gate pad of that arm's channel.
    They run over the deck, down the side and under the plate, clear of every prop circle."""
    # the right header, counting from the nose: VIN GND 13 12 14 27 26 25 ...
    idx = {'back': 4, 'left': 5, 'right': 6, 'front': 7}
    for which in ('front', 'right', 'back', 'left'):
        if only and which not in only:
            continue
        px, py, pz = P.devkit_pin('right', idx[which], z=z + ZD)
        bx = P.MOSFET_XY[0] + 8.5 + (P.CHANNEL[which] - 1) * 11.4
        by = P.MOSFET_XY[1] + 3.4
        wire(sc, [(px, py, pz), (px, py + 12, pz - 2), (bx + 2, by + 16, z + ZM + 3),
                  (bx, by, z + ZM + 1.4)], P.SIG_COL[which], 0.75, layer=layer)


def i2c_wires(sc, z=0.0, layer=4):
    """SDA 21 white and SCL 22 grey, DevKit left header to the MPU6050."""
    for idx, col, dx in ((10, WHITE_W, 0), (13, GREY_W, 2.6)):
        px, py, pz = P.devkit_pin('left', idx, z=z + ZD)
        wire(sc, [(px, py, pz), (px - 6, py - 9, pz + 2),
                  (P.IMU_XY[0] + 4 + dx, P.IMU_XY[1] + 1.4, z + ZD + P.IMU_T + 2)], col, 0.75, layer=layer)


def power_tree(sc, z=0.0, layer=4, battery=False):
    """The six power wires, in the order the card builds them."""
    mx, my = P.MOSFET_XY
    tx, ty = P.MT_XY
    # 1-2  board second BAT+/GND  ->  MT3608 IN (the side with the big inductor)
    for i, col in enumerate((RED, BLACK)):
        wire(sc, [(mx + 44, my + 4 + i * 3, z + ZM + 2),
                  (mx + 52, my - 6 + i * 3, z + 4),
                  (tx + 2, ty + 3 + i * 6, z + ZD + 1)], col, 1.3, layer=layer)
    # 3-4  MT3608 OUT  ->  DevKit VIN and the GND beside it, both on the right header
    for i, col in enumerate((RED, BLACK)):
        px, py, pz = P.devkit_pin('right', i, z=z + ZD)
        wire(sc, [(tx + P.MT_W - 2, ty + 4 + i * 6, z + ZD + 1),
                  (tx + P.MT_W + 8, ty + 10 + i * 4, z + ZD + 5), (px, py, pz)], col, 1.15, layer=layer)
    # 5-6  DevKit 3V3 and its neighbouring GND  ->  the MPU6050
    for i, col in enumerate((RED, BLACK)):
        px, py, pz = P.devkit_pin('left', i, z=z + ZD)
        wire(sc, [(px, py, pz), (px - 8, py - 14, pz + 3),
                  (P.IMU_XY[0] + 12 + i * 2.6, P.IMU_XY[1] + 1.4, z + ZD + P.IMU_T + 2)],
             col, 0.8, layer=layer)
    if battery:
        wire(sc, [(P.BAT_XY[0] - 5, CY - 2, z + ZB + 5), (mx - 4, my + 6, z + ZM + 3),
                  (mx + 4, my + 3.4, z + ZM + 2)], RED, 1.4, layer=layer - 2)
        wire(sc, [(P.BAT_XY[0] - 5, CY + 2, z + ZB + 5), (mx - 4, my + 12, z + ZM + 3),
                  (mx + 4, my + 36, z + ZM + 2)], BLACK, 1.4, layer=layer - 2)


def motor_wires_to_board(sc, z=0.0, layer=2):
    """Each motor's pair landing on its own channel pads."""
    mx, my = P.MOSFET_XY
    for which in P.ORDER:
        rx, ry = P.POS[which]
        bx = mx + 4 + (P.CHANNEL[which] - 1) * 11.4
        ang = math.radians(P.ARM_ANGLE[which] + 180)
        ca, sa = math.cos(ang), math.sin(ang)
        for i, col in enumerate(P.LEAD_COL[P.SPIN[which]]):
            off = (i - 0.5) * 2.4
            wire(sc, [(rx + ca * (P.MOTOR_R + 0.2) - sa * off, ry + sa * (P.MOTOR_R + 0.2) + ca * off,
                       z + P.Z_CAN + 6),
                      (rx + ca * 16 - sa * off, ry + sa * 16 + ca * off, z - 1.2),
                      (bx + 1 + i * 4, my + (3.4 if i == 0 else 36), z + ZM + 1.6)], col, 0.9, layer=layer)


def probes_on(sc, a, b, x=250, y=40, z=-20, reading=None, mode=None):
    P.multimeter(sc, x, y, z, reading=reading, mode=mode, probes=(a, b))


def safe_state(sc, x, y, z, text='מצב בטוח:\nבלי מדחפים ובלי סוללה'):
    """The little green badge the safety-critical cards all carry."""
    cuboid(sc, x, y, z, 54, 30, 0.8, '#dff2e4', layer=3)
    tag(sc, (x + 27, y + 15, z + 1), text, dy=-2, size=6.0, fill='#dff2e4', stroke='#25a05a',
        color='#1c6b3a', leader=False)


# ================================================================ TRACK 1
def t1_m1_parts_contract():
    """Naming every part, signing the contract, and weighing the airframe without a cell."""
    sc = Scene()
    P.bench(sc, 18, 14, 330, 218)
    P.kitchen_scale(sc, 95, 78, -20, reading='75 g')
    P.frame(sc, z=-10.4, front_mark=True)
    tag(sc, (CX, CY - 24, -10.4), 'שוקלים בלי סוללה — בערך 75 גרם', dx=-10, dy=-40, size=6.4)

    P.tray(sc, 232, 34, -20, w=104, d=88)                         # the student's tray
    for i, (mx, my, sp) in enumerate(((248, 48, 'cw'), (248, 68, 'cw'),
                                      (248, 92, 'ccw'), (248, 112, 'ccw'))):
        loose_motor(sc, mx, my, -18.5, spin=sp)
    P.devkit(sc, x=288, y=44, z=-18.5, layer=3)
    P.mpu6050(sc, x=292, y=82, z=-18.5, layer=3)
    P.mt3608(sc, x=288, y=102, z=-18.5, layer=3)
    tag(sc, (256, 60, -12), 'מחזיקים כל רכיב\nואומרים את שמו', dx=44, dy=-34, size=6.4)

    P.mosfet_board(sc, x=232, y=132, z=-19.4, layer=3)
    P.card(sc, 40, 150, -19.4, w=62, d=48, lines=4)               # the R3 safety contract
    tag(sc, (71, 174, -19), 'חותמים על חוזה הבטיחות', dx=-30, dy=32, size=6.4)
    P.goggles(sc, 44, 108, -19.4)

    # the teacher's corner: shown, never handed over
    cuboid(sc, 28, 26, -20, 78, 62, 1.2, '#ecd9d9', layer=0)
    loose_prop(sc, 52, 46, -18.6, cw=True)
    P.lipo(sc, x=68, y=64, z=-18.6, layer=3, leads=False)
    tag(sc, (56, 50, -14), 'מדחף וסוללה —\nהמורה מראה ולא מוסר', dx=-16, dy=-40, size=6.4)
    return 'w_p8_s01_parts_contract', sc, 'parts and the contract'


def t1_m2_press_fit_motors():
    """Thumb pressure only: each 8520 goes down through its rubber grommet, shaft up."""
    sc = Scene()
    bench_for_drone(sc, pad=34)
    P.frame(sc, front_mark=True)
    for which in ('left', 'right', 'back'):
        P.coreless_motor(sc, which, leads=True)
    P.coreless_motor(sc, 'front', leads=False, foot=False, lift=30)
    fx, fy = P.POS['front']
    P.hand_thumb(sc, fx, fy, P.Z_CAN + 30 + P.MOTOR_H + 2)
    arrow(sc, (fx, fy - 12, P.Z_CAN + 34), (fx, fy - 12, P.Z_CAN + 6), HL)
    tag(sc, (fx, fy - 12, P.Z_CAN + 40), 'לוחצים באגודל —\nבלי דבק ובלי כלים', dx=-46, dy=-20, size=6.6)
    tag(sc, (P.POS['back'][0] - 8, CY + 4, P.Z_CAN + 8), 'אדום/כחול — FRONT ו-BACK', dx=58, dy=6, size=6.2)
    tag(sc, (CX + 6, P.POS['right'][1] - 10, P.Z_CAN + 8), 'שחור/לבן — RIGHT ו-LEFT', dx=18, dy=42, size=6.2)
    tag(sc, (CX, CY, P.Z_PLATE_TOP), 'שום חוט לא נשאר במעגל המדחף', dx=-70, dy=30, size=6.2)
    return 'w_p8_s02_press_fit_motors', sc, 'press-fit the motors'


def t1_m3_meet_mosfet_board():
    """Meeting the pre-soldered board: what each part is, and the three meter checks."""
    sc = Scene()
    P.bench(sc, 86, 56, 150, 116)
    P.mosfet_board(sc, x=96, y=70, z=-19.4, pads=True)
    bx, by, zt = 96, 70, -19.4 + P.MOSFET_T
    # one spare MOSFET held up, label toward the viewer, legs down
    P.to220(sc, 176, 84, -19.4, flat=False, shrink=False, layer=5)
    tag(sc, (237, 98, -19.4 + 14), 'הלשונית היא ה-Drain', dx=40, dy=-26, size=6.4)
    tag(sc, (232, 100, -19.4), 'G · D · S', dx=34, dy=26, size=6.2)
    probes_on(sc, (bx + 6, by + 3.4, zt + 1.4), (bx + 44, by + 36, zt + 1.4),
              x=174, y=118, z=-24, reading='OL', mode='Ω')
    tag(sc, (bx + 25, by + 20, zt + 8), 'BAT+ מול GND — אין צפצוף', dx=-24, dy=-42, size=6.4)
    tag(sc, (bx + 8.5, by + 15, zt + 3), 'פד G מול GND — בערך 10kΩ', dx=-64, dy=16, size=6.2)
    tag(sc, (bx + 12, by + 8, zt + 3), 'טבעת הדיודה פונה אל BAT+', dx=-56, dy=44, size=6.2)
    safe_state(sc, 174, 40, -19.4, 'הלוח לא מחובר לכלום')
    return 'w_p8_s03_meet_mosfet_board', sc, 'meet the MOSFET board'


def t1_m4_mount_electronics():
    """Every board comes down onto its own full-footprint pad. The battery bay stays empty."""
    sc = Scene()
    bench_for_drone(sc, pad=40)
    P.frame(sc, front_mark=True, tether_loop=True)
    P.motors_all(sc)
    P.mosfet_board(sc, z=ZM - 26, flip=True, layer=2)
    arrow(sc, (CX + 22, CY + 30, ZM - 22), (CX + 22, CY + 30, ZM - 2), HL)
    tag(sc, (P.MOSFET_XY[0] + 8, P.MOSFET_XY[1] + 3, ZM - 25),
        'רפידה M1 קרובה לזרוע הקדמית', dx=-64, dy=30, size=6.2)

    P.devkit(sc, z=ZD + 34, pad=True)
    arrow(sc, (CX, CY, ZD + 30), (CX, CY, ZD + 4), HL)
    tag(sc, (CX + 20, CY + 12, ZD + 38), 'ה-USB פונה לזרוע האחורית', dx=64, dy=-14, size=6.4)
    P.mpu6050(sc, z=ZD + 16, pad=True)
    tag(sc, (P.IMU_XY[0] + 3, P.IMU_XY[1] + 12, ZD + 18), 'החץ X מצביע על המנוע הקדמי',
        dx=-58, dy=26, size=6.4)
    P.mt3608(sc, z=ZD + 16, pad=True)
    tag(sc, (CX, CY, ZD + 2), 'כל לוח יושב על בידוד משלו', dx=76, dy=34, size=6.2)
    safe_state(sc, CX - 27, CY + 74, P.Z_PLATE, 'תא הסוללה נשאר ריק')
    return 'w_p8_s04_mount_electronics', sc, 'mount the electronics'


def t1_m5_power_tree():
    """Six power wires and nothing else. The cell is still in the teacher's bag."""
    sc = Scene()
    bench_for_drone(sc, pad=40)
    P.frame(sc, front_mark=True)
    P.motors_all(sc)
    P.mosfet_board(sc, z=ZM, flip=True, layer=2)
    P.devkit(sc); P.mt3608(sc, locked=True); P.mpu6050(sc)
    power_tree(sc)
    tx, ty = P.MT_XY
    tag(sc, (tx + 4, ty + 8, ZD + 4), 'אדום לפלוס ושחור למינוס', dx=-62, dy=-16, size=6.2)
    tag(sc, (tx + P.MT_W - 2, ty + 6, ZD + 4), 'מ-OUT+ אל VIN של ה-ESP32', dx=62, dy=-24, size=6.2)
    px, py, pz = P.devkit_pin('left', 0)
    tag(sc, (px, py, pz), '3V3 — לא VIN ולא 5V', dx=-70, dy=22, size=6.2)
    P.lipo_bag(sc, CX + 74, CY - 34, -24, layer=0)
    tag(sc, (CX + 119, CY - 3, -2), 'הסוללה נשארת אצל המורה', dx=34, dy=-24, size=6.4)
    return 'w_p8_s05_power_tree', sc, 'the power tree'


def t1_m6_motor_wiring():
    """Eight joints, two per motor, one channel each — and the meter proves it."""
    sc = Scene()
    P.bench(sc, 52, 46, 168, 164)
    P.frame(sc, front_mark=True)
    P.motors_all(sc, leads=False)
    P.mosfet_board(sc, z=ZM, flip=True, pads=True, layer=2)
    motor_wires_to_board(sc)
    P.devkit(sc); P.mt3608(sc); P.mpu6050(sc)
    mx, my = P.MOSFET_XY
    tag(sc, (mx + 5, my + 3.4, ZM + 3), 'החוט האדום אל +M1 והכחול אל −M1', dx=-58, dy=34, size=6.2)
    tag(sc, (P.POS['right'][0], P.POS['right'][1] - 6, P.Z_CAN + 8),
        'אדום או לבן הם הפלוס', dx=24, dy=40, size=6.2)
    probes_on(sc, (mx + 5, my + 3.4, ZM + 2.2), (mx + 9, my + 36, ZM + 2.2),
              x=62, y=112, z=-24, reading='2.1 Ω', mode='beep')
    tag(sc, (mx + 25, my + 20, ZM + 2), 'צפצוף או 1–3 אוהם', dx=-16, dy=-52, size=6.2)
    safe_state(sc, CX - 27, CY + 76, P.Z_PLATE, 'בלי סוללה ובלי מדחפים')
    return 'w_p8_s06_motor_wiring', sc, 'the motors to their channels'


def t1_m7_signal_wiring():
    """Four gate wires and two sensor wires — the thin ones."""
    sc = Scene()
    bench_for_drone(sc, pad=40)
    P.frame(sc, front_mark=True)
    P.motors_all(sc, leads=False)
    P.mosfet_board(sc, z=ZM, flip=True, layer=2)
    motor_wires_to_board(sc)
    P.devkit(sc); P.mt3608(sc, locked=True); P.mpu6050(sc)
    power_tree(sc)
    gate_wires(sc)
    i2c_wires(sc)
    for which, dy in (('front', -34), ('right', -18), ('back', 24), ('left', 42)):
        px, py, pz = P.devkit_pin('right', {'back': 4, 'left': 5, 'right': 6, 'front': 7}[which])
        tag(sc, (px, py, pz), '%d → G%d' % (P.GPIO[which], P.CHANNEL[which]),
            dx=66, dy=dy, size=6.0)
    tag(sc, (P.IMU_XY[0] + 6, P.IMU_XY[1] + 1.4, ZD + 4), 'לבן 21 · אפור 22', dx=-56, dy=28, size=6.2)
    tag(sc, (CX, CY + 26, ZM + 3), 'מעבירים את חוטי השערים מתחת ללוחית', dx=-30, dy=52, size=6.2)
    safe_state(sc, CX - 27, CY - 90, P.Z_PLATE, 'מחווטים רק במצב הבטוח')
    return 'w_p8_s07_signal_wiring', sc, 'the signal wires'


def t1_m8_pre_power_check():
    """Sweep the carbon for shorts first; only then does the teacher plug the cell in."""
    sc = Scene()
    P.bench(sc, 48, 44, 176, 170)
    P.drone(sc, front_mark=True, battery=False)
    power_tree(sc); gate_wires(sc); i2c_wires(sc); motor_wires_to_board(sc)
    probes_on(sc, (P.POS['left'][0] + 4, P.POS['left'][1] + 3, P.Z_PLATE_TOP + 1),
              (P.MOSFET_XY[0] + 4, P.MOSFET_XY[1] + 3.4, ZM + 2),
              x=58, y=110, z=-24, reading='OL', mode='Ω')
    tag(sc, (P.POS['left'][0] + 4, P.POS['left'][1], P.Z_PLATE_TOP + 3),
        'חלק א׳ — סורקים בלי סוללה\nבכל נקודה המכשיר מראה OL', dx=-54, dy=-34, size=6.2)
    # part B: the cell arrives in the teacher's hand
    P.lipo(sc, x=P.BAT_XY[0] + 44, y=P.BAT_XY[1] + 4, z=ZB - 4, layer=3)
    arrow(sc, (P.BAT_XY[0] + 40, CY, ZB + 2), (P.BAT_XY[0] + 4, CY, ZB + 4), HL)
    disc(sc, P.DEVKIT_XY[0] + 40, P.DEVKIT_XY[1] + 22, ZD + P.DEVKIT_T + 0.6, 1.6, '#e03030', layer=6)
    tag(sc, (P.DEVKIT_XY[0] + 40, P.DEVKIT_XY[1] + 22, ZD + 3),
        'חלק ב׳ — החשמל הראשון, עם המורה\nהנורית נדלקת ואף מנוע לא זז', dx=76, dy=-30, size=6.2)
    return 'w_p8_s08_pre_power_check', sc, 'the pre-power check'


def t1_m9_upload_motor_test():
    """USB in means battery out. The motor-test sketch goes on over the cable."""
    sc = Scene()
    P.bench(sc, 60, 30, 300, 200)
    P.drone(sc, front_mark=True, battery=False)
    power_tree(sc); gate_wires(sc); i2c_wires(sc); motor_wires_to_board(sc)
    P.laptop(sc, 244, 44, -20)
    ux, uy, uz = P.DEVKIT_XY[0] + P.DEVKIT_W - 4, P.DEVKIT_XY[1] + 14, ZD + 3
    wire(sc, [(ux, uy, uz), (238, 70, 8), (262, 84, -12)], '#d0d4d8', 1.8, layer=5)
    tag(sc, (236, 72, 6), 'USB בפנים = סוללה בחוץ', dx=8, dy=-40, size=6.4)
    tag(sc, (300, 44, 46), 'בוחרים מהירות 115200', dx=0, dy=-30, size=6.2)
    P.lipo_bag(sc, 74, 152, -24, layer=0)
    tag(sc, (119, 183, -2), 'הסוללה בשקית', dx=-30, dy=28, size=6.2)
    tag(sc, (P.DEVKIT_XY[0] + 24, P.DEVKIT_XY[1] + 8, ZD + 4),
        'מחזיקים את כפתור ה-BOOT', dx=-60, dy=-30, size=6.2)
    return 'w_p8_s09_upload_motor_test', sc, 'upload the motor test'


def t1_m10_spin_no_props():
    """The first time the motors turn. Four bare shafts, one button at a time."""
    sc = Scene()
    P.bench(sc, 62, 26, 300, 200)
    P.drone(sc, front_mark=True)
    power_tree(sc, battery=True); gate_wires(sc); i2c_wires(sc); motor_wires_to_board(sc)
    P.coreless_motor(sc, 'front', spinning=True, leads=False)
    P.phone_flat(sc, 236, 150, -20, armed=True, throttle=0.25,
                 label='המחוון על 0 לפני ARM')
    fx, fy = P.POS['front']
    tag(sc, (fx, fy, P.Z_SHAFT + 6), 'לוחצים FRONT —\nרק הקדמי מסתובב', dx=-46, dy=-30, size=6.4)
    tag(sc, (P.POS['back'][0], P.POS['back'][1], P.Z_SHAFT + 2),
        'אין מדחף על אף מנוע', dx=52, dy=-24, size=6.2)
    tag(sc, (CX + 26, CY - 30, ZD + 4), 'כבל ה-USB מנותק', dx=48, dy=-42, size=6.2)
    return 'w_p8_s10_spin_no_props', sc, 'motors spin, no props'


def _thrust_rig(sc, spinning=True, reading='168 g'):
    """The drone clamped UPSIDE DOWN on a weighted post: the props hang below the plate and
    blow straight down at the scale pan, so what the scale reads is the thrust."""
    P.kitchen_scale(sc, CX - 60, CY - 48, -120, reading=reading)
    cuboid(sc, CX - 16, CY - 14, -111, 32, 28, 68, '#6f7b88', layer=1)     # the post
    z = -40                                                                # the bottom plate, inverted
    P.frame(sc, z=z, top_plate=False, front_mark=True)
    for which in P.ORDER:
        rx, ry = P.POS[which]
        cw = P.SPIN[which] == 'cw'
        col = P.C_PROP_CW if cw else P.C_PROP_CCW
        cyl_z(sc, rx, ry, z + P.PLATE_T, P.MOTOR_H, P.MOTOR_R, P.C_CAN,
              cap_col=P.C_BELL, layer=3)                                   # can now points up
        cyl_z(sc, rx, ry, z - 5.0, 5.0, P.SHAFT_R, '#9aa0a6', layer=2)     # shaft points down
        cyl_z(sc, rx, ry, z - 8.2, 3.2, P.PROP_HUB, '#1f2329', layer=2, hole=0.6)
        if spinning:
            disc(sc, rx, ry, z - 9.4, P.PROP_R, '#8d99a8', extra='fill-opacity:0.13',
                 layer=2, bump=0.6)
            disc(sc, rx, ry, z - 9.4, P.PROP_R, 'none', stroke=col, sw=0.8, layer=2, bump=0.7)
            spin_arc(sc, rx, ry, z - 12, P.PROP_R + 5, cw=cw)
        else:
            for a in (0, 180):
                blade(sc, rx, ry, z - 9.4, a + (18 if cw else -18), P.PROP_HUB, P.PROP_R,
                      col, cw=cw, layer=2)
    # inverted, everything that hung underneath now sits on top
    P.mosfet_board(sc, z=z + P.PLATE_T + 1.0, flip=True, layer=4)
    P.lipo(sc, z=z + P.PLATE_T + 3.6, layer=4)
    for ox in (CX - 15, CX + 15):                                          # the two rubber bands
        cuboid(sc, ox - 1.2, CY - 20, z - 0.5, 2.4, 40, 1.8, '#7a4a3c', layer=5)
        for sy in (CY - 20, CY + 18):
            cuboid(sc, ox - 1.2, sy, z - 0.5, 2.4, 2.0, 14.0, '#7a4a3c', layer=5)
    return z


def t1_m11_thrust_test():
    """Props on for the first time — pointing at a scale pan, not at the room."""
    sc = Scene()
    P.floor(sc, z=-124, x0=CX - 150, y0=CY - 118, w=300, d=236)
    z = _thrust_rig(sc)
    tag(sc, (CX - 46, CY - 40, z - 9), 'מדחפים כלפי צלחת המאזניים', dx=-46, dy=16, size=6.6)
    tag(sc, (CX + 15, CY + 16, z + 12), 'שתי גומיות על הצלחות המרכזיות', dx=64, dy=-26, size=6.2)
    tag(sc, (CX - 58, CY + 14, -111), 'מאפסים את המאזניים ל-0', dx=-58, dy=30, size=6.2)
    P.tape_line(sc, CX + 108, CY - 110, CY + 110, -122)
    tag(sc, (CX + 110, CY + 70, -122), 'הידיים מאחורי קו הסרט', dx=44, dy=22, size=6.2)
    return 'w_p8_s11_thrust_test', sc, 'the thrust test'


def t1_m12_upload_flight():
    """The gyro check: push one arm down with a pencil and watch that motor's number fall."""
    sc = Scene()
    P.bench(sc, 58, 26, 300, 200)
    P.drone(sc, front_mark=True)
    power_tree(sc, battery=True); gate_wires(sc); i2c_wires(sc); motor_wires_to_board(sc)
    fx, fy = P.POS['front']
    cyl_x(sc, fx - 40, fy - 26, P.Z_PLATE_TOP + 30, 46, 2.6, '#e0b400', layer=6)   # the pencil
    arrow(sc, (fx - 2, fy - 8, P.Z_PLATE_TOP + 22), (fx - 2, fy - 4, P.Z_PLATE_TOP + 3), HL)
    tag(sc, (fx - 4, fy - 10, P.Z_PLATE_TOP + 26), 'דוחפים בעיפרון ולא באצבע', dx=-50, dy=-26, size=6.4)
    P.phone_flat(sc, 232, 152, -20, armed=True, throttle=0.3,
                 label='המחוון על 30% והרחפן חמוש')
    tag(sc, (CX + 20, CY + 30, ZD + 4), 'המספר של המנוע הנדחף יורד', dx=64, dy=26, size=6.2)
    tag(sc, (P.POS['back'][0], P.POS['back'][1], P.Z_SHAFT + 2),
        'אין מדחף על אף מנוע', dx=48, dy=-26, size=6.2)
    return 'w_p8_s12_upload_flight', sc, 'upload the flight code'


def _flight_scene(sc, hover=32, spinning=True, spectator=True):
    """The tethered flight set-up: taped circle, anchor, line, drone in the air.
    The 3 m circle is symbolic — at true scale the drone would be a speck inside it."""
    P.floor(sc, z=-120, x0=CX - 118, y0=CY - 96, w=250, d=200)
    disc(sc, CX, CY, -118, 84, 'none', stroke='#c9c3b6', sw=1.6, layer=0)
    P.anchor_weight(sc, CX - 22, CY - 18, -118)
    z = -118 + hover + 18
    P.drone(sc, z=z, props=True, spinning=spinning, front_mark=True, tether_loop=True)
    P.tether(sc, CX, CY, z - 11, CX, CY - 4, -114)
    P.tape_line(sc, CX + 96, CY - 92, CY + 96, -119)
    if spectator:
        P.goggles(sc, CX + 108, CY + 34, -118)
    return z


def t1_m13_tethered_hover():
    """Ten to thirty centimetres, on a line that stays slack."""
    sc = Scene()
    z = _flight_scene(sc)
    P.phone_flat(sc, CX + 102, CY - 84, -118, armed=True, throttle=0.45)
    tag(sc, (CX, CY, z + P.Z_PROP), 'מעלים את המחוון לאט', dx=-70, dy=-46, size=6.6)
    tag(sc, (CX + 30, CY, z - 30), 'מחזיקים בגובה 10–30 ס״מ', dx=70, dy=-16, size=6.4)
    tag(sc, (CX, CY - 2, -112), 'החוט נשאר רפוי', dx=-64, dy=26, size=6.2)
    tag(sc, (CX + 98, CY + 54, -119), 'טלפון המורה — DISARM בלבד', dx=40, dy=26, size=6.2)
    return 'w_p8_s13_tethered_hover', sc, 'the tethered hover'


def t1_m14_post_flight():
    """The shutdown ritual, in the one order that is always safe."""
    sc = Scene()
    P.bench(sc, 56, 24, 306, 206)
    P.drone(sc, front_mark=True, battery=False)
    power_tree(sc); gate_wires(sc); i2c_wires(sc); motor_wires_to_board(sc)
    for i, which in enumerate(P.ORDER):
        rx, ry = P.POS[which]
        arrow(sc, (rx, ry, P.Z_SHAFT + 4), (rx, ry, P.Z_SHAFT + 26), HL)
    cuboid(sc, 244, 40, -24, 96, 74, 14, '#c8b28a', layer=0)                 # the teacher's prop box
    for i, (px, py) in enumerate(((266, 58), (312, 58), (266, 92), (312, 92))):
        loose_prop(sc, px, py, -9.6, cw=(i < 2), layer=3)
    tag(sc, (292, 46, -8), 'מורידים את ארבעת המדחפים', dx=42, dy=-32, size=6.4)
    P.phone_flat(sc, 62, 164, -20, layer=3)
    tag(sc, (139, 166, -12), 'הטלפון יורד מהיד', dx=-24, dy=32, size=6.2)
    P.lipo(sc, x=250, y=150, z=-19.6, layer=3)
    P.lipo_bag(sc, 250, 152, -24, layer=0)
    tag(sc, (295, 183, -2), 'הסוללה נכנסת לשקית חסינת האש', dx=36, dy=30, size=6.2)
    tag(sc, (P.POS['left'][0], P.POS['left'][1], P.Z_CAN + 10),
        'בגב האצבע בודקים אם חם', dx=-56, dy=-24, size=6.2)
    return 'w_p8_s14_post_flight', sc, 'the shutdown ritual'


# ================================================================ TRACK 2
def t2_m1_startup():
    """Same press-fit as Track 1, plus the four identical piles the channels get built from."""
    sc = Scene()
    P.bench(sc, 56, 24, 306, 200)
    P.frame(sc, front_mark=True)
    for which in ('left', 'right', 'back'):
        P.coreless_motor(sc, which, leads=True)
    P.coreless_motor(sc, 'front', leads=False, foot=False, lift=26)
    fx, fy = P.POS['front']
    P.hand_thumb(sc, fx, fy, P.Z_CAN + 26 + P.MOTOR_H + 2)
    tag(sc, (fx, fy - 10, P.Z_CAN + 36), 'המנועים נכנסים בלחיצת אגודל בלבד',
        dx=-38, dy=-24, size=6.4)
    tag(sc, (P.POS['back'][0] - 6, CY + 4, P.Z_CAN + 8), 'אדום/כחול — FRONT ו-BACK', dx=54, dy=10, size=6.0)
    tag(sc, (CX + 4, P.POS['right'][1] - 8, P.Z_CAN + 8), 'שחור/לבן — RIGHT ו-LEFT', dx=14, dy=40, size=6.0)
    # four identical piles, one per channel
    for c in range(4):
        px, py = 246 + (c % 2) * 56, 46 + (c // 2) * 60
        cuboid(sc, px, py, -20, 48, 50, 0.8, '#efe9dc', layer=0)
        P.to220(sc, px + 6, py + 30, -19.2, flat=False, layer=3)
        cuboid(sc, px + 26, py + 30, -19.2, 2.2, 7.0, 2.2, '#c8b28a', layer=3)
        cuboid(sc, px + 32, py + 30, -19.2, 2.2, 7.0, 2.2, '#8fa2c9', layer=3)
        cyl_y(sc, px + 30, py + 12, -18.0, 7.4, 1.3, '#3a3f46', layer=3)
        tag(sc, (px + 24, py + 25, -19), 'M%d' % (c + 1), dx=0, dy=-38 if c < 2 else 40, size=6.0)
    tag(sc, (302, 106, -19), 'ארבע ערימות זהות — אחת לכל ערוץ', dx=6, dy=64, size=6.4)
    return 'w_p8_t2_s01_startup', sc, 'motors in, four piles ready'


def t2_m2_solder_channel_1():
    """Channel one, joint by joint, with the teacher alongside."""
    sc = Scene()
    P.bench(sc, 84, 58, 140, 96)
    P.mat(sc, 90, 64, 126, 84, z=-19.4)
    P.mosfet_board(sc, x=96, y=72, z=-18.0, channels=1, cap=False, pads=True)
    zt = -18.0 + P.MOSFET_T
    P.soldering_iron(sc, (96 + 10, 72 + 10, zt))
    P.goggles(sc, 98, 146, -19.4)
    tag(sc, (96 + 10, 72 + 8, zt + 3), 'הטבעת פונה אל BAT+', dx=-64, dy=22, size=6.4)
    tag(sc, (96 + 5, 72 + 26, zt + 6), 'הכיתוב פונה לצד פד G1', dx=-56, dy=-34, size=6.2)
    tag(sc, (96 + 42, 72 + 3.4, zt + 2), 'מלחימים בכל חור שלישי', dx=54, dy=-30, size=6.2)
    tag(sc, (96 + 26, 72 + 34, zt + 3), 'לא יותר מ-3 שניות על כל רגל', dx=42, dy=44, size=6.2)
    return 'w_p8_t2_s02_solder_channel_1', sc, 'solder channel 1'


def t2_m3_check_channel_1():
    """Three dial positions prove the channel before three more get built."""
    sc = Scene()
    P.bench(sc, 80, 56, 158, 108)
    P.mosfet_board(sc, x=92, y=70, z=-19.4, channels=1, cap=False, pads=True)
    zt = -19.4 + P.MOSFET_T
    probes_on(sc, (92 + 6, 70 + 36, zt + 1.4), (92 + 4, 70 + 3.4, zt + 1.4),
              x=176, y=90, z=-24, reading='0.28 V', mode='diode')
    tag(sc, (92 + 5, 70 + 20, zt + 4), 'מחוש אדום על −M1 ושחור על BAT+', dx=-56, dy=-30, size=6.2)
    tag(sc, (92 + 30, 70 + 20, zt + 3), 'מחליפים בין המחושים — OL', dx=44, dy=50, size=6.2)
    tag(sc, (92 + 42, 70 + 3.4, zt + 2), 'אין צפצוף בין BAT+ ל-GND', dx=52, dy=-34, size=6.2)
    return 'w_p8_t2_s03_check_channel_1', sc, 'check channel 1'


def t2_m4_solder_channels_2_4():
    """Three more of the same, then the one capacitor that serves the whole board."""
    sc = Scene()
    P.bench(sc, 84, 58, 140, 96)
    P.mat(sc, 90, 64, 126, 84, z=-19.4)
    P.mosfet_board(sc, x=96, y=72, z=-18.0, pads=True)
    zt = -18.0 + P.MOSFET_T
    P.soldering_iron(sc, (96 + 28, 72 + 24, zt))
    tag(sc, (96 + 3, 72 + 24, zt + 6), 'ערוץ 1 כבר מוכן', dx=-58, dy=-14, size=6.2)
    tag(sc, (96 + 20, 72 + 22, zt + 6), 'לפחות שני חורים ריקים\nבין מוספט למוספט',
        dx=-24, dy=-46, size=6.2)
    tag(sc, (96 + 43.5, 72 + 12, zt + 11), 'הרגל הארוכה אל פס BAT+', dx=54, dy=-32, size=6.2)
    tag(sc, (96 + 26, 72 + 34, zt + 5), 'שרוול מתכווץ על ארבע הלשוניות', dx=40, dy=46, size=6.2)
    return 'w_p8_t2_s04_solder_channels_2_4', sc, 'solder channels 2-4'


def t2_m5_tune_mt3608():
    """The booster is tuned alone on the bench, long before the ESP32 is anywhere near it."""
    sc = Scene()
    P.bench(sc, 92, 66, 132, 92)
    P.mt3608(sc, x=118, y=94, z=-19.4, layer=3)
    zt = -19.4 + P.MT_T
    probes_on(sc, (126 + 34, 96 + 5, zt + 1), (126 + 34, 96 + 12, zt + 1),
              x=182, y=76, z=-24, reading='5.00 V', mode='DC V')
    # the trimmer screwdriver
    cyl_z(sc, 126 + 25, 96 + 8.5, zt + 5, 30, 1.4, '#c9ced4', layer=6)
    cuboid(sc, 126 + 19, 96 + 2, zt + 35, 12, 13, 26, '#c0392b', layer=6)
    spin_arc(sc, 126 + 25, 96 + 8.5, zt + 8, 12, cw=True)
    tag(sc, (126 + 25, 96 + 8.5, zt + 34), 'מסובבים שלושה סיבובים לכיוון אחד',
        dx=-30, dy=-26, size=6.4)
    tag(sc, (126 + 34, 96 + 8, zt + 2), 'המחוש האדום על +OUT והשחור על −OUT',
        dx=44, dy=-42, size=6.2)
    P.devkit(sc, x=96, y=166, z=-19.4, layer=3)
    tag(sc, (122, 180, -18), 'ה-ESP32 לא מחובר בשלב הזה', dx=-30, dy=32, size=6.2)
    return 'w_p8_t2_s05_tune_mt3608', sc, 'tune the MT3608 to 5.0 V'


def t2_m6_mount_and_wire():
    """Everything mounted and every wire run — the whole machine in one picture."""
    sc = Scene()
    bench_for_drone(sc, pad=44)
    P.frame(sc, front_mark=True, tether_loop=True)
    P.motors_all(sc, leads=False)
    P.mosfet_board(sc, z=ZM, flip=True, layer=2)
    motor_wires_to_board(sc)
    P.devkit(sc, pad=True); P.mt3608(sc, pad=True, locked=True); P.mpu6050(sc, pad=True)
    power_tree(sc); gate_wires(sc); i2c_wires(sc)
    tag(sc, (P.IMU_XY[0] + 3, P.IMU_XY[1] + 12, ZD + 3), 'החץ X מצביע על המנוע הקדמי',
        dx=-58, dy=30, size=6.2)
    tag(sc, (P.MOSFET_XY[0] + 8, P.MOSFET_XY[1] + 3, ZM + 2), 'רפידה M1 קרובה לזרוע הקדמית',
        dx=-58, dy=42, size=6.2)
    px, py, pz = P.devkit_pin('left', 0)
    tag(sc, (px, py, pz), '3V3 — לא VIN ולא 5V', dx=-64, dy=-24, size=6.2)
    tag(sc, (CX + 20, CY - 24, ZD + 2), 'שום מתכת לא נוגעת בפחמן', dx=66, dy=-30, size=6.2)
    safe_state(sc, CX - 27, CY + 82, P.Z_PLATE, 'תא הסוללה עדיין ריק')
    return 'w_p8_t2_s06_mount_and_wire', sc, 'mount and wire the whole drone'


def t2_m7_pre_power_check():
    """Proving it is safe, then the teacher connects the cell and the meter confirms 5 V."""
    sc = Scene()
    bench_for_drone(sc, pad=52)
    P.drone(sc, front_mark=True)
    power_tree(sc, battery=True); gate_wires(sc); i2c_wires(sc); motor_wires_to_board(sc)
    a = P.devkit_pin('right', 0)
    b = P.devkit_pin('right', 1)
    probes_on(sc, a, b, x=CX - 116, y=CY - 40, z=-24, reading='4.98 V', mode='DC V')
    tag(sc, (a[0], a[1], a[2]), 'מודדים VIN ↔ GND: 4.9–5.1V', dx=64, dy=-34, size=6.2)
    disc(sc, P.DEVKIT_XY[0] + 40, P.DEVKIT_XY[1] + 22, ZD + P.DEVKIT_T + 0.6, 1.6, '#e03030', layer=6)
    tag(sc, (P.POS['left'][0] + 4, P.POS['left'][1], P.Z_PLATE_TOP + 3),
        'סורקים את לוח הפחמן: OL בכל נקודה', dx=-48, dy=-30, size=6.2)
    tag(sc, (P.BAT_XY[0] - 4, CY, ZB + 5), 'המורה מחבר את הסוללה', dx=-58, dy=34, size=6.2)
    tag(sc, (P.POS['back'][0], P.POS['back'][1], P.Z_SHAFT + 2),
        'אין מדחפים וכבל USB לא מחובר', dx=54, dy=-22, size=6.2)
    return 'w_p8_t2_s07_pre_power_check', sc, 'prove it is safe, then power up'


def t2_m8_upload_and_spin():
    """Cable out, cell in, one motor at a time."""
    sc = Scene()
    P.bench(sc, 58, 24, 306, 206)
    P.drone(sc, front_mark=True)
    power_tree(sc, battery=True); gate_wires(sc); i2c_wires(sc); motor_wires_to_board(sc)
    P.coreless_motor(sc, 'front', spinning=True, leads=False)
    P.laptop(sc, 246, 40, -20, screen='#1b2430')
    wire(sc, [(262, 128, -18), (286, 116, -18)], '#d0d4d8', 1.8, layer=5)   # the unplugged cable
    tag(sc, (274, 122, -18), 'מנתקים את כבל ה-USB', dx=26, dy=34, size=6.2)
    P.phone_flat(sc, 60, 160, -20, armed=True, throttle=0.2, label='המחוון על 0 ולוחצים ARM')
    fx, fy = P.POS['front']
    tag(sc, (fx, fy, P.Z_SHAFT + 6), 'לוחצים FRONT:\nרק הקדמי מסתובב', dx=-44, dy=-28, size=6.4)
    tag(sc, (P.POS['back'][0], P.POS['back'][1], P.Z_SHAFT + 2),
        'אין מדחף על אף מנוע', dx=46, dy=-26, size=6.2)
    return 'w_p8_t2_s08_upload_and_spin', sc, 'upload and spin'


def t2_m9_thrust_test():
    """The same rig as Track 1 — this time the numbers decide what to change."""
    sc = Scene()
    P.floor(sc, z=-124, x0=CX - 150, y0=CY - 118, w=300, d=236)
    z = _thrust_rig(sc)
    tag(sc, (CX - 46, CY - 40, z - 9), 'הרחפן הפוך על ראש העמוד', dx=-48, dy=14, size=6.6)
    tag(sc, (CX + 14, CY, z), 'שתי גומיות על הצלחות המרכזיות', dx=64, dy=-8, size=6.2)
    P.tether(sc, CX + 20, CY + 14, z + 2, CX - 26, CY - 8, -108)
    tag(sc, (CX - 20, CY - 6, -106), 'חוט גיבוי של 30 ס״מ — רפוי', dx=-52, dy=26, size=6.2)
    P.tape_line(sc, CX + 108, CY - 110, CY + 110, -122)
    tag(sc, (CX + 110, CY + 70, -122), 'הידיים מאחורי קו הסרט', dx=44, dy=22, size=6.2)
    return 'w_p8_t2_s09_thrust_test', sc, 'measure thrust, decide by numbers'


def t2_m10_choices_and_claude():
    """The safe state first, then the starter sketch's marked blocks."""
    sc = Scene()
    P.bench(sc, 58, 26, 300, 200)
    P.drone(sc, front_mark=True, battery=False)
    power_tree(sc); gate_wires(sc); i2c_wires(sc); motor_wires_to_board(sc)
    for which in P.ORDER:
        rx, ry = P.POS[which]
        disc(sc, rx, ry, P.Z_SHAFT + 5.6, 5.0, 'none', stroke=HL, sw=1.0, layer=6, bump=200)
    arrow(sc, (P.POS['left'][0] - 8, P.POS['left'][1] - 4, P.Z_SHAFT + 8),
          (P.POS['right'][0] + 8, P.POS['right'][1] + 4, P.Z_SHAFT + 8), HL, curve=-12)
    tag(sc, (CX, CY - 40, P.Z_SHAFT + 10), 'עוברים באצבע על ארבעת המנועים', dx=-44, dy=-36, size=6.4)
    P.laptop(sc, 240, 44, -20)
    ux, uy, uz = P.DEVKIT_XY[0] + P.DEVKIT_W - 4, P.DEVKIT_XY[1] + 14, ZD + 3
    wire(sc, [(ux, uy, uz), (234, 72, 6), (258, 84, -12)], '#d0d4d8', 1.8, layer=5)
    tag(sc, (296, 44, 46), 'משנים רק בתוך הבלוקים המסומנים', dx=0, dy=-30, size=6.2)
    P.lipo_bag(sc, 70, 156, -24, layer=0)
    tag(sc, (115, 187, -2), 'הסוללה מנותקת ונמצאת אצל המורה', dx=-24, dy=30, size=6.2)
    return 'w_p8_t2_s10_choices_and_claude', sc, 'the choices that make it yours'


def t2_m11_tethered_hover_tuning():
    """Hover, land, change exactly one constant, fly again."""
    sc = Scene()
    z = _flight_scene(sc)
    P.phone_flat(sc, CX + 102, CY - 84, -118, armed=True, throttle=0.4)
    tag(sc, (CX, CY, z + P.Z_PROP), 'מחוון על 0, לוחצים ARM ומעלים לאט', dx=-58, dy=-48, size=6.4)
    tag(sc, (CX + 30, CY, z - 30), 'מרחפים 10–30 ס״מ', dx=68, dy=-14, size=6.4)
    tag(sc, (CX, CY - 2, -112), 'החוט שוכב רפוי על הרצפה', dx=-62, dy=26, size=6.2)
    P.card(sc, CX - 112, CY + 54, -118, w=56, d=38, lines=3)
    tag(sc, (CX - 84, CY + 73, -117), 'משנים קבוע אחד\nוטסים טיסה אחת', dx=-30, dy=28, size=6.2)
    return 'w_p8_t2_s11_tethered_hover_tuning', sc, 'hover and the tuning loop'


def t2_m12_flight_sequence():
    """Announce the sequence, read R4 aloud, then fly it."""
    sc = Scene()
    P.floor(sc, z=-120, x0=CX - 124, y0=CY - 100, w=262, d=208)
    disc(sc, CX, CY, -118, 88, 'none', stroke='#c9c3b6', sw=1.6, layer=0)
    P.anchor_weight(sc, CX - 22, CY - 18, -118)
    for i, (mx, my, lab) in enumerate(((CX - 50, CY + 44, 'א׳'), (CX, CY + 60, 'ב׳'),
                                       (CX + 50, CY + 44, 'ג׳'))):
        disc(sc, mx, my, -117.6, 9, '#efe4c8', stroke='#c9b98a', sw=0.8, layer=0, bump=40)
        tag(sc, (mx, my, -117), lab, dy=-16, size=6.4)
    z = -118 + 30 + 18
    P.drone(sc, z=z, props=True, spinning=True, front_mark=True, tether_loop=True)
    P.tether(sc, CX, CY, z - 11, CX, CY - 4, -114)
    P.tape_line(sc, CX + 100, CY - 96, CY + 100, -119)
    P.card(sc, CX + 110, CY - 30, -118, w=54, d=40, lines=5)
    tag(sc, (CX + 137, CY - 10, -117), 'קוראים בקול\nאת רשימת R4', dx=38, dy=-18, size=6.2)
    tag(sc, (CX, CY, z + P.Z_PROP), 'בוחרים רצף ומכריזים עליו למורה', dx=-56, dy=-48, size=6.4)
    tag(sc, (CX + 30, CY, z - 30), 'הגובה נשאר 10–30 ס״מ', dx=66, dy=-12, size=6.2)
    return 'w_p8_t2_s12_flight_sequence', sc, 'choose a sequence and fly it'


def t2_m13_signature_flight():
    """The flight the whole project was for — once, on the line, with a witness."""
    sc = Scene()
    z = _flight_scene(sc, hover=42)
    P.phone_flat(sc, CX + 102, CY - 86, -118, armed=True, throttle=0.5)
    P.goggles(sc, CX + 112, CY + 38, -118)
    tag(sc, (CX + 124, CY + 46, -117), 'הצופה נשאר מאחורי קו הצופים', dx=40, dy=26, size=6.2)
    tag(sc, (CX, CY, z + P.Z_PROP), 'מטיסים את הרצף שבחרתם פעם אחת', dx=-56, dy=-50, size=6.6)
    tag(sc, (CX, CY - 2, -112), 'החוט קשור בלולאה ובעוגן השטוח', dx=-60, dy=26, size=6.2)
    P.lipo_bag(sc, CX - 116, CY + 60, -120, layer=0)
    tag(sc, (CX - 71, CY + 91, -98), 'הסוללה יוצאת ואז המדחפים יורדים', dx=-14, dy=34, size=6.2)
    return 'w_p8_t2_s13_signature_flight', sc, 'the signature flight'


# ================================================================ TRACK 3
def t3_planner():
    """Adding one module: free pins only, cell out, props off, then weigh it again."""
    sc = Scene()
    P.bench(sc, 56, 26, 306, 200)
    P.drone(sc, front_mark=True, battery=False)
    power_tree(sc); gate_wires(sc); i2c_wires(sc); motor_wires_to_board(sc)
    # the new module joins the existing I2C line
    nx, ny = P.IMU_XY[0] + 26, P.IMU_XY[1] + 6
    cuboid(sc, nx, ny, ZD + 16, 16, 12, 1.2, '#7a4ea8', layer=5)
    arrow(sc, (nx + 8, ny + 6, ZD + 14), (nx + 8, ny + 6, ZD + 3), HL)
    for i, col in enumerate((WHITE_W, GREY_W)):
        wire(sc, [(P.IMU_XY[0] + 4 + i * 2.6, P.IMU_XY[1] + 1.4, ZD + P.IMU_T + 2),
                  (nx + 2 + i * 3, ny + 2, ZD + 16 + 1.5)], col, 0.7, layer=6)
    tag(sc, (nx + 8, ny + 6, ZD + 20), 'משתמשים רק בפינים הפנויים\n33 · 32 · 4 · 16 · 17',
        dx=54, dy=-26, size=6.2)
    P.kitchen_scale(sc, 240, 44, -20, reading='104 g')
    tag(sc, (300, 130, -11), 'שוקלים את הרחפן שוב במאזניים', dx=34, dy=-30, size=6.4)
    tag(sc, (300, 118, -11), 'יותר מ-3 גרם — חוזרים על מבחן הדחף', dx=30, dy=34, size=6.2)
    cuboid(sc, 66, 154, -24, 82, 62, 12, '#c8b28a', layer=0)                 # the prop box
    for i, (px, py) in enumerate(((84, 168), (124, 168), (84, 196), (124, 196))):
        loose_prop(sc, px, py, -11.6, cw=(i < 2), layer=3)
    tag(sc, (104, 160, -10), 'הסוללה בחוץ, המדחפים למטה', dx=-30, dy=-30, size=6.2)
    return 'w_p8_t3_planner', sc, 'plan your own extension'


SCENES = [
    t1_m1_parts_contract, t1_m2_press_fit_motors, t1_m3_meet_mosfet_board, t1_m4_mount_electronics,
    t1_m5_power_tree, t1_m6_motor_wiring, t1_m7_signal_wiring, t1_m8_pre_power_check,
    t1_m9_upload_motor_test, t1_m10_spin_no_props, t1_m11_thrust_test, t1_m12_upload_flight,
    t1_m13_tethered_hover, t1_m14_post_flight,
    t2_m1_startup, t2_m2_solder_channel_1, t2_m3_check_channel_1, t2_m4_solder_channels_2_4,
    t2_m5_tune_mt3608, t2_m6_mount_and_wire, t2_m7_pre_power_check, t2_m8_upload_and_spin,
    t2_m9_thrust_test, t2_m10_choices_and_claude, t2_m11_tethered_hover_tuning,
    t2_m12_flight_sequence, t2_m13_signature_flight,
    t3_planner,
]
