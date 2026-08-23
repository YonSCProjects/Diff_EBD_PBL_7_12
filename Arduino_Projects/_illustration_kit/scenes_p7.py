"""scenes_p7.py — Project 7 (camera explorer): the same car, now with eyes.

Run: python build.py 7
"""
from iso import Scene, iso, depth, cuboid, cyl_x, cyl_y, wire, arrow, tag, poly, shade
import parts as P
from scenes_p4 import floor, bench, car_on
from scenes_p5 import wifi_arc

RED, BLACK, ORANGE, GREEN, BLUE, YELLOW = P.RED, P.BLACK, P.ORANGE, P.GREEN, P.BLUE, '#e0b400'
HL = '#e0651a'
ZT = P.PLATE_T


def _cam_board(sc, x, y, z, layer=3):
    cuboid(sc, x, y, z, 40.5, 27.0, 1.6, P.C_CAM, layer=layer)
    cuboid(sc, x + 12, y + 7, z + 1.6, 13, 13, 8, '#2b2f36', layer=layer)
    cyl_x(sc, x + 11, y + 13.5, z + 5.6, 3, 4.2, '#0f1114', layer=layer)
    for i in range(8):
        cuboid(sc, x + 2 + i * 2.54, y + 1.2, z + 1.6, 1.6, 2.2, 2.2, '#c9a227', layer=layer)
        cuboid(sc, x + 2 + i * 2.54, y + 23.2, z + 1.6, 1.6, 2.2, 2.2, '#c9a227', layer=layer)


# ---------------------------------------------------------------- M1 — the programmer
def m1_ftdi_upload():
    sc = Scene()
    bench(sc, 30, 30, 250, 170)
    cx, cy, cz = 78, 92, -10
    _cam_board(sc, cx, cy, cz)
    # FTDI board opposite it
    fx, fy = 190, 92
    cuboid(sc, fx, fy, cz, 36, 18, 1.4, '#c0392b', layer=3)
    cuboid(sc, fx + 22, fy + 4, cz + 1.4, 12, 10, 5, '#b9bec6', layer=3)
    for i in range(6):
        cuboid(sc, fx + 2, fy + 2 + i * 2.6, cz + 1.4, 2.2, 1.6, 2.2, '#c9a227', layer=3)
    pairs = ((0, RED, '5V'), (1, BLACK, 'GND'), (2, GREEN, 'TX→U0R'), (3, BLUE, 'RX→U0T'))
    for i, col, _lbl in pairs:
        wire(sc, [(fx + 1, fy + 3 + i * 2.6, cz + 3), (150, 70 + i * 5, cz + 12),
                  (cx + 40, cy + 2 + i * 2.6, cz + 3)], col, 1.2)
    # the flash-mode jumper: IO0 to GND
    wire(sc, [(cx + 2, cy + 24, cz + 3), (cx - 14, cy + 34, cz + 10), (cx + 12, cy + 24, cz + 3)], YELLOW, 1.4)
    tag(sc, (cx - 12, cy + 34, cz + 10), 'IO0 אל GND —\nחוט מצב הצריבה', dx=-40, dy=18, size=6.2)
    tag(sc, (150, 78, cz + 12), 'TX אל U0R, RX אל U0T —\nהחוטים מצטלבים בכוונה', dy=-30, size=6.4)
    tag(sc, (fx + 18, fy + 9, cz + 8), 'המתכנת FTDI', dx=44, dy=-18, size=6.4)
    return 'w_p7_s01_ftdi_upload', sc, 'the FTDI programmer'


# ---------------------------------------------------------------- M2 — the upload ritual
def m2_upload_ritual():
    sc = Scene()
    bench(sc, 30, 30, 250, 170)
    cx, cy, cz = 92, 96, -10
    _cam_board(sc, cx, cy, cz)
    wire(sc, [(cx + 2, cy + 24, cz + 3), (cx - 14, cy + 34, cz + 10), (cx + 12, cy + 24, cz + 3)], YELLOW, 1.4)
    # three numbered beats of the ritual
    for i, (by, txt) in enumerate(((44, 'מחברים\nIO0 אל GND'), (100, 'לוחצים RST\nומעלים'),
                                   (156, 'מוציאים את\nהחוט הצהוב'))):
        cuboid(sc, 214, by, -10, 26, 26, 1.0, '#fff3e0', layer=3)
        cxx, cyy = iso(227, by + 13, -8)
        sc.over('<circle cx="%.2f" cy="%.2f" r="8" style="fill:%s"/>'
                '<text x="%.2f" y="%.2f" style="font-family:Rubik,Arial;font-size:9px;font-weight:800;'
                'fill:#fff;text-anchor:middle">%d</text>' % (cxx, cyy, HL, cxx, cyy + 3.2, i + 1))
        tag(sc, (227, by + 13, -6), txt, dx=56, dy=0, size=6.0)
    tag(sc, (cx + 20, cy + 13, cz + 10), 'בלי החוט הצהוב\nהמצלמה לא נכנסת למצב צריבה', dy=-30, size=6.2)
    return 'w_p7_s02_upload_ritual', sc, 'the upload ritual'


# ---------------------------------------------------------------- M3 — first stream
def m3_first_stream():
    sc = Scene()
    bench(sc, 20, 20, 300, 210)
    cx, cy, cz = 66, 62, -10
    _cam_board(sc, cx, cy, cz)
    wifi_arc(sc, cx + 18, cy + 13, cz + 12)
    P.phone_flat(sc, 148, 126, -10, video=True, label='הווידאו החי\nבדפדפן')
    tag(sc, (cx + 18, cy + 13, cz + 30), 'EXPLORER-01', dx=-46, dy=-14, size=6.2)
    return 'w_p7_s03_first_stream', sc, 'first stream'


# ---------------------------------------------------------------- M4 — mount the camera
def m4_mount_camera():
    sc = Scene()
    P.chassis(sc); P.motors_all(sc, leads=False); P.wheels_all(sc)
    P.l298n(sc, label=False); P.battery_box(sc, label=False)
    # the perch marked on the nose
    pts = [iso(P.CAM_X, P.CAM_Y, ZT + 0.1), iso(P.CAM_X + 27, P.CAM_Y, ZT + 0.1),
           iso(P.CAM_X + 27, P.CAM_Y + 8, ZT + 0.1), iso(P.CAM_X, P.CAM_Y + 8, ZT + 0.1)]
    sc.add(9100, poly(pts, 'none', '#6b46a8', 0.8, 'stroke-dasharray:2.4 1.8'), 3)
    # the camera descending onto it
    lift = 46
    _cam_board(sc, P.CAM_X - 4, P.CAM_Y - 8, ZT + lift, layer=5)
    arrow(sc, (P.CAM_X + 16, P.CAM_Y + 5, ZT + lift - 6), (P.CAM_X + 16, P.CAM_Y + 5, ZT + 8), HL)
    tag(sc, (P.CAM_X + 16, P.CAM_Y + 5, ZT + lift + 12), 'העדשה פונה קדימה\nומעט כלפי מטה', dx=-14, dy=-20, size=6.4)
    tag(sc, (P.CAM_X + 13, P.CAM_Y + 4, ZT), 'מדף המצלמה\nעל החרטום', dx=-58, dy=22, size=6.2)
    return 'w_p7_s04_mount_camera', sc, 'mount the camera'


# ---------------------------------------------------------------- M5 — two power rails
def m5_power_rails():
    sc = Scene()
    P.chassis(sc); P.motors_all(sc, leads=False); P.wheels_all(sc)
    P.l298n(sc, label=False); P.battery_box(sc, label=False)
    _cam_board(sc, P.CAM_X - 4, P.CAM_Y - 8, ZT)
    # the buck converter, zip-tied beside the driver
    bx, by = 104, 148
    cuboid(sc, bx, by, ZT, 36, 17, 4, '#1d5fa8', layer=3)
    cuboid(sc, bx + 12, by + 4, ZT + 4, 10, 9, 5, '#1b1b1b', layer=3)
    # the bulk capacitor by the camera
    cyl_x(sc, 76, 74, ZT + 6, 12, 5, '#2b2d6b', layer=3)
    # battery -> driver (motors)
    wire(sc, [(P.BAT_X, P.BAT_Y + 20, ZT + 12), (P.DRV_X + 16, P.DRV_Y + P.DRV_D + 7, ZT + 8),
              (P.DRV_X + 16, P.DRV_Y + P.DRV_D, ZT + 6)], RED, 2.0)
    wire(sc, [(P.BAT_X, P.BAT_Y + 27, ZT + 12), (P.DRV_X + 23, P.DRV_Y + P.DRV_D + 11, ZT + 8),
              (P.DRV_X + 23, P.DRV_Y + P.DRV_D, ZT + 6)], BLACK, 2.0)
    # battery -> buck -> camera
    wire(sc, [(P.BAT_X, P.BAT_Y + 34, ZT + 12), (150, 160, ZT + 8), (bx + 36, by + 4, ZT + 4)], RED, 1.8)
    wire(sc, [(P.BAT_X, P.BAT_Y + 40, ZT + 12), (152, 166, ZT + 8), (bx + 36, by + 12, ZT + 4)], BLACK, 1.8)
    wire(sc, [(bx, by + 4, ZT + 4), (70, 130, ZT + 8), (P.CAM_X - 2, P.CAM_Y + 2, ZT + 3)], RED, 1.8)
    wire(sc, [(bx, by + 12, ZT + 4), (72, 136, ZT + 8), (P.CAM_X - 2, P.CAM_Y + 6, ZT + 3)], BLACK, 1.8)
    tag(sc, (bx + 18, by + 8, ZT + 8), 'ממיר 5V —\nמסילה נפרדת למצלמה', dx=-16, dy=30, size=6.2)
    tag(sc, (82, 74, ZT + 10), 'קבל צמוד למצלמה\nהפס הלבן אל GND', dx=-16, dy=-26, size=6.2)
    tag(sc, (P.DRV_X + 20, P.DRV_Y + P.DRV_D + 8, ZT + 8), 'הבקר מקבל 12V\nמהסוללה ישירות', dx=56, dy=18, size=6.2)
    tag(sc, (148, 108, ZT), 'שתי מסילות, מינוס אחד משותף', dy=-38, size=6.8)
    return 'w_p7_s05_power_rails', sc, 'two power rails'


# ---------------------------------------------------------------- M6 — CAM to the driver
def m6_cam_to_driver():
    sc = Scene()
    P.chassis(sc); P.motors_all(sc, leads=False); P.wheels_all(sc)
    P.l298n(sc, label=False); P.battery_box(sc, label=False)
    _cam_board(sc, P.CAM_X - 4, P.CAM_Y - 8, ZT)
    labels = ('14', '15', '13', '12')
    for i in range(4):
        col = ORANGE if i < 2 else GREEN
        yy = 72 - i * 1.8
        wire(sc, [(P.DRV_X + 13 + i * 2.6, P.DRV_Y + 2, ZT + 4), (P.DRV_X + 13 + i * 2.6, yy, ZT + 6),
                  (P.CAM_X + 2 + i * 2.54, yy, ZT + 6), (P.CAM_X + 2 + i * 2.54, P.CAM_Y - 6.8, ZT + 4)], col, 1.1)
    # the ENA/ENB caps that stay on
    for hx in (P.DRV_X + 11, P.DRV_X + 27):
        cuboid(sc, hx, P.DRV_Y + 1, ZT + 3.6, 3.4, 4.2, 3.0, '#111418', layer=3)
    tag(sc, (P.DRV_X + 19, P.DRV_Y + 3, ZT + 7), 'הכובעונים על ENA ו-ENB\nנשארים במקומם', dx=64, dy=-16, size=6.2)
    tag(sc, (P.CAM_X + 6, 70, ZT + 6), 'ארבעה חוטים בלבד:\n14 · 15 · 13 · 12', dx=-30, dy=-28, size=6.4)
    return 'w_p7_s06_cam_to_driver', sc, 'camera to the driver'


# ---------------------------------------------------------------- M7 — drive from the page
def m7_drive_from_page():
    sc = Scene()
    floor(sc, -60)
    z = -46
    P.chassis(sc, z=z); P.motors_all(sc, z=z, leads=False); P.wheels_all(sc, z=z)
    P.l298n(sc, z=z, label=False); P.battery_box(sc, z=z, label=False)
    _cam_board(sc, P.CAM_X - 4, P.CAM_Y - 8, z + ZT)
    wifi_arc(sc, P.CAM_X + 16, P.CAM_Y + 5, z + ZT + 14)
    P.phone_flat(sc, 250, 152, -56, video=True, label='וידאו למעלה,\nכפתורי נהיגה למטה')
    arrow(sc, (P.PLATE_X0 - 8, 110, -54), (P.PLATE_X0 - 92, 110, -54), HL, w=3.0, head=7)
    return 'w_p7_s07_drive_from_page', sc, 'drive from the page'


# ---------------------------------------------------------------- M8 — drive by video only
def m8_drive_by_video():
    sc = Scene()
    floor(sc, -60)
    # a wall the driver cannot see past
    cuboid(sc, 150, 20, -58, 10, 90, 90, '#c9c3b6', layer=0)
    z = -46
    P.chassis(sc, z=z); P.motors_all(sc, z=z, leads=False); P.wheels_all(sc, z=z)
    P.l298n(sc, z=z, label=False); P.battery_box(sc, z=z, label=False)
    _cam_board(sc, P.CAM_X - 4, P.CAM_Y - 8, z + ZT)
    wifi_arc(sc, P.CAM_X + 16, P.CAM_Y + 5, z + ZT + 14)
    P.phone_flat(sc, 250, 172, -56, video=True, label='רק המסך —\nלא המכונית')
    tag(sc, (155, 60, 30), 'הנהג לא רואה את המכונית —\nרק את מה שהמצלמה רואה', dx=10, dy=-30, size=6.6)
    return 'w_p7_s08_drive_by_video', sc, 'drive by video only'


SCENES = [m1_ftdi_upload, m2_upload_ritual, m3_first_stream, m4_mount_camera,
          m5_power_rails, m6_cam_to_driver, m7_drive_from_page, m8_drive_by_video]
