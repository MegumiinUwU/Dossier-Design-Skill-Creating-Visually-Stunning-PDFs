# Troubleshooting

Symptom first. Everything here has actually happened.

## Contents

- Black boxes in the text
- A table hangs past the right margin
- Table text runs out of its column
- `LayoutError: too large on page`
- The cover is blank or the motif is missing
- The motif looks wrong at the top of the page
- Page numbers are off by one
- Headers and footers appear on the cover
- Colours look muddy or the accent disappears
- A profile or box splits across a page
- Special characters vanish
- The PDF builds but is nearly empty
- Fonts fail to embed
- Nothing changed after an edit

## Black boxes in the text

A character the built-in Helvetica encoding cannot draw. Almost always a
Unicode superscript (`²`), subscript, an arrow, or a box-drawing character
pasted in from source material.

Use `<super>2</super>` and `<sub>2</sub>` tags, and HTML entities for
punctuation. `python scripts/check_pdf.py out.pdf` lists every offending
character by name.

## A table hangs past the right margin

Column widths do not sum to the frame width. `doc.table()` normalises relative
weights so this cannot happen; if you built a `Table` by hand, its `colWidths`
must sum to exactly `doc.frame_w`.

`check_pdf.py` reports the page and the offending text.

## Table text runs out of its column

A cell was passed as a bare string to a hand-built `Table`. ReportLab does not
wrap raw strings in table cells. Wrap every cell in a `Paragraph` -
`doc.table()` does this for you.

## `LayoutError: too large on page`

One flowable is taller than the frame. Usually a callout box containing many
paragraphs, or a `KeepTogether` block that grew.

Split the box into two, or drop the `KeepTogether`. A profile with ten bullets
is a section, not a profile.

## The cover is blank or the motif is missing

- `motif=` was left as `None`. Pass `motifs.get("name")` or your own callable.
- Your custom motif drew with the fill colour still set to `deep` - it is there,
  it is just invisible. Set `c.setFillColor(t.motif_fill)` before drawing.
- Your motif drew outside the box. Coordinates are absolute points with `(x, y)`
  at the **bottom-left** of the motif box, not the page.

## The motif looks wrong at the top of the page

The motif box is centred at `0.765H` and is 62 x 72mm. If a custom motif is
drawn assuming a square box, it stretches. Work in fractions of the `w` and `h`
you are handed, and pass `motif_box=(w, h)` if the shape needs different
proportions.

## Page numbers are off by one

The footer prints `doc.page - 1` so the cover is not page 1. If you added front
matter before the `NextPageTemplate` switch, or removed the cover, adjust the
offset in `Dossier._paint_body`.

## Headers and footers appear on the cover

The `NextPageTemplate("body")` switch must come *before* the `PageBreak()` that
ends the cover. The constructor handles this; if you rebuilt the story by hand,
check that order.

## Colours look muddy or the accent disappears

`accent` is used for 12.4pt bold text on white. If it is lighter than about
L 0.55 it greys out. Darken it - do not enlarge the type.

If the whole document looks washed, `deep` is probably not dark enough. It
wants L 0.12-0.16; every neutral is derived from it, so a weak `deep` weakens
everything.

## A profile or box splits across a page

Wrap it in `KeepTogether`. `doc.profile()` and titled `doc.box()` calls already
do. For your own blocks:

```python
from reportlab.platypus import KeepTogether
doc.add(KeepTogether([...]))
```

## Special characters vanish

Accented characters must be HTML entities inside `Paragraph` markup, or the
source file must genuinely be UTF-8 and the string a proper `str`. Writing the
build script with `encoding="utf-8"` and using entities for anything unusual is
the reliable path.

## The PDF builds but is nearly empty

Content was appended to a list that was never added to the story, or `build()`
was called before the content. `doc.build()` must be the last call.
`check_pdf.py` flags a suspiciously low character count.

## Fonts fail to embed

Only relevant with `use_font_family()`. The TTF path must be absolute or
relative to the working directory at run time, and the font must contain every
glyph used. If ReportLab raises on registration, fall back to Helvetica - the
style was tuned for it.

## Nothing changed after an edit

The PDF viewer is holding the old file open. Close it, or write to a new path.
On Windows an open viewer can also make the write itself fail with a permission
error.
