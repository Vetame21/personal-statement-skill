#!/usr/bin/env python3
"""Check that in-text citations and the reference list match.

Usage:
    python cite_check.py thesis.md [--style apa|ieee|auto] [--strict]

The reference list is everything after the last heading named one of:
References, Bibliography, Daftar Pustaka, Referensi, 参考文献
(Markdown "#" headings or a line with only that word).

APA / author-year
  In text: (Santoso, 2023), (Santoso & Lee, 2023a), (Santoso, Lee, & Park, 2021),
  (Santoso et al., 2023; Lee, 2021), (World Health Organization, 2020),
  Santoso (2023), van Dijk (2019), Wijaya et al. (2022), (Darwin, 1859), (Lee, n.d.).
  Matched to reference entries by first author + year.
IEEE / numeric
  In text: [1], [1, 3, 5], [2]-[4], [2-4]. Brackets attached to a word
  (arr[7], x[0]) and code spans or fenced code blocks are ignored.

Reports citations with no reference, references never cited, and (IEEE)
out-of-order first citations. --strict exits with code 1 when issues are found.
Standard library only; unusual formats may still need a manual check.
"""

import argparse
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from writing_rules import read_input  # noqa: E402

REF_HEADINGS = re.compile(
    r"^\s*(?:#+\s*)?(references|bibliography|daftar\s+pustaka|referensi|参考文献)\s*:?\s*$",
    re.I | re.M,
)
YEAR = r"(?:1[5-9]|20)\d{2}[a-z]?|n\.d\."
PARTICLES = {"van", "von", "de", "der", "den", "da", "di", "du", "del", "della", "la", "le", "bin", "binti", "al"}
LEAD_WORDS = {"see", "e.g.", "e.g.,", "cf.", "i.e.", "lihat", "misalnya", "also", "and", "dan", "in", "by", "oleh"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip(" .,;:").lower()


def strip_code(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"~~~.*?~~~", " ", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", " ", text)


def split_body_refs(text: str):
    last = None
    for last in REF_HEADINGS.finditer(text):
        pass  # the last matching heading wins (a contents page may mention it earlier)
    if not last:
        return text, ""
    return text[: last.start()], text[last.end():]


# ---------- APA ----------

def first_author(author_part: str) -> str:
    """'Santoso, Lee, & Park' -> 'santoso'; 'World Health Organization' -> 'world health organization'."""
    a = re.sub(r"\b(?:et\s+al\.?|dkk\.?)", "", author_part, flags=re.I)
    a = re.split(r",|\s&\s|\s+and\s+|\s+dan\s+", a)[0]
    words = a.split()
    while words and words[0].lower() in LEAD_WORDS:
        words = words[1:]
    return norm(" ".join(words))


REF_YEAR = re.compile(r"\((" + YEAR + r")(?:,[^)]*)?\)|(?<=[\s.])(" + YEAR + r")\.(?=\s|$)")


def ref_entries(refs: str):
    """Return a list of (aliases, year). Handles (2020), (2021, March 5) and the Indonesian 'Nama, A. 2020.' style.
    'World Health Organization [WHO]. (2020)' gets both the full name and 'who' as aliases."""
    entries = []
    for line in refs.splitlines():
        line = re.sub(r"^\s*(?:[-*]|\d+[.)])\s+", "", line).strip()
        m = REF_YEAR.search(line)
        if not line or not m:
            continue
        year = m.group(1) or m.group(2)
        author_part = line[: m.start()]
        aliases = set()
        abbr = re.search(r"\[([A-Z][A-Za-z0-9&.\- ]{1,15})\]", author_part)
        if abbr:
            aliases.add(norm(abbr.group(1)))
            author_part = author_part[: abbr.start()]
        first = author_part.split(",")[0] if "," in author_part else author_part
        aliases.add(norm(first))
        entries.append((frozenset(a for a in aliases if a), year))
    return entries


def known_names(entries):
    return {a for aliases, _ in entries for a in aliases}


PAREN = re.compile(r"\(([^()]*?(?:" + YEAR + r")[^()]*?)\)")
IN_PAREN = re.compile(r"([^;]*?),?\s+(" + YEAR + r")(?:,\s*(?:p|pp|hlm|hal)\.?\s*[\d\-–]+)?\s*$")
NARRATIVE = re.compile(r"((?:[\w'’\-.&,]+\s+){0,6}?[\w'’\-.]+)\s+\((" + YEAR + r")\)")


def best_key(candidate: str, year: str, known: set) -> str:
    """Find the first author in the words before '(year)' of a narrative citation."""
    cand = re.sub(r"['’]s$", "", candidate.strip())
    cand = re.sub(r"\b(?:et\s+al\.?|dkk\.?)\s*$", "", cand, flags=re.I).strip()
    # drop the last co-author: "Kurniawan dan Sari" -> "Kurniawan"; "Santoso, Lee, and Park" -> "Santoso, Lee"
    cand = re.sub(r",?\s+(?:&|and|dan)\s+(?:\S+\s+)?\S+$", "", cand).strip(" ,")
    names = known_names(known)
    if "," in cand:
        # "However, Santoso, Lee" -> try each comma segment from the left, keep the first known name
        segments = [seg.strip() for seg in cand.split(",") if seg.strip()]
        for seg in segments:
            seg_words = seg.split()
            for i in range(len(seg_words)):
                if norm(" ".join(seg_words[i:])) in names:
                    return norm(" ".join(seg_words[i:]))
        cand = segments[-1] if segments else cand
    words = cand.split()
    for i in range(len(words)):
        key = norm(" ".join(words[i:]))
        if key in names:
            return key
    if not words or not words[-1][:1].isupper():
        return ""
    tail = [words[-1]]
    for w in reversed(words[:-1]):
        if w.lower() in PARTICLES:
            tail.insert(0, w)
        else:
            break
    return norm(" ".join(tail))


def apa(body: str, refs: str) -> int:
    entries = ref_entries(refs)
    listed = {(a, y) for aliases, y in entries for a in aliases}
    cited = set()
    paren_spans = []
    for m in PAREN.finditer(body):
        paren_spans.append(m.span())
        for part in m.group(1).split(";"):
            pm = IN_PAREN.search(part.strip())
            if pm and not re.search(r"[A-Za-z]", pm.group(1)):
                continue  # just "(2019)" after a narrative citation
            if pm and re.search(r"[A-Za-z]", pm.group(1)):
                key = first_author(re.sub(r"['’]s\b", "", pm.group(1)))
                if (key, pm.group(2)) not in listed:
                    key = best_key(pm.group(1), pm.group(2), entries) or key
                cited.add((key, pm.group(2)))
    for m in NARRATIVE.finditer(body):
        if any(s < m.start() and m.end() <= e for s, e in paren_spans):
            continue  # inside a larger parenthesis, already handled
        key = best_key(m.group(1), m.group(2), entries)
        if key and key[:1].isalpha():
            cited.add((key, m.group(2)))

    print(f"Style: APA / author-year. Cited works: {len(cited)}  Reference entries: {len(entries)}")
    missing = sorted(cited - listed)
    unused = sorted((sorted(aliases, key=len)[-1], y) for aliases, y in entries
                    if not any((a, y) in cited for a in aliases))
    for a, y in missing:
        print(f"  ! Cited but not in references: {a.title()} ({y})")
    for a, y in unused:
        print(f"  ! In references but never cited: {a.title()} ({y})")
    return len(missing) + len(unused)


# ---------- IEEE ----------
# Not preceded by an ASCII letter/digit/_ or ']' (so arr[7] is code, but 张三[1] is a citation)
RANGE = re.compile(r"(?<![A-Za-z0-9_\]])\[(\d+)\]\s*[-–]\s*\[(\d+)\]")
BRACKET = re.compile(r"(?<![A-Za-z0-9_\]])\[(\d+(?:\s*[-–,]\s*\d+)*)\]")
MAX_REF = 999      # numbers above this are not reference numbers (years, intervals)
MAX_RANGE = 200    # longer "ranges" are not citation ranges
REF_IEEE = re.compile(r"^\s*\[(\d+)\]", re.M)


def expand(group: str):
    """Numbers in a bracket group, or [] if it looks like an interval or year span, not a citation."""
    nums = []
    for part in re.split(r"\s*,\s*", group):
        if re.search(r"[-–]", part):
            a, b = [int(x) for x in re.split(r"\s*[-–]\s*", part)]
            if b < a or b - a > MAX_RANGE:
                return []
            nums.extend(range(a, b + 1))
        elif part.strip():
            nums.append(int(part))
    if any(n == 0 or n > MAX_REF for n in nums):
        return []
    return nums


def ieee(body: str, refs: str) -> int:
    order, seen = [], set()

    def add(nums):
        for n in nums:
            if n not in seen:
                seen.add(n)
                order.append(n)

    spans = []
    for m in RANGE.finditer(body):
        spans.append(m.span())
    events = [(m.start(), expand(f"{m.group(1)}-{m.group(2)}")) for m in RANGE.finditer(body)]
    for m in BRACKET.finditer(body):
        if any(s <= m.start() < e for s, e in spans):
            continue
        events.append((m.start(), expand(m.group(1))))
    for _, nums in sorted(events):
        add(nums)

    listed = sorted({int(m.group(1)) for m in REF_IEEE.finditer(refs)})
    print(f"Style: IEEE / numeric. Cited numbers: {len(order)}  Reference entries: {len(listed)}")
    problems = 0
    for n in sorted(set(order) - set(listed)):
        print(f"  ! Cited but not in references: [{n}]")
        problems += 1
    for n in sorted(set(listed) - set(order)):
        print(f"  ! In references but never cited: [{n}]")
        problems += 1
    expected = sorted(order)
    if order != expected:
        i = next(i for i, (a, b) in enumerate(zip(order, expected)) if a != b)
        print(f"  ! First citations are not in numeric order (first mismatch: [{order[i]}] appears where [{expected[i]}] was expected)")
        problems += 1
    if listed and listed != list(range(1, len(listed) + 1)):
        print("  ! Reference numbers are not continuous from [1]")
        problems += 1
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="text/markdown file, or - for stdin")
    ap.add_argument("--style", choices=["apa", "ieee", "auto"], default="auto")
    ap.add_argument("--strict", action="store_true", help="exit with code 1 if issues are found")
    args = ap.parse_args()
    text = read_input(args.file)
    has_heading = bool(REF_HEADINGS.search(text))
    body, refs = split_body_refs(strip_code(text))
    if has_heading and not refs.strip():
        print("! The reference list heading is there, but the list under it is empty.")
        return 1 if args.strict else 0
    if not refs:
        print("! No reference list heading found (References / Daftar Pustaka / Bibliography / Referensi / 参考文献).")
        return 1 if args.strict else 0
    style = args.style
    if style == "auto":
        style = "ieee" if len(REF_IEEE.findall(refs)) >= max(1, len(ref_entries(refs))) else "apa"
    problems = ieee(body, refs) if style == "ieee" else apa(body, refs)
    print("\nResult:", "OK" if problems == 0 else f"{problems} issue(s) to check")
    return 1 if (args.strict and problems) else 0


if __name__ == "__main__":
    sys.exit(main())
