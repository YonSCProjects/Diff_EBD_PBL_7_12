# build_card_heroes.py — the "final product" hero at the top of each project's first task card.
#
#   python Arduino_Projects/_posters/build_card_heroes.py
#
# Writes Arduino_Projects/<project>/task_cards_he/assets/hero_final_product.jpg for projects 1-9.
#
# Source per project:
#   - Yon's chosen poster art (2026-09-27: P1, P3-P7 from src_bright/, P8 from src/), cropped
#     to a 16:9 band around the product. YC is the product's vertical centre in the 3:4 frame.
#   - src_hero/ for the two projects whose poster could not serve: P2's poster shows a large
#     arcade button, but the real game uses a small 4-leg tactile button; P9 has no poster.
#     Both were generated 2026-10-15 in the posters' style with the project's real parts.
#
# The images carry no text, so they are reused verbatim in print and on the site.
# Each also gets a small hero_final_product_thumb.jpg for the site's home-page tiles.
# Files are only rewritten when their bytes change, so a re-run never churns git.
import io
from pathlib import Path
from PIL import Image


def save_if_changed(im, path, **kw):
    buf = io.BytesIO()
    im.save(buf, format='JPEG', **kw)
    data = buf.getvalue()
    if path.exists() and path.read_bytes() == data:
        return False
    path.write_bytes(data)
    return True

HERE = Path(__file__).resolve().parent
PROJECTS = HERE.parent

POSTER = {1: 'src_bright', 3: 'src_bright', 4: 'src_bright', 5: 'src_bright',
          6: 'src_bright', 7: 'src_bright', 8: 'src'}
YC = {1: 0.50, 3: 0.42, 4: 0.505, 5: 0.525, 6: 0.62, 7: 0.55, 8: 0.37}
GENERATED = {2: 'src_hero', 9: 'src_hero'}

for n in range(1, 10):
    dirs = sorted(PROJECTS.glob(f'Project_{n}_*'))
    if not dirs:
        print(f'  P{n}: no project folder - skipped'); continue
    out = dirs[0] / 'task_cards_he' / 'assets' / 'hero_final_product.jpg'
    out.parent.mkdir(parents=True, exist_ok=True)
    if n in GENERATED:
        im = Image.open(HERE / GENERATED[n] / f'p{n}.png').convert('RGB')
    else:
        im = Image.open(HERE / POSTER[n] / f'p{n}.png').convert('RGB')
        W, H = im.size
        h = round(W * 9 / 16)
        y0 = min(max(0, round(YC[n] * H - h / 2)), H - h)
        im = im.crop((0, y0, W, y0 + h))
    wrote = save_if_changed(im, out, quality=86, optimize=True, progressive=True)
    thumb = out.with_name('hero_final_product_thumb.jpg')
    t = im.resize((640, 360), Image.LANCZOS)
    wrote_t = save_if_changed(t, thumb, quality=80, optimize=True, progressive=True)
    print(f'  P{n}: {out.relative_to(PROJECTS)}  {im.size[0]}x{im.size[1]}  {out.stat().st_size // 1024} KB'
          f'{"" if wrote else " (unchanged)"}  + thumb {thumb.stat().st_size // 1024} KB{"" if wrote_t else " (unchanged)"}')
