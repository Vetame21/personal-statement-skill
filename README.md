# Agent Skills

A curated collection of agent skills for Claude Code and Cowork.

## Installation

- **Using the `skills` CLI**: `npx skills add OWNER/REPO --skill skill-name`
- **As a Plugin Marketplace (Claude Code / Cowork)**
  - `claude plugin marketplace add OWNER/REPO`
  - `claude plugin install skill-name@OWNER-skills`

## Skills

<!-- SKILLS_TABLE_START -->

| Skill | Description |
|-------|-------------|
| [personal-statement](https://github.com/OWNER/REPO/tree/main/skills/personal-statement) | Assist in writing, structuring, and polishing personal statements and self-introductions. Use when the user mentions writing a PS, personal statement, self-introduction, application essay, motivation letter, statement of purpose, cover letter, or personal bio — for study abroad applications, graduate/PhD admissions, scholarship applications, job applications, or any similar context. |
| | ```npx skills add OWNER/REPO --skill personal-statement``` |
| | ```claude plugin install personal-statement@OWNER-skills``` |

<!-- SKILLS_TABLE_END -->

---

## Project Structure

```
.
├── .claude-plugin/          # Plugin marketplace configuration
│   └── marketplace.json
├── .github/
│   ├── scripts/             # CI/CD automation scripts
│   │   ├── generate-plugins.py
│   │   └── update-readme.py
│   └── workflows/           # GitHub Actions workflows
│       ├── generate-plugins.yml
│       └── update-readme.yml
├── skills/                  # Skill source files (edit here)
│   └── personal-statement/
│       ├── SKILL.md
│       └── references/
├── plugins/                 # Auto-generated plugin distributions
│   └── personal-statement/
│       ├── README.md
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           ├── SKILL.md
│           └── references/
└── README.md
```

### Two Distribution Channels

1. **npx skills** — Direct CLI installation from the `skills/` directory
2. **Claude Plugin Marketplace** — Auto-generated `plugins/` directory, managed via `.claude-plugin/marketplace.json`

### How It Works

- Edit skills in the `skills/` directory
- On push to `main`, GitHub Actions automatically:
  - Regenerates `plugins/` from `skills/` source
  - Updates the skills table in this README

## License

MIT
