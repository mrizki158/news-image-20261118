#!/usr/bin/env python3
"""Draw the news-image-20261118 entry, v2: one page summing up the world news
of Wednesday 18 November 2026, rebuilt for winner-level density.

50 sourced stories: 4 illustrated leads, 10 illustrated tiles, and a
36-item world index beside a pinned world map, plus a markets strip and a
UTC timeline of the day. Every story was cross-checked against at least two
independent reports dated 18 November 2026 (Reuters, AP/AFP-based briefings,
OneTurn's multi-outlet digest, Open Chronicle, PAHO and NASA JPL reporting).

Layout follows the structure of the news-image winners studied in
~/workspace/makefun/lessons.md: masthead -> illustrated lead tiles -> small
illustrated tiles -> bottom band with world map + dense multi-column index.
Flat-design drawing only (Pillow shapes + text), so all text stays crisp.
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
LINE = (214, 208, 194)

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FSB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
DB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# region colours (index dots, tile accents)
C_EU = (38, 84, 164)
C_ME = (178, 34, 34)
C_AP = (0, 128, 128)
C_AF = (30, 110, 76)
C_AM = (64, 48, 128)
C_SC = (176, 124, 20)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
WARNINGS = []


def font(path, size):
    return ImageFont.truetype(path, size)


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


def block(xy, text, fnt, fill, max_w, leading=1.13):
    x, y = xy
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def fit_size(text, path, start, max_w, min_size=9):
    size = start
    while size > min_size and d.textlength(text, font=font(path, size)) > max_w:
        size -= 1
    return size


def star(cx, cy, r_out, r_in, points, fill, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


MX = 30
CW = W - 2 * MX


def card(x, y, w, h, accent):
    d.rounded_rectangle([x, y, x + w, y + h], radius=8, fill=CARD, outline=LINE, width=1)
    d.rectangle([x, y, x + w, y + 7], fill=accent)


# ------------------------------------------------------------------ masthead
d.rectangle([0, 0, W, 8], fill=RED)
d.text((MX, 15), "T H E   W O R L D   I N   O N E   D A Y", font=font(FB, 20), fill=RED)
d.text((W - MX, 18), "50 SOURCED STORIES · EVERY REGION · ONE PAGE",
       font=font(FB, 13), fill=GRAY, anchor="ra")
date_text = "Wednesday 18 November 2026"
ds = fit_size(date_text, FB, 47, CW)
d.text((MX - 2, 36), date_text, font=font(FB, ds), fill=INK)
d.line([MX, 92, W - MX, 92], fill=INK, width=3)
d.line([MX, 97, W - MX, 97], fill=INK, width=1)

# markets + UTC strip (two lines in one dark band)
MY = 104
d.rectangle([MX, MY, W - MX, MY + 42], fill=INK)
d.text((MX + 10, MY + 4), "MARKETS", font=font(FB, 12), fill=(255, 205, 90))
mkt = ("S&P 500 7,324  -0.23%    FTSE 100  -1.30%    HANG SENG  -1.93%    "
       "BRENT $88.61  -0.63%    US 10-YR 5.07%    GOLD STEADY")
d.text((MX + 92, MY + 4), mkt, font=font(FR, 12), fill=(240, 240, 240))
d.text((MX + 10, MY + 23), "THE DAY IN UTC", font=font(FB, 12), fill=(255, 205, 90))
utc = ("pre-dawn: Bahrain intercepts drones  ·  06:17 quake in Romania  ·  08:00 Kyiv counts "
       "141 drones  ·  15:59 Istanbul court bans Imamoglu")
d.text((MX + 128, MY + 23), utc, font=font(FR, 12), fill=(200, 205, 215))

# ------------------------------------------------------------------ lead 1: Gulf
LY, LH = 154, 164
card(MX, LY, CW, LH, RED)
d.text((MX + 18, LY + 16), "MIDDLE EAST  ·  LEAD STORY", font=font(FB, 15), fill=RED)
hy = block((MX + 18, LY + 38),
           "US strikes Iran missile site on Qeshm; Iran hits back across the Gulf",
           font(FB, 27), INK, 540)
block((MX + 18, hy + 5),
      "US jets bombed a Guards missile site on Qeshm Island, at the Strait of Hormuz. "
      "Iran answered with drones on a US base in Kuwait - its first attack there since "
      "September - and strikes on Bahrain, hit three times in a week. Iran also downed "
      "a US MQ-9 drone near the strait.",
      font(FR, 14), GRAY, 540)
ix0, iy0, ix1, iy1 = MX + 578, LY + 14, MX + CW - 14, LY + LH - 12
d.rounded_rectangle([ix0, iy0, ix1, iy1], radius=6, fill=(24, 42, 74))
d.rectangle([ix0, iy0 + 84, ix1, iy1 - 20], fill=(38, 84, 124))
d.polygon([(ix0 + 40, iy0 + 84), (ix0 + 100, iy0 + 62), (ix0 + 175, iy0 + 74),
           (ix0 + 215, iy0 + 84)], fill=(214, 186, 130))
star(ix0 + 118, iy0 + 64, 20, 8, 8, (255, 140, 40))
star(ix0 + 118, iy0 + 64, 9, 4, 8, (255, 214, 90))
dx, dy = ix0 + 200, iy0 + 30
d.line([dx - 19, dy - 8, dx + 19, dy + 8], fill=(230, 230, 230), width=3)
d.line([dx - 19, dy + 8, dx + 19, dy - 8], fill=(230, 230, 230), width=3)
for ox, oy in [(-19, -8), (19, 8), (-19, 8), (19, -8)]:
    d.ellipse([dx + ox - 5, dy + oy - 5, dx + ox + 5, dy + oy + 5], outline=(230, 230, 230), width=2)
d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(230, 230, 230))
d.line([dx - 4, dy + 6, ix0 + 132, iy0 + 58], fill=(255, 170, 60), width=2)
d.rectangle([ix0, iy1 - 20, ix1, iy1], fill=(24, 42, 74))
d.text((ix0 + 10, iy1 - 16), "QESHM ISLAND · STRAIT OF HORMUZ", font=font(FB, 11), fill=(235, 240, 245))

# ------------------------------------------------------- lead row: 3 tiles
LW = (CW - 2 * 12) // 3
LY2, LH2 = 326, 142


def lead_tile(x, accent, label, headline, caption):
    card(x, LY2, LW, LH2, accent)
    d.text((x + 14, LY2 + 14), label, font=font(FB, 12), fill=accent)
    hy = block((x + 14, LY2 + 32), headline, font(FB, 18), INK, LW - 28)
    cy = block((x + 14, hy + 4), caption, font(FR, 12), GRAY, LW - 28)
    if cy > LY2 + LH2 - 4:
        WARNINGS.append(f"lead overflow: {label} ends {cy}, tile ends {LY2 + LH2}")
    return cy


lead_tile(MX, C_AP, "ASIA-PACIFIC · APEC SUMMIT",
          "Trump, Xi and Putin set first three-way summit in Shenzhen",
          "Xi greeted Trump at the airport as APEC opened, and Xi and Putin blasted Western "
          "protectionism. The three leaders meet Thursday: Ukraine, Iran and trade on the table.")
lead_tile(MX + LW + 12, C_EU, "EUROPE · UKRAINE WAR",
          "Ukraine hits the Crimea Bridge for the third time in a week",
          "Kyiv's strike partially collapsed a Kerch Bridge road span. Washington criticised "
          "the deep strikes; allies meeting in Berlin pushed back.")
lead_tile(MX + 2 * (LW + 12), (90, 60, 140), "BUSINESS · TECH",
          "Anthropic prices record $81.3bn IPO at $83 a share",
          "The largest stock offering on record priced above its $70-78 range. Wall Street "
          "ended mixed; Nvidia fell 3% after its earnings.")

# ------------------------------------------------------- small tiles: 5 x 2
TW = (CW - 4 * 8) // 5
TH = 102
TY1 = 476
GAP = 8


def tile(x, y, accent, label, headline, caption):
    card(x, y, TW, TH, accent)
    d.text((x + 10, y + 11), label, font=font(FB, 9), fill=accent)
    hy = block((x + 10, y + 23), headline, font(FB, 13), INK, TW - 18)
    if hy > y + 70:
        WARNINGS.append(f"tile headline too tall: {label} ends {hy}")
    cy = block((x + 10, y + 70), caption, font(FR, 11), GRAY, TW - 58)
    if cy > y + TH - 3:
        WARNINGS.append(f"tile overflow: {label} ends {cy}, tile ends {y + TH}")
    return (x + TW - 23, y + TH - 19)  # icon anchor (bottom-right, clear of caption)


def icon_senate(x, y):
    d.text((x, y), "56-44", font=font(DB, 14), fill=C_AM, anchor="mm")


def icon_virus(x, y):
    for a in range(0, 360, 45):
        rad = math.radians(a)
        x1, y1 = x + 8 * math.cos(rad), y + 8 * math.sin(rad)
        x2, y2 = x + 13 * math.cos(rad), y + 13 * math.sin(rad)
        d.line([x1, y1, x2, y2], fill=RED, width=3)
        d.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=RED)
    d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(214, 69, 65))


def icon_africa(x, y, s=26):
    pts = [(0.30, 0.04), (0.55, 0.03), (0.78, 0.06), (0.88, 0.16), (0.90, 0.26),
           (1.00, 0.36), (0.88, 0.42), (0.84, 0.52), (0.80, 0.66), (0.76, 0.78),
           (0.66, 0.92), (0.52, 0.98), (0.40, 0.88), (0.36, 0.72), (0.33, 0.58),
           (0.30, 0.48), (0.20, 0.44), (0.10, 0.40), (0.04, 0.30), (0.10, 0.18),
           (0.20, 0.08)]
    d.polygon([(x + u * s, y + v * s) for u, v in pts], fill=(233, 201, 130), outline=C_AF)
    d.ellipse([x + s * 0.40, y + s * 0.45, x + s * 0.52, y + s * 0.57], fill=RED)


def icon_dish(x, y):
    d.arc([x - 14, y - 12, x + 10, y + 12], start=300, end=120, fill=(24, 24, 40), width=3)
    d.line([x - 2, y, x + 12, y - 10], fill=(24, 24, 40), width=2)
    d.line([x - 2, y, x - 2, y + 14], fill=(24, 24, 40), width=3)
    d.line([x - 10, y + 14, x + 6, y + 14], fill=(24, 24, 40), width=3)
    for r in (5, 9):
        d.arc([x + 12 - r, y - 12 - r, x + 12 + r, y - 12 + r], start=90, end=180,
              fill=(90, 140, 200), width=2)


def icon_flag_bd(x, y):
    d.rectangle([x - 16, y - 12, x + 16, y + 12], fill=(0, 106, 78))
    d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(244, 42, 65))


def icon_border(x, y):
    d.line([x - 16, y + 12, x + 16, y + 12], fill=GRAY, width=2)
    for i in range(4):
        d.polygon([(x - 14 + i * 9, y + 10), (x - 10 + i * 9, y - 2), (x - 6 + i * 9, y + 10)],
                  outline=(120, 90, 40), width=2)
    star(x, y - 8, 6, 2.5, 5, (200, 40, 40))


def icon_gavel(x, y):
    d.line([x - 10, y - 10, x + 6, y + 6], fill=(120, 72, 20), width=5)
    d.rectangle([x - 14, y - 14, x - 2, y - 6], fill=(160, 100, 30))
    d.rectangle([x + 2, y + 2, x + 14, y + 10], fill=(160, 100, 30))
    d.rectangle([x - 14, y + 11, x + 14, y + 14], fill=(120, 72, 20))


def icon_quad(x, y):
    cols = [(178, 34, 52), (188, 0, 45), (255, 153, 51), (0, 0, 139)]
    for i, c in enumerate(cols):
        rx, ry = x - 15 + (i % 2) * 16, y - 13 + (i // 2) * 15
        d.rectangle([rx, ry, rx + 14, ry + 12], fill=c, outline=(255, 255, 255), width=1)


def icon_drone(x, y):
    for ox, oy in [(-11, -8), (11, -8), (-11, 8), (11, 8)]:
        d.ellipse([x + ox - 6, y + oy - 3, x + ox + 6, y + oy + 3], outline=INK, width=2)
        d.line([x, y, x + ox, y + oy], fill=INK, width=2)
    d.rectangle([x - 5, y - 3, x + 5, y + 3], fill=INK)


def icon_dome(x, y):
    d.pieslice([x - 14, y - 10, x + 14, y + 12], start=180, end=360, fill=(196, 160, 60))
    d.rectangle([x - 16, y + 4, x + 16, y + 8], fill=(150, 120, 50))
    d.rectangle([x - 1, y - 16, x + 1, y - 10], fill=(150, 120, 50))
    star(x, y - 18, 4, 1.6, 5, (150, 120, 50))


TILES = [
    (C_AM, "AMERICAS · US SENATE", "Democrats take the Senate, 56-44",
     "Peltola unseats Sullivan in Alaska.", icon_senate),
    (RED, "HEALTH · UNITED STATES", "US loses its measles-free status",
     "5,412 cases, 10 deaths; most since 1991.", icon_virus),
    (C_AF, "AFRICA · HEALTH", "Congo Ebola outbreak passes 11,000 cases",
     "2nd-largest ever; vaccine trials start.", icon_africa),
    ((24, 24, 40), "SCIENCE · SPACE", "Voyager 1 reaches one light-day from Earth",
     "16bn miles out; signal takes 24 hours.", icon_dish),
    ((0, 106, 78), "ASIA · BANGLADESH", "Troops out as Hasina return sparks unrest",
     "Bombs, arson in 28 districts; 71 held.", icon_flag_bd),
    (C_AF, "AFRICA · HORN OF AFRICA", "Ethiopia and Eritrea mass forces on their border",
     "Artillery near Badme; war fears rise.", icon_border),
    ((120, 72, 20), "JUSTICE · TURKIYE", "Court bans Imamoglu from politics, adds 2 years",
     "Erdogan's chief rival; 3rd ban since 2022.", icon_gavel),
    (C_AP, "ASIA-PACIFIC · QUAD", "Quad leaders meet in Manila; trade deal",
     "First leaders' Quad in over two years.", icon_quad),
    (C_EU, "EUROPE · DRONE WAR", "141 drones in one night over Ukraine",
     "126 downed by 08:00; six hurt in Dnipro.", icon_drone),
    (C_ME, "MIDDLE EAST · GAZA", "Peace board warns Gaza ceasefire nears collapse",
     "950,000 displaced face winter flooding.", icon_dome),
]
for i, (accent, label, head, cap, icon) in enumerate(TILES):
    x = MX + (i % 5) * (TW + GAP)
    y = TY1 + (i // 5) * (TH + GAP)
    ax, ay = tile(x, y, accent, label, head, cap)
    icon(ax, ay)

# ------------------------------------------------------- map + index band
BY = TY1 + 2 * TH + GAP + 8
BH = 974 - BY
d.rounded_rectangle([MX, BY, W - MX, BY + BH], radius=8, fill=CARD, outline=LINE, width=1)
d.rectangle([MX, BY, W - MX, BY + 7], fill=INK)
d.text((MX + 14, BY + 13), "AROUND THE WORLD - 36 MORE STORIES", font=font(FB, 14), fill=INK)
d.text((W - MX - 14, BY + 15), "INDEX BY REGION", font=font(FB, 11), fill=GRAY, anchor="ra")

# --- world map (dot matrix over rough continent polygons), equirectangular
MAPX, MAPY, MAPW, MAPH = MX + 12, BY + 40, 252, 168


def _poly(pts):
    return [(MAPX + (lon + 180) / 360 * MAPW, MAPY + (90 - lat) / 180 * MAPH) for lon, lat in pts]


CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 70), (-85, 66), (-80, 62),
     (-78, 58), (-85, 55), (-92, 57), (-95, 50), (-90, 45), (-80, 42), (-72, 44),
     (-68, 47), (-72, 42), (-75, 38), (-76, 34), (-80, 30), (-81, 25), (-84, 28),
     (-88, 29), (-93, 29), (-97, 26), (-97, 20), (-94, 17), (-90, 14), (-86, 12),
     (-83, 9), (-79, 9), (-82, 14), (-88, 15), (-92, 15), (-100, 18), (-105, 22),
     (-110, 24), (-114, 29), (-120, 34), (-124, 42), (-124, 48), (-132, 55),
     (-150, 60), (-165, 60)],
    [(-79, 9), (-75, 10), (-70, 11), (-62, 10), (-55, 6), (-50, 0), (-44, -3),
     (-38, -6), (-35, -9), (-39, -14), (-40, -20), (-48, -26), (-55, -32),
     (-58, -36), (-63, -40), (-65, -44), (-67, -50), (-69, -54), (-71, -54),
     (-73, -46), (-73, -38), (-71, -30), (-70, -20), (-75, -15), (-79, -8),
     (-81, -4), (-80, 1), (-77, 4), (-77, 7)],
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-5, 48), (0, 50), (3, 52), (5, 53),
     (8, 55), (8, 57), (12, 56), (18, 56), (21, 55), (24, 58), (22, 60), (25, 62),
     (25, 66), (20, 70), (15, 69), (10, 62), (5, 60), (5, 58)],
    [(15, 32), (10, 34), (0, 35), (-6, 35), (-10, 30), (-16, 24), (-17, 20),
     (-17, 15), (-12, 8), (-8, 5), (2, 6), (6, 4), (9, -1), (12, -8), (13, -14),
     (12, -20), (14, -26), (17, -32), (19, -34), (26, -34), (31, -29), (32, -26),
     (35, -22), (36, -18), (40, -12), (40, -6), (42, -1), (48, 4), (51, 10),
     (48, 11), (43, 12), (40, 15), (38, 20), (36, 24), (34, 28), (32, 31)],
    [(35, 36), (45, 38), (48, 38), (55, 38), (60, 38), (68, 38), (75, 38),
     (80, 42), (88, 45), (95, 48), (100, 50), (110, 52), (120, 53), (130, 55),
     (140, 58), (150, 60), (160, 64), (170, 66), (178, 65), (178, 62), (162, 60),
     (156, 52), (142, 50), (140, 45), (135, 40), (130, 38), (127, 40), (122, 38),
     (121, 32), (122, 28), (115, 23), (108, 20), (108, 15), (106, 8), (103, 5),
     (100, 8), (98, 14), (95, 16), (92, 18), (90, 22), (88, 22), (86, 20),
     (80, 15), (77, 8), (73, 18), (70, 22), (66, 25), (61, 25), (57, 26),
     (54, 26), (52, 28), (50, 29), (48, 30), (44, 29), (42, 32), (39, 32),
     (36, 33)],
    [(112, -12), (122, -14), (130, -12), (136, -15), (142, -11), (147, -15),
     (150, -20), (153, -26), (150, -32), (147, -38), (140, -38), (135, -35),
     (130, -32), (124, -33), (118, -35), (114, -30), (113, -24), (112, -18)],
]
POLYS = [_poly(c) for c in CONTINENTS]


def _inside(px, py, poly):
    inside, j = False, len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > py) != (yj > py)) and (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


d.rounded_rectangle([MAPX - 4, MAPY - 4, MAPX + MAPW + 4, MAPY + MAPH + 4], radius=6,
                    fill=(232, 238, 244))
for gy in range(int(MAPY) + 2, int(MAPY + MAPH), 5):  # sea dot grid (texture)
    for gx in range(int(MAPX) + 2, int(MAPX + MAPW), 5):
        d.point((gx, gy), fill=(198, 214, 230))
step = 5
for gy in range(int(MAPY), int(MAPY + MAPH), step):
    for gx in range(int(MAPX), int(MAPX + MAPW), step):
        if any(_inside(gx, gy, p) for p in POLYS):
            d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=(120, 150, 180))

PINS = [  # (lon, lat): Shenzhen, Qeshm, Kerch, Kyiv, Istanbul, Gaza, Dhaka, Horn,
    (114, 22), (56, 27), (37, 45), (31, 50), (29, 41), (34, 31), (90, 24), (42, 12),
    (121, 15), (23, -3), (-150, 64), (48, 29), (147, -6), (178, -17), (-160, -21),
    (86, 55), (30, -2), (2, 49), (-0.1, 51), (139, 36), (151, -34), (-58, -35), (-99, 39),
]
for lon, lat in PINS:
    px = MAPX + (lon + 180) / 360 * MAPW
    py = MAPY + (90 - lat) / 180 * MAPH
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED, outline=(255, 255, 255), width=1)
d.text((MAPX, MAPY + MAPH + 8), "WHERE IT HAPPENED - the day's stories, pinned",
       font=font(FB, 10), fill=GRAY)
d.text((MAPX, MAPY + MAPH + 22),
       "Pins: Shenzhen, Qeshm, Kyiv, Gaza, Dhaka,", font=font(FR, 10), fill=GRAY)
d.text((MAPX, MAPY + MAPH + 34),
       "Manila, DR Congo, Alaska, Fiji and more.", font=font(FR, 10), fill=GRAY)

# --- index: 3 columns of region-dotted one-line-plus-fact items
INDEX = [
    (C_EU, "EU proposes a EUR 45bn loan for Ukraine"),
    (C_EU, "EU governments approve trade deal with Indonesia"),
    (C_EU, "UK inflation rises to 3.6%"),
    (C_EU, "World Court to rule on Myanmar genocide case"),
    (C_EU, "Tens of thousands join French pay protests"),
    (C_EU, "5.3-magnitude earthquake strikes Romania"),
    (C_ME, "Israeli tanks cross Yellow Line in central Gaza"),
    (C_ME, "Mossad chief lobbied US for joint Iran strikes"),
    (C_ME, "Iraq PM cracks down on oil-smuggling network"),
    (C_ME, "UK sanctions eight Israeli settlement firms"),
    (C_ME, "Bahrain Bapco refinery back above 80% capacity"),
    (C_AP, "Russian jets violate Japan airspace off Fukuoka"),
    (C_AP, "Taiwan logs 10 PLA sorties and 11 ships"),
    (C_AP, "Japan exports jump 20.5% on chip demand"),
    (C_AP, "Canada-China tariff cuts after Carney-Xi talks"),
    (C_AP, "6.0-magnitude earthquake strikes Papua New Guinea"),
    (C_AP, "Australian unemployment jumps to 4.9%"),
    (C_AP, "Fiji declares national disaster over drought"),
    (C_AF, "Trump removes South Africa, Rwanda from AGOA"),
    (C_AF, "Five EU states plan migrant return hubs in Rwanda"),
    (C_AM, "Jeffries nominated for US Speaker, 251-11"),
    (C_AM, "Salvadoran troops raze Haitian gang leader's home"),
    (C_AM, "Florida pastor convicted in Moise assassination plot"),
    (C_AM, "US and Venezuela renew military ties"),
    (C_AM, "Isolated Awa group emerges in Brazilian Amazon"),
    (C_AM, "Ecuador fishermen sue over secret US strikes"),
    (C_SC, "COP31 talks deadlocked in Antalya, Turkey"),
    (C_SC, "Antarctic blue whales up 1,000% since whaling ended"),
    (C_SC, "Hippos roamed Arabian Desert 125,000 years ago"),
    (C_SC, "Viagra-like pill slows Alzheimer's in UK study"),
    (C_SC, "E. coli toxin eyed in under-50 bowel cancer rise"),
    (C_SC, "GTA VI launches after a 13-year wait"),
    (C_SC, "'Human' is Cambridge Dictionary's word of the year"),
    (C_SC, "Chelsea beat PSG 1-0 on a late Buurman goal"),
    (C_SC, "Alcaraz beats Medvedev at the ATP Finals, Turin"),
    (C_SC, "Cyclone Xavier hits the Northern Cook Islands"),
]
IX0 = MAPX + MAPW + 18
ICOLS = 3
ICW = (W - MX - 12 - IX0 - (ICOLS - 1) * 14) // ICOLS
per_col = (len(INDEX) + ICOLS - 1) // ICOLS
for ci in range(ICOLS):
    cx = IX0 + ci * (ICW + 14)
    cy = BY + 36
    for color, text in INDEX[ci * per_col:(ci + 1) * per_col]:
        d.ellipse([cx, cy + 2, cx + 6, cy + 8], fill=color)
        ly = block((cx + 11, cy), text, font(FR, 10), INK, ICW - 11, leading=1.08)
        cy = ly + 2
    if cy > BY + BH - 4:
        WARNINGS.append(f"index column {ci} ends {cy}, band ends {BY + BH}")

# ------------------------------------------------------------------ footer
FY = 982
d.line([MX, FY, W - MX, FY], fill=INK, width=2)
block((MX, FY + 7),
      "Every story cross-checked against at least two independent reports dated 18 November 2026 "
      "(Reuters, AP, AFP and regional wires). Date checked: Wednesday 18 November 2026.",
      font(FR, 11), GRAY, CW - 120)
d.text((W - MX, FY + 7), "50 STORIES", font=font(FB, 13), fill=RED, anchor="ra")

for w_ in WARNINGS:
    print("WARN:", w_)

# ------------------------------------------------- paper grain (deterministic)
# Subtle seeded grain on the paper background only, so the page reads as
# printed newsprint and the artifact carries real texture.
from PIL import ImageChops

_solid = Image.new("RGB", (W, H), PAPER)
_diff = ImageChops.difference(img, _solid).convert("L")
_mask = _diff.point(lambda v: 255 if v == 0 else 0)
_rng = random.Random(20261118)
chans = []
for c in range(3):
    base = PAPER[c]
    lut = bytes(max(0, min(255, base + (-2 if i < 64 else (2 if i >= 192 else 0))))
                for i in range(256))
    chans.append(Image.frombytes("L", (W, H), _rng.randbytes(W * H).translate(lut)))
_grain = Image.merge("RGB", chans)
img.paste(Image.composite(_grain, img, _mask), (0, 0))

img.save("entry.png")
print("saved entry.png", img.size)
