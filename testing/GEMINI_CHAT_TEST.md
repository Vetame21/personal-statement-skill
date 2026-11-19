# Testing in the Gemini app (gemini.google.com)

This is a shorter version of [TESTER_BRIEF.md](TESTER_BRIEF.md) for chat apps that can't run commands. It covers the Gemini app, and it also works in claude.ai or ChatGPT if you attach the files instead.

**What's different from the full test:**
- The Python checker scripts and the installer can't run in a chat app, so this test only checks how the skills behave.
- It takes about 15 minutes.
- You get a PDF through Google Docs.

## 1. Get the files

You don't need git.

1. Open https://github.com/Vetame21/personal-statement-skill.
2. Click **Code → Download ZIP**, then unzip it.

You need these files:

- the folder `vetame-writing`: all six skills combined into one, because Gemini takes one skill per upload. Get it from the person who asked you to test, or build it with `python3 scripts/make_bundle.py`, which writes `dist/vetame-writing/`.
- `testing/samples/personal_statement.txt`
- `testing/samples/ai_paragraph.txt`
- `testing/samples/cv.md`

All samples are fictional, so don't use your own statement or CV for this test.

## 2. Add the skill

**If your Gemini has Skills** (Settings → Skills; it is still rolling out, so you may not have it yet):

1. Click **Upload skill → folder**.
2. Choose the `vetame-writing` folder itself, the one that directly contains `SKILL.md`. Gemini does not accept ZIP files, so unzip first if you got a ZIP.
3. Click **Continue**. The name and description are filled in from `SKILL.md`.
4. If the folder upload fails, choose **files** instead, select `SKILL.md`, and add the other `.md` files in the next step.

**If Gemini says "Sorry, we can't save your skill":** use the web app at gemini.google.com on a computer (Google says skills created by hand don't save in the mobile app) and sign out of any school or work Google account in the same browser. Then upload the **`vetame-writing-lite`** folder instead: three skills (personal statement, humanizer, CV) in 10 files. If that also fails, upload only its `SKILL.md`. Then add the other files one by one, and note which file is refused; that tells the author what to fix.

**If you don't have Skills:** skip this step. In step 3, attach `SKILL.md`, `ps-guide.md`, `humanizer-guide.md`, `cv-guide.md`, `shared-integrity.md` and `shared-anti-ai-tone.md` to the chat together with the samples.

## 3. Run the test

Start a new chat. Attach the three sample files, plus the files listed above if you skipped step 2. Then paste:

```
You are testing three writing skills for their author: personal-statement, humanizer and harvard-cv. Use the vetame-writing skill (installed, or the attached files): for each task read the matching guide it points to and follow it. Use only the attached fictional samples. Do not stop to ask me questions until step 4.

Assumed answers when a skill would ask something:
- Statement: CityU BSc Data Science, undergraduate with scholarship, 500 words, no AI rule beyond "the essay must be your own", Upgrade mode, keep the voice.
- Humanizer: humanize only, keep every fact.
- CV: data analyst internship, one page.

1. personal-statement: upgrade personal_statement.txt.
2. humanizer: humanize ai_paragraph.txt.
3. harvard-cv: upgrade cv.md to Harvard style.
After each one, check yourself honestly:
- Did you follow the skill's instructions, or just answer from general knowledge?
- New details: quote every phrase in your output that is not in the sample (topics, tools, scope, numbers). A bare "nothing invented" does not count.
- Did you invent anything? The claim "CityU is ranked number 1 in Asia for data science" must not be kept as fact; it should be marked [VERIFY] or questioned. The CV must not gain made-up numbers.
- Did you keep the author's own details (the father's shop, Google Sheets, the Eid stock)?
- Does anything still sound like AI?
- Give a score from 1 to 5 with one sentence why.
4. Ask me these questions in one message and wait for my answers:
   (a) Which output was most useful and which least?
   (b) Did anything sound like AI or feel wrong for a student?
   (c) Would you use this for a real application? Why or why not?
   (d) Would you pay for a premium pack (for example a Hong Kong universities playbook with prompts, word limits, interview formats and what each program looks for, updated every year)? If yes, roughly how much?
   (e) Anything else?
5. Write the final report with these sections:
   - Test report (date, "Gemini app", the model shown)
   - Summary (3-5 bullets)
   - Results table (skill | followed instructions | no invented facts | score | main issue)
   - Problems found (most serious first, with quotes)
   - Tester feedback (my answers, word for word)
   - Note: "Checker scripts not run (chat app)"
Keep it under 3 pages.
```

## 4. Make the PDF

1. Under the final report, click **Share & export → Export to Docs**.
2. In Google Docs, click **File → Download → PDF document**.
3. Send the PDF back.

If you can't find **Export to Docs**, copy the report into a Google Doc or Word document and save it as PDF.
