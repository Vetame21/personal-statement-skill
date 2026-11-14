# Application Writing Skills for Claude

Agent skills for [Claude Code](https://code.claude.com/docs) and Cowork that help with university, scholarship and job applications:

| Skill | What it does |
|---|---|
| **personal-statement** | Write, upgrade or polish a personal statement / SOP / motivation letter / scholarship essay, keep it close to the applicant's own draft, add verified current facts, and prepare interview or recorded-video answers |
| **harvard-cv** | Create, upgrade or tailor a one-page Harvard-style CV with action-verb, result-focused bullets |
| **debate-mode** | Claude does not just agree: it researches the claim first and returns a sourced verdict (Yes / No / Partly / Not enough evidence) |

> Based on [DiamondhunterSA/personal-statement-skill](https://github.com/DiamondhunterSA/personal-statement-skill) (MIT). See [CREDITS.md](CREDITS.md) for what is original and what changed.

## Install

### Claude Plugin Marketplace (Claude Code / Cowork)

```bash
claude plugin marketplace add __OWNER__/__REPO__
```

```bash
claude plugin install personal-statement@__OWNER__-skills
```

```bash
claude plugin install harvard-cv@__OWNER__-skills
```

```bash
claude plugin install debate-mode@__OWNER__-skills
```

While the repository is private, the marketplace commands need a GitHub login that can read it.

### npx skills (CLI)

```bash
npx skills add __OWNER__/__REPO__ --skill personal-statement
```

### Manual

Copy a folder from `skills/` into `~/.claude/skills/` (personal) or `.claude/skills/` (project).

## Skills

<!-- SKILLS_TABLE_START -->

| Skill | Description |
|-------|-------------|
| [debate-mode](https://github.com/DiamondhunterSA/personal-statement-skill/tree/main/skills/debate-mode) | Evidence-first debate. Instead of agreeing, Claude researches a claim or proposal and returns a sourced verdict (Yes / No / Partly / Not enough evidence) before giving a recommendation. Use when the user asks Claude to debate, argue, challenge them, push back, fact-check, "debat pakai fakta", "jangan iya-iya aja", "don't just agree", "prove it", or asks whether an idea, claim, or edit (for example to a personal statement or CV) is right or relevant. |
| | ```npx skills add DiamondhunterSA/personal-statement-skill --skill debate-mode``` |
| | ```claude plugin install debate-mode@DiamondhunterSA-skills``` |
| [harvard-cv](https://github.com/DiamondhunterSA/personal-statement-skill/tree/main/skills/harvard-cv) | Create, upgrade, or tailor a CV/resume in the Harvard style (one page, reverse chronological, Education → Experience → Leadership & Activities → Skills & Interests, action-verb bullets with results). Use when the user asks to make, fix, review, upgrade, or tailor a CV or resume, mentions "Harvard CV", "Harvard resume", "Harvard format", or needs a CV to go with a university, scholarship, internship, or job application. |
| | ```npx skills add DiamondhunterSA/personal-statement-skill --skill harvard-cv``` |
| | ```claude plugin install harvard-cv@DiamondhunterSA-skills``` |
| [personal-statement](https://github.com/DiamondhunterSA/personal-statement-skill/tree/main/skills/personal-statement) | Write, upgrade, and polish personal statements, statements of purpose, motivation letters, scholarship essays, application essays, self-introductions, and cover letters, for high school/undergraduate, graduate, PhD, scholarship, and job applications. Use when the user shares a PS draft to review or upgrade, asks to write one from scratch, asks to keep a draft close to the original while improving it, wants current facts or news worked into a statement, or wants to prepare video/interview answers from a statement. |
| | ```npx skills add DiamondhunterSA/personal-statement-skill --skill personal-statement``` |
| | ```claude plugin install personal-statement@DiamondhunterSA-skills``` |

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
│   │   │                                # research-and-verify, interview-prep
│   │   └── scripts/ps_check.py
│   ├── harvard-cv/
│   │   ├── SKILL.md
│   │   ├── references/                  # harvard-format, action-verbs, bullet-upgrades
│   │   └── scripts/cv_check.py
│   └── debate-mode/
│       ├── SKILL.md
│       └── references/evidence-standards.md
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
