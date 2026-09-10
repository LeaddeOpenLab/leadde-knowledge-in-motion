#!/usr/bin/env python3
"""Build a GitHub-native, no-JavaScript card navigation README."""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

root = Path(__file__).resolve().parents[1]
items = json.loads((root / "data/prompts.json").read_text(encoding="utf-8"))

library = OrderedDict()
for item in items:
    library.setdefault(item["subject"], OrderedDict()).setdefault(item["course"], []).append(item)

ICONS = {"Computer Science":"💻", "Artificial Intelligence":"✦", "Mathematics":"∑", "Mathematics & Statistics":"◒", "Physics":"⚛", "Chemistry":"⚗", "Life Sciences":"⌬", "Neuroscience":"◉", "Psychology":"◌", "Economics":"↗", "Finance":"◈", "Political Science":"⌁", "Philosophy":"◐", "Literature":"✎", "Astronomy":"✧"}

def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

def card(subject, courses):
    count = sum(len(prompts) for prompts in courses.values())
    return f'''<td width="33%" valign="top">
  <a href="#{slug(subject)}"><strong>{ICONS[subject]}<br>{html.escape(subject)}</strong><br><sub>{len(courses)} courses · {count} prompts</sub></a>
</td>'''

def course_card(course, prompts):
    first = prompts[0]
    return f'''<td width="33%" valign="top">
  <a href="#course-{first['tags'][1].lower()}"><strong>▣<br>{html.escape(course)}</strong><br><sub>{len(prompts)} prompts · {html.escape(first['textbook'])}</sub></a>
</td>'''

lines = [
    "# Leadde Motion Prompt Library",
    "",
    "> A GitHub-native catalog of **227 English Manim prompts** across **15 disciplines** and **20 courses**.",
    ">",
    "> Browse the cards below without leaving this repository. Videos are being produced and will appear in the corresponding entries later.",
    "",
    "## Browse the library",
    "",
    "<table>",
]

for start in range(0, len(library), 3):
    lines.append("<tr>")
    groups = list(library.items())[start:start + 3]
    lines.extend(card(subject, courses) for subject, courses in groups)
    lines.extend("<td></td>" for _ in range(3 - len(groups)))
    lines.append("</tr>")
lines.extend(["</table>", "", "---", ""])

for subject, courses in library.items():
    total = sum(len(prompts) for prompts in courses.values())
    lines.extend([
        f"<a id=\"{slug(subject)}\"></a>",
        f"## {subject}",
        "",
        f"**{len(courses)} courses · {total} prompts** &nbsp; [Back to cards](#browse-the-library)",
        "",
        "<table>",
    ])
    for start in range(0, len(courses), 3):
        lines.append("<tr>")
        groups = list(courses.items())[start:start + 3]
        lines.extend(course_card(course, prompts) for course, prompts in groups)
        lines.extend("<td></td>" for _ in range(3 - len(groups)))
        lines.append("</tr>")
    lines.extend(["</table>", ""])
    for course, prompts in courses.items():
        textbook = html.escape(prompts[0]["textbook"])
        lines.extend([
            f"<a id=\"course-{prompts[0]['tags'][1].lower()}\"></a>",
            f"### {course}",
            "",
            f"**TEXTBOOK · {textbook}** &nbsp; [Back to {subject} courses](#{slug(subject)})",
            "",
            "#### Knowledge points",
            "",
        ])
        for index, prompt in enumerate(prompts, 1):
            lines.extend([
                f"{index}. <details>",
                f"   <summary><strong>{html.escape(prompt['title'])}</strong> &nbsp; <code>{html.escape(prompt['id'])}</code> · VIDEO COMING SOON</summary>",
                "",
                "   ```text",
                "\n".join("   " + line if line else "" for line in prompt["prompt"].splitlines()),
                "   ```",
                "",
                "   Need a similar video? [Create it at leadde.ai](https://leadde.ai).",
                "",
                "   </details>",
                "",
            ])
        lines.append("")
    lines.extend(["---", ""])

lines.extend([
    "## Video import convention",
    "",
    "When a video is complete, place it at:",
    "",
    "```text",
    "assets/videos/<subject-slug>/<course-slug>/<prompt-slug>.mp4",
    "```",
    "",
    "Then set the matching entry in `data/prompts.json` to `status: ready` and populate its `video` path.",
    "",
    "To refresh the prompt catalog from the source spreadsheet, run:",
    "",
    "```bash",
    "python3 scripts/import_csv.py <prompt-master.csv> data/prompts.json",
    "python3 scripts/build_github_readme.py",
    "```",
])

(root / "README.md").write_text("\n".join(lines), encoding="utf-8")
print(f"Built README with {len(items)} prompt cards.")
