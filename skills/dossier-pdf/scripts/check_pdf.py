"""check_pdf.py - verify a built dossier before you hand it over.

Catches the four failures this style actually produces: text that overhangs
the margin (a table column sum that was wrong), characters the built-in
Helvetica encoding cannot draw (they render as black boxes), pages that came
out blank, and content that silently went missing.

    python scripts/check_pdf.py out.pdf
    python scripts/check_pdf.py out.pdf --expect "Quick Fire" --expect "Sources"

Exits 1 if any check fails, so it can gate a build loop. Margin and blank-page
checks need PyMuPDF (`pip install pymupdf`); without it the script still runs
the text checks and reports what it skipped.
"""

from __future__ import annotations

import argparse
import sys
import unicodedata

# Anything outside this set is not drawable by the built-in Helvetica
# encoding (WinAnsi) and will come out as a black box.
_SAFE_EXTRA = set("\n\r\t ‘’“”–—•·…")

MARGIN_TOLERANCE_PT = 2.0   # printers and rounding both wobble by about a point


def _load(path):
    try:
        import fitz
        return "fitz", fitz.open(path)
    except ImportError:
        from pypdf import PdfReader
        return "pypdf", PdfReader(path)


def _undrawable(text: str):
    """Characters the standard 14 fonts cannot render, with their names."""
    bad = {}
    for ch in text:
        if ch in _SAFE_EXTRA or ord(ch) < 0x80:
            continue
        try:
            ch.encode("cp1252")
        except UnicodeEncodeError:
            bad[ch] = unicodedata.name(ch, "U+%04X" % ord(ch))
    return bad


def check(path: str, expect=(), margin_mm=20.0, min_chars=400, quiet=False):
    kind, doc = _load(path)
    fails, notes = [], []

    if kind == "fitz":
        pages = [p.get_text() for p in doc]
    else:
        pages = [p.extract_text() or "" for p in doc.pages]
    text = "\n".join(pages)

    notes.append(f"pages: {len(pages)}")
    notes.append(f"characters: {len(text)}")

    if len(text) < min_chars:
        fails.append(f"only {len(text)} characters extracted - content may not "
                     f"have made it into the PDF")

    bad = _undrawable(text)
    if bad:
        sample = ", ".join(f"{c!r} ({n})" for c, n in list(bad.items())[:8])
        fails.append(f"{len(bad)} character(s) the built-in fonts cannot draw "
                     f"(these become black boxes): {sample}. Replace with HTML "
                     f"entities, or use <sub>/<super> tags instead of Unicode "
                     f"sub/superscripts.")

    for s in expect:
        if s not in text:
            fails.append(f"expected string not found in the PDF: {s!r}")

    if kind == "fitz":
        pt = margin_mm * 72.0 / 25.4
        for i, page in enumerate(doc):
            if i == 0:
                continue  # the cover paints to the edge on purpose
            r = page.rect
            for block in page.get_text("blocks"):
                x0, y0, x1, y1 = block[:4]
                if x0 < pt - MARGIN_TOLERANCE_PT or x1 > r.width - pt + MARGIN_TOLERANCE_PT:
                    snippet = " ".join(str(block[4]).split())[:60]
                    fails.append(f"page {i + 1}: text crosses the side margin "
                                 f"({x0:.0f}pt to {x1:.0f}pt): {snippet!r}. A "
                                 f"table's column widths probably do not sum to "
                                 f"the frame width.")
                    break
        blank = [i + 1 for i, p in enumerate(pages) if i and len(p.strip()) < 40]
        if blank:
            notes.append(f"near-empty pages: {blank} (fine after a section, "
                         f"suspicious in the middle of one)")
    else:
        notes.append("margin and blank-page checks skipped (PyMuPDF not installed)")

    if not quiet:
        for n in notes:
            print(f"  {n}")
        for f in fails:
            print(f"  FAIL  {f}")
        print("OK" if not fails else f"{len(fails)} problem(s) found")
    return fails


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--expect", action="append", default=[],
                    help="a string that must appear in the PDF; repeatable")
    ap.add_argument("--margin-mm", type=float, default=20.0)
    ap.add_argument("--min-chars", type=int, default=400)
    a = ap.parse_args(argv)
    return 1 if check(a.pdf, a.expect, a.margin_mm, a.min_chars) else 0


if __name__ == "__main__":
    sys.exit(main())
