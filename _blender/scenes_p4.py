"""scenes_p4.py — one function per Project 4 step illustration.

Each builds the hardware only. The Hebrew callouts, arrows and highlight rings are composited
over the render afterwards as SVG, so the type stays crisp at print size and a wording change
costs a re-compose rather than a re-render.

Every scene registers named anchors. render.py projects them to pixel coordinates beside the PNG
and compose.js hangs the callouts on them, so a label lands on a real part and follows the camera
if an angle changes.

Scene keys map onto the figure names the CARDS ALREADY REFERENCE — see PUBLISH in build_p4.sh.
Publishing under a fresh name is exactly how the first attempt failed to reach the cards.
"""
import math
import lib as L
import p4_car as C
import tools as T
from lib import MM, box, cyl, prism, prism_xz, tube, mat, hexcol

CAR_CENTRE = (148.0, 110.0, -10.0)


def _studio(strength=1.0):
    L.studio(strength=strength)


def _bench(z, x0=-40, y0=-30, w=420, d=320, colour='#d8cfbe'):
    """The work surface. Scenes that call this must NOT also add L.ground(): two coplanar
    surfaces z-fight, the shadow catcher wins, and you get a black bench-shaped hole."""
    m = mat('bench', hexcol(colour), rough=0.72)
    return box(x0, y0, z - 7, w, d, 7, m, bevel=1.5, name='bench')


def _floor_tape(x0, y, length, z, width=19.0):
    m = mat('tape_black', hexcol('#15181c'), rough=0.7)
    return box(x0, y, z + 0.05, length, width, 0.25, m, bevel=0, name='tape')


def _car_anchors(z=0.0):
    L.anchor('uno', (C.BRAIN_X + 36, C.BRAIN_Y + 30, z + C.PLATE_T + 4))
    L.anchor('driver', (C.DRV_X + 22, C.DRV_Y + 22, z + C.PLATE_T + 16))
    L.anchor('battery', (C.BAT_X + 55, C.BAT_Y + 30, z + C.PLATE_T + 17))
    L.anchor('plate', (150, 110, z + C.PLATE_T))
    L.anchor('motor_rear', (C.MOTOR_RX + 35, C.PLATE_Y1 - 12, z - C.MOTOR_H / 2))
    L.anchor('wheel_front', (C.AXLE_F, C.PLATE_Y0 - 20, z + C.Z_AXLE))
    L.anchor('sensor_left', (C.SENS_L[0], C.SENS_L[1], z - 10.0))


# ---------------------------------------------------------------- M1 — the soldering station
def s_soldering_station():
    """Everything laid out and named before the iron is switched on, the iron parked in its coil."""
    _studio()
    _bench(0, x0=-10, y0=-10, w=400, d=290)
    T.heat_mat(20, 24, 0, 250, 190)
    T.iron_stand(30, 40, 1.4)
    T.soldering_iron(52, 76, 74, ang=-24, tilt=34)
    T.solder_spool(214, 132, 1.4)
    T.goggles(196, 186, 1.4, ang=-16)
    T.rules_card(238, 66, 1.4, 78, 60, ang=-8)
    L.anchor('iron', (104, 60, 58))
    L.anchor('sponge', (40, 108, 12))
    L.anchor('solder', (214, 132, 62))
    L.anchor('goggles', (255, 201, 14))
    L.anchor('rules', (277, 96, 2))
    L.camera((160, 112, 20), 690, azimuth=44, elevation=36, lens=56)


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
    pad_m = mat('pad_cu', hexcol('#a3672e'), rough=0.34, metal=1.0)
    for i in range(2):
        box(mx + C.MOTOR_W + 1, my + 6 + i * 9, mz + 9, 3, 5, 1.4, pad_m, bevel=0.2, name='pad')
    tube([(mx + C.MOTOR_W + 4, my + 8, mz + 10), (mx + C.MOTOR_W + 60, my - 6, mz + 6),
          (mx + C.MOTOR_W + 130, my - 20, mz + 2)], 1.2, C.M['w_red'], name='lead_red')
    tube([(mx + C.MOTOR_W + 4, my + 17, mz + 10), (mx + C.MOTOR_W + 60, my + 34, mz + 6),
          (mx + C.MOTOR_W + 130, my + 52, mz + 2)], 1.2, C.M['w_black'], name='lead_black')
    T.soldering_iron(mx + C.MOTOR_W + 16, my + 12, mz + 20, ang=26, tilt=16)
    T.heat_shrink(96, 214, 1.4, 20, 2.4, ang=-8)
    T.solder_spool(320, 232, 1.4)
    L.anchor('pads', (mx + C.MOTOR_W + 3, my + 12, mz + 11))
    L.anchor('shrink', (106, 214, 5))
    L.anchor('motor', (mx + 28, my + 12, mz + C.MOTOR_H))
    L.anchor('iron_tip', (mx + C.MOTOR_W + 16, my + 12, mz + 22))
    L.camera((150, 116, 14), 540, azimuth=34, elevation=32, lens=62)


# ---------------------------------------------------------------- M3a — cut the plate
def s_cut_plate():
    """The template taped to a polygal sheet, knife on the line."""
    _studio()
    L.ground(z=-6.5, shadow_only=True)
    sheet = mat('polygal_sheet', hexcol('#c9d8e2'), rough=0.28, transmission=0.42, ior=1.5)
    box(8, 20, -6, 285, 180, 8, sheet, bevel=0.5, name='sheet')
    paper = mat('paper_t', hexcol('#fffdf7'), rough=0.9)
    box(23.5, 35, 2.2, 250, 150, 0.4, paper, bevel=0, name='template')
    ink = mat('ink', hexcol('#15181c'), rough=0.8)
    for i in range(len(C.OUTLINE)):
        (x1, y1), (x2, y2) = C.OUTLINE[i], C.OUTLINE[(i + 1) % len(C.OUTLINE)]
        ln = math.hypot(x2 - x1, y2 - y1)
        b = box(0, -0.5, 0, ln, 1.0, 0.15, ink, bevel=0, name='cutline')
        b.location = (x1 * MM, y1 * MM, 2.65 * MM)
        b.rotation_euler = (0, 0, math.atan2(y2 - y1, x2 - x1))
    tape = mat('masking', hexcol('#e0c060'), rough=0.8)
    for tx, ty in ((28, 40), (244, 40), (28, 166), (244, 166)):
        box(tx, ty, 2.6, 22, 13, 0.3, tape, bevel=0, name='masktape')
    T.craft_knife(128, 16, 3.0, ang=8, tilt=-12)
    L.anchor('knife', (196, 24, 12))
    L.anchor('cutline', (150, 35, 3))
    L.anchor('corner', (23.5, 170, 3))
    L.anchor('template', (238, 120, 3))
    L.camera((150, 105, 0), 720, azimuth=40, elevation=44, lens=58)


# ---------------------------------------------------------------- M3b — glue the motors
def s_glue_motors():
    """The plate turned over, motors going onto what becomes the underside."""
    _studio()
    _bench(-6.5)
    C.ensure()
    C.chassis(z=0.0)
    glue = mat('glue', hexcol('#f2e0b0'), rough=0.3, transmission=0.4, ior=1.45)
    for pos, side in (('front', 'left'), ('front', 'right'), ('rear', 'left')):
        C.tt_motor(side, pos, z=0.0, leads=False)
    mx = C.MOTOR_RX
    my = C.PLATE_Y1 - C.MOTOR_D
    for gx in range(int(mx) + 6, int(mx + C.MOTOR_W) - 4, 10):
        cyl(gx, my + C.MOTOR_D / 2, C.PLATE_T, 3.4, 1.6, glue, name='bead')
    T.glue_gun(268, 258, C.PLATE_T, ang=-140)
    L.anchor('gun', (286, 272, C.PLATE_T + 40))
    L.anchor('beads', (mx + 34, my + 12, C.PLATE_T + 3))
    L.anchor('flipped', (110, 110, C.PLATE_T))
    L.anchor('axles', (C.AXLE_F, C.PLATE_Y0 + 6, -C.MOTOR_H + 6))
    L.camera((162, 140, 0), 800, azimuth=36, elevation=34, lens=56)


# ---------------------------------------------------------------- M3c — rolling chassis
def s_wheels_on():
    _studio()
    _bench(C.Z_GROUND)
    C.ensure()
    C.chassis()
    C.motors_all(leads=False)
    C.wheels_all()
    _car_anchors()
    L.camera(CAR_CENTRE, 660, azimuth=38, elevation=26, lens=58)


# ---------------------------------------------------------------- M4 — the full wiring
def s_wiring():
    _studio()
    _bench(C.Z_GROUND)
    C.car()
    _car_anchors()
    L.anchor('splitter', (94, 68, C.PLATE_T + 8))
    L.anchor('common_gnd', (C.DRV_X + 20, 150, C.PLATE_T + 11))
    L.camera(CAR_CENTRE, 600, azimuth=42, elevation=34, lens=60)


# ---------------------------------------------------------------- M5 — wheels in the air
def s_wheels_in_air():
    _studio()
    _bench(C.Z_GROUND - 60)
    T.riser(96, 66, C.Z_GROUND - 60)
    C.car()
    _car_anchors()
    L.anchor('riser', (151, 110, C.Z_GROUND - 30))
    L.camera(CAR_CENTRE, 650, azimuth=34, elevation=22, lens=58)


# ---------------------------------------------------------------- M6 — the sensor test
def s_sensor_test():
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=False, colour='#f4f1ea', size=1700)
    _floor_tape(-90, 101, 460, C.Z_GROUND)
    C.car()
    T.laptop(300, 250, C.Z_GROUND, ang=-52, lid=98)
    _car_anchors()
    L.anchor('tape', (10, 110, C.Z_GROUND + 1))
    L.anchor('laptop', (392, 316, C.Z_GROUND + 52))
    L.camera((214, 176, -14), 940, azimuth=46, elevation=30, lens=54)


# ---------------------------------------------------------------- M7 — the first run
def s_first_run():
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=False, colour='#f4f1ea', size=1700)
    _floor_tape(-110, 101, 520, C.Z_GROUND)
    C.car()
    _car_anchors()
    L.anchor('ahead', (-40, 110, C.Z_GROUND + 2))
    L.camera(CAR_CENTRE, 700, azimuth=52, elevation=18, lens=62)


# ---------------------------------------------------------------- M8 — the closed track
def s_track():
    """A closed loop of black tape with the car on it: wide turns, no sharp corners."""
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=False, colour='#f4f1ea', size=2600)
    tape = mat('tape_black', hexcol('#15181c'), rough=0.7)
    cx, cy, rx, ry = 150.0, 320.0, 300.0, 190.0
    n = 96
    for i in range(n):
        a0 = 2 * math.pi * i / n
        a1 = 2 * math.pi * (i + 1) / n
        x0, y0 = cx + rx * math.cos(a0), cy + ry * math.sin(a0)
        x1, y1 = cx + rx * math.cos(a1), cy + ry * math.sin(a1)
        ln = math.hypot(x1 - x0, y1 - y0) * 1.4
        seg = box(0, -9.5, 0, ln, 19, 0.3, tape, bevel=0, name='tapeseg')
        seg.location = (x0 * MM, y0 * MM, (C.Z_GROUND + 0.05) * MM)
        seg.rotation_euler = (0, 0, math.atan2(y1 - y0, x1 - x0))
    C.car()
    _car_anchors()
    L.anchor('loop', (cx + rx * 0.55, cy + ry * 0.85, C.Z_GROUND + 2))
    L.anchor('turn', (cx - rx, cy, C.Z_GROUND + 2))
    L.camera((150, 290, -30), 1450, azimuth=48, elevation=40, lens=54)


# ---------------------------------------------------------------- checking only
def s_toolcheck2():
    """The chassis-build tools, for checking."""
    _studio()
    _bench(0, x0=-20, y0=-20, w=470, d=330)
    T.ruler(20, 30, 0, ang=4)
    T.pencil(40, 90, 4, ang=8)
    T.screwdriver(30, 140, 13, ang=6)
    T.drill(220, 60, 44, ang=18)
    T.tape_roll(70, 250, 0, ang=0)
    T.zip_tie(200, 210, 0, 3, 60, 18)
    for i in range(3):
        T.m3_screw(160 + i * 12, 160, 0, 30)
        T.m3_nut(160 + i * 12, 176, 0)
    L.camera((208, 132, 24), 760, azimuth=41, elevation=40, lens=56)


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


def s_hero():
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=True)
    C.car()
    L.camera(CAR_CENTRE, 560, azimuth=38, elevation=28, lens=60)
