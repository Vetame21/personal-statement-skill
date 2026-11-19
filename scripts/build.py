#!/usr/bin/env python3
"""Build the skill collection.

    python scripts/build.py           # sync shared files, generate plugins/, update README
    python scripts/build.py --check   # fail if anything is out of date (used in CI)

What it does:
1. Copies shared/references/*.md into every skill as references/shared/,
   and the shared scripts listed in SHARED_SCRIPTS into those skills' scripts/.
   (Skills must be self-contained: they are installed one by one.)
2. Validates each skill's SKILL.md front matter (name = folder, description
   present and <= 1024 characters) and checks that relative links resolve.
3. Regenerates plugins/<name>/ (.claude-plugin/plugin.json, README.md,
   skills/<name>/) and .claude-plugin/marketplace.json, versioned from VERSION.
4. Rewrites the skills table in README.md between the SKILLS_TABLE markers.

Standard library + PyYAML.
"""

import filecmp
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SHARED_REFS = ROOT / "shared" / "references"
SHARED_SCRIPTS_DIR = ROOT / "shared" / "scripts"
SHARED_SCRIPTS = {
    "thesis": ["cite_check.py", "text_check.py", "writing_rules.py"],
    "report": ["cite_check.py", "text_check.py", "writing_rules.py"],
    "personal-statement": ["writing_rules.py"],
    "humanizer": ["writing_rules.py"],
    "harvard-cv": ["writing_rules.py"],
}
CATEGORY = "productivity"
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")
LINK = re.compile(r"\]\(((?!https?:|mailto:|#)[^)\s#]+)")
FRONT = re.compile(r"^---\s*\n(.*?)\n---", re.S)


# Fixed on purpose: forks and contributors must not rename the marketplace or
# rewrite install commands just by running the build from another remote.
OWNER = "Vetame21"
REPO = "personal-statement-skill"


def write(path: Path, text: str) -> None:
    """Write UTF-8 with LF line endings on every OS (Windows would otherwise write CRLF)."""
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def repo_info() -> dict:
    return {"owner": OWNER, "repo": REPO, "url": f"https://github.com/{OWNER}/{REPO}"}


def skills(root: Path):
    for d in sorted((root / "skills").iterdir()):
        if d.is_dir() and (d / "SKILL.md").exists():
            yield d


def front_matter(skill_dir: Path) -> dict:
    m = FRONT.match((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    if not m:
        raise SystemExit(f"{skill_dir.name}: SKILL.md has no front matter")
    return yaml.safe_load(m.group(1)) or {}


def sync_shared(root: Path) -> None:
    refs = sorted((root / "shared" / "references").glob("*.md"))
    for d in skills(root):
        target = d / "references" / "shared"
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)
        write(target / "README.md", "# Shared references\n\nCopied from `shared/references/` by `scripts/build.py`. "
            "Edit the originals there, not these copies.\n")
        for f in refs:
            shutil.copy2(f, target / f.name)
        for name in SHARED_SCRIPTS.get(d.name, []):
            (d / "scripts").mkdir(exist_ok=True)
            shutil.copy2(root / "shared" / "scripts" / name, d / "scripts" / name)


def validate(root: Path) -> list:
    errors = []
    for d in skills(root):
        fm = front_matter(d)
        if fm.get("name") != d.name:
            errors.append(f"{d.name}: front matter name is {fm.get('name')!r}")
        desc = (fm.get("description") or "").strip()
        if not desc or len(desc.encode("utf-8")) > 500:   # Codex skips skills over 500; the open standard allows 1024
            errors.append(f"{d.name}: description missing or over 500 bytes ({len(desc.encode('utf-8'))}); Codex skips it")
        for md in d.rglob("*.md"):
            text = md.read_text(encoding="utf-8")
            # ignore links inside fenced code blocks
            text = re.sub(r"```.*?```", "", text, flags=re.S)
            for link in LINK.findall(text):
                if not (md.parent / link).exists():
                    errors.append(f"{md.relative_to(root)}: broken link {link}")
    return errors


def build_plugins(root: Path, info: dict, version: str) -> None:
    plugins = root / "plugins"
    if plugins.exists():
        shutil.rmtree(plugins)
    plugins.mkdir()
    entries = []
    marketplace = f"{info['owner']}-skills"
    for d in skills(root):
        fm = front_matter(d)
        name, desc = d.name, fm["description"].strip()
        p = plugins / name
        shutil.copytree(d, p / "skills" / name, ignore=IGNORE)
        (p / ".claude-plugin").mkdir()
        write(p / ".claude-plugin" / "plugin.json", json.dumps({
            "name": name,
            "version": version,
            "description": desc,
            "author": {"name": info["owner"], "url": f"https://github.com/{info['owner']}"},
            "repository": info["url"],
            "homepage": f"{info['url']}/tree/main/skills/{name}",
            "license": "MIT",
        }, indent=2, ensure_ascii=False) + "\n")
        write(p / "README.md", f"# {name}\n\n{desc}\n\n## Install\n\n```bash\nclaude plugin marketplace add {info['owner']}/{info['repo']}\n```\n\n"
            f"```bash\nclaude plugin install {name}@{marketplace}\n```\n\n"
            f"> Generated by `scripts/build.py` from [skills/{name}](../../skills/{name}). Do not edit here.\n")
        entries.append({"name": name, "source": f"./plugins/{name}", "description": desc,
                        "version": version, "category": CATEGORY})
    (root / ".claude-plugin").mkdir(exist_ok=True)
    write(root / ".claude-plugin" / "marketplace.json", json.dumps({
        "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
        "name": marketplace,
        "description": f"Application and academic writing skills by {info['owner']}",
        "owner": {"name": info["owner"], "url": f"https://github.com/{info['owner']}"},
        "plugins": entries,
    }, indent=2, ensure_ascii=False) + "\n")


def update_readme(root: Path, info: dict) -> None:
    readme = root / "README.md"
    text = readme.read_text(encoding="utf-8")
    start, end = "<!-- SKILLS_TABLE_START -->", "<!-- SKILLS_TABLE_END -->"
    if start not in text or end not in text:
        raise SystemExit("README.md needs SKILLS_TABLE_START/END markers")
    rows = ["| Skill | Install |", "|---|---|"]
    for d in skills(root):
        rows.append(f"| [{d.name}](skills/{d.name}) | `claude plugin install {d.name}@{info['owner']}-skills` |")
    new = text[: text.index(start) + len(start)] + "\n\n" + "\n".join(rows) + "\n\n" + text[text.index(end):]
    write(readme, new)


def build_chat(root: Path) -> None:
    """chat/vetame-writing-chat.md (.txt): one file people download from GitHub for any chat AI, free or paid."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("make_bundle", root / "scripts" / "make_bundle.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = root
    mod.SHARED = sorted(p.stem for p in (root / "shared" / "references").glob("*.md"))
    with tempfile.TemporaryDirectory() as tmp:
        chat = mod.make_chat(Path(tmp))
        (root / "chat").mkdir(exist_ok=True)
        for src in (chat, chat.with_suffix(".txt")):
            shutil.copyfile(src, root / "chat" / src.name)


def build(root: Path) -> list:
    info = repo_info()
    version = (root / "VERSION").read_text().strip()
    sync_shared(root)
    errors = validate(root)
    build_plugins(root, info, version)
    update_readme(root, info)
    build_chat(root)
    return errors


def same_tree(a: Path, b: Path) -> list:
    diffs = []
    for rel in ["skills", "plugins", ".claude-plugin", "README.md", "chat"]:
        pa, pb = a / rel, b / rel
        if pa.is_file() or pb.is_file():
            if not (pa.exists() and pb.exists() and filecmp.cmp(pa, pb, shallow=False)):
                diffs.append(rel)
            continue
        cmp = filecmp.dircmp(pa, pb, ignore=["__pycache__"])
        stack = [(cmp, rel)]
        while stack:
            c, path = stack.pop()
            diffs += [f"{path}/{x}" for x in c.left_only + c.right_only + c.diff_files]
            _, mismatch, errs = filecmp.cmpfiles(c.left, c.right, c.common_files, shallow=False)
            diffs += [f"{path}/{x}" for x in mismatch + errs if f"{path}/{x}" not in diffs]
            stack += [(sub, f"{path}/{n}") for n, sub in c.subdirs.items()]
    return sorted(set(diffs))


def main() -> int:
    if "--check" in sys.argv:
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "repo"
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            errors = build(copy)
            diffs = same_tree(ROOT, copy)
        for e in errors:
            print("ERROR:", e)
        for d in diffs:
            print("OUT OF DATE:", d)
        if errors or diffs:
            print("\nRun: python scripts/build.py")
            return 1
        print("Build is up to date.")
        return 0
    errors = build(ROOT)
    for e in errors:
        print("ERROR:", e)
    print(f"Built {len(list(skills(ROOT)))} skills, version {(ROOT / 'VERSION').read_text().strip()}.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
