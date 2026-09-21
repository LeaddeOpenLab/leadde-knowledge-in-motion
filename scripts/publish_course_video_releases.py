#!/usr/bin/env python3
"""Create or update the fixed GitHub Release asset for each video course."""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict
from pathlib import Path

root = Path(__file__).resolve().parents[1]
repository = "LeaddeOpenLab/leadde-knowledge-in-motion"
api_root = f"https://api.github.com/repos/{repository}"
token = os.environ.get("GITHUB_TOKEN")
index_only = "--index-only" in sys.argv
if not token:
    raise SystemExit("Set GITHUB_TOKEN before publishing releases.")


def slug(value):
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def request(method, url, body=None, content_type="application/json"):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "Content-Type": content_type,
        "X-GitHub-Api-Version": "2022-11-28",
    }
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            data = response.read()
            return response.status, json.loads(data) if data else None
    except urllib.error.HTTPError as error:
        data = error.read()
        if error.code == 404:
            return 404, None
        message = json.loads(data).get("message", data.decode("utf-8", "replace")) if data else str(error)
        raise RuntimeError(f"GitHub API {error.code}: {message}") from error


if not index_only:
    subprocess.run(["python3", str(root / "scripts/build_course_video_bundles.py")], check=True)
items = json.loads((root / "data/prompts.json").read_text(encoding="utf-8"))
courses = OrderedDict()
for item in items:
    if item.get("status") == "ready" and item.get("video"):
        key = (item["subject"], item["course"], item["tags"][1])
        courses.setdefault(key, []).append(item)

release_index = OrderedDict()
for (subject, course, course_code), prompts in courses.items():
    tag = f"course-videos-{slug(subject)}-{slug(course_code)}"
    asset_name = f"{slug(course_code)}-videos.zip"
    status, release = request("GET", f"{api_root}/releases/tags/{urllib.parse.quote(tag)}")
    if status == 404:
        payload = json.dumps({
            "tag_name": tag,
            "target_commitish": "main",
            "name": f"{course} video bundle",
            "body": f"All currently rendered videos for {course}. This asset is replaced when the course gains new videos.",
        }).encode()
        _, release = request("POST", f"{api_root}/releases", payload)
    course_body = (
        f"All currently rendered videos for {course}. This asset is replaced when the course gains new videos.\n\n"
        "[Browse all course video downloads](https://github.com/LeaddeOpenLab/leadde-knowledge-in-motion/releases/tag/course-video-downloads)"
    )
    _, release = request("PATCH", f"{api_root}/releases/{release['id']}", json.dumps({
        "name": f"[{subject}] {course} video bundle",
        "body": course_body,
    }).encode())
    if not index_only:
        for asset in release.get("assets", []):
            if asset["name"] == asset_name:
                request("DELETE", f"{api_root}/releases/assets/{asset['id']}")
        upload_url = release["upload_url"].split("{")[0]
        archive = root / "dist/course-video-bundles" / asset_name
        url = f"{upload_url}?{urllib.parse.urlencode({'name': asset_name})}"
        request("POST", url, archive.read_bytes(), "application/zip")
    release_index.setdefault(subject, []).append((course_code, course, tag, asset_name, len(prompts)))
    print(f"Indexed {release['html_url']} ({len(prompts)} videos)")

index_lines = [
    "# Course Video Downloads",
    "",
    "Choose a discipline, then a course. Each ZIP contains all currently rendered videos for that course, with English filenames.",
]
for subject, releases in release_index.items():
    index_lines.extend(["", f"## {subject}", ""])
    for course_code, course, tag, asset_name, count in releases:
        release_url = f"https://github.com/{repository}/releases/tag/{tag}"
        download_url = f"https://github.com/{repository}/releases/download/{tag}/{asset_name}"
        index_lines.append(
            f"- **{course_code} · {course}** — [{count} videos / release]({release_url}) · [Download ZIP]({download_url})"
        )

index_tag = "course-video-downloads"
status, index_release = request("GET", f"{api_root}/releases/tags/{index_tag}")
index_payload = {
    "name": "Course Video Downloads",
    "body": "\n".join(index_lines),
    "make_latest": "true",
}
if status == 404:
    index_payload.update({"tag_name": index_tag, "target_commitish": "main"})
    _, index_release = request("POST", f"{api_root}/releases", json.dumps(index_payload).encode())
else:
    _, index_release = request("PATCH", f"{api_root}/releases/{index_release['id']}", json.dumps(index_payload).encode())
print(f"Updated download index: {index_release['html_url']}")
