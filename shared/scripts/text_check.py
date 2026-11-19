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
import re
import sys

ID_FLAGS = [
    r"di era (?:digital|globalisasi|modern|teknologi)",
    r"seiring (?:dengan )?(?:perkembangan|berkembangnya) (?:zaman|teknologi)",
    r"semakin (?:pesat|berkembang) (?:nya )?(?:perkembangan )?",
    r"tidak dapat dipungkiri",
    r"tak dapat dipungkiri",
    r"memainkan peran (?:yang )?(?:penting|krusial|vital|kunci)",
    r"memegang peranan (?:yang )?(?:penting|krusial)",
    r"merupakan hal yang (?:sangat )?penting",
    r"hal ini menunjukkan bahwa",
    r"dapat disimpulkan bahwa",
    r"oleh karena itu,? (?:dapat|perlu)",
    r"dalam rangka",
    r"sangat(?:lah)? (?:penting|krusial|signifikan)",
    r"berbagai macam",
    r"secara keseluruhan",
]
ID_OPENERS = ["selain itu", "lebih lanjut", "oleh karena itu", "dengan demikian", "di sisi lain", "hal ini"]

EN_FLAGS = [
    r"\bdelve", r"\bpivotal\b", r"\bcrucial\b", r"\bparamount\b", r"\blandscape\b", r"\bleverag",
    r"\brealm\b", r"\btapestry\b", r"\btestament\b", r"\bunderscore", r"\bseamless",
    r"plays? an? (?:vital|crucial|key|pivotal|important) role",
    r"in today'?s (?:rapidly )?(?:evolving|changing|digital|fast-paced)",
    r"it is (?:important|worth|crucial) to note that",
    r"\bnot only\b[^.]{1,80}\bbut also\b",
    r"\bfurthermore\b", r"\bmoreover\b",
]
EN_OPENERS = ["furthermore", "moreover", "additionally", "in addition", "however", "therefore"]

PLACEHOLDER = re.compile(r"\[(?:DATA NEEDED|VERIFY|TODO|CITATION NEEDED|REF)[^\]]*\]|\bTODO\b|\bXXX+\b|<[^<>\n]{2,60}>", re.I)
TEST_NEAR = re.compile(r"p\s*[<=>≤]\s*0?[.,]\d|\bt\s*\(\d|\bF\s*\(\d|χ2|chi-?square|α\s*=|\bsig\.|\bp-value|\buji\s+(?:t|f|chi|anova|mann|wilcoxon|regresi)", re.I)
SIGNIF = re.compile(r"\bsignifikan\w*|\bsignificant(?:ly)?\b", re.I)
WORD = re.compile(r"\b[\w'’-]+\b")


def detect_lang(text: str) -> str:
    low = text.lower()
    id_hits = sum(low.count(w) for w in (" yang ", " dan ", " dengan ", " untuk ", " adalah ", " dalam "))
    en_hits = sum(low.count(w) for w in (" the ", " and ", " with ", " for ", " is ", " of "))
    return "id" if id_hits >= en_hits else "en"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--lang", choices=["id", "en", "auto"], default="auto")
    ap.add_argument("--limit-words", type=int)
    ap.add_argument("--long", type=int, default=40, help="flag sentences longer than this many words")
    ap.add_argument("--strict", action="store_true", help="exit with code 1 if issues are found")
    args = ap.parse_args()
    text = sys.stdin.read() if args.file == "-" else open(args.file, encoding="utf-8").read()
    lang = detect_lang(text) if args.lang == "auto" else args.lang
    low = text.lower()

    words = WORD.findall(text)
    paras = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip() and not p.lstrip().startswith("#")]
    sents = [s for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text)) if WORD.search(s)]
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

    flags = ID_FLAGS if lang == "id" else EN_FLAGS
    openers = ID_OPENERS if lang == "id" else EN_OPENERS
    hits = []
    for f in flags:
        found = [m.group(0) for m in re.finditer(f, low)]
        if found:
            hits.append(f'"{found[0][:50]}" x{len(found)}')
    opener_counts = {o: sum(1 for p in paras if p.strip().lower().startswith(o)) for o in openers}
    heavy = {o: n for o, n in opener_counts.items() if n >= 2}
    print(f"Padding / AI-sounding phrases: {len(hits)}")
    for h in hits:
        print(f"  - {h}")
    if heavy:
        print(f"  ! Paragraphs opened with the same connector: {heavy}")
    if len(hits) >= 3 or heavy:
        issues += 1

    for s in sents:
        m = SIGNIF.search(s)
        if m and not TEST_NEAR.search(s):
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
