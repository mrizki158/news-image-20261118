#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: one page summing up the world news of
Wednesday 18 November 2026, as reported that day.

Every story was cross-checked against at least two independent reports dated
18 November 2026 (Reuters via Just Security's Early Edition, AP/AFP-based
briefings, PAHO reporting, NASA JPL via Zark News, Indonesian national press).
Flat-design infographic: drawn icons + short labels, so all text stays crisp.
Layout is zone-based: every tile has a text column and an illustration column,
and text is placed dynamically from measured wrap counts.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (26, 26, 32)
GRAY = (84, 84, 92)
CARD = (255, 255, 255)
RED = (178, 34, 34)

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
DB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
WARNINGS = []


def wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = f"{cur} {w_}".strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block(xy, text, fnt, fill, max_w, leading=1.14):
    """Draw wrapped text; return the y just below it."""
    x, y = xy
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def star(cx, cy, r_out, r_in, points, fill, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


MX = 36
CW = W - 2 * MX


def card(x, y, w, h, accent):
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD, outline=(214, 208, 194), width=2)
    d.rounded_rectangle([x, y, x + w, y + 13], radius=6, fill=accent)
    d.rectangle([x, y + 6, x + w, y + 13], fill=accent)


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 10], fill=RED)
d.text((MX, 24), "T H E   W O R L D   I N   O N E   D A Y", font=font(FB, 24), fill=RED)
d.text((W - MX, 27), "AS REPORTED ON THE DAY", font=font(FR, 16), fill=GRAY, anchor="ra")
date_text = "Wednesday 18 November 2026"
size = 62
while d.textlength(date_text, font=font(FB, size)) > CW and size > 30:
    size -= 2
d.text((MX - 2, 50), date_text, font=font(FB, size), fill=INK)
d.line([MX, 128, W - MX, 128], fill=INK, width=4)
d.line([MX, 135, W - MX, 135], fill=INK, width=1)

# ---------------------------------------------------------------- lead: Gulf
LY, LH = 148, 224
card(MX, LY, CW, LH, RED)
d.text((MX + 22, LY + 24), "MIDDLE EAST  ·  LEAD STORY", font=font(FB, 19), fill=RED)
hy = block((MX + 22, LY + 50), "US strikes Iran missile site; Iran hits back across the Gulf", font(FB, 35), INK, 545)
block(
    (MX + 22, hy + 8),
    "US jets bombed a Guards missile site on Qeshm Island, at the Strait of Hormuz. "
    "Iran answered with drones on a US base in Kuwait and attacks on Bahrain.",
    font(FR, 20), GRAY, 545,
)
ix0, iy0, ix1, iy1 = MX + 592, LY + 26, MX + CW - 18, LY + LH - 18
d.rounded_rectangle([ix0, iy0, ix1, iy1], radius=8, fill=(24, 42, 74))
d.rectangle([ix0, iy0 + 112, ix1, iy1 - 26], fill=(38, 84, 124))
d.polygon([(ix0 + 55, iy0 + 112), (ix0 + 125, iy0 + 84), (ix0 + 210, iy0 + 100), (ix0 + 245, iy0 + 112)], fill=(214, 186, 130))
star(ix0 + 143, iy0 + 88, 25, 10, 8, (255, 140, 40))
star(ix0 + 143, iy0 + 88, 12, 5, 8, (255, 214, 90))
dx, dy = ix0 + 232, iy0 + 40
d.line([dx - 25, dy - 11, dx + 25, dy + 11], fill=(230, 230, 230), width=4)
d.line([dx - 25, dy + 11, dx + 25, dy - 11], fill=(230, 230, 230), width=4)
for ox, oy in [(-25, -11), (25, 11), (-25, 11), (25, -11)]:
    d.ellipse([dx + ox - 7, dy + oy - 7, dx + ox + 7, dy + oy + 7], outline=(230, 230, 230), width=3)
d.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=(230, 230, 230))
d.line([dx - 4, dy + 8, ix0 + 158, iy0 + 80], fill=(255, 170, 60), width=3)
d.rectangle([ix0, iy1 - 26, ix1, iy1], fill=(24, 42, 74))
d.text((ix0 + 12, iy1 - 22), "QESHM ISLAND · STRAIT OF HORMUZ", font=font(FB, 14), fill=(235, 240, 245))

# ---------------------------------------------------------------- half tiles
HW = (CW - 16) // 2
TH = 184
TEXT_W = HW - 176  # text column; right 140px is the illustration column


def half_tile(x, y, accent, label, headline, caption):
    card(x, y, HW, TH, accent)
    d.text((x + 20, y + 24), label, font=font(FB, 17), fill=accent)
    hy = block((x + 20, y + 48), headline, font(FB, 26), INK, TEXT_W)
    cy = block((x + 20, hy + 7), caption, font(FR, 19), GRAY, TEXT_W)
    if cy > y + TH - 6:
        WARNINGS.append(f"tile overflow: {label} ends {cy}, tile ends {y + TH}")
    return (x + HW - 156, y + 26, x + HW - 16, y + TH - 14)  # illustration box


# Row 1: APEC | Crimea Bridge
RY1 = 388
box = half_tile(
    MX, RY1, (196, 30, 58), "ASIA-PACIFIC · APEC",
    "Xi and Putin open APEC in Shenzhen",
    "China and Russia vow to fight protectionism, a day before a three-way summit with Trump.",
)
fx, fy = box[0] + 8, box[1] + 10
for i, kind in enumerate(["cn", "ru", "us"]):
    y0 = fy + i * 48
    d.line([fx, y0 + 38, fx, y0], fill=(130, 130, 130), width=3)
    d.rectangle([fx + 3, y0, fx + 79, y0 + 38], outline=(150, 150, 150), fill=(255, 255, 255))
    if kind == "cn":
        d.rectangle([fx + 3, y0, fx + 79, y0 + 38], fill=(222, 41, 57))
        star(fx + 17, y0 + 13, 8, 3.2, 5, (255, 222, 0))
        for oy in (6, 15, 24):
            d.ellipse([fx + 30, y0 + oy, fx + 35, y0 + oy + 5], fill=(255, 222, 0))
    elif kind == "ru":
        d.rectangle([fx + 3, y0 + 13, fx + 79, y0 + 25], fill=(0, 57, 166))
        d.rectangle([fx + 3, y0 + 25, fx + 79, y0 + 38], fill=(213, 0, 50))
    else:
        for s in range(5):
            d.rectangle([fx + 3, y0 + 4 + s * 7, fx + 79, y0 + 7 + s * 7], fill=(178, 34, 52))
        d.rectangle([fx + 3, y0, fx + 38, y0 + 19], fill=(60, 59, 110))
        for r_ in range(3):
            for c_ in range(4):
                d.ellipse([fx + 7 + c_ * 8, y0 + 3 + r_ * 6, fx + 10 + c_ * 8, y0 + 6 + r_ * 6], fill=(255, 255, 255))

box = half_tile(
    MX + HW + 16, RY1, (38, 84, 124), "EUROPE · UKRAINE WAR",
    "Ukraine breaks the Crimea Bridge",
    "Kyiv's strike partially collapses a Kerch Bridge road span; Putin still refuses serious peace talks.",
)
bx, by = box[0] + 2, box[1] + 52
d.rectangle([bx, by, bx + 138, by + 64], fill=(214, 232, 242))
d.line([bx + 4, by + 24, bx + 52, by + 24], fill=(90, 90, 90), width=6)
d.line([bx + 86, by + 24, bx + 134, by + 24], fill=(90, 90, 90), width=6)
d.line([bx + 52, by + 24, bx + 66, by + 44], fill=(90, 90, 90), width=6)
d.line([bx + 66, by + 44, bx + 86, by + 24], fill=(90, 90, 90), width=6)
d.rectangle([bx + 16, by + 24, bx + 24, by + 56], fill=(90, 90, 90))
d.rectangle([bx + 114, by + 24, bx + 122, by + 56], fill=(90, 90, 90))
star(bx + 69, by + 16, 17, 7, 8, (255, 140, 40))
d.text((bx + 6, by + 70), "KERCH BRIDGE", font=font(FB, 13), fill=GRAY)

# Row 2: Senate | Measles
RY2 = 588
box = half_tile(
    MX, RY2, (40, 64, 128), "AMERICAS · US POLITICS",
    "Democrats take the US Senate",
    "Mary Peltola's Alaska win gives Democrats their largest Senate majority since 2009.",
)
sx, sy = box[0] + 6, box[1] + 14
d.text((sx + 4, sy), "56–44", font=font(DB, 44), fill=(40, 64, 128))
cx0, cy0 = sx + 8, sy + 66
d.rectangle([cx0, cy0 + 40, cx0 + 118, cy0 + 47], fill=(40, 64, 128))
for i in range(5):
    d.rectangle([cx0 + 7 + i * 23, cy0 + 24, cx0 + 14 + i * 23, cy0 + 40], fill=(40, 64, 128))
d.rectangle([cx0 + 3, cy0 + 18, cx0 + 115, cy0 + 24], fill=(40, 64, 128))
d.pieslice([cx0 + 30, cy0 - 14, cx0 + 88, cy0 + 22], start=180, end=360, fill=(40, 64, 128))
d.rectangle([cx0 + 56, cy0 - 22, cx0 + 62, cy0 - 10], fill=(40, 64, 128))
d.text((sx + 2, sy + 122), "SENATE MAJORITY", font=font(FB, 13), fill=GRAY)

box = half_tile(
    MX + HW + 16, RY2, RED, "HEALTH · UNITED STATES",
    "US loses measles-free status",
    "5,412 cases and 10 deaths in 2026, the most since 1991, end the status held since 2000.",
)
vx, vy = box[0] + 70, box[1] + 66
for a in range(0, 360, 30):
    rad = math.radians(a)
    x1, y1 = vx + 25 * math.cos(rad), vy + 25 * math.sin(rad)
    x2, y2 = vx + 39 * math.cos(rad), vy + 39 * math.sin(rad)
    d.line([x1, y1, x2, y2], fill=RED, width=5)
    d.ellipse([x2 - 6, y2 - 6, x2 + 6, y2 + 6], fill=RED)
d.ellipse([vx - 26, vy - 26, vx + 26, vy + 26], fill=(214, 69, 65))
for ox, oy in [(-10, -8), (9, -12), (2, 8), (-13, 10), (13, 12)]:
    d.ellipse([vx + ox - 4, vy + oy - 4, vx + ox + 4, vy + oy + 4], fill=(240, 160, 150))
d.text((box[0] + 18, box[1] + 118), "AFTER 26 YEARS", font=font(FB, 13), fill=GRAY)

# Row 3: Ebola | Voyager
RY3 = 788
box = half_tile(
    MX, RY3, (30, 110, 76), "AFRICA · HEALTH",
    "Congo Ebola outbreak passes 11,000 cases",
    "Now the second-largest Ebola outbreak on record; three in four infected children under five die.",
)
# simplified Africa silhouette in the illustration box
ax, ay = box[0] + 14, box[1] + 8
africa = [
    (0.30, 0.04), (0.55, 0.03), (0.78, 0.06), (0.88, 0.16), (0.90, 0.26), (1.00, 0.36),
    (0.88, 0.42), (0.84, 0.52), (0.80, 0.66), (0.76, 0.78), (0.66, 0.92), (0.52, 0.98),
    (0.40, 0.88), (0.36, 0.72), (0.33, 0.58), (0.30, 0.48), (0.20, 0.44), (0.10, 0.40),
    (0.04, 0.30), (0.10, 0.18), (0.20, 0.08),
]
pts = [(ax + u * 108, ay + v * 128) for u, v in africa]
d.polygon(pts, fill=(233, 201, 130), outline=(30, 110, 76))
d.ellipse([ax + 42, ay + 58, ax + 54, ay + 70], fill=RED)  # DRC, Congo basin
d.text((box[0] + 12, box[1] + 140), "DR CONGO", font=font(FB, 13), fill=GRAY)

box = half_tile(
    MX + HW + 16, RY3, (24, 24, 40), "SCIENCE · SPACE",
    "Voyager 1 reaches one light-day from Earth",
    "The 1977 probe crossed 16 billion miles, a distance light needs 24 hours to travel. A human first.",
)
gx0, gy0, gx1, gy1 = box[0], box[1] + 2, box[2], box[1] + 128
d.rounded_rectangle([gx0, gy0, gx1, gy1], radius=6, fill=(10, 10, 24))
random.seed(18)
for _ in range(30):
    px_, py_ = random.randint(gx0 + 4, gx1 - 4), random.randint(gy0 + 4, gy1 - 4)
    d.ellipse([px_, py_, px_ + 2, py_ + 2], fill=(255, 255, 255))
d.ellipse([gx0 + 12, gy1 - 26, gx0 + 24, gy1 - 14], fill=(86, 156, 214))
d.text((gx0 + 8, gy1 - 44), "EARTH", font=font(FB, 11), fill=(150, 200, 255))
d.ellipse([gx1 - 40, gy0 + 14, gx1 - 12, gy0 + 42], outline=(240, 200, 90), width=3)
d.rectangle([gx1 - 30, gy0 + 24, gx1 - 22, gy0 + 34], fill=(240, 200, 90))
d.rectangle([gx1 - 52, gy0 + 52, gx1 - 30, gy0 + 60], fill=(120, 140, 190))
for t in (0.2, 0.4, 0.6, 0.8):
    px_ = gx0 + 20 + (gx1 - 46 - gx0) * t
    py_ = gy1 - 22 - (gy1 - 30 - gy0) * t * 0.55
    d.ellipse([px_ - 1, py_ - 1, px_ + 2, py_ + 2], fill=(150, 200, 255))
d.text((box[0] + 8, box[1] + 136), "1 LIGHT-DAY AWAY", font=font(FB, 13), fill=GRAY)

# ---------------------------------------------------------------- footer
FY = 978
d.line([MX, FY, W - MX, FY], fill=INK, width=2)
block(
    (MX, FY + 8),
    "ALSO ON 18 NOVEMBER — Israel's Knesset elects speaker Kahana · Trump's peace board faults Israel "
    "and Hamas · Prabowo witnesses Rp1,300T in Indonesia–China deals · European stocks slide (DAX −2.1%)",
    font(FR, 16), GRAY, CW,
)

for w_ in WARNINGS:
    print("WARN:", w_)
img.save("entry.png")
print("saved entry.png", img.size)
