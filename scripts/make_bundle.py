#!/usr/bin/env python3
"""Make one combined skill, "vetame-writing", for chat apps that take a single skill per upload
(the Gemini app, claude.ai). All files sit flat in one folder, because uploads may drop subfolders.

    python3 scripts/make_bundle.py              # writes dist/vetame-writing/ and dist/vetame-writing.zip

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

This one skill contains six. **First pick the guide that matches the task, read that file in full, and follow it.** Read the reference files a guide points to when the guide says so.

| The user wants... | Read first |
|---|---|
| A personal statement, statement of purpose, motivation letter, scholarship essay, short application answer, or interview prep from one | `ps-guide.md` |
| A CV or resume made, upgraded or tailored (Harvard style) | `cv-guide.md` |
| Text to sound natural or human, "kayak AI", "terlalu kaku", or an AI-detector report explained | `humanizer-guide.md` |
| A lab report, laporan praktikum, programming lab, makalah, KP / magang or progress report | `report-guide.md` |
| A skripsi, tugas akhir, undergraduate thesis, proposal, chapter (Bab I-V), or sidang prep | `thesis-guide.md` |
| A debate, push-back or fact-check ("debat pakai fakta", "jangan iya-iya aja", "prove it") | `debate-guide.md` |

If a task spans two (for example a statement, then humanize it), finish the first guide's workflow, then apply the second.

## Rules that always apply

- `shared-integrity.md`: never invent facts, numbers, experiences or sources. Mark anything unconfirmed `[VERIFY: ...]`. Follow the application's or course's AI-use rules.
- `shared-anti-ai-tone.md`: plain, specific wording; no padding phrases.
- Talk to the user in their language; write the document in the language the application or course needs.

## File names in this bundle

The guides were written as separate skills, so they mention paths such as `references/regional.md` or `references/shared/integrity.md`. In this bundle every file sits in one folder with a prefix: the guide's own references are `<prefix>-<name>.md` (ps-, cv-, humanizer-, report-, thesis-, debate-) and the shared ones are `shared-<name>.md`. The links have already been rewritten; if you meet an old path, use this rule.

## Checker scripts

The guides mention scripts such as `python scripts/ps_check.py`. Chat apps usually cannot run them, and this bundle does not include them. When a guide says to run one, do the same checks by reading instead (word count against the limit, placeholders like `[VERIFY]` or `[add ...]` left in, repeated sentence openers, padding phrases, citations that are missing from the reference list), and tell the user the script was not run. For the scripts, use the full repository: https://github.com/Vetame21/personal-statement-skill
"""


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
    text = re.sub(r"\]\(references/shared/\)", "](shared-integrity.md)", text)
    text = text.replace("references/shared/", "the shared-*.md files ")
    names = {n: prefix + "-" + n for n in own}
    names.update({n: "shared-" + n for n in SHARED if n not in names})
    for n, flat in names.items():                       # bare "debate-panel.md" -> "ps-debate-panel.md"
        text = re.sub(r"(?<![\w/-])" + re.escape(n) + r"\.md", flat + ".md", text)
    return text


def make(out_root: Path) -> Path:
    out = out_root / NAME
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    fm = "---\nname: " + NAME + "\ndescription: " + DESCRIPTION + "\n---\n\n"
    save(out / "SKILL.md", fm + ROUTER)
    for ref in sorted((ROOT / "shared" / "references").glob("*.md")):
        save(out / ("shared-" + ref.name), rewrite(ref.read_text(encoding="utf-8"), "shared", SHARED))
    for skill, prefix in PREFIX.items():
        src = ROOT / "skills" / skill
        own = sorted(p.stem for p in (src / "references").glob("*.md"))
        guide = rewrite(body((src / "SKILL.md").read_text(encoding="utf-8")), prefix, own)
        save(out / (prefix + "-guide.md"), guide)
        for ref in sorted((src / "references").glob("*.md")):
            save(out / (prefix + "-" + ref.name), rewrite(ref.read_text(encoding="utf-8"), prefix, own))
    with zipfile.ZipFile(out_root / (NAME + ".zip"), "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(out.iterdir()):
            z.write(f, NAME + "/" + f.name)
    return out


def main() -> int:
    out = make(ROOT / "dist")
    files = sorted(p.name for p in out.iterdir())
    print("Wrote " + str(out) + " (" + str(len(files)) + " files) and " + str(out.parent / (NAME + ".zip")))
    print("Upload the folder (not the zip) in the Gemini app: Settings > Skills > Upload skill > folder.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
