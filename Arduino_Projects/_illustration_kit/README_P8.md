# Project 8 illustrations — where this got to

`parts_p8.py` is the quadcopter's parts library; `scenes_p8.py` does not exist yet.
That is the next thing to write: 28 scenes, one per P8 task card.

## What is already done
- `iso.py` grew the vertical-axis primitives a quadcopter needs, which the car never did:
  `cyl_z`, `disc`, `ring_z`, `prism` (extrude any xy outline, winding normalised),
  `blade` (a real swept-and-twisted prop blade) and `spin_arc`.
- `parts_p8.py` — frame, grommets, 8520 motors, 65 mm props, DevKit, MT3608, GY-521,
  MOSFET perfboard, LiPo, O-rings, plus the bench/tool/room props each card needs.
  Verified by eye through `smoke_p8.py`.
- `p8_facts_and_briefs.json` — the authority for the scenes. Produced by an 11-agent pass over
  `Arduino_Project_8.md`, the `.ino` files and all 28 Hebrew cards. It holds:
  `facts.geometry / pins / rotation / powerTree / mosfetChannel / warnings`, and per card
  `action`, `objects`, `callouts` (Hebrew, house style) and `mustBeCorrect`.
  Read it before writing a scene — it catches things the brief alone does not.

## Facts the drawings must honour (these corrected earlier guesses)
- Opposite arms spin the SAME way: FRONT+BACK = CW, RIGHT+LEFT = CCW. Plus-style, one arm forward.
- CW motors ship with RED(+)/BLUE(-) leads, CCW motors with WHITE(+)/BLACK(-).
- Gate wires: 25 yellow FRONT/G1, 26 orange RIGHT/G2, 14 green BACK/G3, 27 blue LEFT/G4.
  I2C: 21 white SDA, 22 grey SCL. (The older Fritzing figures draw I2C blue/yellow — the brief wins.)
- The MOSFET board hangs UNDER the bottom plate, solder side to the carbon, components facing down,
  M1 pad nearest the FRONT arm. The LiPo sits below it, held only by the two frame O-rings.
- The DevKit's micro-USB faces the BACK arm. The MPU6050's silk-screen X arrow points at the FRONT motor.
- TO-220s lie FLAT with their tabs heat-shrunk; the tab is the Drain and the carbon plate conducts.
- One 220 uF bulk cap per board, not per channel. Flyback is a 1N5819, band toward BAT+.
- Props go on at the very last step. Every practice flight is tethered. No prop guards exist yet.

## How to build
    python build.py 8          # once scenes_p8.py exists
    python smoke_p8.py         # part-level check
    node shot.js <in.svg> <out.png> [widthPx]
