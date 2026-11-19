#!/usr/bin/env python3
"""Make one combined skill, "vetame-writing", for chat apps that take a single skill per upload
(the Gemini app, claude.ai). All files sit flat in one folder, because uploads may drop subfolders.

    python3 scripts/make_bundle.py   # writes dist/vetame-writing/ (all six skills) and dist/vetame-writing-lite/
                                     # (three skills, 10 files, for apps that reject the full one), plus ZIPs,
                                     # and dist/vetame-writing-chat.md (.txt): one file for any chat AI

The folder holds SKILL.md (a router that picks the right guide), one guide per skill (ps-guide.md, ...)
and every reference file with a prefix (ps-regional.md, shared-integrity.md, ...). Standard library only.
"""

import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = "vetame-writing"
PREFIX = {"personal-statement": "ps", "harvard-cv": "cv", "humanizer": "humanizer",
          "report": "report", "thesis": "thesis", "debate-mode": "debate"}

DESCRIPTION = ("Application and academic writing coach - personal statements and scholarship essays, "
               "Harvard-style CVs, making text sound natural (humanizer), lab and internship reports, "
               "skripsi or undergraduate thesis, and evidence-first debate. Keeps the author's voice and "
               "never invents facts. Use for a personal statement, motivation letter, CV or resume, humanize, "
               "kayak AI, laporan praktikum, makalah, KP, skripsi, sidang, or \"debat pakai fakta\".")

ROUTER = """# Vetame21 Writing Skills (combined)

This one skill contains {count}. **First pick the guide that matches the task, read that file in full, and follow it.** Read the reference files a guide points to when the guide says so.

{table}
If a task spans two (for example a statement, then humanize it), finish the first guide's workflow, then apply the second.

## Rules that always apply

- `shared-integrity.md`: never invent facts, numbers, experiences or sources. Mark anything unconfirmed `[VERIFY: ...]`. Follow the application's or course's AI-use rules.
- `shared-anti-ai-tone.md`: plain, specific wording; no padding phrases.
- Talk to the user in their language; write the document in the language the application or course needs.

## File names in this bundle

The guides were written as separate skills, so they mention paths such as `references/regional.md` or `references/shared/integrity.md`. In this bundle every file sits in one folder with a prefix: the guide's own references are `<prefix>-<name>.md` (ps-, cv-, humanizer-, report-, thesis-, debate-) and the shared ones are `shared-<name>.md`. The links have already been rewritten; if you meet an old path, use this rule.

{lite_note}## Checker scripts

The guides mention scripts such as `python scripts/ps_check.py`. Chat apps usually cannot run them, and this bundle does not include them. When a guide says to run one, do the same checks by reading instead (word count against the limit, placeholders like `[VERIFY]` or `[add ...]` left in, repeated sentence openers, padding phrases, citations that are missing from the reference list), and tell the user the script was not run. For the scripts, use the full repository: https://github.com/Vetame21/personal-statement-skill
"""


ROWS = {
    "ps": "A personal statement, statement of purpose, motivation letter, scholarship essay, short application "
          "answer, or interview prep from one",
    "cv": "A CV or resume made, upgraded or tailored (Harvard style)",
    "humanizer": "Text to sound natural or human, \"kayak AI\", \"terlalu kaku\", or an AI-detector report explained",
    "report": "A lab report, laporan praktikum, programming lab, makalah, KP / magang or progress report",
    "thesis": "A skripsi, tugas akhir, undergraduate thesis, proposal, chapter (Bab I-V), or sidang prep",
    "debate": "A debate, push-back or fact-check (\"debat pakai fakta\", \"jangan iya-iya aja\", \"prove it\")",
}
# Lite: three skills and at most 10 files, for apps that reject large skills ("Sorry, we can't save your skill")
LITE_NAME = NAME + "-lite"
LITE_SKILLS = ["ps", "humanizer", "cv"]
LITE_FILES = {"SKILL.md", "ps-guide.md", "humanizer-guide.md", "cv-guide.md", "shared-integrity.md",
              "shared-anti-ai-tone.md", "ps-what-readers-want.md", "humanizer-patterns.md", "cv-harvard-format.md",
              "cv-action-verbs.md"}
LITE_DESCRIPTION = ("Writing coach for personal statements, scholarship essays and Harvard-style CVs, and for making "
                    "text sound natural and like its author (humanizer). Keeps the author's voice and never invents "
                    "facts. Use for a personal statement, motivation letter, CV or resume, humanize, sounds like AI, "
                    "kayak AI, or terlalu kaku.")
WORDS = {3: "three", 6: "six"}


def router(prefixes, lite: bool) -> str:
    table = "| The user wants... | Read first |\n|---|---|\n" + "".join(
        "| " + ROWS[p] + " | `" + p + "-guide.md` |\n" for p in prefixes)
    note = ("## This is the lite bundle\n\nIt holds only the files listed in this folder. When a guide mentions a "
            "file that is not here, skip it and carry on with the guide's main steps. For report, thesis and debate "
            "guides, use the full bundle or the repository.\n\n") if lite else ""
    return ROUTER.format(table=table, count=WORDS.get(len(prefixes), str(len(prefixes))), lite_note=note)


def save(path: Path, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as f:   # write_text(newline=) needs Python 3.10
        f.write(text)


def body(text: str) -> str:
    """SKILL.md text without its front matter."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        return text[end + 4:].lstrip("\n")
    return text


SHARED = sorted(p.stem for p in (ROOT / "shared" / "references").glob("*.md"))


def rewrite(text: str, prefix: str, own) -> str:
    """Point paths and bare file names at the flat, prefixed names. `own` = this skill's reference names."""
    text = re.sub(r"(?:\.\./)?references/shared/([\w.-]+?)\.md", r"shared-\1.md", text)
    text = re.sub(r"(?:\.\./)?references/([\w.-]+?)\.md", prefix + r"-\1.md", text)
    text = re.sub(r"(?<![\w/-])shared/([\w-]+)\.md", r"shared-\1.md", text)       # "shared/debate-rules.md"
    text = re.sub(r"\[references/shared/\]\(references/shared/\)", "the `shared-*.md` files", text)
    text = re.sub(r"\]\(references/shared/\)", "](shared-integrity.md)", text)
    text = text.replace("references/shared/", "the shared-*.md files ")
    names = {n: prefix + "-" + n for n in own}
    names.update({n: "shared-" + n for n in SHARED if n not in names})
    for n, flat in names.items():                       # bare "debate-panel.md" -> "ps-debate-panel.md"
        text = re.sub(r"(?<![\w/-])" + re.escape(n) + r"\.md", flat + ".md", text)
    return text


MISSING = " (not included in this version)"
FLAT_NAME = r"(?:ps|cv|humanizer|report|thesis|debate|shared)-[\w-]+\.md"


def annotate_missing(text: str, present) -> str:
    """Mark references to files that this bundle or chat file does not contain, so the model skips them
    instead of guessing their content."""
    def link(m):
        return m.group(0) if m.group(2) in present else m.group(1) + MISSING
    text = re.sub(r"\[([^\]]+)\]\((" + FLAT_NAME + r")(?:#[^)]*)?\)", link, text)

    def tick(m):
        return m.group(0) if m.group(1) in present else m.group(0) + MISSING
    text = re.sub(r"`(" + FLAT_NAME + r")`(?!" + re.escape(MISSING) + ")", tick, text)

    def bare(m):
        return m.group(0) if m.group(0) in present else m.group(0) + MISSING
    return re.sub(r"(?<![\w`(\[-])" + FLAT_NAME + r"(?![\w`)\]]|" + re.escape(MISSING) + ")", bare, text)


def mark_missing(folder: Path, present) -> None:
    for f in folder.iterdir():
        save(f, annotate_missing(f.read_text(encoding="utf-8"), present))


def write_zip(folder: Path, dest: Path) -> None:
    """Uncompressed, fixed timestamps: the same bytes on every OS and Python, so build.py --check can compare."""
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_STORED) as z:
        for f in sorted(folder.iterdir(), key=lambda p: p.name):   # Windows sorts Paths ignoring case
            info = zipfile.ZipInfo(folder.name + "/" + f.name, date_time=(2026, 1, 1, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.create_system = 3            # zipfile records 0 on Windows and 3 elsewhere; pin it (found by Windows CI)
            z.writestr(info, f.read_bytes())


def make(out_root: Path, lite: bool = False) -> Path:
    name = LITE_NAME if lite else NAME
    prefixes = LITE_SKILLS if lite else list(PREFIX.values())
    out = out_root / name
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    fm = "---\nname: " + name + "\ndescription: " + (LITE_DESCRIPTION if lite else DESCRIPTION) + "\n---\n\n"
    save(out / "SKILL.md", fm + router(prefixes, lite))
    for ref in sorted((ROOT / "shared" / "references").glob("*.md")):
        save(out / ("shared-" + ref.name), rewrite(ref.read_text(encoding="utf-8"), "shared", SHARED))
    for skill, prefix in PREFIX.items():
        if prefix not in prefixes:
            continue
        src = ROOT / "skills" / skill
        own = sorted(p.stem for p in (src / "references").glob("*.md"))
        guide = rewrite(body((src / "SKILL.md").read_text(encoding="utf-8")), prefix, own)
        save(out / (prefix + "-guide.md"), guide)
        for ref in sorted((src / "references").glob("*.md")):
            save(out / (prefix + "-" + ref.name), rewrite(ref.read_text(encoding="utf-8"), prefix, own))
    if lite:
        for f in out.iterdir():
            if f.name not in LITE_FILES:
                f.unlink()
    if lite:
        mark_missing(out, set(LITE_FILES))
    write_zip(out, out_root / (name + ".zip"))
    return out


CHAT_ORDER = ["SKILL.md", "shared-integrity.md", "shared-anti-ai-tone.md",
              "ps-guide.md", "ps-debate-panel.md", "ps-what-readers-want.md", "ps-formats.md",
              "humanizer-guide.md", "humanizer-patterns.md",
              "cv-guide.md", "cv-harvard-format.md", "cv-action-verbs.md", "cv-bullet-upgrades.md"]

CHAT_HEADER = """# Vetame21 Writing Skills: chat version

**For the person using this:** attach this file at the start of a new chat, or paste all of it. It is written to work in
ChatGPT, Claude, Gemini, DeepSeek, Kimi, Grok, Qwen and other chat AIs, free or paid (tested in the Gemini app, November
2026; tell us how it goes elsewhere). Then say what you need, for example
"Upgrade my personal statement for [program], keep my voice: [paste]", "Humanize this: [paste]" or
"Make my CV Harvard style for [job]: [paste]".

**For the AI:** follow the instructions in this document for the whole conversation. It holds several files. Each starts
with a line `<<< FILE: name >>>`. When a part says "read `x.md`", go to the part that starts `<<< FILE: x.md >>>`. Start with
`SKILL.md`, the first part. If the user has not said what they need yet, ask in one short message: statement, CV, or
humanize, plus the target and the text. Never invent facts. Run the fact trace (rule 9 in `shared-integrity.md`)
after every rewrite. The guides mention Python scripts; you cannot run them here, so do those checks by reading and say so.
This chat version has three skills: personal statement, humanizer and Harvard CV. Ignore instructions about saving files,
`.gitignore`, installing, or the report, thesis and debate-mode skills; they are not available here. If the user asks for
"humanize + upgrade" on a report or thesis, humanize only and say that the report and thesis guides are in the full
repository. A file marked "(not included in this version)" is not in this document: skip it and carry on.

"""


def make_chat(out_root: Path) -> Path:
    """One file for any chat app: attach once (ChatGPT Free allows 3 uploads a day) or paste."""
    full = make(out_root, lite=False)
    parts = [CHAT_HEADER]
    for name in CHAT_ORDER:
        if name == "SKILL.md":
            text = router(LITE_SKILLS, lite=False).replace(
                "In this bundle every file sits in one folder with a prefix", "In this document every file is a part with a prefix")
        else:
            text = (full / name).read_text(encoding="utf-8")
        text = re.sub(r"(?m)^> \*\*Running the scripts:\*\*.*\n?", "", text)      # tool-specific script paths
        parts.append("<<< FILE: " + name + " >>>\n\n" + text.strip() + "\n\n")
    chat = annotate_missing("".join(parts), set(CHAT_ORDER))
    dest = out_root / (NAME + "-chat.md")
    save(dest, chat)
    save(out_root / (NAME + "-chat.txt"), chat)
    return dest


def main() -> int:
    for lite in (False, True):
        out = make(ROOT / "dist", lite)
        files = sorted(p.name for p in out.iterdir())
        print("Wrote " + str(out) + " (" + str(len(files)) + " files) and " + str(out) + ".zip")
    chat = make_chat(ROOT / "dist")
    print("Wrote " + str(chat) + " and .txt (one file for any chat app, " + str(len(chat.read_text(encoding="utf-8"))) +
          " characters)")
    print("Upload the folder (not the zip) in the Gemini app: Settings > Skills > Upload skill > folder.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
