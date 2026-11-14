#!/usr/bin/env python3
"""Quick checks for a personal statement, CV text, or any application essay.

Usage:
    python ps_check.py statement.txt [--limit-words 500] [--limit-chars 4000]
    cat statement.txt | python ps_check.py -

Reports word/character counts, paragraph lengths, sentence-length spread,
em-dash density, leftover placeholders, and AI-sounding phrases
(see references/anti-ai-tone.md). Standard library only.
"""

import argparse
import re
import statistics
import sys

RED_FLAG_WORDS = [
    "delve", "tapestry", "testament", "pivotal", "crucial", "paramount",
    "embark", "realm", "landscape", "foster", "cultivate", "nurture",
    "leverage", "harness", "utilize", "navigate", "unwavering", "steadfast",
    "relentless", "ignite", "seamless", "robust", "cutting-edge", "beacon",
    "cornerstone", "linchpin", "poised", "multifaceted", "intricate",
    "nuanced", "profound", "underscore", "resonate", "journey", "passion",
]
RED_FLAG_PHRASES = [
    r"not (?:just|only|merely) [^.;]{1,60}?(?:,|;|—|-)?\s*but",
    r"it'?s not about [^.;]{1,60}?[;,—-]\s*it'?s about",
    r"in today'?s (?:fast-paced|ever-evolving|rapidly changing)",
    r"a unique blend of",
    r"\bin conclusion\b",
    r"\ball in all\b",
    r"\bultimately,",
    r"this (?:experience )?taught me the importance of",
    r"have you ever wondered",
    r"knows no bounds",
    r"golden ticket",
    r"make the world a better place",
    r"i (?:really|truly|do) hope (?:you|i) (?:will |can )?(?:accept|get accepted)",
    r"\bi promise\b",
]
PLACEHOLDER = re.compile(r"<[^>]{2,60}>|\[(?:VERIFY|MS\d|TODO|XX)[^\]]*\]|\bTBD\b|\bXXX+\b", re.I)


WORD = re.compile(r"\b[\w'’-]+\b")


def count_words(text: str) -> int:
    return len(WORD.findall(text))


def sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if re.search(r"[A-Za-z]", p)]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="text/markdown file, or - for stdin")
    ap.add_argument("--limit-words", type=int)
    ap.add_argument("--limit-chars", type=int)
    args = ap.parse_args()

    text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    words = WORD.findall(text)
    paras = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    sents = sentences(text)
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
    for w in RED_FLAG_WORDS:
        n = len(re.findall(rf"\b{re.escape(w)}\w*", low))
        if n:
            hits.append(f"{w} x{n}")
    for ph in RED_FLAG_PHRASES:
        for m in re.finditer(ph, low):
            hits.append(f'"{m.group(0)[:60]}"')
    print(f"AI-tone red flags: {len(hits)}")
    for h in hits:
        print(f"  - {h}")
    if len(hits) >= 3:
        problems += 1

    ph = PLACEHOLDER.findall(text)
    if ph:
        print(f"Placeholders / markers left: {len(ph)}")
        for p in ph:
            print(f"  - {p}")
        problems += 1

    print("\nResult:", "OK" if problems == 0 else f"{problems} issue group(s) to look at")
    return 0


if __name__ == "__main__":
    sys.exit(main())
