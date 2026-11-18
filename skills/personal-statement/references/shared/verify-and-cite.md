# Verify and Cite

Two problems show up again and again when an assistant improves a statement:

1. The user asks for "realistic" filler, and invented details quietly become "facts" the applicant has to defend.
2. The user asks for current news or statistics, and the numbers come from memory, from a vendor blog, or from a page that contradicts another page.

This file sets the rules for both.

---

## 1. The `[VERIFY]` marker

Use it for **every** detail you did not get from the user or from a cited source.

```
I made a simple website about my hobbies [VERIFY: did she actually build this? what was it about?].
```

Rules:

- In working drafts, keep the markers inline.
- In a "clean" final version, remove inline markers but always print a numbered **"Check before submitting"** list after the text naming each invented detail.
- Never invent: grades, awards, competition results, named projects with outcomes, names of teachers or mentors, employers, dates, numbers.
- Acceptable placeholders to suggest (still marked): the *type* of small project a school leaver often does, the *kind* of reason a student might have for a field. Phrase them simply so they are easy to replace.
- If the user insists on keeping an invented detail without confirming it, warn once that it may be asked about in an interview, then follow their call.

## 2. Adding current facts

Use only when the fact makes the applicant's reasoning stronger (e.g. why this city, why this field now).

**Process**

1. Search. If the environment has a web search tool, use it; use a deeper or "extended" mode for recent events. If no search is available, say so and do not add the fact.
2. Prefer, in order: official bodies (governments, central banks, regulators, universities) → reputable news → industry associations → vendor/consultancy reports. Label vendor numbers as such, or avoid them.
3. Look for a second independent source for any number.
4. If sources conflict, use the safest claim both support, without the disputed number.
5. Write the fact in plain words with no more precision than the sources support ("around HK$8 billion", not "HK$8.03 billion").
6. List sources (title + link) after the draft.
7. Remind the user to recheck dates and figures before submitting, because news ages fast.

**Limits**

- One or two facts per statement. A statement is not a news summary.
- The fact must connect to the applicant (why it matters to *them*), not just to the world.
- Avoid scary or negative framing as the main point; frame problems as something the applicant wants to help solve.
- Avoid politically charged claims unless the applicant's field requires them.

## 3. Checking the applicant's own claims

Before finalising, scan for:

- Technical terms used wrongly (language vs editor vs library; statistics terms; finance terms).
- Program names written exactly as the university writes them.
- Claims about the university (courses, labs, schemes) that came from memory. Look them up or mark `[VERIFY]`.
- Word or character limits taken from third-party sites. Tell the user to confirm on the official portal.

## 4. Verifying an academic source

Before a source goes into any text:

1. It exists: title, authors, year and venue match a real record (DOI resolves, or the publisher or repository page exists).
2. It says what the text claims (read at least the abstract and the relevant section).
3. It is the right kind of source for the claim (news can show that something happened; it cannot prove a scientific result).

When you suggest a source, find it with a search in this session and give its link or DOI; otherwise do not suggest it.
