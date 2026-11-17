# If You Wrote It Yourself and Got Flagged

AI detectors produce false positives, especially for non-native English writers and formulaic genres (see `detectors.md`). This guide helps a student or applicant show that work is their own. It is for **genuine authors**; it is not a script for defending AI-written work submitted against the rules.

## 1. Before anything is flagged: keep a trail

- **Write where history is saved automatically.** Google Docs keeps a revision history; Word keeps version history for files saved in OneDrive or SharePoint. Writing in one document over several sessions creates timestamped evidence of the work growing.
- **Keep everything:** outlines, notes, research links, early drafts, screenshots of sources, feedback from teachers or friends. Do not delete old versions.
- **Keep earlier writing samples** (previous essays, reports, messages in the same style) to show your normal voice.
- **Log any AI use you did make** (date, tool, what for), and disclose it as your course requires. Allowed, disclosed help is not a problem; hidden help is.

## 2. If you are flagged

1. **Stay calm and ask for specifics:** which tool, what score, which passages, and what the institution's policy says about AI-detection results.
2. **Point to the policy and the tool's limits.** Many institutions, and detector vendors themselves, state that an AI score alone should not decide a misconduct case. Ask whether the score is being used as the only evidence. (Reported example: in the UK, the student ombudsman has said the burden of proving misconduct lies with the provider. Check what applies where you study.)
3. **Bring your evidence:**
   - version history showing the text being written and revised over time;
   - outline, notes and sources you used;
   - earlier writing samples in the same voice;
   - if relevant, the research on false positives (non-native writers, formulaic genres).
4. **Offer to explain the work in person:** walk through your argument, why you chose each source, what you changed between drafts. People who wrote the text can usually do this easily; this is often the most convincing evidence.
5. **Keep it in writing:** reply by email, keep copies of everything, and ask what the next step and timeline are. Use the student union, ombudsman or academic advisor if the process seems unfair.

Version history is strong but not always decisive (some reviewers argue AI could have been used at some stage), so combine several kinds of evidence.

## 3. How the humanizer skill helps here

- `humanize_check.py --per-sentence` shows which flagged sentences have real style problems and which are plain facts the detector misread. That helps you explain the report.
- Improving a genuinely human text for clarity is fine; keep the old version too, so the history stays complete.
- Do not run your own text through outside "humanizer" or paraphrasing tools to lower the score: that can trigger bypasser detection and makes the case harder to defend.
