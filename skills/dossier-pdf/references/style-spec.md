# Style spec

Every number in the style. Read this to hand-roll the layout in raw ReportLab,
to port it to another toolchain, or to add a component that keeps the look.

## Contents

- Core idea
- Page setup
- Running header and footer
- Cover
- Typography scale
- Components: section opener, callout box, table, list, profile
- Spacing rhythm
- Hard rules
- Porting to another toolchain

## Core idea

A research dossier, not a report: a dramatic dark cover with a single graphic
motif, then clean high-density body pages. Body pages are deliberately plain and
text-dense - all the personality lives in the cover, the rules, the kicker
labels and the two accent colours. Compact leading and small type so a page
holds a lot without feeling cramped.

Colours are named as in `Theme`: `deep`, `accent`, `alt`, `band`, `say`, `ink`,
`body`, `grey`, `rule`, `boxbg`, `quotebg`, `warnbg`. See
[theming.md](theming.md) for how they are derived.

## Page setup

```
Page size   A4 (210 x 297mm). LETTER works; every measurement below is absolute
            except the frame width, which follows the margins.
Margins     20mm left/right, 22mm top, 20mm bottom
Cover frame full width, full height between margins
Body frame  full width, height = page height - 42mm
Frame width 170mm on A4 - all full-width elements match this exactly
```

Two `PageTemplate`s: `cover` (own frame plus a canvas painter) and `body`.
Use a `BaseDocTemplate`, not `SimpleDocTemplate`, so the cover can have its own
painter, and switch with `NextPageTemplate("body")` followed by `PageBreak()`
after the cover flowables.

## Running header and footer

Body pages only. The cover carries none of this.

| Element | Position | Style |
|---|---|---|
| top hairline | `H - 16mm`, margin to margin | 0.4pt `rule` |
| bottom hairline | `14mm`, margin to margin | 0.4pt `rule` |
| subject line | top-left, baseline `H - 14mm` | 7.2pt regular `grey`, ALL CAPS, `SUBJECT / DOCUMENT TYPE` |
| credit line | top-right, same baseline | same style; author, studio, date range |
| purpose line | bottom-left, baseline `10.5mm` | 7.2pt regular `grey`, one line on what the document is for |
| page number | bottom-right, same baseline | 8pt bold `accent` |

The page number is offset so the cover is not page 1: print `doc.page - 1`.

## Cover

Dark, centred, three horizontal zones, drawn on the canvas with no images.

1. Fill the whole page `deep`.
2. Fill the top 40% (`y` from `0.60H` to `H`) with `band`.
3. Motif centred at `(W/2, 0.765H)` in a 62 x 72mm box. See
   [cover-motifs.md](cover-motifs.md).
4. A 2pt `accent` horizontal line at `0.585H`, inset 28mm each side.
5. Text block, all centred, starting 118mm below the top margin:

| Element | Style |
|---|---|
| kicker | 10pt bold, `alt`, ALL CAPS, one line of framing |
| title | 40/42 bold, `cover_title` (white) |
| subtitle | 13/18 regular, `cover_sub` |
| blurb | 8.6/12.6 regular, `cover_blurb`, two lines split with `<br/>` |
| meta | same as blurb; facts joined with ` &#183; ` |

Vertical gaps in the text block: 8pt after the kicker, 6pt after the title,
12pt before the blurb, 9pt before the meta line.

The lower third stays empty on purpose.

## Typography scale

Helvetica family throughout (`Helvetica`, `Helvetica-Bold`,
`Helvetica-Oblique`). Sizes are in points, given as size/leading.

| Style | Font | Size/Leading | Colour | Notes |
|---|---|---|---|---|
| `h1k` kicker | Bold | 8/10 | `alt` | ALL CAPS, e.g. "PART 3", 2pt after |
| `h1` | Bold | 19/22 | `deep` | 4pt after, then the accent rule |
| `h2` | Bold | 12.4/15 | `accent` | 11pt before, 3pt after |
| `h3` | Bold | 10.2/13 | `deep` | 7pt before, 2pt after |
| `lead` | Regular | 11/15.5 | `ink` | one intro paragraph per section, 7pt after |
| `p` body | Regular | 9.6/13.6 | `body` | the workhorse, 5pt after |
| `bullet` | Regular | 9.5/13.2 | `body` | 2.5pt after - tight lists |
| `say` | Oblique | 9.4/13 | `say` | pull lines, 10pt left indent |
| `quote` | Oblique | 9.8/14 | `deep` | inside quote boxes, 8pt indents both sides |
| `small` | Regular | 8.4/11.6 | `grey` | captions, dense reference runs |
| box title | Bold | 9.4/12.6 | `alt` | first line inside a callout |
| table header | Bold | 8.4/11 | white | on `deep` fill |
| table cell | Regular | 8.4/11.4 | `body` | first column bold `deep` |

Small sizes are intentional. Do not scale up - the density is the look.

## Components

### Section opener

Kicker -> H1 -> 1.6pt `accent` rule (full frame width, 8pt space after) -> one
`lead` paragraph. Every major section starts this way and ends with a page
break. Consistency here is most of what makes the document feel edited.

### Callout box

A one-cell table at full frame width:

- fill `boxbg` (notes, TL;DRs, conventions), `quotebg` (quoted material) or
  `warnbg` (caveats, sensitive material)
- 0.6pt `rule` box border
- **2.6pt `alt` vertical bar on the left edge** (`LINEBEFORE`) - the signature
  detail; without it the box is just a grey rectangle
- padding: 9 left/right, 7 top, 5 bottom
- optional bold `alt` 9.4pt title line inside
- 4pt space before, 6pt after

One or two per section, maximum. A page of boxes is a page with no hierarchy.

### Table

- header row: `deep` fill, white bold 8.4pt, repeats across page breaks
- zebra striping: `boxbg` on alternating body rows
- 0.4pt `rule` line below every row, 0.6pt box outline
- `VALIGN=TOP`, padding 6 horizontal / 4.5 vertical
- first column bold `deep` - it acts as a row label
- every cell wrapped in a `Paragraph`, or long text overflows the column
- column widths must sum to the frame width
- 4pt space before, 7pt after

### List

`ListFlowable`, `bulletType="bullet"`, `leftIndent=13`, `bulletFontSize=8`,
2pt before / 4pt after. Numbered variants use `bulletType="1"`, `leftIndent=15`
and a bold bullet font - reserve numbering for genuine sequences.

### Profile block

For repeated entities. An H3 with the name, then the role at 8.4pt regular
`grey` after a `&#183;`, then `&#8226;`-prefixed paragraphs indented 10pt, then
an optional `say` line. Wrap the whole thing in `KeepTogether` so a profile
never splits across a page.

## Spacing rhythm

The document has one vertical rhythm and it is tight:

- between paragraphs: 5pt
- between bullets: 2.5pt
- before a sub-heading: 11pt (H2), 7pt (H3)
- around a table or box: 4pt before, 6-7pt after
- after a section rule: 8pt

If a page looks airy, the content is thin - add content rather than spacing.

## Hard rules

- **Never** use Unicode sub/superscripts or exotic glyphs with the built-in
  fonts - they render as black boxes. Use `<sub>`/`<super>` tags.
- Every table cell must be a `Paragraph`, or long text overflows.
- Column widths must sum to the frame width or the table silently overhangs the
  margin.
- All accented and special characters go in as HTML entities inside `Paragraph`
  markup.
- Use `KeepTogether` for any block that reads badly split - profiles, boxes with
  titles, a heading with its first paragraph.
- Verify after building: page count, character count, and a spot-check that key
  strings actually made it into the extracted text. `scripts/check_pdf.py` does
  all three plus margin overflow.

## Porting to another toolchain

If you rebuild this in HTML/CSS, LaTeX or InDesign, these are the things that
carry the look, in order of importance:

1. The cover: dark ground, lighter top band, one motif, the 2pt accent rule at
   58.5% height, centred kicker/title/subtitle/blurb/meta.
2. The type scale, especially the 9.6/13.6 body and the 8.4pt tables.
3. The section opener: small `alt` caps kicker, 19pt `deep` H1, accent rule.
4. The callout box's 2.6pt warm left bar.
5. The dark table header with a bold first column.
6. Neutrals tinted toward `deep`'s hue rather than true grey.

Everything else is negotiable.
