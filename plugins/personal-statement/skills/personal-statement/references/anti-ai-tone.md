# Anti-AI Tone Checklist

Readers of applications (admissions staff, scholarship panels, recruiters, and any automated screener in front of them) now see a lot of machine-written text. They do not need a detector to spot it: the same words, the same rhythms and the same empty sentences show up again and again. A statement that sounds generated loses trust even when every fact in it is true.

The goal is not to "beat detectors". The goal is writing that sounds like one specific person, because it is built from that person's details. Run this checklist on every draft before showing it.

---

## 1. Word-level red flags

Replace or cut these unless the applicant would genuinely say them out loud.

| Red flag | Plain alternative |
|---|---|
| delve, delve into | look at, study, dig into |
| tapestry, rich tapestry | mix, range, (or name the actual things) |
| testament to | shows |
| pivotal, crucial, paramount | important, key, (or cut) |
| journey (for anything not a trip) | time, years, path, (or cut) |
| embark on | start |
| realm, landscape, sphere | field, area, world |
| foster, cultivate, nurture | build, grow, help |
| leverage, harness, utilize | use |
| navigate (non-physical) | handle, deal with, work through |
| unwavering, steadfast, relentless | (show it with an action instead) |
| passion / passionate (more than once) | interest, curiosity, (or show it) |
| ignite, spark (more than once), fuel | start, push |
| seamless, robust, cutting-edge, innovative (as filler) | (name what is new or good about it) |
| beacon, cornerstone, linchpin | (cut the metaphor) |
| poised to | ready to, about to |
| multifaceted, intricate, nuanced | complex, (or explain the parts) |
| profound, deeply (as intensifiers) | (cut) |
| underscore, highlight (as verbs for ideas) | show |
| resonate with | matter to, connect with |
| in today's fast-paced / ever-evolving world | (cut) |
| a unique blend of | (cut; name the two things) |

One flagged word is not a disaster. Three or more in one paragraph is.

## 2. Structure-level red flags

These patterns give away generated text more reliably than single words.

- **"Not just X, but Y."** / **"It's not about X; it's about Y."** Use at most once per statement.
- **Triplets everywhere.** "curious, driven, and resilient"; "learn, grow, and contribute". Real writing mixes pairs, singles and lists of four.
- **Every paragraph the same length** and the same shape (claim → example → lesson). Vary them.
- **Uniform sentence length.** Mix short sentences (4-8 words) with medium and the occasional long one.
- **Em-dash habit.** More than about one em dash (—) per 150 words reads as machine-made. Use commas, full stops or brackets.
- **Lesson-at-the-end on every paragraph.** "This taught me the importance of..." Keep one or two; let the rest of the stories speak.
- **Rhetorical questions** as openers ("Have you ever wondered...?"). Avoid.
- **Summary closings.** "In conclusion", "Ultimately", "All in all". End on a concrete forward step or an echo of the opening instead.
- **Over-hedged or over-polished balance.** Real applicants have opinions and small rough edges.
- **Colon reveals.** "My goal is simple: to change the world." Avoid.

## 3. Content-level red flags

- Claims with no example ("I am a fast learner").
- Grand, unscoped ambitions ("revolutionise finance", "make the world a better place"). Narrow them to one problem the applicant can name.
- Praise of the school that could apply to any school ("world-class faculty", "vibrant community").
- Generic "global citizen" lines for international applicants.
- Feelings without a trigger ("I was deeply inspired"). Name what happened.

## 4. What human writing does instead

- **Specific nouns:** "a second-hand monitor next to my desk", not "technology".
- **Odd, true details** only this applicant would know (the slides with moving backgrounds, the editor the school used).
- **Plain verbs:** made, built, asked, broke, fixed, tried.
- **Register that fits the writer's age and level.** A 17-year-old can be clear and sharp without sounding like a policy paper.
- **Some contractions** in less formal statements (I'm, didn't). Check the program's style; many undergraduate essays are fine with them.
- **A small admission of limits** ("They were simple, but...") which makes the strong claims more believable.

## 5. The read-aloud test

Ask: *would the applicant say this sentence to a teacher they respect?* If not, rewrite it in the words they would use.

## 6. Final checklist

| Check | Pass? |
|---|---|
| Fewer than 3 red-flag words in total | |
| No "not just X but Y" more than once | |
| No more than one triplet per paragraph | |
| Sentence lengths visibly vary | |
| Paragraph lengths visibly vary | |
| Em dashes ≤ about 1 per 150 words | |
| No "In conclusion" / "Ultimately" closing | |
| Every claim has a concrete detail | |
| "Why this place" names at least one specific thing | |
| A friend would say "this sounds like them" | |

`scripts/ps_check.py` automates the word list, the em-dash count and the sentence-length spread. It does not replace reading the text.
