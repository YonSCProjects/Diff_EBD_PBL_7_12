"""smoke_p8.py — render the P8 parts on their own, to check a part before a scene uses it.

Run: python smoke_p8.py   then   node shot.js smoke_p8_a.svg out.png 700
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iso import Scene, render, tag
import parts_p8 as P

HERE = os.path.dirname(os.path.abspath(__file__))

sc = Scene()
P.bench(sc)
P.drone(sc, front_mark=True)
tag(sc, (P.CTR_X, P.CTR_Y, P.Z_DECK + 8), 'assembled, no props', dy=-72, size=7)
render(sc, os.path.join(HERE, 'smoke_p8_a.svg'))

sc = Scene()
P.bench(sc, 44, 16, 215, 195)
P.drone(sc, props=True, front_mark=True)
render(sc, os.path.join(HERE, 'smoke_p8_b.svg'))

sc = Scene()
P.bench(sc, 100, 70, 105, 90)
P.mosfet_board(sc, x=118, y=88, z=-18, pads=True)
render(sc, os.path.join(HERE, 'smoke_p8_c.svg'))
print('wrote 3')
