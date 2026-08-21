"""gen_specs.py — emits the five Project 6 figure specs (run, then build each with
../../../_fritzing_kit/build_figure.js). One shared station layout so every
figure is literally "the previous one plus one part".

Layout (sketch px, 90 px = 1 in): breadboard at (0,330) — top rails Z (-) / Y (+);
ESP32 DevKit left; OLED plugged into row F at columns 18-21 (body hangs over the
bottom half); DHT22 plugged into row J at columns 40-42 (body above the board).
"""
import json, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))
RED, BLACK, ORANGE, GREEN, BLUE = '#cc1414', '#000000', '#f28a00', '#25cc35', '#418dd9'

def base(name):
    return {
        'name': name, 'out_dir': '..', 'assets_dir': '../../task_cards_he/assets',
        'instances': [
            {'id': 'bb', 'core': 'breadboard2', 'x': 0, 'y': 330, 'title': 'Breadboard'},
            {'id': 'esp', 'part': 'DOIT Esp32 DevKit v1 improved', 'x': 20, 'y': 110, 'title': 'ESP32 DevKit V1'},
            {'id': 'dht', 'part': 'DHT22 temperature-humidity sensor', 'x': 347, 'y': 230, 'title': 'DHT22',
             'snap': {'pin': 'VCC', 'to': 'bb.pin40J'}},
        ],
        'shapes': [],
        'wires': [
            # power rails from the ESP32 (right-hand column, bottom pins)
            {'from': 'esp.3V3', 'to': 'bb.pin12Y', 'color': RED, 'route': 'vh', 'width': 32},
            {'from': 'esp.GND.2', 'to': 'bb.pin15Z', 'color': BLACK, 'route': 'vh', 'width': 32, 'out': ['right', 150]},
            # DHT22: + and - to the rails, out to GPIO 4
            {'from': 'bb.pin40I', 'to': 'bb.pin39Y', 'color': RED, 'route': 'hv'},
            {'from': 'bb.pin42I', 'to': 'bb.pin45Z', 'color': BLACK, 'route': 'hv'},
            {'from': 'bb.pin41G', 'to': 'esp.D4', 'color': ORANGE, 'route': 'hv', 'via': [{'ref': 'esp.D4', 'dx': 330}]},
        ],
        'labels': [
            {'ref': 'esp.3V3', 'dx': 200, 'text': '3V3', 'size': 52},
            {'ref': 'esp.GND.2', 'dx': 420, 'text': 'GND', 'size': 52},
            {'ref': 'esp.D4', 'dx': -210, 'text': '4', 'size': 56},
            {'ref': 'bb.pin3Y', 'dx': -150, 'text': '+', 'size': 60, 'color': RED, 'stroke': RED},
            {'ref': 'bb.pin3Z', 'dx': -150, 'dy': -120, 'text': '−', 'size': 60},
            {'ref': 'dht.@t', 'dy': -110, 'text': 'DHT22', 'size': 52},
            {'ref': 'bb.pin40J', 'dx': 0, 'dy': 430, 'text': '+', 'size': 46, 'color': RED, 'stroke': RED},
            {'ref': 'bb.pin41J', 'dx': 0, 'dy': 560, 'text': 'out', 'size': 46},
            {'ref': 'bb.pin42J', 'dx': 0, 'dy': 430, 'text': '−', 'size': 46},
        ],
    }

OLED_INST = {'id': 'oled', 'part': 'OLED-128x64-I2C-Monochrome-Display-GND-VDD', 'x': 132, 'y': 404, 'title': 'OLED SSD1306',
             'snap': {'pin': 'GND', 'to': 'bb.pin18F'}}
OLED_WIRES = [
    {'from': 'bb.pin18J', 'to': 'bb.pin18Z', 'color': BLACK},
    {'from': 'bb.pin19J', 'to': 'bb.pin19Y', 'color': RED},
    {'from': 'bb.pin20I', 'to': 'esp.D22', 'color': GREEN, 'route': 'hv', 'via': [{'ref': 'esp.D22', 'dx': 620}]},
    {'from': 'bb.pin21H', 'to': 'esp.D21', 'color': BLUE, 'route': 'hv', 'via': [{'ref': 'esp.D21', 'dx': 470}]},
]
OLED_LABELS = [
    {'ref': 'esp.D22', 'dx': -210, 'text': '22', 'size': 56},
    {'ref': 'esp.D21', 'dx': -430, 'text': '21', 'size': 56},
    {'ref': 'oled.@b', 'dy': 110, 'text': 'OLED  (SDA → 21, SCL → 22)', 'size': 46},
]

specs = {}

# 1 — DHT22 only
s = base('w_p6_01_dht22'); specs[s['name']] = s

# 2 — station: DHT22 + OLED
s = base('w_p6_02_dht22_oled')
s['instances'].append(copy.deepcopy(OLED_INST)); s['wires'] += copy.deepcopy(OLED_WIRES); s['labels'] += copy.deepcopy(OLED_LABELS)
specs[s['name']] = s

# 3a — + LED with 220 ohm on GPIO 26
s = base('w_p6_03a_led')
s['instances'].append(copy.deepcopy(OLED_INST)); s['wires'] += copy.deepcopy(OLED_WIRES)
s['instances'] += [
    {'id': 'led', 'core': 'LED-generic-5mm', 'x': 40, 'y': 400, 'title': 'LED', 'snap': {'pin': 'cathode', 'to': 'bb.pin5E', 'offset': [0, -30.8]},
     'properties': {'color': 'Red (633nm)'}},
    {'id': 'res', 'core': 'resistor', 'x': 50, 'y': 450, 'title': '220 ohm', 'snap': {'pin': 'Pin 0', 'to': 'bb.pin6C'},
     'properties': {'resistance': '220'}},
]
s['wires'] += [
    {'from': 'bb.pin10B', 'to': 'esp.D26', 'color': ORANGE, 'route': 'hv', 'via': [{'ref': 'esp.D26', 'dx': -220}]},
    {'from': 'bb.pin5D', 'to': 'bb.pin4Z', 'color': BLACK, 'route': 'hv'},
]
s['labels'] += [
    {'ref': 'esp.D26', 'dx': 210, 'text': '26', 'size': 56},
    {'ref': 'res.@t', 'dy': -90, 'text': '220 Ω', 'size': 46},
    {'ref': 'led.@t', 'dx': -20, 'dy': -90, 'text': 'LED', 'size': 46},
]
specs[s['name']] = s

# 3b — + active buzzer on GPIO 27
s = base('w_p6_03b_buzzer')
s['instances'].append(copy.deepcopy(OLED_INST)); s['wires'] += copy.deepcopy(OLED_WIRES)
s['instances'].append({'id': 'buz', 'core': 'SparkFun-Electromechanical-BUZZER-PTH-NS-KIT', 'x': 40, 'y': 380, 'title': 'Buzzer',
                       'snap': {'pin': '1', 'to': 'bb.pin8C'}})
s['wires'] += [
    {'from': 'bb.pin8J', 'to': 'bb.pin9Z', 'color': BLACK, 'route': 'hv'},
    {'from': 'bb.pin8A', 'to': 'esp.D27', 'color': ORANGE, 'route': 'hv', 'via': [{'ref': 'esp.D27', 'dx': -220}]},
]
s['labels'] += [
    {'ref': 'esp.D27', 'dx': 210, 'text': '27', 'size': 56},
    {'ref': 'bb.pin8H', 'dx': 230, 'dy': -40, 'text': '−', 'size': 50},
    {'ref': 'bb.pin8C', 'dx': 230, 'dy': 40, 'text': '+', 'size': 50, 'color': RED, 'stroke': RED},
]
specs[s['name']] = s

# 3c — + servo on GPIO 14 (power from VIN)
s = base('w_p6_03c_servo')
s['instances'].append(copy.deepcopy(OLED_INST)); s['wires'] += copy.deepcopy(OLED_WIRES)
s['instances'].append({'id': 'servo', 'core': 'servo', 'x': -150, 'y': 150, 'title': 'Servo'})
s['wires'] += [
    {'from': 'servo.pulse', 'to': 'esp.D14', 'color': ORANGE, 'route': 'vh', 'out': ['right', 180]},
    {'from': 'servo.vcc', 'to': 'esp.VIN', 'color': RED, 'route': 'vh', 'out': ['right', 100]},
    {'from': 'servo.gnd', 'to': 'bb.pin3Z', 'color': BLACK, 'route': 'vh', 'out': ['right', 40]},
]
s['labels'] += [
    {'ref': 'esp.D14', 'dx': 210, 'text': '14', 'size': 56},
    {'ref': 'esp.VIN', 'dx': 210, 'text': 'VIN', 'size': 52},
    {'ref': 'servo.@t', 'dy': -90, 'text': 'Servo', 'size': 50},
]
specs[s['name']] = s

for name, spec in specs.items():
    with open(os.path.join(HERE, name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    print('wrote', name + '.json')
