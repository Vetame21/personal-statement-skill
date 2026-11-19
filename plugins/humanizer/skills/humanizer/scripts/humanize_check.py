#!/usr/bin/env python3
"""Find machine-sounding patterns in English or Indonesian text.

Usage:
    python humanize_check.py text.txt [--lang en|id|auto]
    python humanize_check.py --compare before.txt after.txt [--lang auto]
    python humanize_check.py text.txt --per-sentence
    cat text.txt | python humanize_check.py -

Reports AI-typical words and padding phrases, structural patterns
("not just X but Y", triplets, paragraphs opening with the same connector,
moral-of-the-story endings), rhythm (sentence-length spread), em-dash
density and leftover placeholders. With --compare it prints both scans
side by side. It does not estimate "AI probability": it points at
phrases a careful editor would change. Standard library only.
"""

import argparse
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from writing_rules import (FIRST_PERSON, MORAL, NOT_JUST, NUMBER_WORDS, PASSIVE, PLACEHOLDER,  # noqa: E402
                           SIGNIF, TEST_RESULT, TRIPLET, detect_lang, is_empty, phrase_hits, read_input,
                           repeated_openers, split_sentences, unsupported_significance, word_hits, word_severity)

WORD = re.compile(r"\b[\w'’-]+\b")


def scan(text: str, lang: str, register: str = "general") -> dict:
    low = text.lower()
    words = WORD.findall(text)
    paras = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    sents = split_sentences(text)
    lens = [len(WORD.findall(s)) for s in sents]
    strong, context = word_hits(text, lang)
    return {
        "lang": lang,
        "words": len(words),
        "sentences": len(lens),
        "avg_len": statistics.mean(lens) if lens else 0,
        "sd_len": statistics.pstdev(lens) if len(lens) > 1 else 0,
        "strong_words": strong,
        "context_words": context,
        "phrase_hits": phrase_hits(text, lang),
        "not_just": [m.group(0) for m in re.finditer(NOT_JUST[lang], low)],
        "triplets": len(TRIPLET.findall(text)),
        "repeated_openers": repeated_openers(paras, lang),
        "morals": len(re.findall(MORAL[lang], low)),
        "em_dash_per150": text.count("—") / max(len(words), 1) * 150,
        "placeholders": PLACEHOLDER.findall(text),
        # the statistical-significance rule applies to reports and academic writing only
        "unsupported_significance": unsupported_significance(sents) if register != "general" else [],
    }


GENERIC_OPENERS = re.compile(r"^(?:next|then|firstly|secondly|finally|furthermore|moreover|additionally|in addition|overall|selanjutnya|kemudian|selain itu|lebih lanjut)\b,?", re.I)
VAGUE = re.compile(r"\b(?:sharply|significantly|dramatically|greatly|many people|experts? (?:say|agree)|for decades|in recent years|secara signifikan|banyak orang|para ahli|dalam beberapa tahun terakhir)\b", re.I)
STARTERS = {"the", "a", "an", "it", "its", "she", "he", "they", "this", "that", "these", "those", "there",
            "we", "i", "our", "my", "in", "on", "at", "for", "with", "after", "before", "when", "while",
            "next", "then", "first", "finally", "however", "but", "and", "so", "as", "if", "because",
            "ini", "itu", "dia", "mereka", "kami", "saya", "kita", "pada", "dalam", "setelah", "sebelum",
            "namun", "tetapi", "dan", "jadi", "karena", "selain", "kemudian", "selanjutnya", "hal",
            "bab", "bagian", "chapter", "part", "section", "table", "figure", "tabel", "gambar"}
ATTRIBUTION = re.compile(r"\b(?:the|this|her|his|their) (?:film|book|article|study|report|paper|video|talk|author|speaker|documentary|survey)\b|\b(?:film|buku|artikel|penelitian|laporan|video|penulis) ini\b|\baccording to\b|\bmenurut\b", re.I)
CONCRETE = re.compile(r"\d|[A-Z][a-z]+\s[A-Z][a-z]+")


def per_sentence(text: str, lang: str, register: str = "general") -> int:
    flagged = 0
    sents = split_sentences(text)
    # words written with a capital in mid-sentence somewhere = names/proper nouns
    roman = re.compile(r"^[IVXLC]+$")
    names = {t for s in sents for t in WORD.findall(s)[1:]
             if t[:1].isupper() and len(t) > 1 and not roman.match(t)}
    low_words = {t for t in WORD.findall(text) if t.islower()}
    for i, s in enumerate(sents, 1):
        low = s.lower()
        notes = []
        strong, context = word_hits(s, lang)
        notes += [f"word:{w}" for w in strong]
        advisory = [f"advisory: possible AI word '{w}' (fine if literal or natural here)" for w in context]
        notes += [f'phrase:"{ph}"' for ph in phrase_hits(s, lang)]
        if GENERIC_OPENERS.match(s.strip()):
            notes.append("generic transition opener")
        if SIGNIF.search(s) and not TEST_RESULT.search(s):
            if register == "general":
                advisory.append("advisory: 'significant' has a statistical meaning; fine in everyday prose")
            else:
                notes.append("'significant' without a test result")
        if VAGUE.search(s) and not re.search(r"\d", s):
            notes.append("vague claim (no number/source)")
        tokens = WORD.findall(s)
        first = tokens[0] if tokens else ""
        first_is_name = (first[:1].isupper() and first.lower() not in STARTERS
                         and not first.lower().endswith("s") and first.lower() not in low_words)
        has_name = first_is_name or any(t in names for t in tokens[1:])
        has_attribution = bool(ATTRIBUTION.search(low))
        anchored = (CONCRETE.search(s) or NUMBER_WORDS.search(s) or FIRST_PERSON.search(s) or PASSIVE.search(s)
                    or has_name or has_attribution)
        if register == "general" and not anchored and len(tokens) > 6:
            advisory.append("advisory: no concrete anchor (number, name, or writer's voice); fine if the sentence already sounds natural")
        flagged += bool(notes)
        tag = "! " if notes else ("~ " if advisory else "  ")
        print(f"{tag}{i:>2}. {s[:110]}{'...' if len(s) > 110 else ''}")
        for n in notes + advisory:
            print(f"       - {n}")
    print(f"\nSentences with flags: {flagged}/{len(sents)}  (! = fix; ~ = advisory only, not counted)")
    return flagged


def total_flags(r: dict) -> int:
    return (word_severity(r["strong_words"], r["context_words"]) + len(r["phrase_hits"]) + len(r["not_just"])
            + max(0, r["triplets"] - 1) + sum(r["repeated_openers"].values()) + max(0, r["morals"] - 1)
            + len(r["unsupported_significance"]) + (1 if r["em_dash_per150"] > 1 else 0) + (1 if r["sentences"] > 5 and r["sd_len"] < 4 else 0))


def report(r: dict) -> None:
    print(f"Language: {r['lang']}  Words: {r['words']}  Sentences: {r['sentences']}")
    print(f"Sentence length: avg {r['avg_len']:.1f}, spread (sd) {r['sd_len']:.1f}"
          + ("  ! very uniform, mix short and long" if r["sentences"] > 5 and r["sd_len"] < 4 else ""))
    print(f"Em dashes per 150 words: {r['em_dash_per150']:.1f}" + ("  ! high" if r["em_dash_per150"] > 1 else ""))
    if r["strong_words"]:
        print("AI-typical words: " + ", ".join(f"{w} x{n}" for w, n in r["strong_words"].items()))
    if r["context_words"]:
        print("Possible (check context; counted only beyond two): "
              + ", ".join(f"{w} x{n}" for w, n in r["context_words"].items()))
    if r["phrase_hits"]:
        print("Padding / cliché phrases: " + "; ".join(f'"{p}"' for p in r["phrase_hits"]))
    if r["not_just"]:
        print(f"'Not just X but Y' pattern: {len(r['not_just'])}" + ("  ! use at most once" if len(r["not_just"]) > 1 else ""))
    if r["triplets"] > 1:
        print(f"Lists of three: {r['triplets']}  (more than one or two reads as a template)")
    if r["repeated_openers"]:
        print(f"Paragraphs opening with the same connector: {r['repeated_openers']}")
    if r["morals"] > 1:
        print(f"'This taught me...' endings: {r['morals']}  (keep one at most)")
    if r["unsupported_significance"]:
        print(f"'Significant/signifikan' without a test result in the sentence: {len(r['unsupported_significance'])}")
    if r["placeholders"]:
        print(f"Placeholders left: {', '.join(r['placeholders'][:6])}")
    n = total_flags(r)
    level = "light touch" if n <= 3 else "medium" if n <= 8 else "heavy"
    print(f"\nFlags: {n}  ->  {level}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="?")
    ap.add_argument("--compare", nargs=2, metavar=("BEFORE", "AFTER"))
    ap.add_argument("--lang", choices=["en", "id", "auto"], default="auto")
    ap.add_argument("--per-sentence", action="store_true", help="list each sentence with its flags")
    ap.add_argument("--register", choices=["general", "report", "academic"], default="general",
                    help="report/academic: objective prose (lab reports, theses): skip the 'no concrete anchor' advisory "
                         "and require a test result for 'significant'")
    ap.add_argument("--strict", action="store_true",
                    help="exit with code 1 if flags are found (with --compare: if the AFTER text still has flags)")
    args = ap.parse_args()

    load = read_input

    if args.compare:
        a, b = (load(p) for p in args.compare)
        for name, txt in zip(args.compare, (a, b)):
            if is_empty(txt):
                print(f"! Empty input: {name} has no text to compare.")
                return 1 if args.strict else 0
        lang = detect_lang(a) if args.lang == "auto" else args.lang
        ra, rb = scan(a, lang, args.register), scan(b, lang, args.register)
        rows = [
            ("Words", ra["words"], rb["words"]),
            ("Sentence-length spread (sd)", f"{ra['sd_len']:.1f}", f"{rb['sd_len']:.1f}"),
            ("AI-typical words", sum(ra["strong_words"].values()), sum(rb["strong_words"].values())),
            ("Possible (context) words", sum(ra["context_words"].values()), sum(rb["context_words"].values())),
            ("Padding phrases", len(ra["phrase_hits"]), len(rb["phrase_hits"])),
            ("'Not just X but Y'", len(ra["not_just"]), len(rb["not_just"])),
            ("Lists of three", ra["triplets"], rb["triplets"]),
            ("Repeated paragraph openers", sum(ra["repeated_openers"].values()), sum(rb["repeated_openers"].values())),
            ("Em dashes / 150 words", f"{ra['em_dash_per150']:.1f}", f"{rb['em_dash_per150']:.1f}"),
            ("Total flags", total_flags(ra), total_flags(rb)),
        ]
        print(f"{'Check':32} {'Before':>8} {'After':>8}")
        for name, x, y in rows:
            print(f"{name:32} {str(x):>8} {str(y):>8}")
        if ra["words"]:
            change = (rb["words"] - ra["words"]) / ra["words"] * 100
            print(f"\nLength change: {change:+.0f}%" + ("  ! more than ±10%" if abs(change) > 10 else ""))
        return 1 if (args.strict and total_flags(rb)) else 0

    if not args.file:
        ap.error("give a file, '-' for stdin, or --compare BEFORE AFTER")
    text = load(args.file)
    if is_empty(text):
        print("! Empty input: nothing to check.")
        return 1 if args.strict else 0
    lang = detect_lang(text) if args.lang == "auto" else args.lang
    if args.per_sentence:
        flagged = per_sentence(text, lang, args.register)
        return 1 if (args.strict and flagged) else 0
    result = scan(text, lang, args.register)
    report(result)
    return 1 if (args.strict and total_flags(result)) else 0


if __name__ == "__main__":
    sys.exit(main())
