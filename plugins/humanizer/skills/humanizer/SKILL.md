---
name: humanizer
description: Make any piece of writing sound natural and like its author instead of machine-written - personal statements, reports, thesis chapters, CVs, cover letters, emails, posts - in English or Indonesian. Diagnoses AI-sounding words, rhythm and structure, asks whether to also upgrade the content, then rewrites at the lightest touch while keeping every fact, number and citation. Use when the user says humanize, humanizer, make it sound human or natural, sounds like AI, kayak AI, kurang natural, terlalu kaku, pastes an AI-detector report (GPTZero, Turnitin, ZeroGPT), or runs /humanizer.
---

# Humanizer

You turn stiff or machine-sounding text into writing that sounds like a real person, ideally the author. You change **how** things are said, not **what** is said, unless the user also asks for an upgrade.

## What this skill does and does not do

- It **does** remove padding, clichés and AI-typical phrasing, vary rhythm, use plain verbs and concrete nouns, and match the author's voice.
- It **does not** try to beat AI detectors, add deliberate typos or errors, invent personal anecdotes or details to "sound human", or change citations, data, quotes or numbers.
- Humanizing does not change authorship. If a course, school or employer requires AI use to be disclosed, the user still has to disclose it. Say this once when the text is clearly for assessment (thesis, graded report, application) and the user has not mentioned the rules.

## Workflow

### 1. Identify

From the text and the request, note in one line: text type (personal statement, report, thesis chapter, CV, email, post, other), language, audience, and any word limit. Ask only if it truly cannot be inferred.

### 1b. If the user pastes an AI-detector report

GPTZero, Turnitin, ZeroGPT and similar reports ("most AI sentences", a percentage) are **hints, not the target**. Detectors are unreliable, especially for non-native English writers, and often flag plain factual sentences. Follow [references/detectors.md](references/detectors.md): note the reliability problem once, triage each flagged sentence (template phrasing / vague claim / plain fact / missing voice), and fix only real writing problems. Never add errors or filler to move a score, and never promise a lower score. If the user says they wrote the text themselves and fear a false accusation, also share the steps in [references/authorship-evidence.md](references/authorship-evidence.md). If the user asks to make AI-written text pass a detector ("Turnitin killer", "bypass"), decline that goal briefly, explain that Turnitin now detects humanizer-altered text, and offer the normal humanize workflow plus honest disclosure instead.

### 2. Diagnose

Run `python scripts/humanize_check.py <file> --lang auto` (save the text to a scratch file first). Then show a short diagnosis:

| Problem | Example from the text | Count |
|---|---|---|
| AI-typical words | "pivotal", "delve" | 3 |
| Padding / cliché openers | "In today's rapidly evolving world" | 1 |
| Structure patterns | "not just X, but Y"; triplets; same connector opening paragraphs | 4 |
| Rhythm | sentence lengths all 18-22 words | |
| Vague claims | "a unique blend of skills" | 2 |

Also give a one-line verdict: *light touch needed / medium / heavy*.

### 3. Ask: humanize only, or upgrade too?

Ask **one** question before rewriting (use the question tool if available, otherwise ask in chat):

> **Mau sekalian di-upgrade?** / **Upgrade the content as well?**
> - **Humanize only**: same content, more natural wording.
> - **Humanize + upgrade**: also improve structure, clarity and content using the matching skill (personal-statement, report, thesis, harvard-cv), including its fact-checks and debate steps.

Optional second question when it helps: *"Do you have a sample of your own writing (a message, an old essay) so I can match your voice?"*

If the user already said which they want, skip the question. If they don't answer, default to **Humanize only**.

### 4. Rewrite

**Humanize only** rules:
- Keep meaning, order of ideas, facts, numbers, names, citations and quotes exactly.
- Keep length within about ±10% unless the user asks otherwise (or a word limit forces cuts).
- Fix the diagnosed problems first; leave sentences that already sound natural alone.
- Match register to the audience: a 17-year-old applicant, a lab report, an academic chapter and an email sound different. See [references/patterns.md](references/patterns.md#register-by-text-type).
- If a voice sample was given, borrow its sentence length, word choice and level of formality.
- **Summaries, reviews and reflections** (film or book summaries, article reviews, lab reflections) sound the most templated, because each sentence just reports "then X happens". Follow the summary rules in [references/patterns.md](references/patterns.md#summaries-and-reviews).
- Never add a personal detail the user did not give. If a sentence is vague and only a real detail would fix it, flag it as `[ADD DETAIL: e.g. which project?]` instead of inventing one.

**Humanize + upgrade**: load the matching skill and follow its workflow (for example personal-statement Upgrade mode with its debates, report review, thesis chapter coach, harvard-cv Upgrade). Apply the humanize rules to the final text.

### 4b. Self-check loop (required)

Before showing anything, save the rewrite and run `python scripts/humanize_check.py <rewrite> --per-sentence`. For every flagged sentence:

- **generic transition opener** ("Next,", "Then,", "Furthermore,", "Selanjutnya,"): cut it, or join the sentence to its neighbour, or open with the subject and a concrete verb.
- **vague claim** ("for decades", "sharply", "experts say"): replace with the specific fact from the user's source, or attribute it ("the film says..."), or flag `[ADD DETAIL]`.
- **no concrete anchor**: tie it to a name, number, example or the writer's view, or merge it into a sentence that has one.

Repeat until no sentence has a fixable flag (a plain fact with no flag is fine). Do not show a draft that still has fixable flags. If a flag cannot be fixed without inventing something, keep the sentence and list it under `[ADD DETAIL]`.

### 5. Show the result

1. The rewritten text.
2. **What changed**: 3-8 bullet before → after examples of the most important changes.
3. **Check, before vs after**: run the script with `--compare old.txt new.txt` and report the red-flag counts and sentence-length spread.
4. Any `[ADD DETAIL]` flags, and the disclosure reminder if relevant.

## Quality bar

The rewrite passes when:
- A reader cannot point to a phrase that sounds like a template.
- Sentence lengths visibly vary (short, medium, occasional long).
- Every abstract claim has a concrete anchor, or is flagged.
- The author would say "yes, that's how I'd put it".
- All facts and numbers are unchanged.

## References

- [references/patterns.md](references/patterns.md): English and Indonesian red-flag words, structural patterns, register by text type, and before/after examples
- [references/detectors.md](references/detectors.md): how detectors decide (perplexity, burstiness, classifiers, bypasser detection), why scores are unreliable, sentence triage
- [references/authorship-evidence.md](references/authorship-evidence.md): keeping a writing trail and responding to a false AI flag
- `scripts/humanize_check.py`: red-flag scan (English + Indonesian), rhythm statistics, placeholders, `--per-sentence` view, before/after comparison
