# Personal Statement Agent Skill

> **🎯 Agent Skills Enabled** — Structured 5-stage workflow for crafting compelling personal statements

A production-ready agent skill for [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) and [Cowork](https://cowork.ai) that guides users through writing, structuring, and polishing personal statements — from brainstorming to final draft.

## Overview

This skill provides an intelligent **5-stage writing assistant** for personal statements across all application contexts:

- **5-Stage Workflow** — Gather → Plan → Write → Polish → Iterate
- **10+ Discipline Templates** — Tailored guidance for CS, Engineering, Medicine, Law, Business, Humanities, and more
- **4 Reference Modules** — Frameworks, discipline-specific advice, annotated examples, and format templates
- **Multi-Language Support** — Bilingual parallel text, localized tone adaptation
- **Anti-AI Detection** — Built-in vocabulary checks to avoid common AI writing red flags

### Supported Application Types

| Type | Typical Length | Key Focus |
|------|---------------|-----------|
| Graduate / Master's | 500–1000 words | Academic fit, career goals |
| PhD Program | 1000–2000 words | Research interest, advisor fit |
| Scholarship | 500–800 words | Merit, impact, potential |
| Job Application | 300–500 words | Skills, experience, role fit |
| Fellowship | 800–1500 words | Leadership, community impact |
| Motivation Letter (European) | 1–2 pages | Formal letter format |

### How It Works

The skill follows a structured **progressive disclosure** approach:

```
Stage 1: Gather    →  Collect context, CV, program requirements
Stage 2: Plan      →  Build content pillars, discipline-aligned outline
Stage 3: Write     →  Draft with "show don't tell", anti-AI tone
Stage 4: Polish    →  Grammar, flow, specificity, word count
Stage 5: Iterate   →  Targeted revision based on feedback
```

**Key Features:**
- **Context persistence** — Saves applicant info to `.claude/personal-statement-context.md` for reuse across multiple applications
- **Discipline alignment** — Automatically adapts guidance based on target field (CS emphasizes projects, Medicine emphasizes empathy + rigor, etc.)
- **Multi-application support** — Keeps 70% core narrative stable, rewrites only "Why this program" sections for each target

## Quick Start

### Option 1: npx skills (CLI)

```bash
npx skills add DiamondhunterSA/personal-statement-skill --skill personal-statement
```

### Option 2: Claude Plugin Marketplace (Claude Code / Cowork)

```bash
# Step 1: Add the marketplace
claude plugin marketplace add DiamondhunterSA/personal-statement-skill

# Step 2: Install the skill
claude plugin install personal-statement@DiamondhunterSA-skills
```

## Skills

<!-- SKILLS_TABLE_START -->

| Skill | Description |
|-------|-------------|
| [personal-statement](https://github.com/DiamondhunterSA/personal-statement-skill/tree/main/skills/personal-statement) | Assist in writing, structuring, and polishing personal statements and self-introductions. Use when the user mentions writing a PS, personal statement, self-introduction, application essay, motivation letter, statement of purpose, cover letter, or personal bio — for study abroad applications, graduate/PhD admissions, scholarship applications, job applications, or any similar context. |
| | ```npx skills add DiamondhunterSA/personal-statement-skill --skill personal-statement``` |
| | ```claude plugin install personal-statement@DiamondhunterSA-skills``` |

<!-- SKILLS_TABLE_END -->

## Skill Architecture

### Reference Modules

The skill includes 4 reference modules loaded on demand for token efficiency:

| Module | File | Content |
|--------|------|---------|
| **Frameworks** | `references/frameworks.md` | Content Pillars framework, format templates by scenario |
| **Discipline** | `references/discipline.md` | 10+ fields with specific guidance, key questions, and pitfalls |
| **Examples** | `references/examples.md` | Annotated paragraphs, before/after comparisons, opening/closing techniques |
| **Templates** | `references/post-templates.md` | Structural skeletons for essay, formal letter, SoP, and Q&A formats |

### Progressive Disclosure

```
Always loaded:    Skill metadata (name, description, activation criteria)
On activation:    Core 5-stage workflow instructions
On demand:        Reference modules (frameworks, discipline, examples, templates)
```

This keeps token usage minimal — reference materials are only loaded when the relevant stage needs them.

## Usage Examples

### Start from Scratch

```
"Help me write a personal statement for a CS Master's at CMU"
```

The skill will guide you through all 5 stages, starting with context gathering.

### Polish an Existing Draft

```
"Here's my personal statement draft, please help me polish it: [paste draft]"
```

Jumps directly to Stage 4 (Polish) with grammar, flow, and specificity checks.

### Multiple Applications

```
"I need to adapt my PS for both MIT and Stanford"
```

Keeps the core narrative stable and rewrites program-specific sections.

## Project Structure

```
.
├── .claude-plugin/              # Plugin marketplace configuration
│   └── marketplace.json
├── .github/
│   ├── scripts/                 # CI/CD automation scripts
│   │   ├── generate-plugins.py  # Auto-generate plugins/ from skills/
│   │   └── update-readme.py     # Auto-update skills table in README
│   └── workflows/               # GitHub Actions workflows
│       ├── generate-plugins.yml
│       └── update-readme.yml
├── skills/                      # Skill source files (edit here)
│   └── personal-statement/
│       ├── SKILL.md
│       └── references/
│           ├── discipline.md
│           ├── examples.md
│           ├── frameworks.md
│           └── post-templates.md
├── plugins/                     # Auto-generated plugin distributions
│   └── personal-statement/
└── README.md
```

### Two Distribution Channels

| Channel | How It Works | Install Command |
|---------|-------------|-----------------|
| **npx skills** | Direct CLI installation from `skills/` | `npx skills add DiamondhunterSA/personal-statement-skill --skill personal-statement` |
| **Claude Plugin Marketplace** | Auto-generated `plugins/` via `.claude-plugin/marketplace.json` | `claude plugin install personal-statement@DiamondhunterSA-skills` |

### CI/CD Automation

On push to `main`, GitHub Actions automatically:
1. **Regenerates** `plugins/` from `skills/` source (via `generate-plugins.py`)
2. **Updates** the skills table in this README (via `update-readme.py`)

## Contributing

To add a new skill:

1. Create a new directory under `skills/` (e.g., `skills/my-new-skill/`)
2. Add a `SKILL.md` with YAML frontmatter (`name`, `description`) and skill instructions
3. Optionally add a `references/` directory for supporting materials
4. Push to `main` — CI will auto-generate the plugin and update this README

## Resources

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/overview)
- [Plugins Guide](https://docs.claude.com/en/docs/claude-code/plugins)
- [Agent Skills Guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

## License

MIT
