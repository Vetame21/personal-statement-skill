# Changelog

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
