# Changelog

## 2.1.5 - 2026-11-19

- `scripts/make_bundle.py` builds **vetame-writing**: all six skills as one flat skill for chat apps that allow one skill per upload (the Gemini app takes a folder, not a ZIP). A router `SKILL.md` picks the right guide; reference links are rewritten to the flat names, and a test checks that every link resolves.
- `testing/GEMINI_CHAT_TEST.md` now uses the bundle and explains the folder upload.
- `vetame-writing-lite`: three skills (personal statement, humanizer, CV) in 10 files, for when the Gemini app refuses the full bundle ("Sorry, we can't save your skill"); the guide has steps to find the cause.

## 2.1.4 - 2026-11-19

- Skill descriptions shortened to about 400 characters: Codex skips skills whose description is over 500, so five of the six were not loading there. The build now fails over 500 bytes, and a test checks it.
- `testing/GEMINI_CHAT_TEST.md`: a 15-minute test for the Gemini app and other chat apps (no scripts), with a PDF through Google Docs.
- README: how to use the skills in chat apps (Gemini app, claude.ai).

## 2.1.3 - 2026-11-19

- New tester kit in `testing/`: `TESTER_BRIEF.md` tells any agent (Codex, Claude Code, Gemini CLI, ...) to install the skills, run every checker and skill on fictional samples, score them honestly, ask the tester six questions, and write a report; `make_pdf.py` turns the report into a PDF with the standard library only.
- Placeholders: leftover instructions in brackets ("[add more achievements here]", "[insert name]", "[tambahkan contoh]") are now flagged by every checker; Markdown links and numeric citations are not.
- Tests: 71 (was 68).

## 2.1.2 - 2026-11-19

Fixes from a sixth independent review.

- cite_check: references that pandoc or Word wrap over several lines are grouped into one entry (no more crash on wrapped author lists); pandoc's escaped brackets (`\[WHO\]`) are read correctly; month names such as "(Maret 2020)" are not taken for author citations. The thesis guide now suggests `pandoc --wrap=none`.
- humanizer: in `--per-sentence`, context-dependent words ("landscape", "journey") and an everyday "significant" are advisory (`~`) by default; `--register report` or `--register academic` makes "significant" without a statistical test a required fix again.
- cv_check: buzzwords are matched as whole words and technical terms ("dynamic programming", "dynamic pricing") are not flagged; "May 2024" no longer counts as a different date format.
- ps_check: words are counted as whitespace-separated tokens, like Word and application portals ("U.S.", "3.85" and URLs are one word each).
- Installer: prints how many skills were installed and skipped; when everything was skipped it says so and exits with code 1 instead of "Done"; `--project` must be an existing folder.
- harvard-cv: the AI-use policy question is now rule 6 in the numbered list; thesis trigger says "tugas akhir (TA)".
- Tests: regression tests for every item above, including a real pandoc output fixture.

## 2.1.1 - 2026-11-19

Fixes from a fifth independent review, focused on Codex users.

- Codex and multi-tool usage: README "Using the skills" (call skills with `/name` in Claude Code and Qwen Code, `$name` in Codex, or just describe the task), a Codex quick start, `python3`/`py` everywhere, a note that fact-checking needs web search turned on, and `~/.codex/skills` described as also read by Codex. Tagline no longer says Claude-only.
- Installer: a symlink counts as "ours" only if it points into this repository, so a user's own symlinked skill is never replaced or removed; permission errors print a clear ERROR line instead of a traceback; it says when a reinstall replaced an edited copy and when `--link` fell back to a copy.
- cite_check: bold reference headings (`**References**`), "Reference", "Pustaka Acuan", "Daftar Rujukan" and numbered headings; a cited year that differs from the reference list ("Smith (2021)" vs "Smith (2020)") is reported as a year mismatch.
- text_check: any padding phrase now counts (no more "Result: OK" next to listed problems).
- ps_check: plain pleading ("I hope you will accept me", "please consider my application", "mohon menerima saya") is flagged and counts as an issue.
- All checkers: a missing or unreadable file gives a one-line message, not a traceback.
- harvard-cv rule list numbering fixed.
- Tests: 61 (was 55).

## 2.1.0 - 2026-11-19

**Works beyond Claude Code.** Fixes from a fourth independent review.

- New `scripts/install.py`: installs the skills for Claude Code (`~/.claude/skills`), Codex CLI, Gemini CLI, Kimi Code CLI, OpenCode and DeepSeek-TUI (`~/.agents/skills`), and Qwen Code (`~/.qwen/skills`); `--tools`, `--project`, `--link`, `--list`, `--uninstall`, `--dry-run`; never overwrites a same-named skill it did not install.
- `AGENTS.md` for agents working on the repo (with `CLAUDE.md`, `GEMINI.md`, `QWEN.md` pointers); skill text no longer assumes Claude-only tools or paths.
- Windows: scripts print UTF-8 on any console (no more UnicodeEncodeError); `.gitattributes` and LF-only build output; CI now also runs on Windows and macOS.
- stdin (`-`) goes through the same decoder as files (BOM, UTF-16, CRLF).
- humanizer: "no concrete anchor" is advisory (`~`), not a required fix; the self-check loop no longer pushes changes to natural sentences, and the README tension with detector signals is stated openly.
- personal-statement Upgrade mode: quick intake (target, limit, AI policy) and a light quick Check; full debates only in Build mode, for new content, or on request.
- cite_check: Indonesian page forms "(2019:12)", "(Santoso, 2020: 45)"; IEEE lists numbered "1."; warnings when the chosen style finds nothing; footnote files stop after the notice; `--refs FILE` checks one chapter against a separate Daftar Pustaka.
- Sentence splitting no longer merges after units or appendix letters ("1 L.", "80 °C.", "Appendix B."), and keeps headings separate.
- cv_check recognises bold headings (`**SKILLS & INTERESTS**`).
- thesis: chapter and .docx guidance; no AI-rules question before purely mechanical checks.
- Accuracy: CV margins consistent (at least 0.75 in); unverified rubric weights labelled as such; em-dash rule labelled a rule of thumb; authorship-evidence wording corrected; Indonesian phrase list extended.
- Tests: 55 (was 42), including installer tests. Windows CI also caught doubly converted line endings (CR CR LF), now normalised.

## 2.0.3 - 2026-11-19

Fixes from a third independent review (no High findings).

- Integrity gate made consistent: personal-statement (Evidence step) and harvard-cv now ask once about the application's AI-use or authorship policy and follow it, matching the humanizer, thesis and report skills.
- cite_check (APA): the reference list stops at the next heading or an appendix (Lampiran/Appendix); multi-year groups "(Santoso, 2020, 2021)"; APA 7 "(World Health Organization [WHO], 2020)" defines WHO for later citations; "(born 2001)" ignored; "Indonesia (2020)" shown as a "possible" citation, not an error; "Reference List", "Works Cited", "Daftar Referensi" and more headings recognised; footnote styles detected and reported as unsupported.
- humanize_check: passive Methods prose and number words count as anchored; `--register report|academic` skips the anchor check; "Bab I", "Part I" and "US" no longer count as first person; "Bab"/"Part" are not names; empty AFTER text in `--compare` fails `--strict`.
- ps_check: `--lang auto|en|id` with the shared Indonesian lists plus statement-specific phrases in both languages.
- writing_rules.py is now the single source for word lists, phrases, structures, sentence splitting (abbreviation-aware), language detection, first person, number words and passive voice; text_check uses it too. "landscape" can be flagged again. Lists of three need two commas. CRLF is normalised; UTF-16 without a BOM is detected; undecodable files warn.
- Triggers: debate-mode only on explicit debate/fact-check requests; report only for academic and student technical reports.
- Privacy: context files may contain grades or research data; the skills tell users to keep them out of version control.
- Sources: NACAC's own factors pages and UCAS's official reform page linked as primary sources; thesis and harvard-cv references gained source sections; Harvard section-order claim softened to "common convention"; README sourcing wording made accurate.
- Leftover v1 stage names fixed in the personal-statement debate panel; stale docstring path fixed.
- Tests: 42 (was 30), including a YAML front-matter check for every skill.

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
