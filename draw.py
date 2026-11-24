#!/usr/bin/env python3
"""Draw the news-image-20261124 entry: a one-page newspaper-style
infographic summing up Tuesday 24 November 2026. Every fact was checked
against reporting of 24 Nov 2026 (Reuters / CNN / BBC / AP / WSJ /
Le Monde / The Times): COP31's collapse and its fallout, Ukraine's
Benghazi strike as confirmed on Monday, the Saryu-Kamala Express
flag-off, the Lisbon cost-of-living march, Pant's 128 in Wellington,
Seoul's education minister resigning over AI cheating, and Iran's
power rationing. Output: entry.png, 1024x1024, deterministic."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (22, 50, 79)
RED = (179, 38, 30)
GREY = (90, 88, 82)
ORANGE = (214, 106, 24)
GREEN = (46, 125, 50)
YELLOW = (240, 200, 60)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_w):
    """Largest size at or below `size` that fits `text` in `max_w`."""
    while size > 10:
        fnt = load(path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return load(path, size)


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def box(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def kicker(d, x, y, text):
    d.text((x, y), text, font=load(FB, 18), fill=RED)


def headline(d, x, y, text, max_w, size=24):
    fnt = fit(d, text, FB, size, max_w)
    return para(d, x, y, text, fnt, INK, max_w, size + 6)


# ---- icons: small flat pictograms, drawn in code ----

def icon_globe(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], outline=NAVY, width=5)
    d.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=NAVY, width=3)
    d.line([x, y + s * 0.5, x + s, y + s * 0.5], fill=NAVY, width=3)
    d.arc([x - s * 0.25, y + s * 0.18, x + s * 1.25, y + s * 0.82],
          300, 60, fill=NAVY, width=3)
    d.line([x - 6, y + s + 6, x + s + 6, y - 6], fill=RED, width=7)


def icon_warship(d, x, y, s):
    d.polygon([(x, y + s * 0.55), (x + s, y + s * 0.55),
               (x + s * 0.88, y + s * 0.88), (x + s * 0.12, y + s * 0.88)],
              fill=NAVY)
    d.rectangle([x + s * 0.30, y + s * 0.32, x + s * 0.62, y + s * 0.55],
                fill=NAVY)
    d.line([x + s * 0.46, y + s * 0.32, x + s * 0.46, y + s * 0.10],
           fill=NAVY, width=4)
    d.polygon([(x + s * 0.68, y + s * 0.34), (x + s * 0.80, y + s * 0.10),
               (x + s * 0.92, y + s * 0.34)], fill=ORANGE)
    d.polygon([(x + s * 0.74, y + s * 0.30), (x + s * 0.82, y + s * 0.16),
               (x + s * 0.88, y + s * 0.30)], fill=RED)
    for cx, cy, r in [(0.18, 0.22, 7), (0.28, 0.12, 5)]:
        d.ellipse([x + s * cx - r, y + s * cy - r,
                   x + s * cx + r, y + s * cy + r], fill=(150, 148, 140))
    d.line([x, y + s * 0.96, x + s, y + s * 0.96], fill=NAVY, width=3)


def icon_train(d, x, y, s):
    d.rectangle([x + s * 0.08, y + s * 0.18, x + s * 0.92, y + s * 0.72],
                fill=NAVY)
    d.rectangle([x + s * 0.08, y + s * 0.18, x + s * 0.92, y + s * 0.30],
                fill=RED)
    for i in range(3):
        wx = x + s * (0.18 + i * 0.26)
        d.rectangle([wx, y + s * 0.38, wx + s * 0.16, y + s * 0.56],
                    fill=(255, 255, 255))
    for cx in (0.28, 0.72):
        d.ellipse([x + s * cx - 7, y + s * 0.72 - 7,
                   x + s * cx + 7, y + s * 0.72 + 7], fill=INK)
    d.line([x, y + s * 0.92, x + s, y + s * 0.92], fill=INK, width=4)


def icon_march(d, x, y, s):
    for cx, col in [(0.24, NAVY), (0.50, RED), (0.76, NAVY)]:
        d.ellipse([x + s * cx - 8, y + s * 0.12, x + s * cx + 8,
                   y + s * 0.12 + 16], fill=col)
        d.polygon([(x + s * cx - 13, y + s * 0.86), (x + s * cx + 13, y + s * 0.86),
                   (x + s * cx + 8, y + s * 0.34), (x + s * cx - 8, y + s * 0.34)],
                  fill=col)
    d.line([x + s * 0.50, y + s * 0.34, x + s * 0.50, y - s * 0.06],
           fill=INK, width=3)
    d.rectangle([x + s * 0.52, y - s * 0.06, x + s * 0.98, y + s * 0.22],
                fill=ORANGE)


def icon_cricket(d, x, y, s):
    d.polygon([(x + s * 0.30, y + s * 0.05), (x + s * 0.44, y + s * 0.02),
               (x + s * 0.62, y + s * 0.55), (x + s * 0.50, y + s * 0.60)],
              fill=(150, 110, 60))
    d.polygon([(x + s * 0.50, y + s * 0.60), (x + s * 0.62, y + s * 0.55),
               (x + s * 0.78, y + s * 0.92), (x + s * 0.66, y + s * 0.96)],
              fill=NAVY)
    d.ellipse([x + s * 0.12, y + s * 0.62, x + s * 0.12 + 20,
               y + s * 0.62 + 20], fill=RED)
    for i in range(3):
        lx = x + s * (0.82 + i * 0.07)
        d.line([lx, y + s * 0.55, lx, y + s * 0.95], fill=INK, width=3)


def icon_cap(d, x, y, s):
    d.polygon([(x + s * 0.50, y + s * 0.10), (x + s * 0.96, y + s * 0.34),
               (x + s * 0.50, y + s * 0.58), (x + s * 0.04, y + s * 0.34)],
              fill=NAVY)
    d.rectangle([x + s * 0.32, y + s * 0.48, x + s * 0.68, y + s * 0.72],
                fill=NAVY)
    d.line([x + s * 0.90, y + s * 0.36, x + s * 0.90, y + s * 0.80],
           fill=ORANGE, width=4)
    d.ellipse([x + s * 0.90 - 6, y + s * 0.80 - 6,
               x + s * 0.90 + 6, y + s * 0.80 + 6], fill=ORANGE)


def icon_bulb(d, x, y, s):
    d.ellipse([x + s * 0.22, y + s * 0.06, x + s * 0.78, y + s * 0.62],
              outline=NAVY, width=4)
    d.rectangle([x + s * 0.40, y + s * 0.62, x + s * 0.60, y + s * 0.82],
                fill=NAVY)
    d.line([x + s * 0.12, y + s * 0.88, x + s * 0.88, y], fill=RED, width=6)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top bar, masthead, date
    d.rectangle([0, 0, W, 10], fill=RED)
    mast = load(FSB, 66)
    d.text(((W - d.textlength("THE WORLD TODAY", font=mast)) / 2, 28),
           "THE WORLD TODAY", font=mast, fill=INK)
    date = load(FB, 32)
    d.text(((W - d.textlength("TUESDAY  24  NOVEMBER  2026", font=date)) / 2, 112),
           "TUESDAY  24  NOVEMBER  2026", font=date, fill=RED)
    d.line([28, 162, W - 28, 162], fill=INK, width=3)
    d.line([28, 168, W - 28, 168], fill=INK, width=1)

    # lead story: COP31 fallout
    lx, ly, lw, lh = 28, 184, 968, 176
    box(d, lx, ly, lw, lh)
    icon_globe(d, lx + 20, ly + 42, 92)
    tx = lx + 132
    d.text((tx, ly + 14), "CLIMATE  ·  ANTALYA, TURKEY", font=load(FB, 19), fill=RED)
    head = fit(d, "COP31 is dead — and the blame begins", FSB, 40, lw - 152)
    d.text((tx, ly + 42), "COP31 is dead — and the blame begins",
           font=head, fill=INK)
    para(d, tx, ly + 96,
         "The UN climate talks collapsed on Sunday with no deal — the first "
         "COP to fail since Copenhagen in 2009. A day on, the verdicts are "
         "brutal: “the worst COP ever”. More than 190 nations, and a final "
         "draft that never once mentioned fossil fuels.",
         load(FR, 19), INK, lw - 152, 24)

    # story rows: kicker, headline across the full box width, icon tucked
    # into the kicker's top-right corner, body full width below.
    rows = [
        (376, [
            ("LIBYA  ·  BENGHAZI", icon_warship,
             "Ukraine sinks a Russian warship off Libya",
             "Sea drones sank the corvette Merkury at Benghazi on Sunday, "
             "2,400 km from the front; Kyiv confirmed it Monday with video. "
             "Satellite images show it submerged; MV Angara was also hit."),
            ("INDIA  ·  NEPAL", icon_train,
             "A new train links Ayodhya and Janakpur",
             "Modi and Nepal's PM Balendra Shah flag off the "
             "Saryu-Kamala Express, a cross-border line joining the "
             "temple towns of Ayodhya and Janakpur Dham."),
            ("PORTUGAL  ·  LISBON", icon_march,
             "Thousands march over the cost of living",
             "Crowds fill Lisbon's streets to protest rising prices, "
             "as living costs bite across Europe."),
        ]),
        (616, [
            ("SPORT  ·  WELLINGTON", icon_cricket,
             "Pant's 128 puts India on top in Wellington",
             "Rishabh Pant's 128, a record for an Asian wicketkeeper, "
             "powers India in the first Test against New Zealand."),
            ("TECHNOLOGY  ·  SEOUL", icon_cap,
             "Seoul minister quits over AI cheating row",
             "South Korea's education minister steps down amid a row "
             "over AI cheating rules in exams."),
            ("MIDDLE EAST  ·  TEHRAN", icon_bulb,
             "Iran rations power as winter closes in",
             "Daily power cuts are announced amid fuel shortages; the "
             "president switches off office lights to urge citizens "
             "to save energy."),
        ]),
    ]
    bw, bh, gap = 304, 224, 28
    for y0, cells in rows:
        for i, (kick, icon, head_text, body) in enumerate(cells):
            x0 = 28 + i * (bw + gap)
            box(d, x0, y0, bw, bh)
            kicker(d, x0 + 14, y0 + 12, kick)
            icon(d, x0 + bw - 56, y0 + 8, 40)
            hy = headline(d, x0 + 14, y0 + 52, head_text, bw - 28, 22)
            para(d, x0 + 14, hy + 6, body, load(FR, 16), INK, bw - 28, 18)

    # footer strip
    fx, fy, fw, fh = 28, 856, 968, 118
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=NAVY)
    d.text((fx + 18, fy + 12), "THE DAY, AS REPORTED", font=load(FB, 20),
           fill=YELLOW)
    para(d, fx + 18, fy + 44,
         "Events of 22–24 Nov 2026, as reported on 24 Nov. "
         "Sources: Reuters, CNN, BBC, AP, WSJ.",
         load(FR, 18), (255, 255, 255), fw - 36, 23)
    d.text((fx + 18, fy + 88), "One image. One day. The world.",
           font=load(FB, 17), fill=YELLOW)

    d.line([28, 992, W - 28, 992], fill=GREY, width=1)
    d.text((28, 998), "THE WORLD TODAY — 24 NOVEMBER 2026",
           font=load(FR, 13), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
