# Vetame21 Writing Skills

**Application and academic writing skills for Claude Code and Cowork**, built from research on what admissions readers, examiners and markers actually look for, and on how AI-writing detectors such as Turnitin work.

Six skills, one shared set of rules:

| Skill | What it does |
|---|---|
| **personal-statement** | Write, upgrade and stress-test personal statements, statements of purpose, motivation letters, scholarship essays and short answers, keeping the applicant's own story and voice |
| **harvard-cv** | Create, upgrade or tailor a one-page Harvard-style CV with action-verb, result-focused bullets |
| **thesis** | Coach an undergraduate thesis (skripsi / tugas akhir / 毕业论文): topic, Bab I-V or IMRaD chapters, citations, examiner simulation, defense prep |
| **report** | Lab, programming-lab, technical, makalah, internship (KP/magang) and progress reports |
| **humanizer** | `/humanizer`: make any text sound natural and like its author, explain AI-detector flags, and protect genuine authors |
| **debate-mode** | Claude researches before agreeing and returns sourced verdicts (Yes / No / Partly / Not enough evidence) |

## What makes these different

- **Evidence over templates.** Each skill starts from the user's real material and marks anything unconfirmed `[VERIFY]` instead of inventing it.
- **Research-backed guidance.** What readers weigh (e.g. NACAC 2023 admission factors, UCAS's 2026 three-question format), what examiners reward, and how detectors decide, with sources.
- **Debate before and after writing.** Panels (Admissions Reader, Skeptic, Applicant Advocate, Tone Detector; Examiner, Supervisor, Methodologist) argue over choices and drafts, then a moderator decides.
- **Honest about AI detection.** The shared `ai-detection.md` explains perplexity, burstiness, Turnitin's thresholds (300-word minimum, scores under 20% shown as `*`, about 4% sentence-level false positives by Turnitin's own figures), bypasser detection and Turnitin Clarity, with links. The skills use this to explain flags and protect genuine authors. **They do not use evasion tricks or optimise for detector scores.** For assessed work, they first check that the text is the user's own draft and what the rules allow, and they decline requests whose goal is to pass AI-written work off as human.
- **Checker scripts** for five of the six skills (debate-mode has none), tested in CI. Python 3.9+; add `--strict` to make a script exit with code 1 when it finds issues.

## Install

```bash
claude plugin marketplace add Vetame21/personal-statement-skill
```

Then install the skills you want:

<!-- SKILLS_TABLE_START -->

| Skill | Install |
|---|---|
| [debate-mode](skills/debate-mode) | `claude plugin install debate-mode@Vetame21-skills` |
| [harvard-cv](skills/harvard-cv) | `claude plugin install harvard-cv@Vetame21-skills` |
| [humanizer](skills/humanizer) | `claude plugin install humanizer@Vetame21-skills` |
| [personal-statement](skills/personal-statement) | `claude plugin install personal-statement@Vetame21-skills` |
| [report](skills/report) | `claude plugin install report@Vetame21-skills` |
| [thesis](skills/thesis) | `claude plugin install thesis@Vetame21-skills` |

<!-- SKILLS_TABLE_END -->

Or copy a folder from `skills/` into `~/.claude/skills/` (personal) or `.claude/skills/` (project).

## Example prompts

```
Upgrade this personal statement for CityU Data Science, undergraduate + scholarship. Keep it close to the original: [paste]
```

```
/humanizer [paste text]  (it asks: humanize only, or upgrade too?)
```

```
Here is my GPTZero report, which sentences are actually weak? [paste]
```

```
Debat pakai fakta: should I mention this news in my statement?
```

```
Help me narrow my skripsi topic and plan Bab I.
```

```
Upgrade my CV to Harvard style for an AI engineering internship: [paste]
```

## How the repo is organised

```
shared/
  references/      integrity, anti-ai-tone (EN + ID), verify-and-cite, evidence-standards,
                   debate-rules, ai-detection, authorship-evidence   <- edit here
  scripts/         cite_check.py, text_check.py, writing_rules.py (shared rules for every checker)
skills/<name>/
  SKILL.md
  references/      skill-specific guides
  references/shared/   copies of shared/references (generated)
  scripts/         checkers (shared ones copied in by the build)
plugins/           generated plugin packages
scripts/build.py   sync shared files, validate, generate plugins and this table
tests/             tests for every checker script and the build
VERSION, CHANGELOG.md
```

Development:

Requires Python 3.9+.

```bash
pip install pyyaml
```

```bash
python scripts/build.py
```

```bash
python -m unittest discover -s tests -v
```

CI runs the tests and `python scripts/build.py --check` on Python 3.9, 3.11, 3.12 and 3.13 for every push and pull request. Edit `shared/` and `skills/`; never edit `plugins/` or `skills/*/references/shared/` by hand (the build overwrites them).

## Credits

The idea of a structured, stage-based personal statement skill comes from [DiamondhunterSA/personal-statement-skill](https://github.com/DiamondhunterSA/personal-statement-skill) (MIT). This collection is a full rewrite with new structure, content, research and tools; see [CREDITS.md](CREDITS.md).

## License

MIT. See [LICENSE](LICENSE). Not affiliated with Harvard, Turnitin, UCAS, NACAC, or any university named in examples.
