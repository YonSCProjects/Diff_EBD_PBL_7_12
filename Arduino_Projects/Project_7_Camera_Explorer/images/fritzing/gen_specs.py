"""gen_specs.py — emits the four Project 7 figure specs; build each with
../../../_fritzing_kit/build_figure.js <spec.json>.

Sketch px (90 px = 1 in). Rotations pivot on the part origin: a part rotated 180°
occupies (x-w, y-h)..(x, y); 90° CW occupies (x-h, y)..(x, y+w).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RED, BLACK, ORANGE, GREEN, BLUE, YELLOW = '#cc1414', '#000000', '#f28a00', '#25cc35', '#418dd9', '#e0b400'

def spec(name, **kw):
    d = {'name': name, 'out_dir': '..', 'assets_dir': '../../task_cards_he/assets', 'instances': [], 'shapes': [], 'wires': [], 'labels': []}
    d.update(kw); return d

specs = []

# 1 — FTDI programmer on the ESP32-CAM (upload wiring + IO0-GND flash jumper)
specs.append(spec('w_p7_01_ftdi_upload', preview_scale=2,
    instances=[
        {'id': 'cam', 'part': 'ESP32-CAM_FRONT-fixed', 'x': 100, 'y': 0, 'title': 'ESP32-CAM'},
        {'id': 'ftdi', 'part': 'FTDI Basic Programmer', 'x': 378, 'y': 74.5, 'rotation': 180, 'title': 'FTDI programmer'},
    ],
    wires=[
        {'from': 'ftdi.TXO', 'to': 'cam.VOR', 'color': GREEN, 'route': 'vh', 'out': ['left', 200]},
        {'from': 'ftdi.RXI', 'to': 'cam.VOT', 'color': BLUE, 'route': 'vh', 'out': ['left', 300]},
        {'from': 'ftdi.GND', 'to': 'cam.GND.2', 'color': BLACK, 'route': 'vh', 'out': ['left', 400], 'width': 32},
        {'from': 'ftdi.POWER', 'to': 'cam.5V', 'color': RED, 'route': 'vh', 'out': ['left', 50], 'width': 32,
         'via': [{'ref': 'ftdi.POWER', 'dx': -50, 'dy': 1250}, {'ref': 'cam.5V', 'dx': -245, 'dy': 1580}]},
        {'from': 'cam.IO0', 'to': 'cam.GND.3', 'color': YELLOW, 'route': 'vh', 'out': ['right', 150]},
    ],
    labels=[
        {'ref': 'cam.5V', 'dx': 230, 'text': '5V', 'size': 50},
        {'ref': 'cam.GND.2', 'dx': -230, 'text': 'GND', 'size': 46},
        {'ref': 'cam.VOR', 'dx': -230, 'text': 'U0R', 'size': 46},
        {'ref': 'cam.VOT', 'dx': -450, 'text': 'U0T', 'size': 46},
        {'ref': 'cam.IO0', 'dx': 520, 'dy': -140, 'text': 'IO0 → GND\n(flash mode)', 'size': 42, 'leader': True, 'fill': '#fff8d6', 'stroke': '#b08900'},
        {'ref': 'ftdi.TXO', 'dx': 230, 'text': 'TX', 'size': 44},
        {'ref': 'ftdi.RXI', 'dx': 230, 'text': 'RX', 'size': 44},
        {'ref': 'ftdi.POWER', 'dx': 250, 'text': '5V', 'size': 44},
        {'ref': 'ftdi.GND', 'dx': 250, 'text': 'GND', 'size': 44},
        {'ref': 'ftdi.@t', 'dy': -110, 'text': 'FTDI programmer', 'size': 50},
        {'ref': 'cam.@t', 'dy': -110, 'text': 'ESP32-CAM', 'size': 50},
    ]))

# 2 — power: one battery, two rails (L298N for motors, buck → camera), capacitor, common GND
specs.append(spec('w_p7_02_power_rails',
    instances=[
        {'id': 'drv', 'part': 'L298N-DC-motor-driver-improved', 'x': 110, 'y': -70, 'title': 'L298N'},
        {'id': 'bat', 'part': '8xAA_box', 'x': -420, 'y': 230, 'title': '8 x AA battery box'},
        {'id': 'buck', 'part': 'Mini560 buck module', 'x': 300, 'y': 330, 'rotation': 180, 'title': 'Buck 5V'},
        {'id': 'cam', 'part': 'ESP32-CAM_FRONT-fixed', 'x': 420, 'y': 200, 'title': 'ESP32-CAM'},
        {'id': 'cap', 'core': 'capacitor_electrolytic_small', 'x': 385, 'y': 150, 'title': '470 uF', 'properties': {'capacitance': '470µF'}},
    ],
    wires=[
        {'from': 'bat.+', 'to': 'drv.12V', 'color': RED, 'width': 36},
        {'from': 'bat.-', 'to': 'drv.GND', 'color': BLACK, 'width': 36},
        {'from': 'bat.+', 'to': 'buck.Vin1', 'color': RED, 'width': 36},
        {'from': 'bat.-', 'to': 'buck.GND1', 'color': BLACK, 'width': 36},
        {'from': 'buck.Vout1', 'to': 'cam.5V', 'color': RED, 'width': 32},
        {'from': 'buck.GND1*', 'to': 'cam.GND', 'color': BLACK, 'width': 32},
        {'from': 'cap.+', 'to': 'cam.5V', 'color': RED},
        {'from': 'cap.-', 'to': 'cam.GND', 'color': BLACK},
    ],
    labels=[
        {'ref': 'drv.12V', 'dx': -190, 'dy': 170, 'text': '12V', 'size': 60},
        {'ref': 'drv.GND', 'dx': 190, 'dy': 170, 'text': 'GND', 'size': 60},
        {'ref': 'buck.Vin1', 'dx': -260, 'dy': -140, 'text': 'IN +', 'size': 50, 'color': RED, 'stroke': RED},
        {'ref': 'buck.GND1', 'dx': -260, 'dy': 140, 'text': 'IN −', 'size': 50},
        {'ref': 'buck.Vout1', 'dx': 280, 'dy': -140, 'text': 'OUT 5V', 'size': 50, 'color': RED, 'stroke': RED},
        {'ref': 'buck.GND1*', 'dx': 280, 'dy': 140, 'text': 'OUT −', 'size': 50},
        {'ref': 'buck.@b', 'dy': 120, 'text': 'buck converter  12V → 5V', 'size': 50},
        {'ref': 'cam.5V', 'dx': 230, 'text': '5V', 'size': 50},
        {'ref': 'cam.GND', 'dx': 250, 'text': 'GND', 'size': 46},
        {'ref': 'cap.@t', 'dy': -100, 'text': '470 µF\nstripe → GND', 'size': 42},
        {'ref': 'bat.+', 'dx': -90, 'dy': -120, 'text': '+', 'size': 80, 'color': RED, 'stroke': RED},
        {'ref': 'bat.-', 'dx': -90, 'dy': 120, 'text': '−', 'size': 80},
        {'ref': 'drv.@t', 'dy': -110, 'text': 'L298N — motors only', 'size': 54},
        {'ref': 'cam.@b', 'dy': 120, 'text': 'camera — its own 5V rail', 'size': 50},
    ]))

# 3 — the four free CAM pins → L298N IN1..IN4, ENA/ENB jumper caps stay on
specs.append(spec('w_p7_03_cam_to_l298n',
    instances=[
        {'id': 'drv', 'part': 'L298N-DC-motor-driver-improved', 'x': 60, 'y': 0, 'title': 'L298N'},
        {'id': 'cam', 'part': 'ESP32-CAM_FRONT-fixed', 'x': 330, 'y': 190, 'title': 'ESP32-CAM'},
    ],
    shapes=[
        {'a': 'drv.ENA', 'b': 'drv.+5V-J1', 'pad': 42, 'fill': '#1a1a1a', 'stroke': '#000', 'rx': 10},
        {'a': 'drv.ENB', 'b': 'drv.+5V-J2', 'pad': 42, 'fill': '#1a1a1a', 'stroke': '#000', 'rx': 10},
    ],
    wires=[
        {'from': 'drv.IN1', 'to': 'cam.IO14', 'color': ORANGE, 'route': 'vh'},
        {'from': 'drv.IN2', 'to': 'cam.IO15', 'color': ORANGE, 'route': 'vh'},
        {'from': 'drv.IN3', 'to': 'cam.IO13', 'color': GREEN, 'route': 'vh'},
        {'from': 'drv.IN4', 'to': 'cam.IO12', 'color': GREEN, 'route': 'vh'},
    ],
    labels=[
        {'ref': 'cam.IO14', 'dx': 210, 'text': '14', 'size': 56},
        {'ref': 'cam.IO15', 'dx': 210, 'text': '15', 'size': 56},
        {'ref': 'cam.IO13', 'dx': 210, 'text': '13', 'size': 56},
        {'ref': 'cam.IO12', 'dx': 210, 'text': '12', 'size': 56},
        {'ref': 'drv.IN1', 'dy': -200, 'text': 'IN1', 'size': 50},
        {'ref': 'drv.IN2', 'dy': -340, 'text': 'IN2', 'size': 50},
        {'ref': 'drv.IN3', 'dy': -200, 'text': 'IN3', 'size': 50},
        {'ref': 'drv.IN4', 'dy': -340, 'text': 'IN4', 'size': 50},
        {'ref': 'drv.+5V-J2', 'dx': 520, 'dy': -260, 'text': 'ENA / ENB caps\nstay ON', 'size': 44, 'leader': True, 'fill': '#fff8d6', 'stroke': '#b08900'},
    ]))

# 4 — full explorer map
specs.append(spec('w_p7_04_full_explorer',
    instances=[
        {'id': 'drv', 'part': 'L298N-DC-motor-driver-improved', 'x': 400, 'y': 0, 'title': 'L298N'},
        {'id': 'mA', 'part': 'Getriebemotor', 'x': 370, 'y': 72, 'rotation': 180, 'title': 'Front-left motor'},
        {'id': 'mB', 'part': 'Getriebemotor', 'x': 370, 'y': 232, 'rotation': 180, 'title': 'Rear-left motor'},
        {'id': 'mC', 'part': 'Getriebemotor', 'x': 582, 'y': -100, 'title': 'Front-right motor'},
        {'id': 'mD', 'part': 'Getriebemotor', 'x': 582, 'y': 25, 'title': 'Rear-right motor'},
        {'id': 'bat', 'part': '8xAA_box', 'x': -100, 'y': 300, 'title': '8 x AA battery box'},
        {'id': 'cam', 'part': 'ESP32-CAM_FRONT-fixed', 'x': 575.7, 'y': 230, 'rotation': 90, 'title': 'ESP32-CAM',
         'snap': {'pin': 'IO14', 'to': 'drv.IN1', 'axis': 'x'}},
        {'id': 'buck', 'part': 'Mini560 buck module', 'x': 700, 'y': 320, 'rotation': 180, 'title': 'Buck 5V'},
        {'id': 'cap', 'core': 'capacitor_electrolytic_small', 'x': 575, 'y': 180, 'title': '470 uF', 'properties': {'capacitance': '470µF'}},
    ],
    shapes=[
        {'a': 'drv.ENA', 'b': 'drv.+5V-J1', 'pad': 42, 'fill': '#1a1a1a', 'stroke': '#000', 'rx': 10},
        {'a': 'drv.ENB', 'b': 'drv.+5V-J2', 'pad': 42, 'fill': '#1a1a1a', 'stroke': '#000', 'rx': 10},
    ],
    wires=[
        {'from': 'mA.pin 2', 'to': 'drv.OUT1', 'color': RED}, {'from': 'mA.pin 1', 'to': 'drv.OUT2', 'color': BLACK},
        {'from': 'mB.pin 2', 'to': 'drv.OUT1', 'color': RED}, {'from': 'mB.pin 1', 'to': 'drv.OUT2', 'color': BLACK},
        {'from': 'mC.pin 1', 'to': 'drv.OUT4', 'color': RED}, {'from': 'mC.pin 2', 'to': 'drv.OUT3', 'color': BLACK},
        {'from': 'mD.pin 1', 'to': 'drv.OUT4', 'color': RED}, {'from': 'mD.pin 2', 'to': 'drv.OUT3', 'color': BLACK},
        {'from': 'bat.+', 'to': 'drv.12V', 'color': RED, 'width': 36},
        {'from': 'bat.-', 'to': 'drv.GND', 'color': BLACK, 'width': 36},
        {'from': 'bat.+', 'to': 'buck.Vin1', 'color': RED, 'width': 36, 'via': [{'ref': 'buck.Vin1', 'dx': -170, 'dy': 950}, {'ref': 'buck.Vin1', 'dx': -170}]},
        {'from': 'bat.-', 'to': 'buck.GND1', 'color': BLACK, 'width': 36, 'via': [{'ref': 'buck.GND1', 'dx': -110, 'dy': 680}, {'ref': 'buck.GND1', 'dx': -110}]},
        {'from': 'drv.IN1', 'to': 'cam.IO14', 'color': ORANGE},
        {'from': 'drv.IN2', 'to': 'cam.IO15', 'color': ORANGE},
        {'from': 'drv.IN3', 'to': 'cam.IO13', 'color': GREEN},
        {'from': 'drv.IN4', 'to': 'cam.IO12', 'color': GREEN},
        {'from': 'buck.Vout1', 'to': 'cam.5V', 'color': RED, 'width': 32,
         'via': [{'ref': 'buck.Vout1', 'dx': 100}, {'ref': 'buck.Vout1', 'dx': 100, 'dy': -1245}, {'ref': 'cam.5V', 'dy': -245}]},
        {'from': 'buck.GND1*', 'to': 'cam.GND', 'color': BLACK, 'width': 32,
         'via': [{'ref': 'buck.GND1*', 'dx': 200}, {'ref': 'buck.GND1*', 'dx': 200, 'dy': -1805}, {'ref': 'cam.GND', 'dy': -355}]},
        {'from': 'cap.+', 'to': 'cam.5V', 'color': RED},
        {'from': 'cap.-', 'to': 'cam.GND', 'color': BLACK},
    ],
    labels=[
        {'ref': 'cam.IO14', 'dy': 300, 'text': '14', 'size': 52},
        {'ref': 'cam.IO15', 'dy': 440, 'text': '15', 'size': 52},
        {'ref': 'cam.IO13', 'dy': 300, 'text': '13', 'size': 52},
        {'ref': 'cam.IO12', 'dy': 440, 'text': '12', 'size': 52},
        {'ref': 'drv.IN1', 'dy': -200, 'text': 'IN1', 'size': 60},
        {'ref': 'drv.IN2', 'dy': -360, 'text': 'IN2', 'size': 60},
        {'ref': 'drv.IN3', 'dy': -200, 'text': 'IN3', 'size': 60},
        {'ref': 'drv.IN4', 'dy': -360, 'text': 'IN4', 'size': 60},
        {'ref': 'drv.12V', 'dx': -150, 'dy': 260, 'text': '12V', 'size': 64},
        {'ref': 'drv.GND', 'dx': 150, 'dy': 260, 'text': 'GND', 'size': 64},
        {'ref': 'bat.+', 'dx': -90, 'dy': -120, 'text': '+', 'size': 90, 'color': RED, 'stroke': RED},
        {'ref': 'bat.-', 'dx': -90, 'dy': 120, 'text': '−', 'size': 90},
        {'ref': 'mA.@b', 'dy': 230, 'text': 'LEFT MOTORS', 'size': 80},
        {'ref': 'mC.@b', 'dy': 260, 'text': 'RIGHT MOTORS', 'size': 80},
        {'ref': 'buck.@b', 'dy': 120, 'text': 'buck 12V → 5V', 'size': 56},
        {'ref': 'cam.@b', 'dy': 120, 'text': 'ESP32-CAM', 'size': 56},
        {'ref': 'cap.@t', 'dx': 250, 'dy': -60, 'text': '470 µF', 'size': 46},
        {'ref': 'drv.+5V-J2', 'dx': 2750, 'dy': 1420, 'text': 'ENA / ENB caps ON', 'size': 50, 'leader': True, 'fill': '#fff8d6', 'stroke': '#b08900'},
    ]))

for s in specs:
    with open(os.path.join(HERE, s['name'] + '.json'), 'w', encoding='utf-8') as f:
        json.dump(s, f, ensure_ascii=False, indent=2)
    print('wrote', s['name'] + '.json')
