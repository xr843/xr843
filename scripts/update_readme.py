"""Fetch merged PRs by xr843 in external repos and update profile README."""

import json
import subprocess
import sys
import base64
import urllib.request


GITHUB_USER = "xr843"
OWN_REPOS = {"xr843/fojin", "xr843/Buddhist-AI-Translator", "xr843/xr843"}

STATIC_HEADER = """## Hi, I'm Tim Ren

Full-stack developer focused on **Buddhist digital humanities** — building open-source tools that make ancient texts accessible to modern researchers.

### Projects

- **[FoJin 佛津](https://github.com/xr843/fojin)** &nbsp; ![GitHub stars](https://img.shields.io/github/stars/xr843/fojin?style=flat-square&color=blue) — The world's encyclopedic Buddhist digital text platform. 450+ sources, 30 languages, full-text reading, AI Q&A, knowledge graph, parallel reader. FastAPI + React + Elasticsearch.

- **[Buddhist AI Translator](https://github.com/xr843/Buddhist-AI-Translator)** &nbsp; ![GitHub stars](https://img.shields.io/github/stars/xr843/Buddhist-AI-Translator?style=flat-square) — AI translation for Buddhist texts across Sanskrit, Pali, Tibetan, and Classical Chinese.

### Open Source Contributions

<!-- CONTRIBUTIONS:START -->
"""

STATIC_FOOTER = """<!-- CONTRIBUTIONS:END -->

### Tech

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/-TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/-React-61DAFB?style=flat-square&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Elasticsearch](https://img.shields.io/badge/-Elasticsearch-005571?style=flat-square&logo=elasticsearch&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Redis](https://img.shields.io/badge/-Redis-DC382D?style=flat-square&logo=redis&logoColor=white)

### Get in touch

If you're interested in Buddhist studies, digital humanities, or NLP for historical texts — open an issue or start a discussion on any of my repos.
"""


def fetch_merged_prs():
    """Use GitHub API to find all merged PRs by the user in external repos."""
    url = (
        f"https://api.github.com/search/issues?"
        f"q=author:{GITHUB_USER}+type:pr+is:merged&sort=created&order=desc&per_page=100"
    )
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    import os
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    prs = []
    for item in data.get("items", []):
        repo_url = item.get("repository_url", "")
        # extract owner/repo from https://api.github.com/repos/owner/repo
        repo_full = "/".join(repo_url.split("/")[-2:])
        if repo_full in OWN_REPOS:
            continue

        org, repo = repo_full.split("/", 1)
        prs.append({
            "org": org,
            "repo": repo,
            "repo_full": repo_full,
            "number": item["number"],
            "title": item["title"],
            "url": item["html_url"],
        })

    return prs


def build_table(prs):
    """Build markdown table grouped by project, first row per project shows stars badge."""
    lines = [
        "| Project | Stars | PR | Description |",
        "|---------|-------|----|-------------|",
    ]

    seen_repos = set()
    for pr in prs:
        repo_full = pr["repo_full"]
        if repo_full not in seen_repos:
            seen_repos.add(repo_full)
            stars = f"![](https://img.shields.io/github/stars/{repo_full}?style=flat-square&label=)"
        else:
            stars = ""

        name = pr["repo"].replace(".github.io", "")
        name = {"dify": "Dify", "litellm": "LiteLLM", "gstack": "gstack"}.get(name, name)
        link = f"[{name}](https://github.com/{repo_full})"

        # Truncate long titles
        title = pr["title"]
        if len(title) > 60:
            title = title[:57] + "..."

        lines.append(
            f"| {link} | {stars} | "
            f"[#{pr['number']}]({pr['url']}) | {title} |"
        )

    return "\n".join(lines)


def main():
    prs = fetch_merged_prs()
    if not prs:
        print("No external merged PRs found.")
        return

    table = build_table(prs)
    readme = STATIC_HEADER + table + "\n" + STATIC_FOOTER

    with open("README.md", "w") as f:
        f.write(readme)

    print(f"Updated README.md with {len(prs)} contributions.")


if __name__ == "__main__":
    main()
