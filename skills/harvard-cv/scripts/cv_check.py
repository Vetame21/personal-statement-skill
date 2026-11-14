#!/usr/bin/env python3
"""Lint a Harvard-style CV written as plain text or Markdown.

Usage:
    python cv_check.py cv.md
    cat cv.txt | python cv_check.py -

Checks bullets for weak openers, personal pronouns, buzzwords, length and
results; checks date-format consistency and rough one-page length.
Standard library only. It is a helper, not a judge: read the CV too.
"""

import re
import sys

BULLET = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s+(.*)$")
WEAK_OPENERS = ("responsible", "helped", "assisted in", "worked on", "participated",
                "was ", "were ", "involved", "duties", "tasks included", "in charge")
# "I" counts only at the start of a bullet or clause, so "Calculus I and II" passes
PRONOUNS = re.compile(r"(?:^|[.;:,]\s*|\band\s+)I\s+[a-z]|\b(?:[Mm]e|[Mm]y|[Mm]ine|[Ww]e|[Oo]ur|[Uu]s)\b")
BUZZWORDS = ["results-driven", "passionate", "dynamic", "synergy", "synergies", "spearheaded",
             "leverag", "utilized", "utilised", "detail-oriented", "team player",
             "go-getter", "hard-working", "hardworking", "self-starter", "successfully",
             "innovative solutions", "think outside the box", "best-in-class"]
NUMBER = re.compile(r"\d|\b(one|two|three|four|five|six|seven|eight|nine|ten|dozens?|hundreds?)\b", re.I)
DATE_STYLES = {
    "Mon YYYY": re.compile(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.? \d{4}\b"),
    "Month YYYY": re.compile(r"\b(?:January|February|March|April|June|July|August|September|October|November|December) \d{4}\b"),
    "MM/YYYY": re.compile(r"\b\d{1,2}/\d{4}\b"),
}


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = sys.argv[1]
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = text.splitlines()
    bullets = [(i + 1, m.group(1).strip()) for i, l in enumerate(lines) if (m := BULLET.match(l))]

    issues = 0
    print(f"Lines: {len(lines)}  Words: {len(text.split())}  Bullets: {len(bullets)}")
    if len(text.split()) > 650:
        print("  ! Over ~650 words: likely more than one page for a student CV.")
        issues += 1

    with_numbers = 0
    first_verbs = {}
    for ln, b in bullets:
        low = b.lower()
        notes = []
        if low.startswith(WEAK_OPENERS):
            notes.append("weak opener")
        if PRONOUNS.search(b):
            notes.append("personal pronoun")
        for w in BUZZWORDS:
            if w in low:
                notes.append(f"buzzword '{w}'")
        words = len(b.split())
        if words > 32:
            notes.append(f"long ({words} words)")
        if NUMBER.search(b):
            with_numbers += 1
        first = re.sub(r"[^a-z]", "", low.split()[0]) if low.split() else ""
        first_verbs[first] = first_verbs.get(first, 0) + 1
        if notes:
            issues += 1
            print(f"  line {ln}: {', '.join(notes)} -> {b[:70]}")

    if bullets:
        share = with_numbers / len(bullets)
        print(f"Bullets with a number/scale: {with_numbers}/{len(bullets)} ({share:.0%})")
        if share < 0.5:
            print("  ! Fewer than half the bullets show a number, scale or outcome.")
            issues += 1
    repeats = {v: n for v, n in first_verbs.items() if n > 2 and v}
    if repeats:
        print(f"  ! Verbs used more than twice: {repeats}")
        issues += 1

    used = [name for name, rx in DATE_STYLES.items() if rx.search(text)]
    if len(used) > 1:
        print(f"  ! Mixed date formats: {used}")
        issues += 1

    if re.search(r"references available", text, re.I):
        print("  ! Remove 'References available upon request'.")
        issues += 1
    if re.search(r"\[VERIFY", text):
        print(f"  ! Unresolved [VERIFY] markers: {len(re.findall(r'\[VERIFY', text))}")
        issues += 1

    print("\nResult:", "OK" if issues == 0 else f"{issues} item(s) to look at")
    return 0


if __name__ == "__main__":
    sys.exit(main())
