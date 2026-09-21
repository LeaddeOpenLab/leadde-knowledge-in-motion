#!/usr/bin/env python3
"""Render GitHub subject cards in the visual language of the video covers."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "subject-cards"
W, H = 1200, 630

FONT_BOLD = "/System/Library/Fonts/SFNS.ttf"
FONT_REGULAR = "/System/Library/Fonts/SFNS.ttf"

SUBJECTS = [
    ("computer-science", "Computer Science", "#36C5F0", "computer"),
    ("artificial-intelligence", "Artificial Intelligence", "#A78BFA", "ai"),
    ("mathematics", "Mathematics", "#4ADE80", "math"),
    ("mathematics-statistics", "Mathematics & Statistics", "#22D3EE", "stats"),
    ("physics", "Physics", "#60A5FA", "physics"),
    ("chemistry", "Chemistry", "#F59E0B", "chemistry"),
    ("life-sciences", "Life Sciences", "#34D399", "biology"),
    ("neuroscience", "Neuroscience", "#F472B6", "neuroscience"),
    ("psychology", "Psychology", "#C084FC", "psychology"),
    ("economics", "Economics", "#FBBF24", "economics"),
    ("finance", "Finance", "#2DD4BF", "finance"),
    ("political-science", "Political Science", "#FB7185", "politics"),
    ("philosophy", "Philosophy", "#A3A3A3", "philosophy"),
    ("literature", "Literature", "#F0ABFC", "literature"),
    ("astronomy", "Astronomy", "#818CF8", "astronomy"),
]


def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def rgba(value: str, alpha: int = 255) -> tuple[int, int, int, int]:
    return (*rgb(value), alpha)


def line(draw: ImageDraw.ImageDraw, points, fill, width=6):
    draw.line(points, fill=fill, width=width, joint="curve")


def glow(canvas: Image.Image, xy, color: str, blur=48, alpha=110):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(xy, fill=rgba(color, alpha))
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def node(draw, x, y, r, color, fill=(11, 20, 38, 255), width=6):
    draw.ellipse((x - r, y - r, x + r, y + r), fill=fill, outline=color, width=width)


def draw_computer(draw, accent):
    nodes = [(800, 205), (720, 310), (880, 310), (660, 430), (780, 430), (900, 430), (1020, 430)]
    for a, b in [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]:
        line(draw, [nodes[a], nodes[b]], accent, 7)
    for i, (x, y) in enumerate(nodes):
        node(draw, x, y, 25 if i < 3 else 19, accent)
    draw.rounded_rectangle((942, 165, 1060, 285), 18, outline=accent, width=7)
    for d in range(3):
        line(draw, [(970 + d * 30, 145), (970 + d * 30, 165)], accent, 5)
        line(draw, [(970 + d * 30, 285), (970 + d * 30, 305)], accent, 5)


def draw_ai(draw, accent):
    layers = [[(710, 215), (710, 315), (710, 415)], [(850, 180), (850, 260), (850, 340), (850, 420)], [(1000, 235), (1000, 335), (1000, 435)]]
    for left, right in zip(layers, layers[1:]):
        for a in left:
            for b in right:
                line(draw, [a, b], rgba("#6D7490", 130), 3)
    for group in layers:
        for x, y in group:
            node(draw, x, y, 20, accent, width=5)


def draw_math(draw, accent):
    line(draw, [(690, 445), (1070, 445)], rgba("#8993AB"), 5)
    line(draw, [(735, 500), (735, 155)], rgba("#8993AB"), 5)
    pts = []
    for x in range(735, 1061, 5):
        y = 350 - 120 * math.sin((x - 735) / 62)
        pts.append((x, y))
    line(draw, pts, accent, 9)
    draw.text((835, 205), "∫", font=ImageFont.truetype(FONT_REGULAR, 105), fill=accent)
    draw.text((930, 230), "π", font=ImageFont.truetype(FONT_REGULAR, 72), fill=rgba("#F4F7FF"))


def draw_stats(draw, accent):
    base = 465
    for i, h in enumerate([90, 150, 225, 170, 110]):
        x = 700 + i * 66
        draw.rounded_rectangle((x, base - h, x + 44, base), 8, fill=rgba(accent, 150), outline=accent, width=3)
    pts = []
    for x in range(690, 1061, 4):
        z = (x - 875) / 78
        y = 470 - 265 * math.exp(-0.5 * z * z)
        pts.append((x, y))
    line(draw, pts, rgba("#F4F7FF"), 7)


def draw_physics(draw, accent):
    cx, cy = 875, 325
    for angle in (-28, 28, 90):
        box = (cx - 205, cy - 82, cx + 205, cy + 82)
        arc = []
        for t in range(0, 361, 4):
            a = math.radians(t)
            x, y = 205 * math.cos(a), 82 * math.sin(a)
            r = math.radians(angle)
            arc.append((cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)))
        line(draw, arc, rgba("#8993AB", 180), 4)
    node(draw, cx, cy, 32, accent, fill=rgba(accent, 130), width=5)
    for x, y in [(700, 240), (1045, 270), (870, 515)]:
        node(draw, x, y, 12, rgba("#F4F7FF"), fill=accent, width=3)


def draw_chemistry(draw, accent):
    pts = [(775, 210), (885, 150), (995, 210), (995, 340), (885, 400), (775, 340)]
    line(draw, pts + [pts[0]], accent, 8)
    branch = [(995, 210), (1060, 165), (1110, 205)]
    line(draw, branch, accent, 8)
    for x, y in pts[::2] + branch[1:]:
        node(draw, x, y, 17, rgba("#F4F7FF"), fill=accent, width=3)
    line(draw, [(800, 245), (885, 197), (970, 245)], rgba("#F4F7FF", 180), 4)


def draw_biology(draw, accent):
    left, right = [], []
    for i in range(15):
        y = 145 + i * 25
        offset = 62 * math.sin(i * 0.62)
        left.append((850 + offset, y))
        right.append((930 - offset, y))
    line(draw, left, accent, 9)
    line(draw, right, rgba("#F4F7FF"), 9)
    for i in range(0, 15, 2):
        line(draw, [left[i], right[i]], rgba("#8993AB", 210), 5)


def draw_neuroscience(draw, accent):
    nodes = [(730, 220), (825, 175), (925, 220), (1015, 185), (760, 330), (870, 300), (980, 340), (715, 435), (840, 430), (955, 455), (1060, 400)]
    edges = [(0,1),(0,4),(1,2),(1,5),(2,3),(2,5),(2,6),(3,6),(4,5),(4,7),(5,6),(5,8),(6,9),(6,10),(7,8),(8,9),(9,10)]
    for a, b in edges:
        line(draw, [nodes[a], nodes[b]], rgba("#8993AB", 175), 4)
    for i, (x, y) in enumerate(nodes):
        node(draw, x, y, 13 + (i % 3) * 3, accent, fill=rgba(accent, 120), width=4)


def draw_psychology(draw, accent):
    profile = [(1040, 465), (925, 465), (890, 430), (875, 375), (825, 350), (855, 305), (850, 240), (890, 180), (960, 155), (1025, 190), (1050, 245), (1042, 305), (1080, 335), (1042, 355)]
    line(draw, profile, accent, 9)
    for x, y in [(920, 245), (985, 235), (955, 300), (1008, 340), (930, 375)]:
        node(draw, x, y, 14, rgba("#F4F7FF"), fill=accent, width=3)
    line(draw, [(920,245),(955,300),(985,235),(1008,340),(930,375),(955,300)], rgba("#8993AB"), 4)


def draw_economics(draw, accent):
    line(draw, [(700, 475), (1070, 475)], rgba("#8993AB"), 5)
    line(draw, [(720, 500), (720, 155)], rgba("#8993AB"), 5)
    line(draw, [(750, 185), (1035, 445)], accent, 9)
    line(draw, [(755, 445), (1035, 190)], rgba("#F4F7FF"), 9)
    node(draw, 895, 318, 15, accent, fill=rgba("#F4F7FF"), width=5)


def draw_finance(draw, accent):
    values = [(740, 360, 295, 405), (805, 305, 250, 355), (870, 350, 315, 430), (935, 270, 205, 325), (1000, 225, 175, 285)]
    for i, (x, top, wick_top, bottom) in enumerate(values):
        color = accent if i in (0, 1, 3, 4) else rgba("#FB7185")
        line(draw, [(x, wick_top), (x, bottom)], color, 5)
        draw.rounded_rectangle((x - 18, top, x + 18, bottom - 22), 5, fill=color)
    line(draw, [(705,440),(800,390),(875,405),(950,300),(1060,210)], rgba("#F4F7FF"), 7)


def draw_politics(draw, accent):
    draw.polygon([(720, 250), (890, 150), (1060, 250)], outline=accent, fill=rgba(accent, 80))
    line(draw, [(700, 470), (1080, 470)], accent, 10)
    line(draw, [(730, 440), (1050, 440)], rgba("#F4F7FF"), 7)
    for x in (765, 845, 925, 1005):
        draw.rounded_rectangle((x, 260, x + 38, 430), 8, outline=rgba("#F4F7FF"), width=6)
    for x, y in [(720,185),(890,115),(1060,185)]:
        node(draw, x, y, 13, accent, fill=accent, width=3)


def draw_philosophy(draw, accent):
    root = (875, 170)
    mid = [(760, 300), (990, 300)]
    leaves = [(700, 440), (815, 440), (935, 440), (1050, 440)]
    for p in mid:
        line(draw, [root, p], rgba("#F4F7FF"), 6)
    for i, p in enumerate(leaves):
        line(draw, [mid[0 if i < 2 else 1], p], accent, 6)
    node(draw, *root, 30, accent, fill=rgba(accent, 130), width=5)
    for p in mid:
        node(draw, *p, 24, rgba("#F4F7FF"), width=5)
    for p in leaves:
        node(draw, *p, 18, accent, width=5)


def draw_literature(draw, accent):
    draw.polygon([(700,210),(875,245),(875,475),(700,430)], fill=rgba(accent, 70), outline=accent)
    draw.polygon([(875,245),(1050,210),(1050,430),(875,475)], fill=rgba(accent, 105), outline=accent)
    line(draw, [(875,245),(875,475)], rgba("#F4F7FF"), 6)
    for y in (285, 330, 375):
        line(draw, [(730,y),(840,y+10)], rgba("#F4F7FF", 180), 5)
        line(draw, [(910,y+10),(1020,y)], rgba("#F4F7FF", 180), 5)


def draw_astronomy(draw, accent):
    cx, cy = 900, 320
    for rx_, ry_ in [(90,42),(170,80),(250,120)]:
        draw.ellipse((cx-rx_,cy-ry_,cx+rx_,cy+ry_), outline=rgba("#8993AB", 190), width=4)
    glow_layer = rgba(accent, 120)
    node(draw, cx, cy, 44, accent, fill=glow_layer, width=5)
    for x,y,r in [(990,345,15),(745,280,12),(1095,300,18)]:
        node(draw,x,y,r,rgba("#F4F7FF"),fill=accent,width=3)
    for a in range(0, 360, 45):
        rad=math.radians(a)
        x=675+18*math.cos(rad); y=175+18*math.sin(rad)
        line(draw, [(675,175),(x,y)], rgba("#F4F7FF"), 3)


FIGURES = {
    "computer": draw_computer,
    "ai": draw_ai,
    "math": draw_math,
    "stats": draw_stats,
    "physics": draw_physics,
    "chemistry": draw_chemistry,
    "biology": draw_biology,
    "neuroscience": draw_neuroscience,
    "psychology": draw_psychology,
    "economics": draw_economics,
    "finance": draw_finance,
    "politics": draw_politics,
    "philosophy": draw_philosophy,
    "literature": draw_literature,
    "astronomy": draw_astronomy,
}


def title_font(title: str) -> ImageFont.FreeTypeFont:
    size = 74
    if len(title) > 22:
        size = 58
    elif len(title) > 18:
        size = 64
    return ImageFont.truetype(FONT_BOLD, size)


def render(slug: str, title: str, accent: str, figure: str):
    canvas = Image.new("RGBA", (W, H), rgba("#07101F"))
    glow(canvas, (650, 20, 1230, 600), accent, blur=85, alpha=55)
    draw = ImageDraw.Draw(canvas)

    grid = rgba("#93A4C5", 24)
    for x in range(0, W + 1, 48):
        line(draw, [(x, 0), (x, H)], grid, 1)
    for y in range(0, H + 1, 48):
        line(draw, [(0, y), (W, y)], grid, 1)

    for r in (370, 300, 230):
        draw.arc((865-r, 315-r, 865+r, 315+r), 205, 332, fill=rgba(accent, 38), width=2)

    FIGURES[figure](draw, accent)

    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shade)
    for x in range(0, 760, 4):
        alpha = int(245 * (1 - x / 900) ** 1.7)
        sd.rectangle((x, 0, x + 4, H), fill=(7, 16, 31, alpha))
    canvas.alpha_composite(shade)
    draw = ImageDraw.Draw(canvas)

    eyebrow = ImageFont.truetype(FONT_BOLD, 18)
    draw.text((72, 78), "LEADDE  /  KNOWLEDGE IN MOTION", font=eyebrow, fill=rgba(accent), stroke_width=0)

    words = title.split()
    if title == "Mathematics & Statistics":
        title_lines = ["Mathematics", "& Statistics"]
    elif len(title) > 21 and len(words) > 1:
        split = max(1, len(words) // 2)
        title_lines = [" ".join(words[:split]), " ".join(words[split:])]
    else:
        title_lines = [title]
    font = title_font(title)
    y = 220 if len(title_lines) == 1 else 170
    for text in title_lines:
        draw.text((72, y), text, font=font, fill=rgba("#F4F7FF"))
        y += int(font.size * 1.05)
    draw.rounded_rectangle((72, y + 28, 230, y + 35), 4, fill=rgba(accent))

    out = OUT / f"{slug}.png"
    canvas.convert("RGB").save(out, optimize=True, quality=94)
    print(out.relative_to(ROOT))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for item in SUBJECTS:
        render(*item)


if __name__ == "__main__":
    main()
