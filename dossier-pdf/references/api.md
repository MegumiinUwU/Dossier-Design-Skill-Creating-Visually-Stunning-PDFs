# API reference

Everything in `scripts/dossier.py` and `scripts/motifs.py`.

## Contents

- Importing
- `Theme`
- `Dossier` constructor
- Content methods
- Colour helpers
- Custom fonts
- Scripts
- Paragraph markup that is safe

## Importing

```python
import sys
sys.path.insert(0, "/path/to/dossier-pdf/scripts")

import motifs
from dossier import Dossier, Theme, PRESETS, tint, scale, mix
```

`scripts/new_dossier.py` writes that path line for you.

## `Theme`

```python
Theme.from_seeds(deep, accent, alt, **overrides) -> Theme
Theme.preset(name, **overrides) -> Theme
```

Seventeen fields, three of which you supply. See
[theming.md](theming.md) for the derivation rules.

| Field | Used for |
|---|---|
| `deep` | cover background, H1 text, table header fill |
| `accent` | H2 text, section rules, page numbers |
| `alt` | kickers, callout left bar, box titles, the motif's warm element |
| `band` | cover's lighter top 40% |
| `say` | italic pull lines |
| `ink` | lead paragraphs |
| `body` | body text, bullets, table cells |
| `grey` | running header and footer, captions, profile roles |
| `rule` | hairlines, table borders |
| `boxbg` `quotebg` `warnbg` | the three callout fills; `boxbg` also stripes tables |
| `cover_title` `cover_sub` `cover_blurb` | cover text colours |
| `motif_fill` `motif_stroke` | motif silhouette and outline |

Themes are frozen-ish dataclasses; build a variant with
`dataclasses.replace(theme, accent="#123456")`.

## `Dossier` constructor

```python
Dossier(path, theme, cover, motif=None, pagesize=A4,
        header_left="", header_right="", footer_left="",
        margins=(20*mm, 20*mm, 22*mm, 20*mm),
        fonts=("Helvetica", "Helvetica-Bold", "Helvetica-Oblique"),
        motif_box=None, cover_text_top=118*mm, title="", author="")
```

| Argument | Notes |
|---|---|
| `path` | output PDF path |
| `theme` | a `Theme` |
| `cover` | dict: `kicker`, `title`, `subtitle`, `blurb`, `meta`. `blurb` and `meta` accept a list (joined with `<br/>` and ` &#183; ` respectively) or a string |
| `motif` | a callable `(c, x, y, w, h, theme)`, usually `motifs.get("name")` |
| `pagesize` | `A4` (default) or `LETTER`, both re-exported from `dossier` |
| `header_left` | top-left running header, upper-cased. Defaults to the cover title |
| `header_right` | top-right running header, upper-cased. A secondary credit |
| `footer_left` | bottom-left, one line on what the document is for |
| `margins` | `(left, right, top, bottom)` in points |
| `fonts` | `(regular, bold, italic)` names; see Custom fonts below |
| `motif_box` | `(w, h)` in points; default 62mm x 72mm |
| `cover_text_top` | gap above the cover text block; raise it to push the title down |
| `title` `author` | PDF metadata |

Useful attributes: `doc.frame_w` (body frame width in points),
`doc.styles` (the `ParagraphStyle` dict), `doc.story` (the flowable list),
`doc.theme`.

The cover page and the `NextPageTemplate` switch are laid out in the
constructor, so the first thing you add is already page 2.

## Content methods

Every method returns `self`, so calls chain.

### Structure

```python
doc.section(kicker, heading, lead="")   # kicker, H1, accent rule, lead paragraph
doc.h2(text)                            # 12.4pt accent sub-heading
doc.h3(text)                            # 10.2pt deep sub-sub-heading
doc.page_break()
doc.spacer(height=4*mm)
```

`section()` is how every major part opens. End each part with `page_break()`.

### Text

```python
doc.lead(text)      # 11/15.5, one intro paragraph per section
doc.p(text)         # 9.6/13.6, the workhorse
doc.small(text)     # 8.4/11.6 grey, captions and dense reference runs
doc.say(text)       # italic in `say`, suggested lines and pull quotes
doc.bullets(items, numbered=False)
```

`bullets(numbered=True)` uses bold numerals - reserve it for genuine sequences
(causal chains, steps, chronologies), not for every list.

### Tables

```python
doc.table(rows, widths=None, header=True, bold_first_col=True,
          zebra=True, align=None)
```

- `rows` is a list of tuples/lists; `rows[0]` is the header row when
  `header=True`.
- `widths` are **relative weights**, normalised to the frame width - `[30, 70]`
  and `[3, 7]` are the same table. Omit for equal columns. A table can never
  overhang the margin.
- Cells may be strings (wrapped in a `Paragraph` automatically) or flowables.
- `align` takes a per-column list like `[None, "right", "center"]`.
- The header row repeats across page breaks.

Two convenience wrappers:

```python
doc.contents(rows, headings=("#", "Section", "What it gives you"))
doc.sources(rows, headings=("Source", "Domain"))
```

### Callout boxes

```python
doc.box(body, title="", kind="note")     # kind: "note" | "quote" | "warn"
```

`body` is a string or a list of strings/flowables. `kind` picks the fill:
`note` for TL;DRs and conventions, `quote` for quoted material, `warn` for
caveats and sensitive-material notes. The 2.6pt `alt` bar on the left edge is
the signature detail. One or two boxes per section, maximum.

### Profiles and fact banks

```python
doc.profile(name, role="", points=(), takeaway="")
doc.fact_bank(facts, numbered=True)
```

`profile()` is for repeated entities - people, characters, products, locations -
and is wrapped in `KeepTogether` so it never splits across a page.

### Escape hatch

```python
doc.add(flowable)     # append any Platypus flowable
doc.build()           # writes the PDF, returns the path
```

## Colour helpers

```python
tint(seed, l=None, s=None, s_mul=None)   # keep hue, change lightness/saturation
scale(seed, k)                           # multiply RGB; good for lifting darks
mix(a, b, t)                             # linear blend, t=0 -> a, t=1 -> b
```

## Custom fonts

The built-in Helvetica family needs no files and always embeds. Only swap it
when the subject genuinely demands it.

```python
from dossier import use_font_family
fonts = use_font_family("Inter-Regular.ttf", "Inter-Bold.ttf",
                        "Inter-Italic.ttf", family="Inter")
doc = Dossier(..., fonts=fonts)
```

The font must cover every glyph you use, and the size scale may need nudging -
Helvetica's metrics are what the 9.6/13.6 body setting was tuned against.

## Scripts

```bash
python scripts/preview_cover.py --title "X" --preset lab-teal --motif flask
python scripts/preview_cover.py --preset lab-teal --all-motifs --out sheet.pdf
python scripts/new_dossier.py --title "X" --preset lab-teal --motif flask
python scripts/check_pdf.py out.pdf --expect "Sources"
```

`preview_cover.py --help` lists every cover field it accepts.
`check_pdf.py` exits 1 on failure so it can gate a loop.

## Paragraph markup that is safe

ReportLab `Paragraph` accepts a small HTML subset. These are safe with the
built-in fonts:

| Want | Write |
|---|---|
| bold / italic | `<b>`, `<i>` |
| line break | `<br/>` |
| middle dot | `&#183;` |
| em dash | `&#8212;` |
| bullet | `&#8226;` |
| non-breaking space | `&nbsp;` |
| superscript / subscript | `<super>2</super>`, `<sub>2</sub>` |
| a colour or size shift inside a line | `<font face='Helvetica' size=8.4 color='#6E6B7A'>...</font>` |

Never paste Unicode sub/superscripts, arrows, or box-drawing characters -
`check_pdf.py` will flag them, but it is easier not to.
