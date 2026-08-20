"""preview_cover.py - render a cover (or every motif) so you can look at it.

The cover is the whole point of this style, so never ship one you have not
seen. Render, open the PNG, and iterate on the motif and the three seed
colours until it looks deliberate.

    # one cover, from three seed colours and a named motif
    python scripts/preview_cover.py --title "Duskfade" \
        --kicker "Clockpunk platforming from Madrid" \
        --subtitle "A research dossier" \
        --deep 1B1A30 --accent 3B7EA1 --alt C98A2E \
        --motif stopwatch --out cover.pdf

    # a contact sheet of every bundled motif in your palette
    python scripts/preview_cover.py --deep 1B1A30 --accent 3B7EA1 \
        --alt C98A2E --all-motifs --out motifs.pdf

PNG rendering needs PyMuPDF (`pip install pymupdf`). Without it the script
still writes the PDF and says so.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reportlab.lib.pagesizes import A4          # noqa: E402
from reportlab.lib.units import mm              # noqa: E402
from reportlab.pdfgen import canvas as pdfcanvas  # noqa: E402

import motifs as motif_lib                      # noqa: E402
from dossier import Dossier, Theme              # noqa: E402


def _hex(v: str) -> str:
    return v if v.startswith("#") else "#" + v


def to_png(pdf_path: str, dpi: int = 110) -> str | None:
    """Render page 1 to PNG beside the PDF. Returns the path, or None."""
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("PyMuPDF not installed - PDF written, no PNG preview. "
              "Install with: pip install pymupdf")
        return None
    png = os.path.splitext(pdf_path)[0] + ".png"
    doc = fitz.open(pdf_path)
    doc[0].get_pixmap(dpi=dpi).save(png)
    print(f"wrote {png}")
    return png


def contact_sheet(theme: Theme, out: str) -> str:
    """One page, every motif, tiled - the fastest way to choose one."""
    c = pdfcanvas.Canvas(out, pagesize=A4)
    pw, ph = A4
    names = sorted(motif_lib.MOTIFS)
    cols, rows = 4, 6
    cw, ch = (pw - 24 * mm) / cols, (ph - 30 * mm) / rows
    c.setFillColor(theme.deep)
    c.rect(0, 0, pw, ph, stroke=0, fill=1)
    for i, name in enumerate(names):
        col, row = i % cols, i // cols
        if row >= rows:
            break
        bx = 12 * mm + col * cw
        by = ph - 18 * mm - (row + 1) * ch
        motif_lib.MOTIFS[name](c, bx + cw * 0.12, by + ch * 0.20,
                               cw * 0.76, ch * 0.68, theme)
        c.setFillColor(theme.cover_blurb)
        c.setFont("Helvetica", 7)
        c.drawCentredString(bx + cw / 2, by + ch * 0.06, name)
    c.setFillColor(theme.alt)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(12 * mm, ph - 14 * mm, "MOTIF CONTACT SHEET")
    c.save()
    print(f"wrote {out}")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--deep", default="1E1B2E", help="dark base colour")
    ap.add_argument("--accent", default="2E7DB8", help="cool accent")
    ap.add_argument("--alt", default="C4577F", help="warm accent")
    ap.add_argument("--preset", help="use a named preset instead of seed colours")
    ap.add_argument("--motif", default="stitched_mask")
    ap.add_argument("--title", default="Working Title")
    ap.add_argument("--kicker", default="One line of framing")
    ap.add_argument("--subtitle", default="A research dossier")
    ap.add_argument("--blurb", default="Two lines of blurb go here.|The second line lands the promise.",
                    help="lines separated by |")
    ap.add_argument("--meta", default="Author|Date|Scope", help="facts separated by |")
    ap.add_argument("--all-motifs", action="store_true",
                    help="render a contact sheet of every bundled motif")
    ap.add_argument("--out", default="cover_preview.pdf")
    ap.add_argument("--dpi", type=int, default=110)
    a = ap.parse_args(argv)

    theme = (Theme.preset(a.preset) if a.preset
             else Theme.from_seeds(_hex(a.deep), _hex(a.accent), _hex(a.alt)))

    if a.all_motifs:
        contact_sheet(theme, a.out)
        to_png(a.out, a.dpi)
        return 0

    doc = Dossier(
        a.out, theme=theme, motif=motif_lib.get(a.motif),
        cover=dict(kicker=a.kicker, title=a.title, subtitle=a.subtitle,
                   blurb=a.blurb.split("|"), meta=a.meta.split("|")),
        header_left=a.title,
    )
    doc.section("Preview", "Body page sample",
                lead="This page exists only so the preview has a body page to show.")
    doc.p("Body text at 9.6/13.6. Check that the accent colour reads clearly "
          "against white and that the dark heading is not muddy.")
    doc.build()
    to_png(a.out, a.dpi)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
