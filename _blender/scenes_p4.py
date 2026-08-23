"""scenes_p4.py — one function per Project 4 step illustration.

Each builds the hardware only. The Hebrew callouts, arrows and highlight rings are composited
over the render afterwards as SVG, so the type stays crisp at print size and a wording change
costs no re-render.

Naming: s_<same key the SVG kit uses>, so the two stay in step.
"""
import math
import lib as L
import p4_car as C
import tools as T
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
    T.craft_knife(96, 30, 3.0, ang=6, tilt=-14)
    L.camera((150, 105, 0), 620, azimuth=40, elevation=42, lens=62)


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
    T.glue_gun(212, 214, C.PLATE_T, ang=-152)
    L.anchor('gun', (250, 236, C.PLATE_T + 22))
    L.anchor('beads', (mx + 34, my + 12, C.PLATE_T + 2))
    L.camera((150, 120, 0), 680, azimuth=36, elevation=32, lens=58)


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
    T.riser(96, 66, C.Z_GROUND - 60)
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


# ---------------------------------------------------------------- a tool rack, for checking
def s_toolcheck():
    """Not a card figure — every tool side by side, at real scale, so shapes can be judged."""
    _studio()
    _bench(0, x0=-20, y0=-20, w=470, d=330)
    T.soldering_iron(30, 42, 12, ang=6)
    T.iron_stand(24, 96, 0)
    T.solder_spool(176, 96, 0)
    T.craft_knife(250, 40, 0, ang=10)
    T.glue_gun(258, 122, 0, ang=16)
    T.goggles(40, 236, 0, ang=-12)
    T.heat_shrink(196, 42, 3, ang=24)
    T.rules_card(226, 232, 0, 72, 54, ang=-6)
    L.camera((208, 132, 24), 760, azimuth=41, elevation=40, lens=56)


# ---------------------------------------------------------------- M1 — the soldering station
def s_soldering_station():
    """Everything laid out and named before the iron is switched on — and the iron itself
    parked in its coil, which is the whole point of the card."""
    _studio()
    _bench(0, x0=-10, y0=-10, w=400, d=290)
    T.heat_mat(20, 24, 0, 250, 190)
    T.iron_stand(30, 40, 1.4)
    # resting in the coil: nose down into the holder, handle up and back
    T.soldering_iron(52, 76, 74, ang=-24, tilt=34)
    T.solder_spool(214, 52, 1.4)
    T.goggles(178, 168, 1.4, ang=-16)
    T.rules_card(276, 150, 1.4, 74, 56, ang=-8)
    L.anchor('iron', (108, 62, 56))
    L.anchor('sponge', (58, 100, 12))
    L.anchor('solder', (214, 52, 62))
    L.anchor('goggles', (237, 183, 14))
    L.anchor('rules', (313, 178, 2))
    L.camera((168, 104, 22), 700, azimuth=44, elevation=36, lens=58)


# ---------------------------------------------------------------- M2 — solder the motor leads
def s_solder_motor_leads():
    """One motor on the mat, iron on the pad, the two leads going on."""
    _studio()
    _bench(0, x0=-20, y0=-20, w=430, d=300)
    T.heat_mat(20, 30, 0, 230, 180)
    C.ensure()
    mx, my, mz = 70, 96, 1.4
    box(mx, my, mz, C.MOTOR_W, C.MOTOR_D, C.MOTOR_H, C.M['motor_yellow'], bevel=1.2, name='motor')
    cyl(mx + C.MOTOR_W - 24, my + C.MOTOR_D / 2, mz + C.MOTOR_H / 2, 9.6, 24,
        C.M['motor_can'], axis='x', name='can')
    # the two copper tabs on the can's end face
    for i in range(2):
        box(mx + C.MOTOR_W + 1, my + 6 + i * 9, mz + 9, 3, 5, 1.4,
            mat('pad_cu', hexcol('#b87333'), rough=0.34, metal=1.0), bevel=0.2, name='pad')
    L.tube([(mx + C.MOTOR_W + 4, my + 8, mz + 10), (mx + C.MOTOR_W + 60, my - 6, mz + 6),
            (mx + C.MOTOR_W + 130, my - 20, mz + 2)], 1.2, C.M['w_red'], name='lead_red')
    L.tube([(mx + C.MOTOR_W + 4, my + 17, mz + 10), (mx + C.MOTOR_W + 60, my + 34, mz + 6),
            (mx + C.MOTOR_W + 130, my + 52, mz + 2)], 1.2, C.M['w_black'], name='lead_black')
    T.soldering_iron(mx + C.MOTOR_W + 12, my + 12, mz + 16, ang=24, tilt=14)
    T.heat_shrink(96, 208, 1.4, 20, 2.4, ang=-8)
    T.solder_spool(300, 40, 1.4)
    L.anchor('pads', (mx + C.MOTOR_W + 3, my + 12, mz + 11))
    L.anchor('shrink', (106, 208, 5))
    L.anchor('motor', (mx + 28, my + 12, mz + C.MOTOR_H))
    L.camera((170, 110, 16), 620, azimuth=34, elevation=34, lens=60)


# ---------------------------------------------------------------- a plain hero, for checking
def s_hero():
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=True)
    C.car()
    L.camera(CAR_CENTRE, 560, azimuth=38, elevation=28, lens=60)
