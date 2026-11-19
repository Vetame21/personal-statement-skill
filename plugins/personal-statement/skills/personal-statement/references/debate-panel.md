# Debate Panel

Two debates are available: one **before writing** (decide what the statement should say) and one **after the draft** (attack the draft before a real reader does). They run in Build mode, when new content or facts are added, or on request. A light polish gets the **quick Check** instead (end of this file).

The rules in `shared/debate-rules.md` apply to every panelist: no instant agreement, research before any factual verdict, steelman the other side, and change position only for evidence or a better argument.

---

## The panel

| Panelist | Reads as | Pushes for | Typical attack |
|---|---|---|---|
| **Admissions Reader** | A tired committee member with 2 minutes and 300 other files | Clarity, fit with the program, a reason to remember this applicant | "I can't tell why *this* program by paragraph 3." |
| **Skeptic** (fact-checker) | An interviewer who will ask about every claim | Truth, verifiable facts, sources, interview safety | "Did she actually build this? Where does the HK$8 billion come from?" |
| **Applicant Advocate** | The applicant's friend who knows their voice | Keeping the original story, voice and details | "That rewrite sounds like a consultant, not a 17-year-old." |
| **Tone Detector** | Someone who has read too many AI-written essays | Human rhythm, plain words | "Three triplets and a 'not just X but Y' in one paragraph." |
| **Moderator** (you) | Neutral | A decision | Writes the verdicts and the final call |

For scholarship statements, the Admissions Reader also reads as a **Scholarship Panelist** ("will this money produce a good outcome?"). For job applications, use a **Hiring Manager** instead.

---

## How to run the panelists

- **Independent first, then clash.** Write each panelist's position *before* reading the others, so they do not just agree with whoever spoke first. Then each panelist answers one other panelist's strongest point (agree or rebut, with a reason).
- **Subagents.** When the environment can run subagents and the user has asked for a panel debate or a "deep" debate, run each panelist as its own subagent in parallel (give each the draft, the context, its role row above, and these rules), then moderate their outputs. Otherwise, play the roles yourself in sequence, keeping each one's view separate.
- **Research.** Any factual point in dispute (a statistic, a program detail, a word limit, how a program describes itself) gets searched before a verdict. No search tool → mark that verdict *provisional*.
- **Rounds.** *Quick* (default): one round of positions + one clash. *Deep* (on request, or for high-stakes applications): two clash rounds.
- **Length.** Panelists speak in bullets, not essays. The whole debate should fit on one screen in quick mode.

---

## Debate 1: before writing

Run at the end of step 2 (Angle) in Build mode, and before the rewrite in Upgrade mode.

**1. Pick the motions.** Turn the open decisions into 2-5 short motions, for example:

- "The opening should be the cousin-and-monitor scene."
- "Include the 2026 AI-fraud fact about Hong Kong."
- "Mention the second-choice program (CFFT) in one sentence only."
- "Write in a casual register with contractions."
- "Add a scholarship paragraph."

Always include at least one motion about **the main story** and one about **anything the user wants added**.

**2. Debate each motion.** Each panelist: For / Against / Conditional, with one reason. Skeptic adds evidence or a `[VERIFY]` flag.

**3. Moderator verdicts.**

| # | Motion | Verdict | Why (strongest reason) | Condition |
|---|---|---|---|---|
| 1 | ... | Adopt / Reject / Adopt with change / User's call | ... | ... |

"User's call" is for preferences (tone, which story feels like them) once the facts are clear.

**4. Lock the plan.** The outline is updated to match the verdicts and shown to the user. Writing starts only after the user accepts it or says "go".

---

## Debate 2: after the draft

Run in step 4 (Stress-test) in Build mode, and after the rewrite in Upgrade mode. Run `scripts/ps_check.py` first and give the results to the Tone Detector.

**1. Attacks.** Each panelist names its **top 3 problems**, each with a short quote from the draft and a proposed fix.

**2. Clash.** Each panelist answers the strongest point of one other panelist. Typical clashes:
- Advocate vs Admissions Reader: voice vs clarity.
- Skeptic vs Advocate: a vivid detail that cannot be verified.
- Tone Detector vs Admissions Reader: a punchy line that sounds generated.

**3. Moderator verdicts.**

| # | Issue (quote) | Raised by | Verdict | Fix |
|---|---|---|---|---|
| 1 | "..." | Skeptic | Fix now / Keep / User's call | ... |

**4. Apply.** Apply "Fix now" items at the lightest touch (respect Upgrade mode). List "User's call" items as questions. Show the revised statement, then the **"Check before submitting"** list.

**5. Final score** (one line each, 1-5): Clarity · Fit · Truth/verifiability · Voice · Human tone. Anything below 4 gets one sentence on why and what would raise it.

---

## Output format (quick mode)

```
### Debate 1: before writing
| # | Motion | Verdict | Why | Condition |
...
Locked plan: <3-6 bullet outline>

### Debate 2: after the draft
Attacks
- Admissions Reader: 1) "..." → fix  2) ...  3) ...
- Skeptic: ...
- Applicant Advocate: ...
- Tone Detector: (ps_check: N red flags, N words) ...
Clash
- Advocate → Reader: ...
- Skeptic → Advocate: ...
Verdicts
| # | Issue | Raised by | Verdict | Fix |
Score: Clarity 4 · Fit 5 · Truth 3 (two [VERIFY] left) · Voice 5 · Human tone 4
```

Use the user's language for the debate, and the application's language for quotes and fixes.

## Quick Check (light polish)

After a light rewrite, give one short list instead of the panel: up to 5 bullets of what the Skeptic (facts, `[VERIFY]` items, claims that need a source) and the Tone Detector (`ps_check.py` flags, register) would raise, each with its fix. No approval stop, no scores.

## Skipping

The user can say "skip debate", "no debate", or "quick only". Respect it. Note once that the post-draft check was skipped, and still run `ps_check.py` and the `[VERIFY]` sweep, because those protect the applicant.
