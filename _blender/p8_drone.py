"""p8_drone.py — the Project 8 tiny quadcopter as real 3D geometry.

Every dimension here is the one Arduino_Projects/_illustration_kit/parts_p8.py draws with, which
is itself traced to Arduino_Projects/Project_8_Tiny_Quadcopter/Arduino_Project_8.md. Nothing in
this file is invented; if the brief moves, both move together.

  frame    FEICHAO/JMT hollow-cup carbon, 100 mm wheelbase, two 1.5 mm plates on standoffs,
           rubber grommets in the four arm rings. Flown PLUS-style: one arm points FRONT.
  motors   4 x 8520 coreless (8.5 x 20 mm), press-fit shaft-up through the grommets.
           CW motors carry RED(+)/BLUE(-) leads; CCW motors carry WHITE(+)/BLACK(-).
  spin     opposite arms spin the SAME way — FRONT+BACK = CW, RIGHT+LEFT = CCW.
  props    65 mm, 1.0 mm bore; each prop matches its own motor's direction.
  stack    top plate carries the DevKit (micro-USB facing the BACK arm), the MT3608 and the
           MPU6050 (X arrow pointing at the FRONT motor).
           UNDER the bottom plate: the MOSFET perfboard, and below that the LiPo.
  gpio     FRONT=25 yellow, RIGHT=26 orange, BACK=14 green, LEFT=27 blue; SDA=21, SCL=22.
  power    LiPo -> board BAT+/GND (star ground) -> MT3608 IN -> OUT 5.0 V -> DevKit VIN.
           Motors run DIRECTLY off the 1S cell. Nothing ever feeds the DevKit's 3V3 pin.

The one rule that cost a whole adversarial review to learn: a motor's '+' lands on the BAT+
rail, its '-' on the Drain pad, and a GATE wire lands on G1..G4 — never on a motor pad. The pad
offsets below are named for exactly that reason, so no scene can put a GPIO on raw battery
positive by writing a slightly wrong number.
"""
import math
import lib as L
from lib import MM, box, cyl, prism, prism_xz, tube, revolve, mat, hexcol

# ---------------------------------------------------------------- canonical geometry (mm)
CTR_X, CTR_Y = 150.0, 112.0
ARM_R = 50.0
PLATE_T = 1.5
BODY_W, BODY_D = 46.0, 34.0
ARM_W_ROOT, ARM_W_TIP = 13.0, 10.5
RING_RO, RING_RI = 6.8, 4.35
GROMMET_H = 3.2
MOTOR_R, MOTOR_H = 4.25, 20.0
FOOT_H = 3.0
SHAFT_R, SHAFT_H = 0.5, 5.0
PROP_R, PROP_HUB = 32.5, 3.4
STACK_H = 15.0

POS = {
    'front': (CTR_X - ARM_R, CTR_Y),
    'back':  (CTR_X + ARM_R, CTR_Y),
    'left':  (CTR_X, CTR_Y - ARM_R),
    'right': (CTR_X, CTR_Y + ARM_R),
}
ARM_ANGLE = {'front': 180.0, 'back': 0.0, 'left': 270.0, 'right': 90.0}
SPIN = {'front': 'cw', 'back': 'cw', 'left': 'ccw', 'right': 'ccw'}
GPIO = {'front': 25, 'right': 26, 'back': 14, 'left': 27}
CHANNEL = {'front': 1, 'right': 2, 'back': 3, 'left': 4}

DEVKIT_W, DEVKIT_D, DEVKIT_T = 51.5, 28.3, 1.4
MOSFET_W, MOSFET_D, MOSFET_T = 50.0, 40.0, 1.6
CH_PITCH, CH_X0 = 11.4, 3.5
PAD_MPLUS_DY = 3.4                 # motor '+' — sits on the BAT+ rail
PAD_MMINUS_DY = 7.6                # motor '-' — the Drain side, NOT ground
PAD_GATE_DY = 32.6                 # G1..G4, between the gate legs and the GND rail
RAIL_BAT_DY, RAIL_GND_DY = 2.4, MOSFET_D - 4.2
MT_W, MT_D, MT_T = 36.0, 17.0, 1.4
IMU_W, IMU_D, IMU_T = 21.2, 15.7, 1.2
BAT_W, BAT_D, BAT_H = 52.0, 30.0, 9.0
FOAM_T = 2.0

Z_PLATE = 0.0
Z_PLATE_TOP = PLATE_T
Z_TOPPLATE = STACK_H
Z_DECK = STACK_H + PLATE_T
Z_MOSFET = -(FOAM_T + MOSFET_T)
Z_BAT = -15.5
Z_CAN = Z_PLATE_TOP + 5.2 - MOTOR_H
Z_FOOT = Z_CAN - FOOT_H
Z_SHAFT = Z_CAN + MOTOR_H
Z_PROP = Z_SHAFT + 1.4

DEVKIT_XY = (CTR_X - DEVKIT_W / 2, CTR_Y - DEVKIT_D / 2)
MOSFET_XY = (CTR_X - MOSFET_W / 2, CTR_Y - MOSFET_D / 2)
MT_XY = (CTR_X - MT_W / 2 + 2, CTR_Y - MT_D / 2 - 25)
IMU_XY = (CTR_X - IMU_W / 2, CTR_Y + 23)
BAT_XY = (CTR_X - BAT_W / 2, CTR_Y - BAT_D / 2)

SIG_COL = {'front': 'w_yellow', 'right': 'w_orange', 'back': 'w_green', 'left': 'w_blue'}
LEAD_COL = {'cw': ('w_red', 'w_blue'), 'ccw': ('w_white', 'w_black')}


# ---------------------------------------------------------------- materials
M = None


def materials():
    return dict(
        carbon=mat('d_carbon', hexcol('#4d5766'), rough=0.34, clearcoat=0.5, cc_rough=0.16),
        grommet=mat('d_grommet', hexcol('#15181c'), rough=0.88),
        can=mat('d_can', hexcol('#ccd1d7'), rough=0.26, metal=1.0),
        bell=mat('d_bell', hexcol('#8f959c'), rough=0.36, metal=0.9),
        shaft=mat('d_shaft', hexcol('#b9bec6'), rough=0.2, metal=1.0),
        foot=mat('d_foot', hexcol('#1b1f24'), rough=0.9),
        prop_cw=mat('d_prop_cw', hexcol('#20262e'), rough=0.42, clearcoat=0.25),
        prop_ccw=mat('d_prop_ccw', hexcol('#8c2b36'), rough=0.42, clearcoat=0.25),
        pcb_esp=mat('d_esp', hexcol('#23262b'), rough=0.5, clearcoat=0.3, cc_rough=0.32),
        perf=mat('d_perf', hexcol('#0f6b3f'), rough=0.5, clearcoat=0.3, cc_rough=0.32),
        to220=mat('d_to220', hexcol('#16191d'), rough=0.5),
        mt=mat('d_mt', hexcol('#1d5fa8'), rough=0.48, clearcoat=0.35, cc_rough=0.3),
        imu=mat('d_imu', hexcol('#1f4e9c'), rough=0.48, clearcoat=0.35, cc_rough=0.3),
        lipo=mat('d_lipo', hexcol('#2f3540'), rough=0.55, clearcoat=0.2),
        foam=mat('d_foam', hexcol('#c8ccd2'), rough=0.95),
        standoff=mat('d_standoff', hexcol('#aeb4bb'), rough=0.3, metal=1.0),
        gold=mat('d_gold', hexcol('#caa03a'), rough=0.3, metal=1.0),
        header=mat('d_header', hexcol('#14171b'), rough=0.44),
        shield=mat('d_shield', hexcol('#b4b9c0'), rough=0.36, metal=0.95),
        alu=mat('d_alu', hexcol('#c8ccd1'), rough=0.26, metal=1.0),
        solder=mat('d_solder', hexcol('#aeb4bb'), rough=0.24, metal=1.0),
        mark=mat('d_mark', hexcol('#e0651a'), rough=0.7),
        led_blue=mat('d_led', hexcol('#2f6fd0'), rough=0.3, emission=hexcol('#3a7fe0'),
                     emission_strength=2.4),
        w_red=mat('d_w_red', hexcol('#cc1414'), rough=0.5),
        w_black=mat('d_w_black', hexcol('#22262b'), rough=0.55),
        w_blue=mat('d_w_blue', hexcol('#418dd9'), rough=0.5),
        w_white=mat('d_w_white', hexcol('#e9edf2'), rough=0.5),
        w_yellow=mat('d_w_yellow', hexcol('#e0b400'), rough=0.5),
        w_orange=mat('d_w_orange', hexcol('#f28a00'), rough=0.5),
        w_green=mat('d_w_green', hexcol('#25cc35'), rough=0.5),
        w_grey=mat('d_w_grey', hexcol('#9aa3ad'), rough=0.5),
        tether=mat('d_tether', hexcol('#d8d2c4'), rough=0.85),
    )


def ensure():
    global M
    if M is None:
        M = materials()
    return M


def reset():
    global M
    M = None


def _group(objs, name):
    import bpy
    g = bpy.data.objects.new(name, None)
    g.empty_display_size = 0.01
    import bpy as _b
    _b.context.collection.objects.link(g)
    for o in objs:
        if o is not None and o.parent is None:
            o.parent = g
    return g


# ---------------------------------------------------------------- the frame
def _arm_outline(which):
    rx, ry = POS[which]
    hr, ht = ARM_W_ROOT / 2, ARM_W_TIP / 2
    if which in ('front', 'back'):
        bx = CTR_X - BODY_W / 2 if which == 'front' else CTR_X + BODY_W / 2
        return [(bx, CTR_Y - hr), (rx, ry - ht), (rx, ry + ht), (bx, CTR_Y + hr)]
    by = CTR_Y - BODY_D / 2 if which == 'left' else CTR_Y + BODY_D / 2
    return [(CTR_X - hr, by), (rx - ht, ry), (rx + ht, ry), (CTR_X + hr, by)]


def _body_outline(w, d, cut=6.0):
    x0, x1 = CTR_X - w / 2, CTR_X + w / 2
    y0, y1 = CTR_Y - d / 2, CTR_Y + d / 2
    return [(x0 + cut, y0), (x1 - cut, y0), (x1, y0 + cut), (x1, y1 - cut),
            (x1 - cut, y1), (x0 + cut, y1), (x0, y1 - cut), (x0, y0 + cut)]


def _ring(x, y, z, ro, ri, h, m, name='ring'):
    """A flat annulus as ONE mesh, so the ink pass draws two circles rather than a heap of
    little arcs. lib.ribbon round a circle is exactly this shape."""
    pts = L.ellipse_pts(x, y, (ro + ri) / 2, (ro + ri) / 2, n=48)
    return L.ribbon(pts, ro - ri, z + h, m, name=name, closed=True, thickness=h)


def frame(z=0.0, top_plate=True, grommets=True, front_mark=False, standoffs=True):
    """The carbon airframe. front_mark paints the teacher's stripe on the FRONT arm, which is
    the only thing that tells a student which way the drone is pointing once it is on the floor."""
    m = ensure()
    out = []
    for which in POS:
        out.append(prism(_arm_outline(which), z, PLATE_T, m['carbon'], name='arm', bevel=0.2))
        rx, ry = POS[which]
        out.append(_ring(rx, ry, z, RING_RO, RING_RI, PLATE_T, m['carbon'], name='armring'))
    out.append(prism(_body_outline(BODY_W, BODY_D), z, PLATE_T, m['carbon'],
                     name='body', bevel=0.2))
    if grommets:
        for which in POS:
            rx, ry = POS[which]
            out.append(_ring(rx, ry, z - 0.85, RING_RI + 0.9, RING_RI - 0.35, GROMMET_H,
                             m['grommet'], name='grommet'))
    if front_mark:
        fx, fy = POS['front']
        out.append(box(fx + 8, CTR_Y - ARM_W_TIP / 2, z + PLATE_T, 12, ARM_W_TIP, 0.4,
                       m['mark'], bevel=0, name='frontmark'))
    if standoffs:
        for sx in (CTR_X - 17, CTR_X + 17):
            for sy in (CTR_Y - 12, CTR_Y + 12):
                out.append(cyl(sx, sy, z + PLATE_T, 1.6, STACK_H - PLATE_T, m['standoff'],
                               name='standoff', seg=20))
    if top_plate:
        out.append(prism(_body_outline(BODY_W, BODY_D), z + Z_TOPPLATE, PLATE_T, m['carbon'],
                         name='topplate', bevel=0.2))
    return out


# ---------------------------------------------------------------- motors and props
def motor(which=None, x=None, y=None, z=0.0, spin='cw', leads=True, lift=0.0):
    """One 8520 coreless can, shaft up, on its rubber foot. `lift` floats it above its ring for
    the press-fit figure, where the whole point is that the motor is not seated yet."""
    m = ensure()
    if which is not None:
        x, y = POS[which]
        spin = SPIN[which]
    zc = z + Z_CAN + lift
    out = [cyl(x, y, zc, MOTOR_R, MOTOR_H, m['can'], name='can', seg=40),
           cyl(x, y, zc + MOTOR_H - 3.4, MOTOR_R + 0.35, 3.4, m['bell'], name='bell', seg=40),
           cyl(x, y, zc - FOOT_H, MOTOR_R + 0.9, FOOT_H, m['foot'], name='foot', seg=32),
           cyl(x, y, zc + MOTOR_H, SHAFT_R, SHAFT_H, m['shaft'], name='shaft', seg=16)]
    if leads:
        plus, minus = LEAD_COL[spin]
        for i, col in enumerate((plus, minus)):
            o = (i - 0.5) * 1.8
            out.append(tube([(x + o, y - MOTOR_R + 0.4, zc + 1.6),
                             (x + o * 3, y - MOTOR_R - 8, zc - 1),
                             (x + o * 4, y - MOTOR_R - 22, zc - 4)],
                            0.55, m[col], name='lead'))
    return out


def prop(which=None, x=None, y=None, z=0.0, cw=True, lift=0.0, phase=0.0):
    """A 65 mm two-blade prop. The blade has a real planform and a real pitch: a flat paddle
    reads as a lolly stick and gives a student nothing to match a spin direction against."""
    m = ensure()
    if which is not None:
        x, y = POS[which]
        cw = SPIN[which] == 'cw'
    zp = z + Z_PROP + lift
    mat_ = m['prop_cw'] if cw else m['prop_ccw']
    out = [cyl(x, y, zp, PROP_HUB, 3.0, mat_, name='prop_hub', seg=28),
           cyl(x, y, zp, 0.5, 3.2, m['shaft'], name='prop_bore', seg=12)]
    plan = [(PROP_HUB, -2.0), (10, -4.4), (18, -5.2), (26, -4.2), (30.5, -2.2),
            (PROP_R, 0.0), (30.5, 1.8), (24, 3.4), (14, 3.2), (PROP_HUB, 1.8)]
    for k in range(2):
        a = math.radians(phase + k * 180.0)
        blade = prism(plan, 0, 0.7, mat_, name='blade', bevel=0.15)
        # pitch first, about the blade's own long axis, then swing it round the hub
        blade.rotation_euler = (math.radians(15 if cw else -15), 0, a)
        blade.location = (x * MM, y * MM, (zp + 1.4) * MM)
        out.append(blade)
    return out


def motors_all(z=0.0, leads=True, props=False):
    out = []
    for which in POS:
        out += motor(which, z=z, leads=leads)
        if props:
            out += prop(which, z=z)
    return out


# ---------------------------------------------------------------- the boards
def _header(x0, y0, z, n, m, along='x'):
    mm = ensure()
    span = n * 2.54
    out = []
    if along == 'x':
        out.append(box(x0 - 0.2, y0 - 0.2, z, span, 2.54, 2.5, m, bevel=0.2, name='hdr'))
    else:
        out.append(box(x0 - 0.2, y0 - 0.2, z, 2.54, span, 2.5, m, bevel=0.2, name='hdr'))
    for i in range(n):
        dx, dy = (i * 2.54, 0) if along == 'x' else (0, i * 2.54)
        out.append(box(x0 + dx + 0.75, y0 + dy + 0.75, z + 2.5, 0.64, 0.64, 3.0,
                       mm['gold'], bevel=0, name='hdr_pin'))
    return out


def devkit(z=None, x=None, y=None, dz=0.0):
    """The ESP32 DevKit on the top plate, micro-USB facing the BACK arm (+x) so a cable never
    fouls the front prop."""
    m = ensure()
    x = DEVKIT_XY[0] if x is None else x
    y = DEVKIT_XY[1] if y is None else y
    zt = (Z_DECK if z is None else z) + dz
    w, d, t = DEVKIT_W, DEVKIT_D, DEVKIT_T
    out = [box(x, y, zt, w, d, t, m['pcb_esp'], bevel=0.5, name='devkit')]
    zb = zt + t
    out.append(box(x + w - 6.5, y + d / 2 - 4.0, zb, 7.5, 8.0, 3.0, m['alu'],
                   bevel=0.4, name='usb'))
    out.append(box(x + 0.0, y + 5.15, zb, 25.5, 18.0, 0.8, m['header'], bevel=0.2, name='wroom'))
    out.append(box(x + 7.5, y + 5.15, zb + 0.8, 18.0, 18.0, 2.4, m['shield'],
                   bevel=0.4, name='can'))
    for i in range(5):
        out.append(box(x + 0.5, y + 7.5 + i * 2.6, zb + 0.8, 5.0, 1.1, 0.12, m['gold'],
                       bevel=0, name='ant'))
    out += _header(x + 5.5, y + 0.6, zt + t, 15, m['header'])
    out += _header(x + 5.5, y + d - 3.2, zt + t, 15, m['header'])
    out.append(box(x + 29, y + d / 2 - 0.8, zb, 2.4, 1.6, 1.0, m['led_blue'], bevel=0,
                   name='led'))
    return out


def mosfet_board(z=None, x=None, y=None, channels=4, foam=True, dz=0.0, up=False):
    """The MOSFET perfboard, hung under the bottom plate with its solder side against the
    carbon. `channels` is how many are built — the T2 cards solder them one at a time.

    Every landing point on this board comes from a NAMED offset. That is not tidiness: a gate
    wire that drifts onto the BAT+ rail wires a GPIO straight to raw battery positive, which is
    exactly the defect an adversarial pass found in the first version of these figures."""
    m = ensure()
    x = MOSFET_XY[0] if x is None else x
    y = MOSFET_XY[1] if y is None else y
    zt = (Z_MOSFET if z is None else z) + dz
    out = []
    if foam:
        out.append(box(x + 4, y + 4, zt + MOSFET_T, MOSFET_W - 8, MOSFET_D - 8, FOAM_T,
                       m['foam'], bevel=0.3, name='foam'))
    out.append(box(x, y, zt, MOSFET_W, MOSFET_D, MOSFET_T, m['perf'], bevel=0.4, name='perf'))
    # On the aircraft the board hangs solder-side to the carbon, so the components face DOWN and
    # a figure looking at the drone from above sees a blank green rectangle. On the bench the
    # same board is the subject of the card, so `up` turns the component side toward the camera.
    if up:
        zb, sgn = zt + MOSFET_T + 0.1, 1.0
    else:
        zb, sgn = zt - 0.1, -1.0
    # the two rails: BAT+ along one edge, star GND along the other
    out.append(box(x + 1.5, y + RAIL_BAT_DY, zb + sgn * 0.4 - (0.5 if up else 0.9),
                   MOSFET_W - 3, 1.8, 0.5, m['solder'], bevel=0, name='rail_bat'))
    out.append(box(x + 1.5, y + RAIL_GND_DY, zb + sgn * 0.4 - (0.5 if up else 0.9),
                   MOSFET_W - 3, 1.8, 0.5, m['solder'], bevel=0, name='rail_gnd'))
    for ch in range(channels):
        cx = x + CH_X0 + ch * CH_PITCH
        # the TO-220 lying on the board, tab outward, legs toward the gate pads
        out.append(box(cx, y + 14.0, zb if up else zb - 4.6, 10.0, 4.6, 4.6, m['to220'],
                       bevel=0.4, name='to220'))
        out.append(box(cx + 1.4, y + 18.4, zb + (4.0 if up else -4.0), 7.2, 6.0, 0.8,
                       m['shield'], bevel=0.2, name='tab'))
        for leg in range(3):
            out.append(box(cx + 1.6 + leg * 3.2, y + 10.0, zb + (1.9 if up else -2.4),
                           0.8, 4.2, 0.5, m['gold'], bevel=0, name='leg'))
        # the flyback diode, band toward the BAT+ rail
        out.append(cyl(cx + 5, y + 22.0, zb, 1.3, 5.5, m['header'], axis='y', name='diode',
                       seg=16))
        out.append(cyl(cx + 5, y + 22.0, zb, 1.4, 0.9, m['w_white'], axis='y', name='band',
                       seg=16))
        for dy, nm in ((PAD_MPLUS_DY, 'pad_mplus'), (PAD_MMINUS_DY, 'pad_mminus'),
                       (PAD_GATE_DY, 'pad_gate')):
            out.append(cyl(cx + 5, y + dy, zb - (0.0 if up else 0.5), 1.5, 0.5, m['solder'],
                           name=nm, seg=16))
    return out


def mt3608(z=None, x=None, y=None, dz=0.0):
    """The step-up that makes 5.0 V for the DevKit. The trim pot is the part the student turns
    while watching a meter, so it has to be findable."""
    m = ensure()
    x = MT_XY[0] if x is None else x
    y = MT_XY[1] if y is None else y
    zt = (Z_DECK if z is None else z) + dz
    return [box(x, y, zt, MT_W, MT_D, MT_T, m['mt'], bevel=0.4, name='mt3608'),
            cyl(x + 17, y + 6, zt + MT_T, 4.6, 4.4, m['header'], name='mt_coil', seg=24),
            cyl(x + 29, y + 12, zt + MT_T, 2.6, 4.0, m['mark'], name='mt_pot', seg=20),
            box(x + 2, y + 2, zt + MT_T, 4.0, 4.0, 3.6, m['alu'], bevel=0.3, name='mt_capin'),
            box(x + 30, y + 2, zt + MT_T, 4.0, 4.0, 3.6, m['alu'], bevel=0.3, name='mt_capout')]


def mpu6050(z=None, x=None, y=None, dz=0.0, arrow=True):
    """The IMU, silk-screen X arrow pointing at the FRONT motor. Mounted the other way round,
    every correction the drone makes is backwards — so the arrow is real geometry here."""
    m = ensure()
    x = IMU_XY[0] if x is None else x
    y = IMU_XY[1] if y is None else y
    zt = (Z_DECK if z is None else z) + dz
    out = [box(x, y, zt, IMU_W, IMU_D, IMU_T, m['imu'], bevel=0.35, name='mpu'),
           box(x + 7.6, y + 5.4, zt + IMU_T, 4.0, 4.0, 0.9, m['header'], bevel=0.2, name='imu_ic')]
    out += _header(x + 3.0, y + IMU_D - 3.0, zt + IMU_T, 8, m['header'])
    if arrow:
        out.append(box(x + 2.4, y + 1.6, zt + IMU_T, 9.0, 1.2, 0.12, m['mark'], bevel=0,
                       name='imu_arrow'))
        out.append(box(x + 1.2, y + 0.6, zt + IMU_T, 2.6, 3.2, 0.12, m['mark'], bevel=0,
                       name='imu_head'))
    return out


def lipo(z=None, x=None, y=None, dz=0.0, orings=True):
    m = ensure()
    x = BAT_XY[0] if x is None else x
    y = BAT_XY[1] if y is None else y
    zt = (Z_BAT if z is None else z) + dz
    out = [box(x, y, zt, BAT_W, BAT_D, BAT_H, m['lipo'], bevel=1.4, name='lipo'),
           box(x + BAT_W - 2, y + BAT_D / 2 - 5, zt + 2, 6.0, 10.0, 4.0, m['w_white'],
               bevel=0.6, name='lipo_plug')]
    for i, col in enumerate(('w_red', 'w_black')):
        out.append(tube([(x + BAT_W + 3, y + BAT_D / 2 - 2.4 + i * 4.8, zt + 4),
                         (x + BAT_W + 12, y + BAT_D / 2 + (i - 0.5) * 10, zt + 7),
                         (x + BAT_W - 6, y + BAT_D + 6, Z_MOSFET - 1)],
                        0.9, m[col], name='lipo_lead'))
    if orings:
        for ox in (x + 8, x + BAT_W - 8):
            r = L.ribbon(L.ellipse_pts(ox, y + BAT_D / 2, 2.2, BAT_D / 2 + 5, n=40),
                         3.0, zt + BAT_H + 3, m['grommet'], name='oring', closed=True,
                         thickness=BAT_H + 6)
            out.append(r)
    return out


# ---------------------------------------------------------------- wiring
def gate_wires(z=0.0, only=None):
    """z lifts the whole harness with the aircraft — every scene here sits on a bench below the origin.

    Four signal wires, DevKit GPIO to G1..G4. They land on PAD_GATE_DY and nowhere else."""
    m = ensure()
    out = []
    dx, dy = DEVKIT_XY
    mx, my = MOSFET_XY
    for i, which in enumerate(('front', 'right', 'back', 'left')):
        if only and which not in only:
            continue
        ch = CHANNEL[which] - 1
        gx = mx + CH_X0 + ch * CH_PITCH + 5
        gy = my + PAD_GATE_DY
        px = dx + 8 + i * 2.9
        py = dy + DEVKIT_D - 1.4
        # The harness leaves the far header, sweeps round the NEAR side of the aircraft and
        # only then dives under the plate. Run straight from header to pad it disappears
        # between two sheets of dark carbon, and the four wires this card is about cannot be
        # seen at all. 0.9 mm rather than 0.55: at 1800 px a 1.1 mm wire is about six pixels
        # wide and the ink contour eats most of them, so the colour — which is how a student
        # tells 25 from 27 — is lost.
        out.append(tube([(px, py, z + Z_DECK + DEVKIT_T + 4),
                         (px - 8 - i * 3, py + 9, z + Z_DECK + 15 - i * 1.4),
                         (CTR_X - 30 - i * 4, CTR_Y - 42 - i * 2, z + Z_PLATE_TOP + 7),
                         (gx, gy, z + Z_MOSFET - 1)], 0.9, m[SIG_COL[which]], name='gate'))
    return out


def i2c_wires(z=0.0):
    m = ensure()
    dx, dy = DEVKIT_XY
    ix, iy = IMU_XY
    out = []
    for i, col in enumerate(('w_white', 'w_grey')):
        out.append(tube([(dx + 30 + i * 2.9, dy + DEVKIT_D - 1.4, z + Z_DECK + DEVKIT_T + 4),
                         (dx + 36 + i * 3, dy + DEVKIT_D + 9, z + Z_DECK + 15 - i * 1.4),
                         (ix + 6 + i * 2.54, iy + IMU_D - 1.4, z + Z_DECK + IMU_T + 4)],
                        0.75, m[col], name='i2c'))
    return out


def power_tree(z=0.0, battery=True):
    """LiPo -> board rails -> MT3608 IN -> OUT 5 V -> DevKit VIN. One star ground.
    Nothing here ever touches the DevKit's 3V3 pin, and the figure must not suggest it does."""
    m = ensure()
    mx, my = MOSFET_XY
    tx, ty = MT_XY
    dx, dy = DEVKIT_XY
    out = []
    # board BAT+ / GND up to the MT3608 input
    out.append(tube([(mx + 4, my + RAIL_BAT_DY, z + Z_MOSFET - 1),
                     (mx - 6, my - 8, z + Z_PLATE + 4),
                     (tx + 2, ty + 2, z + Z_DECK + 3)], 0.8, m['w_red'], name='pwr_in'))
    out.append(tube([(mx + 4, my + RAIL_GND_DY, z + Z_MOSFET - 1),
                     (mx - 8, my + MOSFET_D + 6, z + Z_PLATE + 4),
                     (tx + 2, ty + MT_D - 2, z + Z_DECK + 3)], 0.8, m['w_black'], name='gnd_in'))
    # MT3608 output to the DevKit VIN / GND
    out.append(tube([(tx + MT_W - 2, ty + 2, z + Z_DECK + 3),
                     (dx + DEVKIT_W - 6, dy - 6, z + Z_DECK + 7),
                     (dx + DEVKIT_W - 9, dy + 1.4, z + Z_DECK + DEVKIT_T + 4)],
                    0.8, m['w_red'], name='vin'))
    out.append(tube([(tx + MT_W - 2, ty + MT_D - 2, z + Z_DECK + 3),
                     (dx + DEVKIT_W - 14, dy - 8, z + Z_DECK + 7),
                     (dx + DEVKIT_W - 14, dy + 1.4, z + Z_DECK + DEVKIT_T + 4)],
                    0.8, m['w_black'], name='vgnd'))
    if battery:
        out += lipo(dz=z)
    return out


def motor_wires_to_board(z=0.0, only=None):
    """Each motor's '+' to the BAT+ rail and its '-' to that channel's Drain pad. Never the
    other way about, and never onto a gate pad."""
    m = ensure()
    mx, my = MOSFET_XY
    out = []
    for which in POS:
        if only and which not in only:
            continue
        ch = CHANNEL[which] - 1
        cx = mx + CH_X0 + ch * CH_PITCH + 5
        rx, ry = POS[which]
        plus, minus = LEAD_COL[SPIN[which]]
        out.append(tube([(rx, ry - MOTOR_R - 20, z + Z_CAN - 4),
                         ((rx + CTR_X) / 2, (ry + CTR_Y) / 2 - 14, z + Z_MOSFET + 4),
                         (cx, my + PAD_MPLUS_DY, z + Z_MOSFET - 1)], 0.85, m[plus],
                        name='m_plus'))
        out.append(tube([(rx + 2, ry - MOTOR_R - 20, z + Z_CAN - 4),
                         ((rx + CTR_X) / 2 + 4, (ry + CTR_Y) / 2 - 6, z + Z_MOSFET + 2),
                         (cx, my + PAD_MMINUS_DY, z + Z_MOSFET - 1)], 0.85, m[minus],
                        name='m_minus'))
    return out


# ---------------------------------------------------------------- the whole aircraft
def drone(z=0.0, props=False, wiring=True, battery=True, front_mark=True, boards=True):
    """The assembled quadcopter. props defaults OFF because most of the build cards are
    explicitly about working with the props removed — that is the safety habit being taught."""
    out = []
    out += frame(z, front_mark=front_mark)
    out += motors_all(z, leads=wiring, props=props)
    if boards:
        out += devkit(dz=z) + mt3608(dz=z) + mpu6050(dz=z) + mosfet_board(dz=z)
    if wiring:
        out += gate_wires(z) + i2c_wires(z) + power_tree(z, battery=battery)
        out += motor_wires_to_board(z)
    elif battery:
        out += lipo(dz=z)
    return out
