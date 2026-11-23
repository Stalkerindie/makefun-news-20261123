#!/usr/bin/env python3
"""Compose the final 1024x1024 entry from the generated 5-panel collage.

Adds a newspaper masthead naming the day and legible PIL-rendered
headlines + captions under each panel (no text comes from the image
generator). Deterministic: same input -> same output bytes.
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps

SRC = "assets/media-generation-news-20261123-collage-0-1f0454d1-fea3-467d-b644-163ec5437c1d.webp"
OUT = "assets/entry.jpg"

# Panel crops in the 1920x1280 collage (small insets avoid the white gutters).
PANELS = [
    ((6, 6, 954, 433), "COP31 COLLAPSES — NO CLIMATE DEAL",
     "Antalya: EU rejects a draft with no fossil fuels mentioned."),
    ((966, 6, 1914, 433), "GULF WAR WIDENS — 25 TANKERS HIT",
     "25 tankers hit near Hormuz; Houthis strike Riyadh again."),
    ((6, 452, 954, 863), "RUSSIAN MISSILES LAND IN POLAND",
     "NATO jets scramble; Warsaw calls it a deliberate provocation."),
    ((966, 452, 1914, 863), "FACTORY FIRE — 50 MISSING IN JAVA",
     "Banten candy plant: 3 dead, 7 body bags; search goes on."),
    ((6, 873, 1914, 1274), "BEPICOLOMBO REACHES MERCURY",
     "After 8 years, the ESA/JAXA craft enters orbit — but a thruster glitch cut its burn short."),
]

W = H = 1024
CREAM = (246, 241, 230)
INK = (20, 20, 20)
RED = (178, 34, 34)
GREY = (90, 90, 90)

src = Image.open(SRC).convert("RGB")
canvas = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(canvas)

serif_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 46)
sans_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
head_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
cap = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
foot = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)


def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# Masthead
d.text((512, 12), "MONDAY 23 NOVEMBER 2026", font=serif_b, fill=INK, anchor="ma")
d.text((512, 64), "—  THE WORLD IN ONE PICTURE  —", font=sans_b, fill=RED, anchor="ma")
d.line([(24, 92), (1000, 92)], fill=INK, width=2)

# Layout: two rows of two panels (476 x 220 + headline/caption block),
# then one wide panel (976 x 168 + headline/caption), then footer.
PW, PH = 476, 220
y = 100
for i, (crop, headline, caption) in enumerate(PANELS[:4]):
    col, row = i % 2, i // 2
    x = 24 + col * (PW + 24)
    yy = y + row * (PH + 80 + 14)
    panel = ImageOps.fit(src.crop(crop), (PW, PH), Image.LANCZOS)
    canvas.paste(panel, (x, yy))
    d.rectangle([x, yy, x + PW - 1, yy + PH - 1], outline=INK, width=2)
    hl = wrap(headline, head_b, PW)
    assert len(hl) <= 2, (headline, hl)
    for j, line in enumerate(hl):
        d.text((x, yy + PH + 5 + j * 29), line, font=head_b, fill=INK)
    cl = wrap(caption, cap, PW)
    assert len(cl) <= 1, (caption, cl)
    d.text((x, yy + PH + 5 + 2 * 29), cl[0], font=cap, fill=INK)

y2 = y + 2 * (PH + 80 + 14)  # 100 + 628 = 728
panel = ImageOps.fit(src.crop(PANELS[4][0]), (976, 168), Image.LANCZOS)
canvas.paste(panel, (24, y2))
d.rectangle([24, y2, 999, y2 + 167], outline=INK, width=2)
d.text((24, y2 + 174), PANELS[4][1], font=head_b, fill=INK)
d.text((24, y2 + 174 + 30), PANELS[4][2], font=cap, fill=INK)
d.text((512, 992),
       "Five stories from Monday 23 November 2026  ·  Antalya  ·  Hormuz  ·  Poland  ·  Indonesia  ·  Mercury",
       font=foot, fill=GREY, anchor="ma")

canvas.save(OUT, "JPEG", quality=88, optimize=True)
print("wrote", OUT)
