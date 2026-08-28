"""scenes_p5.py — Project 5 (Wi-Fi remote-controlled car): the same car, a new brain.

Same contract as scenes_p4.py: build hardware only, register named anchors, let compose.js hang
the Hebrew on them afterwards. Scene keys map onto the figure names the CARDS ALREADY EMBED —
see PUBLISH in build_p5.sh.

The through-line of every figure here is that the CAR DOES NOT CHANGE. Project 4's chassis,
motors, wheels, driver and battery are all still there; only the board on the velcro is
different and the wires that reach it. Figures that redraw the car differently would quietly
teach the opposite of what the cards say.
"""
import math
import lib as L
import p4_car as C
import tools as T
import props as P
from lib import MM, box, cyl, mat, hexcol

CAR_CENTRE = (148.0, 110.0, -10.0)
ESP_X, ESP_Y = C.BRAIN_X + 9, C.BRAIN_Y + 13


def _studio(strength=1.0):
    L.studio(strength=strength)


def _bench(z, x0=-40, y0=-30, w=420, d=320, colour='#a89a88'):
    """The work surface. A scene with a bench must NOT also call L.ground() — two coplanar
    surfaces z-fight and the shadow catcher wins, leaving a black bench-shaped hole."""
    m = mat('bench', hexcol(colour), rough=0.72)
    return box(x0, y0, z - 7, w, d, 7, m, bevel=1.5, name='bench')


def _car_anchors(z=0.0):
    L.anchor('esp32', (ESP_X + 26, ESP_Y + 14, z + C.PLATE_T + 6 + C.ESP_STANDOFF))
    # +22/+16 lands inside the L298N's heatsink, the tallest thing on that board.
    L.anchor('driver', (C.DRV_X + 8, C.DRV_Y + 30, z + C.PLATE_T + 20))
    L.anchor('battery', (C.BAT_X + 55, C.BAT_Y + 30, z + C.PLATE_T + 17))
    # Not the plate's centre: the Uno, the driver and the battery box all sit there, so a
    # whole-vehicle label pointed at a board instead of at the plate. This corner stays bare.
    L.anchor('plate', (C.PLATE_X0 + 26, C.PLATE_Y0 + 20, z + C.PLATE_T))
    # at the axle centre this sat inside its own tyre
    L.anchor('wheel_front', (C.AXLE_F, 1.0, z + C.Z_AXLE - 10))
    # the sensors bolt under a 9 mm opaque deck; anchor on the nose above them
    L.anchor('sensor_left', (C.SENS_L[0] - 14, C.SENS_L[1], z + C.PLATE_T + 1))


# ---------------------------------------------------------------- M1 — meet the ESP32
def s_meet_esp32():
    """The board alone on the mat, big enough that the six-in-a-row is countable. This is the
    only figure in the set where the car is absent, because the card is an introduction."""
    _studio(1.05)
    _bench(0, x0=-16, y0=-14, w=240, d=200)
    T.heat_mat(6, 10, 0, 190, 150)
    C.ensure()
    # the board on its own, rotated off-axis so it reads as an object rather than a diagram
    # the pins now hang below the board, as they do on the real DevKit, so the board has to
    # stand on them rather than lie flat on the mat
    g = C.esp32_devkit(z=0.0, velcro=False, dx=42 - C.BRAIN_X - 9, dy=72 - C.BRAIN_Y - 13,
                       dz=-C.PLATE_T + 1.4)
    ex, ey, ez = 42.0, 72.0, 9.9   # 1.4 board z + the 8.5 mm pin stand-off
    L.anchor('usb', (ex + 6, ey + 14, ez + 6))
    L.anchor('six', (ex + 6 + 8 * 2.9, ey + 1.6, ez + 4))
    L.anchor('can', (ex + 26, ey + 14, ez + 4))
    L.anchor('board', (ex + 26, ey + 14, ez + 2))
    L.camera((ex + 24, ey + 13, 10), 218, azimuth=57, elevation=29, lens=74)


# ---------------------------------------------------------------- M2 — swap the brain
def s_swap_brain():
    """The Uno lifted clear, the ESP32 coming down onto the same patch of velcro. Both boards
    in one frame is the whole argument of the card — nothing else about the car moves."""
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=True)
    C.ensure()
    C.chassis()
    C.sensor_holes()
    C.motors_all(leads=False)
    C.wheels_all()
    C.l298n()
    C.battery_box()
    C.ir_sensor('left')
    C.ir_sensor('right')
    # the velcro patch left bare on the brain zone
    box(C.BRAIN_X + 6, C.BRAIN_Y + 8, C.PLATE_T, 54, 40, 1.2, C.M['velcro'],
        bevel=0, name='velcro')
    # the Uno, lifted up and back — dz raises it, dy walks it off the tail
    C.arduino_uno(z=0.0, velcro=False, dx=4, dy=-74, dz=92)
    # the ESP32, on its way down onto the same velcro
    C.esp32_devkit(z=0.0, velcro=False, dx=-2, dy=0, dz=46)
    L.anchor('uno_off', (C.BRAIN_X + 40, C.BRAIN_Y - 74 + 30, C.PLATE_T + 92 + 8))
    # the board is held 46 mm up AND stands 8.5 mm on its own pins, so +4 was underneath it
    L.anchor('esp_down', (ESP_X + 24, ESP_Y + 14, C.PLATE_T + 46 + C.ESP_STANDOFF + 8.5))
    L.anchor('velcro', (C.BRAIN_X + 12, C.BRAIN_Y + 12, C.PLATE_T + 1.2))
    # (200, 110) is the middle of the deck, which is exactly where the driver and the battery
    # box sit -- the 'same car' label pointed straight into them. The bare nose corner is the
    # one patch of plate that stays plate in every P5 figure.
    L.anchor('plate', (C.PLATE_X0 + 26, C.PLATE_Y0 + 20, C.PLATE_T))
    # The lifted Uno is a 68 mm board hanging off one anchor point, so fitting on the anchors
    # alone cropped half of it away. Its footprint has to be in the must-see set.
    L.camera_fit(azimuth=44, elevation=28, lens=58, only=('esp_down','plate','uno_off'),
                 extra=L.bbox_pts(C.BRAIN_X + 2, C.BRAIN_Y - 76, C.PLATE_T + 90,
                                  C.BRAIN_X + 72, C.BRAIN_Y - 20, C.PLATE_T + 104)
                       + L.bbox_pts(C.PLATE_X0, C.PLATE_Y0, C.PLATE_T - 2,
                                    C.PLATE_X1, C.PLATE_Y1, C.PLATE_T + 20))


# ---------------------------------------------------------------- M3 — rewire to the ESP32
def s_rewire():
    """Six signal wires from the driver header into the six-in-a-row, plus the 5V/GND pair.
    The line sensors stay screwed on and unplugged — the card says so explicitly."""
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=True)
    C.car(brain='esp', wiring=True, leads=True)
    _car_anchors()
    L.anchor('six_wires', (ESP_X + 18, 62, C.PLATE_T + 14 + C.ESP_STANDOFF))
    L.anchor('power_pair', (ESP_X + 40, 150, C.PLATE_T + 13 + C.ESP_STANDOFF))
    L.camera_fit(azimuth=44, elevation=36, lens=60, only=('power_pair','sensor_left','six_wires'),
                 extra=L.bbox_pts(C.PLATE_X0 - 2, C.PLATE_Y0 - 2, C.PLATE_T - 4, C.PLATE_X1 + 2, C.PLATE_Y1 + 2, C.PLATE_T + 26))


# ---------------------------------------------------------------- M4 — upload over USB
def s_upload():
    """Wheels in the air on a riser, switch off, one USB cable to the laptop. The riser is not
    decoration: a car that drives off the bench during an upload is the failure this prevents."""
    _studio()
    BENCH_Z = -90.0                    # 38 mm of daylight under the wheels
    _bench(BENCH_Z, x0=-80, y0=-70, w=560, d=560)
    # two blocks under the clear centre band of the plate — the motors hug both long edges,
    # so anything wider than this band would be driven straight through a gearbox
    T.riser(100, 62, BENCH_Z, 50, 92, -BENCH_Z)
    T.riser(200, 62, BENCH_Z, 50, 92, -BENCH_Z)
    C.car(brain='esp', sensors=False, wiring=True)
    # ang=180 turns the screen toward the camera, which sits on the -y side
    T.laptop(296, 205, BENCH_Z, ang=8, lid=104, screen='code')
    C.ensure()
    from lib import tube
    # the cable drapes round the NEAR side of the car; routed behind it, it is invisible and
    # the figure loses the one thing the card is about
    tube([(ESP_X + 2, ESP_Y + 6, C.PLATE_T + 3),
          (120, 34, C.PLATE_T + 14),
          (250, 60, -46),
          (330, 200, -88),
          (340, 300, -88)], 1.7, C.M['w_black'], name='usb')
    _car_anchors()
    L.anchor('usb_cable', (250, 60, -46))
    # behind the open lid at (400, 330): the callout names what is ON the screen
    L.anchor('laptop', (296, 180, 10))
    # on the near block's front face, not on the seam between the two where the plate hides it
    L.anchor('riser', (125, 60, -50))
    L.camera((190, 190, -14), 1080, azimuth=52, elevation=28, lens=52)


# ---------------------------------------------------------------- M5 — the phone joins
def s_connect_phone():
    """The car has opened a network of its own and the phone is picking it out of the list.
    The Wi-Fi fan is composited, not modelled — radio is not a thing you can render."""
    _studio()
    _bench(C.Z_GROUND, x0=-60, y0=-70, w=520, d=380)
    C.car(brain='esp', sensors=False, wiring=True)
    P.phone(320, -46, C.Z_GROUND, ang=-14, tilt=56, ui='join')
    _car_anchors()
    L.anchor('phone', (348, -104, C.Z_GROUND + 74))
    L.anchor('air', (ESP_X + 26, ESP_Y + 14, C.PLATE_T + 40))
    L.camera((190, 66, 0), 820, azimuth=44, elevation=26, lens=56)


# ---------------------------------------------------------------- M6 — first drive
def s_first_drive():
    """On the floor, thumb on a pad, the car under way. Press and hold to move, let go to stop —
    the figure has to show a hand-held phone and a car that is clearly going somewhere."""
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=False, colour='#e6ded0', size=4200)
    C.car(brain='esp', sensors=False, wiring=True)
    P.phone(330, -66, C.Z_GROUND, ang=-18, tilt=58, ui='drive')
    _car_anchors()
    L.anchor('phone', (356, -124, C.Z_GROUND + 76))
    L.anchor('nose', (C.PLATE_X0 - 4, 110, C.PLATE_T))
    L.anchor('ahead', (C.PLATE_X0 - 130, 110, C.Z_GROUND + 3))
    L.anchor('air', (ESP_X + 26, ESP_Y + 14, C.PLATE_T + 40))
    L.camera((150, 60, -10), 930, azimuth=46, elevation=24, lens=56)


# ---------------------------------------------------------------- M7 — the course
def s_course():
    """A slalom the students lay out themselves. Four cones, the car threading the first gate."""
    _studio()
    L.ground(z=C.Z_GROUND, shadow_only=False, colour='#e6ded0', size=5200)
    for i, cx in enumerate((-120, 20, 160, 300)):
        P.cone(cx, -34 if i % 2 == 0 else 254, C.Z_GROUND)
    C.car(brain='esp', sensors=False, wiring=True)
    P.phone(430, 40, C.Z_GROUND, ang=-16, tilt=56, ui='drive')
    _car_anchors()
    L.anchor('cone', (20, 254, C.Z_GROUND + 62))
    L.anchor('gate', (20, 110, C.Z_GROUND + 6))
    L.anchor('phone', (458, -22, C.Z_GROUND + 76))
    L.camera((130, 110, -16), 1180, azimuth=50, elevation=36, lens=58)
