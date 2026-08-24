"""scenes_p8.py — the Project 8 (tiny quadcopter) step figures.

Same contract as the other scene modules: hardware only, named anchors, Hebrew composited
afterwards. Scene keys map onto the figure names the CARDS ALREADY EMBED — see build_p8.sh.

Project 8 is different from the car projects in one way that shapes almost every figure here:
most of these cards are about what is NOT on the drone. Props off, battery out, USB unplugged.
So the closed prop box, the zipped LiPo bag and the coiled-aside USB cable are not set dressing
— they carry the safety rule the card exists to teach, and a figure that leaves them out is
teaching the opposite. Three rules hold across the whole set:

  * props appear on the aircraft in exactly two scenes — the tethered hovers and the thrust
    tests. Everywhere else the four shafts are bare. No prop guards exist in this kit, so none
    are ever drawn.
  * battery in means USB out. The two are never on the drone in the same frame.
  * the thrust rig is INVERTED: props face down at the scale pan. Drawn upright it teaches the
    wrong measurement.
"""
import math
import lib as L
import p8_drone as D
import tools as T
import props as P
from lib import MM, box, cyl, tube, mat, hexcol

CTR = (D.CTR_X, D.CTR_Y, 6.0)
FLOOR = -30.0                     # the drone's feet rest here when it is on the bench


def _studio(strength=1.0):
    L.studio(strength=strength)


def _bench(z=FLOOR, x0=-60, y0=-60, w=460, d=380, colour='#a89a88'):
    """A scene with a bench must NOT also call L.ground(): two coplanar surfaces z-fight and
    the shadow catcher wins, leaving a black bench-shaped hole."""
    m = mat('bench', hexcol(colour), rough=0.72)
    return box(x0, y0, z - 7, w, d, 7, m, bevel=1.5, name='bench')


def _near(pt, k=0.55):
    """An anchor on the side of a bench accessory that faces the aircraft.

    Anchoring a 130 mm meter or a closed prop box at its own centre makes camera_fit frame the
    whole accessory, and a 100 mm drone ends up occupying a tenth of the picture. Labelling the
    near edge lets the accessory run off the frame while its callout still lands on it."""
    return (D.CTR_X + (pt[0] - D.CTR_X) * k, D.CTR_Y + (pt[1] - D.CTR_Y) * k, pt[2])


def _drone_anchors(z=0.0, props=False):
    L.anchor('drone', (D.CTR_X, D.CTR_Y, z + D.Z_DECK + 8))
    L.anchor('devkit', (D.DEVKIT_XY[0] + 26, D.DEVKIT_XY[1] + 14, z + D.Z_DECK + 6))
    L.anchor('imu', (D.IMU_XY[0] + 10, D.IMU_XY[1] + 8, z + D.Z_DECK + 4))
    L.anchor('mt', (D.MT_XY[0] + 18, D.MT_XY[1] + 8, z + D.Z_DECK + 6))
    L.anchor('board', (D.MOSFET_XY[0] + 25, D.MOSFET_XY[1] + 20, z + D.Z_MOSFET - 4))
    L.anchor('front_arm', (D.POS['front'][0], D.POS['front'][1], z + D.Z_PLATE_TOP + 2))
    L.anchor('back_arm', (D.POS['back'][0], D.POS['back'][1], z + D.Z_PLATE_TOP + 2))
    L.anchor('shafts', (D.CTR_X - 20, D.CTR_Y, z + D.Z_SHAFT + 4))
    if props:
        L.anchor('props', (D.POS['front'][0], D.POS['front'][1], z + D.Z_PROP + 4))


def _usb_aside(z=0.0):
    """The USB cable coiled off to the side, unplugged. In a battery-in scene this is the
    picture of the rule, so it gets drawn rather than implied."""
    m = D.ensure()
    # close enough to the aircraft to survive the crop. Parked out at 330 mm the coil fell
    # outside every frame, and its callout — the one that says the cable is NOT plugged in —
    # ended up with its leader pointing at bare bench.
    return [L.ribbon(L.ellipse_pts(252, 46, 40, 27, n=48), 3.0, FLOOR + 3.0,
                     m['w_black'], name='usbcoil', closed=True, thickness=3.0),
            box(214, 40, FLOOR, 16, 8, 6, m['alu'], bevel=1.0, name='usbplug')]


def _spin(which, z=0.0, r=None):
    """A turning shaft, shown as a translucent sweep of exactly the radius that is moving."""
    x, y = D.POS[which]
    return P.spin_disc(x, y, z + D.Z_SHAFT + 2, r or 3.2)


# ================================================================ TASK 1
def s_p8_parts():
    """Nothing is assembled: the tray of loose parts, the BARE frame sitting on the scale, the
    signed contract — and the props and the cell kept at a distance in the teacher's box and
    bag, which is the whole safety argument of the card."""
    _studio(1.05)
    _bench(FLOOR, x0=-40, y0=-40, w=420, d=340)
    D.ensure()
    # the scale goes UNDER the frame. A scale standing next to the thing it is meant to be
    # weighing says nothing at all, and the card is "weigh it without the battery".
    P.kitchen_scale(D.CTR_X - 90, D.CTR_Y - 70, FLOOR, ang=-4, reading=2)
    D.frame(z=FLOOR + 10.2, top_plate=True, grommets=True, front_mark=True)
    P.tray(6, 224, FLOOR, w=214, d=118, cells=(3, 2), ang=-3)
    for i, (mx, my) in enumerate(((26, 240), (50, 240), (26, 296), (50, 296))):
        D.motor(x=mx, y=my, z=FLOOR - D.Z_CAN + 4, spin='cw' if i < 2 else 'ccw', leads=True)
    D.devkit(z=FLOOR + 4, x=92, y=236)
    D.mpu6050(z=FLOOR + 4, x=98, y=296)
    D.mt3608(z=FLOOR + 4, x=154, y=232)
    D.mosfet_board(z=FLOOR + 4, x=150, y=274, foam=False, up=True)
    P.contract_card(272, 34, FLOOR, ang=-8)
    T.pencil(300, 20, FLOOR + 1, ang=104)
    T.goggles(280, 152, FLOOR, ang=-14)
    P.lidded_box(284, 246, FLOOR, 108, 82, 42, ang=-10)
    P.fireproof_bag(-16, 54, FLOOR, w=118, d=84, ang=-8)
    L.anchor('scale', (D.CTR_X - 22, D.CTR_Y - 62, FLOOR + 12))
    L.anchor('tray', _near((113, 283, FLOOR + 26)))
    L.anchor('contract', _near((327, 72, FLOOR + 2)))
    L.anchor('propbox', _near((338, 287, FLOOR + 26)))
    L.anchor('bag', _near((43, 96, FLOOR + 20)))
    L.camera_fit(subject='scale', azimuth=46, elevation=40, lens=54)


def s_p8_press_fit():
    """The frame flat with the painted FRONT arm pointing away, one motor mid-press into its
    grommet and the other three already seated. Thumb pressure only — no tool in the frame."""
    _studio()
    _bench(FLOOR, x0=-40, y0=-40, w=400, d=340)
    D.ensure()
    zf = FLOOR - D.Z_PLATE
    D.frame(z=zf, front_mark=True)
    for which in ('back', 'left', 'right'):
        D.motor(which, z=zf, leads=True)
    D.motor('front', z=zf, leads=True, lift=26)          # still on its way in
    L.anchor('press', (D.POS['front'][0], D.POS['front'][1], zf + D.Z_CAN + 44))
    L.anchor('grommet', (D.POS['front'][0], D.POS['front'][1] + 8, zf + D.Z_PLATE_TOP + 2))
    L.anchor('leads_cw', (D.POS['back'][0], D.POS['back'][1] - 24, zf + D.Z_CAN - 2))
    L.anchor('leads_ccw', (D.POS['right'][0] + 4, D.POS['right'][1] - 24, zf + D.Z_CAN - 2))
    L.anchor('front_arm', (D.POS['front'][0] + 12, D.CTR_Y, zf + D.Z_PLATE_TOP + 1))
    L.camera_fit(subject='grommet', azimuth=44, elevation=34, lens=63)


def s_p8_meet_board():
    """The MOSFET board alone and BIG, connected to nothing: the pigtail hangs unplugged, a
    spare IRLB8721 stands beside it label-up, and the meter probes sit on the two rails."""
    _studio(1.05)
    _bench(FLOOR, x0=-90, y0=-70, w=380, d=300)
    m = D.ensure()
    bx, by = 60.0, 70.0
    D.mosfet_board(z=FLOOR, x=bx, y=by, foam=False, up=True)
    # one loose TO-220 standing beside the board, label to the viewer and legs down
    box(bx + 62, by + 4, FLOOR + 3, 10.0, 4.6, 15.0, m['to220'], bevel=0.4, name='spare')
    box(bx + 63.4, by + 3.0, FLOOR + 9, 7.2, 6.4, 0.8, m['shield'], bevel=0.2, name='spare_tab')
    for leg in range(3):
        box(bx + 63.6 + leg * 3.2, by + 5.0, FLOOR, 0.8, 0.5, 3.0, m['gold'],
            bevel=0, name='spare_leg')
    # the battery pigtail, hanging unplugged — the thing the card is actually about
    tube([(bx, by + D.RAIL_BAT_DY, FLOOR - 1), (bx - 30, by - 26, FLOOR + 4),
          (bx - 54, by - 48, FLOOR + 2)], 0.9, m['w_red'], name='pigtail')
    tube([(bx, by + D.RAIL_GND_DY, FLOOR - 1), (bx - 36, by - 18, FLOOR + 4),
          (bx - 58, by - 44, FLOOR + 2)], 0.9, m['w_black'], name='pigtail')
    # the PH2.0 shell on the loose end. Two wires ending in mid-air read as a drawing that ran
    # out of room; a visible empty connector reads as "this board is plugged into nothing",
    # which is the entire point of the card.
    box(bx - 66, by - 50, FLOOR, 9.0, 7.0, 5.0, m['w_white'], bevel=0.8, name='ph2_shell')
    P.multimeter(bx + 118, by + 92, FLOOR, ang=-24)
    L.anchor('tab', (bx + 67, by + 6, FLOOR + 13))
    L.anchor('rails', (bx + 24, by + D.RAIL_BAT_DY, FLOOR + 1))
    L.anchor('gnd_rail', (bx + 24, by + D.RAIL_GND_DY, FLOOR + 1))
    L.anchor('gate_pad', (bx + D.CH_X0 + 5, by + D.PAD_GATE_DY, FLOOR + 1))
    L.anchor('meter', _near((bx + 162, by + 186, FLOOR + 38)))
    L.anchor('pigtail', (bx - 52, by - 44, FLOOR + 4))
    L.camera_fit(subject='rails', azimuth=44, elevation=40, lens=62)


def s_p8_mount():
    """Every board on its own full-footprint insulating pad: DevKit centred with its USB facing
    the BACK arm, the MPU6050 flat in front of it with its X arrow on the FRONT motor."""
    _studio()
    _bench(FLOOR, x0=-40, y0=-40, w=400, d=340)
    D.ensure()
    zf = FLOOR - D.Z_PLATE
    D.frame(z=zf, front_mark=True)
    D.motors_all(z=zf, leads=True)
    D.devkit(dz=zf)
    D.mpu6050(dz=zf)
    D.mt3608(dz=zf)
    D.mosfet_board(dz=zf)
    _drone_anchors(zf)
    L.anchor('usb_face', (D.DEVKIT_XY[0] + D.DEVKIT_W, D.CTR_Y, zf + D.Z_DECK + 5))
    L.anchor('arrow', (D.IMU_XY[0] + 3, D.IMU_XY[1] + 2, zf + D.Z_DECK + 3))
    L.anchor('pad_m1', (D.MOSFET_XY[0] + D.CH_X0 + 5, D.MOSFET_XY[1] + D.PAD_MPLUS_DY,
                        zf + D.Z_MOSFET - 2))
    L.camera_fit(subject='drone', azimuth=42, elevation=32, lens=65)


def s_p8_power_tree():
    """Six power wires and nothing else — no gate wires and no I2C yet. The cell is not here;
    it is in the teacher's bag, which is why the bag is in the frame."""
    _studio()
    _bench(FLOOR, x0=-40, y0=-50, w=460, d=380)
    D.ensure()
    zf = FLOOR - D.Z_PLATE
    D.frame(z=zf, front_mark=True)
    D.motors_all(z=zf, leads=True)
    D.devkit(dz=zf)
    D.mpu6050(dz=zf)
    D.mt3608(dz=zf)
    D.mosfet_board(dz=zf)
    D.power_tree(zf, battery=False)
    P.fireproof_bag(236, 208, FLOOR, ang=-14)
    _drone_anchors(zf)
    L.anchor('in_pair', (D.MT_XY[0] + 2, D.MT_XY[1] + 8, zf + D.Z_DECK + 6))
    L.anchor('out_pair', (D.MT_XY[0] + D.MT_W, D.MT_XY[1] + 4, zf + D.Z_DECK + 6))
    L.anchor('bag', _near((298, 254, FLOOR + 20), 0.75))
    L.camera_fit(subject='drone', azimuth=44, elevation=34, lens=60)


def s_p8_motor_wiring():
    """Eight joints, two per motor, on four separate channels. A motor's minus lands on the
    Drain pad and its plus hangs off the BAT+ rail — never on the GND rail."""
    _studio()
    _bench(FLOOR, x0=-40, y0=-40, w=420, d=350)
    D.ensure()
    zf = FLOOR - D.Z_PLATE
    D.frame(z=zf, front_mark=True)
    D.motors_all(z=zf, leads=False)
    D.devkit(dz=zf)
    D.mt3608(dz=zf)
    D.mosfet_board(dz=zf)
    D.motor_wires_to_board(zf)
    D.power_tree(zf, battery=False)
    T.soldering_iron(232, 26, FLOOR + 34, ang=126, tilt=24)
    P.multimeter(300, 236, FLOOR, ang=-24)
    _drone_anchors(zf)
    L.anchor('m1', (D.MOSFET_XY[0] + D.CH_X0 + 5, D.MOSFET_XY[1] + D.PAD_MPLUS_DY,
                    zf + D.Z_MOSFET - 2))
    L.anchor('m1_minus', (D.MOSFET_XY[0] + D.CH_X0 + 5, D.MOSFET_XY[1] + D.PAD_MMINUS_DY,
                          zf + D.Z_MOSFET - 2))
    L.anchor('meter', _near((380, 326, FLOOR + 38)))
    L.camera_fit(subject='drone', azimuth=46, elevation=36, lens=60)


def s_p8_signal_wiring():
    """Four gate wires — yellow 25 to G1, orange 26 to G2, green 14 to G3, blue 27 to G4 —
    plus white SDA and grey SCL. Battery in the bag, USB coiled aside."""
    _studio()
    _bench(FLOOR, x0=-40, y0=-50, w=460, d=390)
    D.ensure()
    zf = FLOOR - D.Z_PLATE
    D.frame(z=zf, front_mark=True)
    D.motors_all(z=zf, leads=False)
    D.devkit(dz=zf)
    D.mpu6050(dz=zf)
    D.mt3608(dz=zf)
    D.mosfet_board(dz=zf)
    D.motor_wires_to_board(zf)
    D.power_tree(zf, battery=False)
    D.gate_wires(zf)
    D.i2c_wires(zf)
    P.fireproof_bag(238, 214, FLOOR, ang=-14)
    _usb_aside(zf)
    _drone_anchors(zf)
    L.anchor('gates', (D.MOSFET_XY[0] - 6, D.MOSFET_XY[1] + D.PAD_GATE_DY, zf + D.Z_MOSFET + 4))
    L.anchor('i2c', (D.IMU_XY[0] + 8, D.IMU_XY[1] + D.IMU_D, zf + D.Z_DECK + 6))
    L.anchor('bag', _near((300, 260, FLOOR + 20), 0.75))
    L.anchor('usb', (252, 46, FLOOR + 6))
    L.camera_fit(subject='drone', azimuth=44, elevation=36, lens=60)


def _drone_on_bench(zf, props=False, battery=True, spin=None):
    D.ensure()
    D.frame(z=zf, front_mark=True)
    D.motors_all(z=zf, leads=False, props=props)
    D.devkit(dz=zf)
    D.mpu6050(dz=zf)
    D.mt3608(dz=zf)
    D.mosfet_board(dz=zf)
    D.motor_wires_to_board(zf)
    D.gate_wires(zf)
    D.i2c_wires(zf)
    D.power_tree(zf, battery=battery)
    for which in (spin or ()):
        _spin(which, zf)


def s_p8_pre_power():
    """Part one is the resistance sweep with no cell in; part two is the teacher pushing the
    PH2.0 plug home. Goggles on, props nowhere, USB coiled aside."""
    _studio()
    _bench(FLOOR, x0=-50, y0=-50, w=470, d=400)
    zf = FLOOR - D.Z_PLATE
    _drone_on_bench(zf, props=False, battery=True)
    P.multimeter(296, 226, FLOOR, ang=-22)
    T.goggles(30, 250, FLOOR, ang=-12)
    P.lidded_box(330, 20, FLOOR, 110, 84, 42, ang=-8)
    _usb_aside(zf)
    _drone_anchors(zf)
    L.anchor('meter', _near((376, 316, FLOOR + 38)))
    L.anchor('plug', (D.BAT_XY[0] + D.BAT_W + 10, D.BAT_XY[1] + D.BAT_D / 2, zf + D.Z_BAT + 5))
    L.anchor('propbox', _near((385, 62, FLOOR + 28)))
    L.anchor('usb', (252, 46, FLOOR + 6))
    L.camera_fit(subject='drone', azimuth=46, elevation=34, lens=58)


def s_p8_upload_test():
    """USB in means battery out: the cable is in the DevKit and the pigtail hangs empty, the
    cell shut in the bag on the far side of the bench."""
    _studio()
    _bench(FLOOR, x0=-60, y0=-60, w=560, d=430)
    zf = FLOOR - D.Z_PLATE
    m = D.ensure()
    _drone_on_bench(zf, props=False, battery=False)
    T.laptop(268, 250, FLOOR, ang=-16, lid=102, screen='code')
    tube([(D.DEVKIT_XY[0] + D.DEVKIT_W + 4, D.CTR_Y, zf + D.Z_DECK + 4),
          (240, 70, FLOOR + 26),
          (300, 180, FLOOR + 12),
          (318, 258, FLOOR + 6)], 1.6, m['w_black'], name='usb')
    P.fireproof_bag(30, 300, FLOOR, ang=-8)
    _drone_anchors(zf)
    L.anchor('usb_in', (D.DEVKIT_XY[0] + D.DEVKIT_W + 4, D.CTR_Y, zf + D.Z_DECK + 5))
    L.anchor('laptop', _near((372, 392, FLOOR + 96)))
    L.anchor('bag', _near((105, 352, FLOOR + 20)))
    L.camera_fit(subject='drone', azimuth=48, elevation=32, lens=56)


def s_p8_spin():
    """Bare shafts, USB unplugged, cell in — and exactly one motor turning."""
    _studio()
    _bench(FLOOR, x0=-50, y0=-50, w=500, d=400)
    zf = FLOOR - D.Z_PLATE
    _drone_on_bench(zf, props=False, battery=True, spin=('front',))
    # the camera sits at +x/-y, so anything placed at -y is the nearest thing to the lens
    # and swells by perspective alone. The phone goes off to the side at the SAME depth
    # as the aircraft instead — perpendicular to the view axis, not in front of it.
    P.phone(246, 196, FLOOR, ang=-16, tilt=56, ui='drive')
    _usb_aside(zf)
    P.lidded_box(400, 250, FLOOR, 120, 90, 44, ang=-10)
    _drone_anchors(zf)
    L.anchor('spinning', (D.POS['front'][0], D.POS['front'][1], zf + D.Z_SHAFT + 6))
    L.anchor('phone', _near((282, 254, FLOOR + 76), 0.7))
    L.anchor('usb', (252, 46, FLOOR + 6))
    L.anchor('propbox', _near((460, 296, FLOOR + 30)))
    L.camera_fit(subject='drone', azimuth=46, elevation=30, lens=58)


# the vertical bookkeeping of the thrust rig, written out once because getting it wrong is
# the difference between a figure that measures thrust and one that measures nothing
PAN_Z = FLOOR + 10.2                       # top face of the scale pan
PROP_CLEAR = 70.0                          # more than one prop diameter above the pan


def _thrust_rig(props=True, reading=3):
    """The drone INVERTED on a weighted post over the scale pan, props facing down at the pan
    and the exhaust going up. Drawn the right way up it measures nothing.

    The flip is a rotation of pi about world X, which maps (x, y, z) to (x, -y, -z) and then
    adds the group location. So the location has to put y back (loc_y = 2 * CTR_Y) and lift the
    stack until the prop plane clears the pan — hence the arithmetic rather than a guessed
    number: the prop disc is the lowest thing on the inverted aircraft that matters."""
    D.ensure()
    P.kitchen_scale(D.CTR_X - 90, D.CTR_Y - 70, FLOOR, ang=-4, reading=reading)
    loc_z = PAN_Z + PROP_CLEAR + 11.3      # 11.3 = |Z_PROP| + blade thickness, flipped
    post_top = loc_z - D.Z_DECK            # where the inverted top plate ends up
    P.post(D.CTR_X, D.CTR_Y, PAN_Z, h=post_top - PAN_Z, top=42, base=96)
    objs = []
    objs += D.frame(z=0, front_mark=True)
    objs += D.motors_all(z=0, leads=False, props=props)
    objs += D.devkit() + D.mpu6050() + D.mt3608() + D.mosfet_board()
    objs += D.motor_wires_to_board() + D.gate_wires() + D.i2c_wires()
    objs += D.power_tree(battery=True)
    g = D._group([o for o in objs if o is not None], 'inverted')
    g.rotation_euler = (math.pi, 0, 0)
    g.location = (0, 2 * D.CTR_Y * MM, loc_z * MM)
    # two rubber bands over the CENTRE PLATES only — never over an arm, never over a motor
    for dy in (-9, 9):
        P.rubber_band(D.CTR_X, D.CTR_Y + dy, post_top - 6, 27, 5.0)
    # the 30 cm backup line, deliberately slack: taut, it would falsify the reading
    P.tether([(D.CTR_X + 18, D.CTR_Y + 20, post_top + 4),
              (D.CTR_X + 60, D.CTR_Y + 96, FLOOR + 54),
              (D.CTR_X + 54, D.CTR_Y + 108, FLOOR + 6),
              (D.CTR_X - 10, D.CTR_Y + 92, FLOOR + 3)])
    L.anchor('pan', (D.CTR_X - 20, D.CTR_Y - 40, PAN_Z + 2))
    L.anchor('rig', (D.CTR_X, D.CTR_Y, PAN_Z + 40))
    L.anchor('bands', (D.CTR_X, D.CTR_Y, post_top - 2))
    L.anchor('line', _near((D.CTR_X + 56, D.CTR_Y + 104, FLOOR + 26)))
    L.anchor('display', (D.CTR_X - 10, D.CTR_Y - 62, PAN_Z + 2))
    L.anchor('propdisc', (D.POS['front'][0], 2 * D.CTR_Y - D.POS['front'][1],
                          loc_z - 11.3))


def s_p8_thrust():
    _studio()
    _bench(FLOOR, x0=-60, y0=-40, w=480, d=420)
    _thrust_rig(props=True, reading=3)
    P.tape_line(-40, 20, 420, 20, FLOOR + 0.4, 24)
    L.anchor('tape', _near((330, 20, FLOOR + 2)))
    L.camera_fit(subject='rig', azimuth=46, elevation=22, lens=58)


def s_p8_upload_flight():
    """Armed at about 30 %, bare shafts turning, and one arm tip lifted 2–3 cm with a PENCIL.
    A finger there is exactly the thing the card forbids."""
    _studio()
    _bench(FLOOR, x0=-50, y0=-50, w=500, d=400)
    zf = FLOOR - D.Z_PLATE
    _drone_on_bench(zf, props=False, battery=True,
                    spin=('front', 'back', 'left', 'right'))
    T.pencil(D.POS['front'][0] - 40, D.CTR_Y - 30, FLOOR + 4, ang=26, tilt=-9)
    # the camera sits at +x/-y, so anything placed at -y is the nearest thing to the lens
    # and swells by perspective alone. The phone goes off to the side at the SAME depth
    # as the aircraft instead — perpendicular to the view axis, not in front of it.
    P.phone(246, 196, FLOOR, ang=-16, tilt=56, ui='drive')
    _usb_aside(zf)
    _drone_anchors(zf)
    L.anchor('pencil', (D.POS['front'][0] - 6, D.CTR_Y - 12, FLOOR + 12))
    L.anchor('lifted', (D.POS['front'][0], D.CTR_Y, zf + D.Z_PLATE_TOP + 18))
    L.anchor('phone', _near((282, 254, FLOOR + 76), 0.7))
    L.camera_fit(subject='drone', azimuth=48, elevation=28, lens=58)


def _flight(hover=170, spectator=True):
    """The only two scenes where props are fitted. The tether lies SLACK on the floor and the
    anchor is a flat weight on a taped X — never a bottle, never furniture, never a loop round
    an arm. There are no prop guards in this kit, so none are drawn."""
    D.ensure()
    L.ground(z=FLOOR, shadow_only=False, colour='#cec2ad', size=4200)
    zf = FLOOR + hover - D.Z_FOOT
    objs = []
    objs += D.frame(z=zf, front_mark=True)
    objs += D.motors_all(z=zf, leads=False, props=True)
    objs += D.devkit(dz=zf) + D.mpu6050(dz=zf) + D.mt3608(dz=zf) + D.mosfet_board(dz=zf)
    objs += D.motor_wires_to_board(zf) + D.gate_wires(zf) + D.i2c_wires(zf)
    objs += D.power_tree(zf, battery=True)
    # the flat anchor on its taped X, 40 cm away, with the line lying slack along the floor
    # the flat anchor sits beside the taped X rather than on top of it, so the mark the card
    # tells the student to lay down is actually visible
    box(292, 262, FLOOR, 68, 68, 12, D.M['grommet'], bevel=2.0, name='anchor')
    P.tape_line(216, 190, 300, 274, FLOOR + 0.3, 16)
    P.tape_line(300, 190, 216, 274, FLOOR + 0.3, 16)
    # SLACK, and visibly so: the line drops to the floor well short of the anchor and lies along
    # it. A cord stretched straight from aircraft to anchor is both wrong and dangerous, and it
    # is the first thing a reader would copy.
    P.tether([(D.CTR_X, D.CTR_Y, zf + D.Z_MOSFET - 6),
              (D.CTR_X + 26, D.CTR_Y + 34, FLOOR + hover * 0.35),
              (200, 200, FLOOR + 4),
              (250, 236, FLOOR + 2),
              (296, 262, FLOOR + 13)])
    if spectator:
        P.tape_line(-90, -40, 430, -40, FLOOR + 0.3, 24)
    L.anchor('gap', (D.CTR_X - 40, D.CTR_Y - 40, FLOOR + hover / 2))
    L.anchor('slack', (216, 212, FLOOR + 8))
    L.anchor('anchor', (326, 296, FLOOR + 14))
    L.anchor('drone', (D.CTR_X, D.CTR_Y, zf + D.Z_DECK + 8))
    L.anchor('props', (D.POS['front'][0], D.POS['front'][1], zf + D.Z_PROP + 4))
    if spectator:
        L.anchor('line', _near((300, -40, FLOOR + 2)))
    return zf


def s_p8_hover():
    _studio()
    zf = _flight(hover=180)
    # the camera sits at +x/-y, so anything placed at -y is the nearest thing to the lens
    # and swells by perspective alone. The phone goes off to the side at the SAME depth
    # as the aircraft instead — perpendicular to the view axis, not in front of it.
    P.phone(272, 236, FLOOR, ang=-18, tilt=58, ui='drive')
    L.anchor('phone', _near((308, 294, FLOOR + 76), 0.7))
    L.camera_fit(subject='drone', azimuth=48, elevation=22, lens=58)


def s_p8_post_flight():
    """The shutdown order, readable in one frame: the phone is already face-down, the PH2.0
    plug already out, and only then do the props come off into the teacher's box."""
    _studio()
    _bench(FLOOR, x0=-60, y0=-60, w=520, d=420)
    zf = FLOOR - D.Z_PLATE
    m = D.ensure()
    _drone_on_bench(zf, props=False, battery=False)
    # all four props already off and in the teacher's tray. An open box lid tips toward the
    # camera and hides the very thing the card is about, so this is a tray: the props are
    # visible in it, which is the whole point of the picture.
    P.tray(238, 178, FLOOR, w=180, d=118, cells=(2, 2), ang=-8)
    for i in range(4):
        D.prop(x=282 + (i % 2) * 88, y=210 + (i // 2) * 58, z=FLOOR - D.Z_PROP + 6,
               cw=(i < 2))
    # face-down: a pi rotation about X flips y and z, so the phone is placed by the far
    # corner it lands on rather than by the corner it started from
    P.phone(40, 186, FLOOR + 8, ang=-10, tilt=180, ui='drive')
    D.lipo(x=-30, y=210, z=FLOOR, orings=False)
    P.fireproof_bag(-40, 290, FLOOR, ang=-6)
    _drone_anchors(zf)
    L.anchor('propbox', _near((328, 237, FLOOR + 20)))
    L.anchor('phone', _near((76, 112, FLOOR + 10)))
    L.anchor('cell', _near((-4, 225, FLOOR + 9)))
    L.anchor('motor', (D.POS['back'][0], D.POS['back'][1], zf + D.Z_CAN + 12))
    L.camera_fit(subject='drone', azimuth=46, elevation=34, lens=56)


# ================================================================ TASK 2
def s_p8_t2_startup():
    """The Task 2 bench before anything is soldered: bare frame, loose parts, the empty
    perfboard, and the safety kit already out."""
    _studio(1.05)
    _bench(FLOOR, x0=-60, y0=-60, w=520, d=420)
    D.ensure()
    zf = FLOOR - D.Z_PLATE
    D.frame(z=zf, front_mark=True)
    D.mosfet_board(z=FLOOR, x=214, y=48, foam=False, channels=0, up=True)
    T.iron_stand(206, 186, FLOOR)
    T.soldering_iron(262, 272, FLOOR + 75, ang=90, tilt=16)
    T.solder_spool(248, 148, FLOOR)
    T.goggles(58, 248, FLOOR, ang=-12)
    P.fireproof_bag(16, 196, FLOOR, ang=-6)
    P.lidded_box(272, 226, FLOOR, 108, 82, 42, ang=-10)
    L.anchor('frame', (D.CTR_X, D.CTR_Y, FLOOR + 16))
    L.anchor('blank', (239, 68, FLOOR + 4))
    L.anchor('iron', _near((262, 224, FLOOR + 52), 0.7))
    L.anchor('goggles', _near((104, 262, FLOOR + 18), 0.7))
    L.camera_fit(subject='frame', azimuth=46, elevation=36, lens=56)


def _board_close(channels, iron=True, meter=False, reading=3):
    """The perfboard alone, big in frame — the shape all four soldering cards share."""
    _studio(1.05)
    _bench(FLOOR, x0=-30, y0=-40, w=420, d=320)
    D.ensure()
    D.mosfet_board(z=FLOOR, x=40, y=90, foam=False, channels=channels, up=True)
    if iron:
        # tip on channel 1, body running AWAY from the lens. Placed at -y the iron is the
        # nearest thing to the camera and swells until the 50 mm board it is working on is a
        # detail in the corner.
        T.soldering_iron(58, 116, FLOOR + 24, ang=48, tilt=18)
        T.solder_spool(196, 186, FLOOR)
    if meter:
        # the meter body is 132 mm against a 50 mm board, so it is allowed to run off the
        # frame; what has to be in shot is where its probes land, and that is what the
        # callout points at
        P.multimeter(180, 216, FLOOR, ang=-122)
    L.anchor('board', (40 + D.MOSFET_W / 2, 90 + D.MOSFET_D / 2, FLOOR + 4))
    L.anchor('ch1', (40 + D.CH_X0 + 5, 90 + 14, FLOOR + 6))
    L.anchor('gate1', (40 + D.CH_X0 + 5, 90 + D.PAD_GATE_DY, FLOOR + 1))
    L.anchor('mplus1', (40 + D.CH_X0 + 5, 90 + D.PAD_MPLUS_DY, FLOOR + 1))
    L.anchor('rails', (60, 90 + D.RAIL_BAT_DY, FLOOR + 1))
    L.anchor('rail_gnd', (60, 90 + D.RAIL_GND_DY, FLOOR + 1))
    if meter:
        L.anchor('meter', (98, 128, FLOOR + 8))
    # _board_close is a helper, not a scene function, so the subject-assignment sweep skipped
    # it and it inherited the previous scene's subject — an anchor that does not exist here.
    # All three soldering figures then died on a KeyError and silently kept their old
    # preview renders, which is why they looked untouched.
    L.camera_fit(subject='board', azimuth=44, elevation=40, lens=60)


def s_p8_t2_solder1():
    _board_close(channels=1, iron=True)


def s_p8_t2_check1():
    _board_close(channels=1, iron=False, meter=True)


def s_p8_t2_solder24():
    _board_close(channels=4, iron=True)


def s_p8_t2_tune():
    """The MT3608 on the bench with the meter on its OUT pins and a screwdriver on the pot.
    Nothing else is powered: this is a bench trim, not a flight."""
    _studio(1.05)
    _bench(FLOOR, x0=-30, y0=-40, w=420, d=320)
    m = D.ensure()
    D.mt3608(z=FLOOR, x=60, y=110)
    T.screwdriver(60 + 29, 110 + 12, FLOOR + D.MT_T + 34, ang=0, tilt=-90)
    P.multimeter(190, 224, FLOOR, ang=-124)
    D.lipo(x=8, y=166, z=FLOOR, orings=False)
    L.anchor('pot', (60 + 29, 110 + 12, FLOOR + 10))
    L.anchor('out', (60 + D.MT_W - 4, 110 + 4, FLOOR + 6))
    L.anchor('meter', (110, 140, FLOOR + 8))
    L.anchor('cell', (34, 181, FLOOR + 9))
    L.camera_fit(subject='out', azimuth=44, elevation=38, lens=63)


def s_p8_t2_mount():
    s_p8_mount()


def s_p8_t2_pre_power():
    s_p8_pre_power()


def s_p8_t2_spin():
    s_p8_spin()


def s_p8_t2_thrust():
    _studio()
    _bench(FLOOR, x0=-60, y0=-40, w=480, d=420)
    _thrust_rig(props=True, reading=3)
    P.tape_line(-40, 20, 420, 20, FLOOR + 0.4, 24)
    # the camera sits at +x/-y, so anything placed at -y is the nearest thing to the lens
    # and swells by perspective alone. The phone goes off to the side at the SAME depth
    # as the aircraft instead — perpendicular to the view axis, not in front of it.
    P.phone(258, 214, FLOOR, ang=-16, tilt=56, ui='drive')
    L.anchor('tape', _near((330, 20, FLOOR + 2)))
    L.anchor('phone', _near((294, 272, FLOOR + 76), 0.7))
    L.camera_fit(subject='rig', azimuth=46, elevation=22, lens=58)


def s_p8_t2_choices():
    """The tuning bench: laptop open on the sketch, drone propless beside it, cell in the bag
    and the prop box shut."""
    _studio()
    _bench(FLOOR, x0=-60, y0=-60, w=560, d=430)
    zf = FLOOR - D.Z_PLATE
    m = D.ensure()
    _drone_on_bench(zf, props=False, battery=False)
    T.laptop(268, 250, FLOOR, ang=-16, lid=102, screen='code')
    tube([(D.DEVKIT_XY[0] + D.DEVKIT_W + 4, D.CTR_Y, zf + D.Z_DECK + 4),
          (240, 70, FLOOR + 26), (300, 180, FLOOR + 12), (318, 258, FLOOR + 6)],
         1.6, m['w_black'], name='usb')
    P.fireproof_bag(20, 300, FLOOR, ang=-8)
    P.lidded_box(430, 30, FLOOR, 120, 90, 44, ang=-12)
    _drone_anchors(zf)
    L.anchor('screen', _near((382, 398, FLOOR + 106)))
    L.anchor('bag', _near((95, 352, FLOOR + 20)))
    L.anchor('propbox', _near((490, 75, FLOOR + 30)))
    L.camera_fit(subject='drone', azimuth=48, elevation=32, lens=56)


def s_p8_t2_hover():
    _studio()
    zf = _flight(hover=200)
    # the camera sits at +x/-y, so anything placed at -y is the nearest thing to the lens
    # and swells by perspective alone. The phone goes off to the side at the SAME depth
    # as the aircraft instead — perpendicular to the view axis, not in front of it.
    P.phone(272, 236, FLOOR, ang=-18, tilt=58, ui='drive')
    L.anchor('phone', _near((308, 294, FLOOR + 76), 0.7))
    L.camera_fit(subject='drone', azimuth=50, elevation=24, lens=58)


def s_p8_t2_sequence():
    """The flight sequence laid out as four physical cards on the bench beside the drone, so
    the order is an object rather than a paragraph. The numerals are composited."""
    _studio(1.05)
    _bench(FLOOR, x0=-50, y0=-60, w=520, d=430)
    zf = FLOOR - D.Z_PLATE
    _drone_on_bench(zf, props=False, battery=False)
    for i, by in enumerate((-40.0, 46.0, 132.0, 218.0)):
        T.rules_card(340, by, FLOOR, 96, 66, ang=-5 + i * 3)
        L.anchor('beat%d' % (i + 1), (388, by + 33, FLOOR + 1))
    _drone_anchors(zf)
    L.camera_fit(subject='drone', azimuth=48, elevation=38, lens=56)


def s_p8_t2_signature():
    _studio()
    zf = _flight(hover=230)
    # the camera sits at +x/-y, so anything placed at -y is the nearest thing to the lens
    # and swells by perspective alone. The phone goes off to the side at the SAME depth
    # as the aircraft instead — perpendicular to the view axis, not in front of it.
    P.phone(280, 244, FLOOR, ang=-18, tilt=58, ui='drive')
    P.cone(-90, 250, FLOOR)
    P.cone(60, -60, FLOOR)
    L.anchor('phone', _near((316, 302, FLOOR + 76), 0.7))
    L.anchor('course', _near((-90, 250, FLOOR + 62)))
    L.camera_fit(subject='drone', azimuth=50, elevation=26, lens=58)


def s_p8_t3_planner():
    """The planning card: the finished aircraft on the bench with a blank sheet and a pencil
    beside it. Nothing is happening — that is the point of a planner."""
    _studio(1.05)
    _bench(FLOOR, x0=-50, y0=-60, w=500, d=420)
    zf = FLOOR - D.Z_PLATE
    _drone_on_bench(zf, props=False, battery=False)
    T.rules_card(320, 40, FLOOR, 150, 200, ang=-6)
    T.pencil(300, 20, FLOOR + 1, ang=64)
    P.lidded_box(400, 300, FLOOR, 120, 90, 44, ang=-10)
    _drone_anchors(zf)
    L.anchor('sheet', _near((395, 140, FLOOR + 1)))
    L.anchor('drone_done', (D.CTR_X, D.CTR_Y, zf + D.Z_DECK + 10))
    L.camera_fit(subject='drone_done', azimuth=46, elevation=38, lens=56)
