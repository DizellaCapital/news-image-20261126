"""Draw the one-page newspaper for Thursday 26 November 2026.

Reads stories_20261126.json next to this file and writes entry.png
(1024x1024, deterministic: same input bytes always produce the same
output bytes). Only Pillow + stdlib are used here; the graded entry
runner (main.py) is stdlib-only and never imports this file.
"""

import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = 1024
H = 1024
PAPER = (246, 241, 230)
INK = (20, 20, 20)
RED = (168, 30, 38)
DARKRED = (120, 18, 26)
BLUE = (31, 78, 121)
SKY = (158, 199, 232)
GRAY = (85, 85, 85)
LIGHT = (232, 226, 212)
GOLD = (201, 138, 20)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


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


def fit_one_line(draw, text, fnt, max_w):
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "..."


STATUS_COLOR = {
    "CONFIRMED": (18, 110, 60),
    "REPORTED": (120, 80, 0),
    "CLAIM": (168, 30, 38),
    "ONGOING": (31, 78, 121),
}


def status_tag(draw, x, y, status, fnt):
    col = STATUS_COLOR.get(status, INK)
    draw.text((x, y), status, font=fnt, fill=col)
    return x + draw.textlength(status, font=fnt)


def rule(draw, x0, x1, y, width=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- scenes
def scene_balloon(w, h):
    img = Image.new("RGB", (w, h), SKY)
    d = ImageDraw.Draw(img)
    for bx, bw, bh in [(0, 46, 58), (52, 40, 80), (250, 44, 66), (292, 26, 44)]:
        d.rectangle([bx, h - bh, bx + bw, h], fill=(70, 80, 95))
    for cx, cy in [(60, 26), (150, 18), (235, 30)]:
        d.ellipse([cx, cy, cx + 44, cy + 16], fill=(255, 255, 255))
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([w // 2 - 52, 6, w // 2 + 52, 74], fill=255)
    tmp = Image.new("RGB", (w, h), (200, 40, 48))
    td = ImageDraw.Draw(tmp)
    for sx in range(w // 2 - 52, w // 2 + 52, 26):
        td.rectangle([sx, 0, sx + 12, h], fill=(255, 255, 255))
    img.paste(tmp, (0, 0), mask)
    d = ImageDraw.Draw(img)
    d.ellipse([w // 2 - 52, 6, w // 2 + 52, 74], outline=(120, 18, 26), width=3)
    d.line([(w // 2 - 16, 74), (w // 2 - 10, h - 8)], fill=(60, 40, 20), width=2)
    d.line([(w // 2 + 16, 74), (w // 2 + 10, h - 8)], fill=(60, 40, 20), width=2)
    d.rectangle([w // 2 - 14, h - 12, w // 2 + 14, h - 2], fill=(120, 80, 30))
    return img


def scene_fire(w, h):
    img = Image.new("RGB", (w, h), (28, 26, 30))
    d = ImageDraw.Draw(img)
    for cx, cy, r in [(40, 18, 16), (90, 12, 20), (150, 20, 14), (230, 14, 18), (280, 22, 13)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(60, 60, 66))
    d.rectangle([20, h - 26, w - 20, h - 14], fill=(15, 15, 18))
    d.rectangle([w - 90, h - 52, w - 30, h - 26], fill=(25, 25, 30))
    d.rectangle([w - 84, h - 64, w - 36, h - 52], fill=(25, 25, 30))
    for fx, fh, col in [(60, 46, (255, 120, 20)), (110, 58, (255, 170, 30)),
                        (160, 44, (255, 100, 10)), (210, 52, (255, 150, 25))]:
        d.polygon([(fx - 16, h - 26), (fx, h - 26 - fh), (fx + 16, h - 26)],
                  fill=col)
        d.polygon([(fx - 8, h - 26), (fx, h - 26 - fh + 14), (fx + 8, h - 26)],
                  fill=(255, 230, 120))
    return img


def scene_tariff(w, h):
    img = Image.new("RGB", (w, h), (18, 48, 88))
    d = ImageDraw.Draw(img)
    cx, cy, r = w // 2 - 52, h // 2, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 130, 190),
              outline=(255, 255, 255), width=2)
    d.ellipse([cx - 16, cy - r, cx + 16, cy + r], outline=(255, 255, 255), width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(255, 255, 255), width=2)
    d.ellipse([cx - r + 6, cy - 18, cx + r - 6, cy + 18], outline=(200, 220, 240), width=1)
    d.text((w // 2 + 6, h // 2 - 30), "20%", font=SANS_B(46), fill=(255, 220, 80))
    d.text((w // 2 + 8, h // 2 + 20), "ON CHINA", font=SANS_B(15), fill=(255, 255, 255))
    return img


def scene_tanker(w, h):
    img = Image.new("RGB", (w, h), (38, 96, 140))
    d = ImageDraw.Draw(img)
    d.rectangle([0, h - 30, w, h], fill=(24, 68, 100))
    for wx in range(0, w, 26):
        d.line([(wx, h - 18), (wx + 12, h - 18)], fill=(160, 200, 230), width=2)
    d.polygon([(14, h - 34), (w - 14, h - 34), (w - 30, h - 52), (30, h - 52)],
              fill=(30, 30, 34))
    d.rectangle([w - 52, h - 74, w - 26, h - 52], fill=(30, 30, 34))
    for fx, fh, col in [(w // 2 - 26, 40, (255, 120, 20)), (w // 2 + 8, 50, (255, 170, 30))]:
        d.polygon([(fx - 13, h - 52), (fx, h - 52 - fh), (fx + 13, h - 52)], fill=col)
    return img


def scene_refinery(w, h):
    img = Image.new("RGB", (w, h), (226, 130, 50))
    d = ImageDraw.Draw(img)
    d.rectangle([0, h - 22, w, h], fill=(60, 45, 40))
    for tx, tw, th in [(18, 16, 52), (44, 14, 66), (120, 18, 58), (148, 14, 44)]:
        d.rectangle([tx, h - 22 - th, tx + tw, h - 22], fill=(50, 50, 55))
        d.rectangle([tx + tw // 2 - 2, h - 22 - th - 12, tx + tw // 2 + 2, h - 22 - th],
                    fill=(50, 50, 55))
    d.ellipse([84, h - 62, 116, h - 30], fill=(120, 90, 80))
    for fx, fh in [(90, 34), (110, 42)]:
        d.polygon([(fx - 10, h - 60), (fx, h - 60 - fh), (fx + 10, h - 60)],
                  fill=(255, 220, 90))
    return img


def scene_rocket(w, h):
    img = Image.new("RGB", (w, h), (12, 18, 48))
    d = ImageDraw.Draw(img)
    for sx, sy in [(20, 14), (60, 30), (110, 10), (150, 26), (176, 12), (40, 52), (140, 52)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    cx = w // 2
    d.polygon([(cx - 12, h - 26), (cx - 12, 22), (cx, 6), (cx + 12, 22), (cx + 12, h - 26)],
              fill=(235, 235, 235), outline=(150, 150, 150))
    d.polygon([(cx - 12, 22), (cx, 6), (cx + 12, 22)], fill=(200, 40, 48))
    d.rectangle([cx - 12, h - 46, cx + 12, h - 38], fill=(200, 40, 48))
    d.polygon([(cx - 20, h - 26), (cx - 12, h - 40), (cx - 12, h - 26)], fill=(200, 40, 48))
    d.polygon([(cx + 20, h - 26), (cx + 12, h - 40), (cx + 12, h - 26)], fill=(200, 40, 48))
    d.polygon([(cx - 7, h - 26), (cx, h - 8), (cx + 7, h - 26)], fill=(255, 170, 30))
    return img


def scene_lab(w, h):
    img = Image.new("RGB", (w, h), (16, 110, 110))
    d = ImageDraw.Draw(img)
    for i in range(6):
        y = 10 + i * 9
        x1 = w // 2 - 34 + int(14 * math.sin(i))
        x2 = w // 2 + 34 - int(14 * math.sin(i))
        d.line([(x1, y), (x2, y)], fill=(255, 255, 255), width=2)
        d.ellipse([x1 - 3, y - 3, x1 + 3, y + 3], fill=(255, 220, 80))
        d.ellipse([x2 - 3, y - 3, x2 + 3, y + 3], fill=(255, 220, 80))
    d.text((w - 58, h - 24), "$600m", font=SANS_B(20), fill=(255, 255, 255))
    return img


SCENES = {
    "balloon": scene_balloon,
    "fire": scene_fire,
    "tariff": scene_tariff,
    "tanker": scene_tanker,
    "refinery": scene_refinery,
    "rocket": scene_rocket,
    "lab": scene_lab,
}

# ---------------------------------------------------------------- map
CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
           (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
           (-105, 20), (-115, 30), (-125, 40), (-125, 49), (-150, 60)],
    "SA": [(-80, 10), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
           (-58, -38), (-65, -45), (-70, -55), (-73, -40), (-72, -20), (-80, -5)],
    "EU": [(-10, 36), (-9, 43), (0, 46), (-2, 49), (5, 53), (8, 57), (18, 56),
           (21, 55), (28, 60), (30, 70), (40, 68), (45, 60), (40, 50), (30, 46),
           (23, 40), (19, 42), (12, 44), (3, 42)],
    "AF": [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
           (40, 15), (51, 12), (48, 0), (40, -15), (35, -25), (28, -33), (18, -35),
           (12, -18), (9, -1), (9, 4), (-8, 5)],
    "AS": [(40, 68), (60, 70), (80, 73), (110, 76), (140, 72), (160, 66), (178, 65),
           (170, 60), (158, 52), (142, 45), (135, 35), (127, 33), (120, 25),
           (108, 18), (105, 8), (100, 8), (95, 15), (90, 22), (80, 15), (77, 8),
           (72, 20), (66, 25), (58, 26), (52, 28), (48, 30), (44, 30), (40, 36),
           (40, 44), (40, 60)],
    "OC": [(113, -22), (114, -30), (115, -35), (125, -33), (135, -35), (142, -38),
           (147, -39), (150, -37), (153, -27), (146, -19), (142, -11), (136, -12),
           (132, -11), (126, -14), (122, -17), (118, -20)],
}


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 170.0) / 360.0 * (x1 - x0)
    y = y0 + (80.0 - lat) / 135.0 * (y1 - y0)
    return x, y


def draw_map(draw, box, stories):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(214, 231, 240), outline=INK, width=1)
    for pts in CONTINENTS.values():
        xy = [project(lon, lat, box) for lon, lat in pts]
        draw.polygon(xy, fill=(216, 210, 192), outline=(120, 112, 96))
    offsets = {3: (18, 14), 7: (-14, -10), 8: (16, -12)}
    for st in stories:
        if st["kind"] not in ("lead", "grid"):
            continue
        lat, lon = st["pin"]
        px, py = project(lon, lat, box)
        ox, oy = offsets.get(st["n"], (0, 0))
        if (ox, oy) != (0, 0):
            draw.line([(px, py), (px + ox, py + oy)], fill=RED, width=1)
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
            px, py = px + ox, py + oy
        r = 9
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=2)
        label = str(st["n"])
        tw = draw.textlength(label, font=SANS_B(10))
        draw.text((px - tw / 2, py - 6), label, font=SANS_B(10),
                  fill=(255, 255, 255))
    draw.text((x0 + 6, y0 + 4), "WORLD MAP — PINS 1-8", font=SANS_B(11), fill=INK)


# ---------------------------------------------------------------- build
def build():
    with open(os.path.join(HERE, "stories_20261126.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    meta = data["meta"]
    stories = data["stories"]
    leads = [s for s in stories if s["kind"] == "lead"]
    grid = [s for s in stories if s["kind"] == "grid"]
    also = [s for s in stories if s["kind"] == "also"]
    assert len(stories) == 36 and len(leads) == 3 and len(grid) == 5
    assert len(also) == 28

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26
    right = W - M

    # top kicker
    d.text((M, 12), "THE WORLD IN ONE DAY", font=SANS_B(15), fill=RED)
    tag = "36 STORIES  •  7 REGIONS  •  17 SOURCES"
    d.text((right - d.textlength(tag, font=SANS_B(13)), 14), tag,
           font=SANS_B(13), fill=INK)

    # masthead: the date, giant
    mast = "THURSDAY 26 NOVEMBER 2026"
    mf = SERIF_B(54)
    mw = d.textlength(mast, font=mf)
    d.text(((W - mw) / 2, 30), mast, font=mf, fill=INK)
    rule(d, M, right, 96, 3)

    # region-count subline + press time
    counts = "  •  ".join(
        "%s %d" % (c["region"].upper(), c["count"]) for c in meta["region_counts"])
    sub = counts + "   —   TO PRESS TIME %s" % meta["press_time"]
    sf = SANS(12)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 102), sub, font=sf, fill=GRAY)
    rule(d, M, right, 120, 1, GRAY)

    # number strip
    strip = meta["numbers_strip"]
    y0, y1 = 128, 186
    cw = (right - M - 5 * 8) / 6
    for i, cell in enumerate(strip):
        x0 = M + i * (cw + 8)
        d.rectangle([x0, y0, x0 + cw, y1], outline=RED, width=2)
        vf = SANS_B(30)
        v = cell["value"]
        d.text((x0 + (cw - d.textlength(v, font=vf)) / 2, y0 + 4), v,
               font=vf, fill=RED)
        lf = SANS(11)
        lab = cell["label"]
        d.text((x0 + (cw - d.textlength(lab, font=lf)) / 2, y1 - 18), lab,
               font=lf, fill=INK)

    # three leads
    ly0, ly1 = 196, 400
    colw = (right - M - 2 * 10) / 3
    for i, st in enumerate(leads):
        x0 = M + i * (colw + 10)
        d.rectangle([x0, ly0, x0 + colw, ly1], outline=INK, width=1)
        scene = SCENES[st["scene"]](int(colw), 92)
        img.paste(scene, (int(x0), ly0))
        d.rectangle([x0, ly0, x0 + colw, ly0 + 92], outline=INK, width=1)
        tx = x0 + 8
        tw = colw - 16
        d.text((tx, ly0 + 98), "%d  •  %s" % (st["n"], st["region"].upper()),
               font=SANS_B(12), fill=RED)
        hf = SERIF_B(19)
        lines = wrap(d, st["headline"], hf, tw)[:2]
        yy = ly0 + 116
        for ln in lines:
            d.text((tx, yy), ln, font=hf, fill=INK)
            yy += 20
        df = SANS(11)
        dlines = wrap(d, st["deck"], df, tw)
        if len(dlines) > 2:
            dlines = dlines[:2]
            dlines[1] = fit_one_line(d, dlines[1], df, tw)
        for ln in dlines:
            d.text((tx, yy), ln, font=df, fill=INK)
            yy += 13
        meta_line = st["source"] + "  •  "
        d.text((tx, ly1 - 18), meta_line, font=SANS(11), fill=GRAY)
        status_tag(d, tx + d.textlength(meta_line, font=SANS(11)),
                   ly1 - 18, st["status"], SANS_B(11))

    # grid of five
    gy0, gy1 = 408, 526
    gw = (right - M - 4 * 8) / 5
    for i, st in enumerate(grid):
        x0 = M + i * (gw + 8)
        d.rectangle([x0, gy0, x0 + gw, gy1], outline=INK, width=1)
        scene = SCENES[st["scene"]](int(gw), 50)
        img.paste(scene, (int(x0), gy0))
        d.rectangle([x0, gy0, x0 + gw, gy0 + 50], outline=INK, width=1)
        tx = x0 + 6
        tw = gw - 12
        hf = SANS_B(12)
        lines = wrap(d, "%d. %s" % (st["n"], st["headline"]), hf, tw)
        yy = gy0 + 54
        for ln in lines[:3]:
            d.text((tx, yy), ln, font=hf, fill=INK)
            yy += 14
        d.text((tx, gy1 - 15), st["source"], font=SANS(10), fill=GRAY)
        status_tag(d, tx + d.textlength(st["source"], font=SANS(10)) + 4,
                   gy1 - 15, st["status"], SANS_B(10))

    # map band + date check + how sure
    my0, my1 = 534, 692
    map_box = (M, my0, M + 470, my1)
    draw_map(d, map_box, stories)
    rx = M + 482
    rw = right - rx
    d.rectangle([rx, my0, rx + rw, my1], outline=RED, width=2)
    d.text((rx + 8, my0 + 5), "DATE CHECK — LEFT OUT ON PURPOSE",
           font=SANS_B(12), fill=RED)
    df = SANS(11)
    yy = my0 + 24
    for ln in meta["date_check"]:
        for part in wrap(d, "•  " + ln, df, rw - 16):
            d.text((rx + 8, yy), part, font=df, fill=INK)
            yy += 13
    yy += 2
    d.text((rx + 8, yy), "HOW SURE ARE WE?", font=SANS_B(11), fill=INK)
    yy += 14
    for ln in meta["how_sure"]:
        d.text((rx + 8, yy), ln, font=SANS(10), fill=GRAY)
        yy += 12

    # ALSO 9-36, two columns, one line per story
    ay = 700
    d.text((M, ay), "ALSO TODAY — 9 TO 36", font=SANS_B(14), fill=RED)
    rule(d, M, right, ay + 20, 1, GRAY)
    row_h = 20
    colw2 = (right - M - 24) / 2
    hf2 = SANS_B(11)
    mf2 = SANS(10)
    short_region = {"North America": "N. America", "Middle East": "M. East",
                    "South America": "S. America"}
    for j, st in enumerate(also):
        col = j // 14
        row = j % 14
        x0 = M + col * (colw2 + 24)
        y = ay + 26 + row * row_h
        meta2 = " • %s • %s • " % (
            short_region.get(st["region"], st["region"]), st["source"])
        meta_w = d.textlength(meta2, font=mf2)
        st_w = d.textlength(st["status"], font=SANS_B(10))
        head = "%d. %s" % (st["n"], st["headline"])
        head = fit_one_line(d, head, hf2, colw2 - meta_w - st_w - 2)
        d.text((x0, y), head, font=hf2, fill=INK)
        hx = x0 + d.textlength(head, font=hf2)
        d.text((hx, y + 1), meta2, font=mf2, fill=GRAY)
        status_tag(d, hx + meta_w, y + 1, st["status"], SANS_B(10))

    # footer
    rule(d, M, right, 1006, 1, GRAY)
    foot = "All 36 stories happened or were first reported on 26 November 2026, or were still the day's news.  @dizellacapital  •  make.fun/bounty/news-image-20261126"
    d.text((M, 1010), foot, font=SANS(10), fill=GRAY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    return out


if __name__ == "__main__":
    path = build()
    size = os.path.getsize(path)
    print("wrote %s (%d bytes)" % (path, size))
    sys.exit(0 if size < 1024 * 1024 else 1)
