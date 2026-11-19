# Changelog

## 2.0.1 - 2026-11-19

Fixes from an independent fresh-eyes review.

- cite_check: IEEE ranges `[2]-[4]` and `[5-6]` work; brackets attached to words (`arr[7]`) and code spans/blocks are ignored; APA handles corporate authors, lowercase particles (van, de), three or more authors, years before 1900, page numbers, and narrative citations such as "Kurniawan dan Sari (2018)".
- text_check and humanize_check share one rule: "signifikan/significant" is fine only with a test result in the same sentence.
- cv_check: argparse (`--help` works); Coursework, GPA and Skills bullets no longer count against the "bullets with numbers" ratio or repeated verbs.
- All checkers accept `--strict` (exit code 1 when issues are found).
- Sources: linked sources with check dates in ai-detection, integrity, authorship-evidence, what-readers-want and regional; the unsourced "essay weight doubled" claim replaced with sourced figures.
- README: integrity wording now matches behaviour; Python 3.9+ documented; which files are generated; checker count corrected.
- build.py: owner/repo fixed, so forks do not rename the marketplace.
- Repo hygiene: `.gitignore`, committed `__pycache__` removed; thesis links to the shared tone list instead of copying it; harvard-cv points to the shared checklist; script-path notes in SKILL.md files.

## 2.0.0 - 2026-11-18

Full rewrite as **Vetame21 Writing Skills**.

- personal-statement: new workflow (Evidence → Angle → Draft → Stress-test → Finalise); new references `what-readers-want.md`, `formats.md`, `fields.md`, `openings-and-closings.md` replace the original frameworks, discipline, examples and templates files.
- New `shared/` foundation copied into every skill: integrity, anti-AI tone (EN + ID), verify-and-cite, evidence standards, debate rules, AI detection (Turnitin thresholds, bypasser detection, Clarity), authorship evidence.
- humanizer: detector triage moved to `detector-reports.md`; detection research now shared.
- thesis: integrity guidance merged into the shared rules.
- Build: `scripts/build.py` replaces the old generator and README scripts; plugin versions come from `VERSION` instead of commit timestamps (no more bot commits).
- Tests for all checker scripts and the build; CI runs tests and `build.py --check`.

## 1.x

Upgrades on top of the original fork: debate-mode, harvard-cv, thesis, report and humanizer skills; plugin layout fix; panel debates; detector handling.
