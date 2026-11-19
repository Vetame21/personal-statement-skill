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
import re
import sys
import unicodedata

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


def ref_entries(refs: str):
    entries = set()
    for line in refs.splitlines():
        line = re.sub(r"^\s*(?:[-*]|\d+[.)])\s+", "", line).strip()
        m = re.search(r"\((" + YEAR + r")\)", line)
        if not line or not m:
            continue
        author_part = line[: m.start()]
        # person: "Lee, J., & Park, S." -> before first comma; corporate: "World Health Organization."
        first = author_part.split(",")[0] if "," in author_part else author_part
        entries.add((norm(first), m.group(1)))
    return entries


PAREN = re.compile(r"\(([^()]*?(?:" + YEAR + r")[^()]*?)\)")
IN_PAREN = re.compile(r"([^;]*?),?\s+(" + YEAR + r")(?:,\s*(?:p|pp|hlm|hal)\.?\s*[\d\-–]+)?\s*$")
NARRATIVE = re.compile(r"((?:[\w'’\-.&]+\s+){0,6}?[\w'’\-.]+)\s+\((" + YEAR + r")\)")


def best_key(candidate: str, year: str, known: set) -> str:
    """Find the first author in the words before '(year)' of a narrative citation."""
    cand = re.sub(r"\b(?:et\s+al\.?|dkk\.?)\s*$", "", candidate.strip(), flags=re.I).strip()
    # drop the last co-author: "Kurniawan dan Sari" -> "Kurniawan"
    cand = re.sub(r"\s+(?:&|and|dan)\s+(?:\S+\s+)?\S+$", "", cand).strip(" ,")
    words = cand.split()
    names = {a for a, _ in known}
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
    listed = ref_entries(refs)
    cited = set()
    paren_spans = []
    for m in PAREN.finditer(body):
        paren_spans.append(m.span())
        for part in m.group(1).split(";"):
            pm = IN_PAREN.search(part.strip())
            if pm and not re.search(r"[A-Za-z]", pm.group(1)):
                continue  # just "(2019)" after a narrative citation
            if pm and re.search(r"[A-Za-z]", pm.group(1)):
                key = first_author(pm.group(1))
                if (key, pm.group(2)) not in listed:
                    key = best_key(pm.group(1), pm.group(2), listed) or key
                cited.add((key, pm.group(2)))
    for m in NARRATIVE.finditer(body):
        if any(s < m.start() and m.end() <= e for s, e in paren_spans):
            continue  # inside a larger parenthesis, already handled
        key = best_key(m.group(1), m.group(2), listed)
        if key and key[:1].isalpha():
            cited.add((key, m.group(2)))

    print(f"Style: APA / author-year. Cited works: {len(cited)}  Reference entries: {len(listed)}")
    missing = sorted(cited - listed)
    unused = sorted(listed - cited)
    for a, y in missing:
        print(f"  ! Cited but not in references: {a.title()} ({y})")
    for a, y in unused:
        print(f"  ! In references but never cited: {a.title()} ({y})")
    return len(missing) + len(unused)


# ---------- IEEE ----------
RANGE = re.compile(r"(?<![\w\])])\[(\d+)\]\s*[-–]\s*\[(\d+)\]")
BRACKET = re.compile(r"(?<![\w\])])\[(\d+(?:\s*[-–,]\s*\d+)*)\]")
REF_IEEE = re.compile(r"^\s*\[(\d+)\]", re.M)


def expand(group: str):
    nums = []
    for part in re.split(r"\s*,\s*", group):
        if re.search(r"[-–]", part):
            a, b = [int(x) for x in re.split(r"\s*[-–]\s*", part)]
            nums.extend(range(a, b + 1))
        elif part.strip():
            nums.append(int(part))
    return nums


def ieee(body: str, refs: str) -> int:
    order = []

    def add(nums):
        for n in nums:
            if n not in order:
                order.append(n)

    spans = []
    for m in RANGE.finditer(body):
        spans.append(m.span())
    events = [(m.start(), list(range(int(m.group(1)), int(m.group(2)) + 1))) for m in RANGE.finditer(body)]
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
    text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    body, refs = split_body_refs(strip_code(text))
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
