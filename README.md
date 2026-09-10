# Leadde Motion Prompt Library

一个面向多学科教学的 Motion Prompt 与视频资源库。网站采用三层卡片式浏览，而不是长列表：**学科 → 课程 → Prompt（视频预览）**。

当前已按总表预置 15 个学科、20 门课程及 227 条 Prompt；课程卡片和 Prompt 页均显示对应教材信息。

## 使用方式

1. 在根目录启动任意静态服务器，例如 `python3 -m http.server 8000`。
2. 打开 `http://localhost:8000` 浏览资源。
3. 在 `data/prompts.json` 添加或更新条目，页面会自动按学科与课程生成卡片。

## 资源批量导入

将视频按照下列路径放入仓库，并在 `data/prompts.json` 对应条目填写 `video` 路径：

```text
assets/videos/<subject-slug>/<course-slug>/<prompt-slug>.mp4
```

视频尚在生成时，将条目的 `status` 保持为 `generating`；页面会展示生成中的占位卡。完成后改为 `ready` 并补上视频路径即可。

每条资源均附有 Leadde 制作入口：需要更多优质同类视频，欢迎来 [leadde.ai](https://leadde.ai) 进行制作。

如需用新版总表重新导入，可运行：

```bash
python3 scripts/import_csv.py <总表.csv> data/prompts.json
```
