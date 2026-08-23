"""parts_p8.py — the physical parts of the Project 8 tiny quadcopter, drawn isometrically at
their real millimetre sizes and in their real places on the airframe.

Every dimension, colour and orientation here traces to
Arduino_Projects/Project_8_Tiny_Quadcopter/Arduino_Project_8.md. The load-bearing ones:

  frame    FEICHAO/JMT hollow-cup carbon, 100 mm wheelbase, two 1.5 mm plates on metal standoffs,
           rubber grommets in the four arm rings. Flown PLUS-style: one arm points FRONT.
  motors   4x 8520 coreless (8.5 x 20 mm), press-fit shaft-up through the grommets.
           CW motors carry RED(+)/BLUE(-) leads; CCW motors carry WHITE(+)/BLACK(-).
  spin     opposite arms spin the SAME way — FRONT+BACK = CW, RIGHT+LEFT = CCW.
  props    65 mm, 1.0 mm bore; each prop matches its own motor's direction.
  stack    top plate carries the DevKit (micro-USB facing the BACK arm), the MT3608 and the
           MPU6050 (silk-screen X arrow pointing at the FRONT motor).
           UNDER the bottom plate: the MOSFET perfboard (solder side to the carbon, components
           facing down), and below that the LiPo, held by two frame O-rings.
  gpio     FRONT=25 yellow, RIGHT=26 orange, BACK=14 green, LEFT=27 blue; SDA=21 white, SCL=22 grey.
  power    LiPo -> board BAT+/GND (star ground) -> MT3608 IN -> OUT 5.0 V -> DevKit VIN.
           Motors run DIRECTLY off the 1S cell. Nothing ever feeds the DevKit's 3V3 pin.
"""
import math
from iso import (Scene, iso, depth, cuboid, cyl_x, cyl_y, cyl_z, disc, ring_z, prism, blade,
                 spin_arc, shadow, wire, dupont, arrow, tag, poly, shade)

# ---------------------------------------------------------------- canonical geometry (mm)
CTR_X, CTR_Y = 150.0, 112.0        # frame centre in world coordinates
ARM_R = 50.0                       # motor centre to frame centre (100 mm wheelbase)
PLATE_T = 1.5
BODY_W, BODY_D = 46.0, 34.0        # centre plate footprint
ARM_W_ROOT, ARM_W_TIP = 13.0, 10.5
RING_RO, RING_RI = 6.8, 4.35       # arm ring outer radius / grommet bore (= the motor)
GROMMET_H = 3.2
MOTOR_R, MOTOR_H = 4.25, 20.0      # 8520 coreless can
FOOT_H = 3.0                       # the rubber motor cap that the drone stands on
SHAFT_R, SHAFT_H = 0.5, 5.0
PROP_R, PROP_HUB = 32.5, 3.4       # 65 mm prop, 1.0 mm bore
STACK_H = 15.0                     # standoff length between the two plates

# small x is the NOSE (FRONT), small y is the LEFT side — the same convention the car uses
POS = {
    'front': (CTR_X - ARM_R, CTR_Y),
    'back':  (CTR_X + ARM_R, CTR_Y),
    'left':  (CTR_X, CTR_Y - ARM_R),
    'right': (CTR_X, CTR_Y + ARM_R),
}
ARM_ANGLE = {'front': 180.0, 'back': 0.0, 'left': 270.0, 'right': 90.0}
ORDER = ('front', 'left', 'right', 'back')          # far to near, for painter's order

SPIN = {'front': 'cw', 'back': 'cw', 'left': 'ccw', 'right': 'ccw'}
GPIO = {'front': 25, 'right': 26, 'back': 14, 'left': 27}
CHANNEL = {'front': 1, 'right': 2, 'back': 3, 'left': 4}

# ---------------------------------------------------------------- colours
C_CARBON = '#39414d'
C_GROMMET = '#15181c'
C_CAN = '#c2c7cd'
C_BELL = '#8f959c'
C_PROP_CW = '#20262e'
C_PROP_CCW = '#8c2b36'
C_ESP = '#23262b'
C_PERF = '#0f6b3f'
C_TO220 = '#16191d'
C_MT = '#1d5fa8'
C_IMU = '#1f4e9c'
C_LIPO = '#2f3540'
C_FOAM = '#c8ccd2'
RED, BLACK, ORANGE, GREEN, BLUE, YELLOW, WHITE_W, GREY_W = (
    '#cc1414', '#22262b', '#f28a00', '#25cc35', '#418dd9', '#e0b400', '#e9edf2', '#9aa3ad')
HL = '#e0651a'

# the four signal wires, by arm — the colours the brief's pin map specifies
SIG_COL = {'front': YELLOW, 'right': ORANGE, 'back': GREEN, 'left': BLUE}
# CW motors ship with red/blue leads, CCW motors with white/black
LEAD_COL = {'cw': (RED, BLUE), 'ccw': (WHITE_W, BLACK)}

# ---------------------------------------------------------------- board footprints
DEVKIT_W, DEVKIT_D, DEVKIT_T = 51.5, 28.3, 1.4
MOSFET_W, MOSFET_D, MOSFET_T = 50.0, 40.0, 1.6
MT_W, MT_D, MT_T = 36.0, 17.0, 1.4
IMU_W, IMU_D, IMU_T = 21.2, 15.7, 1.2
BAT_W, BAT_D, BAT_H = 52.0, 30.0, 9.0
FOAM_T = 2.0

# ---------------------------------------------------------------- the vertical stack
Z_PLATE = 0.0                      # bottom face of the bottom plate
Z_PLATE_TOP = PLATE_T
Z_TOPPLATE = STACK_H               # bottom face of the top plate
Z_DECK = STACK_H + PLATE_T         # where the DevKit, MT3608 and MPU6050 sit
Z_MOSFET = -(FOAM_T + MOSFET_T)    # bottom face of the perfboard, hung under the plate
Z_BAT = -15.5                      # bottom face of the cell
Z_CAN = Z_PLATE_TOP + 5.2 - MOTOR_H     # bottom of the motor can
Z_FOOT = Z_CAN - FOOT_H                 # the rubber feet the drone stands on
Z_SHAFT = Z_CAN + MOTOR_H
Z_PROP = Z_SHAFT + 1.4

# where each board sits
DEVKIT_XY = (CTR_X - DEVKIT_W / 2, CTR_Y - DEVKIT_D / 2)
MOSFET_XY = (CTR_X - MOSFET_W / 2, CTR_Y - MOSFET_D / 2)
MT_XY = (CTR_X - MT_W / 2 + 2, CTR_Y - MT_D / 2 - 25)
IMU_XY = (CTR_X - IMU_W / 2, CTR_Y + 23)
BAT_XY = (CTR_X - BAT_W / 2, CTR_Y - BAT_D / 2)


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


def frame(sc, z=0.0, top_plate=True, grommets=True, front_mark=False, tether_loop=False, layer=1):
    """The carbon frame. front_mark draws the teacher's paint stripe on the FRONT arm."""
    for which in POS:
        prism(sc, _arm_outline(which), z, PLATE_T, C_CARBON, layer=layer,
              key=depth(*POS[which], z) - 6)
    prism(sc, _body_outline(BODY_W, BODY_D), z, PLATE_T, C_CARBON, layer=layer,
          key=depth(CTR_X, CTR_Y, z) - 5)
    if front_mark:
        fx, fy = POS['front']
        pts = [(fx + 12, fy - 4.6), (fx + 17, fy - 4.6), (fx + 17, fy + 4.6), (fx + 12, fy + 4.6)]
        sc.add(depth(fx + 14, fy, z) + 40,
               poly([iso(px, py, z + PLATE_T + 0.05) for px, py in pts], '#e0651a', None), layer + 1)
    for which, (rx, ry) in POS.items():
        ring_z(sc, rx, ry, z, RING_RO, RING_RI, PLATE_T, C_CARBON, layer=layer)
        if grommets:
            ring_z(sc, rx, ry, z + PLATE_T, RING_RI + 1.5, RING_RI, GROMMET_H, C_GROMMET, layer=layer + 2)
    if tether_loop:
        cyl_z(sc, CTR_X, CTR_Y, z - 11, 11, 0.7, '#c8b28a', layer=layer - 1)
        disc(sc, CTR_X, CTR_Y, z - 11, 3.4, 'none', stroke='#c8b28a', sw=1.1, layer=layer - 1)
    if top_plate:
        for sx in (-1, 1):
            for sy in (-1, 1):
                cyl_z(sc, CTR_X + sx * (BODY_W / 2 - 5), CTR_Y + sy * (BODY_D / 2 - 5),
                      z + PLATE_T, STACK_H - PLATE_T, 1.6, '#9aa0a6', layer=layer + 2)
        prism(sc, _body_outline(BODY_W - 4, BODY_D - 2), z + STACK_H, PLATE_T, C_CARBON,
              layer=layer + 2, key=depth(CTR_X, CTR_Y, z + STACK_H) + 40)


# ---------------------------------------------------------------- motors, props
def coreless_motor(sc, which, z=0.0, leads=True, foot=True, layer=3, lift=0.0, spinning=False):
    """An 8520 coreless motor seated shaft-up in its grommet. lift > 0 holds it above the ring
    for the press-fit step."""
    rx, ry = POS[which]
    zb = z + Z_CAN + lift
    cyl_z(sc, rx, ry, zb, MOTOR_H, MOTOR_R, C_CAN, cap_col=C_BELL, layer=layer)
    cyl_z(sc, rx, ry, zb + MOTOR_H, SHAFT_H, SHAFT_R, '#9aa0a6', layer=layer)
    if foot:
        cyl_z(sc, rx, ry, zb - FOOT_H, FOOT_H, MOTOR_R + 0.9, C_GROMMET, layer=max(0, layer - 3))
    if spinning:
        spin_arc(sc, rx, ry, zb + MOTOR_H + 7, 11, cw=SPIN[which] == 'cw')
    if leads:
        # the two leads run inboard along the underside of the arm to this motor's pad on the
        # MOSFET board, so they stay clear of every prop disc
        ang = math.radians(ARM_ANGLE[which] + 180)
        ca, sa = math.cos(ang), math.sin(ang)
        for i, col in enumerate(LEAD_COL[SPIN[which]]):
            off = (i - 0.5) * 2.4
            sx = rx + ca * (MOTOR_R + 0.2) - sa * off
            sy = ry + sa * (MOTOR_R + 0.2) + ca * off
            wire(sc, [(sx, sy, zb + MOTOR_H * 0.30),
                      (rx + ca * 14 - sa * off, ry + sa * 14 + ca * off, z - 1.2),
                      (rx + ca * 30 - sa * off, ry + sa * 30 + ca * off, z + Z_MOSFET + 0.6)],
                 col, 0.9, layer=2)


def motors_all(sc, z=0.0, leads=True, foot=True, layer=3, spinning=False):
    for which in ORDER:
        coreless_motor(sc, which, z=z, leads=leads, foot=foot, layer=layer, spinning=spinning)


def prop_on(sc, which, z=0.0, spinning=False, layer=5, lift=0.0, hub=True):
    """The 65 mm prop that matches this motor's direction of rotation."""
    rx, ry = POS[which]
    cw = SPIN[which] == 'cw'
    col = C_PROP_CW if cw else C_PROP_CCW
    zt = z + Z_PROP + lift
    if hub:
        cyl_z(sc, rx, ry, zt, 3.2, PROP_HUB, '#1f2329', layer=layer, hole=0.6)
    if spinning:
        # a spinning prop is a blur, not a coloured cloud — the ring keeps the CW/CCW cue
        disc(sc, rx, ry, zt + 2.4, PROP_R, '#8d99a8', extra='fill-opacity:0.13', layer=layer, bump=0.6)
        disc(sc, rx, ry, zt + 2.4, PROP_R, 'none', stroke=col, sw=0.8, layer=layer, bump=0.7)
        spin_arc(sc, rx, ry, zt + 5, PROP_R + 5, cw=cw)
    else:
        for a in (0, 180):
            blade(sc, rx, ry, zt + 2.4, a + (18 if cw else -18), PROP_HUB, PROP_R, col,
                  cw=cw, layer=layer)


def props_all(sc, z=0.0, spinning=False, layer=5):
    for which in ORDER:
        prop_on(sc, which, z=z, spinning=spinning, layer=layer)


# ---------------------------------------------------------------- boards
def _header(sc, x0, y0, z, n, along='x', col='#c9a227', layer=3):
    for i in range(n):
        if along == 'x':
            cuboid(sc, x0 + i * 2.54, y0, z, 1.6, 2.2, 2.2, col, layer=layer)
        else:
            cuboid(sc, x0, y0 + i * 2.54, z, 2.2, 1.6, 2.2, col, layer=layer)


def foam_pad(sc, x, y, z, w, d, layer=3):
    """The full-footprint foam tape that goes under every board — never corner dots."""
    cuboid(sc, x - 1, y - 1, z, w + 2, d + 2, FOAM_T, C_FOAM, layer=layer)


def devkit(sc, x=None, y=None, z=None, label=False, layer=5, pad=False, pins=None):
    """ESP32 DevKit V1. The micro-USB faces the BACK arm (large x), which fixes its orientation.
    pins = list of (name, side, index) to flag on the header."""
    x = DEVKIT_XY[0] if x is None else x
    y = DEVKIT_XY[1] if y is None else y
    z = Z_DECK if z is None else z
    if pad:
        foam_pad(sc, x, y, z - FOAM_T, DEVKIT_W, DEVKIT_D, layer=layer - 1)
    cuboid(sc, x, y, z, DEVKIT_W, DEVKIT_D, DEVKIT_T, C_ESP, layer=layer)
    cuboid(sc, x + DEVKIT_W - 10, y + 9, z + DEVKIT_T, 8, 10, 4.2, '#b9bec6', layer=layer)  # micro-USB, aft
    cuboid(sc, x + 8, y + 5, z + DEVKIT_T, 18, 18, 2.6, '#3a3f46', layer=layer)             # shield can
    _header(sc, x + 6, y + 0.6, z + DEVKIT_T, 15, 'x', layer=layer)                         # LEFT header
    _header(sc, x + 6, y + DEVKIT_D - 2.2, z + DEVKIT_T, 15, 'x', layer=layer)              # RIGHT header
    if label:
        tag(sc, (x + DEVKIT_W / 2, y + DEVKIT_D / 2, z + 10), 'ESP32 DevKit V1', dy=-16)


def devkit_pin(which_row, idx, x=None, y=None, z=None):
    """World coordinates of one DevKit header pin, so wires can land on a real place.
    which_row: 'left' (y-) or 'right' (y+). idx: 0..14 from the nose end."""
    x = DEVKIT_XY[0] if x is None else x
    y = DEVKIT_XY[1] if y is None else y
    z = Z_DECK if z is None else z
    py = y + 1.7 if which_row == 'left' else y + DEVKIT_D - 1.1
    return (x + 6.8 + idx * 2.54, py, z + DEVKIT_T + 2.2)


def to220(sc, x, y, z, layer=3, flat=True, shrink=True, label=None):
    """One IRLB8721. On this build they lie FLAT on the board, body toward the near edge and
    the heat-shrunk metal tab at the far end. Legs (G-D-S, left to right) point toward +y."""
    if flat:
        cuboid(sc, x, y, z, 10.16, 11.0, 4.6, C_TO220, layer=layer)             # plastic body
        cuboid(sc, x - 0.2, y - 4.4, z, 10.56, 4.6, 5.0,
               '#1b2b6b' if shrink else '#9aa0a6', layer=layer)                  # tab (heat-shrunk)
        for i in range(3):
            cuboid(sc, x + 1.9 + i * 2.54, y + 11.0, z, 0.9, 4.0, 0.9, '#c9ced4', layer=layer)
    else:
        cuboid(sc, x, y, z + 2.6, 10.16, 4.6, 11.0, C_TO220, layer=layer)
        cuboid(sc, x + 0.4, y + 0.3, z + 13.4, 9.4, 4.0, 4.2, '#9aa0a6', layer=layer)
        for i in range(3):
            cuboid(sc, x + 1.9 + i * 2.54, y + 1.6, z, 0.9, 0.9, 2.6, '#c9ced4', layer=layer)
    if label:
        tag(sc, (x + 5, y + 5, z + 6), label, dy=-18, size=6.0)


def mosfet_board(sc, x=None, y=None, z=None, label=False, layer=3, channels=4,
                 flip=False, rails=True, cap=True, pads=False):
    """The perfboard of four low-side switches.
    flip=True draws it as mounted — solder side up against the carbon, components hidden below."""
    x = MOSFET_XY[0] if x is None else x
    y = MOSFET_XY[1] if y is None else y
    z = Z_MOSFET if z is None else z
    cuboid(sc, x, y, z, MOSFET_W, MOSFET_D, MOSFET_T, C_PERF, layer=layer)
    zt = z + MOSFET_T
    if flip:
        # mounted under the plate: what faces the viewer is the solder side, so the components
        # are hidden and only the joints and the labelled motor pads show
        for gx in range(3, int(MOSFET_W) - 2, 4):
            for gy in range(3, int(MOSFET_D) - 2, 4):
                disc(sc, x + gx, y + gy, zt + 0.02, 0.8, '#b9bec6', layer=layer, bump=0.05)
        if pads:
            for c, which in enumerate(('front', 'right', 'back', 'left')[:channels]):
                px = x + 8.5 + c * 11.4
                for py, lab in ((y + 3.4, '+'), (y + MOSFET_D - 4.2, '−')):
                    disc(sc, px, py, zt + 0.05, 1.7, '#c87533', layer=layer, bump=0.2)
                tag(sc, (px, y + 3.4, zt + 1), 'M%d' % CHANNEL[which],
                    dx=(c - 1.5) * 15, dy=-24 - abs(c - 1.5) * 9, size=5.8)
        return
    for gx in range(3, int(MOSFET_W) - 2, 5):              # the perfboard hole grid
        for gy in range(3, int(MOSFET_D) - 2, 5):
            disc(sc, x + gx, y + gy, zt + 0.02, 0.62, '#0a4c2c', layer=layer, bump=0.05)
    if rails:
        # BAT+ (bare copper, far edge) and GND (tinned, near edge) — both flooded with solder
        cuboid(sc, x + 2, y + 2.4, zt, MOSFET_W - 4, 1.8, 1.2, '#c87533', layer=layer)
        cuboid(sc, x + 2, y + MOSFET_D - 4.2, zt, MOSFET_W - 4, 1.8, 1.2, '#c9ced4', layer=layer)
    for c in range(channels):
        cx = x + 3.5 + c * 11.4                            # four channels side by side
        to220(sc, cx, y + 24.5, zt, layer=layer)           # body mid-board, tab toward BAT+
        cuboid(sc, cx + 0.6, y + 15.0, zt, 2.2, 7.0, 2.2, '#c8b28a', layer=layer)    # 100R gate resistor
        cuboid(sc, cx + 5.4, y + 15.0, zt, 2.2, 7.0, 2.2, '#8fa2c9', layer=layer)    # 10k pull-down
        cyl_y(sc, cx + 8.6, y + 6.0, zt + 1.3, 7.4, 1.3, '#3a3f46', layer=layer)     # 1N5819 flyback
        cuboid(sc, cx + 7.7, y + 11.4, zt + 0.4, 1.8, 1.4, 1.6, '#e8edf2', layer=layer)  # cathode band
    if cap:
        cyl_z(sc, x + MOSFET_W - 6.5, y + 12, zt, 11.0, 4.0, '#1b2b6b', layer=layer)
    if pads:
        for c, which in enumerate(('front', 'right', 'back', 'left')[:channels]):
            tag(sc, (x + 8.5 + c * 11.4, y + 3.4, zt + 2),
                'M%d' % CHANNEL[which], dx=(c - 1.5) * 15, dy=-26 - abs(c - 1.5) * 9, size=5.8)
    if label:
        tag(sc, (x + MOSFET_W / 2, y + MOSFET_D / 2, zt + 12), 'לוח המוספטים', dy=-18)


def mt3608(sc, x=None, y=None, z=None, label=False, layer=5, pad=False, locked=False):
    """MT3608 boost. The blue 25-turn trimmer is what gets turned to reach 5.00 V."""
    x = MT_XY[0] if x is None else x
    y = MT_XY[1] if y is None else y
    z = Z_DECK if z is None else z
    if pad:
        foam_pad(sc, x, y, z - FOAM_T, MT_W, MT_D, layer=layer - 1)
    cuboid(sc, x, y, z, MT_W, MT_D, MT_T, C_MT, layer=layer)
    cuboid(sc, x + 7, y + 4, z + MT_T, 10, 9, 5.2, '#1b1b1b', layer=layer)              # inductor
    cuboid(sc, x + 21, y + 4.5, z + MT_T, 8, 8, 4.4, '#2b6fd0', layer=layer)            # trimmer
    cuboid(sc, x + 23.6, y + 7.2, z + MT_T + 4.4, 2.8, 0.9, 0.5, '#e8edf2', layer=layer)  # screw slot
    if locked:
        disc(sc, x + 25, y + 8.5, z + MT_T + 5.0, 5.2, '#e8b4c8', extra='fill-opacity:0.55',
             layer=layer, bump=1.2)
    if label:
        tag(sc, (x + MT_W / 2, y + MT_D / 2, z + 8), 'MT3608', dy=-16, size=6.4)


def mpu6050(sc, x=None, y=None, z=None, label=False, layer=5, pad=False, arrow_mark=True):
    """GY-521, chip side up, its silk-screen X arrow pointing at the FRONT motor."""
    x = IMU_XY[0] if x is None else x
    y = IMU_XY[1] if y is None else y
    z = Z_DECK if z is None else z
    if pad:
        foam_pad(sc, x, y, z - FOAM_T, IMU_W, IMU_D, layer=layer - 1)
    cuboid(sc, x, y, z, IMU_W, IMU_D, IMU_T, C_IMU, layer=layer)
    cuboid(sc, x + 7.5, y + 5.5, z + IMU_T, 5.0, 5.0, 1.2, '#15181c', layer=layer)
    _header(sc, x + 2, y + 0.8, z + IMU_T, 8, 'x', layer=layer)
    if arrow_mark:                       # X arrow toward the nose (small x)
        a = iso(x + 5.5, y + 12.5, z + IMU_T + 0.05)
        b = iso(x + 1.5, y + 12.5, z + IMU_T + 0.05)
        sc.add(depth(x + 3, y + 12.5, z + IMU_T) + 60,
               '<path d="M %.2f %.2f L %.2f %.2f" style="stroke:#e8edf2;stroke-width:0.8"/>'
               '<circle cx="%.2f" cy="%.2f" r="1.0" style="fill:#e8edf2"/>'
               % (a[0], a[1], b[0], b[1], b[0], b[1]), layer)
    if label:
        tag(sc, (x + IMU_W / 2, y + IMU_D / 2, z + 8), 'GY-521', dy=-14, size=6.2)


def lipo(sc, x=None, y=None, z=None, label=False, layer=0, leads=True, plug=True):
    """1S LiPo 1000 mAh, slung under the bottom plate on its two O-rings."""
    x = BAT_XY[0] if x is None else x
    y = BAT_XY[1] if y is None else y
    z = Z_BAT if z is None else z
    cuboid(sc, x, y, z, BAT_W, BAT_D, BAT_H, C_LIPO, layer=layer)
    cuboid(sc, x + 6, y + 4, z + BAT_H, BAT_W - 12, BAT_D - 8, 0.4, '#3f4653', layer=layer)
    if plug:
        cuboid(sc, x - 5.0, y + BAT_D / 2 - 3, z + BAT_H * 0.35, 5.0, 6.0, 4.0, WHITE_W, layer=layer)
    if leads:
        for i, col in enumerate((RED, BLACK)):
            wire(sc, [(x - 5.0, y + BAT_D / 2 - 1.4 + i * 2.6, z + BAT_H * 0.5),
                      (x - 17, y + BAT_D / 2 - 1.4 + i * 2.6, z + BAT_H + 5)], col, 1.3, layer=4)
    if label:
        tag(sc, (x + BAT_W / 2, y + BAT_D / 2, z), '1S LiPo 1000mAh', dx=-40, dy=26, size=6.2)


def orings(sc, z=None, layer=2):
    """The two rubber O-rings that are the ONLY thing holding the cell on — thin bands
    running down each side of the pack and up through the plate slots."""
    z = Z_PLATE if z is None else z
    h = abs(Z_BAT) + PLATE_T + 1.0
    for ox in (CTR_X - 15, CTR_X + 15):
        for sy, lay in ((CTR_Y - BAT_D / 2 - 2.2, layer), (CTR_Y + BAT_D / 2 + 2.2, layer + 3)):
            cuboid(sc, ox - 1.6, sy - 0.8, z + Z_BAT - 1.0, 3.2, 1.6, h, '#1a1d22', layer=lay)
        cuboid(sc, ox - 1.6, CTR_Y - BAT_D / 2 - 2.2, z + Z_BAT - 1.0, 3.2, BAT_D + 4.4, 1.6,
               '#1a1d22', layer=layer)


# ---------------------------------------------------------------- the assembled machine
def drone(sc, z=0.0, props=False, spinning=False, battery=True, electronics=True,
          leads=True, front_mark=False, tether_loop=False, motors=True):
    """The whole quadcopter at height z. The default state is the safe one: no props fitted."""
    frame(sc, z=z, front_mark=front_mark, tether_loop=tether_loop)
    if motors:
        motors_all(sc, z=z, leads=leads, spinning=spinning and not props)
    if electronics:
        mosfet_board(sc, z=z + Z_MOSFET, flip=True, layer=2)
        devkit(sc, z=z + Z_DECK)
        mt3608(sc, z=z + Z_DECK)
        mpu6050(sc, z=z + Z_DECK)
    if battery:
        lipo(sc, z=z + Z_BAT)
        orings(sc, z=z)
    if props:
        props_all(sc, z=z, spinning=spinning)


# ---------------------------------------------------------------- bench, tools, room
def bench(sc, x0=82, y0=48, w=140, d=130, z=-24):
    cuboid(sc, x0, y0, z, w, d, 4, '#d9cfbe', layer=0)


def mat(sc, x0=70, y0=40, w=160, d=145, z=-19.4, col='#3f4a55'):
    cuboid(sc, x0, y0, z, w, d, 1.2, col, layer=0)


def floor(sc, z=-120, x0=20, y0=10, w=290, d=210):
    cuboid(sc, x0, y0, z - 2, w, d, 2, '#f4f1ea', layer=0)


def tray(sc, x, y, z, w=110, d=80, layer=0):
    cuboid(sc, x, y, z, w, d, 1.5, '#e8e2d4', layer=layer)
    for dx, dy, dw, dd in ((4, 4, w / 2 - 6, d / 2 - 6), (w / 2 + 2, 4, w / 2 - 6, d / 2 - 6),
                           (4, d / 2 + 2, w / 2 - 6, d / 2 - 6), (w / 2 + 2, d / 2 + 2, w / 2 - 6, d / 2 - 6)):
        pts = [(x + dx, y + dy), (x + dx + dw, y + dy), (x + dx + dw, y + dy + dd), (x + dx, y + dy + dd)]
        sc.add(depth(x + dx + dw / 2, y + dy + dd / 2, z + 1.5) + 2,
               poly([iso(px, py, z + 1.55) for px, py in pts], 'none', '#b8ae9a', 0.5,
                    'stroke-dasharray:2.4 1.8'), layer + 1)


def kitchen_scale(sc, x, y, z, layer=0, reading=None):
    cuboid(sc, x, y, z, 120, 100, 9, '#e8ebee', layer=layer)
    cuboid(sc, x + 6, y + 6, z + 9, 108, 62, 0.6, '#ccd2d8', layer=layer)
    cuboid(sc, x + 32, y + 74, z + 9, 56, 18, 0.9, '#15181c', layer=layer)
    if reading:
        cx, cy = iso(x + 60, y + 83, z + 10)
        sc.over('<text x="%.2f" y="%.2f" style="font-family:JetBrains Mono,monospace;font-size:7.5px;'
                'font-weight:700;fill:#7ee0a0;text-anchor:middle">%s</text>' % (cx, cy + 2.6, reading))


def multimeter(sc, x, y, z, layer=3, reading=None, mode=None, probes=None, probe_col=(None, None)):
    """A pocket multimeter. probes = the two world points the tips touch."""
    W, D, H = 52.0, 86.0, 16.0
    cuboid(sc, x, y, z, W, D, H, '#e0651a', layer=layer)
    cuboid(sc, x + 5, y + 56, z + H, W - 10, 22, 0.8, '#15181c', layer=layer)     # display
    cyl_z(sc, x + W / 2, y + 30, z + H, 2.4, 11, '#2b3038', layer=layer)          # dial
    if reading:
        cx, cy = iso(x + W / 2, y + 68, z + H + 1)
        sc.over('<text x="%.2f" y="%.2f" style="font-family:JetBrains Mono,monospace;font-size:7.5px;'
                'font-weight:700;fill:#7ee0a0;text-anchor:middle">%s</text>' % (cx, cy + 2.6, reading))
    if mode:
        cx, cy = iso(x + W / 2, y + 30, z + H + 3)
        sc.over('<text x="%.2f" y="%.2f" style="font-family:Rubik,Arial;font-size:5.6px;font-weight:700;'
                'fill:#e8edf2;text-anchor:middle">%s</text>' % (cx, cy + 2.0, mode))
    if probes:
        for (p, col) in zip(probes, (RED, BLACK)):
            wire(sc, [(x + 16, y + 3, z + 9), (x - 6, y - 20, z + 14), p], col, 1.2, layer=4)
            cyl_z(sc, p[0], p[1], p[2], 6, 0.7, col, layer=5)


def soldering_iron(sc, tip, layer=6):
    """The iron, held nearly flat with its bit on `tip` and the handle running out toward +x
    (which in this projection is toward the viewer's lower right, i.e. out of the work)."""
    tx, ty, tz = tip
    cyl_x(sc, tx, ty, tz + 2.6, 15, 1.2, '#b9873a', layer=layer)          # the bit
    cyl_x(sc, tx + 15, ty, tz + 4.4, 8, 2.6, '#7d848c', layer=layer)      # the nut
    cyl_x(sc, tx + 23, ty, tz + 5.6, 16, 3.4, '#9aa0a6', layer=layer)     # the shaft sleeve
    cyl_x(sc, tx + 39, ty, tz + 8.0, 54, 6.4, '#2f343b', layer=layer)     # the handle
    cyl_x(sc, tx + 93, ty, tz + 8.0, 13, 5.2, '#c0392b', layer=layer)     # the cable boot


def iron_stand(sc, x, y, z, layer=3):
    cuboid(sc, x, y, z, 46, 34, 6, '#6b7078', layer=layer)
    cyl_x(sc, x - 2, y + 17, z + 16, 60, 5.0, '#2f343b', layer=layer)
    cyl_x(sc, x + 58, y + 17, z + 16, 14, 2.0, '#b9873a', layer=layer)
    cuboid(sc, x + 4, y + 40, z, 28, 22, 5, '#8fc98f', layer=layer)          # damp sponge


def solder_reel(sc, x, y, z, layer=3):
    cyl_y(sc, x, y, z + 13, 13, 13, '#c9ced4', layer=layer)


def goggles(sc, x, y, z, layer=3):
    cuboid(sc, x, y, z, 46, 20, 9, '#2f6fb5', layer=layer)
    cuboid(sc, x + 4, y + 2, z + 2, 16, 16, 6.4, '#b9d6ef', layer=layer)
    cuboid(sc, x + 26, y + 2, z + 2, 16, 16, 6.4, '#b9d6ef', layer=layer)


def lipo_bag(sc, x, y, z, layer=0, label=None):
    cuboid(sc, x, y, z, 90, 62, 20, '#3a3f46', layer=layer)
    cuboid(sc, x + 5, y + 5, z + 20, 80, 52, 1.4, '#4b515a', layer=layer)
    cuboid(sc, x + 26, y + 22, z + 21.4, 38, 18, 0.6, '#e0651a', layer=layer)
    if label:
        tag(sc, (x + 45, y + 31, z + 22), label, dy=-20, size=6.2)


def card(sc, x, y, z, w=58, d=44, col='#fffdf7', lines=3, layer=3):
    """A printed card / contract / checklist lying on the bench."""
    cuboid(sc, x, y, z, w, d, 0.6, col, layer=layer)
    for i in range(lines):
        a = iso(x + 5, y + 8 + i * (d - 14) / max(1, lines - 1), z + 0.65)
        b = iso(x + w - 5, y + 8 + i * (d - 14) / max(1, lines - 1), z + 0.65)
        sc.add(depth(x + w / 2, y + 8 + i * 6, z) + 40 + i,
               '<path d="M %.2f %.2f L %.2f %.2f" style="stroke:#b9bec6;stroke-width:0.7"/>'
               % (a[0], a[1], b[0], b[1]), layer)


def tether(sc, x, y, z_top, ax, ay, az, layer=5):
    """The fishing line every practice flight is flown on: drone loop to floor anchor."""
    a = iso(x, y, z_top)
    b = iso(ax, ay, az)
    sc.over('<path d="M %.2f %.2f L %.2f %.2f" style="fill:none;stroke:#8a94a2;stroke-width:0.9;'
            'stroke-dasharray:5 3"/>' % (a[0], a[1], b[0], b[1]))
    sc.over('<circle cx="%.2f" cy="%.2f" r="1.5" style="fill:none;stroke:#8a94a2;stroke-width:0.9"/>'
            % (a[0], a[1]))


def anchor_weight(sc, x, y, z, layer=0):
    cuboid(sc, x, y, z, 44, 36, 14, '#5a6674', layer=layer)
    cuboid(sc, x + 8, y + 8, z + 14, 28, 20, 3, '#717e8c', layer=layer)


def tape_line(sc, x, y0, y1, z, col='#e0b400', layer=0, bump=9400):
    """The spectator line taped on the floor."""
    pts = [(x, y0), (x + 5, y0), (x + 5, y1), (x, y1)]
    sc.add(bump, poly([iso(px, py, z) for px, py in pts], col, None), layer)


# The laptop and the phone are drawn at roughly 3/4 of life size. At true scale they are each
# bigger than the whole 100 mm drone and swallow the subject of the picture; the drone is what
# the card is about, so the desk props are the ones that give way.
def laptop(sc, x, y, z, layer=5, screen='#e8edf2'):
    cuboid(sc, x, y, z, 112, 80, 4, '#3a4048', layer=layer)
    cuboid(sc, x + 9, y + 15, z + 4, 94, 46, 0.6, '#22262c', layer=layer)
    cuboid(sc, x + 39, y + 65, z + 4, 34, 10, 0.6, '#4a5058', layer=layer)
    cuboid(sc, x, y - 4, z, 112, 4, 74, '#4a5058', layer=layer)
    cuboid(sc, x + 5, y - 0.5, z + 6, 102, 0.7, 63, screen, layer=layer)
    cuboid(sc, x + 11, y - 0.9, z + 45, 90, 0.4, 6, '#2f8fd0', layer=layer)


def phone_flat(sc, x, y, z, label=None, armed=False, throttle=0.0, layer=5):
    """The phone running the drone's page: the big ARM/DISARM button and the throttle slider."""
    W, D = 122.0, 58.0
    cuboid(sc, x, y, z, W, D, 7, '#2b3038', layer=layer)
    zt = z + 7
    key = depth(x + W / 2, y + D / 2, z + 3.5)

    def face(x0, y0, w, d_, col, bump):
        sc.add(key + bump, poly([iso(x0, y0, zt), iso(x0 + w, y0, zt),
                                 iso(x0 + w, y0 + d_, zt), iso(x0, y0 + d_, zt)], col, None), layer)

    face(x + 3, y + 3, W - 6, D - 6, '#e8edf2', 1)
    face(x + 9, y + 9, 42, D - 18, '#dc2626' if armed else '#25a05a', 2)       # ARM / DISARM
    face(x + 60, y + 14, 52, 8, '#c3cad2', 3)                                  # throttle track
    face(x + 60 + 3 + throttle * 38, y + 10, 11, 16, '#2563eb', 4)             # knob
    if label:
        tag(sc, (x + W / 2, y + 2, z + 9), label, dy=-30, size=6.4)


def hand_thumb(sc, x, y, z, ang=225.0, layer=6):
    """A stylised thumb pressing straight down on (x, y, z) — the press-fit gesture."""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)
    cyl_z(sc, x, y, z, 13, 5.2, '#e8c9a8', layer=layer)
    cuboid(sc, x + ca * 6 - 7, y + sa * 6 - 7, z + 12, 26, 16, 12, '#e8c9a8', layer=layer)
