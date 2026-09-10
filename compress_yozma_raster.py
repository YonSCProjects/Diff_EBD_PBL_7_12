# Produces a portal-friendly compressed twin of the full Tnufa proposal PDF by
# rasterizing each page at print-adequate resolution (the source pages carry
# enormous vector ink-outline figures that no stream compression can tame).
# The vector original stays untouched as the archive/quality copy.
import pymupdf

SRC = r"C:\Users\Yon\Documents\Diferential pbl for BE\build_output\Arduino_Yozma_Tnufa_he.pdf"
DST = r"C:\Users\Yon\Documents\Diferential pbl for BE\build_output\Arduino_Yozma_Tnufa_he.compressed.pdf"
DPI = 130
JPG_Q = 72

src = pymupdf.open(SRC)
out = pymupdf.open()
for i, page in enumerate(src):
    pix = page.get_pixmap(dpi=DPI, colorspace=pymupdf.csRGB)
    img = pix.tobytes("jpeg", jpg_quality=JPG_Q)
    p = out.new_page(width=page.rect.width, height=page.rect.height)
    p.insert_image(page.rect, stream=img)
    if (i + 1) % 50 == 0:
        print(f"  {i + 1}/{len(src)} pages")
out.save(DST, garbage=4, deflate=True)
print(f"done: {len(src)} pages -> {DST}")
