"""cadparts.py — the real components, from KiCad's published CAD library.

Everything on these boards used to be a box or a cylinder with a bevel. That is why a header read
as a slotted block and a DIP as a slab with rectangular stubs: the shapes a person recognises a
part BY — the formed and cranked leads of a DIP, the individual sprung bays of a socket strip, the
knurl and bore of a barrel jack, the cross-slot in a trimmer — are exactly the shapes primitives
cannot make.

These are the manufacturers' own outlines, as published in KiCad's packages3D library (CC-BY-SA
with an explicit exception for use in rendered output). Each wrapper below fixes one part's real
size in millimetres and its colours, so the call site only has to say where it goes.

Not everything is available: KiCad has no USB-B, micro-USB or 5.08 mm screw terminal in a form
this pipeline can read, so those three stay hand-built in pcb.py — built up rather than blocked
out, since they are the biggest landmarks on the Uno and the L298N.
"""
import os
import wrl

CAD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cad')


def set_dir(p):
    global CAD
    CAD = p


BLACK = {'dark': (0.045, 0.045, 0.05), 'light': (0.05, 0.05, 0.055)}
GOLD = {'metal': (0.72, 0.55, 0.18)}
STEEL = {'metal': (0.62, 0.64, 0.68), 'light': (0.66, 0.68, 0.72)}


def _p(name):
    return os.path.join(CAD, name + '.wrl')


def _go(model, x, y, z, size, rot=0, name=None, recolour=None, tint=None, flip=False):
    # flip=True turns the part upside down about X, which is how a male pin strip is actually
    # fitted to a dev board: plastic body under the PCB, pins pointing down into the breadboard,
    # only the soldered tails showing on top.
    return wrl.load(_p(model), x, y, z, size_mm=size, rot=(180 if flip else 0, 0, rot),
                    name=name or model, recolour=recolour, tint=tint)


# ---- the parts, each at its real size -------------------------------------------------
def dip28(x, y, z, rot=0, name='atmega'):
    """ATmega328P in a 28-pin 0.6 inch DIP — 35.6 x 7.62 mm body."""
    return _go('dip28', x, y, z, (35.6, 7.62), rot, name, {**BLACK, 'metal': (0.70, 0.72, 0.75)})


def dip8(x, y, z, rot=0, name='lm393'):
    return _go('dip8', x, y, z, (9.8, 7.62), rot, name, {**BLACK, 'metal': (0.70, 0.72, 0.75)})


def socket(n, x, y, z, rot=0, name=None):
    """A female header strip — the thing a jumper actually plugs into."""
    m = {6: ('sock1x06', 15.2), 8: ('sock1x08', 20.3), 10: ('sock1x10', 25.4)}
    model, ln = m[n]
    return _go(model, x, y, z, (ln, 2.54), rot, name or f'sock{n}', {**BLACK, **GOLD})


def header(n, x, y, z, rot=0, name=None, flip=False):
    """A male pin strip. flip=True points the pins DOWN (a dev board's breadboard header)."""
    m = {8: ('hdr1x08', 20.3), 15: ('hdr1x15', 38.1)}
    model, ln = m[n]
    return _go(model, x, y, z, (ln, 2.54), rot, name or f'hdr{n}', {**BLACK, **GOLD}, flip=flip)


def header2x3(x, y, z, rot=0, name='icsp'):
    return _go('hdr2x03', x, y, z, (7.6, 5.08), rot, name, {**BLACK, **GOLD})


def electrolytic(x, y, z, name='cap'):
    """A 6.3 mm radial electrolytic — the little blue-black can."""
    return _go('cap63', x, y, z, (6.3, 6.3), 0, name, {'dark': (0.06, 0.09, 0.18),
                                                       'light': (0.10, 0.14, 0.28),
                                                       'metal': (0.55, 0.57, 0.60)})


def crystal(x, y, z, rot=0, name='xtal'):
    """HC-49 quartz can."""
    return _go('xtal', x, y, z, (11.5, 4.6), rot, name, STEEL)


def button(x, y, z, name='btn', cap=(0.62, 0.16, 0.10)):
    """6 mm tact switch. `cap` colours the plunger — red on an Uno reset."""
    return _go('btn', x, y, z, (6.0, 6.0), 0, name, {**BLACK, 'metal': cap, 'light': cap})


def sot223(x, y, z, rot=0, name='reg'):
    """The 5 V regulator."""
    return _go('sot223', x, y, z, (6.5, 3.5), rot, name, {**BLACK, 'metal': (0.68, 0.70, 0.73)})


def trimpot(x, y, z, rot=0, name='pot'):
    """The blue 10k trimmer — a strong recognition cue on any sensor carrier."""
    return _go('pot', x, y, z, (9.5, 4.8), rot, name, {'dark': (0.06, 0.16, 0.55),
                                                       'light': (0.10, 0.28, 0.72),
                                                       'metal': (0.72, 0.58, 0.24)})


def barrel_jack(x, y, z, rot=0, name='barrel'):
    """The 2.1 mm DC power jack on the Uno."""
    return _go('barrel', x, y, z, (14.0, 9.0), rot, name, BLACK)


AVAILABLE = ('dip28', 'dip8', 'sock1x06', 'sock1x08', 'sock1x10', 'hdr1x08', 'hdr1x15',
             'hdr2x03', 'cap63', 'xtal', 'btn', 'sot223', 'pot', 'barrel')


def present():
    return [m for m in AVAILABLE if os.path.exists(_p(m))]
