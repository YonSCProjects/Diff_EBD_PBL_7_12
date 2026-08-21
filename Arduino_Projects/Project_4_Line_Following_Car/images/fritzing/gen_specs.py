"""gen_specs.py — Project 4 figure specs on the _fritzing_kit pipeline (2026-08-22 regeneration:
4 TT motors, 8xAA battery box, native Uno / breadboard / TCRT5000 parts).
Build each with ../../../_fritzing_kit/build_figure.js <spec.json>.
w_p4_00 / w_p4_03 / w_p4_05 are unchanged Fritzing exports from the older pipeline (see README).
"""
import json, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))
RED, BLACK, ORANGE, GREEN = '#cc1414', '#000000', '#f28a00', '#25cc35'

DRV = {'id': 'drv', 'part': 'L298N-DC-motor-driver-improved', 'x': 400, 'y': 0, 'title': 'L298N'}
MOTORS = [
    {'id': 'mA', 'part': 'Getriebemotor', 'x': 370, 'y': 72, 'rotation': 180, 'title': 'Front-left motor'},
    {'id': 'mB', 'part': 'Getriebemotor', 'x': 370, 'y': 232, 'rotation': 180, 'title': 'Rear-left motor'},
    {'id': 'mC', 'part': 'Getriebemotor', 'x': 582, 'y': -45, 'title': 'Front-right motor'},
    {'id': 'mD', 'part': 'Getriebemotor', 'x': 582, 'y': 115, 'title': 'Rear-right motor'},
]
BAT = {'id': 'bat', 'part': '8xAA_box', 'x': -170, 'y': 300, 'title': '8 x AA battery box'}
UNO = {'id': 'uno', 'core': 'arduino_Uno_Rev3(fix)', 'x': 440, 'y': 250, 'title': 'Arduino Uno',
       'snap': {'pin': 'c53', 'to': 'drv.ENA', 'axis': 'x'}}          # D10 straight under ENA
BB = {'id': 'bb', 'core': 'breadboard2', 'x': 600, 'y': 290, 'title': 'Breadboard'}
SENS = [
    {'id': 'sL', 'part': 'TCRT5000 line sensor', 'x': 720, 'y': 520, 'title': 'LEFT line sensor'},
    {'id': 'sR', 'part': 'TCRT5000 line sensor', 'x': 890, 'y': 520, 'title': 'RIGHT line sensor'},
]

MOTOR_WIRES = [
    {'from': 'mA.pin 2', 'to': 'drv.OUT1', 'color': RED}, {'from': 'mA.pin 1', 'to': 'drv.OUT2', 'color': BLACK},
    {'from': 'mB.pin 2', 'to': 'drv.OUT1', 'color': RED}, {'from': 'mB.pin 1', 'to': 'drv.OUT2', 'color': BLACK},
    {'from': 'mC.pin 1', 'to': 'drv.OUT4', 'color': RED}, {'from': 'mC.pin 2', 'to': 'drv.OUT3', 'color': BLACK},
    {'from': 'mD.pin 1', 'to': 'drv.OUT4', 'color': RED}, {'from': 'mD.pin 2', 'to': 'drv.OUT3', 'color': BLACK},
]
MOTOR_LABELS = [
    {'ref': 'mA.@b', 'dy': 230, 'text': 'LEFT MOTORS', 'size': 80},
    {'ref': 'mC.@b', 'dy': 230, 'text': 'RIGHT MOTORS', 'size': 80},
]
BAT_WIRES = [
    {'from': 'bat.+', 'to': 'drv.12V', 'color': RED, 'width': 36},
    {'from': 'bat.-', 'to': 'drv.GND', 'color': BLACK, 'width': 36},
]
BAT_LABELS = [
    {'ref': 'bat.+', 'dx': -90, 'dy': -120, 'text': '+', 'size': 90, 'color': RED, 'stroke': RED},
    {'ref': 'bat.-', 'dx': -90, 'dy': 120, 'text': '−', 'size': 90},
    {'ref': 'drv.12V', 'dx': -150, 'dy': 260, 'text': '12V', 'size': 64},
    {'ref': 'drv.GND', 'dx': 150, 'dy': 260, 'text': 'GND', 'size': 64},
]
# common ground + Uno power to the breadboard's bottom rails (W = +, X = -)
POWER_WIRES = [
    {'from': 'drv.GND', 'to': 'uno.c89', 'color': BLACK, 'width': 44},
    {'from': 'uno.c87', 'to': 'bb.pin5W', 'color': RED, 'route': 'vh', 'width': 32},
    {'from': 'uno.c88', 'to': 'bb.pin3X', 'color': BLACK, 'route': 'vh', 'width': 32},
]
POWER_LABELS = [
    {'ref': 'uno.c89', 'dx': 120, 'dy': 260, 'text': '★ common ground', 'size': 64, 'fill': '#fff8d6', 'stroke': '#b08900'},
    {'ref': 'uno.c87', 'dx': -260, 'dy': 420, 'text': '5V', 'size': 56},
    {'ref': 'bb.pin3W', 'dx': -150, 'dy': 0, 'text': '+', 'size': 60, 'color': RED, 'stroke': RED},
    {'ref': 'bb.pin3X', 'dx': -150, 'dy': 0, 'text': '−', 'size': 60},
]
SIGNAL_WIRES = [
    {'from': 'drv.ENA', 'to': 'uno.c53', 'color': GREEN},
    {'from': 'drv.IN1', 'to': 'uno.c52', 'color': ORANGE},
    {'from': 'drv.IN2', 'to': 'uno.c51', 'color': ORANGE},
    {'from': 'drv.IN3', 'to': 'uno.c68', 'color': ORANGE},
    {'from': 'drv.IN4', 'to': 'uno.c67', 'color': ORANGE},
    {'from': 'drv.ENB', 'to': 'uno.c66', 'color': GREEN},
]
SIGNAL_LABELS = [
    {'ref': 'drv.ENA', 'dy': -200, 'text': 'ENA', 'size': 60}, {'ref': 'drv.IN1', 'dy': -360, 'text': 'IN1', 'size': 60},
    {'ref': 'drv.IN2', 'dy': -200, 'text': 'IN2', 'size': 60}, {'ref': 'drv.IN3', 'dy': -360, 'text': 'IN3', 'size': 60},
    {'ref': 'drv.IN4', 'dy': -200, 'text': 'IN4', 'size': 60}, {'ref': 'drv.ENB', 'dy': -360, 'text': 'ENB', 'size': 60},
    {'ref': 'uno.c53', 'dy': 300, 'text': '10', 'size': 60}, {'ref': 'uno.c52', 'dy': 440, 'text': '9', 'size': 60},
    {'ref': 'uno.c51', 'dy': 300, 'text': '8', 'size': 60}, {'ref': 'uno.c68', 'dy': 440, 'text': '7', 'size': 60},
    {'ref': 'uno.c67', 'dy': 300, 'text': '6', 'size': 60}, {'ref': 'uno.c66', 'dy': 440, 'text': '5', 'size': 60},
]
SENSOR_WIRES = [
    {'from': 'sL.Vcc', 'to': 'bb.pin21W', 'color': RED, 'route': 'vh', 'out': ['left', 100]},
    {'from': 'sL.Gnd', 'to': 'bb.pin23X', 'color': BLACK, 'route': 'vh', 'out': ['left', 200]},
    {'from': 'sL.Do', 'to': 'uno.c54', 'color': ORANGE, 'route': 'vh', 'out': ['left', 300], 'via': [{'ref': 'uno.c54', 'dy': -350}]},
    {'from': 'sR.Vcc', 'to': 'bb.pin40W', 'color': RED, 'route': 'vh', 'out': ['left', 100]},
    {'from': 'sR.Gnd', 'to': 'bb.pin42X', 'color': BLACK, 'route': 'vh', 'out': ['left', 200]},
    {'from': 'sR.Do', 'to': 'uno.c55', 'color': GREEN, 'route': 'vh', 'out': ['left', 400], 'via': [{'ref': 'uno.c55', 'dy': -500}]},
]
SENSOR_LABELS = [
    {'ref': 'sL.@b', 'dy': 110, 'text': 'LEFT sensor → 11', 'size': 56},
    {'ref': 'sR.@b', 'dy': 110, 'text': 'RIGHT sensor → 12', 'size': 56},
    {'ref': 'uno.c54', 'dx': -160, 'dy': -110, 'text': '11', 'size': 56},
    {'ref': 'uno.c55', 'dx': 160, 'dy': -110, 'text': '12', 'size': 56},
]

def spec(name, instances, wires, labels):
    return {'name': name, 'out_dir': '..', 'assets_dir': '../../task_cards_he/assets',
            'instances': copy.deepcopy(instances), 'shapes': [], 'wires': copy.deepcopy(wires), 'labels': copy.deepcopy(labels)}

specs = [
    spec('w_p4_01_motors_to_driver', [DRV] + MOTORS, MOTOR_WIRES, MOTOR_LABELS),
    spec('w_p4_02_power_and_common_ground', [DRV, BAT, UNO, BB], BAT_WIRES + POWER_WIRES, BAT_LABELS + POWER_LABELS),
    spec('w_p4_04_line_sensors', [UNO, BB] + SENS,
         [{'from': 'uno.c87', 'to': 'bb.pin5W', 'color': RED, 'route': 'vh', 'width': 32},
          {'from': 'uno.c88', 'to': 'bb.pin3X', 'color': BLACK, 'route': 'vh', 'width': 32}] + SENSOR_WIRES,
         POWER_LABELS[1:] + SENSOR_LABELS),
    spec('w_p4_01_driver_wiring', [DRV] + MOTORS + [BAT, UNO, BB] + SENS,
         MOTOR_WIRES + BAT_WIRES + POWER_WIRES + SIGNAL_WIRES + SENSOR_WIRES,
         MOTOR_LABELS + BAT_LABELS + POWER_LABELS + SIGNAL_LABELS + SENSOR_LABELS),
]
# the sensors-only figure has no L298N to snap the Uno to
for s in specs:
    if s['name'] == 'w_p4_04_line_sensors':
        for i in s['instances']:
            if i['id'] == 'uno': i.pop('snap', None)

for s in specs:
    with open(os.path.join(HERE, s['name'] + '.json'), 'w', encoding='utf-8') as f:
        json.dump(s, f, ensure_ascii=False, indent=2)
    print('wrote', s['name'] + '.json')
