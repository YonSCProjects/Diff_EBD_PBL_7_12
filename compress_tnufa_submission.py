# Portal-friendly compressed twin of the final Tnufa submission PDF (the card
# pages carry heavy vector ink-outline figures; rasterizing is the only real
# lever). The vector original stays untouched as the print/archive copy.
import pymupdf

BASE = r"C:\Users\Yon\Documents\Diferential pbl for BE\build_output"
SRC = BASE + "\\הצעת_יוזמה_תנופה_תשפז_סדנת_ארדואינו_עם_נספח_הכרטיסיות.pdf"
DST = BASE + "\\הצעת_יוזמה_תנופה_תשפז_סדנת_ארדואינו_עם_נספח_הכרטיסיות.compressed.pdf"
DPI = 130
JPG_Q = 72

src = pymupdf.open(SRC)
out = pymupdf.open()
relinked = 0
for i, page in enumerate(src):
    pix = page.get_pixmap(dpi=DPI, colorspace=pymupdf.csRGB)
    img = pix.tobytes("jpeg", jpg_quality=JPG_Q)
    p = out.new_page(width=page.rect.width, height=page.rect.height)
    p.insert_image(page.rect, stream=img)
    # rasterizing drops annotations - copy the clickable URL links back
    for link in page.get_links():
        if link.get("kind") == pymupdf.LINK_URI:
            p.insert_link(link)
            relinked += 1
    if (i + 1) % 50 == 0:
        print(f"  {i + 1}/{len(src)} pages")
out.save(DST, garbage=4, deflate=True)
print(f"done: {len(src)} pages, {relinked} links restored -> {DST}")
