"""Regenerate profile README — fetch xr843's merged + open PRs in external repos,
group by project, sort by (stars × PR count) descending, and emit a single table
with a Status column.

Usage:
    python scripts/update_readme.py         # uses `gh auth token` for auth
    GITHUB_TOKEN=... python scripts/update_readme.py

Sort rationale:
    Pure PR count ranks stale low-impact projects above hot flagship ones;
    pure stars hides depth. stars × count balances "how high the mountain"
    against "how many times you climbed it".
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

GITHUB_USER = "xr843"
# All xr843-owned repos are excluded from the external-contributions table.
# Matched by owner prefix, so new personal repos auto-excluded without edit.
OWN_REPO_OWNER = "xr843"

# Repos whose names start with "awesome-" are treated as curated-list
# promotional submissions (adding xr843's own projects — FoJin, Master-skill —
# to someone else's list). Those PRs advertise rather than contribute, so
# they don't belong on the profile "Open Source Contributions" table.
# If a genuinely-contributed-to repo ever happens to be named "awesome-*",
# add its owner/name to AWESOME_ALLOWLIST below.
AWESOME_ALLOWLIST: set[str] = set()

# Human-readable names for repos whose slug doesn't match their displayed name.
# Add entries here when a new project with a stylized name is contributed to.
DISPLAY_NAMES = {
    "dify": "Dify",
    "litellm": "LiteLLM",
    "gstack": "gstack",
    "cherry-studio": "Cherry Studio",
    "gradio": "Gradio",
    "haystack": "Haystack",
    "SurfSense": "SurfSense",
    "crewAI": "crewAI",
    "skills": "trailofbits/skills",
    "awesome-claude-skills": "awesome-claude-skills",
}

STATIC_HEADER = """## Hi, I'm Tim Ren

Full-stack developer focused on **Buddhist digital humanities** and **AI security** — building open-source tools that make ancient texts accessible to modern researchers, and securing LLM applications.

### Projects

- **[FoJin 佛津](https://github.com/xr843/fojin)** &nbsp; ![GitHub stars](https://img.shields.io/github/stars/xr843/fojin?style=flat-square&color=blue) — The world's encyclopedic Buddhist digital text platform. 500+ sources, 30 languages, full-text reading, AI Q&A, knowledge graph, parallel reader. FastAPI + React + Elasticsearch.

- **[Master-skill](https://github.com/xr843/Master-skill)** &nbsp; ![GitHub stars](https://img.shields.io/github/stars/xr843/Master-skill?style=flat-square) — Chinese Buddhist master AI skill generator powered by FoJin. 8 pre-built masters across Chan, Tiantai, Huayan, Pure Land, Yogācāra, Mādhyamaka, and cross-tradition. AgentSkills standard.

- **[llm-pgvector](https://github.com/xr843/llm-pgvector)** &nbsp; ![GitHub stars](https://img.shields.io/github/stars/xr843/llm-pgvector?style=flat-square) — PostgreSQL pgvector storage backend for [LLM](https://llm.datasette.io/). HNSW/IVFFlat indexes for sub-millisecond semantic search at scale. Born from [FoJin](https://fojin.app)'s 678K+ vector production workload.

- **[llm-seclint](https://github.com/xr843/llm-seclint)** &nbsp; ![GitHub stars](https://img.shields.io/github/stars/xr843/llm-seclint?style=flat-square) — Static security linter for LLM-powered applications. The Bandit for the AI era.

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


def _gh_token() -> str:
    """Use $GITHUB_TOKEN if set, else fall back to `gh auth token` (authenticated CLI)."""
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        return token
    try:
        out = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=True
        )
        return out.stdout.strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return ""


def _api_get(path: str, token: str) -> dict:
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        sys.stderr.write(f"GET {path} → HTTP {exc.code}: {exc.read().decode()[:200]}\n")
        raise


def fetch_prs(state: str, token: str) -> list[dict]:
    """Fetch PRs by xr843. state is 'is:merged' or 'is:open'.

    GitHub search caps at 1000 results across 10 pages × 100 per page;
    we paginate defensively so older merged PRs don't silently drop off.
    """
    query = f"author:{GITHUB_USER}+type:pr+{state}"
    prs: list[dict] = []

    for page in range(1, 11):  # GitHub search max = 10 pages
        data = _api_get(
            f"/search/issues?q={query}&sort=updated&order=desc"
            f"&per_page=100&page={page}",
            token,
        )
        items = data.get("items", [])
        if not items:
            break

        for item in items:
            repo_url = item.get("repository_url", "")
            repo_full = "/".join(repo_url.split("/")[-2:])
            org, repo = repo_full.split("/", 1)
            if org == OWN_REPO_OWNER:
                continue
            if repo.lower().startswith("awesome-") and repo_full not in AWESOME_ALLOWLIST:
                continue
            prs.append({
                "org": org,
                "repo": repo,
                "repo_full": repo_full,
                "number": item["number"],
                "title": item["title"],
                "url": item["html_url"],
                "updated_at": item.get("updated_at", ""),
                "status": "✅" if state == "is:merged" else "⏳",
            })

        # If we got fewer than a full page, we're done.
        if len(items) < 100:
            break

    return prs


def fetch_stars(repo_full: str, token: str, cache: dict[str, int]) -> int:
    if repo_full in cache:
        return cache[repo_full]
    try:
        data = _api_get(f"/repos/{repo_full}", token)
        stars = int(data.get("stargazers_count", 0))
    except Exception:
        stars = 0
    cache[repo_full] = stars
    return stars


def display_name(repo_slug: str) -> str:
    return DISPLAY_NAMES.get(repo_slug, repo_slug)


def build_table(prs: list[dict], stars_by_repo: dict[str, int]) -> str:
    """Group by repo; sort repos by stars × PR count desc; within repo, newest PR first."""
    by_repo: dict[str, list[dict]] = {}
    for pr in prs:
        by_repo.setdefault(pr["repo_full"], []).append(pr)

    def repo_sort_key(item):
        repo_full, pr_list = item
        stars = stars_by_repo.get(repo_full, 0)
        count = len(pr_list)
        # Primary: stars × count desc. Tiebreak: stars desc, then count desc.
        return (-(stars * count), -stars, -count, repo_full.lower())

    sorted_repos = sorted(by_repo.items(), key=repo_sort_key)

    lines = [
        "| Status | Project | Stars | PR | Description |",
        "|--------|---------|-------|----|-------------|",
    ]

    for repo_full, pr_list in sorted_repos:
        pr_list_sorted = sorted(pr_list, key=lambda p: p["number"], reverse=True)
        for i, pr in enumerate(pr_list_sorted):
            stars_cell = (
                f"![](https://img.shields.io/github/stars/{repo_full}?style=flat-square&label=)"
                if i == 0 else ""
            )
            name = display_name(pr["repo"])
            link = f"[{name}](https://github.com/{repo_full})"
            title = pr["title"]
            if len(title) > 72:
                title = title[:69] + "..."
            lines.append(
                f"| {pr['status']} | {link} | {stars_cell} | "
                f"[#{pr['number']}]({pr['url']}) | {title} |"
            )

    return "\n".join(lines)


def main() -> None:
    token = _gh_token()
    if not token:
        sys.stderr.write(
            "WARNING: no GITHUB_TOKEN and `gh auth token` unavailable — "
            "falling back to unauthenticated API (60 req/hr limit).\n"
        )

    merged = fetch_prs("is:merged", token)
    open_prs = fetch_prs("is:open", token)
    all_prs = merged + open_prs

    if not all_prs:
        sys.stderr.write("No PRs found.\n")
        return

    # Fetch stars once per unique repo
    stars_cache: dict[str, int] = {}
    for pr in all_prs:
        fetch_stars(pr["repo_full"], token, stars_cache)

    table = build_table(all_prs, stars_cache)
    readme = STATIC_HEADER + table + "\n" + STATIC_FOOTER

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    merged_n = sum(1 for p in all_prs if p["status"] == "✅")
    open_n = sum(1 for p in all_prs if p["status"] == "⏳")
    print(f"Updated README.md: {merged_n} merged + {open_n} in review "
          f"across {len(stars_cache)} projects.")


if __name__ == "__main__":
    main()
