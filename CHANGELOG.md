# Changelog

## 2.0.2 - 2026-11-19

Fixes from a second independent review.

- Python 3.9-3.11: `cv_check.py` used a backslash inside an f-string (3.12+ only); fixed. CI now tests 3.9, 3.11, 3.12 and 3.13 (interpreters provided by uv, since current GitHub runners no longer ship 3.9).
- New `shared/scripts/writing_rules.py`, copied next to every checker: one source for placeholders, the significance rule, AI-typical word lists, technical-term allowlist, first-person detection and file reading (UTF-8, BOM, UTF-16).
- humanize_check / ps_check: whole-word matching; words split into "strong" and "possible (check context)", with possible words counted only beyond two; technical phrases (robust standard errors, CPU utilization, wiring harness, landscape mode...) no longer flagged; "We..." / "My..." / "Saya..." count as the writer's voice.
- Placeholders: `[ADD DETAIL]`, `[DATA NEEDED]`, `[VERIFY]` etc. detected everywhere; `x < 3`, `<div>` and `<https://...>` no longer reported.
- cite_check: Chinese GB/T 7714 (张三[1]); intervals and years in brackets ([0, 255], [2010-2020]) ignored; huge ranges no longer hang; narrative "Santoso, Lee, and Park (2021)"; possessives; abbreviations such as WHO via "[WHO]" in the reference entry; dated references "(2021, March 5)"; Indonesian "Nama, A. 2020." style; empty reference list reported clearly.
- `--strict` now also works with `--per-sentence` and `--compare`; every checker warns on empty input.
- humanizer: assessed-work gate (asks whether it is the user's own draft and what the rules allow before polishing a thesis chapter, graded report or application essay); Turnitin bypasser wording corrected (English-only, not every language covered).
- debate-mode: the "no instant agreement" rule and the verdict format no longer contradict each other.
- SKILL.md notes explain how to run scripts from the skill folder; NACAC public summary linked; second source for the OpenAI classifier withdrawal.
- Tests: 30 (was 21).

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
