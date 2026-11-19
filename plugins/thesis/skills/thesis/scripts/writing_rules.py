"""Shared rules for the checker scripts in this collection.

Copied next to each checker by scripts/build.py; edit shared/scripts/writing_rules.py.
Every checker imports it from its own folder, so the rules cannot drift apart.
Standard library only; works on Python 3.9+.
"""

import re

# ---------------------------------------------------------------- input

def read_input(path: str) -> str:
    """Read a file (or '-' for stdin) as text: UTF-8, UTF-8 with BOM, or UTF-16 with BOM."""
    import sys
    if path == "-":
        return sys.stdin.read()
    with open(path, "rb") as f:
        raw = f.read()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return raw.decode("utf-8", errors="replace")


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
    r"|landscape (?:mode|orientation|survey|ecolog\w*|architect\w*)|(?:land|sea)scape"
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
FIRST_PERSON = re.compile(r"\b(?:i|me|my|mine|we|us|our|saya|aku|kami|kita)\b", re.I)
