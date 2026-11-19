#!/usr/bin/env python3
"""Lint a Harvard-style CV written as plain text or Markdown.

Usage:
    python cv_check.py cv.md [--strict]
    cat cv.txt | python cv_check.py -

Checks bullets for weak openers, personal pronouns, buzzwords, length and
results; checks date-format consistency and rough one-page length.
Standard library only. It is a helper, not a judge: read the CV too.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from writing_rules import PLACEHOLDER, is_empty, read_input  # noqa: E402

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


# Sections whose bullets are facts or lists, not achievement bullets
NON_ACHIEVEMENT_SECTION = re.compile(r"skills|interests|languages?|coursework|certifications?|bahasa|keahlian", re.I)
NON_ACHIEVEMENT_BULLET = re.compile(r"^(?:relevant\s+)?coursework\b|^(?:cumulative\s+)?gpa\b|^honou?rs\b|^ipk\b|^grades?\b", re.I)
# "## SKILLS", "SKILLS & INTERESTS", "**SKILLS & INTERESTS**" or "__Skills__" on their own line
HEADING = re.compile(r"^\s*(?:#+\s*(.+?)\s*$|([A-Z][A-Z &/]{2,})\s*$|(?:\*\*|__)([^*_]{2,60})(?:\*\*|__)\s*:?\s*$)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="text/markdown file, or - for stdin")
    ap.add_argument("--strict", action="store_true", help="exit with code 1 if issues are found")
    args = ap.parse_args()
    text = read_input(args.file)
    if is_empty(text):
        print("! Empty input: nothing to check.")
        return 1 if args.strict else 0
    lines = text.splitlines()
    bullets = []
    section = ""
    for i, line in enumerate(lines):
        h = HEADING.match(line)
        if h:
            section = h.group(1) or h.group(2) or h.group(3)
            continue
        m = BULLET.match(line)
        if m:
            body = m.group(1).strip()
            counts = not (NON_ACHIEVEMENT_SECTION.search(section) or NON_ACHIEVEMENT_BULLET.search(body))
            bullets.append((i + 1, body, counts))

    issues = 0
    print(f"Lines: {len(lines)}  Words: {len(text.split())}  Bullets: {len(bullets)}")
    if len(text.split()) > 650:
        print("  ! Over ~650 words: likely more than one page for a student CV.")
        issues += 1

    with_numbers = 0
    first_verbs = {}
    achievement = [b for b in bullets if b[2]]
    for ln, b, counts in bullets:
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
        if counts and NUMBER.search(b):
            with_numbers += 1
        if counts:
            first = re.sub(r"[^a-z]", "", low.split()[0]) if low.split() else ""
            first_verbs[first] = first_verbs.get(first, 0) + 1
        if notes:
            issues += 1
            print(f"  line {ln}: {', '.join(notes)} -> {b[:70]}")

    if achievement:
        share = with_numbers / len(achievement)
        print(f"Achievement bullets with a number/scale: {with_numbers}/{len(achievement)} ({share:.0%})")
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
    markers = PLACEHOLDER.findall(text)
    if markers:
        print(f"  ! Unresolved markers or placeholders: {len(markers)} -> {', '.join(markers[:5])}")
        issues += 1

    print("\nResult:", "OK" if issues == 0 else f"{issues} item(s) to look at")
    return 1 if (args.strict and issues) else 0


if __name__ == "__main__":
    sys.exit(main())
