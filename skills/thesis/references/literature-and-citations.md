# Literature and Citations

## 1. Finding sources

Good places to search (use what the student's library gives access to):

- Google Scholar, Semantic Scholar, and the publisher databases the campus subscribes to (IEEE Xplore, ACM Digital Library, ScienceDirect, SpringerLink).
- Indonesian sources: Garuda (Garba Rujukan Digital), SINTA-indexed journals, university repositories.
- Chinese sources: CNKI (中国知网), Wanfang.
- arXiv for recent CS work (note when a paper is a preprint, not peer-reviewed).

Prefer peer-reviewed, recent (often the last 5-10 years for fast-moving fields), and directly relevant work. Classic foundational papers are fine at any age.

## 2. Verify every source

Before a source goes into the thesis:

1. It exists: title, authors, year and venue match a real record (DOI resolves, or the publisher/repository page exists).
2. It says what the thesis claims it says (read at least the abstract and the relevant section).
3. It is the right type of source for the claim (a news article can show that something happened; it cannot prove a scientific result).

**AI tools invent references that look real.** Never paste a citation from a chatbot without checking it. When you (the assistant) suggest a source, find it with a search in this session and give its link or DOI; otherwise do not suggest it.

## 3. Literature matrix

Have the student keep one table while reading:

| Author (year) | Problem | Data | Method | Main result | Limitation | Relevance to my thesis |
|---|---|---|---|---|---|---|

This becomes the "penelitian terdahulu" table and makes the gap visible: look for empty or repeated cells (methods nobody tried on this data, data nobody used, limitations nobody fixed).

## 4. Writing the review

- Organise by theme or approach, not by author.
- For each theme: what is known, how studies disagree, what is missing.
- End with the gap and how this thesis addresses it.
- Paraphrase in your own words and cite; quote only when the exact words matter.

## 5. Citation styles (basics)

Use the style the campus guide names. Do not mix styles.

**APA 7 (author-year)**
- In text: (Santoso, 2023) / Santoso (2023) / (Santoso & Lee, 2023) / (Santoso et al., 2023) for three or more authors.
- Journal: Author, A. A., & Author, B. B. (Year). Title of article. *Journal Name, volume*(issue), pages. https://doi.org/...
- Book: Author, A. A. (Year). *Title of book* (edition). Publisher.
- Web page: Author or Organisation. (Year, Month Day). *Title*. Site. URL

**IEEE (numeric)**
- In text: [1], [2]-[4], numbered in order of first appearance.
- Journal: [1] A. Author and B. Author, "Title of article," *Journal Abbrev.*, vol. x, no. x, pp. xx-xx, Year, doi: ...
- Conference: [2] A. Author, "Title," in *Proc. Conf. Name*, City, Year, pp. xx-xx.

**GB/T 7714** (many Chinese universities): numeric, with a document-type code after the title, e.g. [J] journal, [M] book, [C] conference, [D] thesis.

Reference managers (Zotero, Mendeley) prevent most formatting mistakes. `scripts/cite_check.py` finds citations missing from the reference list and listed references never cited.
