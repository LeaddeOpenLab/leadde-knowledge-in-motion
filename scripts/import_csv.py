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
COURSES = {"计算机科学导论":"Introduction to Computer Science","算法导论":"Introduction to Algorithms","机器学习导论":"Introduction to Machine Learning","单变量微积分":"Single-Variable Calculus","线性代数":"Linear Algebra","应用概率":"Applied Probability","经典力学":"Classical Mechanics","电磁学":"Electromagnetism","有机化学 I":"Organic Chemistry I","生物学导论":"Introduction to Biology","神经科学导论":"Introduction to Neuroscience","心理学导论":"Introduction to Psychology","微观经济学原理":"Principles of Microeconomics","宏观经济学原理":"Principles of Macroeconomics","博弈论":"Game Theory","金融市场":"Financial Markets","政治哲学导论":"Introduction to Political Philosophy","死亡哲学":"Philosophy of Death","美国现代主义文学":"American Modernist Literature","天体物理前沿与争议":"Frontiers and Controversies in Astrophysics"}

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

def english_visual_metaphor(value, topic):
    """Replace the source's quoted Chinese concept name with its English translation."""
    return re.sub(r'[“"][^”"]*[”"]', topic, value)

def display_title(topic):
    return topic[:1].upper() + topic[1:]

def english_prompt(row, topic):
    duration = float(row["duration_seconds"])
    mechanism_end, resolution_end = duration * .73, duration * .83
    return f'''Create a {duration:g}-second silent educational animation in Manim Community Edition.

Explain “{topic}” using this visual metaphor: “{english_visual_metaphor(row["visual_metaphor"], topic)}”. Dynamically demonstrate the core formula or conclusion: {row["core_formula_or_conclusion"]}.

Use one continuous scene and one clear narrative line. Explain only this concept; do not add comparisons, extensions, or side cases. Structure the motion in three connected beats:
1. 0–3 seconds: establish the objects, input, or initial state.
2. 3–{mechanism_end:g} seconds: show at least two causally connected state changes that reveal the mechanism and progressively connect key variables or conclusions to the visual.
3. {mechanism_end:g}–{resolution_end:g} seconds: resolve the result, invariant, or central insight.

Keep introducing meaningful animation information until {resolution_end:g} seconds. Hold the final still frame for no more than {duration - resolution_end:g} seconds.

All on-screen titles, labels, and supporting annotations must be short English phrases in Arial. Use a bright, non-black background ({row["background"]}); main visual ({row["primary"]}); secondary visual ({row["secondary"]}); highlight ({row["highlight"]}); and text ({row["text"]}). Maintain strong contrast and legibility.

Use ThreeDScene for a genuinely spatial main visual: at least one core object must show volume, depth, or occlusion, and include one smooth camera move that reveals spatial structure. The 3D motion must clarify the concept rather than merely tilt a flat diagram. Render in 16:9.'''

source, destination = map(Path, sys.argv[1:3])
with source.open(encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))
missing_subjects = set(row["discipline"] for row in rows) - SUBJECTS.keys()
missing_courses = set(row["course_title_zh"] for row in rows) - COURSES.keys()
if missing_subjects or missing_courses:
    raise ValueError(f"Missing translations: {missing_subjects=}, {missing_courses=}")
topics = list(dict.fromkeys(row["knowledge_point"] for row in rows))
translations = {}
for start in range(0, len(topics), 20):
    batch = topics[start:start + 20]
    translations.update(zip(batch, translate_batch(batch)))
    time.sleep(.4)
if any(not value or any("\u4e00" <= char <= "\u9fff" for char in value) for value in translations.values()):
    raise ValueError("A topic translation was incomplete")
prompts = [{"id":row["knowledge_id"],"subject":SUBJECTS[row["discipline"]],"course":COURSES[row["course_title_zh"]],"textbook":english_textbook(row["textbook"]),"title":display_title(translations[row["knowledge_point"]]),"status":"coming_soon","video":"","tags":[row["knowledge_id"],row["course_code"],row["priority"]],"prompt":english_prompt(row, translations[row["knowledge_point"]])} for row in rows]
destination.write_text(json.dumps(prompts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Imported and translated {len(prompts)} prompts to {destination}")
