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
import re
import statistics
import sys

EN_WORDS = ["delve", "tapestry", "testament", "pivotal", "crucial", "paramount", "vital", "embark",
            "realm", "landscape", "sphere", "foster", "cultivate", "nurture", "leverag", "harness",
            "utiliz", "utilis", "navigat", "seamless", "robust", "cutting-edge", "unwavering",
            "relentless", "steadfast", "underscor", "resonat", "multifaceted", "intricate",
            "nuanced", "profound", "beacon", "cornerstone", "journey", "passion", "furthermore",
            "moreover", "additionally"]
EN_PHRASES = [
    r"in today'?s (?:rapidly |fast-paced |ever-)?(?:evolving|changing|digital|modern)",
    r"plays? an? (?:vital|crucial|key|pivotal|important|significant) role",
    r"it is (?:important|worth|crucial) (?:to note|noting) that",
    r"a unique blend of", r"\bin conclusion\b", r"\bultimately,", r"\ball in all\b",
    r"have you ever wondered", r"(?:this|it) taught me the importance of",
    r"make the world a better place", r"knows no bounds",
]
EN_NOTJUST = r"\bnot (?:just|only|merely)\b[^.;!?]{1,80}?\bbut\b"
EN_OPENERS = ["furthermore", "moreover", "additionally", "in addition", "however", "therefore", "overall"]
EN_MORAL = r"(?:this|it|that) (?:taught|showed|reminded) me (?:that|the importance|how)"

ID_WORDS = ["signifikan", "krusial", "esensial", "fundamental", "komprehensif", "holistik", "sinergi", "transformatif"]
ID_PHRASES = [
    r"di era (?:digital|globalisasi|modern|teknologi)",
    r"seiring (?:dengan )?(?:perkembangan|berkembangnya) (?:zaman|teknologi)",
    r"tidak dapat dipungkiri", r"tak dapat dipungkiri",
    r"memainkan peran (?:yang )?(?:penting|krusial|vital|kunci)",
    r"memegang peranan (?:yang )?(?:penting|krusial)",
    r"merupakan hal yang (?:sangat )?penting",
    r"hal ini menunjukkan bahwa", r"dapat disimpulkan bahwa", r"dalam rangka",
    r"sangat(?:lah)? (?:penting|krusial)", r"berbagai macam", r"secara keseluruhan",
    r"pernahkah (?:anda|kamu) (?:bertanya|berpikir)",
]
ID_NOTJUST = r"\b(?:bukan|tidak) (?:hanya|sekadar|cuma)\b[^.;!?]{1,80}?\b(?:tetapi|tapi|melainkan)\b"
ID_OPENERS = ["selain itu", "lebih lanjut", "oleh karena itu", "dengan demikian", "di sisi lain", "hal ini", "secara keseluruhan"]
ID_MORAL = r"(?:hal ini|pengalaman ini) (?:mengajarkan|menunjukkan|mengingatkan) (?:saya|kita)"

TRIPLET = re.compile(r"\b\w+(?:\s\w+)?,\s\w+(?:\s\w+)?,?\s(?:and|or|dan|atau|serta)\s\w+")
PLACEHOLDER = re.compile(r"\[(?:ADD DETAIL|DATA NEEDED|VERIFY|TODO)[^\]]*\]|\bTODO\b|\bXXX+\b|<[^<>\n]{2,60}>", re.I)
WORD = re.compile(r"\b[\w'’-]+\b")


def detect_lang(text: str) -> str:
    low = f" {text.lower()} "
    id_hits = sum(low.count(w) for w in (" yang ", " dan ", " dengan ", " untuk ", " adalah ", " dalam ", " saya "))
    en_hits = sum(low.count(w) for w in (" the ", " and ", " with ", " for ", " is ", " of ", " my "))
    return "id" if id_hits > en_hits else "en"


def scan(text: str, lang: str) -> dict:
    low = text.lower()
    words = WORD.findall(text)
    paras = [p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    sents = [s for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text.strip())) if WORD.search(s)]
    lens = [len(WORD.findall(s)) for s in sents]

    if lang == "id":
        word_list, phrases, notjust, openers, moral = ID_WORDS, ID_PHRASES, ID_NOTJUST, ID_OPENERS, ID_MORAL
    else:
        word_list, phrases, notjust, openers, moral = EN_WORDS, EN_PHRASES, EN_NOTJUST, EN_OPENERS, EN_MORAL

    word_hits = {}
    for w in word_list:
        n = len(re.findall(rf"\b{re.escape(w)}\w*", low))
        if n:
            word_hits[w] = n
    phrase_hits = []
    for p in phrases:
        for m in re.finditer(p, low):
            phrase_hits.append(m.group(0))
    opener_counts = {}
    for p in paras:
        start = p.strip().lower()
        for o in openers:
            if start.startswith(o):
                opener_counts[o] = opener_counts.get(o, 0) + 1
    repeated_openers = {o: n for o, n in opener_counts.items() if n >= 2}

    return {
        "lang": lang,
        "words": len(words),
        "sentences": len(lens),
        "avg_len": statistics.mean(lens) if lens else 0,
        "sd_len": statistics.pstdev(lens) if len(lens) > 1 else 0,
        "word_hits": word_hits,
        "phrase_hits": phrase_hits,
        "not_just": [m.group(0) for m in re.finditer(notjust, low)],
        "triplets": len(TRIPLET.findall(text)),
        "repeated_openers": repeated_openers,
        "morals": len(re.findall(moral, low)),
        "em_dash_per150": text.count("—") / max(len(words), 1) * 150,
        "placeholders": PLACEHOLDER.findall(text),
    }


GENERIC_OPENERS = re.compile(r"^(?:next|then|firstly|secondly|finally|furthermore|moreover|additionally|in addition|overall|selanjutnya|kemudian|selain itu|lebih lanjut)\b,?", re.I)
VAGUE = re.compile(r"\b(?:sharply|significantly|dramatically|greatly|many people|experts? (?:say|agree)|for decades|in recent years|secara signifikan|banyak orang|para ahli|dalam beberapa tahun terakhir)\b", re.I)
CONCRETE = re.compile(r"\d|[A-Z][a-z]+\s[A-Z][a-z]+|\b(?:I|my|we|saya|kami|aku)\b")


def per_sentence(text: str, lang: str) -> None:
    words = EN_WORDS if lang == "en" else ID_WORDS
    phrases = EN_PHRASES if lang == "en" else ID_PHRASES
    sents = [s for s in re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", text.strip())) if WORD.search(s)]
    # words written with a capital in mid-sentence somewhere = names/proper nouns
    names = {t for s in sents for t in WORD.findall(s)[1:] if t[:1].isupper()}
    for i, s in enumerate(sents, 1):
        low = s.lower()
        notes = []
        notes += [f"word:{w}" for w in words if re.search(rf"\b{re.escape(w)}\w*", low)]
        notes += [f'phrase:"{m.group(0)}"' for p in phrases for m in re.finditer(p, low)]
        if GENERIC_OPENERS.match(s.strip()):
            notes.append("generic transition opener")
        if VAGUE.search(s) and not re.search(r"\d", s):
            notes.append("vague claim (no number/source)")
        tokens = WORD.findall(s)
        has_name = any(t in names for t in tokens)
        if not (CONCRETE.search(s) or has_name) and len(tokens) > 6:
            notes.append("no concrete anchor (number, name, or writer's voice)")
        tag = "  " if not notes else "! "
        print(f"{tag}{i:>2}. {s[:110]}{'...' if len(s) > 110 else ''}")
        for n in notes:
            print(f"       - {n}")


def total_flags(r: dict) -> int:
    return (sum(r["word_hits"].values()) + len(r["phrase_hits"]) + len(r["not_just"])
            + max(0, r["triplets"] - 1) + sum(r["repeated_openers"].values()) + max(0, r["morals"] - 1)
            + (1 if r["em_dash_per150"] > 1 else 0) + (1 if r["sentences"] > 5 and r["sd_len"] < 4 else 0))


def report(r: dict) -> None:
    print(f"Language: {r['lang']}  Words: {r['words']}  Sentences: {r['sentences']}")
    print(f"Sentence length: avg {r['avg_len']:.1f}, spread (sd) {r['sd_len']:.1f}"
          + ("  ! very uniform, mix short and long" if r["sentences"] > 5 and r["sd_len"] < 4 else ""))
    print(f"Em dashes per 150 words: {r['em_dash_per150']:.1f}" + ("  ! high" if r["em_dash_per150"] > 1 else ""))
    if r["word_hits"]:
        print("AI-typical words: " + ", ".join(f"{w} x{n}" for w, n in r["word_hits"].items()))
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
    args = ap.parse_args()

    def load(path):
        return sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()

    if args.compare:
        a, b = (load(p) for p in args.compare)
        lang = detect_lang(a) if args.lang == "auto" else args.lang
        ra, rb = scan(a, lang), scan(b, lang)
        rows = [
            ("Words", ra["words"], rb["words"]),
            ("Sentence-length spread (sd)", f"{ra['sd_len']:.1f}", f"{rb['sd_len']:.1f}"),
            ("AI-typical words", sum(ra["word_hits"].values()), sum(rb["word_hits"].values())),
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
        return 0

    if not args.file:
        ap.error("give a file, '-' for stdin, or --compare BEFORE AFTER")
    text = load(args.file)
    lang = detect_lang(text) if args.lang == "auto" else args.lang
    if args.per_sentence:
        per_sentence(text, lang)
        return 0
    report(scan(text, lang))
    return 0


if __name__ == "__main__":
    sys.exit(main())
