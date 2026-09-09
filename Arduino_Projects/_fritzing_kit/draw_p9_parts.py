"""draw_p9_parts.py — generates the custom Fritzing parts Project 9 (custom mouse) needs and nobody publishes:
  parts/esp32_s3_devkitc   ESP32-S3-DevKitC-1 44-pin, top view, pin order per Espressif user guide v1.1
  parts/pmw3360_module     PMW3360DM-T2QU breakout with LM19 lens, 8-pin header
  parts/kailh_enc_11       Kailh 11 mm mouse encoder (front scroll wheel), pins A/GND/B + PUSH
  parts/kailh_enc_9        Kailh 9 mm mouse encoder (rear speed roller), same pin set
  parts/gm80_switch        Kailh GM 8.0 mouse microswitch, 2 wired legs
  parts/tactile_6x6        6x6x5 mm through-hole tactile switch, 2 effective legs
  parts/led_330            5 mm LED with its 330 ohm resistor drawn in series as one unit (S / GND)
  parts/tp4056_usb_c       TP4056 USB-C charger module with protection (B+/B-/OUT+/OUT-)
  parts/holder_18650       18650 spring holder with protected NCR18650B inside, red/black leads
  parts/ss12f15_switch     SS12F15 slide switch (1/COM/2)
Run from this folder: python draw_p9_parts.py && python normalize_parts.py
All drawings: solid fills + style= attributes only (Qt SVG in the Fritzing CLI drops gradients/opacity)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

def write_part(dirname, moduleid, title, svg, connectors, desc):
    d = os.path.join(HERE, 'parts', dirname); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f'svg.breadboard.{dirname}_breadboard.svg'), 'w', encoding='utf-8').write(svg)
    for v, layer in (('icon', 'icon'), ('schematic', 'schematic'), ('pcb', 'copper0')):
        open(os.path.join(d, f'svg.{v}.{dirname}_{v}.svg'), 'w', encoding='utf-8').write(svg.replace('id="breadboard"', f'id="{layer}"'))
    conns = ''.join(f'''
        <connector id="connector{i}" type="male" name="{n}">
            <description>{n}</description>
            <views>
                <breadboardView><p layer="breadboard" svgId="connector{i}pin"/></breadboardView>
                <schematicView><p layer="schematic" svgId="connector{i}pin"/></schematicView>
                <pcbView><p layer="copper0" svgId="connector{i}pin"/></pcbView>
            </views>
        </connector>''' for i, n in enumerate(connectors))
    fzp = f'''<?xml version="1.0" encoding="UTF-8"?>
<module fritzingVersion="0.9.4" moduleId="{moduleid}">
    <author>Yon (drawn for the Arduino PBL program, 2026)</author>
    <title>{title}</title>
    <label>P</label>
    <date>2026-09-07</date>
    <tags><tag>mouse</tag></tags>
    <properties><property name="family">{title}</property></properties>
    <description>{desc}</description>
    <views>
        <iconView><layers image="icon/{dirname}_icon.svg"><layer layerId="icon"/></layers></iconView>
        <schematicView><layers image="schematic/{dirname}_schematic.svg"><layer layerId="schematic"/></layers></schematicView>
        <pcbView><layers image="pcb/{dirname}_pcb.svg"><layer layerId="copper0"/></layers></pcbView>
        <breadboardView><layers image="breadboard/{dirname}_breadboard.svg"><layer layerId="breadboard"/></layers></breadboardView>
    </views>
    <connectors>{conns}
    </connectors>
</module>
'''
    open(os.path.join(d, f'part.{dirname}.fzp'), 'w', encoding='utf-8').write(fzp)
    print('part', dirname, len(connectors), 'connectors')

def pin(i, x, y, w=1.2, h=1.2):
    return f'<rect id="connector{i}pin" x="{x-w/2:.2f}" y="{y-h/2:.2f}" width="{w}" height="{h}" style="fill:none;stroke:none"/>'

def text(x, y, s, size=2.2, fill='#111', weight='bold', anchor='middle'):
    return f'<text x="{x:.2f}" y="{y:.2f}" style="font-family:Arial;font-size:{size}px;font-weight:{weight};fill:{fill};text-anchor:{anchor}">{s}</text>'

def gold(x, y, r=0.85):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" style="fill:#e9c46a;stroke:#8a6f3c;stroke-width:0.25"/>'
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r*0.38:.2f}" style="fill:#3a3a3a;stroke:none"/>')

def svg_open(W, H):
    return ['<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="{W/25.4:.4f}in" height="{H/25.4:.4f}in" viewBox="0 0 {W} {H}">',
            '<g id="breadboard">']

# ------------------------------------------------------------ ESP32-S3-DevKitC-1, top view, 1 unit = 1 mm
# Pin order (Espressif user guide v1.1): J1 (left, top->bottom), J3 (right, top->bottom).
J1 = ['3V3', '3V3', 'RST', '4', '5', '6', '7', '15', '16', '17', '18', '8', '3', '46', '9', '10', '11', '12', '13', '14', '5V', 'G']
J3 = ['G', 'TX', 'RX', '1', '2', '42', '41', '40', '39', '38', '37', '36', '35', '0', '45', '48', '47', '21', '20', '19', 'G', 'G']

def devkit_svg():
    W, H = 26.0, 63.5
    s = svg_open(W, H)
    s.append(f'<rect x="0.3" y="0.3" width="25.4" height="62.9" rx="1.4" style="fill:#14161a;stroke:#000;stroke-width:0.35"/>')
    # module can with antenna region (top end)
    s.append(f'<rect x="6.2" y="1.1" width="13.6" height="3.4" style="fill:#2b2d33;stroke:#000;stroke-width:0.2"/>')
    for k in range(5):
        s.append(f'<rect x="{7.0+k*2.5:.2f}" y="1.7" width="1.4" height="2.2" style="fill:#4a4d55;stroke:none"/>')
    s.append(f'<rect x="6.2" y="4.5" width="13.6" height="12.5" rx="0.6" style="fill:#b9bcc2;stroke:#6f737a;stroke-width:0.35"/>')
    s.append(text(13.0, 9.6, 'ESP32-S3', 2.3, '#3b3e43'))
    s.append(text(13.0, 12.6, 'WROOM-1', 1.9, '#3b3e43'))
    s.append(text(13.0, 20.0, 'DevKitC-1', 1.9, '#c9ccd1'))
    # RGB LED (drawn on the empty centre so it hides no pin silk)
    s.append(f'<rect x="11.7" y="26.4" width="2.6" height="2.6" rx="0.4" style="fill:#dfe2e6;stroke:#8a8d92;stroke-width:0.2"/>')
    s.append(text(13.0, 31.6, 'RGB', 1.4, '#c9ccd1'))
    # RST / BOOT buttons + two USB-C at the bottom end
    for bx, lab in ((7.0, 'RST'), (15.6, 'BOOT')):
        s.append(f'<rect x="{bx}" y="53.6" width="4.2" height="3.2" rx="0.5" style="fill:#c8ccd1;stroke:#7d8288;stroke-width:0.3"/>')
        s.append(f'<circle cx="{bx+2.1:.2f}" cy="55.2" r="0.9" style="fill:#e9ecef;stroke:#7d8288;stroke-width:0.25"/>')
        s.append(text(bx+2.1, 52.8, lab, 1.5, '#c9ccd1'))
    for ux, lab in ((5.4, 'USB'), (14.6, 'COM')):
        s.append(f'<rect x="{ux}" y="59.6" width="6.4" height="3.6" rx="1.2" style="fill:#b9bcc2;stroke:#6f737a;stroke-width:0.3"/>')
        s.append(f'<rect x="{ux+0.8:.2f}" y="60.6" width="4.8" height="1.6" rx="0.8" style="fill:#3a3d42;stroke:none"/>')
        s.append(text(ux+3.2, 59.0, lab, 1.4, '#c9ccd1'))
    conns, ci = [], 0
    y0, pitch = 7.6, 2.54
    xl, xr = 1.57, 24.43
    for k, name in enumerate(J1):
        y = y0 + k*pitch
        s.append(gold(xl, y)); s.append(pin(ci, xl, y)); conns.append(name); ci += 1
        s.append(text(3.2, y+0.6, name, 1.6, '#d8d8d8', 'bold', 'start'))
    for k, name in enumerate(J3):
        y = y0 + k*pitch
        s.append(gold(xr, y)); s.append(pin(ci, xr, y)); conns.append(name); ci += 1
        s.append(text(22.8, y+0.6, name, 1.6, '#d8d8d8', 'bold', 'end'))
    s.append('</g></svg>')
    return '\n'.join(s), conns

# ------------------------------------------------------------ PMW3360 breakout, top view, header on top edge
def pmw_svg():
    W, H = 22.0, 30.0
    s = svg_open(W, H)
    s.append(f'<rect x="0.3" y="0.3" width="21.4" height="29.4" rx="1.2" style="fill:#1d2430;stroke:#000;stroke-width:0.3"/>')
    names = ['MOT', 'RST', 'GND', 'VCC', 'MI', 'MO', 'SC', 'CS']
    conns = []
    x0, pitch, yh = 2.11, 2.54, 2.1
    for k, name in enumerate(names):
        x = x0 + k*pitch
        s.append(gold(x, yh, 0.8)); s.append(pin(k, x, yh)); conns.append(name)
        s.append(text(x, 4.9 if k % 2 == 0 else 6.6, name, 1.25, '#c9ccd1'))
    # sensor package + lens window (the eye)
    s.append(f'<rect x="6.5" y="11.0" width="9.0" height="11.5" rx="0.6" style="fill:#14161a;stroke:#000;stroke-width:0.25"/>')
    s.append(f'<circle cx="11.0" cy="16.7" r="3.3" style="fill:#2b2d33;stroke:#4a4d55;stroke-width:0.3"/>')
    s.append(f'<circle cx="11.0" cy="16.7" r="1.6" style="fill:#3f4450;stroke:none"/>')
    s.append(text(11.0, 26.8, 'PMW3360', 2.0, '#c9ccd1'))
    s.append('</g></svg>')
    return '\n'.join(s), conns

# ------------------------------------------------------------ Kailh mouse encoders, top view: 3 pins left (A/GND/B), PUSH right
def enc_svg(body_w, body_h, wheel_label):
    lead = 3.2
    W, H = body_w + 2*lead + 2.0, body_h + 2.0
    ox, oy = lead + 1.0, 1.0
    s = svg_open(W, H)
    s.append(f'<rect x="{ox}" y="{oy}" width="{body_w}" height="{body_h}" rx="1.0" style="fill:#b9bcc2;stroke:#6f737a;stroke-width:0.35"/>')
    # the roller across the middle
    wy = oy + body_h/2 - 2.0
    s.append(f'<rect x="{ox+1.6:.2f}" y="{wy:.2f}" width="{body_w-3.2:.2f}" height="4.0" rx="1.9" style="fill:#3a3d42;stroke:#1d1f22;stroke-width:0.3"/>')
    for k in range(int(body_w-5)):
        s.append(f'<line x1="{ox+2.6+k:.2f}" y1="{wy+0.3:.2f}" x2="{ox+2.6+k:.2f}" y2="{wy+3.7:.2f}" style="stroke:#55585c;stroke-width:0.25"/>')
    s.append(text(ox+body_w/2, oy+body_h-0.9, wheel_label, 1.6, '#3b3e43'))
    conns = []
    ys = [oy + body_h/2 - 2.54, oy + body_h/2, oy + body_h/2 + 2.54]
    for k, name in enumerate(['A', 'GND', 'B']):
        y = ys[k]
        s.append(f'<line x1="{ox:.2f}" y1="{y:.2f}" x2="{ox-lead+0.6:.2f}" y2="{y:.2f}" style="stroke:#b5b5b5;stroke-width:0.7;stroke-linecap:round"/>')
        s.append(gold(ox-lead+0.4, y, 0.75)); s.append(pin(k, ox-lead+0.4, y)); conns.append(name)
    py = oy + body_h/2
    s.append(f'<line x1="{ox+body_w:.2f}" y1="{py:.2f}" x2="{ox+body_w+lead-0.6:.2f}" y2="{py:.2f}" style="stroke:#b5b5b5;stroke-width:0.7;stroke-linecap:round"/>')
    s.append(gold(ox+body_w+lead-0.4, py, 0.75)); s.append(pin(3, ox+body_w+lead-0.4, py)); conns.append('PUSH')
    s.append('</g></svg>')
    return '\n'.join(s), conns

# ------------------------------------------------------------ Kailh GM 8.0 mouse microswitch, 2 wired legs
def gm_svg():
    W, H = 14.0, 10.0
    s = svg_open(W, H)
    s.append(f'<rect x="0.5" y="2.2" width="13.0" height="6.2" rx="0.8" style="fill:#2b3a8c;stroke:#15204f;stroke-width:0.3"/>')
    s.append(f'<rect x="2.6" y="0.8" width="3.4" height="1.6" rx="0.4" style="fill:#cc2222;stroke:#7a1414;stroke-width:0.25"/>')
    s.append(text(7.0, 6.3, 'GM 8.0', 1.7, '#dfe2e6'))
    conns = []
    for k, x in enumerate((3.0, 11.0)):
        s.append(f'<line x1="{x}" y1="8.4" x2="{x}" y2="9.4" style="stroke:#b5b5b5;stroke-width:0.7;stroke-linecap:round"/>')
        s.append(gold(x, 9.3, 0.75)); s.append(pin(k, x, 9.3)); conns.append(str(k+1))
    s.append('</g></svg>')
    return '\n'.join(s), conns

# ------------------------------------------------------------ 6x6x5 tactile switch, legs left+right (each pair joined inside)
def tact_svg():
    W, H = 10.0, 8.0
    ox = 1.8
    s = svg_open(W, H)
    s.append(f'<rect x="{ox}" y="1.0" width="6.4" height="6.4" rx="0.7" style="fill:#b9bcc2;stroke:#6f737a;stroke-width:0.3"/>')
    s.append(f'<circle cx="{ox+3.2:.2f}" cy="4.2" r="1.8" style="fill:#3a3d42;stroke:#1d1f22;stroke-width:0.25"/>')
    for y in (2.0, 6.4):
        s.append(f'<line x1="{ox}" y1="{y}" x2="{ox-1.0:.2f}" y2="{y}" style="stroke:#b5b5b5;stroke-width:0.6"/>')
        s.append(f'<line x1="{ox+6.4:.2f}" y1="{y}" x2="{ox+7.4:.2f}" y2="{y}" style="stroke:#b5b5b5;stroke-width:0.6"/>')
    conns = []
    s.append(gold(ox-1.0, 4.2, 0.7)); s.append(pin(0, ox-1.0, 4.2)); conns.append('1')
    s.append(f'<line x1="{ox-1.0:.2f}" y1="2.0" x2="{ox-1.0:.2f}" y2="6.4" style="stroke:#b5b5b5;stroke-width:0.5"/>')
    s.append(gold(ox+7.4, 4.2, 0.7)); s.append(pin(1, ox+7.4, 4.2)); conns.append('2')
    s.append(f'<line x1="{ox+7.4:.2f}" y1="2.0" x2="{ox+7.4:.2f}" y2="6.4" style="stroke:#b5b5b5;stroke-width:0.5"/>')
    s.append('</g></svg>')
    return '\n'.join(s), conns

# ------------------------------------------------------------ 5 mm LED + 330 ohm resistor as one series unit: S -> resistor -> LED -> GND
def led330_svg():
    W, H = 20.0, 7.0
    s = svg_open(W, H)
    yc = 4.0
    s.append(gold(1.0, yc, 0.75)); s.append(f'<line x1="1.4" y1="{yc}" x2="3.4" y2="{yc}" style="stroke:#b5b5b5;stroke-width:0.6"/>')
    s.append(f'<rect x="3.4" y="{yc-1.1:.2f}" width="4.6" height="2.2" rx="0.9" style="fill:#e8d2a8;stroke:#8a6f3c;stroke-width:0.25"/>')
    for j, col in enumerate(('#f28a00', '#f28a00', '#7b3f00')):
        s.append(f'<rect x="{4.2+j*1.1:.2f}" y="{yc-1.1:.2f}" width="0.55" height="2.2" style="fill:{col};stroke:none"/>')
    s.append(text(5.7, 1.9, '330', 1.5, '#5a4a2a'))
    s.append(f'<line x1="8.0" y1="{yc}" x2="10.6" y2="{yc}" style="stroke:#b5b5b5;stroke-width:0.6"/>')
    s.append(f'<circle cx="13.2" cy="{yc}" r="2.6" style="fill:#cc2222;stroke:#7a1414;stroke-width:0.35"/>')
    s.append(f'<circle cx="12.4" cy="{yc-0.8:.2f}" r="0.7" style="fill:#e86a6a;stroke:none"/>')
    s.append(f'<line x1="15.8" y1="{yc}" x2="18.2" y2="{yc}" style="stroke:#b5b5b5;stroke-width:0.6"/>')
    s.append(gold(19.0, yc, 0.75))
    s.append(pin(0, 1.0, yc)); s.append(pin(1, 19.0, yc))
    s.append('</g></svg>')
    return '\n'.join(s), ['S', 'GND']

# ------------------------------------------------------------ TP4056 USB-C charger module with protection
def tp_svg():
    W, H = 18.0, 29.0
    s = svg_open(W, H)
    s.append(f'<rect x="0.3" y="0.3" width="17.4" height="27.4" rx="1.0" style="fill:#2458a6;stroke:#12305e;stroke-width:0.35"/>')
    s.append(f'<rect x="5.5" y="0.0" width="7.0" height="3.8" rx="1.2" style="fill:#b9bcc2;stroke:#6f737a;stroke-width:0.3"/>')
    s.append(f'<rect x="6.4" y="1.0" width="5.2" height="1.7" rx="0.85" style="fill:#3a3d42;stroke:none"/>')
    s.append(f'<circle cx="4.4" cy="6.6" r="0.9" style="fill:#cc2222;stroke:#7a1414;stroke-width:0.2"/>')
    s.append(f'<circle cx="13.6" cy="6.6" r="0.9" style="fill:#2158c7;stroke:#12305e;stroke-width:0.2"/>')
    s.append(text(4.4, 9.6, 'CHRG', 1.2, '#c9ccd1'))
    s.append(text(13.6, 9.6, 'FULL', 1.2, '#c9ccd1'))
    s.append(f'<rect x="5.4" y="11.5" width="7.2" height="4.6" rx="0.4" style="fill:#1d1d1d;stroke:#000;stroke-width:0.2"/>')
    s.append(text(9.0, 14.6, 'TP4056', 1.5, '#cfcfcf'))
    s.append(f'<rect x="3.0" y="17.6" width="5.2" height="3.0" rx="0.3" style="fill:#1d1d1d;stroke:#000;stroke-width:0.2"/>')
    s.append(f'<rect x="9.8" y="17.6" width="5.2" height="3.0" rx="0.3" style="fill:#1d1d1d;stroke:#000;stroke-width:0.2"/>')
    s.append(text(9.0, 23.3, 'protected', 1.3, '#c9ccd1', 'normal'))
    conns = []
    pads = [('OUT+', 2.2, '#e86a6a'), ('B+', 6.7, '#e86a6a'), ('B-', 11.2, '#c9ccd1'), ('OUT-', 15.7, '#c9ccd1')]
    for k, (name, x, col) in enumerate(pads):
        s.append(gold(x, 26.6, 0.85)); s.append(pin(k, x, 26.6)); conns.append(name)
        s.append(text(x, 25.0, name, 1.25, col))
    s.append('</g></svg>')
    return '\n'.join(s), conns

# ------------------------------------------------------------ 18650 spring holder with protected NCR18650B, leads exit left
def holder_svg():
    lead = 5.0
    W, H = 78.0 + lead, 22.0
    ox = lead
    s = svg_open(W, H)
    s.append(f'<rect x="{ox}" y="0.5" width="77.5" height="21" rx="1.6" style="fill:#14161a;stroke:#000;stroke-width:0.4"/>')
    # spring (left inside) + positive contact (right inside)
    for k in range(4):
        s.append(f'<line x1="{ox+2.5+k*1.1:.2f}" y1="5.5" x2="{ox+2.5+k*1.1+0.55:.2f}" y2="16.5" style="stroke:#8d9096;stroke-width:0.5"/>')
        s.append(f'<line x1="{ox+2.5+k*1.1+0.55:.2f}" y1="16.5" x2="{ox+2.5+k*1.1+1.1:.2f}" y2="5.5" style="stroke:#8d9096;stroke-width:0.5"/>')
    s.append(f'<rect x="{ox+72.6:.2f}" y="6.5" width="1.6" height="9" style="fill:#9a9ca0;stroke:#55585c;stroke-width:0.2"/>')
    # the green protected cell
    s.append(f'<rect x="{ox+8.0:.2f}" y="3.8" width="63" height="14.4" rx="6.8" style="fill:#1f7a4d;stroke:#0f4d2e;stroke-width:0.4"/>')
    s.append(f'<rect x="{ox+64.0:.2f}" y="7.2" width="4.4" height="7.6" style="fill:#dfe2e6;stroke:#8a8d92;stroke-width:0.25"/>')
    s.append(text(ox+36, 12.4, 'NCR18650B protected', 2.4, '#e8f5ee'))
    s.append(text(ox+70.6, 12.9, '+', 3.2, '#e8f5ee'))
    s.append(text(ox+5.4, 12.9, '-', 3.2, '#e8f5ee'))
    conns = []
    for k, (y, col, name) in enumerate(((7.0, '#cc1414', '+'), (15.0, '#111111', '-'))):
        s.append(f'<path d="M {ox+0.2:.2f} {y} C {ox-2.5:.2f} {y}, {ox-3.2:.2f} {y}, 1.6 {y}" style="fill:none;stroke:{col};stroke-width:0.9;stroke-linecap:round"/>')
        s.append(gold(1.0, y, 0.75)); s.append(pin(k, 1.0, y)); conns.append(name)
    s.append('</g></svg>')
    return '\n'.join(s), conns

# ------------------------------------------------------------ SS12F15 slide switch, 3 pins bottom
def slide_svg():
    W, H = 10.0, 8.0
    s = svg_open(W, H)
    s.append(f'<rect x="0.6" y="2.6" width="8.8" height="3.6" rx="0.5" style="fill:#b9bcc2;stroke:#6f737a;stroke-width:0.3"/>')
    s.append(f'<rect x="1.6" y="0.7" width="2.6" height="2.0" rx="0.3" style="fill:#3a3d42;stroke:#1d1f22;stroke-width:0.25"/>')
    s.append(text(5.0, 5.2, 'ON/OFF', 1.3, '#3b3e43'))
    conns = []
    for k, (x, name) in enumerate(((2.5, '1'), (5.0, 'COM'), (7.5, '2'))):
        s.append(f'<line x1="{x}" y1="6.2" x2="{x}" y2="7.0" style="stroke:#b5b5b5;stroke-width:0.6"/>')
        s.append(gold(x, 7.0, 0.7)); s.append(pin(k, x, 7.0)); conns.append(name)
    s.append('</g></svg>')
    return '\n'.join(s), conns

if __name__ == '__main__':
    svg, conns = devkit_svg()
    write_part('esp32_s3_devkitc', 'esp32_s3_devkitc_yon_2026', 'ESP32-S3 DevKitC-1 (44-pin)', svg, conns,
               'ESP32-S3-DevKitC-1 dev board, 44-pin, top view; pin order per the Espressif user guide v1.1 (J1 left, J3 right). Two USB-C ports, RST/BOOT buttons, onboard RGB LED.')
    svg, conns = pmw_svg()
    write_part('pmw3360_module', 'pmw3360_module_yon_2026', 'PMW3360 optical sensor module', svg, conns,
               'PixArt PMW3360DM-T2QU breakout with LM19 lens (lens faces down). 8-pin header: MOT RST GND VCC MI MO SC CS. 3.3V SPI.')
    svg, conns = enc_svg(15.0, 13.0, '11 mm')
    write_part('kailh_enc_11', 'kailh_enc_11_yon_2026', 'Kailh 11 mm mouse encoder (scroll wheel)', svg, conns,
               'Kailh 11 mm mouse scroll encoder with push. Pins: A / GND (common) / B on one side, PUSH on the other (its second switch leg is tied to GND in this drawing).')
    svg, conns = enc_svg(12.0, 11.0, '9 mm')
    write_part('kailh_enc_9', 'kailh_enc_9_yon_2026', 'Kailh 9 mm mouse encoder (speed roller)', svg, conns,
               'Kailh 9 mm mouse encoder with push — the rear speed roller. Pins: A / GND (common) / B, PUSH on the other side (second switch leg tied to GND in this drawing).')
    svg, conns = gm_svg()
    write_part('gm80_switch', 'gm80_switch_yon_2026', 'Kailh GM 8.0 mouse switch', svg, conns,
               'Kailh GM 8.0 mouse microswitch (clicky). Two wired legs: COM and NO, drawn as 1 and 2.')
    svg, conns = tact_svg()
    write_part('tactile_6x6', 'tactile_6x6_yon_2026', '6x6 tactile switch', svg, conns,
               '6x6x5 mm through-hole tactile switch; the two legs on each side are joined internally, drawn as one effective leg per side.')
    svg, conns = led330_svg()
    write_part('led_330', 'led_330_yon_2026', '5 mm LED with 330 ohm resistor', svg, conns,
               'A 5 mm red LED and its 330 ohm series resistor drawn as one unit: S (signal, via the resistor into the anode) and GND (cathode).')
    svg, conns = tp_svg()
    write_part('tp4056_usb_c', 'tp4056_usb_c_yon_2026', 'TP4056 USB-C charger (protected)', svg, conns,
               'TP4056 lithium charger module, USB-C, with DW01A+8205A protection. Pads: OUT+ B+ B- OUT-. Load connects to OUT so charging and use share the cell safely.')
    svg, conns = holder_svg()
    write_part('holder_18650', 'holder_18650_yon_2026', '18650 holder with protected cell', svg, conns,
               '18650 spring holder sized for a protected NCR18650B (~68 mm). Red (+) and black (-) leads exit on the left.')
    svg, conns = slide_svg()
    write_part('ss12f15_switch', 'ss12f15_switch_yon_2026', 'SS12F15 slide switch', svg, conns,
               'SS12F15 slide switch: COM in the middle, positions 1 and 2. Used as the mouse main power switch.')
