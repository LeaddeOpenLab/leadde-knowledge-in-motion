#!/usr/bin/env python3
"""Sync the validated four-course delivery from the render workspace."""
import json
import shutil
from pathlib import Path

SOURCE = Path('/Users/zhoutianshuo/Desktop/leadde motion/.workbuddy/math-four-course-cover-manifest.json')
ROOT = Path(__file__).resolve().parents[1]
COURSES = {
    'Ordinary Differential Equations',
    'Discrete Mathematics',
    'Abstract Algebra',
    'Optimization Theory',
}

rows = json.loads(SOURCE.read_text(encoding='utf-8'))
data_path = ROOT / 'data/prompts.json'
items = json.loads(data_path.read_text(encoding='utf-8'))
by_key = {(item['course'], item['title'].lower()): item for item in items}

synced = 0
for row in rows:
    if row['course'] not in COURSES:
        continue
    item = by_key[(row['course'], row['name'].lower())]
    destination = ROOT / item['video']
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(row['mp4'], destination)
    item['status'] = 'ready'
    item['prompt'] = row['prompt']
    synced += 1

data_path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Synced {synced} videos and prompts across four mathematics courses')
