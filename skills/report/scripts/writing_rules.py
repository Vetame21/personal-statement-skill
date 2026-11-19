"""Shared rules for the checker scripts in this collection.

Copied next to each checker by scripts/build.py; edit shared/scripts/writing_rules.py.
Every checker imports it from its own folder, so the rules cannot drift apart.
Standard library only; works on Python 3.9+.
"""

import re
import sys

# Print UTF-8 whatever the console uses (Windows pipes default to cp1252, which
# cannot encode 参考文献, arrows or em dashes in the user's text).
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# ---------------------------------------------------------------- input


def decode_bytes(raw: bytes) -> str:
    """Decode UTF-8 (with or without BOM) or UTF-16 (with or without BOM); normalise line endings."""
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        text = raw.decode("utf-16")
    elif len(raw) >= 4 and raw.count(b"\x00") > len(raw) // 4:
        # UTF-16 without a byte-order mark: NULs sit in the odd (LE) or even (BE) positions
        text = raw.decode("utf-16-le" if raw[1:2] == b"\x00" else "utf-16-be", errors="replace")
    else:
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        text = raw.decode("utf-8", errors="replace")
    if text.count("\ufffd") > max(3, len(text) // 200):
        print("! Warning: parts of this input could not be decoded; save it as UTF-8 and re-run.", file=sys.stderr)
    return normalise_newlines(text)


def normalise_newlines(text: str) -> str:
    """CRLF, doubly converted CR CR LF and bare CR all become one LF."""
    return re.sub(r"\r+\n?", "\n", text)

def read_input(path: str) -> str:
    """Read a file, or '-' for stdin, through the same decoder (BOMs, UTF-16, CRLF)."""
    if path == "-":
        stream = getattr(sys.stdin, "buffer", None)
        return decode_bytes(stream.read()) if stream else normalise_newlines(sys.stdin.read())
    with open(path, "rb") as f:
        return decode_bytes(f.read())


def is_empty(text: str) -> bool:
    return not re.search(r"\w", text)


# ---------------------------------------------------------------- placeholders
# The markers these skills use, plus common draft leftovers. Uppercase or
# snake_case angle brackets only, so "x < 3 and y > 9", <div> and <https://...> pass.
PLACEHOLDER = re.compile(
    r"\[(?:ADD DETAIL|DATA NEEDED|VERIFY|TODO|CITATION NEEDED|REF\b|XX+|MS\d)[^\]]*\]"
    r"|\bTODO\b|\bXXX+\b|\bTBD\b"
    r"|<[a-z]+(?:_[a-z]+)+>"
    r"|<[A-Z][A-Z0-9 _\-]{2,40}>"
)

# ---------------------------------------------------------------- significance
SIGNIF = re.compile(r"\bsignifikan\w*|\bsignificant(?:ly)?\b", re.I)
TEST_RESULT = re.compile(
    r"p\s*[<=>≤]\s*0?[.,]\d|\bt\s*\(\d|\bF\s*\(\d|χ2|chi-?square|α\s*=|\bsig\.|\bp-value"
    r"|\buji\s+(?:t|f|chi|anova|mann|wilcoxon|regresi)\b",
    re.I,
)


def unsupported_significance(sentences):
    """Sentences using 'signifikan'/'significant' without a test result in the same sentence."""
    return [s for s in sentences if SIGNIF.search(s) and not TEST_RESULT.search(s)]


# ---------------------------------------------------------------- AI-typical words
# STRONG: almost always template phrasing in applications and essays.
# CONTEXT: fine in some contexts (technical, literal), so shown as "possible"
# and only counted towards severity when they pile up.
EN_STRONG = {
    "delve": r"delv(?:e|es|ed|ing)", "tapestry": r"tapestr(?:y|ies)", "testament": r"testaments?",
    "beacon": r"beacons?", "embark": r"embark(?:s|ed|ing)?", "cornerstone": r"cornerstones?",
    "linchpin": r"linchpins?", "multifaceted": r"multifaceted", "unwavering": r"unwavering",
    "poised": r"poised", "paramount": r"paramount",
}
EN_CONTEXT = {
    "pivotal": r"pivotal", "crucial": r"crucial", "vital": r"vital", "realm": r"realms?",
    "landscape": r"landscapes?", "foster": r"foster(?:s|ed|ing)?", "cultivate": r"cultivat(?:e|es|ed|ing)",
    "nurture": r"nurtur(?:e|es|ed|ing)", "leverage": r"leverag(?:e|es|ed|ing)", "harness": r"harness(?:es|ed|ing)?",
    "utilize": r"utili[sz](?:e|es|ed|ing|ation)", "navigate": r"navigat(?:e|es|ed|ing)",
    "seamless": r"seamless(?:ly)?", "robust": r"robust(?:ly)?", "cutting-edge": r"cutting-edge",
    "relentless": r"relentless(?:ly)?", "steadfast": r"steadfast", "intricate": r"intricate",
    "nuanced": r"nuanced", "profound": r"profound(?:ly)?", "underscore": r"underscor(?:e|es|ed|ing)",
    "resonate": r"resonat(?:e|es|ed|ing)", "journey": r"journeys?", "passion": r"passion(?:s|ate|ately)?",
    "ignite": r"ignit(?:e|es|ed|ing)", "furthermore": r"furthermore", "moreover": r"moreover", "additionally": r"additionally",
}
ID_STRONG = {}
ID_CONTEXT = {
    "krusial": r"krusial", "esensial": r"esensial", "fundamental": r"fundamental", "komprehensif": r"komprehensif",
    "holistik": r"holistik", "sinergi": r"sinergi\w*", "transformatif": r"transformatif",
}
# Technical or literal uses that are not template phrasing
TECH_ALLOWLIST = re.compile(
    r"robust (?:standard errors?|regression|estimat\w*|statistics?|to outliers)"
    r"|(?:wiring|test|safety) harness|harness(?:es|ed)? (?:the )?(?:power|energy|wind|solar)"
    r"|landscape (?:mode|orientation|survey|ecolog\w*|architect\w*|photograph\w*|painting)"
    r"|(?:cpu|gpu|memory|bandwidth|capacity|resource) utili[sz]ation|utili[sz]ation rates?"
    r"|navigat\w* (?:bar|stack|menu|drawer|controller|system|to the)|(?:page|screen|app) navigation"
    r"|vital signs?|crucial (?:point|temperature|exponent)"
    r"|foster (?:care|parents?|families|homes?|child\w*)",
    re.I,
)


def word_hits(text: str, lang: str):
    """Return (strong_hits, context_hits) as {word: count}, after removing allowlisted technical phrases."""
    low = TECH_ALLOWLIST.sub(" ", text.lower())
    strong_list, context_list = (ID_STRONG, ID_CONTEXT) if lang == "id" else (EN_STRONG, EN_CONTEXT)

    def count(table):
        out = {}
        for word, pattern in table.items():
            n = len(re.findall(rf"\b{pattern}\b", low))
            if n:
                out[word] = n
        return out

    return count(strong_list), count(context_list)


def word_severity(strong: dict, context: dict) -> int:
    """Strong words count fully; context words only beyond the first two."""
    return sum(strong.values()) + max(0, sum(context.values()) - 2)


# ---------------------------------------------------------------- first person
# "I" only as a pronoun (not "Bab I", "Part I", "World War I"); "us" lowercase only (not "US")
FIRST_PERSON = re.compile(
    r"(?<!Bab )(?<!Part )(?<!Chapter )(?<!Bagian )(?<!War )(?<!Tahap )\bI\b(?!\.)"
    r"|\b(?:[Mm]e|[Mm]y|[Mm]ine|[Ww]e|[Oo]urs?|us|Us|[Ss]aya|[Aa]ku|[Kk]ami|[Kk]ita)\b"
)
NUMBER_WORDS = re.compile(
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|hundred|thousand|million|"
    r"half|dozen|satu|dua|tiga|empat|lima|enam|tujuh|delapan|sembilan|sepuluh|puluh|ratus|ribu|juta)\b", re.I)
# Procedural passive ("was heated", "were weighed"): normal in Methods sections
PASSIVE = re.compile(r"\b(?:was|were|is|are|been|being|be)\s+(?:\w+ly\s+)?\w+(?:ed|en|wn|ung|ept|ade|ut|et)\b"
                     # Indonesian di- passives (dipanaskan, ditimbang), not digital, diri, dia, disini
                     r"|\bdi(?!gital|ri\b|rinya|a\b|ana|ni\b|sini|situ|mana|skusi|ploma|rektur|ksi|et)[a-z]{4,}\b", re.I)


# ---------------------------------------------------------------- sentences and language
ABBREVIATIONS = ["U.S.", "U.K.", "e.g.", "i.e.", "etc.", "et al.", "vs.", "Dr.", "Mr.", "Mrs.", "Ms.", "Prof.",
                 "No.", "Fig.", "Figs.", "Eq.", "Vol.", "pp.", "p.", "St.", "Jr.", "Sr.", "dkk.", "hlm.", "dll.",
                 "dsb.", "Jl.", "a.n.", "S.Kom.", "M.T.", "Ph.D."]
_PROTECT = {a: a.replace(".", "\u2024") for a in ABBREVIATIONS}


_SENTENCE_STARTERS = (r"The|A|An|This|That|These|Those|It|We|I|In|On|At|For|After|Before|When|Then|There|"
                      r"Ini|Itu|Kami|Saya|Pada|Dalam|Setelah|Hasil|Data")
# A single capital + "." is an initial ("J. Smith") unless it follows a digit or a unit
# ("1 L.", "80 °C.") or the next word starts a new sentence ("Appendix B. The ...").
_INITIAL = re.compile(r"(?<![\w°])(?<!\d )\b([A-Z])\.(?=\s(?!(?:" + _SENTENCE_STARTERS + r")\b)[A-Z])")


def split_sentences(text: str):
    """Split prose into sentences: headings and blank-line blocks stay separate, and common
    abbreviations (U.S., Dr., e.g., et al., dkk.) and initials do not end a sentence."""
    sentences = []
    for block in re.split(r"\n\s*\n|\n(?=\s*#)|(?<=\n)(?=\s*#)", text):
        lines = block.strip().splitlines()
        if lines and lines[0].lstrip().startswith("#"):
            heading = lines.pop(0).strip()
            if re.search(r"\w", heading):
                sentences.append(heading)
        s = re.sub(r"\s+", " ", " ".join(lines).strip())
        if not s:
            continue
        for a, b in _PROTECT.items():
            s = s.replace(a, b)
        s = _INITIAL.sub("\\1\u2024", s)
        parts = re.split(r"(?<=[.!?])\s+(?=[\"'“(\[]?[A-Z0-9])", s)
        sentences += [part.replace("\u2024", ".") for part in parts if re.search(r"\w", part)]
    return sentences


def detect_lang(text: str) -> str:
    low = f" {text.lower()} "
    id_hits = sum(low.count(w) for w in (" yang ", " dan ", " dengan ", " untuk ", " adalah ", " dalam ", " saya ", " ini "))
    en_hits = sum(low.count(w) for w in (" the ", " and ", " with ", " for ", " is ", " of ", " my ", " this "))
    return "id" if id_hits > en_hits else "en"


# ---------------------------------------------------------------- phrases and structures
EN_PHRASES = [
    r"in today'?s (?:rapidly |fast-paced |ever-)?(?:evolving|changing|digital|modern)(?: world| landscape| era)?",
    r"plays? an? (?:vital|crucial|key|pivotal|important|significant) role",
    r"it is (?:important|worth|crucial) (?:to note|noting) that",
    r"a unique blend of", r"\bin conclusion\b", r"\bultimately,", r"\ball in all\b",
    r"have you ever wondered", r"(?:this|it) (?:experience )?taught me the importance of",
    r"make the world a better place", r"knows no bounds", r"golden ticket",
]
ID_PHRASES = [
    r"di era (?:digital|globalisasi|modern|teknologi)",
    r"seiring (?:dengan )?(?:perkembangan|berkembangnya) (?:zaman|teknologi)",
    r"semakin (?:pesat|berkembang)nya (?:perkembangan )?",
    r"tidak dapat dipungkiri", r"tak dapat dipungkiri",
    r"memainkan peran (?:yang )?(?:sangat |amat )?(?:penting|krusial|vital|kunci|besar)",
    r"memegang peranan (?:yang )?(?:penting|krusial)",
    r"merupakan hal yang (?:sangat )?penting",
    r"hal ini menunjukkan bahwa", r"dapat disimpulkan bahwa", r"dalam rangka", r"oleh karena itu,? (?:dapat|perlu)",
    r"sangat(?:lah)? (?:penting|krusial)", r"berbagai macam", r"secara keseluruhan",
    r"pernahkah (?:anda|kamu) (?:bertanya|berpikir)",
]
NOT_JUST = {
    "en": r"\bnot (?:just|only|merely)\b[^.;!?]{1,80}?\bbut\b",
    "id": r"\b(?:bukan|tidak) (?:hanya|sekadar|cuma)\b[^.;!?]{1,80}?\b(?:tetapi|tapi|melainkan)\b",
}
OPENERS = {
    "en": ["furthermore", "moreover", "additionally", "in addition", "however", "therefore", "overall"],
    "id": ["selain itu", "lebih lanjut", "oleh karena itu", "dengan demikian", "di sisi lain", "hal ini", "secara keseluruhan"],
}
MORAL = {
    "en": r"(?:this|it|that) (?:taught|showed|reminded) me (?:that|the importance|how)",
    "id": r"(?:hal ini|pengalaman ini) (?:mengajarkan|menunjukkan|mengingatkan) (?:saya|kita)",
}
# Lists of three with two commas ("A, B, and C" / "A, B, C"); "Yesterday, I went and..." no longer counts
TRIPLET = re.compile(r"\b[\w-]+(?:\s[\w-]+)?,\s[\w-]+(?:\s[\w-]+)?,\s(?:(?:and|or|dan|atau|serta)\s)?[\w-]+")


def phrase_hits(text: str, lang: str):
    low = text.lower()
    return [m.group(0) for p in (ID_PHRASES if lang == "id" else EN_PHRASES) for m in re.finditer(p, low)]


def repeated_openers(paragraphs, lang: str):
    counts = {}
    for para in paragraphs:
        start = para.strip().lower()
        for o in OPENERS[lang]:
            if start.startswith(o):
                counts[o] = counts.get(o, 0) + 1
    return {o: n for o, n in counts.items() if n >= 2}
