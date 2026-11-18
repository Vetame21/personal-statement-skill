# How AI-Writing Detection Works

Shared reference for every skill in this collection. Use it to **explain** detector results and to protect genuine authors. Do not use it to help AI-generated text pass as human work where that is not allowed: the research below also shows why that is a losing game.

Facts below come from published research and from Turnitin's own documentation and blog posts (2023-2025). Vendors change their systems; re-check before quoting numbers in anything important.

---

## 1. The three signals

| Signal | What it measures | Why human text gets caught |
|---|---|---|
| **Perplexity** | How predictable each next word is to a language model | Simple vocabulary, set phrases, definitions and plain facts are predictable even when a person wrote them |
| **Burstiness** | How much sentences vary (length, structure, per-sentence predictability) | Careful, uniform academic writing and formulaic genres vary little |
| **Trained classifiers** | Many style features at once, learned from labelled human and AI text (usually fine-tuned transformer models) | Their features are not public, so false positives cannot be explained sentence by sentence |

## 2. How Turnitin specifically does it

- **Eligibility**: only long-form prose between **300 and 30,000 words**, in .docx, .pdf, .txt or .rtf, under 100 MB, at institutions that license Turnitin Originality.
- **Languages**: English, Spanish and Japanese (some institutions also list Arabic). Other languages, such as Indonesian, are not covered by the AI detector; similarity (plagiarism) checking is separate.
- **Scoring** (as described in Turnitin's materials and summarised by third parties): the text is split into overlapping segments of a few hundred words; each sentence gets a score in context; the document percentage is the share of sentences judged AI-written.
- **Low scores are hidden**: results from 1% to 19% show only as an asterisk, because Turnitin found more false positives below 20%. The minimum length was raised from 150 to 300 words for the same reason.
- **False positives, by Turnitin's own figures (2023)**:
  - document level: under 1% for documents with 20% or more AI writing;
  - sentence level: about 4% of highlighted sentences may be human-written;
  - false positives cluster **at transitions between human and AI text** and in the **first and last few sentences** of a document.
- **Paraphrase and bypasser detection**: paraphrasing detection arrived in 2024; **AI bypasser detection** (27 August 2025) targets text altered by "humanizer" tools (English only at launch).
- **Turnitin Clarity** (generally available July 2025): an optional writing space where instructors can replay draft history and see typed vs pasted text and time spent. The direction of the industry is towards **evidence of the writing process**, not just scoring the final text.

## 3. Who gets false positives

- **Non-native English writers**: Liang et al. (2023) found seven detectors labelled on average about 61% of TOEFL essays as AI-written, while being near-perfect on US eighth-graders' essays. Lower vocabulary variety reads as low perplexity.
- **Formulaic genres**: summaries, lab reports, definitions, literature overviews, translated text.
- **Mixed documents**: the edges between a person's writing and pasted or AI-assisted passages.

## 4. Why "beating the detector" is a dead end

- Paraphrasing can defeat older detectors (Krishna et al., NeurIPS 2023: DetectGPT's detection fell from 70.3% to 4.6% at a 1% false-positive rate), but the same paper showed a retrieval defence, and Turnitin now detects humanizer output specifically.
- A **bypasser flag looks like deliberate concealment**, which is treated more seriously than undisclosed AI help.
- OpenAI withdrew its own detector in July 2023 for low accuracy (26% of AI text caught, 9% of human text wrongly flagged): **scores are weak evidence in both directions**. The honest strategy is the same either way: write it yourself, keep the trail, disclose permitted AI use.

## 5. How the skills use this

1. **Explain** a flag: is the sentence genuinely generic (fix it) or a plain fact / formulaic but correct sentence (keep it)?
2. **Write well for its own sake**: specific content, the author's own details, varied rhythm, no template phrasing (see `anti-ai-tone.md`). This is good writing, and genuinely human writing done this way is less often misread.
3. **Protect genuine authors** with `authorship-evidence.md`.
4. **Decline** requests whose goal is to make AI-written work pass a detector against the rules; offer honest alternatives (write it with coaching, disclose, keep evidence).
