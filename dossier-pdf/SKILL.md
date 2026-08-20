---
name: dossier-pdf
description: Builds research dossiers and briefing documents as designed PDFs - a dark cover whose palette and geometric motif are derived from the subject, then dense editorial body pages with themed tables, callout boxes and running furniture. Use when the user asks for a dossier, research brief, deep dive, briefing pack, field guide or report as a PDF, when they want collected research or web findings turned into a polished document, or when they mention a themed PDF cover, dossier styling, or making a PDF look designed rather than default.
license: MIT
---

# Dossier PDF

Turns researched material into a document that looks commissioned. One dark
cover carrying a single geometric motif, then body pages that are deliberately
plain and text-dense. All the personality lives in three places: the cover, the
two accent colours, and the kicker labels. Nothing else is decorated.

The style's one real idea: **the palette and the motif come from the subject**,
not from a fixed brand. A folk-horror dossier is plum and crimson with a deer's
head. A clockpunk one is indigo and amber with a stopwatch. Same document, same
type scale, different soul.

## Setup

```bash
pip install reportlab        # required
pip install pymupdf          # optional, enables PNG previews and margin checks
```

The default typography uses the built-in Helvetica family, so no font files are
needed and text always embeds correctly.

## Workflow

Copy this checklist and work through it:

```
- [ ] 1. Pick three seed colours from the subject
- [ ] 2. Pick or draw the cover motif
- [ ] 3. Preview the cover and look at it
- [ ] 4. Write the build script and fill it with content
- [ ] 5. Run check_pdf.py, fix, repeat until clean
```

### 1. Pick three seed colours

Every colour in the document derives from three:

| Seed | Role | How to choose it |
|---|---|---|
| `deep` | cover background, H1s, table headers | the subject's "night" colour, very dark, L around 0.14 |
| `accent` | H2s, rules, page numbers | mid-tone, cooler, structural |
| `alt` | kickers, box left-bars, the one warm spot | the subject's signature warm or bright colour |

```python
theme = Theme.from_seeds(deep="#2A1B28", accent="#3E6B52", alt="#B0304A")
```

Everything else - body ink, hairlines, callout fills, the cover's subtitle and
blurb greys, the motif's cream - is derived and **tinted toward `deep`'s hue**.
That is why a plum dossier reads plum all the way down to its table borders.

Seven ready palettes live in `PRESETS` (`Theme.preset("folk-crimson")`). Read
[references/theming.md](references/theming.md) for how to pull colours off a
subject, the exact derivation maths, and three worked examples.

### 2. Pick or draw the motif

One recognisable silhouette, 8-14 canvas primitives, in the subject's most
iconic object. A mask, a stopwatch, a deer's head, a flask, a key.

```bash
python scripts/preview_cover.py --deep 2A1B28 --accent 3E6B52 --alt B0304A \
    --all-motifs --out motifs.pdf
```

That renders every bundled motif in your palette on one page. Twenty-one ship
with the skill. If none fits the subject, write one - the recipe and the colour
discipline are in [references/cover-motifs.md](references/cover-motifs.md). A
custom motif that matches the subject beats a generic one that does not.

### 3. Preview the cover and look at it

```bash
python scripts/preview_cover.py --title "Scarlet Deer Inn" \
    --kicker "Embroidered folk horror from the Czech Republic" \
    --subtitle "A research dossier for an eight minute video review" \
    --preset folk-crimson --motif antlered_head --out cover.pdf
```

Read the PNG it writes. The cover is the whole point of this style - never ship
one you have not actually seen.

### 4. Write the build script

Scaffold it, then fill it in:

```bash
python scripts/new_dossier.py --title "Scarlet Deer Inn" \
    --preset folk-crimson --motif antlered_head --out build_scarlet.py
```

The generated script is ordinary Python. Every component is one call:

```python
import sys; sys.path.insert(0, "<skill>/scripts")
import motifs
from dossier import Dossier, Theme

doc = Dossier("out.pdf",
              theme=Theme.preset("folk-crimson"),
              motif=motifs.get("antlered_head"),
              cover=dict(kicker="...", title="...", subtitle="...",
                         blurb=["line one", "line two"],
                         meta=["studio", "released", "compiled"]),
              header_left="Scarlet Deer Inn / research dossier",
              header_right="Attu Games / released 21 July 2026",
              footer_left="Prepared as source material for a video review.")

doc.section("Part 1", "The Studio", lead="One framing paragraph.")
doc.h2("Sub-heading"); doc.p("Body text."); doc.bullets(["a", "b"])
doc.table([("Field", "Value"), ("Released", "2026")], widths=[30, 70])
doc.box("A TL;DR worth boxing.", title="In short")
doc.say("A line the reader can say out loud.")
doc.profile("Name", "role", points=["fact"], takeaway="what it means")
doc.page_break()
doc.build()
```

Full API in [references/api.md](references/api.md). A complete runnable
document is in [assets/example_dossier.py](assets/example_dossier.py) - read it
if you want to see the shape of a real one before writing your own.

To hand-roll the layout in raw ReportLab instead, every number in the style is
specified in [references/style-spec.md](references/style-spec.md).

### 5. Verify

```bash
python scripts/check_pdf.py out.pdf --expect "Sources" --expect "Quick Fire"
```

It catches the four failures this style actually produces: text overhanging a
margin, characters the built-in fonts cannot draw (they become black boxes),
blank pages, and content that silently went missing. Fix and re-run until it
prints OK. Then render a couple of body pages to PNG and look at them.

## Content shape

A dossier is not a report. It is written so the reader always knows the next
true thing they could say. The conventions that make it one - the contents
table of *purposes*, confidence flags, the profile block, the quick-fire fact
bank, the sources table - are in
[references/content-structure.md](references/content-structure.md). Follow them
when the user asks for a dossier or a research brief; relax them when they ask
for something else in this look.

## Non-negotiables

These are the rules that break the document when ignored:

- **Small type is the point.** Body is 9.6/13.6. Do not scale it up because a
  page looks dense - the density is the look.
- **One motif, one warm spot.** The motif is `motif_fill` outlined in
  `motif_stroke` with exactly one `alt`-coloured element. Never a third colour,
  never an illustration.
- **Every table cell is a Paragraph and column widths must sum to the frame
  width.** `doc.table()` enforces both; if you build tables by hand, ReportLab
  will silently overhang the margin when you get it wrong.
- **No Unicode sub/superscripts or exotic glyphs** with the built-in fonts -
  they render as black boxes. Use `<sub>`/`<super>` tags and HTML entities
  (`&#183;` for the middle dot, `&#8212;` for the em dash).
- **Sections open the same way every time**: kicker, H1, accent rule, one lead
  paragraph. Then `doc.page_break()` at the end of each.
- **Look at the output.** Render pages to PNG and inspect them before handing
  the PDF over.

## Reference files

| File | Read it when |
|---|---|
| [references/theming.md](references/theming.md) | choosing colours for a subject, or overriding a derived colour |
| [references/cover-motifs.md](references/cover-motifs.md) | choosing a motif, or drawing a custom one |
| [references/api.md](references/api.md) | writing the build script; every method and argument |
| [references/style-spec.md](references/style-spec.md) | hand-rolling the layout, or extending it with a new component |
| [references/content-structure.md](references/content-structure.md) | deciding what sections a dossier contains and how to write them |
| [references/troubleshooting.md](references/troubleshooting.md) | ReportLab misbehaves, or the output looks wrong |

## Adapting it

The look survives well outside research dossiers: field guides, technical
briefs, pitch documents, post-mortems, onboarding packs. Keep the cover, the
type scale and the section opener; swap the content conventions for whatever
the document actually needs. What does not survive is diluting it - two motifs,
a third accent, or bigger body text and it stops looking commissioned.
