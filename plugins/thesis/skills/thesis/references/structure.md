# Thesis Structures and Chapter Checklists

**The campus thesis guide (pedoman penulisan) always wins.** Use these as defaults and to check what a guide leaves out.

---

## A. Indonesian skripsi (Bab I-V)

Front matter (typical): cover, approval pages (lembar pengesahan), statement of originality (pernyataan keaslian), foreword (kata pengantar), abstract (Indonesian + English), table of contents, lists of tables/figures/appendices.

### Bab I Pendahuluan

| Sub-bab | Checklist |
|---|---|
| Latar belakang | Moves from the general situation to the specific problem with evidence (data, cases, prior studies). States the gap. **No long theory here** (that belongs in Bab II). Ends by pointing at the research. |
| Rumusan masalah | 1-3 questions, each answerable with this study's data and method. Usually phrased as questions ("Bagaimana...", "Seberapa besar..."). |
| Tujuan penelitian | One objective per research question, same order and wording. |
| Batasan masalah | Scope: data, place, period, variables, tools. Honest limits, not excuses. |
| Manfaat penelitian | Theoretical and practical; specific to who benefits. Keep it short. |
| Sistematika penulisan | One or two lines per chapter (if the guide requires it). |

### Bab II Tinjauan Pustaka / Landasan Teori

- Previous studies (penelitian terdahulu): 5-15 relevant studies, recent where possible, often as a comparison table (author, year, method, data, result, how this thesis differs).
- Theory and concepts the study actually uses, with sources. Not a textbook summary.
- Framework (kerangka pemikiran) diagram connecting the concepts.
- Hypotheses (for quantitative studies), derived from theory and prior work.
- **Test:** every theory introduced here is used in Bab III or IV.

### Bab III Metodologi Penelitian

- Research type and design (quantitative, qualitative, mixed, experimental, R&D/system development).
- Data: population and sample (and how sampled), sources, period, collection technique, instruments (with validity/reliability checks where relevant).
- Variables and operational definitions (for quantitative work).
- Analysis technique (statistical tests with assumptions checked, or qualitative coding approach), and tools/software.
- For system or model projects: requirements, design, development method (e.g. waterfall, prototyping, CRISP-DM), evaluation plan and metrics.
- Research flow diagram.
- **Test:** someone else could repeat the study from this chapter.

### Bab IV Hasil dan Pembahasan

- Results first: descriptive data, test results, system output, tables and figures with captions.
- Then discussion: what the results mean, compared with prior studies from Bab II (agree / differ / why), answering each research question in order.
- Limitations that affected the results.
- **Test:** every rumusan masalah has a clearly labelled answer here.

### Bab V Kesimpulan dan Saran

- Conclusions: one per research question, short, no new data.
- Suggestions (saran): for practice and for future research, grounded in the findings and limitations. Not generic ("perlu penelitian lebih lanjut" alone is not enough).

Back matter: references (daftar pustaka), appendices (lampiran: instruments, raw data summaries, code listings, permits).

---

## B. International / IMRaD thesis

1. **Abstract** (150-300 words): problem, method, main results with numbers, conclusion.
2. **Introduction**: context, problem, research questions or objectives, contribution, thesis outline.
3. **Background / Literature review**: organised by theme, critical (what each work does well and where it falls short), ending with the gap.
4. **Methodology** (or Design): data, method, setup, justification of choices, evaluation plan.
5. **Results**: what was found, without interpretation.
6. **Discussion**: meaning, comparison with prior work, threats to validity, limitations.
7. **Conclusion and future work**.
8. References, appendices.

Many universities merge 5 and 6, or split 4 into Design and Implementation.

---

## C. CS / engineering design-and-implementation projects

Common at technical universities (including the Chinese "graduation design" track).

1. Introduction: problem, users, objectives, contributions.
2. Related work / existing systems: compare features and approaches in a table.
3. Requirements: functional and non-functional, with priorities.
4. Design: architecture diagram, data model, key algorithms, design decisions and alternatives rejected (and why).
5. Implementation: stack, key modules, interesting problems solved. **Not a code dump**; code goes in appendices or a repository link.
6. Testing and evaluation: test plan, test cases, results, performance numbers, user evaluation if any. Compare with a baseline.
7. Conclusion: what was achieved against the objectives, limitations, future work.

Examiners reward: clear justification of design choices, honest evaluation against a baseline, and evidence that the student understands every part of the system (especially if AI coding tools were used).

---

## D. Chinese universities (本科毕业论文 / 毕业设计)

Typical process (the exact rules are in each university's thesis management measures; for SCUT, the "Full-time Undergraduate Graduation Design (Thesis) Management Measures"):

1. Topic selection (选题) with the supervisor.
2. Task assignment (任务书).
3. **Opening report (开题报告)**: background, literature review, aims, method, schedule, expected results.
4. **Foreign literature translation (外文翻译)**: read and translate professional literature in the field.
5. Design and implementation, with mid-term check (中期检查).
6. Thesis writing.
7. Evaluation by supervisor and reviewer (评阅).
8. Defense (答辩).

Ask whether international students may write in English, the required length, citation style (many Chinese universities use GB/T 7714), and the template.

---

## Chapter-to-chapter consistency map

| Bab I | must match | Later |
|---|---|---|
| Rumusan masalah 1..n | → | Bab IV sections 1..n → Kesimpulan 1..n |
| Tujuan 1..n | → | same order as rumusan masalah |
| Batasan | → | Bab III data and scope |
| Key terms | → | same names and definitions throughout |
| Theories in Bab II | → | used in Bab III design or Bab IV discussion |
