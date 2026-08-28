"""scenes_p7.py — Project 7 (camera explorer): the same car, now with eyes.

Same contract as scenes_p4.py and scenes_p5.py: hardware only, named anchors, Hebrew composited
afterwards. Scene keys map onto the figure names the CARDS ALREADY EMBED — see build_p7.sh.

Two things these figures have to get right or they teach the wrong lesson:
  * the FTDI TX/RX pair CROSSES — TX goes to U0R and RX to U0T. Drawn straight across, the
    figure shows a wiring that cannot work.
  * there are TWO power rails and ONE shared minus. The camera is fed from a buck converter,
    never from the driver's 12 V, and the figure has to make the two paths separable by eye.
"""
import math
import lib as L
import p4_car as C
import tools as T
import props as P
from lib import MM, box, cyl, tube, mat, hexcol

CAR_CENTRE = (148.0, 110.0, -10.0)
CAM_X, CAM_Y = 42.0, 63.0            # the camera perch on the nose, same mm as the SVG kit
BUCK_X, BUCK_Y = 104.0, 148.0


def _studio(strength=1.0):
    L.studio(strength=strength)


def _bench(z, x0=-40, y0=-30, w=420, d=320, colour='#a89a88'):
    """A scene with a bench must NOT also call L.ground() — coplanar surfaces z-fight and the
    shadow catcher wins, leaving a black bench-shaped hole."""
    m = mat('bench', hexcol(colour), rough=0.72)
    return box(x0, y0, z - 7, w, d, 7, m, bevel=1.5, name='bench')


def _car_body(z=0.0, sensors=False):
    """The Project 4 car minus its brain — every P7 figure builds on this and adds the camera."""
    C.ensure()
    C.chassis(z)
    C.motors_all(z, leads=False)
    C.wheels_all(z)
    C.l298n(z)
    C.battery_box(z)
    if sensors:
        C.ir_sensor('left', z)
        C.ir_sensor('right', z)


def _phone_extent(x, y, z, w=86.0, h=170.0):
    """The phone's real footprint, for camera_fit.

    camera_fit frames on ANCHOR POINTS, and a phone carries a single anchor somewhere on its
    screen. A tall handset tilted back therefore reached well outside the fitted frame and got
    cropped to a sliver at the edge -- on the two cards whose whole point is that the driver
    watches the phone rather than the car.
    """
    return L.bbox_pts(x - w, y - w, z - 6, x + w, y + w, z + h)


def _car_extent(z=0.0):
    """The car's real outline, for camera_fit. Without it the fit frames the three boards on
    the deck and crops the wheels off the picture."""
    return L.bbox_pts(C.PLATE_X0 - 8, C.PLATE_Y0 - 40, z + C.Z_GROUND,
                      C.PLATE_X1 + 8, C.PLATE_Y1 + 40, z + C.PLATE_T + 26)


def _nose_extent(z=0.0):
    """Just the nose half of the car. A 40 mm camera board on a 250 mm chassis is a speck in
    any frame that holds the whole vehicle, and the cards that mount and wire the camera are
    about the board, not about the car."""
    return L.bbox_pts(C.PLATE_X0 - 8, C.PLATE_Y0 - 40, z + C.Z_GROUND,
                      C.DRV_X + C.DRV_W + 6, C.PLATE_Y1 + 40, z + C.PLATE_T + 60)


def _near(pt, k=0.55, c=(148.0, 110.0)):
    """An anchor on the side of an accessory that faces the car, so the accessory itself is
    free to run off the frame edge while its callout still lands on it."""
    return (c[0] + (pt[0] - c[0]) * k, c[1] + (pt[1] - c[1]) * k, pt[2])


def _car_anchors(z=0.0):
    # +12 is inside the module's own perch bracket from the rear-quarter cameras
    L.anchor('camera', (CAM_X + 16, CAM_Y + 5, z + C.PLATE_T + 24))
    # +22/+16 lands inside the L298N's heatsink, the tallest thing on that board.
    L.anchor('driver', (C.DRV_X + 8, C.DRV_Y + 30, z + C.PLATE_T + 20))
    L.anchor('battery', (C.BAT_X + 55, C.BAT_Y + 30, z + C.PLATE_T + 17))
    # Not the plate's centre: the Uno, the driver and the battery box all sit there, so a
    # whole-vehicle label pointed at a board instead of at the plate. This corner stays bare.
    L.anchor('plate', (C.PLATE_X0 + 26, C.PLATE_Y0 + 20, z + C.PLATE_T))


# ---------------------------------------------------------------- M1 — the programmer
def s_ftdi_upload():
    """Camera and adapter facing each other on the mat, four wires between them and the yellow
    flash-mode jumper looped from IO0 to GND. The crossing TX/RX pair is the point."""
    _studio(1.05)
    _bench(0, x0=-10, y0=-10, w=350, d=250)
    T.heat_mat(16, 22, 0, 300, 190)
    C.ensure()
    cx, cy, cz = 58.0, 96.0, 1.4
    P.esp32_cam(cx, cy, cz, ribbon_up=True)
    fx, fy = 152.0, 94.0
    P.ftdi(fx, fy, cz, ang=180)
    # 5V, GND, then the crossing serial pair
    pairs = (('w_red', 0), ('w_black', 1), ('w_green', 2), ('w_blue', 3))
    for col, i in pairs:
        tube([(fx - 19 + 1.0, fy - 1.6 - i * 2.54, cz + 5),
              (118, 70 + i * 5, cz + 16),
              (cx + 42, cy + 2.5 + i * 2.54, cz + 5)], 1.0, C.M[col], name='serial')
    # the flash-mode jumper: IO0 looped to GND
    tube([(cx + 4, cy + 25, cz + 2), (cx - 12, cy + 38, cz + 14),
          (cx + 16, cy + 25, cz + 2)], 1.1, C.M['w_yellow'], name='io0')
    L.anchor('cam', (cx + 20, cy + 13, cz + 6))
    L.anchor('ftdi', (fx - 18, fy - 9, cz + 6))
    L.anchor('cross', (118, 76, cz + 18))
    L.anchor('io0', (cx - 10, cy + 38, cz + 15))
    L.camera_fit(subject='cam', azimuth=46, elevation=36, lens=60,
                 extra=L.bbox_pts(cx - 6, cy - 6, cz, fx + 4, fy + 22, cz + 26))


# ---------------------------------------------------------------- M2 — the upload ritual
def s_upload_ritual():
    """Three beats laid out as three physical cards beside the board, so the order is a thing
    on the bench rather than a paragraph. The numbers are composited over the blanks."""
    _studio(1.05)
    _bench(0, x0=-10, y0=-10, w=380, d=270)
    T.heat_mat(10, 30, 0, 150, 150)
    C.ensure()
    cx, cy, cz = 66.0, 100.0, 1.4
    P.esp32_cam(cx, cy, cz, ribbon_up=True)
    tube([(cx + 4, cy + 25, cz + 2), (cx - 12, cy + 38, cz + 14),
          (cx + 16, cy + 25, cz + 2)], 1.1, C.M['w_yellow'], name='io0')
    for i, by in enumerate((44.0, 96.0, 148.0)):
        T.rules_card(150, by, 0, 62, 42, ang=-4 + i * 3)
        L.anchor('beat%d' % (i + 1), (181, by + 21, 1))
    L.anchor('cam', (cx + 20, cy + 13, cz + 6))
    L.anchor('io0', (cx - 10, cy + 38, cz + 15))
    L.camera_fit(subject='cam', azimuth=42, elevation=42, lens=58,
                 extra=L.bbox_pts(cx - 8, cy - 8, cz, 216, 196, cz + 24))


# ---------------------------------------------------------------- M3 — first stream
def s_first_stream():
    """The board on the bench, the phone beside it showing what the lens sees. Nothing is
    mounted yet — the card is deliberately about the camera alone working first."""
    _studio()
    _bench(0, x0=-30, y0=-30, w=320, d=300)
    C.ensure()
    cx, cy, cz = 60.0, 78.0, 1.4
    P.esp32_cam(cx, cy, cz, ribbon_up=True)
    # behind the board, not in front of it: a phone between the lens and the camera fills
    # half the frame by perspective alone
    P.phone(116, 122, 0, ang=-8, tilt=58, ui='video')
    L.anchor('cam', (cx + 20, cy + 13, cz + 8))
    L.anchor('air', (cx + 18, cy + 13, cz + 44))
    L.anchor('phone', (150, 82, 74))
    L.camera_fit(subject='cam', azimuth=46, elevation=34, lens=58,
                 extra=L.bbox_pts(cx - 8, cy - 8, cz, 192, 150, cz + 90))


# ---------------------------------------------------------------- M4 — mount the camera
def s_mount_camera():
    """The camera descending onto its perch on the nose, lens forward and a little down."""
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=True)
    _car_body()
    C.ensure()
    # the perch marked out on the plate
    box(CAM_X - 4, CAM_Y - 8, C.PLATE_T, 48, 34, 0.6, C.M['velcro'], bevel=0, name='perch')
    lift = 52.0
    P.esp32_cam(CAM_X - 4, CAM_Y - 8, C.PLATE_T + lift, ribbon_up=True)
    L.anchor('cam', (CAM_X + 16, CAM_Y + 5, C.PLATE_T + lift + 14))
    L.anchor('perch', (CAM_X + 20, CAM_Y + 9, C.PLATE_T + 1))
    # the lens barrel itself blocked a point directly above it; come forward and down instead
    L.anchor('lens', (CAM_X + 8, CAM_Y - 12, C.PLATE_T + lift + 10))
    # mid-deck is where the boards are; the bare nose corner is the one patch that stays plate
    L.anchor('plate', (C.PLATE_X0 + 26, C.PLATE_Y0 + 20, C.PLATE_T))
    L.camera_fit(subject='perch', azimuth=48, elevation=30, lens=60, extra=_nose_extent())


# ---------------------------------------------------------------- M5 — two power rails
def s_power_rails():
    """Battery straight to the driver for the motors; battery through the buck converter for the
    camera; one shared minus. Two colours of red would be a lie, so the separation is spatial —
    the motor pair runs down the tail, the camera pair runs up the far side to the buck."""
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=True)
    _car_body()
    C.ensure()
    P.esp32_cam(CAM_X - 4, CAM_Y - 8, C.PLATE_T, ribbon_up=True)
    P.buck(BUCK_X, BUCK_Y, C.PLATE_T, ang=0)
    P.capacitor(78, 74, C.PLATE_T)
    zt = C.PLATE_T
    # battery -> driver: the motor rail
    for i, col in enumerate(('w_red', 'w_black')):
        tube([(C.BAT_X, C.BAT_Y + 20 + i * 7, zt + 12),
              (C.DRV_X + 30, C.DRV_Y + C.DRV_D + 12 + i * 4, zt + 9),
              (C.DRV_X + 16 + i * 7, C.DRV_Y + C.DRV_D, zt + 5)], 1.5, C.M[col], name='rail_m')
    # battery -> buck: the camera rail, kept up the far side
    for i, col in enumerate(('w_red', 'w_black')):
        tube([(C.BAT_X, C.BAT_Y + 40 + i * 6, zt + 12),
              (150, 172 + i * 4, zt + 16),
              (BUCK_X + 43, BUCK_Y + 6 + i * 8, zt + 5)], 1.3, C.M[col], name='rail_c')
    # buck -> camera
    for i, col in enumerate(('w_red', 'w_black')):
        tube([(BUCK_X, BUCK_Y + 6 + i * 8, zt + 5),
              (70, 128 + i * 5, zt + 14),
              (CAM_X + 2 + i * 5, CAM_Y + 20, zt + 3)], 1.3, C.M[col], name='cam_pwr')
    L.anchor('buck', (BUCK_X + 21, BUCK_Y + 10, zt + 11))
    L.anchor('cap', (78, 74, zt + 13))
    L.anchor('motor_rail', (C.DRV_X + 24, C.DRV_Y + C.DRV_D + 10, zt + 9))
    L.anchor('plate', (C.PLATE_X0 + 26, C.PLATE_Y0 + 20, zt))
    L.camera_fit(azimuth=44, elevation=38, lens=58, only=('buck','cap','motor_rail','plate'),
                 extra=L.bbox_pts(C.PLATE_X0 - 2, C.PLATE_Y0 - 2, C.PLATE_T - 4, C.PLATE_X1 + 2, C.PLATE_Y1 + 2, C.PLATE_T + 30))


# ---------------------------------------------------------------- M6 — CAM to the driver
def s_cam_to_driver():
    """Four wires only — 14, 15, 13, 12 — and the ENA/ENB jumper caps stay put."""
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=True)
    _car_body()
    C.ensure()
    P.esp32_cam(CAM_X - 4, CAM_Y - 8, C.PLATE_T, ribbon_up=True)
    zt = C.PLATE_T
    for i in range(4):
        col = 'w_orange' if i < 2 else 'w_green'
        lane = 44 - i * 3.6
        tube([(C.DRV_X + 13 + i * 2.6, C.DRV_Y + 2, zt + 5),
              (C.DRV_X - 10, lane, zt + 11 + i * 1.4),
              (CAM_X + 20, lane - 2, zt + 10 + i * 1.4),
              (CAM_X + 2 + i * 2.54, CAM_Y - 6.0, zt + 4)], 0.8, C.M[col], name='cam_sig')
    for hx in (C.DRV_X + 11, C.DRV_X + 27):     # the ENA/ENB caps
        box(hx, C.DRV_Y + 1, zt + 3.6, 3.6, 4.4, 3.2, C.M['header'], bevel=0.3, name='cap_jmp')
    L.anchor('cam', (CAM_X + 16, CAM_Y + 5, zt + 12))
    L.anchor('four', (CAM_X + 30, 40, zt + 14))
    L.anchor('jumpers', (C.DRV_X + 19, C.DRV_Y + 3, zt + 8))
    L.camera_fit(azimuth=48, elevation=34, lens=60, only=('four','jumpers'),
                 extra=L.bbox_pts(C.PLATE_X0 + 10, C.PLATE_Y0, C.PLATE_T - 2, C.PLATE_X1 - 10, C.PLATE_Y1, C.PLATE_T + 34))


# ---------------------------------------------------------------- M7 — drive from the page
def s_drive_from_page():
    """On the floor, the whole explorer assembled, the phone showing video on top and drive
    pads underneath. Both halves of the page have to be visible in one frame."""
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=False, colour='#f4f1ea', size=2000)
    _car_body()
    C.ensure()
    P.esp32_cam(CAM_X - 4, CAM_Y - 8, C.PLATE_T, ribbon_up=True)
    P.buck(BUCK_X, BUCK_Y, C.PLATE_T)
    P.phone(286, 176, C.Z_GROUND, ang=-20, tilt=56, ui='video')
    _car_anchors()
    L.anchor('phone', _near((320, 118, C.Z_GROUND + 78), 0.8))
    L.anchor('air', (CAM_X + 16, CAM_Y + 5, C.PLATE_T + 46))
    L.anchor('ahead', (C.PLATE_X0 - 110, 110, C.Z_GROUND + 2))
    L.camera_fit(subject='plate', azimuth=50, elevation=26, lens=56,
                 extra=_car_extent() + _phone_extent(286, 176, C.Z_GROUND))


# ---------------------------------------------------------------- M8 — drive by video only
def s_drive_by_video():
    """A wall between the driver and the car. The camera is round the corner and the phone is
    the only way to know where the car is — which is the whole exercise."""
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=False, colour='#d6cab6', size=3400)
    # the barrier runs ACROSS the view, with the car in front of it and the driver behind.
    # Placed along the car's own axis it simply cuts the car in half, which is what the first
    # version of this figure did.
    P.wall(-60, 214, C.Z_GROUND, 440, 14, 124)
    _car_body()
    C.ensure()
    P.esp32_cam(CAM_X - 4, CAM_Y - 8, C.PLATE_T, ribbon_up=True)
    P.buck(BUCK_X, BUCK_Y, C.PLATE_T)
    # the driver stands behind the barrier, so the phone has to clear it to stay visible
    T.riser(212, 286, C.Z_GROUND, 120, 90, 76)
    P.phone(232, 258, C.Z_GROUND + 76, ang=-10, tilt=56, ui='video')
    _car_anchors()
    L.anchor('wall', (150, 221, C.Z_GROUND + 124))
    L.anchor('phone', _near((268, 200, C.Z_GROUND + 150), 0.75))
    L.anchor('air', (CAM_X + 16, CAM_Y + 5, C.PLATE_T + 46))
    L.camera_fit(subject='plate', azimuth=74, elevation=28, lens=52,
                 extra=_car_extent() + _phone_extent(232, 258, C.Z_GROUND + 76))
