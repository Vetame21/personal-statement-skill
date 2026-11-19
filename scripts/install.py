#!/usr/bin/env python3
"""Install these skills for Claude Code, Codex, Gemini CLI, Qwen Code, Kimi Code, OpenCode and other
agents that read the open Agent Skills format (a folder with a SKILL.md).

    python3 scripts/install.py                      # (py on Windows) default: Claude Code + the shared ~/.agents/skills + Qwen Code
    python scripts/install.py --tools codex gemini  # only what those tools read
    python scripts/install.py --project .           # install into the current project instead of your home folder
    python scripts/install.py --list                # show where each tool looks
    python scripts/install.py --uninstall           # remove what this script installed
    python scripts/install.py --dry-run             # show what would happen

Each tool reads skills from a folder (checked November 2026; tools change, see --list):
  claude    ~/.claude/skills            Claude Code (also read by OpenCode)
  agents    ~/.agents/skills            Codex CLI, Gemini CLI, Kimi Code CLI, OpenCode, DeepSeek-TUI and other
                                        Agent Skills tools
  qwen      ~/.qwen/skills              Qwen Code
  gemini    ~/.gemini/skills            Gemini CLI (only needed if you do not use ~/.agents/skills)
  kimi      ~/.kimi-code/skills         Kimi Code CLI (only needed if you do not use ~/.agents/skills)
  opencode  ~/.config/opencode/skills   OpenCode (only needed if you do not use ~/.agents/skills)
  codex-legacy ~/.codex/skills          older Codex versions

Models such as DeepSeek, Qwen or Kimi are used through one of these tools; the skills follow the tool.

Safety: a skill folder that already exists and was not installed by this script is never overwritten
unless you pass --force. Standard library only, Python 3.9+, works on Windows, macOS and Linux.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = ".installed-by-vetame21-writing-skills"

LOCATIONS = {
    # name: (user folder relative to home, project folder relative to project, who reads it)
    "claude": (".claude/skills", ".claude/skills", "Claude Code (OpenCode also reads it)"),
    "agents": (".agents/skills", ".agents/skills", "Codex CLI, Gemini CLI, Kimi Code CLI, OpenCode, DeepSeek-TUI"),
    "qwen": (".qwen/skills", ".qwen/skills", "Qwen Code"),
    "gemini": (".gemini/skills", ".gemini/skills", "Gemini CLI"),
    "kimi": (".kimi-code/skills", ".kimi-code/skills", "Kimi Code CLI"),
    "opencode": (".config/opencode/skills", ".opencode/skills", "OpenCode"),
    "codex-legacy": (".codex/skills", ".codex/skills", "older Codex CLI versions"),
}
# Friendly tool names -> locations. Shared ~/.agents/skills first, so one copy serves many tools.
TOOLS = {
    "claude": ["claude"], "claude-code": ["claude"],
    "codex": ["agents"], "gemini": ["agents"], "gemini-cli": ["agents"],
    "kimi": ["agents"], "kimi-code": ["agents"], "opencode": ["agents"],
    "deepseek": ["agents"], "deepseek-tui": ["agents"],
    "qwen": ["qwen"], "qwen-code": ["qwen"],
    "all": ["claude", "agents", "qwen"],
}
DEFAULT = ["claude", "agents", "qwen"]


def available_skills():
    return sorted(d.name for d in (ROOT / "skills").iterdir() if (d / "SKILL.md").exists())


def resolve_locations(tools, locations):
    chosen = []
    for loc in (locations or []):
        if loc not in LOCATIONS:
            raise SystemExit(f"Unknown location '{loc}'. Choose from: {', '.join(LOCATIONS)}")
        chosen.append(loc)
    for tool in (tools or []):
        key = tool.lower()
        if key not in TOOLS:
            raise SystemExit(f"Unknown tool '{tool}'. Choose from: {', '.join(sorted(TOOLS))}")
        chosen += TOOLS[key]
    return list(dict.fromkeys(chosen or DEFAULT))


def target_dir(location: str, project):
    user_rel, project_rel, _ = LOCATIONS[location]
    return (Path(project).resolve() / project_rel) if project else (Path.home() / user_rel)


def is_ours(dest: Path) -> bool:
    """A copy carrying our marker, or a symlink that points into this repository's skills folder."""
    if dest.is_symlink():
        try:
            target = Path(os.path.realpath(dest))
            return target.parent == (ROOT / "skills").resolve()
        except OSError:
            return False
    return (dest / MARKER).exists()


def install_one(src: Path, dest: Path, link: bool, force: bool, dry: bool) -> str:
    replaced = False
    if dest.exists() or dest.is_symlink():
        if not is_ours(dest) and not force:
            return f"SKIP   {dest} (exists and was not installed by this script; use --force to replace)"
        replaced = True
        if not dry:
            if dest.is_symlink() or dest.is_file():
                dest.unlink()
            else:
                shutil.rmtree(dest)
    if dry:
        return f"WOULD  {'replace' if replaced else 'add'} ({'link' if link else 'copy'}) {dest}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    note = " (replaced the previous copy; edits made to it are gone)" if replaced and not dest.is_symlink() else ""
    if link:
        try:
            os.symlink(src, dest, target_is_directory=True)
            return f"LINK   {dest} -> {src}"
        except OSError:
            note += " (symlinks not permitted here, so this is a copy: re-run the installer after 'git pull')"
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (dest / MARKER).write_text("Installed by scripts/install.py; safe to delete with --uninstall.\n", encoding="utf-8")
    return f"COPY   {dest}{note}"


def uninstall_one(dest: Path, dry: bool) -> str:
    if not (dest.exists() or dest.is_symlink()):
        return ""
    if not is_ours(dest):
        return f"KEEP   {dest} (not installed by this script)"
    if not dry:
        if dest.is_symlink():
            dest.unlink()
        else:
            shutil.rmtree(dest)
    return f"{'WOULD  remove' if dry else 'REMOVE'} {dest}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tools", nargs="+", help="tool names, e.g. claude codex gemini qwen kimi opencode deepseek (default: all)")
    ap.add_argument("--locations", nargs="+", help=f"install folders by name: {', '.join(LOCATIONS)}")
    ap.add_argument("--skills", nargs="+", help="install only these skills (default: all)")
    ap.add_argument("--project", metavar="DIR", help="install into this project instead of your home folder")
    ap.add_argument("--link", action="store_true", help="symlink instead of copy (updates follow 'git pull')")
    ap.add_argument("--force", action="store_true", help="replace same-named skill folders not installed by this script")
    ap.add_argument("--uninstall", action="store_true", help="remove skills installed by this script")
    ap.add_argument("--dry-run", action="store_true", help="show what would happen")
    ap.add_argument("--list", action="store_true", help="list install locations and the tools that read them")
    args = ap.parse_args()

    if args.list:
        for name, (user_rel, project_rel, who) in LOCATIONS.items():
            print(f"{name:13} ~/{user_rel:28} {project_rel:26} {who}")
        return 0

    skills = available_skills()
    wanted = args.skills or skills
    unknown = sorted(set(wanted) - set(skills))
    if unknown:
        raise SystemExit(f"Unknown skill(s): {', '.join(unknown)}. Available: {', '.join(skills)}")
    locations = resolve_locations(args.tools, args.locations)
    if "claude" in locations and "agents" in locations:
        print("Note: OpenCode reads both ~/.claude/skills and ~/.agents/skills. If you use OpenCode, install to only "
              "one of them (e.g. --tools codex gemini) to avoid duplicate skill names.\n")

    failures = 0
    for loc in locations:
        base = target_dir(loc, args.project)
        print(f"[{loc}] {base}  ({LOCATIONS[loc][2]})")
        for name in wanted:
            dest = base / name
            try:
                msg = uninstall_one(dest, args.dry_run) if args.uninstall else \
                    install_one(ROOT / "skills" / name, dest, args.link, args.force, args.dry_run)
            except OSError as exc:
                msg = f"ERROR  {dest}: {exc.strerror or exc} (check permissions or close programs using it)"
                failures += 1
            if msg:
                print("  " + msg)
    if failures:
        print(f"\n{failures} item(s) failed; see ERROR lines above.")
        return 1
    if not args.uninstall and not args.dry_run:
        print("\nDone. Restart your agent (or start a new session) so it discovers the skills.")
        print("Use a skill by describing the task, or by name: /skill-name in Claude Code, $skill-name in Codex.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
