"""scenes_p5.py — Project 5 (Wi-Fi remote-controlled car): the same car, a new brain.

Run: python build.py 5
"""
from iso import Scene, iso, depth, cuboid, cyl_x, cyl_y, plate, wire, arrow, tag, poly, shade
import parts as P
from scenes_p4 import floor, bench, car_on

RED, BLACK, ORANGE, GREEN, BLUE = P.RED, P.BLACK, P.ORANGE, P.GREEN, P.BLUE
HL = '#e0651a'
ZT = P.PLATE_T


def wifi_arc(sc, x, y, z, n=3, col='#2f8fd0', flip=False):
    """Three widening arcs = 'this thing is talking over Wi-Fi'."""
    cx, cy = iso(x, y, z)
    for i in range(n):
        r = 9 + i * 7
        sweep = 1 if not flip else 0
        sc.over('<path d="M %.2f %.2f a %.1f %.1f 0 0 %d %.2f %.2f" style="fill:none;stroke:%s;'
                'stroke-width:1.5;stroke-linecap:round;stroke-opacity:%.2f"/>'
                % (cx - r * 0.55, cy - r * 0.42, r, r, sweep, r * 1.1, r * 0.84, col, 0.85 - i * 0.18))


# ---------------------------------------------------------------- M1 — meet the ESP32
def m1_meet_esp32():
    sc = Scene()
    bench(sc, 40, 40, 220, 150)
    x, y, z = 96, 96, -10
    cuboid(sc, x, y, z, 51.5, 28.3, 1.4, P.C_ESP, layer=3)
    cuboid(sc, x + 2, y + 9, z + 1.4, 8, 10, 4.2, '#b9bec6', layer=3)          # micro-USB
    cuboid(sc, x + 17, y + 5, z + 1.4, 18, 18, 2.6, '#3a3f46', layer=3)        # shield
    for i in range(15):                                                        # gold pins
        cuboid(sc, x + 6 + i * 2.9, y + 0.6, z + 1.4, 1.6, 2.2, 2.2, '#c9a227', layer=3)
        cuboid(sc, x + 6 + i * 2.9, y + 26.1, z + 1.4, 1.6, 2.2, 2.2, '#c9a227', layer=3)
    # the six-in-a-row highlight
    hx0 = x + 6 + 6 * 2.9
    pts = [iso(hx0 - 1.6, y - 1.6, z + 4.2), iso(hx0 + 6 * 2.9, y - 1.6, z + 4.2),
           iso(hx0 + 6 * 2.9, y + 4.4, z + 4.2), iso(hx0 - 1.6, y + 4.4, z + 4.2)]
    sc.over(poly(pts, 'none', '#25a05a', 1.2))
    tag(sc, (hx0 + 8, y + 1, z + 5), 'שישה חיבורים בשורה\n32 · 33 · 25 · 26 · 27 · 14', dy=-28, size=6.4)
    tag(sc, (x + 6, y + 14, z + 6), 'שקע USB\nפונה קדימה', dx=-56, dy=8, size=6.2)
    wifi_arc(sc, x + 26, y + 14, z + 8)
    return 'w_p5_s01_meet_esp32', sc, 'meet the ESP32'


# ---------------------------------------------------------------- M2 — swap the brain
def m2_swap_brain():
    sc = Scene()
    P.chassis(sc); P.motors_all(sc, leads=False); P.wheels_all(sc)
    P.l298n(sc, label=False); P.battery_box(sc, label=False)
    # velcro patch left behind on the brain zone
    cuboid(sc, P.BRAIN_X + 6, P.BRAIN_Y + 8, ZT, 54, 40, 0.8, '#4a5560', layer=3)
    # the Uno lifted off, up and to the back-right
    P.arduino_uno(sc, z=96, label=False, dy=-92, layer=5)
    ux, uy, uz = P.BRAIN_X + 2, P.BRAIN_Y + 3 - 92, ZT + 96
    tag(sc, (ux + 68, uy + 46, uz + 2), 'ה-Uno יורד\nמהמכונית', dx=74, dy=6, size=6.6)
    arrow(sc, (P.BRAIN_X + 62, P.BRAIN_Y + 4, ZT + 12), (ux + 62, uy + 30, uz - 6), HL, curve=-22)
    # the ESP32 coming down onto the same velcro
    P.esp32_devkit(sc, z=38, label=False, dx=-4, layer=5)
    ex, ey, ez = P.BRAIN_X + 5, P.BRAIN_Y + 13, ZT + 38
    tag(sc, (ex + 4, ey + 28, ez), 'ה-ESP32 עולה\nעל אותו סקוץ׳', dx=-84, dy=6, size=6.6)
    arrow(sc, (ex + 26, ey + 14, ez - 5), (ex + 30, ey + 14, ZT + 5), HL)
    tag(sc, (60, 168, ZT), 'אותה מכונית — מוח חדש', dx=-30, dy=40, size=7.2)
    return 'w_p5_s02_swap_brain', sc, 'swap the brain'


# ---------------------------------------------------------------- M3 — rewire to the ESP32
def m3_rewire():
    sc = Scene()
    P.chassis(sc); P.motors_all(sc, leads=False); P.wheels_all(sc)
    P.esp32_devkit(sc, label=False); P.l298n(sc, label=False); P.battery_box(sc, label=False)
    ex, ey = P.BRAIN_X + 9, P.BRAIN_Y + 13
    # six signal wires, driver header -> the six-in-a-row
    for i in range(6):
        col = GREEN if i in (0, 5) else ORANGE
        yy = 74 - i * 1.7
        wire(sc, [(P.DRV_X + 12 + i * 2.6, P.DRV_Y + 2, ZT + 4), (P.DRV_X + 12 + i * 2.6, yy, ZT + 6),
                  (ex + 8 + i * 2.9, yy, ZT + 6), (ex + 8 + i * 2.9, ey + 0.6, ZT + 4)], col, 1.0)
    # the power pair: L298N 5V -> VIN, GND -> GND
    wire(sc, [(P.DRV_X + 30, P.DRV_Y + P.DRV_D, ZT + 6), (P.DRV_X + 30, 150, ZT + 9),
              (ex + 44, 150, ZT + 9), (ex + 44, ey + 27, ZT + 4)], RED, 1.8)
    wire(sc, [(P.DRV_X + 36, P.DRV_Y + P.DRV_D, ZT + 6), (P.DRV_X + 36, 156, ZT + 9),
              (ex + 38, 156, ZT + 9), (ex + 38, ey + 27, ZT + 4)], BLACK, 1.8)
    tag(sc, (ex + 20, 74, ZT + 6), 'שישה חוטים בשורה —\nאותו סדר בשני הקצוות', dy=-30, size=6.4)
    tag(sc, (ex + 41, 152, ZT + 9), '5V אל VIN\nו-GND אל GND', dx=-4, dy=32, size=6.2)
    tag(sc, (P.SENS_L[0] + 20, 110, -6), 'חיישני הקו נשארים\nמוברגים ולא מחוברים', dx=-56, dy=24, size=6.0)
    return 'w_p5_s03_rewire', sc, 'rewire to the ESP32'


# ---------------------------------------------------------------- M4 — upload over USB
def m4_upload():
    sc = Scene()
    car_on(sc, 0, brain='esp', sensors=False)
    # laptop at the side of the bench
    P.laptop(sc, 300, 40, -12)
    ex, ey = P.BRAIN_X + 9, P.BRAIN_Y + 13
    wire(sc, [(ex + 2, ey + 14, ZT + 4), (180, 40, ZT + 22), (280, 60, 6), (312, 84, -6)], '#d0d4d8', 2.2)
    tag(sc, (250, 50, 14), 'כבל USB — רק להעלאה', dy=-26, size=6.4)
    tag(sc, (P.BAT_X + 55, P.BAT_Y + 30, ZT + 28), 'המתג כבוי\nוהגלגלים באוויר', dy=-26, size=6.4)
    return 'w_p5_s04_upload', sc, 'upload over USB'


# ---------------------------------------------------------------- M5 — the phone joins
def m5_connect_phone():
    sc = Scene()
    car_on(sc, 0, brain='esp', sensors=False)
    ex, ey = P.BRAIN_X + 9, P.BRAIN_Y + 13
    wifi_arc(sc, ex + 26, ey + 14, ZT + 14)
    # the phone, lying screen-up beside the car
    P.phone_flat(sc, 296, 66, -12, label='CAR-01\n192.168.4.1')
    tag(sc, (ex + 26, ey + 14, ZT + 34), 'המכונית פותחת\nרשת Wi-Fi משלה', dx=-58, dy=-18, size=6.2)
    return 'w_p5_s05_connect_phone', sc, 'the phone joins'


# ---------------------------------------------------------------- M6 — first drive
def m6_first_drive():
    sc = Scene()
    floor(sc, -60)
    car_on(sc, -46, brain='esp', sensors=False)
    P.phone_flat(sc, 300, 150, -56, label='לוחצים ומחזיקים —\nמשחררים והיא עוצרת')
    wifi_arc(sc, P.BRAIN_X + 35, P.BRAIN_Y + 27, -46 + ZT + 14)
    arrow(sc, (P.PLATE_X0 - 8, 110, -54), (P.PLATE_X0 - 92, 110, -54), HL, w=3.0, head=7)
    tag(sc, (P.PLATE_X0 - 46, 110, -56), 'קדימה', dy=-18, size=6.6)
    return 'w_p5_s06_first_drive', sc, 'first drive'


# ---------------------------------------------------------------- M7 — the course
def m7_course():
    sc = Scene()
    floor(sc, -60)
    for i, cx in enumerate((-30, 90, 210, 330)):
        P.cone(sc, cx, 4 if i % 2 == 0 else 208, -58)
    car_on(sc, -46, brain='esp', sensors=False)
    tag(sc, (210, 4, -14), 'מסלול סללום —\nאתם בונים אותו', dy=-26, size=6.6)
    return 'w_p5_s07_course', sc, 'the course'


SCENES = [m1_meet_esp32, m2_swap_brain, m3_rewire, m4_upload, m5_connect_phone, m6_first_drive, m7_course]
