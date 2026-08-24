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
import hand as H
from lib import MM, box, cyl, prism, prism_xz, tube, mat, hexcol

CAR_CENTRE = (148.0, 110.0, -10.0)


def _studio(strength=1.0):
    L.studio(strength=strength)


def _bench(z, x0=-40, y0=-30, w=420, d=320, colour='#a89a88'):
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
    _bench(0, x0=-16, y0=-16, w=350, d=290)
    T.heat_mat(10, 14, 0, 250, 200)
    T.iron_stand(30, 70, 1.4)
    # the iron PARKED IN ITS COIL, which is the safety habit the card is teaching. The coil
    # runs roughly along -y and tips up, so the iron lies along it: tip high and to the back,
    # handle coming down toward the front. Standing it on end taught the opposite lesson.
    T.soldering_iron(86, -5, 75, ang=90, tilt=16)
    T.solder_spool(232, 52, 1.4)
    T.goggles(172, 176, 1.4, ang=-20)
    T.heat_shrink(146, 30, 3.6, ang=18, length=26, r=3.0)
    T.rules_card(218, 118, 1.4, 76, 60, ang=-7)
    L.anchor('iron', (86, 70, 52))
    L.anchor('sponge', (40, 138, 12))
    L.anchor('solder', (232, 52, 62))
    L.anchor('goggles', (216, 184, 18))
    L.anchor('rules', (256, 148, 2))
    L.camera((140, 104, 20), 560, azimuth=44, elevation=36, lens=58)


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
    _bench(-6.5, x0=-60, y0=-50, w=470, d=380)
    sheet = mat('polygal_sheet', hexcol('#bcd0dd'), rough=0.3, transmission=0.34, ior=1.5)
    box(4, 16, -6, 296, 190, 8, sheet, bevel=0.5, name='sheet')
    paper = mat('paper_t', hexcol('#fbf7ec'), rough=0.9)
    box(23.5, 35, 2.2, 250, 150, 0.4, paper, bevel=0, name='template')
    ink = mat('ink', hexcol('#15181c'), rough=0.8)
    for i in range(len(C.OUTLINE)):
        (x1, y1), (x2, y2) = C.OUTLINE[i], C.OUTLINE[(i + 1) % len(C.OUTLINE)]
        ln = math.hypot(x2 - x1, y2 - y1)
        b = box(0, 0, 0, ln, 1.0, 0.15, ink, bevel=0, name='cutline')
        # box() bakes the scale into the mesh and puts the origin at the box CENTRE, so a line
        # placed by its START vertex hangs half its own length past the outline. Place the
        # midpoint. This is the same bug that once turned the M3 template into stray diagonals.
        b.location = ((x1 + x2) / 2 * MM, (y1 + y2) / 2 * MM, 2.72 * MM)
        b.rotation_euler = (0, 0, math.atan2(y2 - y1, x2 - x1))
    # the three zones the template prints — brain, driver, battery
    zone = mat('zone', hexcol('#8fa8bd'), rough=0.85)
    for zx, zy, zw, zd in ((C.BRAIN_X, C.BRAIN_Y, C.BRAIN_W, C.BRAIN_D),
                           (C.DRV_X, C.DRV_Y, C.DRV_W, C.DRV_D),
                           (C.BAT_X, C.BAT_Y, C.BAT_W, C.BAT_D)):
        for ex, ey, ew, ed in ((zx, zy, zw, 0.9), (zx, zy + zd, zw, 0.9),
                               (zx, zy, 0.9, zd), (zx + zw, zy, 0.9, zd)):
            box(ex, ey, 2.66, ew, ed, 0.1, zone, bevel=0, name='zone')
    # the 5 cm check strip the card makes the student measure before anything is cut
    for i in range(6):
        box(196 + i * 10, 156, 2.66, 0.9, 11 if i % 5 == 0 else 7, 0.1, ink,
            bevel=0, name='scale')
    for hx, hy in (C.SENS_L, C.SENS_R):
        cyl(hx, hy, 2.6, 1.9, 0.16, ink, name='drillmark')
    tape = mat('masking', hexcol('#e0c060'), rough=0.8)
    for tx, ty in ((26, 38), (240, 38), (26, 164), (240, 164)):
        box(tx, ty, 2.6, 26, 15, 0.3, tape, bevel=0, name='masktape')
    T.craft_knife(120, 22, 3.0, ang=10, tilt=-14)
    T.ruler(24, 206, 0, ang=-3, length=200)
    L.anchor('knife', (188, 30, 12))
    L.anchor('cutline', (150, 35, 3))
    L.anchor('corner', (23.5, 170, 3))
    L.anchor('scale', (222, 160, 3))
    L.anchor('template', (150, 110, 3))
    L.camera((150, 108, 0), 640, azimuth=40, elevation=46, lens=60)


# ---------------------------------------------------------------- M3b — glue the motors
def s_glue_motors():
    """The plate turned over with the motors going on — SCREWED, two M3x30 apiece.

    This figure used to show a hot-glue bead, which contradicted step 4 of the very card it
    sits in ("screwed, not glued"). A figure that argues with the step above it is worse than
    no figure. The published filename stays as it is, because that is the name the card
    embeds and renaming it would silently drop the picture from the page."""
    _studio()
    _bench(-6.5, x0=-50, y0=-40, w=440, d=340)
    C.ensure()
    C.chassis(z=0.0)
    for pos, side in (('front', 'left'), ('front', 'right'), ('rear', 'left')):
        C.tt_motor(side, pos, z=0.0, leads=False, up=True)
    mx, my = C.MOTOR_RX, C.PLATE_Y1 - C.MOTOR_D
    # the fourth corner still open, its two screws standing in the holes just drilled for them
    for sx in (mx + 9, mx + C.MOTOR_W - 9):
        T.m3_screw(sx, my + C.MOTOR_D / 2, C.PLATE_T + 30, 30, down=True)
    T.screwdriver(mx + C.MOTOR_W - 9, my + C.MOTOR_D / 2, C.PLATE_T + 36, ang=0, tilt=-90)
    T.pencil(288, 56, 0, ang=104)
    L.anchor('screws', (mx + 34, my + 12, C.PLATE_T + 32))
    L.anchor('driver_tool', (mx + C.MOTOR_W - 9, my + 12, C.PLATE_T + 100))
    L.anchor('flipped', (110, 110, C.PLATE_T))
    L.anchor('axles', (C.AXLE_F, C.PLATE_Y0 + 6, -C.MOTOR_H + 6))
    L.camera((156, 118, 20), 720, azimuth=38, elevation=30, lens=58)


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
    L.ground(z=C.Z_GROUND, shadow_only=False, colour='#d6cab6', size=4200)
    _floor_tape(-140, 98, 620, C.Z_GROUND, 24)
    C.car()
    T.laptop(305, 186, C.Z_GROUND, ang=12, lid=102, screen='serial')
    _car_anchors()
    L.anchor('tape', (10, 110, C.Z_GROUND + 1))
    L.anchor('laptop', (388, 316, C.Z_GROUND + 96))
    L.camera((190, 220, -10), 1160, azimuth=48, elevation=28, lens=52)


# ---------------------------------------------------------------- M7 — the first run
def s_first_run():
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=False, colour='#d6cab6', size=4200)
    _floor_tape(-180, 98, 680, C.Z_GROUND, 24)
    C.car()
    _car_anchors()
    L.anchor('ahead', (-40, 110, C.Z_GROUND + 2))
    L.camera(CAR_CENTRE, 790, azimuth=52, elevation=20, lens=60)


# ---------------------------------------------------------------- M8 — the closed track
def s_track():
    """A closed loop of black tape with the car on it: wide turns, no sharp corners."""
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=False, colour='#cec2ad', size=5600)
    tape = mat('tape_black', hexcol('#15181c'), rough=0.7)
    cx, cy, rx, ry = 45.0, 300.0, 268.0, 190.0
    # thickness 0 keeps the loop a flat strip. Solidified, the ink pass outlines its side wall
    # too and a piece of tape on the floor comes out looking like a wire hoop.
    L.ribbon(L.ellipse_pts(cx, cy, rx, ry, n=120), 24.0, C.Z_GROUND + 0.35, tape,
             name='loop', thickness=0.0)
    C.car()
    _car_anchors()
    L.anchor('loop', (cx + rx * 0.7, cy + ry * 0.78, C.Z_GROUND + 2))
    L.anchor('turn', (cx - rx, cy, C.Z_GROUND + 2))
    L.camera((90, 280, -30), 1380, azimuth=48, elevation=40, lens=54)


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


# ---------------------------------------------------------------- checking only
def s_handcheck():
    """Not a card figure — the hand in every pose, at real scale beside a 65 mm wheel, so the
    proportions can be judged before it goes anywhere near a card."""
    _studio(1.05)
    _bench(0, x0=-60, y0=-60, w=560, d=420)
    C.ensure()
    for i, pose in enumerate(('flat', 'point', 'press', 'pinch', 'grip')):
        H.hand(30 + i * 112, 30, 40, ang=84, pitch=-18, pose=pose)
        L.anchor(pose, (30 + i * 112, 150, 40))
    cyl(60, 300, 0, 32.5, 27, C.M['tyre'], axis='y', name='scalecheck', seg=64)
    L.anchor('wheel', (60, 314, 0))
    L.camera((260, 150, 26), 980, azimuth=56, elevation=30, lens=52)
