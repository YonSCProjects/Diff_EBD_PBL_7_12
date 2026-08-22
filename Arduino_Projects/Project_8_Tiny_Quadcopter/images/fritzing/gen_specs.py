"""gen_specs.py — Project 8 (tiny quadcopter) figure specs on the _fritzing_kit pipeline.
Build each with ../../../_fritzing_kit/build_figure.js <spec.json>.
Parts: DevKit V1 (kit), MT3608 boost module (kit), LiPo 1S (kit, Adafruit pouch), mosfet_board_4ch +
motor_8520_cw/ccw (drawn in the kit), core InvenSense_MPU6050 (GY-521), basic_fet_n (TO-220), schottky diode, resistor.
Pin map (locked 2026-08-22): FRONT 25, RIGHT 26, BACK 14, LEFT 27; I2C SDA 21 / SCL 22; DevKit VIN <- MT3608 OUT 5.0 V.
Rotation pairs: FRONT+BACK = CW (red/blue leads), RIGHT+LEFT = CCW (white/black leads).
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
RED, BLACK, ORANGE, GREEN, BLUE, YELLOW, PURPLE = '#cc1414', '#000000', '#f28a00', '#25cc35', '#418dd9', '#e0b400', '#8e44ad'

def spec(name, **kw):
    d = {'name': name, 'out_dir': '..', 'assets_dir': '../../task_cards_he/assets', 'instances': [], 'shapes': [], 'wires': [], 'labels': []}
    d.update(kw); return d

specs = []

# 1 — one MOSFET channel, pictorial schematic (what Tier 2 solders four times)
#   BAT+ rail along the top (y = 40 px), GND rail along the bottom (y = 300 px); FET legs point down,
#   so the drain is fed from above via the motor/diode node and gate/source fan out below.
specs.append(spec('w_p8_01_mosfet_channel', preview_scale=2,
    instances=[
        {'id': 'lipo', 'part': 'lipo_1s_1000', 'x': 0, 'y': 120, 'title': '1S LiPo'},
        {'id': 'm', 'part': 'motor_8520_cw', 'x': 420, 'y': 60, 'title': 'Motor'},
        {'id': 'd', 'core': 'diode_schottky_1N5817_300mil', 'x': 580, 'y': 60, 'rotation': 90, 'title': 'Flyback diode'},
        {'id': 'fet', 'core': 'basic_fet_n', 'x': 480, 'y': 120, 'title': 'IRLB8721'},
        {'id': 'rg', 'core': 'resistor', 'x': 340, 'y': 230, 'title': '100 ohm', 'properties': {'resistance': '100'}},
        {'id': 'rp', 'core': 'resistor', 'x': 530, 'y': 228, 'rotation': 90, 'title': '10k', 'properties': {'resistance': '10k'}},
    ],
    wires=[
        # BAT+ : plug -> up to the top rail -> motor + ; rail continues to the diode's band end
        {'from': 'lipo.+', 'to': 'm.+', 'color': RED, 'width': 32, 'via': [{'ref': 'lipo.+', 'dx': 180}, {'ref': 'lipo.+', 'dx': 180, 'dy': -1455}, {'ref': 'm.+', 'dx': -260, 'dy': -411}, {'ref': 'm.+', 'dx': -260}]},
        {'from': {'ref': 'm.+', 'dx': -260, 'dy': -411}, 'to': 'd.cathode', 'color': RED, 'width': 32, 'via': [{'ref': 'd.cathode', 'dy': -229}]},
        # motor - and diode anode meet at the drain
        {'from': 'm.-', 'to': 'fet.drain', 'color': BLACK, 'width': 30},
        {'from': 'd.anode', 'to': 'fet.drain', 'color': BLACK, 'width': 30},
        # gate: 100 ohm from the GPIO, 10k pull-down to GND
        {'from': 'fet.gate', 'to': 'rg.Pin 1', 'color': ORANGE},
        {'from': 'fet.gate', 'to': 'rp.Pin 0', 'color': ORANGE},
        {'from': {'ref': 'rg.Pin 0', 'dx': -450}, 'to': 'rg.Pin 0', 'color': ORANGE},
        # GND rail: plug - -> down to the bottom rail -> source ; pull-down joins the rail
        {'from': 'lipo.-', 'to': 'fet.source', 'color': BLACK, 'width': 32, 'via': [{'ref': 'lipo.-', 'dx': 300}, {'ref': 'lipo.-', 'dx': 300, 'dy': 1154}, {'ref': 'fet.source', 'dy': 1410}]},
        {'from': 'rp.Pin 1', 'to': {'ref': 'fet.source', 'dy': 1410}, 'color': BLACK, 'via': [{'ref': 'rp.Pin 1', 'dy': 366}]},
    ],
    labels=[
        {'ref': 'rg.Pin 0', 'dx': -640, 'text': 'GPIO 25', 'size': 50, 'fill': '#fff3e0', 'stroke': '#b06000'},
        {'ref': 'rg.@t', 'dy': -90, 'text': '100 Ω', 'size': 44},
        {'ref': 'rp.@r', 'dx': 260, 'text': '10 kΩ\npull-down', 'size': 40},
        {'ref': 'fet.@r', 'dx': 330, 'dy': -100, 'text': 'IRLB8721\nG · D · S', 'size': 44},
        {'ref': 'd.@r', 'dx': 360, 'text': 'flyback\nband → BAT+', 'size': 40},
        {'ref': 'm.@t', 'dy': -130, 'text': 'M1', 'size': 50},
        {'ref': 'lipo.+', 'dx': 180, 'dy': -1600, 'text': 'BAT+', 'size': 50, 'color': RED, 'stroke': RED},
        {'ref': 'lipo.-', 'dx': 300, 'dy': 1300, 'text': 'GND', 'size': 50},
    ]))


# 2 — the four-channel board alone, with callouts
specs.append(spec('w_p8_02_mosfet_board', preview_scale=2,
    instances=[{'id': 'b', 'part': 'mosfet_board_4ch', 'x': 100, 'y': 100, 'title': 'MOSFET board'}],
    labels=[
        {'ref': 'b.BAT+', 'dx': -300, 'text': 'BAT+', 'size': 60, 'color': RED, 'stroke': RED},
        {'ref': 'b.GND', 'dx': -300, 'text': 'GND', 'size': 60},
        {'ref': 'b.M1+', 'dx': 100, 'dy': -330, 'text': 'M1 = FRONT', 'size': 52},
        {'ref': 'b.M2+', 'dx': 100, 'dy': -330, 'text': 'M2 = RIGHT', 'size': 52},
        {'ref': 'b.M3+', 'dx': 100, 'dy': -330, 'text': 'M3 = BACK', 'size': 52},
        {'ref': 'b.M4+', 'dx': 100, 'dy': -330, 'text': 'M4 = LEFT', 'size': 52},
        {'ref': 'b.G1', 'dy': 360, 'text': 'G1 ← 25', 'size': 50},
        {'ref': 'b.G2', 'dy': 360, 'text': 'G2 ← 26', 'size': 50},
        {'ref': 'b.G3', 'dy': 360, 'text': 'G3 ← 14', 'size': 50},
        {'ref': 'b.G4', 'dy': 360, 'text': 'G4 ← 27', 'size': 50},
    ]))

# 3 — power tree: LiPo -> MT3608 -> DevKit VIN ; LiPo -> board BAT+/GND ; DevKit 3V3 -> MPU
specs.append(spec('w_p8_03_power_tree',
    instances=[
        {'id': 'lipo', 'part': 'lipo_1s_1000', 'x': -60, 'y': 80, 'title': '1S LiPo 1000 mAh'},
        {'id': 'mt', 'part': 'mt3608_module', 'x': 150, 'y': 40, 'title': 'MT3608 → 5.0 V'},
        {'id': 'esp', 'part': 'DOIT Esp32 DevKit v1 improved', 'x': 330, 'y': 0, 'title': 'ESP32 DevKit V1'},
        {'id': 'mpu', 'core': 'InvenSense_MPU6050', 'x': 520, 'y': 40, 'title': 'MPU6050'},
        {'id': 'b', 'part': 'mosfet_board_4ch', 'x': 150, 'y': 250, 'title': 'MOSFET board'},
    ],
    wires=[
        {'from': 'lipo.+', 'to': 'mt.Vin', 'color': RED, 'width': 34, 'route': 'hv'},
        {'from': 'lipo.-', 'to': 'mt.GND', 'color': BLACK, 'width': 34, 'route': 'hv'},
        {'from': 'mt.Vout', 'to': 'esp.VIN', 'color': RED, 'width': 32, 'route': 'hv'},
        {'from': 'mt.GND*', 'to': 'esp.GND', 'color': BLACK, 'width': 32, 'route': 'hv'},
        {'from': 'lipo.+', 'to': 'b.BAT+', 'color': RED, 'width': 34, 'route': 'vh', 'out': ['right', 120]},
        {'from': 'lipo.-', 'to': 'b.GND', 'color': BLACK, 'width': 34, 'route': 'vh', 'out': ['right', 240]},
        {'from': 'esp.3V3', 'to': 'mpu.VCC', 'color': RED, 'route': 'hv', 'out': ['right', 200]},
        {'from': 'esp.GND.2', 'to': 'mpu.GND', 'color': BLACK, 'route': 'hv', 'out': ['right', 300]},
    ],
    labels=[
        {'ref': 'mt.Vin', 'dx': -60, 'dy': -120, 'text': 'IN', 'size': 48}, {'ref': 'mt.Vout', 'dx': 60, 'dy': -120, 'text': 'OUT 5.0 V', 'size': 48},
        {'ref': 'esp.VIN', 'dx': -230, 'text': 'VIN', 'size': 54}, {'ref': 'esp.GND', 'dx': -240, 'text': 'GND', 'size': 54},
        {'ref': 'esp.3V3', 'dx': 230, 'text': '3V3', 'size': 52}, {'ref': 'esp.GND.2', 'dx': 450, 'text': 'GND', 'size': 52},
        {'ref': 'mpu.VCC', 'dx': -200, 'text': 'VCC', 'size': 44}, {'ref': 'mpu.GND', 'dx': -200, 'text': 'GND', 'size': 44},
        {'ref': 'b.BAT+', 'dx': -260, 'text': 'BAT+', 'size': 54, 'color': RED, 'stroke': RED}, {'ref': 'b.GND', 'dx': -260, 'text': 'GND', 'size': 54},
        {'ref': 'mt.@t', 'dy': -110, 'text': 'MT3608 — pre-tuned to 5.0 V', 'size': 50},
        {'ref': 'lipo.@b', 'dy': 120, 'text': '1S LiPo · PH2.0', 'size': 50},
    ]))

# 4 — motors to the board (2 CW + 2 CCW)
specs.append(spec('w_p8_04_motors',
    instances=[
        {'id': 'b', 'part': 'mosfet_board_4ch', 'x': 0, 'y': 200, 'title': 'MOSFET board'},
        {'id': 'mF', 'part': 'motor_8520_cw', 'x': 42, 'y': 160, 'rotation': 270, 'title': 'FRONT (CW)', 'snap': {'pin': '+', 'to': 'b.M1+', 'axis': 'x', 'offset': [2.5, 0]}},
        {'id': 'mR', 'part': 'motor_8520_ccw', 'x': 93, 'y': 160, 'rotation': 270, 'title': 'RIGHT (CCW)', 'snap': {'pin': '+', 'to': 'b.M2+', 'axis': 'x', 'offset': [2.5, 0]}},
        {'id': 'mB', 'part': 'motor_8520_cw', 'x': 145, 'y': 160, 'rotation': 270, 'title': 'BACK (CW)', 'snap': {'pin': '+', 'to': 'b.M3+', 'axis': 'x', 'offset': [2.5, 0]}},
        {'id': 'mL', 'part': 'motor_8520_ccw', 'x': 196, 'y': 160, 'rotation': 270, 'title': 'LEFT (CCW)', 'snap': {'pin': '+', 'to': 'b.M4+', 'axis': 'x', 'offset': [2.5, 0]}},
    ],
    wires=[
        {'from': 'mF.+', 'to': 'b.M1+', 'color': RED, 'route': 'vh'}, {'from': 'mF.-', 'to': 'b.M1-', 'color': BLUE, 'route': 'vh'},
        {'from': 'mR.+', 'to': 'b.M2+', 'color': '#e8e8e8', 'route': 'vh'}, {'from': 'mR.-', 'to': 'b.M2-', 'color': BLACK, 'route': 'vh'},
        {'from': 'mB.+', 'to': 'b.M3+', 'color': RED, 'route': 'vh'}, {'from': 'mB.-', 'to': 'b.M3-', 'color': BLUE, 'route': 'vh'},
        {'from': 'mL.+', 'to': 'b.M4+', 'color': '#e8e8e8', 'route': 'vh'}, {'from': 'mL.-', 'to': 'b.M4-', 'color': BLACK, 'route': 'vh'},
    ],
    labels=[
        {'ref': 'mF.@t', 'dy': -100, 'text': 'FRONT\nCW', 'size': 46}, {'ref': 'mR.@t', 'dy': -100, 'text': 'RIGHT\nCCW', 'size': 46},
        {'ref': 'mB.@t', 'dy': -100, 'text': 'BACK\nCW', 'size': 46}, {'ref': 'mL.@t', 'dy': -100, 'text': 'LEFT\nCCW', 'size': 46},
    ]))

# 5 — signals: DevKit 25/26/14/27 -> G1..G4 ; 21/22 -> MPU SDA/SCL
specs.append(spec('w_p8_05_signals',
    instances=[
        {'id': 'esp', 'part': 'DOIT Esp32 DevKit v1 improved', 'x': 0, 'y': 0, 'title': 'ESP32 DevKit V1'},
        {'id': 'mpu', 'core': 'InvenSense_MPU6050', 'x': 200, 'y': 20, 'title': 'MPU6050'},
        {'id': 'b', 'part': 'mosfet_board_4ch', 'x': -100, 'y': 260, 'title': 'MOSFET board'},
    ],
    wires=[
        {'from': 'esp.D25', 'to': 'b.G1', 'color': ORANGE, 'route': 'hv', 'out': ['left', 150]},
        {'from': 'esp.D26', 'to': 'b.G2', 'color': ORANGE, 'route': 'hv', 'out': ['left', 300]},
        {'from': 'esp.D14', 'to': 'b.G3', 'color': GREEN, 'route': 'hv', 'out': ['left', 450]},
        {'from': 'esp.D27', 'to': 'b.G4', 'color': GREEN, 'route': 'hv', 'out': ['left', 600]},
        {'from': 'esp.D21', 'to': 'mpu.SDA', 'color': BLUE, 'route': 'hv', 'out': ['right', 200]},
        {'from': 'esp.D22', 'to': 'mpu.SCL', 'color': YELLOW, 'route': 'hv', 'out': ['right', 350]},
    ],
    labels=[
        {'ref': 'esp.D25', 'dx': 230, 'text': '25 → G1 FRONT', 'size': 46}, {'ref': 'esp.D26', 'dx': 230, 'text': '26 → G2 RIGHT', 'size': 46},
        {'ref': 'esp.D14', 'dx': 230, 'text': '14 → G3 BACK', 'size': 46}, {'ref': 'esp.D27', 'dx': 230, 'text': '27 → G4 LEFT', 'size': 46},
        {'ref': 'esp.D21', 'dx': -230, 'text': '21 SDA', 'size': 46}, {'ref': 'esp.D22', 'dx': -230, 'text': '22 SCL', 'size': 46},
        {'ref': 'mpu.@t', 'dy': -110, 'text': 'MPU6050 — arrow forward, flat', 'size': 48},
    ]))

# 6 — full map
specs.append(spec('w_p8_06_full_drone',
    instances=[
        {'id': 'esp', 'part': 'DOIT Esp32 DevKit v1 improved', 'x': 0, 'y': 0, 'title': 'ESP32 DevKit V1'},
        {'id': 'mpu', 'core': 'InvenSense_MPU6050', 'x': 200, 'y': 20, 'title': 'MPU6050'},
        {'id': 'mt', 'part': 'mt3608_module', 'x': -200, 'y': 120, 'title': 'MT3608 → 5.0 V'},
        {'id': 'lipo', 'part': 'lipo_1s_1000', 'x': -300, 'y': 150, 'title': '1S LiPo 1000 mAh'},
        {'id': 'b', 'part': 'mosfet_board_4ch', 'x': -100, 'y': 420, 'title': 'MOSFET board'},
        {'id': 'mF', 'part': 'motor_8520_cw', 'x': -58, 'y': 380, 'rotation': 270, 'title': 'FRONT (CW)', 'snap': {'pin': '+', 'to': 'b.M1+', 'axis': 'x', 'offset': [2.5, 0]}},
        {'id': 'mR', 'part': 'motor_8520_ccw', 'x': -7, 'y': 380, 'rotation': 270, 'title': 'RIGHT (CCW)', 'snap': {'pin': '+', 'to': 'b.M2+', 'axis': 'x', 'offset': [2.5, 0]}},
        {'id': 'mB', 'part': 'motor_8520_cw', 'x': 45, 'y': 380, 'rotation': 270, 'title': 'BACK (CW)', 'snap': {'pin': '+', 'to': 'b.M3+', 'axis': 'x', 'offset': [2.5, 0]}},
        {'id': 'mL', 'part': 'motor_8520_ccw', 'x': 96, 'y': 380, 'rotation': 270, 'title': 'LEFT (CCW)', 'snap': {'pin': '+', 'to': 'b.M4+', 'axis': 'x', 'offset': [2.5, 0]}},
    ],
    wires=[
        {'from': 'lipo.+', 'to': 'mt.Vin', 'color': RED, 'width': 34, 'route': 'hv'},
        {'from': 'lipo.-', 'to': 'mt.GND', 'color': BLACK, 'width': 34, 'route': 'hv'},
        {'from': 'mt.Vout', 'to': 'esp.VIN', 'color': RED, 'width': 32, 'route': 'hv'},
        {'from': 'mt.GND*', 'to': 'esp.GND', 'color': BLACK, 'width': 32, 'route': 'hv'},
        {'from': 'lipo.+', 'to': 'b.BAT+', 'color': RED, 'width': 34, 'route': 'vh', 'out': ['right', 120]},
        {'from': 'lipo.-', 'to': 'b.GND', 'color': BLACK, 'width': 34, 'route': 'vh', 'out': ['right', 240]},
        {'from': 'esp.3V3', 'to': 'mpu.VCC', 'color': RED, 'route': 'hv', 'out': ['right', 200]},
        {'from': 'esp.GND.2', 'to': 'mpu.GND', 'color': BLACK, 'route': 'hv', 'out': ['right', 300]},
        {'from': 'esp.D21', 'to': 'mpu.SDA', 'color': BLUE, 'route': 'hv', 'out': ['right', 400]},
        {'from': 'esp.D22', 'to': 'mpu.SCL', 'color': YELLOW, 'route': 'hv', 'out': ['right', 500]},
        {'from': 'esp.D25', 'to': 'b.G1', 'color': ORANGE, 'route': 'hv', 'out': ['left', 150]},
        {'from': 'esp.D26', 'to': 'b.G2', 'color': ORANGE, 'route': 'hv', 'out': ['left', 300]},
        {'from': 'esp.D14', 'to': 'b.G3', 'color': GREEN, 'route': 'hv', 'out': ['left', 450]},
        {'from': 'esp.D27', 'to': 'b.G4', 'color': GREEN, 'route': 'hv', 'out': ['left', 600]},
        {'from': 'mF.+', 'to': 'b.M1+', 'color': RED, 'route': 'vh'}, {'from': 'mF.-', 'to': 'b.M1-', 'color': BLUE, 'route': 'vh'},
        {'from': 'mR.+', 'to': 'b.M2+', 'color': '#e8e8e8', 'route': 'vh'}, {'from': 'mR.-', 'to': 'b.M2-', 'color': BLACK, 'route': 'vh'},
        {'from': 'mB.+', 'to': 'b.M3+', 'color': RED, 'route': 'vh'}, {'from': 'mB.-', 'to': 'b.M3-', 'color': BLUE, 'route': 'vh'},
        {'from': 'mL.+', 'to': 'b.M4+', 'color': '#e8e8e8', 'route': 'vh'}, {'from': 'mL.-', 'to': 'b.M4-', 'color': BLACK, 'route': 'vh'},
    ],
    labels=[
        {'ref': 'esp.D25', 'dx': 230, 'text': '25', 'size': 52}, {'ref': 'esp.D26', 'dx': 230, 'text': '26', 'size': 52},
        {'ref': 'esp.D14', 'dx': 230, 'text': '14', 'size': 52}, {'ref': 'esp.D27', 'dx': 230, 'text': '27', 'size': 52},
        {'ref': 'esp.D21', 'dx': -230, 'text': '21', 'size': 52}, {'ref': 'esp.D22', 'dx': -230, 'text': '22', 'size': 52},
        {'ref': 'mt.@t', 'dy': -110, 'text': 'MT3608 → 5.0 V → VIN', 'size': 50},
        {'ref': 'mF.@t', 'dy': -90, 'text': 'FRONT\nCW', 'size': 42}, {'ref': 'mR.@t', 'dy': -90, 'text': 'RIGHT\nCCW', 'size': 42},
        {'ref': 'mB.@t', 'dy': -90, 'text': 'BACK\nCW', 'size': 42}, {'ref': 'mL.@t', 'dy': -90, 'text': 'LEFT\nCCW', 'size': 42},
    ]))

for s in specs:
    with open(os.path.join(HERE, s['name'] + '.json'), 'w', encoding='utf-8') as f:
        json.dump(s, f, ensure_ascii=False, indent=2)
    print('wrote', s['name'] + '.json')
