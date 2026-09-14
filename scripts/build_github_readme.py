#!/usr/bin/env python3
"""Build a GitHub-native, no-JavaScript card navigation README."""
import html
import json
import re
from collections import OrderedDict
from pathlib import Path

root = Path(__file__).resolve().parents[1]
items = json.loads((root / "data/prompts.json").read_text(encoding="utf-8"))
repository_url = "https://github.com/LeaddeOpenLab/leadde-motion-prompt-library"

library = OrderedDict()
for item in items:
    library.setdefault(item["subject"], OrderedDict()).setdefault(item["course"], []).append(item)
course_count = sum(len(courses) for courses in library.values())

def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

def course_page(first):
    return f"catalog/{slug(first['subject'])}/{slug(first['tags'][1])}.md"

def release_tag(first):
    return f"course-videos-{slug(first['subject'])}-{slug(first['tags'][1])}"

def bundle_name(first):
    return f"{slug(first['tags'][1])}-videos.zip"

def card(subject, courses):
    count = sum(len(prompts) for prompts in courses.values())
    return f'''<td width="33%" valign="top">
  <img src="assets/subject-icons/{slug(subject)}.svg" width="54" alt="{html.escape(subject)} icon"><br>
  <a href="#{slug(subject)}"><strong>{html.escape(subject)}</strong></a><br>
  <sub>{len(courses)} courses · {count} prompts</sub>
</td>'''

def course_card(course, prompts):
    first = prompts[0]
    course_code = first["tags"][1].lower()
    page = course_page(first)
    return f'''<td width="33%" valign="top">
  <a href="{page}"><img src="assets/course-covers/{course_code}.svg" width="100%" alt="{html.escape(course)} course cover"></a><br>
  <a href="{page}"><strong>{html.escape(course)}</strong></a><br>
  <sub>{len(prompts)} prompts · {html.escape(first['textbook'])}</sub>
</td>'''

def write_course_page(subject, course, prompts):
    first = prompts[0]
    page = root / course_page(first)
    page.parent.mkdir(parents=True, exist_ok=True)
    page_lines = [
        f"# {course}",
        "",
        f"[← Back to {subject}](../../README.md#{slug(subject)})",
        "",
        f"**Textbook:** {first['textbook']}  ",
        f"**Knowledge points:** {len(prompts)}",
        "",
        "> **Turn your own idea into an animation:** [Create with Leadde →](https://leadde.ai/animation)",
        "",
    ]
    ready_prompts = [prompt for prompt in prompts if prompt.get("status") == "ready" and prompt.get("video")]
    if ready_prompts:
        bundle_url = f"{repository_url}/releases/download/{release_tag(first)}/{bundle_name(first)}"
        page_lines.extend([
            f"**Course download:** [Download all {len(ready_prompts)} videos as ZIP]({bundle_url})",
            "",
        ])
    page_lines.extend(["---", ""])
    for prompt in prompts:
        video_ready = prompt.get("status") == "ready" and prompt.get("player")
        page_lines.extend([
            f'<a id="{prompt["id"].lower()}"></a>',
            f"## {prompt['title']}",
            "",
            f"`{prompt['id']}` · " + ("**▶ Play video below**" if video_ready else "Video coming soon"),
            "",
        ])
        if video_ready:
            # A GitHub attachment URL on its own line renders as GitHub's native video player.
            download_url = f"{repository_url}/raw/refs/heads/main/{prompt['video']}"
            page_lines.extend([
                prompt["player"],
                "",
                f"[Download {Path(prompt['video']).name}]({download_url})",
                "",
            ])
        page_lines.extend([
            "> **Make this concept move:** [Create an animation with Leadde →](https://leadde.ai/animation)",
            "",
            "<details>",
            '<summary><strong>View prompt</strong></summary>',
            "",
            "```text",
            prompt["prompt"],
            "```",
            "",
            "</details>",
            "",
            f"[Back to course top](#{slug(course)})",
            "",
            "---",
            "",
        ])
    page.write_text("\n".join(page_lines), encoding="utf-8")

lines = [
    "# Leadde Motion Prompt Library",
    "",
    f"> A GitHub-native catalog of **{len(items)} English Manim prompts** across **{len(library)} disciplines** and **{course_count} courses**.",
    ">",
    "> Browse prompts and play finished videos directly with GitHub's native video player.",
    ">",
    "> **Ready to create your own? [Turn a prompt into an animation with Leadde →](https://leadde.ai/animation)**",
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
        write_course_page(subject, course, prompts)
        textbook = html.escape(prompts[0]["textbook"])
        page = course_page(prompts[0])
        lines.extend([
            f"### [{course}]({page})",
            "",
            f"**TEXTBOOK · {textbook}** &nbsp; [Open course page]({page})",
            "",
            "#### Knowledge points",
            "",
        ])
        for index, prompt in enumerate(prompts, 1):
            video_ready = prompt.get("status") == "ready" and prompt.get("player")
            marker = "▶ PLAY VIDEO + VIEW PROMPT" if video_ready else "VIEW PROMPT"
            lines.append(f"{index}. [**{html.escape(prompt['title'])}**]({page}#{prompt['id'].lower()}) · `{prompt['id']}` · {marker}")
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
    "Then set the matching entry in `data/prompts.json` to `status: ready`, populate its repository `video` path, and add its GitHub attachment URL as `player`. A standalone GitHub attachment URL renders as the native inline player.",
    "",
    "Course ZIP assets use fixed Release tags and filenames. Rebuild and replace them after adding videos with:",
    "",
    "```bash",
    "GITHUB_TOKEN=... python3 scripts/publish_course_video_releases.py",
    "```",
    "",
    "To refresh the prompt catalog from the source spreadsheet, run:",
    "",
    "```bash",
    "python3 scripts/import_csv.py <prompt-master.csv> data/prompts.json",
    "python3 scripts/build_github_readme.py",
    "```",
    "",
    "The importer preserves existing English entries, translates the title and explanatory fields of newly added Chinese rows into English, and aborts before writing if any Chinese remains in a prompt.",
])

(root / "README.md").write_text("\n".join(lines), encoding="utf-8")
print(f"Built README with {len(items)} prompt cards.")
