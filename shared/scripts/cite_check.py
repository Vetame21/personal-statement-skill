#!/usr/bin/env python3
"""Check that in-text citations and the reference list match.

Usage:
    python cite_check.py thesis.md [--style apa|ieee|auto]

The reference list is everything after a heading named one of:
References, Bibliography, Daftar Pustaka, Referensi, 参考文献
(Markdown "#" headings or a line with only that word).

APA / author-year: finds (Santoso, 2023), (Santoso & Lee, 2023a),
(Santoso et al., 2023; Lee, 2021), Santoso (2023), and matches them to
reference entries by first-author surname + year.
IEEE / numeric: finds [1], [2]-[4], [1, 3, 5] and checks they exist in a
numbered reference list and are first cited in order.

It reports citations with no reference, references never cited, and
(IEEE) out-of-order first citations. Standard library only. It is a
helper: unusual names or formats may need a manual check.
"""

import argparse
import re
import sys
import unicodedata

REF_HEADINGS = re.compile(
    r"^\s*(?:#+\s*)?(references|bibliography|daftar\s+pustaka|referensi|参考文献)\s*:?\s*$",
    re.I | re.M,
)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower().strip()


def split_body_refs(text: str):
    m = None
    for m in REF_HEADINGS.finditer(text):
        pass  # last matching heading wins (a contents page may mention it earlier)
    if not m:
        return text, ""
    return text[: m.start()], text[m.end():]


# ---------- APA ----------
NAME = r"[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’\-]+(?:\s+(?:van|de|der|von|da|di)\s+[A-Z][A-Za-zÀ-ÖØ-öø-ÿ'’\-]+)?"
YEAR = r"(?:19|20)\d{2}[a-z]?|n\.d\."
PAREN = re.compile(r"\(([^()]*?(?:" + YEAR + r")[^()]*?)\)")
ONE = re.compile(r"(" + NAME + r")(?:\s+(?:et\s+al\.|dkk\.)|\s*(?:&|and|dan)\s*" + NAME + r")?,?\s+(" + YEAR + r")")
NARRATIVE = re.compile(r"(" + NAME + r")(?:\s+(?:et\s+al\.|dkk\.)|\s+(?:&|and|dan)\s+" + NAME + r")?\s+\((" + YEAR + r")\)")
REF_APA = re.compile(r"^\s*(?:[-*]\s+)?(" + NAME + r"),?.*?\((" + YEAR + r")", re.M)


def apa(body: str, refs: str) -> int:
    cited = set()
    for m in PAREN.finditer(body):
        for part in m.group(1).split(";"):
            for n in ONE.finditer(part):
                cited.add((norm(n.group(1)), n.group(2)))
    for n in NARRATIVE.finditer(body):
        cited.add((norm(n.group(1)), n.group(2)))
    listed = {(norm(m.group(1)), m.group(2)) for m in REF_APA.finditer(refs)}

    print(f"Style: APA / author-year. Cited works: {len(cited)}  Reference entries: {len(listed)}")
    missing = sorted(cited - listed)
    unused = sorted(listed - cited)
    for a, y in missing:
        print(f"  ! Cited but not in references: {a.title()} ({y})")
    for a, y in unused:
        print(f"  ! In references but never cited: {a.title()} ({y})")
    return len(missing) + len(unused)


# ---------- IEEE ----------
BRACKET = re.compile(r"\[(\d+(?:\s*[-–,]\s*\d+)*)\]")
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
    for m in BRACKET.finditer(body):
        for n in expand(m.group(1)):
            if n not in order:
                order.append(n)
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
        first_bad = next(i for i, (a, b) in enumerate(zip(order, expected)) if a != b)
        print(f"  ! First citations are not in numeric order (first mismatch: [{order[first_bad]}] appears where [{expected[first_bad]}] was expected)")
        problems += 1
    if listed and listed != list(range(1, len(listed) + 1)):
        print("  ! Reference numbers are not continuous from [1]")
        problems += 1
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--style", choices=["apa", "ieee", "auto"], default="auto")
    args = ap.parse_args()
    text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    body, refs = split_body_refs(text)
    if not refs:
        print("! No reference list heading found (References / Daftar Pustaka / Bibliography / Referensi / 参考文献).")
        return 1
    style = args.style
    if style == "auto":
        style = "ieee" if len(REF_IEEE.findall(refs)) >= max(1, len(REF_APA.findall(refs))) else "apa"
    problems = ieee(body, refs) if style == "ieee" else apa(body, refs)
    print("\nResult:", "OK" if problems == 0 else f"{problems} issue(s) to check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
