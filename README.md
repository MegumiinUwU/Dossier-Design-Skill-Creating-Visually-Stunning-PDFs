# Dossier PDF — an Agent Skill

Turn researched material into a PDF that looks commissioned: a dark cover whose
palette and geometric motif are derived from the subject, then dense editorial
body pages with themed tables, callout boxes and running furniture.

The style's one idea: **the palette and the motif come from the subject, not
from a fixed brand.** A folk-horror dossier is plum and crimson with a deer's
head. A clockpunk one is indigo and amber with a stopwatch. Same document, same
type scale, different soul.

![Cover and two body pages from the bundled example](dossier-pdf/assets/preview.png)

## Install

Copy the `dossier-pdf/` folder into your skills directory:

```bash
# Claude Code / Claude Desktop, personal skills
cp -r dossier-pdf ~/.claude/skills/

# or, project-scoped
cp -r dossier-pdf .claude/skills/
```

Then:

```bash
pip install reportlab        # required
pip install pymupdf          # optional: PNG previews and margin checks
```

The skill triggers on requests like *"turn this research into a dossier PDF"*,
*"make me a briefing document"*, or *"give this PDF a proper designed cover"*.

## Use it without an agent

The Python library stands on its own:

```bash
python dossier-pdf/scripts/new_dossier.py --title "Scarlet Deer Inn" \
    --preset folk-crimson --motif antlered_head --out build.py
python build.py
python dossier-pdf/scripts/check_pdf.py scarlet_deer_inn_dossier.pdf
```

See every bundled motif in your own palette:

```bash
python dossier-pdf/scripts/preview_cover.py --preset folk-crimson \
    --all-motifs --out motifs.pdf
```

## What is in here

```
dossier-pdf/
  SKILL.md                        the skill itself: workflow and non-negotiables
  references/
    theming.md                    turning a subject into a palette
    cover-motifs.md               the 21 bundled motifs, and writing your own
    api.md                        every method and argument
    style-spec.md                 every number, for hand-rolling or porting
    content-structure.md          what a dossier contains and how to write it
    troubleshooting.md            symptom-first fixes
  scripts/
    dossier.py                    the builder library
    motifs.py                     21 cover motifs
    preview_cover.py              render a cover, or a motif contact sheet
    new_dossier.py                scaffold a build script
    check_pdf.py                  verify before shipping
  assets/
    example_dossier.py            a complete, runnable document
```

## Credit

Built from three research dossiers whose covers, palettes and typography set the
standard this skill generalises.

MIT licensed.
