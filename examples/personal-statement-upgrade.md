# Example: personal statement, Upgrade mode

> **How this was made.** Claude Code followed `skills/personal-statement/SKILL.md` (Upgrade mode) on the fictional sample [`testing/samples/personal_statement.txt`](../testing/samples/personal_statement.txt) on 19 November 2026. The checker output is copied from real runs of `ps_check.py`. "Rina" is not a real person. Your result will differ by model and by what you tell it.

**Assumed intake:** CityU BSc Data Science, undergraduate with scholarship, 500 words, the application asks that the essay be the applicant's own work, keep the voice.

## Map

1. Paragraph 1: generic AI-sounding opener, then the real story (the father's shop, the notebook, Google Sheets, the Eid pattern).
2. Paragraph 2: self-study and math club, with a leftover placeholder.
3. Paragraph 3: why CityU (a ranking claim nobody checked), three self-praising adjectives, a pleading line.
4. Paragraph 4: the goal, then "In conclusion".

## Keep list

The Surabaya shop and the monthly notebook · Google Sheets and the chart · phone cases before Eid · ordering more stock the next year · half of a free Python course · math club, top 3 in the olympiad selection · tools for small shops like her father's.

## Changes

| What changed | Why |
|---|---|
| Cut "In today's rapidly evolving digital landscape, data science plays a pivotal role…" and "My journey with data began…" | Padding opener; the shop story is a stronger first line |
| Cut "I am passionate, hardworking, and resilient" | Claims without evidence; the story already shows them |
| "CityU is ranked number 1 in Asia for data science" → `[VERIFY: …]` | Unchecked ranking; a specific course or project shows fit better |
| "I really hope you accept me because this is my dream…" → a plain statement of need | Declare, don't plead |
| "[add more achievements here]" → `[ADD DETAIL: …]` | A gap only Rina can fill |
| Cut "In conclusion, I believe I am a perfect fit" | Summary cliché; ends on her goal instead |

## Upgraded text (220 words)

In grade 10, I noticed my father writing each month's sales in a notebook at his small phone accessories shop in Surabaya. I asked if I could put the numbers into Google Sheets. When I made a chart, one thing stood out: phone cases sold much more in the month before Eid. The next year he ordered more stock, and the shop did better.

That chart made me want to learn more. I started a free online Python course and have finished about half of it. I also joined my school's math club and placed in the top 3 of the school olympiad selection. [ADD DETAIL: one more thing you did with data, code or math, if there is one]

I want to study Data Science at CityU because I want to learn to find patterns like the one in my father's notebook properly, with statistics and code. I also want to study in Hong Kong, a global financial hub. [VERIFY: replace the ranking claim with one or two specific things about CityU's BSc Data Science, such as a course or project, checked on CityU's website]

My family cannot afford the full tuition, so a scholarship would decide whether I can take this place.

Later, I want to build tools that help small shops like my father's understand their customers.

## New details (fact trace)

- "with statistics and code": what she wants to learn, not something she has done. Rina should confirm it is how she would put it.
- "a scholarship would decide whether I can take this place": a plainer form of "my family cannot afford to pay the full tuition". Confirm it is true.
- No new names, numbers, tools, places or achievements.

## Check, before vs after (`ps_check.py --limit-words 500`)

| | Before | After |
|---|---|---|
| Words | 217 | 220 |
| AI-tone red flags | 8 | 0 |
| Placeholders | 1 (`[add more achievements here]`) | 2 (`[ADD DETAIL]`, `[VERIFY]`), left on purpose for Rina |
| Sentence length spread (sd) | 6.1 | 5.6 |

## Quick check

- **Skeptic:** "half of a free Python course" is honest. Be ready to say which topics it covered.
- **Tone Detector:** no red-flag phrases left. The voice is a school leaver's.

## Check before submitting

- `[VERIFY]`: one or two real, checked details about CityU's BSc Data Science.
- `[ADD DETAIL]`: fill it, or delete the line.
- Be ready to explain the chart: what was on each axis and how big the pre-Eid jump was.
- The application asks for the applicant's own work: Rina should rewrite any sentence that doesn't sound like her.
