"""parts.py — the physical parts of the workshop car, drawn isometrically at their real
millimetre sizes and at their real places on the chassis template.

Every coordinate here is checked against
Arduino_Projects/Project_4_Line_Following_Car/chassis_template/chassis_template_he.html —
if the template moves, these move with it.
"""
from iso import (Scene, iso, depth, cuboid, cyl_x, cyl_y, plate, shadow, wire, dupont,
                 arrow, tag, poly, shade)

# ---------------------------------------------------------------- canonical geometry (mm)
PLATE_X0, PLATE_X1 = 23.5, 273.5      # nose .. tail   (250 mm)
PLATE_Y0, PLATE_Y1 = 35.0, 185.0      # left .. right  (150 mm)
PLATE_T = 9.0                          # polygal thickness (8-10 mm)

AXLE_F, AXLE_R = 68.5, 228.5           # front / rear axle centres
MOTOR_W, MOTOR_D, MOTOR_H = 70.0, 23.0, 22.0   # TT gearbox body
MOTOR_FX, MOTOR_RX = 56.5, 170.5       # motor body x-start, front / rear
WHEEL_R, WHEEL_W = 32.5, 27.0          # 65 mm wheel

BRAIN_X, BRAIN_Y, BRAIN_W, BRAIN_D = 46.0, 86.0, 68.0, 54.0     # Uno / ESP32 zone
DRV_X, DRV_Y, DRV_W, DRV_D = 116.0, 88.5, 43.0, 43.0            # L298N zone
BAT_X, BAT_Y, BAT_W, BAT_D = 161.0, 79.5, 110.0, 61.0           # 8xAA box zone
CAM_X, CAM_Y, CAM_W, CAM_D = 42.0, 63.0, 27.0, 8.0              # P7 camera perch
SENS_L, SENS_R = (45.0, 97.0), (45.0, 123.0)                    # line-sensor bolt drops

# ---------------------------------------------------------------- colours
C_PLATE = '#eef2f6'
C_MOTOR = '#f2c200'
C_GEAR = '#b9bec6'
C_TYRE = '#2c3138'
C_RIM = '#f0f2f4'
C_UNO = '#1c7d90'
C_ESP = '#23262b'
C_CAM = '#1b1e23'
C_DRV = '#b03a2e'
C_BAT = '#31373f'
C_SENS = '#1f4e9c'
RED, BLACK, ORANGE, GREEN, BLUE, WHITE_W = '#cc1414', '#22262b', '#f28a00', '#25cc35', '#418dd9', '#e9edf2'


# ---------------------------------------------------------------- the plate
def chassis(sc, z=0.0, holes=True):
    plate(sc, z=z, thickness=PLATE_T, col=C_PLATE)
    if holes:
        for (hx, hy) in (SENS_L, SENS_R):
            cx, cy = iso(hx, hy, z + PLATE_T)
            sc.add(depth(hx, hy, z + PLATE_T) + 0.1,
                   '<ellipse cx="%.2f" cy="%.2f" rx="2.0" ry="1.15" style="fill:#c8d0d8;stroke:#9aa6b2;stroke-width:0.3"/>' % (cx, cy))


# ---------------------------------------------------------------- motors + wheels
def tt_motor(sc, side, pos, z=0.0, leads=True, lead_col=(RED, BLACK)):
    """A TT gear motor glued UNDER the plate. side='left'(y=35) or 'right'(y=185);
    pos='front' or 'rear'. The yellow gearbox sits inboard, the silver can outboard."""
    x = MOTOR_FX if pos == 'front' else MOTOR_RX
    y = PLATE_Y0 if side == 'left' else PLATE_Y1 - MOTOR_D
    zb = z - MOTOR_H                       # hangs below the plate
    L = 0 if side == 'left' else 2         # far side behind the plate, near side in front
    cuboid(sc, x, y, zb, MOTOR_W, MOTOR_D, MOTOR_H, C_MOTOR, layer=L)
    # silver motor can on the inboard end of the body
    can_x = x + MOTOR_W - 24 if pos == 'front' else x
    cuboid(sc, can_x, y + 2.5, zb + 2.5, 24, MOTOR_D - 5, MOTOR_H - 5, C_GEAR, layer=L)
    # axle stub out through the side wall
    ax = AXLE_F if pos == 'front' else AXLE_R
    ay = PLATE_Y0 - 6 if side == 'left' else PLATE_Y1
    cyl_y(sc, ax, ay, zb + MOTOR_H / 2, 6, 1.6, '#9aa0a6', layer=L)
    if leads:
        ly = y + MOTOR_D / 2
        lx = x if pos == 'front' else x + MOTOR_W
        for i, col in enumerate(lead_col):
            wire(sc, [(lx, ly + (i * 3 - 1.5), zb + MOTOR_H * 0.6),
                      (lx + (14 if pos == 'front' else -14), ly + (i * 3 - 1.5) + 4, zb + MOTOR_H * 0.9),
                      (DRV_X + DRV_W / 2, DRV_Y + (6 if side == 'left' else DRV_D - 6), z + 2)],
                 col, 1.3, layer=4)


def wheel(sc, side, pos, z=0.0):
    x = AXLE_F if pos == 'front' else AXLE_R
    zc = z - MOTOR_H / 2 - MOTOR_H / 2 + 3      # axle height
    if side == 'left':
        y0 = PLATE_Y0 - 6 - WHEEL_W
    else:
        y0 = PLATE_Y1 + 6
    L = 0 if side == 'left' else 2
    cyl_y(sc, x, y0, zc, WHEEL_W, WHEEL_R, C_TYRE, cap_col=C_TYRE, layer=L)
    # hub cap
    cyl_y(sc, x, y0 + (WHEEL_W - 4 if side == 'right' else 0), zc, 4, WHEEL_R * 0.42, C_RIM, cap_col=C_RIM, layer=L)


def wheels_all(sc, z=0.0):
    for s in ('left', 'right'):
        for p in ('front', 'rear'):
            wheel(sc, s, p, z)


def motors_all(sc, z=0.0, leads=True):
    for s in ('left', 'right'):
        for p in ('front', 'rear'):
            tt_motor(sc, s, p, z, leads=leads)


# ---------------------------------------------------------------- boards
def _header(sc, x0, y0, z, n, along='x', col='#1a1a1a', layer=3):
    for i in range(n):
        if along == 'x':
            cuboid(sc, x0 + i * 2.54, y0, z, 1.6, 2.2, 2.2, col, layer=layer)
        else:
            cuboid(sc, x0, y0 + i * 2.54, z, 2.2, 1.6, 2.2, col, layer=layer)


def arduino_uno(sc, z=0.0, label=True, dx=0.0, dy=0.0, layer=3):
    x, y = BRAIN_X + 2 + dx, BRAIN_Y + 3 + dy
    w, d, h = 68.6, 53.4, 1.6
    cuboid(sc, x, y, z + PLATE_T, w, d, h, C_UNO, layer=layer)
    cuboid(sc, x + 3, y + 4, z + PLATE_T + h, 12, 16, 11, '#c8ccd1', layer=layer)     # USB jack
    cuboid(sc, x + 3, y + 34, z + PLATE_T + h, 13, 12, 11, '#1a1a1a', layer=layer)    # barrel jack
    cuboid(sc, x + 26, y + 20, z + PLATE_T + h, 22, 14, 2.6, '#111318', layer=layer)  # MCU
    _header(sc, x + 20, y + 1.5, z + PLATE_T + h, 10, 'x', layer=layer)               # digital side
    _header(sc, x + 20, y + d - 3.5, z + PLATE_T + h, 8, 'x', layer=layer)            # power side
    if label:
        tag(sc, (x + w / 2, y + d / 2, z + PLATE_T + h + 12), 'Arduino Uno', dy=-16)


def esp32_devkit(sc, z=0.0, label=True, dx=0.0, dy=0.0, layer=3):
    x, y = BRAIN_X + 9 + dx, BRAIN_Y + 13 + dy
    w, d, h = 51.5, 28.3, 1.4
    cuboid(sc, x, y, z + PLATE_T, w, d, h, C_ESP, layer=layer)
    cuboid(sc, x + 2, y + 9, z + PLATE_T + h, 8, 10, 4.2, '#b9bec6', layer=layer)     # micro-USB
    cuboid(sc, x + 17, y + 5, z + PLATE_T + h, 18, 18, 2.6, '#3a3f46', layer=layer)   # shield can
    _header(sc, x + 6, y + 0.6, z + PLATE_T + h, 15, 'x', '#c9a227', layer=layer)
    _header(sc, x + 6, y + d - 2.2, z + PLATE_T + h, 15, 'x', '#c9a227', layer=layer)
    if label:
        tag(sc, (x + w / 2, y + d / 2, z + PLATE_T + h + 10), 'ESP32', dy=-15)


def esp32_cam(sc, z=0.0, label=True):
    x, y = CAM_X - 4, CAM_Y - 8
    w, d, h = 40.5, 27.0, 1.6
    cuboid(sc, x, y, z + PLATE_T, w, d, h, C_CAM)
    cuboid(sc, x + 12, y + 7, z + PLATE_T + h, 13, 13, 8, '#2b2f36')          # camera module
    cyl_x(sc, x + 11, y + 13.5, z + PLATE_T + h + 4, 3, 4.2, '#0f1114')       # lens barrel
    _header(sc, x + 2, y + 1.2, z + PLATE_T + h, 8, 'x', '#c9a227')
    _header(sc, x + 2, y + d - 2.8, z + PLATE_T + h, 8, 'x', '#c9a227')
    if label:
        tag(sc, (x + w / 2, y + d / 2, z + PLATE_T + h + 12), 'ESP32-CAM', dy=-16)


def l298n(sc, z=0.0, label=True):
    x, y = DRV_X, DRV_Y
    w, d, h = DRV_W, DRV_D, 1.6
    cuboid(sc, x, y, z + PLATE_T, w, d, h, C_DRV)
    cuboid(sc, x + 14, y + 8, z + PLATE_T + h, 16, 26, 12, '#2b2f36')         # heat sink
    for i in range(5):                                                        # fins
        cuboid(sc, x + 15 + i * 3, y + 8, z + PLATE_T + h + 12, 1.4, 26, 2.2, '#3d434b')
    cuboid(sc, x - 1.5, y + 6, z + PLATE_T + h, 5, 14, 8, '#1f6fb2')          # OUT1/2 terminal
    cuboid(sc, x + w - 3.5, y + 6, z + PLATE_T + h, 5, 14, 8, '#1f6fb2')      # OUT3/4 terminal
    cuboid(sc, x + 10, y + d - 4.5, z + PLATE_T + h, 20, 6, 8, '#1f6fb2')     # 12V/GND/5V
    _header(sc, x + 12, y + 2.0, z + PLATE_T + h, 6, 'x', '#c9a227')          # ENA..ENB
    if label:
        tag(sc, (x + w / 2, y + d / 2, z + PLATE_T + h + 14), 'L298N', dy=-16)


def battery_box(sc, z=0.0, label=True, switch=True):
    x, y = BAT_X, BAT_Y
    w, d, h = BAT_W, BAT_D, 28.0
    cuboid(sc, x, y, z + PLATE_T, w, d, h, C_BAT)
    # lid seam + cell hints
    for r in range(2):
        for c in range(4):
            cuboid(sc, x + 7 + c * 24.5, y + 8 + r * 25, z + PLATE_T + h, 21, 19, 0.5, '#3a4049')
    if switch:
        cuboid(sc, x + w - 26, y + 5, z + PLATE_T + h, 14, 7, 3.4, '#14171b')
    if label:
        tag(sc, (x + w / 2, y + d / 2, z + PLATE_T + h + 8), '8 × AA', dy=-14)


def ir_sensor(sc, which='left', z=0.0, label=None):
    """TCRT5000 module bolted under the nose, eyes facing the floor."""
    sx, sy = SENS_L if which == 'left' else SENS_R
    w, d, h = 30.0, 12.0, 1.6
    x, y = sx - w / 2 + 6, sy - d / 2
    cuboid(sc, x, y, z - 6 - h, w, d, h, C_SENS, layer=2)
    for i in range(2):                                                        # the two eyes
        cyl_x(sc, x + 4 + i * 8, y + d / 2, z - 6 - h - 2.6, 2.2, 2.6, '#78c0e8' if i == 0 else '#161616', layer=2)
    _header(sc, x + w - 9, y + 3.5, z - 6, 3, 'x', '#c9a227', layer=2)
    if label:
        tag(sc, (sx, sy, z - 6), label, dy=16)


def y_splitter(sc, z=0.0, label=True):
    """The soldered Y-splitter that replaced the breadboard: one 5 V wire in, two out,
    the joint covered in heat-shrink."""
    jx, jy, jz = 92.0, 148.0, z + PLATE_T + 3
    cuboid(sc, jx, jy - 2.4, jz, 12, 4.8, 4.0, '#1d2733')                     # heat-shrink sleeve
    wire(sc, [(BRAIN_X + 40, BRAIN_Y + 50, z + PLATE_T + 4), (jx, jy, jz + 2)], RED, 1.4)
    wire(sc, [(jx + 12, jy, jz + 2), (72, 132, z + PLATE_T + 2), (SENS_L[0] + 12, SENS_L[1], z - 4)], RED, 1.2)
    wire(sc, [(jx + 12, jy, jz + 2), (76, 140, z + PLATE_T + 2), (SENS_R[0] + 12, SENS_R[1], z - 4)], RED, 1.2)
    if label:
        tag(sc, (jx + 6, jy, jz + 4), 'מפצל 5V\nבשרוול מתכווץ', dy=-17, size=6.0)


# ---------------------------------------------------------------- tools / hands
def glue_gun(sc, x, y, z, ang=0.0):
    cuboid(sc, x, y, z, 34, 14, 20, '#e06666')
    cuboid(sc, x + 30, y + 4, z + 6, 16, 6, 6, '#9aa0a6')                     # nozzle
    cuboid(sc, x + 4, y + 3, z - 16, 10, 8, 16, '#c9553f')                    # handle
    cuboid(sc, x - 12, y + 5, z + 10, 14, 4, 4, '#f2f2f2')                    # glue stick


def craft_knife(sc, x, y, z):
    cuboid(sc, x, y, z, 46, 6, 5, '#3a4149')
    poly_pts = [iso(x + 46, y + 3, z + 5), iso(x + 62, y + 3, z + 4), iso(x + 62, y + 3, z + 1), iso(x + 46, y + 3, z)]
    sc.add(depth(x + 54, y + 3, z + 3), poly(poly_pts, '#c9ced4', '#8d959d', 0.3))


def screwdriver(sc, x, y, z):
    cuboid(sc, x, y, z, 26, 9, 9, '#e8b83a')
    cyl_x(sc, x + 26, y + 4.5, z + 4.5, 40, 1.8, '#b9bec6')


def phone(sc, x, y, z, screen='#123456', ang='flat'):
    cuboid(sc, x, y, z, 70, 34, 7, '#1a1d22')
    cuboid(sc, x + 2, y + 2, z + 7, 66, 30, 0.4, screen)


def multimeter(sc, x, y, z):
    cuboid(sc, x, y, z, 44, 70, 12, '#e0a020')
    cuboid(sc, x + 5, y + 8, z + 12, 34, 22, 0.6, '#0f1a12')
    cyl_x(sc, x + 12, y + 46, z + 12, 2, 8, '#2b2f36')


# ---------------------------------------------------------------- props (drawn flat, so they read)
def phone_flat(sc, x, y, z, buttons=('#2563eb', '#2563eb'), video=False, label=None, layer=5):
    """A phone lying screen-up beside the car: 75 x 155 mm, real scale."""
    W, D = 155.0, 75.0
    cuboid(sc, x, y, z, W, D, 7, '#2b3038', layer=layer)
    zt = z + 7
    key = depth(x + W / 2, y + D / 2, z + 3.5)          # the body's own sort key

    def face(x0, y0, w, d_, col, bump):
        """A flat rectangle lying on the screen, painted in a fixed order above the body."""
        sc.add(key + bump, poly([iso(x0, y0, zt), iso(x0 + w, y0, zt),
                                 iso(x0 + w, y0 + d_, zt), iso(x0, y0 + d_, zt)], col, None), layer)

    face(x + 4, y + 4, W - 8, D - 8, '#e8edf2', 1)                              # lit screen
    if video:
        vw = W * 0.52
        face(x + 8, y + 8, vw, D - 16, '#3c4a57', 2)                            # video pane
        px_, py_ = iso(x + 8 + vw / 2, y + D / 2, zt)
        sc.add(key + 3, '<path d="M %.2f %.2f l 12 6.5 l -12 6.5 z" style="fill:#e8edf2"/>'
               % (px_ - 5, py_ - 6.5), layer)
        bx = x + 12 + vw
    else:
        bx = x + 14
    for i, col in enumerate(buttons):
        face(bx + i * 30, y + 14, 26, D - 28, col, 4 + i)
    if label:
        tag(sc, (x + W / 2, y + 2, z + 9), label, dy=-34, size=6.4)


def laptop(sc, x, y, z, layer=5):
    """Laptop: base lying flat, screen standing at the FAR edge (small y), facing the viewer."""
    cuboid(sc, x, y, z, 150, 108, 5, '#3a4048', layer=layer)                     # base
    cuboid(sc, x + 12, y + 20, z + 5, 126, 62, 0.6, '#22262c', layer=layer)      # keyboard
    cuboid(sc, x + 52, y + 88, z + 5, 46, 14, 0.6, '#4a5058', layer=layer)       # trackpad
    cuboid(sc, x, y - 5, z, 150, 5, 100, '#4a5058', layer=layer)                 # lid
    cuboid(sc, x + 6, y - 0.6, z + 8, 138, 0.7, 86, '#e8edf2', layer=layer)      # bright screen
    cuboid(sc, x + 14, y - 1.0, z + 60, 122, 0.4, 8, '#2f8fd0', layer=layer)     # IDE toolbar


def cone(sc, x, y, z, h=42, layer=0):
    cuboid(sc, x, y, z, 30, 30, 3, '#c2540f', layer=layer)
    cuboid(sc, x + 6, y + 6, z + 3, 18, 18, h * 0.5, '#f08a3c', layer=layer)
    cuboid(sc, x + 8, y + 8, z + 3 + h * 0.5, 14, 14, h * 0.18, '#ffffff', layer=layer)
    cuboid(sc, x + 10, y + 10, z + 3 + h * 0.68, 10, 10, h * 0.32, '#f08a3c', layer=layer)
