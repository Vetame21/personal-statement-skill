#!/usr/bin/env python3
"""Quick checks for a personal statement, CV text, or any application essay.

Usage:
    python ps_check.py statement.txt [--limit-words 500] [--limit-chars 4000]
    cat statement.txt | python ps_check.py -

Reports word/character counts, paragraph lengths, sentence-length spread,
em-dash density, leftover placeholders, and AI-sounding phrases
(see references/shared/anti-ai-tone.md). Standard library only.
"""

import argparse
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from writing_rules import (NOT_JUST, PLACEHOLDER, detect_lang, is_empty, phrase_hits, read_input,  # noqa: E402
                           paragraphs, split_sentences, template_signals, word_hits, word_severity)

# Statement-specific phrases on top of the shared lists in writing_rules.py
PS_PHRASES = {
    "en": [
        r"it'?s not about [^.;]{1,60}?[;,—-]\s*it'?s about",
        r"i (?:really |truly |do |sincerely )?hope (?:that )?(?:you|i) (?:will |can |would )?(?:accept|admit|get accepted|be accepted|be admitted)",
        r"please (?:accept|consider|admit) (?:me|my application)",
        r"\bi promise\b",
    ],
    "id": [
        r"saya (?:sangat |benar-benar )?berharap (?:dapat |bisa )?diterima",
        r"mohon (?:untuk )?(?:menerima|diterima|mempertimbangkan) (?:saya|lamaran saya)",
        r"\bsaya berjanji\b",
        r"sejak kecil saya (?:sudah )?(?:bercita-cita|bermimpi|menyukai)",
    ],
}


WORD = re.compile(r"\b[\w'’-]+\b")


def count_words(text: str) -> int:
    return len(WORD.findall(text))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="text/markdown file, or - for stdin")
    ap.add_argument("--limit-words", type=int)
    ap.add_argument("--limit-chars", type=int)
    ap.add_argument("--lang", choices=["en", "id", "auto"], default="auto", help="language of the statement")
    ap.add_argument("--strict", action="store_true", help="exit with code 1 if issues are found")
    args = ap.parse_args()

    text = read_input(args.file)
    if is_empty(text):
        print("! Empty input: nothing to check.")
        return 1 if args.strict else 0
    # Count like Word and application portals: whitespace-separated tokens ("U.S.", "3.85" and URLs are one word)
    words = [tok for tok in text.split() if re.search(r"\w", tok)]
    paras = paragraphs(text)
    sents = split_sentences(text)
    lang = detect_lang(text) if args.lang == "auto" else args.lang
    lens = [count_words(s) for s in sents]
    para_counts = [count_words(p) for p in paras]
    chars_no_space = len(re.sub(r"\s", "", text))

    print(f"Words: {len(words)}" + (f" / limit {args.limit_words}" if args.limit_words else ""))
    print(f"Characters (with spaces): {len(text.strip())}" + (f" / limit {args.limit_chars}" if args.limit_chars else ""))
    print(f"Characters (no spaces): {chars_no_space}")
    print(f"Paragraphs: {len(paras)}  word counts: {para_counts}")
    if lens:
        sd = statistics.pstdev(lens) if len(lens) > 1 else 0
        print(f"Sentences: {len(lens)}  avg {statistics.mean(lens):.1f} words, min {min(lens)}, max {max(lens)}, spread (sd) {sd:.1f}")
        if sd < 4 and len(lens) > 5:
            print("  ! Sentence lengths are very uniform; mix short and long sentences.")

    problems = 0
    if args.limit_words and len(words) > args.limit_words:
        print(f"  ! Over word limit by {len(words) - args.limit_words}.")
        problems += 1
    if args.limit_chars and len(text.strip()) > args.limit_chars:
        print(f"  ! Over character limit by {len(text.strip()) - args.limit_chars}.")
        problems += 1

    dashes = text.count("—")
    per150 = dashes / max(len(words), 1) * 150
    print(f"Em dashes: {dashes} ({per150:.1f} per 150 words)")
    if per150 > 1:
        print("  ! Em-dash density is high; use commas or full stops.")
        problems += 1

    low = text.lower()
    hits = []
    strong, context = word_hits(text, lang)
    hits += [f"{w} x{n}" for w, n in strong.items()]
    hits += [f"{w} x{n} (possible, check context)" for w, n in context.items()]
    found = phrase_hits(text, lang) + [m.group(0) for m in re.finditer(NOT_JUST[lang], low)]
    ps_specific = [m.group(0) for ph in PS_PHRASES[lang] for m in re.finditer(ph, low)]
    found += ps_specific
    hits += [f'"{f[:60]}"' for f in found]
    phrase_count = len(found)
    print(f"Language: {lang}")
    print(f"AI-tone red flags: {len(hits)}")
    for h in hits:
        print(f"  - {h}")
    # Pleading or "it's not about X" lines break the statement's own rules: one is enough to report
    if word_severity(strong, context) + phrase_count >= 3 or ps_specific:
        problems += 1

    template = template_signals(text, lang)
    if template:
        print(f"Template structure (hints, not an AI score): {len(template)}")
        for name, detail in template:
            print(f"  - {name}: {detail}")
        if len(template) >= 2:      # one pattern is a choice; several together read as a formula
            problems += 1

    ph = PLACEHOLDER.findall(text)
    if ph:
        print(f"Placeholders / markers left: {len(ph)}")
        for p in ph:
            print(f"  - {p}")
        problems += 1

    print("\nResult:", "OK" if problems == 0 else f"{problems} issue group(s) to look at")
    return 1 if (args.strict and problems) else 0


if __name__ == "__main__":
    sys.exit(main())
