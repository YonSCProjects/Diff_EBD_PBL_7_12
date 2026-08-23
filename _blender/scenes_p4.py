"""scenes_p4.py — one function per Project 4 step illustration.

Each builds the hardware only. The Hebrew callouts, arrows and highlight rings are composited
over the render afterwards as SVG, so the type stays crisp at print size and a wording change
costs no re-render.

Naming: s_<same key the SVG kit uses>, so the two stay in step.
"""
import math
import lib as L
import p4_car as C
from lib import MM, box, cyl, prism, tube, mat, hexcol

CAR_CENTRE = (148.0, 110.0, -10.0)


def _studio(strength=1.0):
    L.studio(strength=strength)


def _bench(z, x0=-40, y0=-30, w=420, d=320, colour='#d8cfbe'):
    """The work surface. Scenes that call this must NOT also add L.ground(): two coplanar
    surfaces z-fight, and the shadow catcher wins, leaving a black bench-shaped hole."""
    m = mat('bench', hexcol(colour), rough=0.72)
    return box(x0, y0, z - 7, w, d, 7, m, bevel=1.5, name='bench')


def _floor_tape(x0, y, length, z, width=19.0):
    m = mat('tape_black', hexcol('#15181c'), rough=0.7)
    return box(x0, y, z + 0.05, length, width, 0.25, m, bevel=0, name='tape')


# ---------------------------------------------------------------- M3a — cut the plate
def s_cut_plate():
    """The template taped to a polygal sheet, knife on the line."""
    _studio()
    L.ground(z=-6.5, shadow_only=True)
    sheet = mat('polygal_sheet', hexcol('#dfe9f0'), rough=0.26, transmission=0.7, ior=1.52)
    box(8, 20, -6, 285, 180, 8, sheet, bevel=0.5, name='sheet')
    paper = mat('paper', hexcol('#fffdf7'), rough=0.9)
    box(23.5, 35, 2.2, 250, 150, 0.4, paper, bevel=0, name='template')
    ink = mat('ink', hexcol('#15181c'), rough=0.8)
    for i in range(len(C.OUTLINE)):
        (x1, y1), (x2, y2) = C.OUTLINE[i], C.OUTLINE[(i + 1) % len(C.OUTLINE)]
        ln = math.hypot(x2 - x1, y2 - y1)
        b = box(0, -0.5, 0, ln, 1.0, 0.15, ink, bevel=0, name='cutline')
        b.location = ((x1) * MM, (y1) * MM, 2.65 * MM)
        b.rotation_euler = (0, 0, math.atan2(y2 - y1, x2 - x1))
    tape = mat('masking', hexcol('#ffdf7a'), rough=0.8)
    for tx, ty in ((28, 40), (244, 40), (28, 166), (244, 166)):
        box(tx, ty, 2.6, 22, 13, 0.3, tape, bevel=0, name='masktape')
    knife(150, 27, 4.0)
    L.camera((150, 105, 0), 620, azimuth=40, elevation=42, lens=62)


def knife(x, y, z):
    m_h = mat('knife_h', hexcol('#c8542a'), rough=0.45)
    m_b = mat('knife_b', hexcol('#d5d9de'), rough=0.22, metal=1.0)
    box(x, y - 5, z, 96, 12, 11, m_h, bevel=1.5, name='knife')
    b = box(x - 22, y - 1, z + 1, 26, 1.0, 12, m_b, bevel=0, name='blade')
    b.rotation_euler = (0, math.radians(-12), 0)


# ---------------------------------------------------------------- M3b — glue the motors
def s_glue_motors():
    """The plate turned over, motors going onto what becomes the underside."""
    _studio()
    _bench(-6.5)
    C.ensure()
    C.chassis(z=0.0)
    glue = mat('glue', hexcol('#f7e3b8'), rough=0.35, transmission=0.35, ior=1.45)
    for pos, side in (('front', 'left'), ('front', 'right'), ('rear', 'left')):
        C.tt_motor(side, pos, z=-C.MOTOR_H - C.PLATE_T + C.PLATE_T, leads=False)
    # beads under the fourth, which is still coming down
    mx = C.MOTOR_RX
    my = C.PLATE_Y1 - C.MOTOR_D
    for gx in range(int(mx) + 6, int(mx + C.MOTOR_W) - 4, 10):
        cyl(gx, my + C.MOTOR_D / 2, C.PLATE_T, 3.4, 1.6, glue, name='bead')
    L.camera((150, 110, 0), 640, azimuth=36, elevation=30, lens=58)


# ---------------------------------------------------------------- M3c — rolling chassis
def s_wheels_on():
    _studio()
    _bench(C.Z_GROUND)
    C.ensure()
    C.chassis()
    C.motors_all(leads=False)
    C.wheels_all()
    L.anchor('wheel_front_left', (C.AXLE_F, C.PLATE_Y0 - 20, C.Z_AXLE))
    L.anchor('motor_rear', (C.MOTOR_RX + 35, C.PLATE_Y1 - 12, -C.MOTOR_H / 2))
    L.anchor('plate', (150, 110, C.PLATE_T))
    L.camera(CAR_CENTRE, 660, azimuth=38, elevation=26, lens=58)


# ---------------------------------------------------------------- M4 — the full wiring
def s_wiring():
    _studio()
    _bench(C.Z_GROUND)
    C.car()
    L.anchor('uno', (C.BRAIN_X + 36, C.BRAIN_Y + 30, C.PLATE_T + 4))
    L.anchor('driver', (C.DRV_X + 22, C.DRV_Y + 22, C.PLATE_T + 16))
    L.anchor('battery', (C.BAT_X + 55, C.BAT_Y + 30, C.PLATE_T + 17))
    L.anchor('splitter', (94, 68, C.PLATE_T + 8))
    L.anchor('sensor_left', C.SENS_L + (-10.0,))
    L.anchor('sensor_right', C.SENS_R + (-10.0,))
    L.anchor('common_gnd', (C.DRV_X + 20, 150, C.PLATE_T + 11))
    L.camera(CAR_CENTRE, 600, azimuth=42, elevation=34, lens=60)


# ---------------------------------------------------------------- M5 — wheels in the air
def s_wheels_in_air():
    _studio()
    _bench(C.Z_GROUND - 60)
    riser = mat('riser', hexcol('#c8b28a'), rough=0.8)
    box(96, 66, C.Z_GROUND - 60, 110, 88, 60, riser, bevel=1.5, name='box')
    C.car()
    L.camera(CAR_CENTRE, 640, azimuth=34, elevation=22, lens=58)


# ---------------------------------------------------------------- M6 — the sensor test
def s_sensor_test():
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=False, colour='#f4f1ea', size=1600)
    _floor_tape(-60, 101, 420, C.Z_GROUND)
    C.car()
    L.camera(CAR_CENTRE, 620, azimuth=44, elevation=24, lens=58)


# ---------------------------------------------------------------- M7 — the first run
def s_first_run():
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=False, colour='#f4f1ea', size=1600)
    _floor_tape(-80, 101, 480, C.Z_GROUND)
    C.car()
    L.camera(CAR_CENTRE, 700, azimuth=52, elevation=18, lens=62)


# ---------------------------------------------------------------- a plain hero, for checking
def s_hero():
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=True)
    C.car()
    L.camera(CAR_CENTRE, 560, azimuth=38, elevation=28, lens=60)
