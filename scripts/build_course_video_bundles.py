#!/usr/bin/env python3
"""Build one updateable Release ZIP for every course with ready videos."""
import json
import re
import zipfile
from collections import OrderedDict
from pathlib import Path

root = Path(__file__).resolve().parents[1]
output_dir = root / "dist/course-video-bundles"
items = json.loads((root / "data/prompts.json").read_text(encoding="utf-8"))


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


courses = OrderedDict()
for item in items:
    if item.get("status") == "ready" and item.get("video"):
        key = (item["subject"], item["course"], item["tags"][1])
        courses.setdefault(key, []).append(item)

output_dir.mkdir(parents=True, exist_ok=True)
for subject, course, course_code in courses:
    prompts = courses[(subject, course, course_code)]
    archive = output_dir / f"{slug(course_code)}-videos.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for prompt in prompts:
            video = root / prompt["video"]
            if not video.is_file():
                raise FileNotFoundError(video)
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]*\.mp4", video.name):
                raise ValueError(f"Video filename must be an English slug: {video.name}")
            bundle.write(video, video.name)
    tag = f"course-videos-{slug(subject)}-{slug(course_code)}"
    print(f"{tag}\t{archive}\t{len(prompts)} videos")
