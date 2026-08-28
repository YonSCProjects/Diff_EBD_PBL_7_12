"""pcb.py — real-looking printed circuit boards.

The boards used to be coloured slabs with a couple of blocks on them: a teal rectangle stood for
an Arduino Uno, a red one for the L298N, a blue one for a line sensor. A student holding the real
part could not match it to the picture, which is the whole job of a build figure.

What makes a board recognisable is not polygon count. It is, in order: the silhouette, the two or
three big landmarks (the silver USB-B can on an Uno, the finned heatsink on an L298N, the blue
trimmer on a TCRT5000 carrier), and the white silkscreen — the pin numbers a student actually has
to read to follow the card.

So each board here is a real outline extruded to 1.6 mm, with its top face carrying a generated
silkscreen image and its landmarks modelled as separate parts. The silkscreen is drawn with PIL at
24 px/mm and cached in _blender/textures/; pin labels are set a little larger than true scale,
which is normal practice for a technical illustration and is what keeps them readable once the
figure is 620 px wide on a card.
"""
import os
import math
import bpy
import bmesh
from mathutils import Vector
from PIL import Image, ImageDraw, ImageFont

import lib as L
import cadparts as CAD
from lib import MM, box, cyl, mat, hexcol

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, 'textures')
PXMM = 24                                   # silkscreen resolution
_FONT = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
_FONT_R = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
for _f in (_FONT, _FONT_R):
    if not os.path.exists(_f):
        _FONT = _FONT_R = None
        break

_cache = {}


def _font(px, bold=True):
    if _FONT is None:
        return ImageFont.load_default()
    return ImageFont.truetype(_FONT if bold else _FONT_R, max(6, int(px)))


class Silk:
    """A tiny mm-space drawing surface. Everything is in board millimetres, y down from the top."""

    def __init__(self, w, d, base):
        self.w, self.d = w, d
        self.im = Image.new('RGB', (int(w * PXMM), int(d * PXMM)), base)
        self.dr = ImageDraw.Draw(self.im)

    def _p(self, x, y):
        return (x * PXMM, y * PXMM)

    def rect(self, x, y, w, h, fill=None, outline=None, width=0.22):
        self.dr.rectangle([self._p(x, y), self._p(x + w, y + h)],
                          fill=fill, outline=outline, width=max(1, int(width * PXMM)))

    def line(self, x1, y1, x2, y2, fill='#e8e8e4', width=0.22):
        self.dr.line([self._p(x1, y1), self._p(x2, y2)], fill=fill, width=max(1, int(width * PXMM)))

    def circle(self, x, y, r, fill=None, outline=None, width=0.2):
        self.dr.ellipse([self._p(x - r, y - r), self._p(x + r, y + r)],
                        fill=fill, outline=outline, width=max(1, int(width * PXMM)))

    def text(self, x, y, s, h=1.7, fill='#f2f2ee', anchor='lt', bold=True, angle=0):
        """angle rotates the label about (x, y), which is how a real board fits a five-letter
        power label into a 2.54 mm pitch without it running into its neighbours."""
        f = _font(h * PXMM, bold)
        if not angle:
            self.dr.text(self._p(x, y), s, font=f, fill=fill, anchor=anchor)
            return
        bb = self.dr.textbbox((0, 0), s, font=f, anchor='lt')
        tw, th = bb[2] - bb[0] + 4, bb[3] - bb[1] + 4
        tmp = Image.new('RGBA', (int(tw), int(th)), (0, 0, 0, 0))
        ImageDraw.Draw(tmp).text((2 - bb[0], 2 - bb[1]), s, font=f, fill=fill)
        tmp = tmp.rotate(angle, expand=True, resample=Image.BICUBIC)
        px, py = self._p(x, y)
        self.im.paste(tmp, (int(px - tmp.size[0] / 2), int(py - tmp.size[1] / 2)), tmp)

    def pads(self, x, y, n, pitch=2.54, r=0.9, dr=0.5, horiz=True, colour='#d8b246'):
        """A row of through-hole pads: gold annulus, dark hole. This is what reads as 'header'."""
        for i in range(n):
            cx = x + (i * pitch if horiz else 0)
            cy = y + (0 if horiz else i * pitch)
            self.circle(cx, cy, r, fill=colour)
            self.circle(cx, cy, dr, fill='#2b2b2b')

    def save(self, name):
        os.makedirs(TEX, exist_ok=True)
        p = os.path.join(TEX, name + '.png')
        self.im.save(p)
        return p


def tex_mat(name, path, rough=0.42, spec=0.4):
    """A material whose base colour comes from an image, UV-mapped 1:1 onto the board face."""
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes['Principled BSDF']
    img = nt.nodes.new('ShaderNodeTexImage')
    img.image = bpy.data.images.load(path, check_existing=True)
    img.interpolation = 'Cubic'
    nt.links.new(img.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value = rough
    if 'Specular IOR Level' in bsdf.inputs:
        bsdf.inputs['Specular IOR Level'].default_value = spec
    if 'Coat Weight' in bsdf.inputs:
        bsdf.inputs['Coat Weight'].default_value = 0.12
    return m


def face(x, y, z, w, d, material, name='pcbface', flip_v=False):
    """A quad at z with UVs mapped so the image lands exactly on the rectangle."""
    me = bpy.data.meshes.new(name)
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    bm = bmesh.new()
    v = [bm.verts.new((vx * MM, vy * MM, z * MM)) for vx, vy in
         ((x, y), (x + w, y), (x + w, y + d), (x, y + d))]
    f = bm.faces.new(v)
    uv = bm.loops.layers.uv.new()
    coords = [(0, 0), (1, 0), (1, 1), (0, 1)] if not flip_v else [(0, 1), (1, 1), (1, 0), (0, 0)]
    for loop, c in zip(f.loops, coords):
        loop[uv].uv = c
    bm.to_mesh(me)
    bm.free()
    ob.data.materials.append(material)
    return ob


def board(x, y, z, w, d, silk_png, t=1.6, edge='#0d5c6b', name='pcb', notch=None):
    """A board: coloured body for the edges, textured top face, plain underside."""
    parts = []
    body = box(x, y, z, w, d, t, mat('pcb_edge_' + name, hexcol(edge), rough=0.5), bevel=0.15,
               name=name + '_body')
    parts.append(body)
    m = tex_mat('silk_' + name, silk_png)
    parts.append(face(x, y, z + t + 0.02, w, d, m, name=name + '_top'))
    return parts


# ------------------------------------------------------------------ headers and hardware
def header_female(x, y, z, n, rows=1, pitch=2.54, name='hdr', colour='#1b1b1e'):
    """A black female strip with visible square sockets — the thing you push a jumper into."""
    m = mat('hdr_black', hexcol(colour), rough=0.62)
    hole = mat('hdr_hole', hexcol('#08080a'), rough=0.9)
    w = n * pitch
    d = rows * pitch
    out = [box(x, y, z, w, d, 8.5, m, bevel=0.18, name=name)]
    for r in range(rows):
        for i in range(n):
            out.append(box(x + i * pitch + 0.62, y + r * pitch + 0.62, z + 8.5 - 1.1,
                           1.3, 1.3, 1.2, hole, bevel=0, name=name + '_hole'))
    return out


def header_male(x, y, z, n, rows=1, pitch=2.54, name='mhdr'):
    """A male pin strip: black base, gold pins."""
    base = mat('hdr_black', hexcol('#1b1b1e'), rough=0.62)
    pin = mat('pin_gold', hexcol('#c9a227'), rough=0.28, metal=0.85)
    out = [box(x, y, z, n * pitch, rows * pitch, 2.5, base, bevel=0.12, name=name)]
    for r in range(rows):
        for i in range(n):
            out.append(box(x + i * pitch + 0.95, y + r * pitch + 0.95, z, 0.64, 0.64, 8.6,
                           pin, bevel=0, name=name + '_pin'))
    return out


def screw_terminal(x, y, z, n, pitch=5.0, name='term', colour='#1a4b8f'):
    """A blue/green screw terminal block with the slotted screws showing on top."""
    body = mat('term_body_' + colour.strip('#'), hexcol(colour), rough=0.55)
    screw = mat('term_screw', hexcol('#b9bcc2'), rough=0.32, metal=0.75)
    dark = mat('term_mouth', hexcol('#0b0d12'), rough=0.9)
    w = n * pitch
    out = [box(x, y, z, w, 8.4, 10.0, body, bevel=0.3, name=name)]
    for i in range(n):
        cx = x + pitch / 2 + i * pitch
        out.append(box(cx - 1.9, y - 0.3, z + 0.6, 3.8, 1.2, 4.2, dark, bevel=0, name=name + '_mouth'))
        s = cyl(cx, y + 5.2, z + 10.0, 1.9, 0.9, screw, name=name + '_screw')
        out.append(s)
        out.append(box(cx - 1.7, y + 4.9, z + 10.5, 3.4, 0.55, 0.35, dark, bevel=0, name=name + '_slot'))
    return out


def electrolytic(x, y, z, r=3.2, h=7.0, name='cap'):
    can = mat('cap_can', hexcol('#1d2a44'), rough=0.35, metal=0.35)
    top = mat('cap_top', hexcol('#0e1526'), rough=0.55)
    return [cyl(x, y, z, r, h, can, name=name),
            cyl(x, y, z + h - 0.15, r * 0.94, 0.2, top, name=name + '_top')]


def dip_chip(x, y, z, w, d, name='dip', pins=14):
    """A black DIP package with the notch and two rows of legs."""
    body = mat('ic_black', hexcol('#17181b'), rough=0.52)
    leg = mat('ic_leg', hexcol('#a8acb3'), rough=0.3, metal=0.8)
    out = [box(x, y, z, w, d, 3.4, body, bevel=0.25, name=name)]
    out.append(cyl(x + 1.6, y + d / 2, z + 3.4, 0.85, 0.25, mat('ic_notch', hexcol('#0a0a0c'), rough=0.7),
                   name=name + '_notch'))
    per = max(2, pins // 2)
    for i in range(per):
        px = x + 1.4 + i * (w - 2.8) / max(1, per - 1)
        for yy in (y - 0.7, y + d):
            out.append(box(px - 0.32, yy, z - 0.4, 0.64, 0.7, 1.4, leg, bevel=0, name=name + '_leg'))
    return out


def trimpot(x, y, z, name='pot'):
    """The blue 10k trimmer every cheap sensor carrier has — a strong recognition cue."""
    body = mat('pot_blue', hexcol('#1c49b8'), rough=0.42)
    top = mat('pot_white', hexcol('#dcdcd6'), rough=0.6)
    slot = mat('pot_slot', hexcol('#15161a'), rough=0.8)
    return [box(x, y, z, 6.4, 6.6, 4.4, body, bevel=0.3, name=name),
            cyl(x + 3.2, y + 3.3, z + 4.4, 2.3, 0.5, top, name=name + '_knob'),
            box(x + 1.6, y + 3.05, z + 4.85, 3.2, 0.5, 0.25, slot, bevel=0, name=name + '_slot')]


def smd_led(x, y, z, colour='#c8382c', name='led'):
    m = mat('led_' + colour.strip('#'), hexcol(colour), rough=0.3,
            emission=hexcol(colour), emission_strength=0.5)
    return [box(x, y, z, 1.6, 0.9, 0.7, m, bevel=0.1, name=name)]


def tact_button(x, y, z, name='btn'):
    base = mat('btn_base', hexcol('#1c1d21'), rough=0.55)
    cap = mat('btn_cap', hexcol('#b8391f'), rough=0.45)
    return [box(x, y, z, 6.0, 6.0, 3.0, base, bevel=0.2, name=name),
            cyl(x + 3.0, y + 3.0, z + 3.0, 1.7, 1.2, cap, name=name + '_cap')]


# ================================================================== silkscreens
UNO_TEAL = '#00767f'
UNO_W, UNO_D, UNO_T = 68.6, 53.4, 1.6


def silk_uno():
    """The Uno's top face. What a student matches against the real board: the two header runs
    with their pin numbers, the ARDUINO wordmark, and the ATmega outline. Label heights are set
    so nothing collides at 2.54 mm pitch — the power names rotate, exactly as they do on the
    real board, because RESET and IOREF are far wider than one pitch."""
    if 'uno' in _cache:
        return _cache['uno']
    s = Silk(UNO_W, UNO_D, UNO_TEAL)
    s.rect(0.25, 0.25, UNO_W - 0.5, UNO_D - 0.5, outline='#0a5f68', width=0.3)

    # --- digital header along the top edge
    top_y = 2.4
    x0, x1 = 20.6, 41.9
    s.pads(x0, top_y, 8)
    s.pads(x1, top_y, 8)
    for i, t in enumerate(['AREF', 'GND', '13', '12', '~11', '~10', '~9', '8']):
        if len(t) > 2:
            s.text(x0 + i * 2.54, top_y + 3.6, t, h=1.2, angle=-90)
        else:
            s.text(x0 + i * 2.54, top_y + 1.9, t, h=1.45, anchor='mt')
    for i, t in enumerate(['7', '~6', '~5', '4', '~3', '2', 'TX', 'RX']):
        s.text(x1 + i * 2.54, top_y + 1.9, t, h=(1.15 if len(t) > 1 else 1.45), anchor='mt')
    s.text(41.0, 5.6, 'DIGITAL  (PWM ~)', h=1.5, anchor='mt')

    # --- power and analog along the bottom edge
    bot_y = UNO_D - 2.4
    xp, xa = 19.8, 43.2
    s.pads(xp, bot_y, 7)
    s.pads(xa, bot_y, 6)
    for i, t in enumerate(['IOREF', 'RESET', '3V3', '5V', 'GND', 'GND', 'VIN']):
        s.text(xp + i * 2.54, bot_y - 4.6, t, h=1.25, angle=90)
    s.text(24.5, bot_y - 8.6, 'POWER', h=1.5, anchor='mm')
    for i, t in enumerate(['A0', 'A1', 'A2', 'A3', 'A4', 'A5']):
        s.text(xa + i * 2.54, bot_y - 2.5, t, h=1.35, anchor='mb')
    s.text(49.5, bot_y - 5.6, 'ANALOG IN', h=1.5, anchor='mm')

    # --- the ATmega footprint and the wordmark
    s.rect(25.0, 21.5, 34.0, 10.2, outline='#cfd8d8', width=0.24)
    s.text(42.0, 26.6, 'ATmega328P', h=1.5, anchor='mm')
    s.text(4.5, 24.0, 'ARDUINO', h=2.5, anchor='lm')
    s.text(4.5, 27.6, 'UNO', h=1.9, anchor='lm')

    # ICSP blocks
    s.pads(62.4, 22.4, 3, r=0.8, dr=0.42)
    s.pads(62.4, 25.0, 3, r=0.8, dr=0.42)
    s.text(65.0, 20.2, 'ICSP', h=1.2, anchor='mb')

    # the four indicator LEDs, named
    for lx, t in ((47.0, 'L'), (50.4, 'TX'), (53.8, 'RX'), (57.2, 'ON')):
        s.rect(lx, 16.4, 1.8, 1.0, fill='#dcdcd6')
        s.text(lx + 0.9, 15.9, t, h=1.15, anchor='mb')
    s.text(64.6, 46.4, 'RESET', h=1.15, anchor='mm')
    p = s.save('silk_uno')
    _cache['uno'] = p
    return p


L298_W, L298_D = 43.0, 43.0


def silk_l298n():
    if 'l298' in _cache:
        return _cache['l298']
    s = Silk(L298_W, L298_D, '#8e1c1c')
    s.rect(0.3, 0.3, L298_W - 0.6, L298_D - 0.6, outline='#e6d9d9', width=0.3)
    s.text(L298_W / 2, 20.0, 'L298N', h=3.0, anchor='mm')
    s.text(L298_W / 2, 23.6, 'MOTOR DRIVE', h=1.5, anchor='mm')
    s.rect(11.0, 12.0, 21.0, 6.0, outline='#e6d9d9', width=0.22)
    # output terminals
    s.text(6.0, 5.0, 'OUT1', h=1.6, anchor='mm')
    s.text(6.0, 11.0, 'OUT2', h=1.6, anchor='mm')
    s.text(37.0, 5.0, 'OUT3', h=1.6, anchor='mm')
    s.text(37.0, 11.0, 'OUT4', h=1.6, anchor='mm')
    # power terminal
    for i, t in enumerate(('+12V', 'GND', '+5V')):
        s.text(13.0 + i * 5.0, 39.0, t, h=1.45, anchor='mm')
    # logic header
    labels = ['ENA', 'IN1', 'IN2', 'IN3', 'IN4', 'ENB']
    x0 = 12.0
    s.pads(x0, 31.0, 6)
    for i, t in enumerate(labels):
        s.text(x0 + i * 2.54, 27.6, t, h=1.3, angle=90)
    s.rect(8.4, 34.2, 3.0, 3.0, outline='#e6d9d9', width=0.25)
    s.text(9.9, 37.4, 'ENA', h=1.1, anchor='mm')
    p = s.save('silk_l298n')
    _cache['l298'] = p
    return p


IR_W, IR_D = 32.0, 14.0


def silk_tcrt():
    if 'ir' in _cache:
        return _cache['ir']
    s = Silk(IR_W, IR_D, '#1b3f8f')
    s.rect(0.3, 0.3, IR_W - 0.6, IR_D - 0.6, outline='#dfe4ee', width=0.3)
    s.text(IR_W / 2, 2.4, 'TCRT5000  IR LINE', h=1.5, anchor='mm')
    x0 = 24.5
    s.pads(x0, 11.6, 3)
    for i, t in enumerate(['VCC', 'GND', 'D0']):
        s.text(x0 + i * 2.54, 8.0, t, h=1.2, angle=90)
    s.rect(3.0, 4.5, 9.0, 6.5, outline='#dfe4ee', width=0.25)
    s.text(19.0, 5.6, 'LM393', h=1.3, anchor='mm')
    p = s.save('silk_tcrt')
    _cache['ir'] = p
    return p


ESP_W, ESP_D = 51.5, 25.5


def silk_esp32():
    """ESP32 DevKit V1, the 30-pin board. The pin numbers down both edges are the point."""
    if 'esp' in _cache:
        return _cache['esp']
    s = Silk(ESP_W, ESP_D, '#141619')
    s.rect(0.3, 0.3, ESP_W - 0.6, ESP_D - 0.6, outline='#8a8f98', width=0.28)
    left = ['EN', 'VP', 'VN', '34', '35', '32', '33', '25', '26', '27', '14', '12', 'GND', '13', 'D2']
    right = ['VIN', 'GND', '23', '22', 'TX', 'RX', '21', 'GND', '19', '18', '5', '17', '16', '4', '0']
    x0 = 4.0
    s.pads(x0, 1.6, 15)
    s.pads(x0, ESP_D - 1.6, 15)
    for i, t in enumerate(left):
        s.text(x0 + i * 2.54, 3.2, t, h=1.35, anchor='mt', fill='#eceff3')
    for i, t in enumerate(right):
        s.text(x0 + i * 2.54, ESP_D - 3.2, t, h=1.35, anchor='mb', fill='#eceff3')
    s.text(ESP_W / 2, ESP_D / 2 + 5.6, 'ESP32  DEVKIT V1', h=1.7, anchor='mm', fill='#c9ced6')
    p = s.save('silk_esp32')
    _cache['esp'] = p
    return p


def _sy(depth, silk_y):
    """Silkscreen y (down from the top edge) -> mesh y (up from the bottom edge)."""
    return depth - silk_y


# ================================================================== whole boards
def uno(x, y, z, name='uno'):
    """An Arduino Uno R3, board origin at (x, y), USB end at low x.

    Board and silkscreen are built here; every through-hole part is the manufacturer's own CAD
    outline (cadparts.py). Each is placed at the coordinate its own silkscreen prints, so the
    part lands on its pads rather than near them. KiCad's strip packages run along Y, hence the
    90 degree turn on every header and the DIP.

    Three parts stay hand-built: the USB-B (KiCad publishes none this pipeline can read), and the
    crystal and trimmer, whose KiCad models are the tall vertical variants — 17 mm standing proud
    of a 1.6 mm board — not the low cans these boards actually carry.
    """
    D = UNO_D
    out = board(x, y, z, UNO_W, D, silk_uno(), t=UNO_T, edge='#0a5f68', name=name)
    zt = z + UNO_T
    out += usb_b(x - 1.5, y + _sy(D, 20.0), zt)
    out += CAD.barrel_jack(x + 9.6, y + _sy(D, 40.0), zt, rot=90, name='barrel')
    out += CAD.dip28(x + 42.0, y + _sy(D, 26.6), zt, rot=90, name='atmega')
    out += CAD.sot223(x + 9.3, y + _sy(D, 30.0), zt, rot=0, name='reg')
    out += CAD.electrolytic(x + 15.5, y + _sy(D, 40.0), zt, name='c1')
    out += CAD.electrolytic(x + 15.5, y + _sy(D, 14.0), zt, name='c2')
    out += CAD.button(x + 64.6, y + _sy(D, 46.4), zt, name='reset')
    # a low quartz can, lying down as it does on this board
    out.append(box(x + 21.5, y + _sy(D, 35.3) - 2.3, zt, 11.2, 4.6, 3.6,
                   mat('xtal_can', hexcol('#9aa0a8'), rough=0.28, metal=0.72), bevel=0.5, name='xtal'))
    for lx, col in ((47.0, '#e0d44a'), (50.4, '#4ad07a'), (53.8, '#4ad07a'), (57.2, '#e04a4a')):
        out += smd_led(x + lx, y + _sy(D, 16.9), zt, colour=col, name='led')
    # the four header runs, centred on the pad rows the silkscreen prints
    out += CAD.socket(8, x + 20.6 + 8.89, y + _sy(D, 2.4), zt, rot=90, name='hdr_d_hi')
    out += CAD.socket(8, x + 41.9 + 8.89, y + _sy(D, 2.4), zt, rot=90, name='hdr_d_lo')
    out += CAD.socket(8, x + 19.8 + 8.89, y + _sy(D, D - 2.4), zt, rot=90, name='hdr_pwr')
    out += CAD.socket(6, x + 43.2 + 6.35, y + _sy(D, D - 2.4), zt, rot=90, name='hdr_ana')
    out += CAD.header2x3(x + 63.7, y + _sy(D, 23.7), zt, rot=90, name='icsp')
    return out


def usb_b(x, y, z, name='usbB'):
    """A USB-B receptacle, built up rather than blocked out.

    The shape people recognise is the stepped shell with its rolled seam and the dark cavity with
    the plastic tongue inside — not a plain silver cube, which is what this was."""
    shell = mat('usb_shell', hexcol('#b9bec6'), rough=0.24, metal=0.82)
    seam = mat('usb_seam', hexcol('#9aa0a8'), rough=0.3, metal=0.8)
    cav = mat('usb_cav', hexcol('#0a0b0e'), rough=0.86)
    tongue = mat('usb_tongue', hexcol('#e8e6e0'), rough=0.55)
    out = [box(x, y, z, 16.4, 12.2, 8.2, shell, bevel=0.55, name=name),
           box(x + 1.6, y - 0.35, z + 8.2, 13.2, 12.9, 3.0, shell, bevel=0.5, name=name + '_top'),
           box(x - 0.25, y + 1.1, z + 1.0, 0.6, 10.0, 9.6, seam, bevel=0.15, name=name + '_seam')]
    out.append(box(x - 0.1, y + 1.9, z + 1.5, 1.4, 8.4, 8.2, cav, bevel=0, name=name + '_mouth'))
    out.append(box(x + 0.5, y + 3.0, z + 2.4, 1.0, 6.2, 3.0, tongue, bevel=0, name=name + '_tongue'))
    for sy in (y + 0.9, y + 10.6):
        out.append(box(x + 3.0, sy, z - 2.6, 2.0, 0.7, 2.8, seam, bevel=0, name=name + '_tab'))
    return out


def l298n_board(x, y, z, name='l298n'):
    """The red L298N carrier: finned heatsink, three screw terminals, the logic header."""
    out = board(x, y, z, L298_W, L298_D, silk_l298n(), t=1.6, edge='#6b1414', name=name)
    zt = z + 1.6
    sink = mat('heatsink_alu', hexcol('#9fa5ad'), rough=0.42, metal=0.6)
    out.append(box(x + 11.0, y + 10.5, zt, 21.0, 9.0, 3.0,
                   mat('l298_ic', hexcol('#17181b'), rough=0.5), bevel=0.2, name='l298ic'))
    out.append(box(x + 12.0, y + 12.5, zt + 3.0, 19.0, 4.0, 16.0, sink, bevel=0.4, name='sink'))
    for i in range(7):
        out.append(box(x + 12.4 + i * 2.6, y + 8.0, zt + 3.0, 1.5, 4.5, 16.0, sink, bevel=0,
                       name='fin'))
    out += screw_terminal(x + 0.5, y + 1.5, zt, 2, name='out12', colour='#12407c')
    out += screw_terminal(x + L298_W - 10.5, y + 1.5, zt, 2, name='out34', colour='#12407c')
    out += screw_terminal(x + 11.0, y + L298_D - 9.0, zt, 3, name='pwr', colour='#12407c')
    out += CAD.header(8, x + 12.0 + 6.35, y + _sy(L298_D, 31.0), zt, rot=90, name='logic')
    out.append(box(x + 8.0, y + 33.6, zt, 3.2, 5.6, 6.0,
                   mat('jumper_blk', hexcol('#1c1d21'), rough=0.6), bevel=0.2, name='jumper'))
    return out


def tcrt(x, y, z, name='ir'):
    """A TCRT5000 line-sensor carrier seen from below: the lens pair, the blue trimmer, LM393."""
    out = board(x, y, z, IR_W, IR_D, silk_tcrt(), t=1.5, edge='#12306e', name=name)
    zt = z + 1.5
    out += trimpot(x + 5.4, y + _sy(IR_D, 9.4), zt, name='pot')
    out += CAD.dip8(x + 19.0, y + _sy(IR_D, 5.6), zt, rot=90, name='lm393')
    out += smd_led(x + 21.0, y + 1.6, zt, colour='#4ad07a', name='ledp')
    out += smd_led(x + 21.0, y + 12.0, zt, colour='#e04a4a', name='ledd')
    out += CAD.header(8, x + 24.5 + 2.54, y + _sy(IR_D, 11.6), zt, rot=90, name='irpins')
    # the sensor itself hangs UNDER the board: a black block with two lenses side by side
    blk = mat('tcrt_body', hexcol('#17181c'), rough=0.6)
    emit = mat('tcrt_emit', hexcol('#2a3fb8'), rough=0.15, clearcoat=0.8)
    recv = mat('tcrt_recv', hexcol('#0d0f14'), rough=0.18, clearcoat=0.8)
    out.append(box(x + 2.6, y + 3.6, z - 6.4, 10.4, 6.8, 6.4, blk, bevel=0.35, name='tcrt5000'))
    out.append(cyl(x + 5.2, y + 7.0, z - 6.4, 2.0, -1.4, emit, name='lens_e'))
    out.append(cyl(x + 10.2, y + 7.0, z - 6.4, 2.0, -1.4, recv, name='lens_r'))
    return out


def esp32(x, y, z, name='esp32'):
    """ESP32 DevKit V1: the shielded module with its meander antenna is the recognition cue."""
    out = board(x, y, z, ESP_W, ESP_D, silk_esp32(), t=1.6, edge='#0d0e11', name=name)
    zt = z + 1.6
    can = mat('esp_can', hexcol('#c6cad1'), rough=0.3, metal=0.78)
    sub = mat('esp_sub', hexcol('#16181c'), rough=0.6)
    out.append(box(x + 12.0, y + 6.0, zt, 26.0, 14.0, 0.9, sub, bevel=0.1, name='esp_sub'))
    out.append(box(x + 12.6, y + 6.6, zt + 0.9, 18.0, 12.8, 2.2, can, bevel=0.35, name='esp_can'))
    # the PCB meander antenna, drawn as a few strokes of copper
    gold = mat('ant_gold', hexcol('#c9a227'), rough=0.3, metal=0.8)
    for i in range(6):
        out.append(box(x + 31.4 + i * 1.1, y + 8.0, zt + 0.9, 0.5, 9.5, 0.15, gold, bevel=0,
                       name='ant'))
    out.append(box(x + 2.0, y + 8.0, zt, 8.0, 8.0, 3.2,
                   mat('esp_usb', hexcol('#b7bcc4'), rough=0.3, metal=0.7), bevel=0.3, name='microusb'))
    out += CAD.button(x + 44.0, y + 5.6, zt, name='boot', cap=(0.10, 0.10, 0.12))
    out += CAD.button(x + 44.0, y + ESP_D - 5.6, zt, name='en', cap=(0.10, 0.10, 0.12))
    # A DevKit's two 15-way strips are fitted from below -- body under the board, pins pointing
    # down so it can sit in a breadboard. Standing them up on top turned the board into a bed of
    # nails and hid the module and the silkscreen the student has to read.
    out += CAD.header(15, x + 4.0 + 17.78, y + _sy(ESP_D, 1.6), z, rot=90, name='esp_l', flip=True)
    out += CAD.header(15, x + 4.0 + 17.78, y + _sy(ESP_D, ESP_D - 1.6), z, rot=90, name='esp_r', flip=True)
    return out


CAM_W, CAM_D = 40.5, 27.0


def silk_esp32cam():
    """ESP32-CAM. The pins a Project 7 student has to find are U0R, U0T, IO0, GND and 5V."""
    if 'cam' in _cache:
        return _cache['cam']
    s = Silk(CAM_W, CAM_D, '#1a1d22')
    s.rect(0.3, 0.3, CAM_W - 0.6, CAM_D - 0.6, outline='#8f949c', width=0.28)
    left = ['5V', 'GND', 'IO12', 'IO13', 'IO15', 'IO14', 'IO2', 'IO4']
    right = ['3V3', 'IO16', 'IO0', 'GND', 'VCC', 'U0R', 'U0T', 'GND']
    x0 = 3.0
    s.pads(x0, 1.5, 8)
    s.pads(x0, CAM_D - 1.5, 8)
    for i, t in enumerate(left):
        s.text(x0 + i * 2.54, 4.4, t, h=1.15, angle=-90, fill='#eceff3')
    for i, t in enumerate(right):
        s.text(x0 + i * 2.54, CAM_D - 4.4, t, h=1.15, angle=-90, fill='#eceff3')
    s.text(CAM_W / 2 + 6, CAM_D / 2, 'ESP32-CAM', h=1.7, anchor='mm', fill='#c9ced6')
    p = s.save('silk_esp32cam')
    _cache['cam'] = p
    return p


FTDI_W, FTDI_D = 36.0, 18.0


def silk_ftdi():
    """The six-pin FTDI header, named. TX and RX are the two that must cross."""
    if 'ftdi' in _cache:
        return _cache['ftdi']
    s = Silk(FTDI_W, FTDI_D, '#8b1414')
    s.rect(0.3, 0.3, FTDI_W - 0.6, FTDI_D - 0.6, outline='#e8dada', width=0.28)
    s.text(12.0, 15.0, 'FTDI  USB-SERIAL', h=1.5, anchor='mm')
    labels = ['GND', 'CTS', 'VCC', 'TX', 'RX', 'DTR']
    y0 = 2.4
    s.pads(20.0, y0, 6, horiz=False)
    for i, t in enumerate(labels):
        s.text(17.2, y0 + i * 2.54, t, h=1.2, anchor='rm')
    s.rect(25.5, 2.0, 4.5, 6.0, outline='#e8dada', width=0.25)
    s.text(27.8, 9.6, '5V/3V3', h=1.1, anchor='mt')
    p = s.save('silk_ftdi')
    _cache['ftdi'] = p
    return p
