# Application Writing Skills for Claude

Agent skills for [Claude Code](https://code.claude.com/docs) and Cowork that help with university, scholarship and job applications:

| Skill | What it does |
|---|---|
| **personal-statement** | Write, upgrade or polish a personal statement / SOP / motivation letter / scholarship essay, keep it close to the applicant's own draft, add verified current facts, and prepare interview or recorded-video answers |
| **harvard-cv** | Create, upgrade or tailor a one-page Harvard-style CV with action-verb, result-focused bullets |
| **debate-mode** | Claude does not just agree: it researches the claim first and returns a sourced verdict (Yes / No / Partly / Not enough evidence) |
| **thesis** | Coach an undergraduate thesis (skripsi / tugas akhir / 毕业论文): topic and proposal, Bab I-V or IMRaD chapters, literature and citations, examiner-simulation debate, defense (sidang) prep, AI-use and similarity rules |
| **report** | Lab reports, programming lab reports, technical/project reports, makalah, internship (KP/magang) and progress reports |
| **humanizer** | `/humanizer`: make any text (personal statement, report, thesis, CV, email) sound natural and like its author; diagnoses AI-sounding patterns, asks whether to upgrade the content too, keeps every fact and citation |

> Based on [DiamondhunterSA/personal-statement-skill](https://github.com/DiamondhunterSA/personal-statement-skill) (MIT). See [CREDITS.md](CREDITS.md) for what is original and what changed.

## Install

### Claude Plugin Marketplace (Claude Code / Cowork)

```bash
claude plugin marketplace add Vetame21/personal-statement-skill
```

```bash
claude plugin install personal-statement@Vetame21-skills
```

```bash
claude plugin install harvard-cv@Vetame21-skills
```

```bash
claude plugin install debate-mode@Vetame21-skills
```

```bash
claude plugin install thesis@Vetame21-skills
```

```bash
claude plugin install report@Vetame21-skills
```

```bash
claude plugin install humanizer@Vetame21-skills
```

While the repository is private, the marketplace commands need a GitHub login that can read it.

### npx skills (CLI)

```bash
npx skills add Vetame21/personal-statement-skill --skill personal-statement
```

### Manual

Copy a folder from `skills/` into `~/.claude/skills/` (personal) or `.claude/skills/` (project).

## Skills

<!-- SKILLS_TABLE_START -->

| Skill | Description |
|-------|-------------|
| [debate-mode](https://github.com/Vetame21/personal-statement-skill/tree/main/skills/debate-mode) | Evidence-first debate. Instead of agreeing, Claude researches a claim or proposal and returns a sourced verdict (Yes / No / Partly / Not enough evidence) before giving a recommendation. Use when the user asks Claude to debate, argue, challenge them, push back, fact-check, "debat pakai fakta", "jangan iya-iya aja", "don't just agree", "prove it", or asks whether an idea, claim, or edit (for example to a personal statement or CV) is right or relevant. |
| | ```npx skills add Vetame21/personal-statement-skill --skill debate-mode``` |
| | ```claude plugin install debate-mode@Vetame21-skills``` |
| [harvard-cv](https://github.com/Vetame21/personal-statement-skill/tree/main/skills/harvard-cv) | Create, upgrade, or tailor a CV/resume in the Harvard style (one page, reverse chronological, Education → Experience → Leadership & Activities → Skills & Interests, action-verb bullets with results). Use when the user asks to make, fix, review, upgrade, or tailor a CV or resume, mentions "Harvard CV", "Harvard resume", "Harvard format", or needs a CV to go with a university, scholarship, internship, or job application. |
| | ```npx skills add Vetame21/personal-statement-skill --skill harvard-cv``` |
| | ```claude plugin install harvard-cv@Vetame21-skills``` |
| [humanizer](https://github.com/Vetame21/personal-statement-skill/tree/main/skills/humanizer) | Make any piece of writing sound natural and like its author instead of machine-written - personal statements, reports, thesis chapters, CVs, cover letters, emails, posts - in English or Indonesian. Diagnoses AI-sounding words, rhythm and structure, asks whether to also upgrade the content, then rewrites at the lightest touch while keeping every fact, number and citation. Use when the user says humanize, humanizer, make it sound human or natural, sounds like AI, kayak AI, kurang natural, terlalu kaku, pastes an AI-detector report (GPTZero, Turnitin, ZeroGPT), or runs /humanizer. |
| | ```npx skills add Vetame21/personal-statement-skill --skill humanizer``` |
| | ```claude plugin install humanizer@Vetame21-skills``` |
| [personal-statement](https://github.com/Vetame21/personal-statement-skill/tree/main/skills/personal-statement) | Write, upgrade, and polish personal statements, statements of purpose, motivation letters, scholarship essays, application essays, self-introductions, and cover letters, for high school/undergraduate, graduate, PhD, scholarship, and job applications. Use when the user shares a PS draft to review or upgrade, asks to write one from scratch, asks to keep a draft close to the original while improving it, wants current facts or news worked into a statement, wants the statement debated or stress-tested by a reviewer panel, or wants to prepare video/interview answers from a statement. |
| | ```npx skills add Vetame21/personal-statement-skill --skill personal-statement``` |
| | ```claude plugin install personal-statement@Vetame21-skills``` |
| [report](https://github.com/Vetame21/personal-statement-skill/tree/main/skills/report) | Plan, write, review and polish academic and technical reports - lab reports (laporan praktikum), programming lab and assignment reports, technical/project reports, makalah, internship reports (laporan magang / kerja praktik / KP), and research or progress reports - in Indonesian or English. Use when the user asks to write, structure, fix, shorten, or review a report, mentions laporan, lab report, praktikum, makalah, KP, magang, project report, or wants a report checked for structure, citations, or AI-sounding language. |
| | ```npx skills add Vetame21/personal-statement-skill --skill report``` |
| | ```claude plugin install report@Vetame21-skills``` |
| [thesis](https://github.com/Vetame21/personal-statement-skill/tree/main/skills/thesis) | Coach a student through an undergraduate thesis (skripsi, tugas akhir, bachelor's thesis, graduation project / 毕业论文), from choosing a topic, writing the proposal, structuring chapters (Indonesian Bab I-V or international IMRaD), literature review, methodology, results and discussion, citations, similarity and AI-use rules, and preparing for the defense (sidang). Use when the user mentions skripsi, tugas akhir, TA, thesis, proposal penelitian, seminar proposal, sidang, bab 1/2/3/4/5, latar belakang, rumusan masalah, tinjauan pustaka, metodologi, or wants a thesis chapter reviewed, debated, or improved. |
| | ```npx skills add Vetame21/personal-statement-skill --skill thesis``` |
| | ```claude plugin install thesis@Vetame21-skills``` |

<!-- SKILLS_TABLE_END -->

## What each skill does

### personal-statement

| Mode | When |
|---|---|
| **Upgrade** | You have a draft and want it better without losing its story or voice |
| **Full** | Start from scratch: Gather → Plan → Write → Polish → Iterate → Interview prep |
| **Review only** | Feedback, no rewrite |
| **Debate** | Challenge a choice before it goes into the statement |
| **Interview prep** | Live interview notes, or a story bank for pre-recorded video interviews |

Built-in rules:

- **Panel debate, twice**: before writing, a panel (Admissions Reader, Skeptic, Applicant Advocate, Tone Detector) debates the plan as motions; after the draft, it attacks the text, rebuts each other, and a moderator gives verdicts and 1-5 scores ([debate-panel.md](skills/personal-statement/references/debate-panel.md)).
- **No silent fabrication**: any invented detail is marked `[VERIFY: ...]` and listed under "Check before submitting".
- **Current facts must be searched and cited**, with vendor reports and conflicting numbers flagged.
- **Anti-AI tone**: word, structure and content red flags ([anti-ai-tone.md](skills/personal-statement/references/anti-ai-tone.md)).
- **Undergraduate and scholarship guidance**, two programs (1st/2nd choice) in one statement, and regional conventions (Hong Kong, UK UCAS, US Common App, Europe, Asia).
- `scripts/ps_check.py`: word/character counts, sentence-length spread, em-dash density, red-flag phrases, leftover placeholders.

```bash
python skills/personal-statement/scripts/ps_check.py statement.txt --limit-words 500
```

### harvard-cv

- Modes: **Create**, **Upgrade** (audit table → rewrite → before/after), **Tailor** (map to a program or job), **Review only**.
- Layout variants for secondary school students, university students and experienced applicants.
- Bullet formula: *action verb + what + how + result*; no invented numbers.
- `scripts/cv_check.py`: weak openers, pronouns, buzzwords, bullets without results, repeated verbs, mixed date formats, length.

```bash
python skills/harvard-cv/scripts/cv_check.py cv.md
```

### debate-mode

1. Restates your message as checkable claims (fact, causal, relevance, preference).
2. Researches them with web search (deeper research for recent or high-stakes claims).
3. Returns a verdict per claim with confidence and sources, the strongest counter-argument, and a recommendation.
4. Changes its verdict only for new evidence or a better argument, not for insistence.

Example prompts:

```
Debat pakai fakta: AI fraud news itu nggak relevan buat PS Data Science, kan?
```

```
Don't just agree. Is it true that Hong Kong is still the biggest IPO market this year?
```

### thesis

- **Integrity first**: never invents data or references, coaches rather than ghostwrites, follows the campus AI-use and similarity rules (e.g. Indonesia's 2024 GenAI guidance).
- Structures for Indonesian skripsi (Bab I-V), international IMRaD theses, CS design-and-implementation projects, and the Chinese 毕业论文 process (开题报告, 外文翻译, 答辩).
- What examiners reward vs. common mistakes, a 10-criterion scoring sheet, a defense question bank and mock defense.
- Debate panel (Examiner, Supervisor, Methodologist, Tone Detector) for topic choice and draft review.
- `scripts/cite_check.py` (in-text citations vs reference list, APA and IEEE) and `scripts/text_check.py` (Indonesian + English padding/AI phrases, "signifikan" without a test, long sentences, placeholders).

### report

- Structures and checklists for lab reports, programming lab reports, technical/project reports, makalah, KP/magang and progress reports.
- Marker-style review panel; same checker scripts as `thesis`.

### humanizer

1. Diagnoses the text (English or Indonesian): AI-typical words, padding phrases, "not just X but Y", lists of three, repeated paragraph openers, uniform sentence length, em dashes.
2. Asks: **humanize only**, or **humanize + upgrade** with the matching skill (personal-statement, report, thesis, harvard-cv)?
3. Rewrites at the lightest touch (length within about ±10%), never changing facts, numbers, citations or quotes, and never inventing details; unclear spots are flagged `[ADD DETAIL]`.
4. Shows a before/after check with `scripts/humanize_check.py --compare`.
5. Accepts AI-detector reports (GPTZero, Turnitin, ZeroGPT) as hints: triages each flagged sentence (template phrasing / vague claim / plain fact / missing voice) and fixes only real writing problems, since detectors are unreliable, especially for non-native writers. `--per-sentence` shows which sentences have real red flags.

It improves style; it is not a detector-evasion tool and does not replace any AI-use disclosure a school or employer requires.

## Usage examples

```
Upgrade this personal statement for CityU Data Science (1st) and CFFT (2nd), undergraduate + scholarship. Keep it close to the original: [paste]
```

```
Turn my personal statement into a story bank for a recorded video interview.
```

```
Upgrade my CV to Harvard style and tailor it for a fintech internship: [paste]
```

## Project structure

```
.
├── .claude-plugin/marketplace.json      # generated
├── .github/
│   ├── scripts/generate-plugins.py      # skills/ → plugins/
│   ├── scripts/update-readme.py         # skills table above
│   └── workflows/
├── skills/                              # edit here
│   ├── personal-statement/
│   │   ├── SKILL.md
│   │   ├── references/                  # frameworks, discipline, examples, templates,
│   │   │                                # anti-ai-tone, undergraduate-scholarship, regional,
│   │   │                                # research-and-verify, interview-prep, debate-panel
│   │   └── scripts/ps_check.py
│   ├── harvard-cv/
│   │   ├── SKILL.md
│   │   ├── references/                  # harvard-format, action-verbs, bullet-upgrades
│   │   └── scripts/cv_check.py
│   ├── debate-mode/
│   │   ├── SKILL.md
│   │   └── references/evidence-standards.md
│   ├── thesis/                          # structure, what-examiners-want, literature-and-citations,
│   │                                    # defense-prep, debate-panel, integrity-and-ai + 2 scripts
│   ├── report/                          # report-types, review-panel + 2 scripts
│   └── humanizer/                       # patterns (EN + ID) + humanize_check.py
├── plugins/                             # generated: plugins/<name>/skills/<name>/
├── CREDITS.md
└── LICENSE
```

On every push to `main`, GitHub Actions regenerates `plugins/` and the skills table. To run it locally:

```bash
pip install pyyaml && python .github/scripts/generate-plugins.py && python .github/scripts/update-readme.py
```

## License

MIT. See [LICENSE](LICENSE) and [CREDITS.md](CREDITS.md). Not affiliated with Harvard University or any university mentioned in examples.
