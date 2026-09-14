#!/usr/bin/env python3
"""Create or update the fixed GitHub Release asset for each video course."""
import json
import os
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict
from pathlib import Path

root = Path(__file__).resolve().parents[1]
repository = "LeaddeOpenLab/leadde-motion-prompt-library"
api_root = f"https://api.github.com/repos/{repository}"
token = os.environ.get("GITHUB_TOKEN")
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


subprocess.run(["python3", str(root / "scripts/build_course_video_bundles.py")], check=True)
items = json.loads((root / "data/prompts.json").read_text(encoding="utf-8"))
courses = OrderedDict()
for item in items:
    if item.get("status") == "ready" and item.get("video"):
        key = (item["subject"], item["course"], item["tags"][1])
        courses.setdefault(key, []).append(item)

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
    for asset in release.get("assets", []):
        if asset["name"] == asset_name:
            request("DELETE", f"{api_root}/releases/assets/{asset['id']}")
    upload_url = release["upload_url"].split("{")[0]
    archive = root / "dist/course-video-bundles" / asset_name
    url = f"{upload_url}?{urllib.parse.urlencode({'name': asset_name})}"
    request("POST", url, archive.read_bytes(), "application/zip")
    print(f"Updated {release['html_url']} with {asset_name} ({len(prompts)} videos)")
