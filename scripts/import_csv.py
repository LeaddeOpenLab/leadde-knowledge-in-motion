#!/usr/bin/env python3
"""Convert the Manim prompt master CSV into the English site catalog."""
import csv
import json
import re
import sys
import time
from pathlib import Path
from subprocess import run

SUBJECTS = {"计算机科学":"Computer Science","人工智能":"Artificial Intelligence","数学":"Mathematics","数学与统计":"Mathematics & Statistics","物理学":"Physics","化学":"Chemistry","生命科学":"Life Sciences","神经科学":"Neuroscience","心理学":"Psychology","经济学":"Economics","金融学":"Finance","政治学":"Political Science","哲学":"Philosophy","文学":"Literature","天文学":"Astronomy"}
COURSES = {
    "计算机科学导论":"Introduction to Computer Science", "算法导论":"Introduction to Algorithms",
    "计算机组成原理":"Computer Organization and Architecture", "操作系统":"Operating Systems",
    "计算机网络":"Computer Networks", "数据库系统":"Database Systems", "编译原理":"Compiler Design",
    "机器学习导论":"Introduction to Machine Learning", "深度学习":"Deep Learning",
    "自然语言处理":"Natural Language Processing", "计算机视觉":"Computer Vision",
    "强化学习":"Reinforcement Learning", "生成式人工智能":"Generative Artificial Intelligence",
    "单变量微积分":"Single-Variable Calculus", "线性代数":"Linear Algebra",
    "多变量微积分":"Multivariable Calculus", "常微分方程":"Ordinary Differential Equations",
    "离散数学":"Discrete Mathematics", "抽象代数":"Abstract Algebra", "优化理论":"Optimization Theory",
    "应用概率":"Applied Probability", "经典力学":"Classical Mechanics", "电磁学":"Electromagnetism",
    "有机化学 I":"Organic Chemistry I", "生物学导论":"Introduction to Biology",
    "神经科学导论":"Introduction to Neuroscience", "心理学导论":"Introduction to Psychology",
    "微观经济学原理":"Principles of Microeconomics", "宏观经济学原理":"Principles of Macroeconomics",
    "博弈论":"Game Theory", "金融市场":"Financial Markets",
    "政治哲学导论":"Introduction to Political Philosophy", "死亡哲学":"Philosophy of Death",
    "美国现代主义文学":"American Modernist Literature", "天体物理前沿与争议":"Frontiers and Controversies in Astrophysics",
}

def english_textbook(value):
    return (value.replace("课程讲义（无指定必读教材）", "Course notes (no required textbook)")
                 .replace("课程讲义；", "Course notes; ")
                 .replace("（参考）", " (reference)")
                 .replace("按讲次指定阅读（课程无统一教材）", "Assigned readings by lecture (no single textbook)"))

def translate_batch(topics):
    result = run([
        "curl", "-L", "--max-time", "15", "-sS", "-G",
        "https://translate.googleapis.com/translate_a/single",
        "--data-urlencode", "client=gtx", "--data-urlencode", "sl=zh-CN",
        "--data-urlencode", "tl=en", "--data-urlencode", "dt=t",
        "--data-urlencode", "q=" + "\n".join(topics),
    ], capture_output=True, text=True, check=True)
    translated = "".join(part[0] for part in json.loads(result.stdout)[0]).strip()
    values = translated.split("\n")
    if len(values) != len(topics):
        raise ValueError("Translation API returned an incomplete batch")
    return values

def display_title(topic):
    return topic[:1].upper() + topic[1:]

def english_prompt(row, topic, visual_metaphor, conclusion):
    duration = float(row["duration_seconds"])
    mechanism_end, resolution_end = duration * .73, duration * .83
    return f'''Create a {duration:g}-second silent educational animation in Manim Community Edition.

Explain “{topic}” using this visual metaphor: “{visual_metaphor}”. Dynamically demonstrate the core formula or conclusion: {conclusion}.

Use one continuous scene and one clear narrative line. Explain only this concept; do not add comparisons, extensions, or side cases. Structure the motion in three connected beats:
1. 0–3 seconds: establish the objects, input, or initial state.
2. 3–{mechanism_end:g} seconds: show at least two causally connected state changes that reveal the mechanism and progressively connect key variables or conclusions to the visual.
3. {mechanism_end:g}–{resolution_end:g} seconds: resolve the result, invariant, or central insight.

Keep introducing meaningful animation information until {resolution_end:g} seconds. Hold the final still frame for no more than {duration - resolution_end:g} seconds.

All on-screen titles, labels, and supporting annotations must be short English phrases in Arial. Use a bright, non-black background ({row["background"]}); main visual ({row["primary"]}); secondary visual ({row["secondary"]}); highlight ({row["highlight"]}); and text ({row["text"]}). Maintain strong contrast and legibility.

Strict typography requirements:
- Render every complete title, label, phrase, or sentence as one native Text(...) object so every character shares one baseline.
- Never rebuild a line from separately positioned word or letter objects, and never align words by their individual bounding boxes.
- Create Arial text at a base font_size of 64, then uniformly scale the complete Text object to its final visual size; do not render explanatory text directly at a tiny font size.
- Preserve ordinary spaces inside the same Text object, set disable_ligatures=True, and do not add manual tracking, special-width spaces, or per-character offsets.

Use ThreeDScene for a genuinely spatial main visual: at least one core object must show volume, depth, or occlusion, and include one smooth camera move that reveals spatial structure. The 3D motion must clarify the concept rather than merely tilt a flat diagram. Render in 16:9.'''

source, destination = map(Path, sys.argv[1:3])
with source.open(encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))
missing_subjects = set(row["discipline"] for row in rows) - SUBJECTS.keys()
missing_courses = set(row["course_title_zh"] for row in rows) - COURSES.keys()
if missing_subjects or missing_courses:
    raise ValueError(f"Missing translations: {missing_subjects=}, {missing_courses=}")
topics = list(dict.fromkeys(row["knowledge_point"] for row in rows))
previous_items = {}
if destination.exists():
    previous_items = {item["id"]: item for item in json.loads(destination.read_text(encoding="utf-8"))}
translations = {
    row["knowledge_point"]: previous_items[row["knowledge_id"]]["title"]
    for row in rows if row["knowledge_id"] in previous_items
}
missing_topics = [topic for topic in topics if topic not in translations]
for start in range(0, len(missing_topics), 20):
    batch = missing_topics[start:start + 20]
    translations.update(zip(batch, translate_batch(batch)))
    time.sleep(.4)
if any(not value or any("\u4e00" <= char <= "\u9fff" for char in value) for value in translations.values()):
    raise ValueError("A topic translation was incomplete")
new_rows = [row for row in rows if row["knowledge_id"] not in previous_items]
free_text = []
for row in new_rows:
    free_text.extend([row["visual_metaphor"], row["core_formula_or_conclusion"]])
translated_free_text = []
for start in range(0, len(free_text), 20):
    translated_free_text.extend(translate_batch(free_text[start:start + 20]))
    time.sleep(.4)
translated_fields = {
    row["knowledge_id"]: tuple(translated_free_text[index:index + 2])
    for index, row in zip(range(0, len(translated_free_text), 2), new_rows)
}
prompts = []
for row in rows:
    if row["knowledge_id"] in previous_items:
        prompts.append(previous_items[row["knowledge_id"]])
        continue
    topic = translations[row["knowledge_point"]]
    visual_metaphor, conclusion = translated_fields[row["knowledge_id"]]
    prompts.append({"id":row["knowledge_id"],"subject":SUBJECTS[row["discipline"]],"course":COURSES[row["course_title_zh"]],"textbook":english_textbook(row["textbook"]),"title":display_title(topic),"status":"coming_soon","video":"","tags":[row["knowledge_id"],row["course_code"],row["priority"]],"prompt":english_prompt(row, topic, visual_metaphor, conclusion)})
if any(re.search(r"[\u3400-\u9fff]", item["prompt"]) for item in prompts):
    raise ValueError("Chinese text remains in a prompt; destination was not changed")
destination.write_text(json.dumps(prompts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Imported and translated {len(prompts)} prompts to {destination}")
