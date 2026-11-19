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
            cols = max(len(r) for r in rows)
            widths = [max(len(r[c]) if c < len(r) else 0 for r in rows) for c in range(cols)]
            for n, r in enumerate(rows):
                yield "code", "  ".join((r[c] if c < len(r) else "").ljust(widths[c]) for c in range(cols)).rstrip()
                if n == 0 and len(rows) > 1:
                    yield "code", "  ".join("-" * w for w in widths)
            yield "gap", ""
            continue
        elif re.match(r"^#{1,6}\s", line):
            yield from flush()
            level = len(line) - len(line.lstrip("#"))
            yield "h" + str(min(level, 3)), plain(line.lstrip("#").strip())
        elif re.match(r"^\s*([-*+]|\d+[.)])\s+", line):
            yield from flush()
            m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)", line)
            indent, mark, text = len(m.group(1)) // 2, m.group(2), m.group(3)
            while i + 1 < len(lines) and lines[i + 1].startswith("  ") and lines[i + 1].strip() \
                    and not re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i + 1]):
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


def width_chars(size: float, mono: bool, indent: float = 0) -> int:
    avg = 0.6 if mono else 0.53                     # Courier is exactly 0.6 em; Helvetica averages ~0.5
    return max(20, int((PAGE_W - 2 * MARGIN - indent) / (size * avg)))


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
            wrapped = textwrap.wrap(text, width_chars(size, False, x - MARGIN + 14)) or [""]
            put(font, size, lh, x, bullet + " " + wrapped[0])
            for rest in wrapped[1:]:
                put(font, size, lh, x + 10, rest)
        elif kind == "code":
            for part in textwrap.wrap(content, width_chars(size, True), drop_whitespace=False) or [""]:
                put(font, size, lh, MARGIN, part)
        else:
            for part in textwrap.wrap(content, width_chars(size, False)) or [""]:
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
