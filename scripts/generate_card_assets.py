#!/usr/bin/env python3
"""Create repository-owned SVG art for the GitHub README card navigation."""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = json.loads((ROOT / "data/prompts.json").read_text(encoding="utf-8"))
ICON_DIR = ROOT / "assets" / "subject-icons"
COVER_DIR = ROOT / "assets" / "course-covers"
ICON_DIR.mkdir(parents=True, exist_ok=True)
COVER_DIR.mkdir(parents=True, exist_ok=True)

def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

def svg(content, width, height):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none">{content}</svg>\n'''

STYLE = 'stroke="#24292f" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {
    "Computer Science": '<rect x="16" y="21" width="64" height="43" rx="4" ' + STYLE + '/><path d="M39 82h18M48 64v18" ' + STYLE + '/>',
    "Artificial Intelligence": '<path d="M48 11 55 34 78 41 55 48 48 71 41 48 18 41 41 34Z" ' + STYLE + '/><circle cx="48" cy="41" r="4" fill="#24292f"/>',
    "Mathematics": '<path d="M67 19H32l25 27-25 27h35" ' + STYLE + '/><path d="M19 28h18M19 58h18" ' + STYLE + '/>',
    "Mathematics & Statistics": '<path d="M17 68c13-39 49-39 62 0" ' + STYLE + '/><path d="M17 68h62M29 51v17M48 38v30M67 51v17" ' + STYLE + '/>',
    "Physics": '<circle cx="48" cy="46" r="7" fill="#24292f"/><ellipse cx="48" cy="46" rx="37" ry="16" ' + STYLE + '/><ellipse cx="48" cy="46" rx="37" ry="16" transform="rotate(60 48 46)" ' + STYLE + '/><ellipse cx="48" cy="46" rx="37" ry="16" transform="rotate(120 48 46)" ' + STYLE + '/>',
    "Chemistry": '<path d="M37 15h22M44 15v25L24 73a7 7 0 0 0 6 10h36a7 7 0 0 0 6-10L52 40V15" ' + STYLE + '/><path d="M31 64h34" ' + STYLE + '/>',
    "Life Sciences": '<path d="M20 73C21 36 43 17 77 17 76 51 57 73 20 73Z" ' + STYLE + '/><path d="M21 73c16-15 30-29 46-45" ' + STYLE + '/>',
    "Neuroscience": '<path d="M34 69c-18 1-23-24-7-32-3-18 22-24 29-10 15-9 32 10 18 24 7 16-12 31-26 20-4 7-12 7-14-2Z" ' + STYLE + '/><path d="M34 47h28M48 32v30" ' + STYLE + '/>',
    "Psychology": '<circle cx="48" cy="43" r="28" ' + STYLE + '/><path d="M48 25v36M30 43h36" ' + STYLE + '/><path d="M36 80h24" ' + STYLE + '/>',
    "Economics": '<path d="M18 72 42 49l14 12 23-34" ' + STYLE + '/><path d="M63 27h16v16" ' + STYLE + '/><path d="M18 80h62" ' + STYLE + '/>',
    "Finance": '<path d="M48 14 76 42 48 70 20 42Z" ' + STYLE + '/><path d="M48 28v28M39 36c3-6 15-6 18 0 3 7-18 6-18 14 3 6 15 6 18 0" ' + STYLE + '/>',
    "Political Science": '<path d="M24 76V24h48v52M16 76h64M35 35h26M35 47h26M35 59h26" ' + STYLE + '/>',
    "Philosophy": '<path d="M48 15c18 0 31 13 31 31S66 77 48 77 17 64 17 46 30 15 48 15Z" ' + STYLE + '/><path d="M48 15v62" ' + STYLE + '/>',
    "Literature": '<path d="M20 20c13-5 27-3 28 7v50c-1-10-15-12-28-7V20ZM76 20c-13-5-27-3-28 7v50c1-10 15-12 28-7V20Z" ' + STYLE + '/><path d="M48 27v50" ' + STYLE + '/>',
    "Astronomy": '<circle cx="48" cy="45" r="24" ' + STYLE + '/><path d="M48 10v11M48 69v11M13 45h11M72 45h11M22 19l8 8M66 63l8 8M74 19l-8 8M30 63l-8 8" ' + STYLE + '/>',
}

for subject, drawing in ICONS.items():
    (ICON_DIR / f"{slug(subject)}.svg").write_text(svg(f'<g {STYLE}>{drawing}</g>', 96, 96), encoding="utf-8")

library = OrderedDict()
for item in ITEMS:
    library.setdefault(item["course"], item)

PALETTES = [
    ("#1258C8", "#DDE9FF"), ("#6D3FCC", "#F0E8FF"), ("#008B83", "#DFFFFA"),
    ("#C54C2E", "#FFE9E0"), ("#155E9B", "#E1F3FF"), ("#8A3F86", "#FFE9FB"),
    ("#1D7461", "#E4FFF7"), ("#9E5B13", "#FFF1DD"), ("#425CA8", "#E9EEFF"),
    ("#B3415E", "#FFE8EF"), ("#166C9A", "#E2F6FF"), ("#4E6678", "#E9F2F8"),
]

def title_lines(title):
    words, lines, current = title.split(), [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > 25:
            lines.append(current)
            current = word
        else:
            current = candidate
    lines.append(current)
    return lines

for index, (course, first) in enumerate(library.items()):
    color, pale = PALETTES[index % len(PALETTES)]
    lines = title_lines(course)
    start = 280 - (len(lines) - 1) * 47
    text = "".join(
        f'<text x="600" y="{start + line_index * 94}" text-anchor="middle" fill="white" font-family="Arial, Helvetica, sans-serif" font-size="68" font-weight="700">{html.escape(line)}</text>'
        for line_index, line in enumerate(lines)
    )
    art = f'''<rect width="1200" height="630" rx="28" fill="{color}"/>
<circle cx="108" cy="100" r="128" stroke="{pale}" stroke-width="7" opacity=".7"/>
<circle cx="1090" cy="542" r="166" stroke="{pale}" stroke-width="7" opacity=".7"/>
<path d="M0 536C137 450 186 558 319 488M881 114c104-85 177 20 319-72" stroke="{pale}" stroke-width="7" stroke-linecap="round" opacity=".7"/>
<path d="M92 152h54M106 138v28M1026 454h54M1040 440v28" stroke="{pale}" stroke-width="7" stroke-linecap="round" opacity=".7"/>
{text}'''
    code = first["tags"][1].lower()
    cover = COVER_DIR / f"{code}.svg"
    if not cover.exists():
        cover.write_text(svg(art, 1200, 630), encoding="utf-8")

print(f"Created {len(ICONS)} subject icons and {len(library)} course covers.")
