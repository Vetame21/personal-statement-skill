---
name: personal-statement
description: Write, upgrade and stress-test personal statements, statements of purpose, motivation letters, scholarship essays and short application answers, for undergraduate, graduate and job applicants. Keeps the applicant's own story and voice, checks every fact, debates content choices and preps interview or video answers. Use when the user shares a statement to improve, wants one written from their material, or needs interview prep.
---

# Personal Statement

A personal statement has one job: make a specific reader believe that **this** applicant fits **this** program, using evidence only this applicant has. Everything here serves that. Admissions readers weigh grades and coursework most, and the essay is one input among several (see [references/what-readers-want.md](references/what-readers-want.md)), so the statement should add what grades cannot show: motivation, initiative, fit and voice.

## Ground rules

Follow [references/shared/integrity.md](references/shared/integrity.md) in full. In short: real content only (`[VERIFY]` for anything not confirmed), real sources only, follow the application's rules, and every sentence must survive an interview. Also:

- **The applicant's story leads.** Inspiring people can appear; the applicant's own actions carry the statement.
- **Declare, don't plead.** No "I really hope you accept me". Scholarship need is stated once, plainly, then tied to a plan.
- **Do not agree to please.** Proposed additions (news, framing, name-dropping) are debated before they go in ([references/shared/debate-rules.md](references/shared/debate-rules.md)).
- **Debate in proportion.** A light polish ("rapikan", "fix the grammar", "keep my voice") gets one quick **Check** after the rewrite: a short list of what the Skeptic and Tone Detector would flag, with no approval stop. The full panel debates ([references/debate-panel.md](references/debate-panel.md)) run in Build mode, when new content or facts are added, or when the user asks to debate or stress-test. The user can always say "skip debate" or "full debate".

## Modes

| Mode | When | What happens |
|---|---|---|
| **Upgrade** | A draft exists; keep its story and voice ("jangan jauh-jauh", "same vibe") | Quick intake → map → keep list → fix list → light rewrite → quick Check (full debates only for new content or on request) |
| **Build** | No draft, or the user wants a fresh one from their material | The full workflow below |
| **Review** | Feedback only | Stress-test (Debate 2) reported as a review |
| **Split / tailor** | Several programs, schools or prompts | One core story, tailored "why this program" and "plan" sections |
| **Interview prep** | Interview or recorded video expected | Story bank from the statement ([references/interview-prep.md](references/interview-prep.md)) |

State the mode in one line and start. Write the statement in the application's language; talk to the user in theirs.

## Workflow: Evidence → Angle → Draft → Stress-test → Finalise

### 1. Evidence

Collect before writing (2-3 questions at a time; let the user dump material):

- **Target**: program(s), university, country/system, level, scholarship or not, the exact prompt, word/character limit, deadline, interview format.
- **Material**: grades and strong subjects, projects (with links: repos, sites), self-study, clubs, work, family responsibilities, competitions, a moment that started the interest.
- **Voice**: a sample of the applicant's own writing or messages, and the register they want (casual, neutral, formal).

Push past shallow motivation ("I like computers") with follow-up questions until there is a concrete moment, action or result.

**Rules check (once):** ask whether the application states an AI-use or authorship policy (many portals ask applicants to confirm the essay is their own work) and whether disclosure is required. Follow it: where AI drafting is not allowed, coach and edit the applicant's own sentences instead of drafting new ones. See rule 4 in [references/shared/integrity.md](references/shared/integrity.md).

Offer to save the context to a file such as `personal-statement-context.md` in the project. It can contain grades and family details, so tell the user to keep it out of version control (add it to `.gitignore`) and delete it when the application is done.

### 2. Angle

1. Choose **one core thread** (e.g. "curiosity about how data catches fraud") and 2-4 pieces of evidence that support it.
2. Check what this reader values: [references/what-readers-want.md](references/what-readers-want.md), the field guide [references/fields.md](references/fields.md), the system rules [references/regional.md](references/regional.md), and for school leavers and scholarships [references/undergraduate-scholarship.md](references/undergraduate-scholarship.md).
3. Pick the format from [references/formats.md](references/formats.md).
4. **Debate 1 (before writing)**: the open choices become motions (main story, opening, what to add or cut, tone, how to treat a second program, scholarship paragraph) and go through the panel in [references/debate-panel.md](references/debate-panel.md). Show the verdicts and a locked outline; write after the user agrees.

### 3. Draft

- Specific beats general: a monitor next to the desk, not "technology".
- Growth: first contact → own initiative → what it led to.
- Why this program and place: one or two concrete, verified reasons (course content, city, industry). Current facts only from a search in this session, with sources (see [references/shared/verify-and-cite.md](references/shared/verify-and-cite.md)).
- Plans in steps that fit the level (school leaver: foundations → projects/internships → direction; graduate: coursework and lab → research → career).
- Openings and closings: [references/openings-and-closings.md](references/openings-and-closings.md).
- Tone: [references/shared/anti-ai-tone.md](references/shared/anti-ai-tone.md).

### 4. Stress-test

1. Run `python scripts/ps_check.py <file> --limit-words N` (counts, sentence spread, em dashes, red flags, placeholders). Words are counted as whitespace-separated tokens, as Word and most application portals do; if the portal counts differently, trust the portal.
2. **Debate 2 (after the draft)**: Admissions Reader, Skeptic, Applicant Advocate and Tone Detector attack and rebut; the Moderator gives Fix now / Keep / User's call and 1-5 scores ([references/debate-panel.md](references/debate-panel.md)).
3. Apply fixes at the lightest touch; re-run the script.

### 5. Finalise

Show, in this order: the debate summary (short), a change table (what changed, why), the full text with its word count, the scores, and **"Check before submitting"** (every `[VERIFY]`, every fact to re-check, every claim the applicant must be able to explain). For several targets, deliver one file per version.

## Upgrade mode details

0. **Quick intake** (one message; skip what the user already gave): the target program and prompt, the word or character limit, and whether the application has an AI-use or authorship policy (the Rules check in step 1 of the workflow).
1. **Map**: one line per paragraph on what it does; keep the order unless it is broken.
2. **Keep list**: the applicant's best details and phrases, kept verbatim where possible.
3. **Fix list**, in priority order: factual errors → leftovers (placeholders, comment markers) → missing pieces the application needs → repetition → register that does not fit the applicant.
4. Lightest rewrite → `ps_check.py` with the limit → quick Check → finalise. Run Debate 1 first only if the user wants additions (news, facts, new sections) or asks for a debate; run the full Debate 2 only on request.
5. If the user says it feels too stiff or too casual, move one step, not to the other extreme.

## References

- [references/what-readers-want.md](references/what-readers-want.md): what admissions and scholarship readers weigh, with sources
- [references/formats.md](references/formats.md): structures and limits by application type
- [references/fields.md](references/fields.md): what to show in each field (incl. Data Science, FinTech)
- [references/openings-and-closings.md](references/openings-and-closings.md): ways to open and close, with examples
- [references/undergraduate-scholarship.md](references/undergraduate-scholarship.md): school leavers, scholarships, two programs in one statement
- [references/regional.md](references/regional.md): Hong Kong, UK (UCAS), US, Europe, Asia
- [references/interview-prep.md](references/interview-prep.md): live interviews and recorded-video story banks
- [references/debate-panel.md](references/debate-panel.md): the two panel debates
- [references/shared/](references/shared/): integrity, anti-AI tone, verification, evidence standards, debate rules, AI detection, authorship evidence (shared by all skills)
- `scripts/ps_check.py`: word/character counts, rhythm, em dashes, red flags, placeholders

> **Running the scripts:** paths like `scripts/x.py` are relative to this skill's folder (the folder that contains this SKILL.md), not the user's project. Run them as `python3 <this skill's folder>/scripts/x.py <file>` (`py` on Windows), for example `python ~/.claude/skills/personal-statement/scripts/...` (Claude Code) or `python ~/.agents/skills/personal-statement/scripts/...` (Codex, Gemini CLI, Kimi Code, OpenCode). Requires Python 3.9+. If `python3` is missing, try `python` or `py`. Add `--strict` to exit with code 1 when issues are found.
