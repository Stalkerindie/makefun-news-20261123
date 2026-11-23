#!/usr/bin/env python3
"""Build the newspaper-style entry picture for Monday 23 November 2026.

Takes the five-panel AI collage produced earlier and lays it out as a
front page: a masthead up top, four square-ish stories in a 2x2 grid,
one wide story along the bottom, and a small footer line. Every bit of
text on the page is drawn here with PIL, so the wording stays crisp
instead of coming out of the image generator.

Running this script twice over the same collage gives byte-identical
output: nothing here reads the clock, rolls dice, or touches the net.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
COLLAGE = ROOT / "assets" / "media-generation-news-20261123-collage-0-1f0454d1-fea3-467d-b644-163ec5437c1d.webp"
RESULT = ROOT / "assets" / "entry.jpg"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

PAGE_W, PAGE_H = 1024, 1024
EDGE = 24            # outer margin on the left and right
GUTTER = 24          # gap between the two columns
TILE_W, TILE_H = 476, 220
WIDE_W, WIDE_H = 976, 168
TEXT_GAP = 5         # space between a picture and its headline
ROW_STEP = TILE_H + 80 + 14   # picture + text block + gap to next row

PAPER = (246, 241, 230)
BLACK = (20, 20, 20)
CRIMSON = (178, 34, 34)
MUTED = (90, 90, 90)
FRAME_WIDTH = 2    # stroke of the picture frames and the masthead rule

# Each story: where its picture sits inside the 1920x1280 collage
# (a few pixels are trimmed off every side to dodge the white seams),
# plus the headline and one-line caption printed underneath it.
STORIES = [
    {
        "box": (6, 6, 954, 433),
        "title": "COP31 COLLAPSES — NO CLIMATE DEAL",
        "blurb": "Antalya: EU rejects a draft with no fossil fuels mentioned.",
    },
    {
        "box": (966, 6, 1914, 433),
        "title": "GULF WAR WIDENS — 25 TANKERS HIT",
        "blurb": "25 tankers hit near Hormuz; Houthis strike Riyadh again.",
    },
    {
        "box": (6, 452, 954, 863),
        "title": "RUSSIAN MISSILES LAND IN POLAND",
        "blurb": "NATO jets scramble; Warsaw calls it a deliberate provocation.",
    },
    {
        "box": (966, 452, 1914, 863),
        "title": "FACTORY FIRE — 50 MISSING IN JAVA",
        "blurb": "Banten candy plant: 3 dead, 7 body bags; search goes on.",
    },
    {
        "box": (6, 873, 1914, 1274),
        "title": "BEPICOLOMBO REACHES MERCURY",
        "blurb": "After 8 years, the ESA/JAXA craft enters orbit — but a thruster glitch cut its burn short.",
    },
]


def load_typefaces():
    """Return the five DejaVu faces this page needs, at their sizes."""
    def face(name, size):
        return ImageFont.truetype(str(FONT_DIR / name), size)

    return {
        "masthead": face("DejaVuSerif-Bold.ttf", 46),
        "kicker": face("DejaVuSans-Bold.ttf", 16),
        "title": face("DejaVuSans-Bold.ttf", 26),
        "blurb": face("DejaVuSans.ttf", 14),
        "footer": face("DejaVuSans.ttf", 15),
    }


def split_lines(pen, text, face, width):
    """Greedy word wrap: pack as many words per line as fit in `width`."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if pen.textlength(trial, font=face) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paint_masthead(pen, faces):
    """Date line, red kicker, and the rule underneath them."""
    pen.text((PAGE_W // 2, 12), "MONDAY 23 NOVEMBER 2026",
             font=faces["masthead"], fill=BLACK, anchor="ma")
    pen.text((PAGE_W // 2, 64), "—  THE WORLD IN ONE PICTURE  —",
             font=faces["kicker"], fill=CRIMSON, anchor="ma")
    pen.line([(EDGE, 92), (PAGE_W - EDGE, 92)], fill=BLACK, width=FRAME_WIDTH)


def paint_tile(pen, sheet, collage, story, left, top, faces, line_pitch):
    """One grid story: picture with a frame, then headline + caption."""
    picture = ImageOps.fit(
        collage.crop(story["box"]), (TILE_W, TILE_H), Image.LANCZOS)
    sheet.paste(picture, (left, top))
    pen.rectangle([left, top, left + TILE_W - 1, top + TILE_H - 1],
                  outline=BLACK, width=FRAME_WIDTH)

    text_top = top + TILE_H + TEXT_GAP
    title_lines = split_lines(pen, story["title"], faces["title"], TILE_W)
    if len(title_lines) > 2:
        raise ValueError(f"headline spills past two lines: {story['title']!r}")
    for offset, line in enumerate(title_lines):
        pen.text((left, text_top + offset * line_pitch),
                 line, font=faces["title"], fill=BLACK)

    # The caption always starts exactly two title-lines below the
    # headline, so a two-line headline can never touch it. With the
    # real line pitch (ascent + descent of the 26pt face = 32px) the
    # gap between a second-line descender and the caption is 4px.
    caption_lines = split_lines(pen, story["blurb"], faces["blurb"], TILE_W)
    if len(caption_lines) > 1:
        raise ValueError(f"caption spills past one line: {story['blurb']!r}")
    pen.text((left, text_top + 2 * line_pitch),
             caption_lines[0], font=faces["blurb"], fill=BLACK)


def build_page():
    """Compose the whole 1024x1024 page and return it."""
    collage = Image.open(COLLAGE).convert("RGB")
    sheet = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    pen = ImageDraw.Draw(sheet)
    faces = load_typefaces()

    # True line pitch of the 26pt bold face, measured from the font
    # itself rather than guessed: ascent plus descent.
    ascent, descent = faces["title"].getmetrics()
    line_pitch = ascent + descent

    paint_masthead(pen, faces)

    top_row = 100
    for index, story in enumerate(STORIES[:4]):
        column = index % 2
        row = index // 2
        left = EDGE + column * (TILE_W + GUTTER)
        top = top_row + row * ROW_STEP
        paint_tile(pen, sheet, collage, story, left, top, faces, line_pitch)

    wide_top = top_row + 2 * ROW_STEP
    wide = STORIES[4]
    picture = ImageOps.fit(
        collage.crop(wide["box"]), (WIDE_W, WIDE_H), Image.LANCZOS)
    sheet.paste(picture, (EDGE, wide_top))
    pen.rectangle([EDGE, wide_top, EDGE + WIDE_W - 1, wide_top + WIDE_H - 1],
                  outline=BLACK, width=FRAME_WIDTH)
    pen.text((EDGE, wide_top + WIDE_H + 6),
             wide["title"], font=faces["title"], fill=BLACK)
    pen.text((EDGE, wide_top + WIDE_H + 6 + 30),
             wide["blurb"], font=faces["blurb"], fill=BLACK)

    pen.text((PAGE_W // 2, 992),
             "Five stories from Monday 23 November 2026  ·  Antalya  ·  Hormuz  ·  Poland  ·  Indonesia  ·  Mercury",
             font=faces["footer"], fill=MUTED, anchor="ma")
    return sheet


def main():
    page = build_page()
    page.save(RESULT, "JPEG", quality=88, optimize=True)
    print("wrote", RESULT)


if __name__ == "__main__":
    main()
