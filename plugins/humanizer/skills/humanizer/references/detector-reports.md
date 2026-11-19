# Using AI-Detector Reports (Triage)

Users often paste results from GPTZero, Turnitin, ZeroGPT, Copyleaks or similar tools ("Your most AI sentences", a percentage, highlighted lines). Use these reports as **hints about where the text may be generic**, never as the goal.

For how detectors work (perplexity, burstiness, classifiers, Turnitin's thresholds and bypasser detection), see `shared/ai-detection.md`.

## Why the score is not the target

- OpenAI withdrew its own AI classifier on 20 July 2023 because of its "low rate of accuracy". In OpenAI's own evaluation it caught 26% of AI-written text and wrongly labelled 9% of human text as AI.
- A Stanford-led study (Liang et al., *Patterns*, 2023) ran seven detectors, including GPTZero, on essays by non-native English writers (TOEFL) and US eighth-graders. The detectors were near-perfect on the native essays but labelled more than half of the TOEFL essays as AI-generated (average false positive rate about 61%). The authors link this to low "perplexity": simpler, more predictable word choice looks machine-like to the detector.
- Vendors publish their own (lower) error rates; independent tests have been less kind. Treat any single score as uncertain.
- Plain factual sentences ("CO2 is about 0.04% of the atmosphere") are often flagged because facts are predictable. That is not a writing problem.

Say this briefly to the user the first time a detector report appears, especially if they are a non-native English writer.

## Triage each flagged sentence

For every sentence the report marks as AI-like, decide which case it is:

| Case | Sign | Action |
|---|---|---|
| **Template phrasing** | Cliché opener, AI-typical word, "not just X but Y", generic transition ("Next,", "Furthermore,") | Rewrite with plain, specific wording |
| **Vague claim** | "has gone up sharply", "experts agree", "many people" with nothing concrete | Add the concrete fact **only if the user's source supports it** (number, name, date), or flag `[ADD DETAIL]` |
| **Plain fact** | A correct, simple factual sentence | Keep it. Optionally tie it to the author's point or merge it with a neighbouring sentence for flow |
| **Missing voice** | Summary sentences that never show the writer's view (common in reviews, reflections, personal statements) | Where the genre allows, add the writer's angle in their own words, or ask the user for it |

Rules:
- Facts, numbers, names, quotes and citations stay correct. In Humanize only mode, add no new numbers or facts. In Humanize + upgrade mode, a new number must come from the user's source or a search you ran (cite it), and it goes in the "New details" list.
- Do not add mistakes, odd synonyms, random typos, or filler to "confuse" a detector. It hurts the writing and is a known evasion trick.
- Do not promise a lower score. Promise clearer writing.
- If the text is for assessment and the user used AI to draft it, remind them once that disclosure rules still apply.

## Output for a detector report

1. One-line note on detector reliability (first time only).
2. A table: flagged sentence → case → suggested rewrite (or "keep").
3. If the user wants, the whole passage rewritten under the normal humanize rules.
4. `scripts/humanize_check.py --per-sentence` output for the passage, so the user can see which sentences have real red flags.

## Sources (checked November 2026)

- [OpenAI: New AI classifier for indicating AI-written text](https://openai.com/blog/new-ai-classifier-for-indicating-ai-written-text/) (26% / 9%; note added 20 July 2023 on its withdrawal) · [Decrypt: OpenAI shuts its AI text classifier](https://decrypt.co/149826/openai-quietly-shutters-its-ai-text-classifier-due-to-low-accuracy)
- [Liang et al. (2023), GPT detectors are biased against non-native English writers, *Patterns*](https://arxiv.org/abs/2304.02819)
