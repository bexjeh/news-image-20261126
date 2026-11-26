#!/usr/bin/env python3
"""Render the 26 November 2026 world-news front page as entry.png.

A newspaper-style 1024x1024 image, drawn with Pillow from fixed text and
shapes only: no network, no timestamps, no randomness, so the output bytes
are identical on every run. Run: python3 build_overlay.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
NAVY = (16, 36, 62)
GOLD = (232, 184, 75)
RED = (163, 22, 33)
TEAL = (14, 92, 92)
AMBER = (146, 86, 0)
SLATE = (52, 68, 88)
CARD = (255, 255, 255)
MUTED = (70, 70, 70)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=6):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def headline(draw, x, y, text, fnt, max_w, fill=INK, leading=4):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def tag(draw, x, y, text, color):
    fnt = font(SANS_B, 16)
    w = draw.textlength(text, font=fnt) + 18
    draw.rounded_rectangle([x, y, x + w, y + 26], radius=4, fill=color)
    draw.text((x + 9, y + 4), text, font=fnt, fill=(255, 255, 255))
    return w


def card(draw, x, y, w, h):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6,
                           fill=CARD, outline=(200, 192, 172), width=2)


def bar_chart(draw, x, y, w, data, max_v=40):
    """data: list of (label, value, color). Horizontal bars with % labels."""
    fnt = font(SANS_B, 14)
    lab_f = font(SANS, 13)
    row_h = 26
    for i, (label, value, color) in enumerate(data):
        by = y + i * row_h
        draw.text((x, by + 2), label, font=lab_f, fill=INK)
        bx = x + 78
        bw = int((w - 78 - 52) * value / max_v)
        draw.rectangle([bx, by + 2, bx + max(bw, 4), by + 20], fill=color)
        draw.text((bx + max(bw, 4) + 6, by + 2), f"{value}%",
                  font=fnt, fill=INK)
    return y + len(data) * row_h


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    title = font(SERIF_B, 56)
    d.text((W // 2, 14), "THE WORLD IN ONE IMAGE", font=title,
           fill=(255, 255, 255), anchor="ma")
    date_f = font(SANS_B, 27)
    d.text((W // 2, 76), "THURSDAY  •  26 NOVEMBER 2026",
           font=date_f, fill=GOLD, anchor="ma")

    sub = font(SERIF, 17)
    d.text((W // 2, 130), "Tariffs, oil, remembrance, Thanksgiving, chess and space — the day in full",
           font=sub, fill=MUTED, anchor="ma")

    # ---- Row A: lead tariffs + oil --------------------------------------
    y0, rh = 158, 340
    # Lead card
    card(d, 16, y0, 620, rh)
    tag(d, 32, y0 + 12, "TRADE  •  LEAD STORY", RED)
    y = headline(d, 32, y0 + 48,
                 "TRUMP'S NEW TARIFF SALVO HITS 14 PARTNERS",
                 font(SERIF_B, 35), 588, fill=INK)
    y = para(d, 32, y + 6,
             "Taiwan says it will keep its agreed 15% US rate as Washington "
             "proposes duties of up to 40% to fight 'excess capacity'.",
             font(SANS, 18), 588, leading=5)
    d.text((32, y + 8), "CAPPED RATES PROPOSED (USTR):",
           font=font(SANS_B, 14), fill=MUTED)
    bar_chart(d, 32, y + 30, 588,
              [("China", 20, RED), ("Vietnam", 35, RED),
               ("India", 25, (196, 90, 20)), ("EU", 15, NAVY),
               ("Taiwan", 15, TEAL)], max_v=40)

    # Oil card
    card(d, 648, y0, 360, rh)
    tag(d, 664, y0 + 12, "OIL  •  GULF", AMBER)
    y = headline(d, 664, y0 + 48,
                 "HOUTHIS CLAIM STRIKE ON SAUDI REFINERY",
                 font(SERIF_B, 27), 328, fill=INK)
    para(d, 664, y + 6,
         "Riyadh says four drones were downed over Ras Tanura. Brent "
         "settles at $94.61 a barrel, up 3.5% on supply fears.",
         font(SANS, 18), 328, leading=5)
    # Big price + flame, fixed positions inside the card
    d.text((664, y0 + 240), "$94.61", font=font(SERIF_B, 52),
           fill=AMBER)
    d.text((664, y0 + 300), "BRENT CRUDE  •  +3.5% IN A DAY",
           font=font(SANS_B, 14), fill=MUTED)
    # simple flame
    fx, fy = 950, y0 + 240
    d.polygon([(fx, fy + 52), (fx - 26, fy + 96), (fx + 26, fy + 96)],
              fill=(226, 88, 34))
    d.polygon([(fx, fy + 18), (fx - 14, fy + 62), (fx + 14, fy + 62)],
              fill=(245, 176, 65))

    # ---- Row B: three panels --------------------------------------------
    y1, rh2 = 510, 232
    pw, gap = 322, 13
    xs = [16, 16 + pw + gap, 16 + 2 * (pw + gap)]

    # India
    card(d, xs[0], y1, pw, rh2)
    tag(d, xs[0] + 14, y1 + 12, "INDIA", RED)
    y = headline(d, xs[0] + 14, y1 + 48, "MUMBAI REMEMBERS 26/11",
                 font(SERIF_B, 25), pw - 28)
    para(d, xs[0] + 14, y + 6,
         "India marks 18 years since the Mumbai attacks and celebrates "
         "Constitution Day.",
         font(SANS, 17), pw - 28, leading=5)
    # candle, fixed near the card bottom
    cx = xs[0] + pw // 2
    cy = y1 + 188
    d.rectangle([cx - 8, cy + 10, cx + 8, cy + 34], fill=(240, 240, 230),
                outline=(150, 150, 150))
    d.ellipse([cx - 7, cy, cx + 7, cy + 12], fill=(245, 176, 65))

    # Thanksgiving
    card(d, xs[1], y1, pw, rh2)
    tag(d, xs[1] + 14, y1 + 12, "USA", TEAL)
    y = headline(d, xs[1] + 14, y1 + 48, "AMERICA GIVES THANKS",
                 font(SERIF_B, 25), pw - 28)
    para(d, xs[1] + 14, y + 6,
         "81.5m Americans travel for the holiday; the 100th Macy's parade "
         "steps off in New York.",
         font(SANS, 17), pw - 28, leading=5)
    # parade balloon: three circles, fixed near the card bottom
    bx = xs[1] + pw // 2
    by = y1 + 188
    d.ellipse([bx - 46, by + 6, bx - 6, by + 36], fill=(196, 60, 60))
    d.ellipse([bx - 20, by, bx + 20, by + 42], fill=(232, 184, 75))
    d.ellipse([bx + 6, by + 6, bx + 46, by + 36], fill=(60, 110, 180))

    # Chess
    card(d, xs[2], y1, pw, rh2)
    tag(d, xs[2] + 14, y1 + 12, "SPORT  •  CHESS", NAVY)
    y = headline(d, xs[2] + 14, y1 + 48, "GAME 3 TODAY IN GENEVA",
                 font(SERIF_B, 25), pw - 28)
    para(d, xs[2] + 14, y + 6,
         "Tied 1–1 after two draws; Game 3 today, Sindarov has White.",
         font(SANS, 17), pw - 28, leading=5)
    # mini chessboard 4x4, fixed near the card bottom
    bs, ox = 15, xs[2] + pw // 2 - 30
    oy = y1 + 172
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([ox + c * bs, oy + r * bs,
                             ox + (c + 1) * bs, oy + (r + 1) * bs],
                            fill=INK)

    # ---- Row C: space + Cairo -------------------------------------------
    y2, rh3 = 742, 164
    card(d, 16, y2, 492, rh3)
    tag(d, 30, y2 + 12, "SPACE", SLATE)
    y = headline(d, 30, y2 + 48, "HERA SHOWS ASTEROID'S SCAR",
                 font(SERIF_B, 25), 330)
    para(d, 30, y + 4,
         "ESA's first Hera images: DART left a stadium-sized crater on "
         "Dimorphos.",
         font(SANS, 17), 330, leading=5)
    # crater: grey circle with darker bowl
    d.ellipse([396, y2 + 46, 492, y2 + 142], fill=(148, 148, 148))
    d.ellipse([414, y2 + 62, 474, y2 + 122], fill=(88, 88, 88))
    d.ellipse([428, y2 + 76, 460, y2 + 108], fill=(52, 52, 52))

    card(d, 520, y2, 488, rh3)
    tag(d, 534, y2 + 12, "EGYPT", RED)
    y = headline(d, 534, y2 + 48, "CAIRO TANKER FIRE TOLL RISES TO 31",
                 font(SERIF_B, 25), 330)
    para(d, 534, y + 4,
         "A fuel tanker crash on the Ring Road set cars ablaze; 21 hurt.",
         font(SANS, 17), 330, leading=5)
    # flame bars, fixed near the card bottom
    for i, hgt in enumerate([34, 52, 40]):
        x = 920 + i * 26
        d.polygon([(x + 10, y2 + 140 - hgt), (x, y2 + 140),
                   (x + 20, y2 + 140)], fill=(226, 88, 34))

    # ---- Bottom strip: also today ---------------------------------------
    y3 = 918
    d.rectangle([0, y3, W, H], fill=NAVY)
    d.text((16, y3 + 8), "ALSO TODAY", font=font(SANS_B, 16), fill=GOLD)
    briefs_l = [
        "Bangladesh raises garment wage 36% after weeks of protests",
        "North Korea expels Swiss envoy; shuts Pyongyang office",
        "Solomons signs Australia treaty: no foreign bases",
    ]
    briefs_r = [
        "Shenzhou-24: first Pakistani astronaut boards Tiangong",
        "Flipkart CEO Krishnamurthy steps down after 11 years",
        "Duran Duran guitarist Andy Taylor dies at 65",
    ]
    bf = font(SANS, 15)
    for i, t in enumerate(briefs_l):
        d.text((16, y3 + 30 + i * 20), "•  " + t, font=bf,
               fill=(255, 255, 255))
    for i, t in enumerate(briefs_r):
        d.text((520, y3 + 30 + i * 20), "•  " + t, font=bf,
               fill=(255, 255, 255))
    d.text((W - 16, y3 + 8), "26 NOVEMBER 2026", font=font(SANS_B, 16),
           fill=GOLD, anchor="ra")

    img.save(OUT, format="PNG")
    print(f"wrote {OUT} {img.size} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
