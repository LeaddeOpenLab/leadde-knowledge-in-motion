#!/usr/bin/env python3
"""Sync the validated embedded-systems and digital-electronics delivery."""

import json
import re
import shutil
from pathlib import Path


SOURCE = Path("/Users/zhoutianshuo/Desktop/leadde motion/.workbuddy/embedded-digital-16-manifest.json")
ROOT = Path(__file__).resolve().parents[1]
COURSES = {
    "Microcontroller Fundamentals": ("Embedded Systems", "ES-MCU", "C36", "Course notes (no required textbook)"),
    "Real-Time Operating Systems": ("Embedded Systems", "ES-RTOS", "C37", "Course notes (no required textbook)"),
    "Digital Logic Design": ("Digital Electronics", "DE-DLD", "C38", "Digital Design and Computer Architecture (Harris and Harris)"),
    "FPGA Fundamentals": ("Digital Electronics", "DE-FPGA", "C39", "Course notes (no required textbook)"),
}


def prompt_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"```text\n(.*?)\n```", text, re.S)
    if not match:
        raise RuntimeError(f"Prompt block missing: {path}")
    return match.group(1).strip()


rows = json.loads(SOURCE.read_text(encoding="utf-8"))
data_path = ROOT / "data/prompts.json"
items = json.loads(data_path.read_text(encoding="utf-8"))
items = [item for item in items if item["course"] not in COURSES]

course_indexes = {course: 0 for course in COURSES}
for row in rows:
    course = row["course"]
    subject, course_code, id_prefix, textbook = COURSES[course]
    course_indexes[course] += 1
    item_id = f"{id_prefix}-A{course_indexes[course]:03d}"
    subject_slug = re.sub(r"[^a-z0-9]+", "-", subject.lower()).strip("-")
    course_slug = re.sub(r"[^a-z0-9]+", "-", course.lower()).strip("-")
    video_path = f"assets/videos/{subject_slug}/{course_slug}/{row['slug']}.mp4"
    cover_path = f"assets/video-covers/{subject_slug}/{course_slug}/{row['slug']}.jpg"
    video_destination = ROOT / video_path
    cover_destination = ROOT / cover_path
    video_destination.parent.mkdir(parents=True, exist_ok=True)
    cover_destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(row["mp4"], video_destination)
    shutil.copy2(row["cover_jpg"], cover_destination)
    items.append({
        "id": item_id,
        "subject": subject,
        "course": course,
        "textbook": textbook,
        "title": row["name"],
        "seo_title": row["title"],
        "cover": cover_path,
        "status": "ready",
        "video": video_path,
        "tags": [item_id, course_code, "P0"],
        "prompt": prompt_text(Path(row["prompt_md"])),
    })

data_path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Synced {len(rows)} videos, covers, titles, and prompts across four courses")
