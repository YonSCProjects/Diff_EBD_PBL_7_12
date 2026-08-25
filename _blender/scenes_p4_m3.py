"""scenes_p4_m3.py — one figure per step of P4 T1 M3, "assembling the chassis".

The card runs seven numbered steps and now gets seven figures, one per step. They are kept in
their own module because they share a lot of staging (the plate at various stages of completion)
that the other P4 scenes do not need.

The card's own wording is the authority. Two things it says that earlier figures got wrong:
  * the motors are SCREWED to the plate with 2x M3x30 each — NOT hot-glued
  * the sensors are screwed with M3x20 and TWO NUTS as a spacer, so they sit ~1 cm off the floor
"""
import math
import lib as L
import p4_car as C
import tools as T
from lib import MM, box, cyl, prism, prism_xz, tube, revolve, mat, hexcol

SHEET = (8, 20, -6, 285, 180, 8)          # the raw polygal offcut the plate is cut from


def _studio():
    L.studio()


def _bench(z, x0=-40, y0=-30, w=430, d=330, colour='#9c8f78'):
    return box(x0, y0, z - 7, w, d, 7, mat('bench', hexcol(colour), rough=0.72),
               bevel=1.5, name='bench')


def _mats():
    return dict(
        sheet=mat('m3_sheet', hexcol('#aec6d6'), rough=0.26, transmission=0.34, ior=1.5),
        paper=mat('m3_paper', hexcol('#fffdf7'), rough=0.9),
        ink=mat('m3_ink', hexcol('#15181c'), rough=0.8),
        red_ink=mat('m3_red', hexcol('#b0342a'), rough=0.8),
        green_zone=mat('m3_green', hexcol('#2f8a52'), rough=0.85),
        masking=mat('m3_mask', hexcol('#e0c060'), rough=0.8),
        pencil_mark=mat('m3_mark', hexcol('#5a5348'), rough=0.9),
    )


def _template(z=2.2, marks=True):
    """The paper template taped on: outline, drill crosses, zip-tie slots, the green Uno zone."""
    m = _mats()
    box(23.5, 35, z, 250, 150, 0.4, m['paper'], bevel=0, name='template')
    for i in range(len(C.OUTLINE)):
        (x1, y1), (x2, y2) = C.OUTLINE[i], C.OUTLINE[(i + 1) % len(C.OUTLINE)]
        ln = math.hypot(x2 - x1, y2 - y1)
        b = box(0, -0.5, 0, ln, 1.0, 0.15, m['ink'], bevel=0, name='cutline')
        b.location = ((x1 + x2) / 2 * MM, (y1 + y2) / 2 * MM, (z + 0.45) * MM)
        b.rotation_euler = (0, 0, math.atan2(y2 - y1, x2 - x1))
    if not marks:
        return
    for hx, hy in (C.SENS_L, C.SENS_R):                      # 3.5 mm drill crosses
        for w_, d_ in ((9, 0.8), (0.8, 9)):
            box(hx - w_ / 2, hy - d_ / 2, z + 0.42, w_, d_, 0.14, m['red_ink'],
                bevel=0, name='drillmark')
    for sx in (C.BAT_X + 6, C.BAT_X + C.BAT_W - 12):         # zip-tie slots
        for sy in (C.BAT_Y - 4, C.BAT_Y + C.BAT_D + 1):
            box(sx, sy, z + 0.42, 4, 3, 0.14, m['ink'], bevel=0, name='slot')
    box(C.BRAIN_X, C.BRAIN_Y, z + 0.42, C.BRAIN_W, C.BRAIN_D, 0.12, m['green_zone'],
        bevel=0, name='greenzone')
    # the 5 cm check strip
    box(200, 24, z + 0.42, 50, 3.5, 0.14, m['ink'], bevel=0, name='checkstrip')


def _screwed_motor(side, pos, z=0.0, screws=True):
    """A motor bolted under the plate, with the two M3x30 heads showing on the top face."""
    C.tt_motor(side, pos, z=z, leads=False)
    if not screws:
        return
    x = C.MOTOR_FX if pos == 'front' else C.MOTOR_RX
    y = C.PLATE_Y0 if side == 'left' else C.PLATE_Y1 - C.MOTOR_D
    for dx in (12, C.MOTOR_W - 12):
        T.m3_screw(x + dx, y + C.MOTOR_D / 2, z + C.PLATE_T, 30)


# ================================================================ step 1
def s_m3_1_template():
    """Print at 100%, check the 5 cm strip with a ruler, tape the template to the polygal."""
    _studio()
    m = _mats()
    _bench(-6.5)
    box(*SHEET, m['sheet'], bevel=0.5, name='sheet')
    _template()
    for tx, ty in ((28, 40), (244, 40), (28, 166), (244, 166)):
        box(tx, ty, 2.6, 22, 13, 0.3, m['masking'], bevel=0, name='masktape')
    T.ruler(190, 8, 2.7, ang=0)
    T.tape_roll(316, 150, 48, ang=0)
    L.anchor('strip', (225, 26, 3))
    L.anchor('ruler', (250, 20, 5))
    L.anchor('tape', (30, 44, 3))
    L.anchor('template', (150, 130, 3))
    L.camera((156, 96, 4), 600, azimuth=40, elevation=46, lens=62)


# ================================================================ step 2
def s_m3_2_cut():
    """With the teacher: cut the outline. The cross-cuts run across the flutes."""
    _studio()
    m = _mats()
    _bench(-6.5)
    box(*SHEET, m['sheet'], bevel=0.5, name='sheet')
    # the flutes the two cross-cuts have to get through
    for fy in range(26, 196, 7):
        box(10, fy, -5.2, 281, 0.5, 6.4, m['sheet'], bevel=0, name='flute')
    _template(marks=False)
    for tx, ty in ((28, 40), (244, 40), (28, 166), (244, 166)):
        box(tx, ty, 2.6, 22, 13, 0.3, m['masking'], bevel=0, name='masktape')
    T.craft_knife(112, 14, 3.0, ang=8, tilt=-12)
    L.anchor('blade', (150, 35, 4))
    L.anchor('cross', (258.5, 60, 3))
    L.anchor('corner', (26, 168, 3))
    L.anchor('flutes', (60, 100, -2))
    L.camera((150, 98, 0), 590, azimuth=40, elevation=46, lens=62)


# ================================================================ step 3
def s_m3_3_holes():
    """Two knife stabs at each zip-tie slot; a 3.5 mm hole at each drill cross."""
    _studio()
    m = _mats()
    _bench(-6.5)
    C.ensure()
    C.chassis(z=0.0)
    _template(z=C.PLATE_T + 0.1)
    T.drill(C.SENS_R[0], C.SENS_R[1], C.PLATE_T + 6, ang=16, tilt=-90)
    for hx, hy in (C.SENS_L, C.SENS_R):
        cyl(hx, hy, -0.2, 1.75, C.PLATE_T + 0.6, m['ink'], name='hole')
    for sx in (C.BAT_X + 6, C.BAT_X + C.BAT_W - 12):
        for sy in (C.BAT_Y - 4, C.BAT_Y + C.BAT_D + 1):
            box(sx, sy, -0.2, 4, 3, C.PLATE_T + 0.6, m['ink'], bevel=0, name='slit')
    L.anchor('drill', (C.SENS_R[0] + 6, C.SENS_R[1] + 10, C.PLATE_T + 130))
    L.anchor('hole', (C.SENS_L[0], C.SENS_L[1], C.PLATE_T + 2))
    L.anchor('slot', (C.BAT_X + 8, C.BAT_Y - 3, C.PLATE_T + 2))
    L.camera((132, 104, 46), 760, azimuth=40, elevation=34, lens=58)


# ================================================================ step 4
def s_m3_4_motors():
    """The plate turned over, a bead of hot glue down each motor body, the fourth going on.

    GLUED, not screwed: these 8520-style gearboxes have no mounting holes, so there is nothing
    to bolt through. The card said "screwed, not glued" and the figure used to agree with it —
    both were wrong about the hardware."""
    _studio()
    m = _mats()
    _bench(-6.5)
    C.ensure()
    C.chassis(z=0.0)
    glue = mat('glue_bead', hexcol('#f2e2b4'), rough=0.28, transmission=0.42, ior=1.46)
    # three already down, the fourth held over its bead
    for pos, side in (('front', 'left'), ('front', 'right'), ('rear', 'left')):
        C.tt_motor(side, pos, z=0.0, leads=False, up=True)
    mx, my = C.MOTOR_RX, C.PLATE_Y1 - C.MOTOR_D
    box(mx, my, C.PLATE_T + 30, C.MOTOR_W, C.MOTOR_D, C.MOTOR_H, C.M['motor_yellow'],
        bevel=1.2, name='motor4')
    # the bead waiting on the plate, and a bead already squeezed out under each fitted motor
    for gx in range(int(mx) + 7, int(mx + C.MOTOR_W) - 5, 9):
        cyl(gx, my + C.MOTOR_D / 2, C.PLATE_T, 3.2, 1.5, glue, name='bead')
    # the gun goes off to the SIDE at the plate's own depth. Parked at -y it is the
    # nearest thing to the lens and swells until it covers the motors it is gluing.
    T.glue_gun(272, 240, C.PLATE_T, ang=-42)
    L.anchor('motor4', (mx + 35, my + 12, C.PLATE_T + 30 + C.MOTOR_H))
    L.anchor('bead', (mx + 34, my + 12, C.PLATE_T + 3))
    L.anchor('gun', (290, 270, C.PLATE_T + 40))
    L.anchor('glued', (C.MOTOR_FX + 35, C.PLATE_Y0 + 12, C.PLATE_T + 10))
    L.camera_fit(subject='bead', azimuth=36, elevation=36, lens=58,
                 extra=L.bbox_pts(C.PLATE_X0 - 6, C.PLATE_Y0 - 6, -8,
                                  C.PLATE_X1 + 6, C.PLATE_Y1 + 6, C.PLATE_T + 60))


# ================================================================ step 5
def s_m3_5_wheels():
    """Push all four wheels onto the axles: wheels outside, tight to the plate."""
    _studio()
    _bench(C.Z_GROUND)
    C.ensure()
    C.chassis()
    for s in ('left', 'right'):
        for p in ('front', 'rear'):
            _screwed_motor(s, p)
    for s, p in (('left', 'rear'), ('right', 'front'), ('right', 'rear')):
        C.wheel(s, p)
    # the fourth still coming onto its axle
    w = C.wheel('left', 'front')
    for ob in w:
        ob.location.y -= 26 * MM
    L.anchor('wheel_on', (C.AXLE_F, C.PLATE_Y0 - 40, C.Z_AXLE))
    L.anchor('axle', (C.AXLE_F, C.PLATE_Y0 - 4, C.Z_AXLE))
    L.anchor('seated', (C.AXLE_R, C.PLATE_Y1 + 20, C.Z_AXLE))
    L.camera((148, 100, -12), 720, azimuth=34, elevation=26, lens=56)


# ================================================================ step 6
def s_m3_6_boards():
    """Three parts onto the plate: battery box on zip ties, L298N screwed, Uno on velcro."""
    _studio()
    _bench(C.Z_GROUND)
    C.ensure()
    C.chassis()
    for s in ('left', 'right'):
        for p in ('front', 'rear'):
            _screwed_motor(s, p)
    C.wheels_all()
    C.battery_box()
    C.l298n()
    C.arduino_uno()
    for sx in (C.BAT_X + 6, C.BAT_X + C.BAT_W - 12):
        T.zip_tie(sx, C.BAT_Y - 4, C.PLATE_T, 3, C.BAT_D + 8, 16)
    for dx, dy in ((3, 3), (C.DRV_W - 6, C.DRV_D - 6)):
        T.m3_screw(C.DRV_X + dx, C.DRV_Y + dy, C.PLATE_T + 2.0, 10)
    L.anchor('battery', (C.BAT_X + 55, C.BAT_Y + 30, C.PLATE_T + 17))
    L.anchor('switch', (C.BAT_X + C.BAT_W - 16, C.BAT_Y + 11, C.PLATE_T + 21))
    L.anchor('driver', (C.DRV_X + 22, C.DRV_Y + 22, C.PLATE_T + 16))
    L.anchor('uno', (C.BRAIN_X + 36, C.BRAIN_Y + 30, C.PLATE_T + 6))
    L.anchor('ziptie', (C.BAT_X + 7, C.BAT_Y - 3, C.PLATE_T + 16))
    L.camera((150, 110, -6), 630, azimuth=44, elevation=34, lens=58)


# ================================================================ step 7
def s_m3_7_sensors():
    """Both line sensors on the nose: M3x20 with two nuts as a spacer, eyes at the floor."""
    _studio()
    _bench(C.Z_GROUND)
    C.ensure()
    C.chassis()
    for s in ('left', 'right'):
        for p in ('front', 'rear'):
            _screwed_motor(s, p)
    C.wheels_all()
    C.battery_box()
    C.l298n()
    C.arduino_uno()
    C.ir_sensor('right')
    # the left one going on, with its two spacer nuts visible on the bolt
    C.ir_sensor('left')
    hx, hy = C.SENS_L
    T.m3_screw(hx, hy, C.PLATE_T, 20, axis='z')  # head on top, shank down to the sensor
    T.m3_nut(hx, hy, -3.0)
    T.m3_nut(hx, hy, -6.0)
    T.screwdriver(250, 26, 14, ang=24)
    L.anchor('sensor', (C.SENS_R[0] - 8, C.SENS_R[1], -14))
    L.anchor('nuts', (hx, hy, -4.5))
    L.anchor('eye', (C.SENS_L[0] - 12, C.SENS_L[1], -17))
    L.anchor('bolt', (hx, hy, C.PLATE_T + 2))
    L.camera((120, 106, -14), 560, azimuth=28, elevation=22, lens=62)
