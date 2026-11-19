#!/usr/bin/env python3
"""Quick writing checks for academic text in Indonesian or English.

Usage:
    python text_check.py chapter.md [--lang id|en|auto] [--limit-words N] [--long 40]

Reports word count, paragraph and sentence statistics, very long sentences,
leftover placeholders ([DATA NEEDED], [VERIFY], TODO, XXX, <...>), and
phrases that make academic text read as machine-written or padded.
"signifikan"/"significant" is flagged when no test result (p-value, t, F,
chi-square, "uji t") appears in the same sentence. --strict exits 1 on issues. Standard library only; read the text too.
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from writing_rules import (NOT_JUST, PLACEHOLDER, SIGNIF, TEST_RESULT, detect_lang, is_empty,  # noqa: E402
                           phrase_hits, read_input, repeated_openers, split_sentences, word_hits, word_severity)



WORD = re.compile(r"\b[\w'’-]+\b")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--lang", choices=["id", "en", "auto"], default="auto")
    ap.add_argument("--limit-words", type=int)
    ap.add_argument("--long", type=int, default=40, help="flag sentences longer than this many words")
    ap.add_argument("--strict", action="store_true", help="exit with code 1 if issues are found")
    args = ap.parse_args()
    text = read_input(args.file)
    if is_empty(text):
        print("! Empty input: nothing to check.")
        return 1 if args.strict else 0
    lang = detect_lang(text) if args.lang == "auto" else args.lang
    low = text.lower()

    words = WORD.findall(text)
    paras = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip() and not p.lstrip().startswith("#")]
    sents = split_sentences(text)
    issues = 0

    print(f"Language: {lang}  Words: {len(words)}" + (f" / limit {args.limit_words}" if args.limit_words else ""))
    print(f"Paragraphs: {len(paras)}  Sentences: {len(sents)}")
    if args.limit_words and len(words) > args.limit_words:
        print(f"  ! Over the word limit by {len(words) - args.limit_words}")
        issues += 1

    long_s = [s for s in sents if len(WORD.findall(s)) > args.long]
    if long_s:
        issues += 1
        print(f"  ! {len(long_s)} sentence(s) over {args.long} words, e.g.: {long_s[0][:90]}...")

    strong, context = word_hits(text, lang)
    hits = [f'"{h}"' for h in phrase_hits(text, lang)]
    hits += [f'"{m.group(0)[:60]}"' for m in re.finditer(NOT_JUST[lang], low)]
    hits += [f"{w} x{n}" for w, n in strong.items()]
    possible = [f"{w} x{n}" for w, n in context.items()]
    heavy = repeated_openers(paras, lang)
    print(f"Padding / AI-sounding phrases: {len(hits)}")
    for h in hits:
        print(f"  - {h}")
    if possible:
        print(f"Possible (check context): {', '.join(possible)}")
    if heavy:
        print(f"  ! Paragraphs opened with the same connector: {heavy}")
    # Any padding phrase or strong AI word counts; context words only when they pile up
    if hits or max(0, sum(context.values()) - 2) > 0 or heavy:
        issues += 1

    for s in sents:
        m = SIGNIF.search(s)
        if m and not TEST_RESULT.search(s):
            issues += 1
            print(f"  ! '{m.group(0)}' without a test result in the same sentence: {s[:100]}")
            break

    ph = PLACEHOLDER.findall(text)
    if ph:
        issues += 1
        print(f"Placeholders left: {len(ph)} -> {', '.join(ph[:5])}")

    print("\nResult:", "OK" if issues == 0 else f"{issues} issue group(s) to look at")
    return 1 if (args.strict and issues) else 0


if __name__ == "__main__":
    sys.exit(main())
