# Credits

This repository is based on **[DiamondhunterSA/personal-statement-skill](https://github.com/DiamondhunterSA/personal-statement-skill)** by DiamondhunterSA, published under the MIT License (as stated in its README). The original 5-stage personal statement workflow, its reference modules (frameworks, discipline guide, examples, templates) and the CI scripts that generate the plugin marketplace come from that project. Thank you!

## What changed here

- **Bug fixes**: plugin generator now writes `plugins/<name>/skills/<name>/SKILL.md` (the layout Claude Code discovers); removed the duplicate root `SKILL.md` with an invalid name; replaced VS Code tool names (`create_file`, `replace_string_in_file`) with Claude Code's `Write`/`Edit`; README workflow rebases before pushing; added the missing `LICENSE` file.
- **personal-statement**: Upgrade (light edit) mode, undergraduate and scholarship guidance, two-program statements, `[VERIFY]` markers for invented details, a research-and-cite step for current facts, regional conventions, interview and recorded-video prep, Data Science and FinTech guidance, a two-stage panel debate (before writing and after the draft), a full anti-AI tone checklist, and a `ps_check.py` script; example sentences now follow the anti-AI rules.
- **debate-mode** (new): Claude researches before agreeing and returns sourced verdicts.
- **harvard-cv** (new): create, upgrade and tailor Harvard-style CVs, with a `cv_check.py` linter.

The Harvard-style CV guidance summarises public resume guides from Harvard's Mignone Center for Career Success. This project is not affiliated with or endorsed by Harvard University.
