#!/usr/bin/env python3
"""Sync the validated calculus delivery from the render workspace into this catalog."""
import json
import shutil
from pathlib import Path

SOURCE = Path('/Users/zhoutianshuo/Desktop/leadde motion/.workbuddy/calculus-cover-manifest.json')
ROOT = Path(__file__).resolve().parents[1]
rows = json.loads(SOURCE.read_text(encoding='utf-8'))
data_path = ROOT / 'data/prompts.json'
items = json.loads(data_path.read_text(encoding='utf-8'))
by_key = {(item['course'], item['title'].lower()): item for item in items}

for row in rows:
    item = by_key[(row['course'], row['name'].lower())]
    relative_video = f"assets/videos/mathematics/{row['course_slug']}/{row['slug']}.mp4"
    destination = ROOT / relative_video
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(row['mp4'], destination)
    item['status'] = 'ready'
    item['video'] = relative_video
    item['prompt'] = row['prompt']

data_path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Synced {len(rows)} calculus videos and prompts')
