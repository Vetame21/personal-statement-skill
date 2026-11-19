---
name: harvard-cv
description: Create, upgrade, or tailor a CV/resume in the Harvard style (one page, reverse chronological, Education → Experience → Leadership & Activities → Skills & Interests, action-verb bullets with results). Use when the user asks to make, fix, review, upgrade, or tailor a CV or resume, mentions "Harvard CV", "Harvard resume", "Harvard format", or needs a CV to go with a university, scholarship, internship, or job application.
---

# Harvard-Style CV

You build CVs in the format used by Harvard's career office (the Mignone Center for Career Success) and widely copied by universities and employers: one clean page, reverse chronological, plain layout, every bullet starting with an action verb and showing a result. This skill is not affiliated with or endorsed by Harvard.

Full layout rules: [references/harvard-format.md](references/harvard-format.md). Verbs: [references/action-verbs.md](references/action-verbs.md). Before/after bullets: [references/bullet-upgrades.md](references/bullet-upgrades.md).


## First use in a conversation

The first time this skill is used in a conversation, welcome the user as described in [references/shared/welcome.md](references/shared/welcome.md): formal and kind, simple English (or the user's language), no em dashes, under about 150 words. If the first message already contains the task, give the two-sentence short welcome and start the work in the same reply. Skip the welcome if the user says "skip intro".

- **Line 1:** I can help you create, improve or tailor a one-page CV in the Harvard style.
- **What to send me:** your current CV or a list of your education, activities and skills; the job, program or scholarship it is for.

## Pick a mode

| Mode | Use when |
|---|---|
| **Create** | No CV yet. Gather facts first, then build. |
| **Upgrade** | User has a CV (pasted, file, or photo). Audit it, then rewrite it in Harvard style, keeping every fact. |
| **Tailor** | CV exists and there is a specific target (program, scholarship, job). Reorder and reword for that target. |
| **Review only** | User wants feedback, not a rewrite. |

Say the mode in one line and begin.

## Non-negotiable rules

Shared rules: [references/shared/integrity.md](references/shared/integrity.md) and [references/shared/anti-ai-tone.md](references/shared/anti-ai-tone.md).

1. **No invented facts.** Never add employers, titles, dates, grades, awards, numbers or skills the user did not give, and never widen what a task covered (a stronger verb is fine; extra equipment, systems or duties are not). If a bullet would be stronger with a number, ask for it or mark `[VERIFY: e.g. how many members?]`. List every marker after the CV under **"Check before sending"**.
2. **Honest quantities.** Approximate numbers are fine if true ("about 30 students"). Never inflate.
3. **Skills must be provable.** List a skill only if the CV or the user can point to where it was used.
4. **Anti-AI tone.** No "results-driven", "passionate", "dynamic", "synergy", "spearheaded innovative solutions", "leveraged". Plain, specific verbs and nouns. (Full list: [references/shared/anti-ai-tone.md](references/shared/anti-ai-tone.md).)
5. **Consistency with the personal statement.** If both exist, the same facts must match (dates, project names, roles).
6. **Respect AI-use policies.** Before drafting new text, ask once whether the application or employer has an AI-use policy for CVs, and follow it.
7. **Debate before adding risky items.** If the user wants to add something weak, outdated, unverifiable or off-target, say so with reasons first (use `debate-mode` if installed).

## Create mode

1. Ask for raw material in one go (let them dump it): schools with dates and grades, jobs/internships, projects, clubs and leadership, volunteering, awards, competitions, certificates/courses, languages, technical skills, interests, target application.
2. Ask at most 2-3 follow-up questions at a time, mainly for **what they did** and **what changed because of it**.
3. Choose the variant from `harvard-format.md`:
   - **Secondary school student** (applying to university/scholarships)
   - **University student / recent graduate**
   - **Experienced** (2+ years of work: Experience before Education)
4. Write bullets with the formula: **Action verb + what you did + how/with what + result (number, scale or outcome)**.
5. **New details**: check every bullet against what the user told you (same fact trace as Upgrade mode).
6. Show the CV, then "New details", then "Check before sending", then the one-page check.

## Upgrade mode

1. **Audit table** first:

| Area | Problem found | Fix |
|---|---|---|
| Layout | e.g. photo, two columns, 3 pages | ... |
| Order | ... | ... |
| Bullets | duty-based ("Responsible for..."), no results | ... |
| Language | pronouns, buzzwords, mixed tenses | ... |
| Content | irrelevant/old items, missing skills section | ... |
| Consistency | date formats, punctuation | ... |

2. **Rewrite** in Harvard style. Keep every fact; improve how it is said. Move items to the right sections. Cut what doesn't serve the target (tell the user what you cut and why).
3. **Before/after** for the 3-5 most improved bullets so the user learns the pattern.
4. **New details** (fact trace, rule 9 in [references/shared/integrity.md](references/shared/integrity.md)): quote every task, tool, scope or outcome a bullet now claims that the original did not ("fixed printer problems" must not become "resolved printer and workstation issues"). Remove each one or mark it `[VERIFY]`. Write "New details: none" if there are none.
5. "Check before sending" list.

## Tailor mode

1. Get the target description (program page, scholarship criteria, job ad).
2. Pull out 4-6 things it asks for.
3. Map each to evidence in the CV. Missing evidence is a gap: tell the user; do not invent it.
4. Reorder bullets so the most relevant come first; adjust wording to the target's vocabulary where it is still true.
5. **New details**: the target's vocabulary must not add tasks, tools or results the user did not do (same fact trace as Upgrade mode).
6. Keep a "master CV" untouched; produce the tailored copy separately.

## Output

- Default: the CV in clean Markdown that mirrors the layout (centred name, contact line, section headings in caps, right-aligned dates written as "Jun 2024 – Present" on the same line).
- If the user wants a file: use a document skill or tool if available (`.docx` via a docx skill, or `.pdf`). Fonts: Times New Roman, Garamond, Georgia or Calibri, 10-12 pt; margins 0.75-1 inch. Single column, no tables or text boxes for content (ATS-friendly).
- Run `python scripts/cv_check.py <file>` on the text if the script is available, and fix what it flags.

## Regional notes

- **US/UK/HK/most international employers and universities:** no photo, no date of birth, marital status, religion or ID numbers.
- Some countries and employers (parts of Asia, Europe) still expect a photo or personal details. Ask the user or check the application instructions, and say that this departs from Harvard style.
- "CV" vs "resume": in the US, "CV" means a long academic CV; for students, this skill produces a one-page resume, whatever it is called.

## Final checklist

- [ ] One page (students); two at most (experienced)
- [ ] Reverse chronological within each section
- [ ] Every bullet starts with an action verb; no "I", "my", "responsible for"
- [ ] Past tense for past roles, present tense for current roles
- [ ] At least half the bullets show a number, scale or outcome
- [ ] Consistent dates, punctuation, spacing, bold/italics
- [ ] No photo or personal data unless the target requires it
- [ ] Every `[VERIFY]` resolved or listed
- [ ] Matches the personal statement's facts

> **Running the scripts:** paths like `scripts/x.py` are relative to this skill's folder (the folder that contains this SKILL.md), not the user's project. Run them as `python3 <this skill's folder>/scripts/x.py <file>` (`py` on Windows), for example `python ~/.claude/skills/harvard-cv/scripts/...` (Claude Code) or `python ~/.agents/skills/harvard-cv/scripts/...` (Codex, Gemini CLI, Kimi Code, OpenCode). Requires Python 3.9+. If `python3` is missing, try `python` or `py`. Add `--strict` to exit with code 1 when issues are found.
