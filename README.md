# Leadde Motion Prompt Library

A multidisciplinary library of English Motion Prompts and future video assets. The experience uses a three-level card layout—not a long sequential list:

**Discipline → Course → Prompt with video preview**

The current catalog contains 227 English Manim prompts across 15 disciplines and 20 courses. Course cards and prompt pages display the associated textbook.

## Run locally

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Video imports

Place completed videos in this structure and set the matching catalog item's `status` to `ready` and its `video` path accordingly:

```text
assets/videos/<subject-slug>/<course-slug>/<prompt-slug>.mp4
```

Before a video is ready, leave `status` as `coming_soon`. The interface will show the video placeholder automatically.

## Update from the prompt master

The source CSV can be re-imported and translated into the English catalog with:

```bash
python3 scripts/import_csv.py <prompt-master.csv> data/prompts.json
```

Need more high-quality videos like these? Create them with [leadde.ai](https://leadde.ai).
