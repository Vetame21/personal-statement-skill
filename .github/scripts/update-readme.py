#!/usr/bin/env python3
"""Update README.md with a table of skills from the skills directory."""

import os
import re
import subprocess
from pathlib import Path

import yaml


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return {}


def get_skills(skills_dir: Path) -> list[dict]:
    """Get all skills from the skills directory."""
    skills = []

    for skill_path in skills_dir.iterdir():
        if not skill_path.is_dir():
            continue

        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            continue

        content = skill_md.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(content)

        if "description" in frontmatter:
            name = frontmatter.get("name", skill_path.name).strip().replace(" ", "-").lower()
            skills.append({
                "name": name,
                "dir_name": skill_path.name,
                "description": frontmatter["description"],
            })

    return sorted(skills, key=lambda s: s["name"].lower())


def get_repo_info() -> dict:
    """Get repository info from environment or git remote."""
    github_repository = os.environ.get("GITHUB_REPOSITORY")
    if github_repository:
        owner, repo = github_repository.split("/", 1)
        return {"owner": owner, "repo": repo, "url": f"https://github.com/{github_repository}"}

    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True
        )
        url = result.stdout.strip()
        if url.startswith("git@github.com:"):
            url = url.replace("git@github.com:", "https://github.com/")
        if url.endswith(".git"):
            url = url[:-4]
        parts = url.rstrip("/").split("/")
        return {"owner": parts[-2], "repo": parts[-1], "url": url}
    except Exception:
        return {"owner": "DiamondhunterSA", "repo": "personal-statement-skill", "url": "https://github.com/DiamondhunterSA/personal-statement-skill"}


def generate_table(skills: list[dict], repo_info: dict) -> str:
    """Generate a markdown table of skills."""
    repo_url = repo_info["url"]
    owner_repo = f"{repo_info['owner']}/{repo_info['repo']}"
    marketplace_name = f"{repo_info['owner']}-skills"

    lines = [
        "| Skill | Description |",
        "|-------|-------------|",
    ]

    for skill in skills:
        skill_link = f"[{skill['name']}]({repo_url}/tree/main/skills/{skill['dir_name']})"
        description = skill["description"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {skill_link} | {description} |")
        npx_cmd = f'```npx skills add {owner_repo} --skill {skill["name"]}```'
        lines.append(f"| | {npx_cmd} |")
        plugin_cmd = f'```claude plugin install {skill["name"]}@{marketplace_name}```'
        lines.append(f"| | {plugin_cmd} |")

    return "\n".join(lines)


def update_readme(readme_path: Path, table: str) -> None:
    """Update README.md with the skills table between <!-- SKILLS_TABLE --> markers."""
    content = readme_path.read_text(encoding="utf-8")

    start_marker = "<!-- SKILLS_TABLE_START -->"
    end_marker = "<!-- SKILLS_TABLE_END -->"

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        raise ValueError("README.md must contain <!-- SKILLS_TABLE_START --> and <!-- SKILLS_TABLE_END --> markers")

    new_content = (
        content[:start_idx + len(start_marker)]
        + "\n\n"
        + table
        + "\n\n"
        + content[end_idx:]
    )

    readme_path.write_text(new_content, encoding="utf-8")


def main():
    repo_root = Path(__file__).parent.parent.parent
    skills_dir = repo_root / "skills"
    readme_path = repo_root / "README.md"

    repo_info = get_repo_info()
    skills = get_skills(skills_dir)
    table = generate_table(skills, repo_info)
    update_readme(readme_path, table)

    print(f"Updated README.md with {len(skills)} skills")


if __name__ == "__main__":
    main()
