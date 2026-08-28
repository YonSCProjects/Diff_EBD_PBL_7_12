"""props.py — the objects Projects 5, 7 and 8 need that are not Project 4 hand tools.

Kept apart from tools.py on purpose: tools.py is the soldering bench, this is everything the
later projects put next to the car — a phone, slalom cones, the serial adapter, the camera.

Same two shaping rules as tools.py: lathe anything rotationally symmetric, sweep a side
profile for anything shaped in side view. Real sizes throughout, because a phone at the wrong
scale beside a 250 mm chassis is the fastest way to make a figure read as a cartoon.

  phone        71 x 146 x 8, screen carrying the actual control layout
  cone         95 mm slalom cone with a real flared foot
  ftdi         36 x 18 USB-to-serial adapter
  esp32_cam    40.5 x 27 board, OV2640 on its ribbon
"""
import math
import lib as L
import pcb as PCB
from lib import MM, box, cyl, prism_xz, tube, revolve, mat, hexcol

_M = None


def materials():
    global _M
    if _M is None:
        _M = dict(
            phone_body=mat('p_phone', hexcol('#23272d'), rough=0.36, metal=0.6),
            phone_glass=mat('p_pglass', hexcol('#0a0e14'), rough=0.06, clearcoat=1.0,
                            cc_rough=0.03),
            phone_ui=mat('p_pui', hexcol('#eef3f7'), rough=0.4,
                         emission=hexcol('#f2f6fa'), emission_strength=1.4),
            phone_btn=mat('p_pbtn', hexcol('#e0651a'), rough=0.4,
                          emission=hexcol('#e0651a'), emission_strength=1.0),
            phone_wifi=mat('p_pwifi', hexcol('#2f8fd0'), rough=0.4,
                           emission=hexcol('#3a9fe0'), emission_strength=1.5),
            phone_dark=mat('p_pdark', hexcol('#2a3038'), rough=0.5),
            cone_orange=mat('p_cone', hexcol('#e2560f'), rough=0.6),
            cone_white=mat('p_conew', hexcol('#f2f4f6'), rough=0.62),
            ftdi_pcb=mat('p_ftdi', hexcol('#14544a'), rough=0.5, clearcoat=0.3, cc_rough=0.32),
            cam_pcb=mat('p_campcb', hexcol('#1d2126'), rough=0.5, clearcoat=0.3, cc_rough=0.32),
            cam_lens=mat('p_camlens', hexcol('#0b0e12'), rough=0.08, clearcoat=1.0, cc_rough=0.04),
            cam_barrel=mat('p_cambar', hexcol('#1a1d21'), rough=0.55),
            ribbon=mat('p_ribbon', hexcol('#c8a06a'), rough=0.5),
            chrome=mat('p_chrome', hexcol('#c6cbd2'), rough=0.20, metal=1.0),
            brass=mat('p_brass', hexcol('#9c6d34'), rough=0.32, metal=1.0),
            dark=mat('p_dark', hexcol('#1a1d22'), rough=0.54),
            grey=mat('p_grey', hexcol('#3a4048'), rough=0.52),
            tape_line=mat('p_tapeline', hexcol('#15181c'), rough=0.72),
        )
    return _M


def reset():
    global _M
    _M = None


def _group(objs, name):
    import bpy
    g = bpy.data.objects.new(name, None)
    g.empty_display_size = 0.01
    bpy.context.collection.objects.link(g)
    for o in objs:
        if o is not None and o.parent is None:
            o.parent = g
    return g


# ---------------------------------------------------------------- the phone
def phone(x, y, z, ang=0.0, tilt=0.0, ui='drive'):
    """A phone lying screen-up. The screen is not a blank slab — it carries the control layout
    the student actually sees, because "press and hold to drive" is the point of the card.

      ui='drive'  four arrow pads around a stop pad
      ui='join'   a Wi-Fi fan over a network list, the top row selected
      ui='video'  a live-video panel above two drive pads (Project 7)
    """
    m = materials()
    W, D, T = 71.0, 146.0, 8.0
    parts = [box(0, 0, 0, W, D, T, m['phone_body'], bevel=2.4, name='ph_body'),
             box(1.6, 1.6, T, W - 3.2, D - 3.2, 0.4, m['phone_glass'], bevel=1.6, name='ph_glass')]
    sx, sy = 4.0, 8.0
    sw, sd = W - 8.0, D - 16.0
    zt = T + 0.45
    parts.append(box(sx, sy, zt, sw, sd, 0.25, m['phone_ui'], bevel=1.2, name='ph_screen'))
    cx, cy = sx + sw / 2, sy + sd / 2
    if ui == 'drive':
        pad, gap = 17.0, 3.0
        for dx, dy in ((0, 1), (0, -1), (-1, 0), (1, 0)):
            parts.append(box(cx - pad / 2 + dx * (pad + gap), cy - pad / 2 + dy * (pad + gap),
                             zt + 0.25, pad, pad, 1.1, m['phone_btn'], bevel=3.0, name='ph_pad'))
        parts.append(box(cx - 9, cy - 9, zt + 0.25, 18, 18, 1.0, m['phone_dark'],
                         bevel=3.0, name='ph_stop'))
        parts.append(box(sx + 5, sy + sd - 13, zt + 0.25, sw - 10, 8, 0.8, m['phone_wifi'],
                         bevel=2.0, name='ph_title'))
    elif ui == 'join':
        for i in range(3):                       # a Wi-Fi fan drawn as three widening bars
            w = 12 + i * 13
            parts.append(box(cx - w / 2, cy + 6 + i * 9, zt + 0.25, w, 4.0, 0.9,
                             m['phone_wifi'], bevel=1.6, name='ph_arc'))
        parts.append(cyl(cx, cy + 2, zt + 0.25, 3.2, 1.0, m['phone_wifi'], name='ph_dot'))
        for i in range(3):                       # the network list, ours picked out at the top
            parts.append(box(sx + 6, cy - 16 - i * 11, zt + 0.25, sw - 12, 7.0, 0.6,
                             m['phone_btn'] if i == 0 else m['phone_dark'],
                             bevel=1.6, name='ph_row'))
    elif ui == 'video':
        parts.append(box(sx + 4, cy + 2, zt + 0.25, sw - 8, sd / 2 - 8, 0.9,
                         m['phone_dark'], bevel=1.6, name='ph_video'))
        parts.append(cyl(cx, cy + sd / 4 - 3, zt + 1.15, 6.0, 0.8, m['phone_wifi'],
                         name='ph_play'))
        for dx in (-1, 1):
            parts.append(box(cx + dx * 20 - 15, cy - 32, zt + 0.25, 30, 22, 1.1,
                             m['phone_btn'], bevel=3.0, name='ph_pad'))
    g = _group(parts, 'phone')
    g.rotation_euler = (math.radians(tilt), 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


# ---------------------------------------------------------------- slalom cone
def cone(x, y, z, h=95.0):
    """A slalom cone. Lathed, so the flare at the foot is a real curve — a plain tapered
    cylinder reads as a party hat."""
    m = materials()
    profile = [(31, 0), (30, 3), (17, 6), (15, 10), (10.5, h * 0.45),
               (6.0, h * 0.78), (3.4, h - 4), (1.2, h)]
    parts = [revolve(profile, 0, 0, 0, m['cone_orange'], seg=48, name='cone'),
             cyl(0, 0, h * 0.44, 11.6, h * 0.16, m['cone_white'], name='cone_band')]
    g = _group(parts, 'cone_g')
    g.location = (x * MM, y * MM, z * MM)
    return g


# ---------------------------------------------------------------- serial adapter
def ftdi(x, y, z, ang=0.0):
    """A USB-to-serial adapter — the thing that makes an ESP32-CAM uploadable at all."""
    m = materials()
    parts = [box(0, 0, 0, 36.0, 18.0, 1.4, m['ftdi_pcb'], bevel=0.5, name='ftdi'),
             PCB.face(0, 0, 1.42, 36.0, 18.0, PCB.tex_mat('silk_ftdi', PCB.silk_ftdi()),
                      name='ftdi_silk'),
             box(1.5, 3.0, 1.4, 13.0, 12.0, 6.5, m['chrome'], bevel=0.6, name='ftdi_usb'),
             box(25.0, 2.0, 1.4, 4.5, 14.0, 2.4, m['dark'], bevel=0.3, name='ftdi_jmp')]
    for i in range(6):
        parts.append(box(19.0, 1.6 + i * 2.54, 1.4, 1.6, 1.6, 8.0, m['brass'],
                         bevel=0, name='ftdi_pin'))
    g = _group(parts, 'ftdi_g')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


# ---------------------------------------------------------------- ESP32-CAM
def esp32_cam(x, y, z, ang=0.0, tilt=0.0, ribbon_up=True):
    """ESP32-CAM: 40.5 x 27 board, shield can, microSD slot, OV2640 on its ribbon.

    The lens stands off the board on its barrel. Flush against the PCB it reads as a sticker,
    and every Project 7 card asks the student to aim it."""
    m = materials()
    parts = [box(0, 0, 0, 40.5, 27.0, 1.4, m['cam_pcb'], bevel=0.5, name='cam_pcb'),
             PCB.face(0, 0, 1.42, 40.5, 27.0, PCB.tex_mat('silk_cam', PCB.silk_esp32cam()),
                      name='cam_silk'),
             box(4.0, 4.0, 1.4, 22.0, 19.0, 2.4, m['chrome'], bevel=0.3, name='cam_can'),
             box(27.0, 3.0, 1.4, 12.0, 14.0, 2.0, m['grey'], bevel=0.3, name='cam_sd')]
    for i in range(8):
        for yy in (0.8, 24.6):
            parts.append(box(3.0 + i * 2.54, yy, -2.2, 1.6, 1.6, 2.2, m['brass'],
                             bevel=0, name='cam_pin'))
    lens = [box(0, 0, 0, 8.5, 8.5, 1.6, m['cam_pcb'], bevel=0.3, name='ov_pcb'),
            cyl(4.25, 4.25, 1.6, 4.2, 6.0, m['cam_barrel'], name='ov_barrel'),
            cyl(4.25, 4.25, 7.6, 3.1, 0.9, m['cam_lens'], name='ov_lens')]
    cg = _group(lens, 'ov2640')
    if ribbon_up:
        parts.append(box(14.0, 9.0, 3.8, 9.0, 0.6, 11.0, m['ribbon'], bevel=0.2, name='cam_ribbon'))
        cg.location = (14.0 * MM, 9.0 * MM, 14.5 * MM)
        # +84, not -84: the lens sits on the sub-board's +z face, and a negative rotation turns
        # that face away from the camera — the figure then shows the blank back of the lens
        # board, which is the one part of an ESP32-CAM a student has to be able to find.
        cg.rotation_euler = (math.radians(84), 0, 0)
    else:
        parts.append(box(14.0, 9.0, 3.8, 9.0, 12.0, 0.6, m['ribbon'], bevel=0.2, name='cam_ribbon'))
        cg.location = (14.0 * MM, 20.0 * MM, 3.8 * MM)
    g = _group(parts, 'esp32cam')
    cg.parent = g
    g.rotation_euler = (math.radians(tilt), 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


# ---------------------------------------------------------------- floor tape
def tape_line(x0, y0, x1, y1, z, width=19.0):
    """A strip of black electrical tape on the floor — the line the Project 4 car follows."""
    m = materials()
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    # box() bakes the scale into the mesh and puts the object origin at the box CENTRE, so a
    # rotation turns about the midpoint — place the midpoint, not the start.
    b = box(0, 0, 0, length, width, 0.3, m['tape_line'], bevel=0, name='tapeline')
    b.rotation_euler = (0, 0, math.atan2(dy, dx))
    b.location = ((x0 + x1) / 2 * MM, (y0 + y1) / 2 * MM, (z + 0.15) * MM)
    return b


# ---------------------------------------------------------------- Project 7 power parts
def buck(x, y, z, ang=0.0):
    """An adjustable buck converter, the part that gives the camera its own clean 5 V.
    Two screw terminals, an inductor and the trim pot — enough that it reads as itself."""
    m = materials()
    parts = [box(0, 0, 0, 43.0, 21.0, 1.4, m['ftdi_pcb'], bevel=0.5, name='buck'),
             box(2.0, 3.0, 1.4, 10.0, 15.0, 9.5, m['phone_wifi'], bevel=0.5, name='buck_in'),
             box(31.0, 3.0, 1.4, 10.0, 15.0, 9.5, m['cone_orange'], bevel=0.5, name='buck_out'),
             cyl(21.0, 8.0, 1.4, 5.2, 5.0, m['dark'], name='buck_coil'),
             cyl(21.0, 17.0, 1.4, 3.0, 4.4, m['phone_btn'], name='buck_pot')]
    g = _group(parts, 'buck_g')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def capacitor(x, y, z, r=6.3, h=12.0, ang=0.0):
    """An electrolytic can standing on the plate, white stripe down the minus side — the card
    makes the student read that stripe, so it has to be visible."""
    m = materials()
    parts = [cyl(0, 0, 0, r, h, m['phone_wifi'], name='cap_body', seg=40),
             cyl(0, 0, h, r * 0.92, 0.5, m['grey'], name='cap_top', seg=40),
             box(-r - 0.2, -1.9, 0.6, 0.6, 3.8, h - 1.6, m['cone_white'], bevel=0, name='cap_stripe')]
    for dx in (-2.5, 2.5):
        parts.append(cyl(dx, 0, -4.0, 0.35, 4.2, m['brass'], name='cap_leg'))
    g = _group(parts, 'cap_g')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def wall(x, y, z, w=12.0, d=200.0, h=180.0):
    """A barrier the driver cannot see past — the whole point of Project 7's last card."""
    m = mat('p_wall', hexcol('#9aa7b2'), rough=0.86)
    return box(x, y, z, w, d, h, m, bevel=1.5, name='wall')


# ---------------------------------------------------------------- Project 8 bench props
def kitchen_scale(x, y, z, ang=0.0, reading=3):
    """A flat digital kitchen scale. The display is the content — every card that puts a drone
    on a scale is putting it there to read a number — so the panel carries real digit bars."""
    m = materials()
    parts = [box(0, 0, 0, 180, 140, 9, m['phone_body'], bevel=2.2, name='scale_body'),
             box(6, 30, 9, 168, 106, 1.2, m['chrome'], bevel=1.2, name='scale_pan'),
             box(40, 4, 9, 100, 22, 0.8, m['phone_ui'], bevel=1.0, name='scale_lcd')]
    # digits as seven-segment-ish bars, right to left
    for d in range(max(1, reading)):
        dx = 122 - d * 18
        parts.append(box(dx, 9, 9.9, 3.0, 12.0, 0.5, m['dark'], bevel=0, name='digit'))
        parts.append(box(dx + 8, 9, 9.9, 3.0, 12.0, 0.5, m['dark'], bevel=0, name='digit'))
        for yy in (8.4, 14.2, 20.0):
            parts.append(box(dx, yy, 9.9, 11.0, 2.6, 0.5, m['dark'], bevel=0, name='digit'))
    for bx in (56, 76):
        parts.append(cyl(bx, 16, 9, 4.0, 1.4, m['grey'], name='scale_btn'))
    g = _group(parts, 'scale')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def tray(x, y, z, w=300.0, d=210.0, cells=(3, 2), ang=0.0):
    """A parts tray with divider walls. The compartments are what make a pile of loose parts
    read as 'laid out in named groups' rather than as a mess on the bench."""
    m = materials()
    wall, h = 2.4, 26.0
    parts = [box(0, 0, 0, w, d, 3.0, m['grey'], bevel=1.2, name='tray_floor'),
             box(0, 0, 0, w, wall, h, m['grey'], bevel=0.8, name='tray_wall'),
             box(0, d - wall, 0, w, wall, h, m['grey'], bevel=0.8, name='tray_wall'),
             box(0, 0, 0, wall, d, h, m['grey'], bevel=0.8, name='tray_wall'),
             box(w - wall, 0, 0, wall, d, h, m['grey'], bevel=0.8, name='tray_wall')]
    for i in range(1, cells[0]):
        parts.append(box(w * i / cells[0], 0, 0, wall, d, h - 6, m['grey'], bevel=0.8,
                         name='tray_div'))
    for j in range(1, cells[1]):
        parts.append(box(0, d * j / cells[1], 0, w, wall, h - 6, m['grey'], bevel=0.8,
                         name='tray_div'))
    g = _group(parts, 'tray')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def multimeter(x, y, z, ang=0.0, leads=True):
    """A handheld meter with its probes. Used in Project 8 to read the MT3608 output while it
    is being trimmed, so the dial and the display both have to be legible."""
    m = materials()
    # a pocket meter, not a bench instrument: at 90 x 165 it swamped a 50 x 40 perfboard
    # and a 100 mm airframe in every figure it appeared in
    parts = [box(0, 0, 0, 72, 132, 27, m['cone_orange'], bevel=2.6, name='dmm_body'),
             box(3, 80, 27, 66, 45, 1.0, m['phone_ui'], bevel=1.4, name='dmm_lcd'),
             cyl(36, 50, 27, 21, 2.6, m['dark'], name='dmm_dial', seg=40),
             box(34.5, 50, 29.6, 3.4, 18.0, 1.2, m['cone_white'], bevel=0,
                 name='dmm_pointer')]
    for i in range(3):
        parts.append(cyl(16 + i * 20, 11, 27, 3.6, 2.0, m['grey'], name='dmm_jack'))
    for d in range(3):
        dx = 48 - d * 15
        parts.append(box(dx, 94, 28.1, 2.6, 11.0, 0.5, m['dark'], bevel=0, name='dmm_digit'))
        parts.append(box(dx + 7.5, 94, 28.1, 2.6, 11.0, 0.5, m['dark'], bevel=0,
                         name='dmm_digit'))
        for yy in (93, 99, 105):
            parts.append(box(dx, yy, 28.1, 10.0, 2.4, 0.5, m['dark'], bevel=0,
                             name='dmm_digit'))
    if leads:
        for i, col in enumerate((m['cone_orange'], m['dark'])):
            sx = 16 + i * 40
            parts.append(tube([(sx, 8, 27), (sx - 24 + i * 48, -32, 16),
                               (sx - 48 + i * 104, -78, 5)], 1.6, col, name='dmm_lead'))
    g = _group(parts, 'dmm')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def tether(pts, r=0.8):
    """A light line from an anchor point down to the aircraft — the safety habit that lets a
    first hover happen at all."""
    return tube(pts, r, materials()['cone_white'], name='tether')


def contract_card(x, y, z, ang=0.0, w=110.0, d=76.0):
    """The safety-contract card with its two signature lines and a pen lying across it."""
    m = materials()
    parts = [box(0, 0, 0, w, d, 0.5, m['cone_white'], bevel=0, name='contract'),
             box(6, d - 12, 0.5, w - 12, 4.0, 0.12, m['cone_orange'], bevel=0, name='c_title')]
    for i in range(4):
        parts.append(box(8, d - 26 - i * 8, 0.5, w - 30 - (i % 2) * 14, 2.2, 0.12,
                         m['grey'], bevel=0, name='c_line'))
    for i in range(2):
        parts.append(box(10 + i * (w / 2 - 6), 8, 0.5, w / 2 - 22, 1.4, 0.12, m['dark'],
                         bevel=0, name='c_sigline'))
    g = _group(parts, 'contract_g')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def lidded_box(x, y, z, w=112.0, d=82.0, h=42.0, ang=0.0, open_lid=False, colour=None):
    """The teacher's closed box. Half the Project 8 cards are about what is NOT on the drone,
    and a shut box with the props inside says that better than any label."""
    m = materials()
    body = colour or m['cone_orange']
    parts = [box(0, 0, 0, w, d, h, body, bevel=2.0, name='box_body'),
             box(-2, -2, h, w + 4, d + 4, 5.0, m['dark'], bevel=1.4, name='box_lid')]
    if open_lid:
        parts[-1].rotation_euler = (math.radians(-104), 0, 0)
        parts[-1].location = (((w + 4) / 2 - 2) * MM, -2 * MM, (h + 2.5) * MM)
    parts.append(box(w * 0.28, -0.6, h * 0.45, w * 0.44, 1.2, 14.0, m['cone_white'],
                     bevel=0, name='box_label'))
    g = _group(parts, 'lidded_box')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def fireproof_bag(x, y, z, w=126.0, d=90.0, h=24.0, ang=0.0):
    """The zipped LiPo bag. In Project 8 the battery lives here except when the teacher has it,
    so the bag appearing in a figure is itself the safety statement."""
    m = materials()
    parts = [box(0, 0, 0, w, d, h, m['dark'], bevel=5.0, name='bag'),
             box(6, d - 5, h - 4, w - 12, 3.0, 2.0, m['cone_orange'], bevel=0.6, name='zip'),
             box(w * 0.3, -0.8, h * 0.3, w * 0.4, 1.4, 11.0, m['cone_orange'],
                 bevel=0, name='bag_label')]
    g = _group(parts, 'bag')
    g.rotation_euler = (0, 0, math.radians(ang))
    g.location = (x * MM, y * MM, z * MM)
    return g


def spin_disc(x, y, z, r, m=None, alpha=True):
    """A faint disc standing for a turning shaft or rotor. Motion cannot be rendered, so this is
    the honest substitute: a translucent sweep exactly the radius of what is actually moving."""
    mm = materials()
    return cyl(x, y, z, r, 0.6, m or mm['phone_wifi'], name='spin', seg=48)


def post(x, y, z, h=110.0, top=42.0, base=90.0):
    """The weighted post the drone is strapped to, upside down, for the thrust test. The top is
    deliberately narrow and the base wide: a tall thin post that can tip over is the hazard the
    card is trying to remove."""
    m = materials()
    parts = [cyl(0, 0, 0, base / 2, 16.0, m['dark'], name='post_base', seg=40),
             cyl(0, 0, 16.0, 16.0, h - 30.0, m['grey'], name='post_stem', seg=32),
             cyl(0, 0, h - 14.0, top / 2, 14.0, m['dark'], name='post_head', seg=36)]
    g = _group(parts, 'post_g')
    g.location = (x * MM, y * MM, z * MM)
    return g


def rubber_band(cx, cy, z, rx, ry, thick=2.6, height=3.0):
    """A band stretched over the two centre plates. One mesh, so the ink pass draws a band and
    not a chain of little links."""
    m = materials()
    return L.ribbon(L.ellipse_pts(cx, cy, rx, ry, n=48), thick, z + height,
                    m['dark'], name='band', closed=True, thickness=height)
