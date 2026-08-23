"""onwhite.py — flatten a transparent render onto white, for eyeballing.
Usage: python _blender/onwhite.py in.png out.png
"""
import sys
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGBA')
bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
Image.alpha_composite(bg, im).convert('RGB').save(dst)
print('wrote', dst)
