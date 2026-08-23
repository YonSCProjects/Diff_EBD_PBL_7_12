"""p4_car.py — the Project 4 line-following car as real 3D geometry.

Every number here is the one parts.py draws with, which is itself checked against
Arduino_Projects/Project_4_Line_Following_Car/chassis_template/chassis_template_he.html.
If the template moves, both move together.

  plate    250 x 150 x 9 polygal twin-wall, corners clipped 15 mm, flutes along the car
  motors   4 x TT gear motor, 70 x 23 x 22, glued UNDER the plate
  wheels   65 mm diameter, 27 mm wide
  brain    Arduino Uno on the nose half, L298N beside it, 8xAA box at the tail
  sensors  2 x TCRT5000 hanging under the nose, eyes down
"""
import math
import lib as L
from lib import MM, box, cyl, prism, tube, torus, mat, hexcol

# ---------------------------------------------------------------- canonical geometry (mm)
PLATE_X0, PLATE_X1 = 23.5, 273.5
PLATE_Y0, PLATE_Y1 = 35.0, 185.0
PLATE_T = 9.0
OUTLINE = [(38.5, 35), (258.5, 35), (273.5, 50), (273.5, 170),
           (258.5, 185), (38.5, 185), (23.5, 170), (23.5, 50)]

AXLE_F, AXLE_R = 68.5, 228.5
MOTOR_W, MOTOR_D, MOTOR_H = 70.0, 23.0, 22.0
MOTOR_FX, MOTOR_RX = 56.5, 170.5
WHEEL_R, WHEEL_W = 32.5, 27.0

BRAIN_X, BRAIN_Y, BRAIN_W, BRAIN_D = 46.0, 86.0, 68.0, 54.0
DRV_X, DRV_Y, DRV_W, DRV_D = 116.0, 88.5, 43.0, 43.0
BAT_X, BAT_Y, BAT_W, BAT_D = 161.0, 79.5, 110.0, 61.0
SENS_L, SENS_R = (45.0, 97.0), (45.0, 123.0)

Z_MOTOR = -MOTOR_H            # motors hang under the plate
Z_AXLE = -19.0
Z_GROUND = Z_AXLE - WHEEL_R   # where the wheels touch

CENTRE = (148.0, 110.0, 0.0)


# ---------------------------------------------------------------- materials
def materials():
    return dict(
        polygal=mat('polygal', hexcol('#eef4f8'), rough=0.16, transmission=0.88,
                    ior=1.50, clearcoat=0.35),
        polygal_rib=mat('polygal_rib', hexcol('#e6eef4'), rough=0.22, transmission=0.80, ior=1.50),
        motor_yellow=mat('motor_yellow', hexcol('#c99a06'), rough=0.46, clearcoat=0.28),
        motor_can=mat('motor_can', hexcol('#b9bec6'), rough=0.30, metal=1.0),
        gearbox_dark=mat('gearbox_dark', hexcol('#2b2f36'), rough=0.5),
        tyre=mat('tyre', hexcol('#24282e'), rough=0.86),
        rim=mat('rim', hexcol('#c9ccd1'), rough=0.46, clearcoat=0.22),
        pcb_uno=mat('pcb_uno', hexcol('#0d4a57'), rough=0.5, clearcoat=0.35, cc_rough=0.32),
        pcb_drv=mat('pcb_drv', hexcol('#6e1f18'), rough=0.5, clearcoat=0.35, cc_rough=0.32),
        pcb_sens=mat('pcb_sens', hexcol('#1b4890'), rough=0.46, clearcoat=0.45, cc_rough=0.3),
        header=mat('header', hexcol('#14171b'), rough=0.44),
        gold=mat('gold', hexcol('#caa03a'), rough=0.3, metal=1.0),
        steel=mat('steel', hexcol('#9aa0a6'), rough=0.3, metal=1.0),
        alu=mat('alu', hexcol('#c8ccd1'), rough=0.26, metal=1.0),
        heatsink=mat('heatsink', hexcol('#22262c'), rough=0.44, metal=0.65),
        terminal=mat('terminal', hexcol('#1f6fb2'), rough=0.42),
        batbox=mat('batbox', hexcol('#14181d'), rough=0.62, clearcoat=0.12),
        switch=mat('switch', hexcol('#d8dce1'), rough=0.4),
        led_red=mat('led_red', hexcol('#e03030'), rough=0.3, emission=hexcol('#ff3020'),
                    emission_strength=3.0),
        w_red=mat('w_red', hexcol('#c21b1b'), rough=0.5),
        w_black=mat('w_black', hexcol('#15181c'), rough=0.55),
        w_orange=mat('w_orange', hexcol('#e07a1a'), rough=0.5),
        w_green=mat('w_green', hexcol('#27a83c'), rough=0.5),
        w_blue=mat('w_blue', hexcol('#2f6fd0'), rough=0.5),
        w_yellow=mat('w_yellow', hexcol('#d8b430'), rough=0.5),
        shrink=mat('shrink', hexcol('#1b2b6b'), rough=0.5),
        velcro=mat('velcro', hexcol('#3f4650'), rough=0.92),
        tape=mat('tape', hexcol('#15181c'), rough=0.72),
    )


M = None


def ensure():
    global M
    if M is None:
        M = materials()
    return M


# ---------------------------------------------------------------- the plate
def chassis(z=0.0, flutes=True):
    """The polygal plate. The twin-wall ribs are real geometry — with a translucent skin they
    are what makes the material read as polygal rather than as white plastic."""
    m = ensure()
    parts = [prism(OUTLINE, z, PLATE_T, m['polygal'], name='plate', bevel=0.4)]
    if flutes:
        y = PLATE_Y0 + 6
        while y < PLATE_Y1 - 5:
            parts.append(box(PLATE_X0 + 5, y, z + 0.9, PLATE_X1 - PLATE_X0 - 10, 0.45,
                             PLATE_T - 1.8, m['polygal'], bevel=0, name='rib'))
            y += 7.5
    return parts


def sensor_holes(z=0.0):
    m = ensure()
    return [cyl(hx, hy, z - 0.1, 2.0, PLATE_T + 0.2, m['gearbox_dark'], name='hole')
            for hx, hy in (SENS_L, SENS_R)]


# ---------------------------------------------------------------- motors and wheels
def tt_motor(side, pos, z=0.0, leads=True):
    """One TT gear motor glued under the plate: yellow gearbox inboard, silver can outboard,
    output shaft through the side wall."""
    m = ensure()
    x = MOTOR_FX if pos == 'front' else MOTOR_RX
    y = PLATE_Y0 if side == 'left' else PLATE_Y1 - MOTOR_D
    zb = z + Z_MOTOR
    out = [box(x, y, zb, MOTOR_W, MOTOR_D, MOTOR_H, m['motor_yellow'], bevel=1.2, name='gearbox')]
    can_x = x + MOTOR_W - 24 if pos == 'front' else x
    out.append(cyl(can_x, y + MOTOR_D / 2, zb + MOTOR_H / 2, 9.6, 24, m['motor_can'],
                   axis='x', name='can'))
    # the gearbox output boss and the axle through the plate's side wall
    ax = AXLE_F if pos == 'front' else AXLE_R
    ay = PLATE_Y0 - 3 if side == 'left' else PLATE_Y1 + 3
    out.append(cyl(ax, y + MOTOR_D / 2, z + Z_AXLE, 6.0, MOTOR_D, m['gearbox_dark'],
                   axis='y', name='boss'))
    sgn = -1 if side == 'left' else 1
    out.append(cyl(ax, ay, z + Z_AXLE, 2.6, sgn * 9, m['steel'], axis='y', name='axle'))
    if leads:
        lx = x if pos == 'front' else x + MOTOR_W
        ly = y + MOTOR_D / 2
        for i, col in enumerate(('w_red', 'w_black')):
            o = (i - 0.5) * 4
            out.append(tube([(lx, ly + o, zb + 13),
                             (lx + (-16 if pos == 'front' else 16), ly + o + 4, zb + 17),
                             (DRV_X + 8 + i * 6, DRV_Y + (4 if side == 'left' else DRV_D - 4), z + 3)],
                            1.1, m[col], name='lead'))
    return out


def wheel(side, pos, z=0.0):
    """A 65 mm wheel: rubber tyre, cream hub, spokes."""
    m = ensure()
    x = AXLE_F if pos == 'front' else AXLE_R
    y0 = (PLATE_Y0 - 6 - WHEEL_W) if side == 'left' else (PLATE_Y1 + 6)
    zc = z + Z_AXLE
    # A real 65 mm wheel is a black rubber tyre with the cream rim face standing slightly proud
    # of it on both sides. Modelling the rim LARGER than the tyre's inner radius (as a torus tempts
    # you to) makes the rim swallow the tyre and the wheel reads as a blob.
    out = [cyl(x, y0, zc, WHEEL_R, WHEEL_W, m['tyre'], axis='y', name='tyre', seg=96)]
    out.append(cyl(x, y0 - 0.3, zc, WHEEL_R - 7.0, WHEEL_W + 0.6, m['rim'],
                   axis='y', name='rim', seg=80))
    # five spoke slots so the rim face is not a blank disc
    for k in range(5):
        a = 2 * math.pi * k / 5
        sx = x + math.cos(a) * (WHEEL_R - 15)
        sz = zc + math.sin(a) * (WHEEL_R - 15)
        out.append(cyl(sx, y0 - 0.6, sz, 4.6, WHEEL_W + 1.2, m['gearbox_dark'],
                       axis='y', name='spoke', seg=28))
    hub_y = y0 + WHEEL_W - 1 if side == 'right' else y0 - 3
    out.append(cyl(x, hub_y, zc, 7.0, 4, m['rim'], axis='y', name='hub', seg=44))
    out.append(cyl(x, hub_y - 0.4, zc, 2.9, 4.8, m['gearbox_dark'], axis='y', name='bore', seg=28))
    return out


def motors_all(z=0.0, leads=True):
    out = []
    for s in ('left', 'right'):
        for p in ('front', 'rear'):
            out += tt_motor(s, p, z, leads)
    return out


def wheels_all(z=0.0):
    out = []
    for s in ('left', 'right'):
        for p in ('front', 'rear'):
            out += wheel(s, p, z)
    return out


# ---------------------------------------------------------------- boards
def _header(x0, y0, z, n, m, along='x'):
    out = []
    for i in range(n):
        dx, dy = (i * 2.54, 0) if along == 'x' else (0, i * 2.54)
        out.append(box(x0 + dx, y0 + dy, z, 2.2, 2.2, 2.4, m, bevel=0, name='hdr'))
    return out


def arduino_uno(z=0.0, velcro=True):
    m = ensure()
    x, y = BRAIN_X + 2, BRAIN_Y + 3
    w, d, t = 68.6, 53.4, 1.6
    zt = z + PLATE_T
    out = []
    if velcro:
        out.append(box(x + 4, y + 5, zt, w - 8, d - 10, 1.2, m['velcro'], bevel=0, name='velcro'))
        zt += 1.2
    out.append(box(x, y, zt, w, d, t, m['pcb_uno'], bevel=0.5, name='uno'))
    out.append(box(x + 3, y + 4, zt + t, 12, 16, 11, m['alu'], bevel=0.4, name='usb'))
    out.append(box(x + 2, y + 34, zt + t, 13, 12, 11, m['gearbox_dark'], bevel=0.6, name='barrel'))
    out.append(box(x + 26, y + 20, zt + t, 22, 14, 2.6, m['header'], bevel=0.2, name='mcu'))
    out += _header(x + 20, y + 1.2, zt + t, 10, m['header'])
    out += _header(x + 20, y + d - 3.4, zt + t, 8, m['header'])
    out.append(box(x + 52, y + 22, zt + t, 3, 1.6, 1.2, m['led_red'], bevel=0, name='led'))
    return out


def l298n(z=0.0):
    m = ensure()
    x, y = DRV_X, DRV_Y
    w, d, t = DRV_W, DRV_D, 1.6
    zt = z + PLATE_T
    out = [box(x, y, zt, w, d, t, m['pcb_drv'], bevel=0.5, name='l298n')]
    out.append(box(x + 14, y + 8, zt + t, 16, 26, 12, m['heatsink'], bevel=0.4, name='sink'))
    for i in range(6):
        out.append(box(x + 15 + i * 2.6, y + 8, zt + t + 12, 1.3, 26, 3.0, m['heatsink'],
                       bevel=0, name='fin'))
    out.append(box(x - 1.5, y + 6, zt + t, 5, 14, 9, m['terminal'], bevel=0.3, name='out12'))
    out.append(box(x + w - 3.5, y + 6, zt + t, 5, 14, 9, m['terminal'], bevel=0.3, name='out34'))
    out.append(box(x + 10, y + d - 4.5, zt + t, 20, 6, 9, m['terminal'], bevel=0.3, name='pwr'))
    out += _header(x + 11, y + 1.2, zt + t, 6, m['header'])
    return out


def battery_box(z=0.0, switch=True):
    m = ensure()
    x, y = BAT_X, BAT_Y
    zt = z + PLATE_T
    out = [box(x, y, zt, BAT_W, BAT_D, 15, m['batbox'], bevel=1.2, name='batbox')]
    out.append(box(x + 1.5, y + 1.5, zt + 15, BAT_W - 3, BAT_D - 3, 2.0, m['batbox'],
                   bevel=0.8, name='batlid'))
    if switch:
        out.append(box(x + BAT_W - 24, y + 7, zt + 17, 15, 9, 4, m['switch'], bevel=0.5,
                       name='switch'))
    out.append(tube([(x, y + BAT_D / 2 - 4, zt + 7), (x - 18, y + BAT_D / 2 - 6, zt + 12),
                     (DRV_X + 14, DRV_Y + DRV_D, z + PLATE_T + 8)], 1.4, m['w_red'], name='batred'))
    out.append(tube([(x, y + BAT_D / 2 + 4, zt + 7), (x - 18, y + BAT_D / 2 + 6, zt + 12),
                     (DRV_X + 22, DRV_Y + DRV_D, z + PLATE_T + 8)], 1.4, m['w_black'], name='batblk'))
    return out


def ir_sensor(side, z=0.0):
    """A TCRT5000 board bolted under the nose, eyes pointing at the floor."""
    m = ensure()
    hx, hy = SENS_L if side == 'left' else SENS_R
    w, d, t = 32.0, 12.0, 1.5
    zb = z - 12.0
    out = [box(hx - 22, hy - d / 2, zb, w, d, t, m['pcb_sens'], bevel=0.4, name='ir')]
    for dx in (-6, 0):
        out.append(box(hx - 14 + dx, hy - 2.6, zb - 4.4, 5, 5.2, 4.4, m['gearbox_dark'],
                       bevel=0.3, name='eye'))
    out.append(cyl(hx, hy, zb, 1.6, PLATE_T + 12, m['steel'], name='bolt'))
    out.append(box(hx - 22 + w - 9, hy - 1.4, zb + t, 6, 2.8, 2.6, m['header'], bevel=0, name='pins'))
    return out


def y_splitter(z=0.0):
    """The soldered 5 V splitter that replaced the breadboard: one lead in, two out,
    heat-shrink over the joint."""
    m = ensure()
    ux, uy = BRAIN_X + 2, BRAIN_Y + 3
    jx, jy, jz = 92.0, 66.0, z + PLATE_T + 6
    out = [tube([(ux + 46, uy + 2, z + PLATE_T + 4), (jx + 8, jy + 6, jz)], 1.1, m['w_red'],
                name='y_in')]
    for (sx, sy) in (SENS_L, SENS_R):
        out.append(tube([(jx, jy, jz), (70, sy - 6, z + PLATE_T + 2), (sx - 8, sy, z - 9)],
                        1.0, m['w_red'], name='y_out'))
    out.append(cyl(jx + 2, jy + 2, jz - 2, 3.0, 12, m['shrink'], axis='x', name='shrink'))
    return out


def signal_wires(z=0.0):
    """The six driver wires to pins 5-10, plus the thick common ground."""
    m = ensure()
    ux, uy = BRAIN_X + 2, BRAIN_Y + 3
    cols = ('w_green', 'w_orange', 'w_orange', 'w_orange', 'w_orange', 'w_green')
    out = []
    for i in range(6):
        out.append(tube([(DRV_X + 12 + i * 2.6, DRV_Y + 2, z + PLATE_T + 6),
                         (DRV_X - 6, 74 - i * 2, z + PLATE_T + 10),
                         (ux + 22 + i * 2.54, uy + 2.2, z + PLATE_T + 5)],
                        0.85, m[cols[i]], name='sig'))
    out.append(tube([(DRV_X + 30, DRV_Y + DRV_D, z + PLATE_T + 8),
                     (DRV_X + 10, 152, z + PLATE_T + 12),
                     (ux + 30, uy + 52, z + PLATE_T + 5)], 1.5, m['w_black'], name='gnd'))
    return out


# ---------------------------------------------------------------- the whole car
def car(z=0.0, brain='uno', wheels=True, motors=True, sensors=True, battery=True,
        wiring=True, leads=True):
    out = []
    out += chassis(z)
    if sensors:
        out += sensor_holes(z)
    if motors:
        out += motors_all(z, leads=leads and not wiring)
    if wheels:
        out += wheels_all(z)
    if brain == 'uno':
        out += arduino_uno(z)
    out += l298n(z)
    if battery:
        out += battery_box(z)
    if sensors:
        out += ir_sensor('left', z) + ir_sensor('right', z)
    if wiring:
        out += signal_wires(z) + y_splitter(z)
        out += motors_all.__wrapped__(z) if False else []
    return out
