#!/usr/bin/env python3
"""
Generate plugins/ directory from skills/ source.

This script:
1. Clears the plugins/ directory
2. For each skill in skills/:
   - Creates plugin directory structure
   - Copies skill files into plugins/{name}/skills/
   - Generates .claude-plugin/plugin.json
   - Generates README.md
3. Generates root .claude-plugin/marketplace.json
"""

import json
import shutil
import subprocess
import re
from pathlib import Path

import yaml


def get_skill_timestamp(skill_path: Path) -> int:
    """Get Unix timestamp of last git commit that modified this skill."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "--", str(skill_path)],
        capture_output=True,
        text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        return int(result.stdout.strip())
    # Fallback to current time if no git history
    import time
    return int(time.time())


def extract_frontmatter(skill_md_path: Path) -> dict:
    """Extract YAML frontmatter from SKILL.md."""
    content = skill_md_path.read_text(encoding="utf-8")
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1)) or {}
    return {}


def get_repo_info() -> dict:
    """Get repository info from environment or git remote."""
    import os

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


def generate_plugin_json(name: str, description: str, version: str, repo_info: dict) -> dict:
    """Generate plugin.json manifest."""
    return {
        "name": name,
        "version": version,
        "description": description,
        "author": {
            "name": repo_info["owner"],
            "url": repo_info["url"]
        },
        "repository": repo_info["url"],
        "homepage": f"{repo_info['url']}/tree/main/plugins/{name}",
        "license": "MIT"
    }


# Category mapping based on skill characteristics
SKILL_CATEGORIES = {
    "personal-statement": "productivity",
    "harvard-cv": "productivity",
    "debate-mode": "productivity",
}


def get_category(name: str) -> str:
    """Get category for a skill, defaulting to 'productivity'."""
    return SKILL_CATEGORIES.get(name, "productivity")


def generate_readme(name: str, description: str, repo_info: dict) -> str:
    """Generate plugin README.md."""
    owner_repo = f"{repo_info['owner']}/{repo_info['repo']}"
    marketplace_name = f"{repo_info['owner']}-skills"
    return f"""# {name}

{description}

## Installation

### Claude Code / Cowork

```bash
claude plugin marketplace add {owner_repo}
claude plugin install {name}@{marketplace_name}
```

### npx skills

```bash
npx skills add {owner_repo} --skill {name}
```

---

> This plugin is auto-generated from [skills/{name}](../../skills/{name}).
"""


def copy_skill_to_plugin(skill_path: Path, plugin_path: Path, name: str):
    """Copy the whole skill into plugins/<name>/skills/<name>/.

    Claude Code discovers plugin skills at skills/<skill-name>/SKILL.md.
    The previous version copied SKILL.md straight into skills/, which
    broke discovery, and dropped any other folders (e.g. scripts/) at
    the plugin root where the skill's relative links could not reach them.
    """
    dest = plugin_path / "skills" / name
    shutil.copytree(
        skill_path,
        dest,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"),
    )


def main():
    skills_dir = Path("skills")
    plugins_dir = Path("plugins")

    repo_info = get_repo_info()

    # Clear plugins directory
    if plugins_dir.exists():
        shutil.rmtree(plugins_dir)
    plugins_dir.mkdir()

    marketplace_plugins = []

    for skill_path in sorted(skills_dir.iterdir()):
        if not skill_path.is_dir() or skill_path.name.startswith("."):
            continue

        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            continue

        # Extract metadata
        frontmatter = extract_frontmatter(skill_md)
        name = frontmatter.get("name", skill_path.name)
        # Normalize name: replace spaces with hyphens
        name = name.strip().replace(" ", "-").lower()
        description = frontmatter.get("description", "").strip()

        if not description:
            print(f"Warning: {name} has no description")
            description = f"Agent skill: {name}"

        # Get version from git timestamp
        timestamp = get_skill_timestamp(skill_path)
        version = f"0.1.{timestamp}"

        # Create plugin directory
        plugin_path = plugins_dir / name
        plugin_path.mkdir()

        # Copy skill files
        copy_skill_to_plugin(skill_path, plugin_path, name)

        # Generate plugin.json
        plugin_json_dir = plugin_path / ".claude-plugin"
        plugin_json_dir.mkdir()

        plugin_json = generate_plugin_json(name, description, version, repo_info)
        (plugin_json_dir / "plugin.json").write_text(
            json.dumps(plugin_json, indent=2) + "\n",
            encoding="utf-8"
        )

        # Generate README
        readme = generate_readme(name, description, repo_info)
        (plugin_path / "README.md").write_text(readme, encoding="utf-8")

        # Add to marketplace
        marketplace_plugins.append({
            "name": name,
            "source": f"./plugins/{name}",
            "description": description,
            "version": version,
            "category": get_category(name)
        })

        print(f"Generated plugin: {name}")

    # Generate marketplace.json
    owner_repo = f"{repo_info['owner']}/{repo_info['repo']}"
    marketplace_name = f"{repo_info['owner']}-skills"
    marketplace = {
        "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
        "name": marketplace_name,
        "description": f"A curated collection of agent skills by {repo_info['owner']}",
        "owner": {
            "name": repo_info["owner"],
            "url": repo_info["url"]
        },
        "plugins": marketplace_plugins
    }

    marketplace_dir = Path(".claude-plugin")
    marketplace_dir.mkdir(exist_ok=True)
    (marketplace_dir / "marketplace.json").write_text(
        json.dumps(marketplace, indent=2) + "\n",
        encoding="utf-8"
    )

    print(f"\nGenerated {len(marketplace_plugins)} plugins")
    print("Generated .claude-plugin/marketplace.json")


if __name__ == "__main__":
    main()
