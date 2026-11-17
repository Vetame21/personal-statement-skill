# Using AI-Detector Reports

Users often paste results from GPTZero, Turnitin, ZeroGPT, Copyleaks or similar tools ("Your most AI sentences", a percentage, highlighted lines). Use these reports as **hints about where the text may be generic**, never as the goal.

## How detectors decide (research summary)

Use this to explain **why** a sentence was flagged, so the user can tell a weak sentence from a detector mistake.

1. **Perplexity: how predictable the words are.** Language models are built to produce predictable text, so any text a model finds easy to predict looks machine-made. Simple vocabulary, set phrases and plain facts all score as predictable, even when a person wrote them.
2. **Burstiness: how much sentences vary.** Human writing tends to swing between short and long, plain and unusual sentences; model text is more even. Detectors measure the spread of per-sentence scores.
3. **Trained classifiers.** Current commercial detectors (GPTZero, Turnitin, Copyleaks, Originality.ai) do not rely on those two numbers alone. They use models, typically fine-tuned transformers, trained on labelled human and AI text, which weigh many style features at once. Their exact features are not public.
4. **Who gets false positives most:** non-native English writers (Liang et al., 2023: about 61% of TOEFL essays flagged on average across seven detectors), and formulaic genres such as summaries, lab reports, definitions and literature overviews.
5. **Paraphrasing and "humanizers".** Research shows paraphrasing can defeat older detectors: in Krishna et al. (NeurIPS 2023) a paraphrase model cut DetectGPT's detection rate from 70.3% to 4.6% at a 1% false-positive rate. The same paper showed a counter-measure (retrieval against stored model outputs), and since 27 August 2025 Turnitin offers **AI bypasser detection** aimed specifically at text altered by humanizer tools (English only at launch). A bypasser flag can look worse than an ordinary AI flag, because it suggests deliberate concealment.

**What this means for this skill:** improving clarity, specificity and voice is worth doing for its own sake, and it often makes genuinely human text read more like its author. Rewriting AI-generated text to slip past a detector is not what this skill does, and it is increasingly detected anyway.

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
- Facts, numbers, names, quotes and citations stay correct. If you add a number, it must come from the user's source or a search you ran (cite it).
- Do not add mistakes, odd synonyms, random typos, or filler to "confuse" a detector. It hurts the writing and is a known evasion trick.
- Do not promise a lower score. Promise clearer writing.
- If the text is for assessment and the user used AI to draft it, remind them once that disclosure rules still apply.

## Output for a detector report

1. One-line note on detector reliability (first time only).
2. A table: flagged sentence → case → suggested rewrite (or "keep").
3. If the user wants, the whole passage rewritten under the normal humanize rules.
4. `scripts/humanize_check.py --per-sentence` output for the passage, so the user can see which sentences have real red flags.
