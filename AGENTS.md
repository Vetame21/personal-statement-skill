# AGENTS.md

Guide for AI coding agents (Codex, Claude Code, Gemini CLI, Qwen Code, Kimi Code, OpenCode, ...) working **on this repository**. To *use* the skills, install them with `python scripts/install.py` (see README).

## What this repo is

Six Agent Skills (folders with a `SKILL.md`) for application and academic writing: `personal-statement`, `harvard-cv`, `thesis`, `report`, `humanizer`, `debate-mode`. The format is the open Agent Skills standard, so the same folders work in every tool that supports it.

## Layout and rules

- Edit **sources** only: `shared/references/*.md`, `shared/scripts/*.py`, `skills/<name>/SKILL.md`, `skills/<name>/references/*.md` (not `references/shared/`), `skills/<name>/scripts/*.py` (except copied shared scripts), `scripts/`, `tests/`, `testing/` (tester brief, samples, `make_pdf.py`), `README.md` outside the generated table.
- **Generated, never edit by hand:** `plugins/`, `.claude-plugin/marketplace.json`, `skills/*/references/shared/`, the shared scripts copied into `skills/*/scripts/` (`writing_rules.py`, `cite_check.py`, `text_check.py`), and the skills table in `README.md`.
- After any change run, in this order:

```bash
python scripts/build.py
```

```bash
python -m unittest discover -s tests -v
```

```bash
python scripts/build.py --check
```

- Python 3.9+, standard library only in `skills/` and `shared/scripts/` (PyYAML is used by the build only). No f-strings with backslashes inside `{}` (Python < 3.12 rejects them). Keep YAML front matter free of `": "` inside descriptions.
- Every checker imports `writing_rules.py` from its own folder; put shared word lists, regexes and file reading there, not in individual scripts.
- Add a regression test in `tests/test_scripts.py` for every bug fixed.
- Content rules: never invent facts or sources; every factual claim in a reference file gets a linked source and a check date; follow `shared/references/integrity.md`.
- Bump `VERSION` and add a `CHANGELOG.md` entry for releases. Commit as the repository owner's noreply identity; never commit personal emails.
