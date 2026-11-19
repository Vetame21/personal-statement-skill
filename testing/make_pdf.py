#!/usr/bin/env python3
"""Turn a simple Markdown report into a PDF. Standard library only, Python 3.9+.

    python3 testing/make_pdf.py testing/out/report.md testing/out/report.pdf

Handles headings, paragraphs, bullets, numbered lists, code blocks and tables (as monospace text).
Bold/italic markers and links are simplified to plain text. Characters outside Windows-1252 become '?'.
"""

import re
import sys
import textwrap
from pathlib import Path

PAGE_W, PAGE_H, MARGIN = 595, 842, 50          # A4 in points
BODY, MONO = 10, 8.5
STYLES = {  # kind: (font, size, line height, space before)
    "h1": ("F2", 16, 22, 10), "h2": ("F2", 13, 18, 10), "h3": ("F2", 11, 15, 6),
    "p": ("F1", BODY, 13, 4), "li": ("F1", BODY, 13, 1), "code": ("F3", MONO, 10.5, 0),
}
# Adobe Helvetica / Helvetica-Bold advance widths (1/1000 em) for ASCII 32-126; other characters use AVG_WIDTH.
HELV = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556, 556,
        556, 556, 556, 556, 278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667,
        556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556,
        556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722,
        500, 500, 500, 334, 260, 334, 584]
HELV_BOLD = [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556,
             556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278,
             556, 722, 611, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584,
             556, 333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611, 611, 389, 556,
             333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584]
AVG_WIDTH = 667          # accented capitals are as wide as their base letters; err on the wide side
LIST_MARK = r"^(\s*)([-*+]|\d{1,2}[.)])\s+"   # "2025. That year..." is a sentence, not item 2025


def text_width(text: str, font: str, size: float) -> float:
    if font == "F3":
        return len(text) * 0.6 * size
    table = HELV_BOLD if font == "F2" else HELV
    return sum(table[ord(c) - 32] if 32 <= ord(c) < 127 else AVG_WIDTH for c in text) * size / 1000


def wrap(text: str, font: str, size: float, max_w: float):
    """Greedy word wrap by real glyph widths; words longer than a line are split."""
    lines, cur = [], ""
    for word in text.split():
        while text_width(word, font, size) > max_w:              # split an over-long word (URLs, paths)
            cut = len(word)
            while cut > 1 and text_width(word[:cut], font, size) > max_w:
                cut -= 1
            if cur:
                lines.append(cur)
                cur = ""
            lines.append(word[:cut])
            word = word[cut:]
        trial = (cur + " " + word) if cur else word
        if text_width(trial, font, size) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur or not lines:
        lines.append(cur)
    return lines


def table_lines(rows, max_chars: int):
    """Lay out a table in monospace: wrap each cell inside its column. Too many columns -> one line per cell."""
    cols = max(len(r) for r in rows)
    rows = [r + [""] * (cols - len(r)) for r in rows]
    gap = 2
    widths = [max(len(r[c]) for r in rows) for c in range(cols)]
    avail = max_chars - gap * (cols - 1)
    while sum(widths) > avail and max(widths) > 8:
        widths[widths.index(max(widths))] -= 1
    if sum(widths) > avail:                                      # cannot fit even at 8 chars a column
        out = []
        for n, r in enumerate(rows[1:], 1):
            out.append("Row " + str(n) + ":")
            out += ["  " + rows[0][c] + ": " + r[c] for c in range(cols)]
        return out
    out = []
    for n, r in enumerate(rows):
        cells = [textwrap.wrap(r[c], widths[c]) or [""] for c in range(cols)]
        for i in range(max(len(x) for x in cells)):
            out.append((" " * gap).join((cells[c][i] if i < len(cells[c]) else "").ljust(widths[c])
                                        for c in range(cols)).rstrip())
        if n == 0 and len(rows) > 1:
            out.append((" " * gap).join("-" * w for w in widths))
    return out


REPLACE = {"→": "->", "←": "<-", "✓": "[ok]", "✗": "[x]", "✔": "[ok]", "✖": "[x]",
           "≥": ">=", "≤": "<=", " ": " ", "−": "-"}


def plain(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)      # [label](url) -> label (url)
    text = re.sub(r"(\*\*|__)(.+?)\1", r"\2", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"\1", text)
    text = text.replace("`", "")
    for a, b in REPLACE.items():
        text = text.replace(a, b)
    return text


def blocks(md: str):
    """Yield (kind, text) pairs."""
    lines = md.replace("\r\n", "\n").split("\n")
    i, para = 0, []

    def flush():
        if para:
            yield "p", " ".join(s.strip() for s in para)
            para.clear()

    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            yield from flush()
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                yield "code", lines[i]
                i += 1
            yield "gap", ""
        elif re.match(r"^\s*\|", line):
            yield from flush()
            rows = []
            while i < len(lines) and re.match(r"^\s*\|", lines[i]):
                if not re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i]):           # skip |---|---| rows
                    rows.append([plain(c.strip()) for c in lines[i].strip().strip("|").split("|")])
                i += 1
            for line in table_lines(rows, int((PAGE_W - 2 * MARGIN) / (MONO * 0.6))):
                yield "code", line
            yield "gap", ""
            continue
        elif re.match(r"^#{1,6}\s", line):
            yield from flush()
            level = len(line) - len(line.lstrip("#"))
            yield "h" + str(min(level, 3)), plain(line.lstrip("#").strip())
        elif re.match(LIST_MARK, line):
            yield from flush()
            m = re.match(LIST_MARK + r"(.*)", line)
            indent, mark, text = len(m.group(1)) // 2, m.group(2), m.group(3)
            while i + 1 < len(lines) and lines[i + 1].startswith("  ") and lines[i + 1].strip() \
                    and not re.match(LIST_MARK, lines[i + 1]):
                i += 1
                text += " " + lines[i].strip()
            bullet = "-" if mark in "-*+" else mark
            yield "li", (indent, bullet, plain(text))
        elif not line.strip() or re.match(r"^\s*(-{3,}|\*{3,})\s*$", line):
            yield from flush()
        else:
            para.append(plain(line))
        i += 1
    yield from flush()


def layout(md: str):
    """Return pages, each a list of (font, size, x, y, text)."""
    pages, page, y = [], [], PAGE_H - MARGIN

    def put(font, size, lh, x, text):
        nonlocal page, y
        if y - lh < MARGIN:
            pages.append(page)
            page, y = [], PAGE_H - MARGIN
        y -= lh
        page.append((font, size, x, y, text))

    for kind, content in blocks(md):
        if kind == "gap":
            y -= 4
            continue
        font, size, lh, before = STYLES[kind]
        y -= before
        if kind == "li":
            indent, bullet, text = content
            x = MARGIN + 12 + indent * 14
            wrapped = wrap(bullet + " " + text, font, size, PAGE_W - MARGIN - x - 10)
            put(font, size, lh, x, wrapped[0])
            for rest in wrapped[1:]:
                put(font, size, lh, x + 10, rest)
        elif kind == "code":
            per_line = int((PAGE_W - 2 * MARGIN) / (size * 0.6))
            for part in [content[i:i + per_line] for i in range(0, len(content), per_line)] or [""]:
                put(font, size, lh, MARGIN, part)
        else:
            for part in wrap(content, font, size, PAGE_W - 2 * MARGIN):
                put(font, size, lh, MARGIN, part)
    if page:
        pages.append(page)
    return pages or [[]]


def pdf_string(text: str) -> bytes:
    raw = text.encode("cp1252", errors="replace")
    return b"(" + raw.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)") + b")"


def build_pdf(pages) -> bytes:
    objs = []                                       # object bodies; object n is objs[n-1]
    fonts = {"F1": "Helvetica", "F2": "Helvetica-Bold", "F3": "Courier"}
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(b"")                                # pages tree, filled in below
    font_ids = {}
    for key, name in fonts.items():
        objs.append(("<< /Type /Font /Subtype /Type1 /BaseFont /" + name + " /Encoding /WinAnsiEncoding >>").encode())
        font_ids[key] = len(objs)
    res = " ".join("/" + k + " " + str(v) + " 0 R" for k, v in font_ids.items())
    kids = []
    for n, page in enumerate(pages, 1):
        ops = []
        for font, size, x, y, text in page:
            ops.append(b"BT /" + font.encode() + b" " + str(size).encode() + b" Tf " +
                       ("%.1f %.1f" % (x, y)).encode() + b" Td " + pdf_string(text) + b" Tj ET")
        footer = "Page " + str(n) + " of " + str(len(pages))
        ops.append(b"BT /F1 8 Tf " + ("%.1f 30 Td " % (PAGE_W - MARGIN - 45)).encode() + pdf_string(footer) + b" Tj ET")
        stream = b"\n".join(ops)
        objs.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
        content_id = len(objs)
        objs.append(("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %d %d] /Resources << /Font << %s >> >> "
                     "/Contents %d 0 R >>" % (PAGE_W, PAGE_H, res, content_id)).encode())
        kids.append(len(objs))
    objs[1] = ("<< /Type /Pages /Kids [" + " ".join(str(k) + " 0 R" for k in kids) + "] /Count " +
               str(len(kids)) + " >>").encode()
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += str(i).encode() + b" 0 obj\n" + body + b"\nendobj\n"
    xref = len(out)
    out += ("xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)).encode()
    for off in offsets:
        out += ("%010d 00000 n \n" % off).encode()
    out += ("trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)).encode()
    return bytes(out)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python3 testing/make_pdf.py REPORT.md REPORT.pdf", file=sys.stderr)
        return 2
    src, dest = Path(sys.argv[1]), Path(sys.argv[2])
    if not src.is_file():
        print("File not found: " + str(src), file=sys.stderr)
        return 2
    md = src.read_text(encoding="utf-8-sig", errors="replace")
    pages = layout(md)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(build_pdf(pages))
    print("Wrote " + str(dest) + " (" + str(len(pages)) + " page(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
