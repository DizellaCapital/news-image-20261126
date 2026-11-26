#!/usr/bin/env python3
"""Draw entry.png for THE THURSDAY LEDGER — 26 November 2026.

Local-only renderer (Pillow). Reads stories_20261126.json next to this file
and draws one 1024x1024 front page: giant date masthead, three illustrated
leads, a red six-number strip, five illustrated grid stories, a pinned world
map, a 28-item ALSO list, a DATE CHECK box and region bars. Deterministic:
two runs write byte-identical files.
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
PAPER = (248, 243, 230)
INK = (26, 26, 26)
RED = (179, 32, 42)
DARKRED = (140, 20, 30)
GREY = (110, 105, 95)
TAN = (222, 210, 185)
TAN_DARK = (190, 175, 145)
BLUE = (38, 84, 124)
SKY = (178, 208, 228)
NAVY = (24, 38, 64)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(draw, text, fnt, width):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, text, fnt, fill, width, leading, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, color=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def flame(draw, cx, base, s):
    draw.polygon([(cx - s, base), (cx - s * 0.45, base - s * 1.7),
                  (cx, base - s * 0.7), (cx + s * 0.45, base - s * 1.7),
                  (cx + s, base)], fill=(235, 110, 20))
    draw.polygon([(cx - s * 0.5, base), (cx - s * 0.2, base - s),
                  (cx, base - s * 0.4), (cx + s * 0.2, base - s),
                  (cx + s * 0.5, base)], fill=(245, 200, 40))


def illustration(draw, kind, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(235, 228, 210),
                   outline=TAN_DARK)
    if kind == "tanker":
        draw.rectangle([x, y, x + w, y + h * 0.62], fill=SKY)
        draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=BLUE)
        draw.rectangle([x + w * 0.18, y + h * 0.5, x + w * 0.82, y + h * 0.68],
                       fill=(52, 52, 58))
        draw.rectangle([x + w * 0.68, y + h * 0.32, x + w * 0.78, y + h * 0.5],
                       fill=(52, 52, 58))
        flame(draw, x + w * 0.35, y + h * 0.52, int(w * 0.09))
        flame(draw, x + w * 0.55, y + h * 0.52, int(w * 0.07))
        for cx, cy, r in ((0.3, 0.22, 9), (0.42, 0.15, 12), (0.55, 0.2, 8)):
            draw.ellipse([x + w * cx - r, y + h * cy - r,
                          x + w * cx + r, y + h * cy + r], fill=(120, 120, 120))
    elif kind == "refinery":
        draw.rectangle([x, y, x + w, y + h], fill=(250, 190, 120))
        for bx, bw, bh in ((0.08, 0.16, 0.62), (0.30, 0.20, 0.78),
                           (0.56, 0.14, 0.55), (0.76, 0.16, 0.68)):
            draw.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw),
                            y + h], fill=(70, 60, 55))
        flame(draw, x + w * 0.40, y + h * 0.22, int(w * 0.08))
        flame(draw, x + w * 0.84, y + h * 0.32, int(w * 0.06))
        draw.ellipse([x + w * 0.78, y + h * 0.06, x + w * 0.90, y + h * 0.18],
                     fill=(245, 220, 130))
    elif kind == "space":
        draw.rectangle([x, y, x + w, y + h], fill=NAVY)
        for sx, sy in ((0.1, 0.2), (0.25, 0.1), (0.5, 0.18), (0.7, 0.08),
                       (0.88, 0.25), (0.35, 0.3), (0.6, 0.32)):
            draw.ellipse([x + w * sx - 2, y + h * sy - 2,
                          x + w * sx + 2, y + h * sy + 2], fill=(255, 255, 255))
        draw.rectangle([x + w * 0.2, y + h * 0.45, x + w * 0.8, y + h * 0.58],
                       fill=(200, 205, 215))
        draw.ellipse([x + w * 0.44, y + h * 0.38, x + w * 0.56, y + h * 0.65],
                     fill=(150, 160, 175))
        draw.ellipse([x + w * 0.05, y + h * 0.7, x + w * 0.45, y + h * 1.15],
                     fill=(90, 130, 170))
    elif kind == "city":
        draw.rectangle([x, y, x + w, y + h], fill=(205, 200, 190))
        for bx, bw, bh in ((0.05, 0.2, 0.55), (0.3, 0.24, 0.8),
                           (0.58, 0.2, 0.62), (0.82, 0.14, 0.45)):
            draw.rectangle([x + w * bx, y + h - h * bh, x + w * (bx + bw),
                            y + h], fill=(90, 88, 84))
        draw.rectangle([x + w * 0.3, y + h * 0.2, x + w * 0.54, y + h * 0.32],
                       fill=RED)
        for wy in (0.45, 0.6, 0.75):
            for wx in (0.35, 0.45):
                draw.rectangle([x + w * wx, y + h * wy, x + w * wx + 6,
                                y + h * wy + 6], fill=(245, 220, 130))
    elif kind == "missile":
        draw.rectangle([x, y, x + w, y + h], fill=(30, 32, 48))
        draw.arc([x + w * 0.1, y + h * 0.1, x + w * 0.9, y + h * 0.9],
                 start=200, end=330, fill=(245, 200, 60), width=3)
        draw.polygon([(x + w * 0.62, y + h * 0.28), (x + w * 0.72, y + h * 0.42),
                      (x + w * 0.58, y + h * 0.45)], fill=(220, 220, 225))
        for sx, sy in ((0.15, 0.2), (0.3, 0.12), (0.85, 0.15), (0.9, 0.4)):
            draw.ellipse([x + w * sx - 2, y + h * sy - 2,
                          x + w * sx + 2, y + h * sy + 2], fill=(255, 255, 255))
        flame(draw, x + w * 0.6, y + h * 0.5, int(w * 0.05))
    elif kind == "court":
        draw.rectangle([x, y, x + w, y + h], fill=(228, 222, 205))
        draw.polygon([(x + w * 0.1, y + h * 0.3), (x + w * 0.5, y + h * 0.08),
                      (x + w * 0.9, y + h * 0.3)], fill=(120, 110, 95))
        for cx in (0.2, 0.4, 0.6, 0.8):
            draw.rectangle([x + w * cx - 7, y + h * 0.32, x + w * cx + 7,
                            y + h * 0.85], fill=(245, 242, 235),
                           outline=(120, 110, 95))
        draw.rectangle([x + w * 0.08, y + h * 0.85, x + w * 0.92, y + h * 0.92],
                       fill=(120, 110, 95))
    elif kind == "chart":
        draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        draw.line([(x + 8, y + h - 12), (x + w - 8, y + h - 12)], fill=GREY)
        pts = [(0.12, 0.3), (0.28, 0.42), (0.44, 0.38), (0.6, 0.55),
               (0.76, 0.62), (0.9, 0.78)]
        for i, (px, py) in enumerate(pts):
            col = (34, 139, 34) if i < 2 else RED
            draw.rectangle([x + w * px - 4, y + h * py, x + w * px + 4,
                            y + h * (py + 0.14)], fill=col)
            draw.line([(x + w * px, y + h * (py - 0.06)),
                       (x + w * px, y + h * (py + 0.2))], fill=col, width=2)
        draw.polygon([(x + w * 0.85, y + h * 0.82), (x + w * 0.95, y + h * 0.82),
                      (x + w * 0.9, y + h * 0.95)], fill=RED)
    elif kind == "globe":
        draw.rectangle([x, y, x + w, y + h], fill=(200, 225, 235))
        cx, cy, r = x + w * 0.5, y + h * 0.5, min(w, h) * 0.34
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 140, 90),
                     outline=(40, 90, 50), width=2)
        draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                     outline=(40, 90, 50))
        draw.line([(cx - r, cy), (cx + r, cy)], fill=(40, 90, 50), width=2)
        draw.polygon([(cx + r * 0.55, cy + r * 0.7), (cx + r * 0.75, cy + r * 0.2),
                      (cx + r * 0.9, cy + r * 0.65)], fill=(34, 139, 34))


def main():
    with open(os.path.join(HERE, "stories_20261126.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    by_n = {s["n"]: s for s in data["stories"]}
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 22
    right = W - mx

    # ---- Masthead: giant date ----
    d.text((mx, 10), "THE THURSDAY LEDGER", font=font(SANSB, 15), fill=INK)
    tag = "ONE DAY  ·  ONE PICTURE  ·  THE WHOLE WORLD"
    tw = d.textlength(tag, font=font(SANS, 13))
    d.text((right - tw, 12), tag, font=font(SANS, 13), fill=GREY)
    rule(d, mx, 34, right)
    date = data["date"]
    df = font(SERIFB, 56)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 40), date, font=df, fill=INK)
    sub = data["tagline"]
    sf = font(SERIF, 17)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 104), sub, font=sf, fill=GREY)
    rule(d, mx, 128, right, width=3)
    rule(d, mx, 133, right, width=1)

    # ---- Three illustrated leads ----
    col_w = 313
    gap = (W - 2 * mx - 3 * col_w) // 2
    y0 = 144
    for i, n in enumerate(data["leads"]):
        s = by_n[n]
        x = mx + i * (col_w + gap)
        illustration(d, s["kind"], x, y0, col_w, 100)
        y = y0 + 108
        d.text((x, y), s["kicker"], font=font(SANSB, 14), fill=RED)
        y += 20
        y = draw_text_block(d, x, y, s["headline"], font(SERIFB, 22), INK,
                            col_w, 25, max_lines=3)
        y += 2
        y = draw_text_block(d, x, y, s["deck"], font(SANS, 12), INK,
                            col_w, 15, max_lines=3)
        d.text((x, y + 2), s["source"], font=font(SANS, 10), fill=GREY)

    # ---- Red number strip ----
    ny = 404
    d.rectangle([mx, ny, right, ny + 56], fill=RED)
    cell = (right - mx) / 6
    for i, num in enumerate(data["numbers"]):
        cx = mx + i * cell
        vf = font(SANSB, 27)
        vw = d.textlength(num["value"], font=vf)
        d.text((cx + (cell - vw) / 2, ny + 4), num["value"], font=vf,
               fill=(255, 255, 255))
        draw_text_block(d, cx + 8, ny + 34, num["label"], font(SANS, 9),
                        (255, 235, 235), cell - 16, 11, max_lines=2)

    # ---- Five illustrated grid stories ----
    gw = 188
    ggap = (W - 2 * mx - 5 * gw) // 4
    gy = 472
    for i, n in enumerate(data["grid"]):
        s = by_n[n]
        x = mx + i * (gw + ggap)
        illustration(d, s["kind"], x, gy, gw, 58)
        y = gy + 64
        d.text((x, y), s["kicker"], font=font(SANSB, 11), fill=RED)
        y += 14
        y = draw_text_block(d, x, y, s["headline"], font(SERIFB, 14), INK,
                            gw, 16, max_lines=3)
        d.text((x, y + 2), s["source"], font=font(SANS, 9), fill=GREY)

    # ---- Bottom: map (left) + ALSO list (right) ----
    by = 618
    rule(d, mx, by - 6, right, width=2)
    # Map panel
    map_x0, map_y0, map_w, map_h = mx, by + 4, 478, 172
    d.text((mx, by), "WHERE IT HAPPENED — 8 PINNED STORIES",
           font=font(SANSB, 13), fill=INK)
    d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h],
                fill=(232, 226, 208), outline=TAN_DARK)
    continents = [
        [(80, 120), (300, 100), (340, 180), (280, 260), (160, 280), (70, 200)],
        [(320, 320), (420, 320), (430, 450), (360, 520), (310, 430)],
        [(480, 120), (600, 110), (620, 180), (520, 200), (470, 160)],
        [(490, 230), (620, 230), (640, 360), (560, 440), (490, 360)],
        [(630, 100), (920, 90), (940, 220), (800, 280), (650, 230)],
        [(830, 380), (900, 380), (890, 430), (840, 430)],
    ]
    for poly in continents:
        pts = [(map_x0 + px / 1000 * map_w, map_y0 + py / 600 * map_h)
               for px, py in poly]
        d.polygon(pts, fill=TAN, outline=TAN_DARK)
    for n in data["pins"]:
        s = by_n[n]
        px, py = s["pin"]
        cx = map_x0 + px / 1000 * map_w
        cy = map_y0 + py / 600 * map_h
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=RED,
                  outline=(255, 255, 255), width=2)
        nf = font(SANSB, 12)
        tw2 = d.textlength(str(n), font=nf)
        d.text((cx - tw2 / 2, cy - 8), str(n), font=nf, fill=(255, 255, 255))
    # Date check box
    dc_y = map_y0 + map_h + 10
    d.rectangle([mx, dc_y, mx + map_w, dc_y + 66], outline=RED, width=2)
    d.text((mx + 8, dc_y + 5), "DATE CHECK", font=font(SANSB, 12), fill=RED)
    draw_text_block(d, mx + 8, dc_y + 22, data["date_check"], font(SANS, 10),
                    INK, map_w - 16, 13, max_lines=3)
    # Region bars
    regions = ["Middle East", "Europe", "Asia", "Africa",
               "North America", "South America", "Oceania"]
    counts = {r: 0 for r in regions}
    for s in data["stories"]:
        counts[s["region"]] += 1
    rb_y = dc_y + 76
    d.text((mx, rb_y), "STORIES BY REGION — 36 IN ALL",
           font=font(SANSB, 11), fill=INK)
    rb_y += 16
    top = max(counts.values())
    for r in regions:
        d.text((mx, rb_y), r, font=font(SANS, 10), fill=INK)
        bx = mx + 108
        bw = int(counts[r] / top * 300)
        d.rectangle([bx, rb_y + 1, bx + bw, rb_y + 9], fill=RED)
        d.text((bx + bw + 6, rb_y), str(counts[r]), font=font(SANSB, 10),
               fill=INK)
        rb_y += 14

    # ALSO list (right panel, 2 columns x 14)
    ax = mx + map_w + 14
    aw = right - ax
    d.text((ax, by), "ALSO ON THURSDAY — 28 MORE STORIES",
           font=font(SANSB, 13), fill=INK)
    col2_w = (aw - 10) // 2
    also = [s for s in data["stories"] if s["n"] >= 9]
    for idx, s in enumerate(also):
        col = idx // 14
        row = idx % 14
        x = ax + col * (col2_w + 10)
        y = by + 24 + row * 25
        txt = "%d. %s — %s · %s" % (s["n"], s["headline"], s["region"],
                                   s["source"])
        draw_text_block(d, x, y, txt, font(SANS, 10), INK, col2_w, 12,
                        max_lines=2)

    # Footer
    fy = H - 16
    foot = data["sources_note"]
    ff = font(SANS, 9)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, fy), foot, font=ff, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG")
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
