#!/usr/bin/env python3
"""Sync four validated AI course deliveries from the render workspace."""
import json
import re
import shutil
from pathlib import Path

SOURCE_ROOT = Path('/Users/zhoutianshuo/Desktop/leadde motion/Artificial Intelligence')
ROOT = Path(__file__).resolve().parents[1]
COURSES = (
    'Natural Language Processing',
    'Computer Vision',
    'Reinforcement Learning',
    'Generative Artificial Intelligence',
)


def normalize(value: str) -> str:
    return re.sub(r'[^a-z0-9]', '', value.lower())


items_path = ROOT / 'data/prompts.json'
items = json.loads(items_path.read_text(encoding='utf-8'))
by_key = {(item['course'], normalize(item['title'])): item for item in items}

synced = 0
for course in COURSES:
    source_dir = SOURCE_ROOT / course
    for card in sorted(source_dir.glob('[0-9][0-9]_*.md')):
        if card.name == '00_ALL_PROMPTS.md':
            continue
        text = card.read_text(encoding='utf-8')
        name_match = re.search(r'^knowledge_point:\s*["\']?(.*?)["\']?\s*$', text, re.M)
        video_match = re.search(r'^video:\s*(.*?)\s*$', text, re.M)
        prompt_match = re.search(r'```text\n(.*?)\n```', text, re.S)
        if not (name_match and video_match and prompt_match):
            raise RuntimeError(f'Invalid prompt card: {card}')
        knowledge_point = name_match.group(1)
        item = by_key[(course, normalize(knowledge_point))]
        source_video = source_dir / video_match.group(1)
        destination = ROOT / item['video']
        shutil.copy2(source_video, destination)
        item['status'] = 'ready'
        item['prompt'] = prompt_match.group(1).strip()
        synced += 1

items_path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Synced {synced} videos and prompts across four AI courses')
