"""new_dossier.py - write a starter build script wired to this skill.

Saves you from hand-writing the imports, the sys.path line and the cover
block every time.

    python scripts/new_dossier.py --title "Scarlet Deer Inn" \
        --kicker "Embroidered folk horror from the Czech Republic" \
        --subtitle "A research dossier for an eight minute video review" \
        --preset folk-crimson --motif antlered_head --out build_scarlet.py

Then edit the generated file: it is an ordinary Python script, and every
section is a plain function call you can reorder, delete or repeat.
"""

from __future__ import annotations

import argparse
import os
import re

TEMPLATE = '''"""Build {title} as a dossier PDF. Run: python {script_name}"""

import sys
sys.path.insert(0, r"{scripts_dir}")

import motifs
from dossier import Dossier, Theme

theme = {theme_expr}

doc = Dossier(
    "{pdf_name}",
    theme=theme,
    motif=motifs.get("{motif}"),
    cover=dict(
        kicker="{kicker}",
        title="{title}",
        subtitle="{subtitle}",
        blurb=["First line of the promise.",
               "Second line, what the reader gets."],
        meta=["Author", "Scope", "Compiled <date>"],
    ),
    header_left="{title} / {doctype}",
    header_right="Secondary credit",
    footer_left="One line on what this document is for.",
)

# ---------------------------------------------------------------- front matter
doc.section("Front matter", "How to use this dossier",
            lead="One paragraph telling the reader what the sections are and "
                 "how to read them.")
doc.contents([
    ("01", "First section", "What it gives you."),
    ("02", "Second section", "What it gives you."),
])
doc.box(["Everything past this page assumes X.",
         "A second line if the caution needs one."],
        title="Scope and content note", kind="warn")
doc.page_break()

# ---------------------------------------------------------------- section 01
doc.section("Part 1", "First section",
            lead="The one paragraph that frames everything below it.")
doc.h2("A sub-heading")
doc.p("Body text. Keep it dense - the density is the look.")
doc.bullets([
    "A tight bullet.",
    "Another one.",
])
doc.say("A suggested line the reader can say out loud.")
doc.table([
    ("Field", "Value"),
    ("Released", "..."),
    ("Platforms", "..."),
], widths=[30, 70])
doc.box("A short takeaway worth boxing.", title="TL;DR")
doc.page_break()

# ---------------------------------------------------------------- closing
doc.section("Appendix", "Sources",
            lead="Where every claim came from.")
doc.sources([
    ("Source name", "example.com"),
])

doc.build()
'''


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_") or "dossier"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True)
    ap.add_argument("--kicker", default="One line of framing")
    ap.add_argument("--subtitle", default="A research dossier")
    ap.add_argument("--doctype", default="RESEARCH DOSSIER")
    ap.add_argument("--motif", default="stitched_mask")
    ap.add_argument("--preset", help="a name from PRESETS in dossier.py")
    ap.add_argument("--deep", default="1E1B2E")
    ap.add_argument("--accent", default="2E7DB8")
    ap.add_argument("--alt", default="C4577F")
    ap.add_argument("--out", help="path for the generated build script")
    a = ap.parse_args(argv)

    slug = slugify(a.title)
    out = a.out or f"build_{slug}.py"
    scripts_dir = os.path.dirname(os.path.abspath(__file__))

    def h(v):
        return v if v.startswith("#") else "#" + v

    theme_expr = (f'Theme.preset("{a.preset}")' if a.preset else
                  f'Theme.from_seeds("{h(a.deep)}", "{h(a.accent)}", "{h(a.alt)}")')

    src = TEMPLATE.format(
        title=a.title, kicker=a.kicker, subtitle=a.subtitle, doctype=a.doctype,
        motif=a.motif, theme_expr=theme_expr, scripts_dir=scripts_dir,
        script_name=os.path.basename(out), pdf_name=f"{slug}_dossier.pdf",
    )
    if os.path.exists(out):
        raise SystemExit(f"refusing to overwrite existing file: {out}")
    with open(out, "w", encoding="utf-8") as f:
        f.write(src)
    print(f"wrote {out}\nnext: python {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
