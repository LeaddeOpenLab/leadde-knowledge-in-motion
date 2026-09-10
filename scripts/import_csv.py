#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path

source, destination = map(Path, sys.argv[1:3])
with source.open(encoding="utf-8-sig", newline="") as file:
    rows = csv.DictReader(file)
    prompts = [
        {
            "id": row["knowledge_id"],
            "subject": row["discipline"],
            "course": row["course_title_zh"],
            "textbook": row["textbook"],
            "title": row["knowledge_point"],
            "status": "generating",
            "video": "",
            "tags": [row["chapter_scope"], row["priority"], row["course_code"]],
            "prompt": row["prompt"],
        }
        for row in rows
    ]
destination.write_text(json.dumps(prompts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Imported {len(prompts)} prompts to {destination}")
