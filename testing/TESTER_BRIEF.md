# Tester brief: Vetame21 Writing Skills

Thanks for testing. This takes about 20–30 minutes, and most of it is your agent working by itself. At the end you get **one PDF** (`testing/out/report.pdf`) to send back.

## For the human tester

1. Clone the repo and install the skills. Use `py` instead of `python3` on Windows.

   ```bash
   git clone https://github.com/Vetame21/personal-statement-skill
   ```

   ```bash
   python3 personal-statement-skill/scripts/install.py --tools codex
   ```

   If you use another agent, swap `codex` for `claude`, `gemini`, `qwen`, `kimi` or `opencode`.

2. **Restart your agent.** Open it inside the `personal-statement-skill` folder.
3. Paste this prompt and let it run:

   ```
   Read testing/TESTER_BRIEF.md and carry out the section "Task for the agent" from start to finish. Do not stop to ask me anything until step 6.
   ```

4. At step 6 the agent asks you a few short questions. Answer honestly; negative feedback is the useful kind.
5. Send `testing/out/report.pdf` back to the person who asked you to test.

**Privacy:** the test only uses the fictional samples in `testing/samples/`. Don't paste your own statement or CV into this test. The report is meant to be shared, so it should contain nothing personal.

---

## Task for the agent

You are testing a set of Agent Skills on behalf of the repository owner. Work through steps 1–7 in order.

**Rules:**
- **Report, don't fix.** Do not edit any file in the repository except inside `testing/out/`, which you create.
- **Be honest.** If something fails, is confusing, or a skill could not be found, write that down with the exact error. A report that says everything is fine when it isn't is worthless. Never mark a step as passed if you did not run it.
- **Use only the samples** in `testing/samples/`. They are fictional. Do not add personal data about the tester (name, email, paths containing their username: write `~` instead of the home path).
- **Don't stop to ask questions before step 6.** When a skill would normally ask the user something (target program, word limit, AI policy, "humanize only or upgrade too?"), use the answers under "Assumed answers" below and note which ones you used.
- Save the raw output of every step in `testing/out/` (for example `testing/out/step3_ps_check.txt`).

**Assumed answers** for questions a skill asks:
- Personal statement: target is CityU BSc Data Science, undergraduate with scholarship. The limit is 500 words. The application has no AI-use rule beyond "the essay must be your own". The user wants Upgrade mode and to keep the voice.
- Humanizer: "humanize only, keep every fact".
- CV: target is a data analyst internship, one page.
- Report: a Java programming lab report, in Indonesian, APA style.
- Debate: web search may or may not be available. If it is not, say so and give a provisional verdict.

### Step 1: Environment

Record:
- which agent and version you are (run its version command if you can)
- the OS
- the output of `python3 --version` (or `py --version` / `python --version`)
- the output of `git log -1 --format=%h`

### Step 2: Installation

1. Run `python3 scripts/install.py --list`.
2. Run `python3 scripts/install.py --tools <your tool> --dry-run`.
3. Check whether the six skills (debate-mode, harvard-cv, humanizer, personal-statement, report, thesis) are present in the folder your tool reads: list it.
4. Say whether **you can see the skills as skills** (they appear in your skills list, or you can load them by name such as `$humanizer` or `/humanizer`). If you can only read them as plain files, say so.

### Step 3: Checker scripts

Run each command from the repository root and record the exit code and the last 15 lines of output:

```bash
python3 skills/personal-statement/scripts/ps_check.py testing/samples/personal_statement.txt --limit-words 500
python3 skills/humanizer/scripts/humanize_check.py testing/samples/ai_paragraph.txt --per-sentence
python3 skills/harvard-cv/scripts/cv_check.py testing/samples/cv.md
python3 skills/report/scripts/cite_check.py testing/samples/report.md
python3 skills/report/scripts/text_check.py testing/samples/report.md --lang id
python3 -m unittest discover -s tests
```

Each sample starts with a "FICTIONAL SAMPLE" line (and the statement with a "Target" line). The checkers count those lines too, so expect one extra sentence and a few extra words. That is not a bug.

For each checker, the expected behaviour is roughly:
- **personal statement:** flags the placeholder, the pleading line and the cliché opener
- **AI paragraph:** flags the "Furthermore/Moreover" openers and words such as "testament"
- **CV:** flags "Responsible for", "Spearheaded", "I fixed" and bullets with no numbers
- **report:** says Sedgewick (2011) is cited but not listed, Knuth (1998) is listed but not cited, and flags "Di era digital" and "signifikan"

Say whether each checker matched this expectation.

The unit tests may skip or fail the build tests if PyYAML is not installed. If so, record it and note that this is expected.

### Step 4: Skills in use

Use each skill the way a real user would: call it by name, or describe the task so the skill is picked up. Save each full answer to `testing/out/`.

1. **personal-statement**: "Upgrade this personal statement, keep my voice" with `testing/samples/personal_statement.txt`.
2. **humanizer**: humanize `testing/samples/ai_paragraph.txt`.
3. **harvard-cv**: upgrade `testing/samples/cv.md` to Harvard style.
4. **report**: review `testing/samples/report.md` and list what to fix.
5. **debate-mode**: "Debate with facts: should Rina mention that Hong Kong is a global financial hub in her Data Science statement?"
6. **thesis**: "Help me narrow a skripsi topic about sorting algorithms and plan Bab I." Give only an outline.

### Step 5: Score each skill honestly

For each skill in step 4, answer these questions:

- **Loaded?** Did the skill's instructions actually load, or did you just answer from general knowledge?
- **No invented facts?** Did it avoid inventing facts?
  - The sample's claim "CityU is ranked number 1 in Asia for data science" must **not** be kept as fact. It should be marked `[VERIFY]` or questioned.
  - The CV must not gain made-up numbers.
- **Voice kept?** Did it keep the author's own details and voice (the father's shop, Google Sheets, the Eid stock)?
- **Clean output?** Did the output avoid AI-sounding phrasing?
- **Workflow followed?** Did it follow its own workflow (for example, `ps_check.py` run on the rewrite, a change table, a "Check before submitting" list)?
- **Score:** give a 1–5 score with one sentence explaining why.

List every problem you noticed, including small ones:
- confusing instructions
- steps that took too long
- paths that didn't work on this OS
- scripts the skill told you to run that failed

### Step 6: Questions for the tester

Now ask the human these questions in one message, wait for the answers, and copy them into the report word for word:

1. Did installation work the first time? If not, what went wrong?
2. Which skill's output was the most useful, and which was the least useful?
3. Did anything sound "like AI" or feel wrong for a student?
4. Would you use this for a real application, report or thesis? Why or why not?
5. Would you pay for a premium pack (for example, a Hong Kong universities playbook with prompts, word limits, interview formats and what each program looks for, updated every application year)? If yes, roughly how much? If no, what would change your mind?
6. Anything else?

### Step 7: Write the report and make the PDF

Write `testing/out/report.md` with exactly these sections:

```
# Test report: Vetame21 Writing Skills
Date, agent and version, OS, Python version, repo commit

## Summary
3-5 bullets: what worked, what broke, the most important fix

## 1. Installation
## 2. Checker scripts
A table: script | exit code | matched expectation (yes/partly/no) | note
## 3. Skills
A table: skill | loaded (yes/no) | no invented facts (yes/no) | score 1-5 | main issue
Then a short paragraph per skill
## 4. Problems found
A numbered list, most serious first, each with the exact error or quote
## 5. Tester feedback
The answers from step 6, word for word
## 6. Raw output files
List of files in testing/out/
```

Keep it under about 4 pages. Use plain Markdown: headings, bullets, tables and code blocks. No images.

Then make the PDF:

```bash
python3 testing/make_pdf.py testing/out/report.md testing/out/report.pdf
```

If that fails, record the error. If pandoc is installed, try `pandoc testing/out/report.md -o testing/out/report.pdf`, and if neither works, leave the `.md`.

Finish by telling the tester the exact path of the PDF and asking them to send it back.
