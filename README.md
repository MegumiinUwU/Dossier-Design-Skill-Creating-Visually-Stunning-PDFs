# Dossier PDF: an Agent Skill

Turn researched material into a PDF that looks commissioned: a dark cover whose
palette and geometric motif are derived from the subject, then dense editorial
body pages with themed tables, callout boxes and running furniture.

The style's one idea: **the palette and the motif come from the subject, not
from a fixed brand.** A folk-horror dossier is plum and crimson with a deer's
head. A clockpunk one is indigo and amber with a stopwatch. Same document, same
type scale, different soul.

![Cover and two body pages from the bundled example](skills/dossier-pdf/assets/preview.png)

## Examples

Three dossiers produced end to end by an agent that was asked to research three
games online in depth, gather the guides and coverage, and turn all of it into
source material for an eight minute video script on each. Same skill, same type
scale, three palettes and three motifs pulled from the subjects themselves.

Click any image for full resolution.

**Duskfade**, a clockpunk platformer. Indigo, steel blue and brass, with a stopwatch.

![Duskfade dossier: cover, contents page and fact sheet](screenshots/duskfade.png)

**Scarlet Deer Inn**, embroidered folk horror. Plum, moss and crimson, with an antlered head.

![Scarlet Deer Inn dossier: cover, contents page and character tables](screenshots/scarlet-deer-inn.png)

**Sally Face**, psychological horror. Indigo, blue and pink, with a stitched mask.

![Sally Face dossier: cover, contents page and developer profile](screenshots/sally-face.png)

## Install

### Simplest: just ask your agent

Paste this to Claude Code, Cursor, or any agent that can read a repo:

```
Install the dossier-pdf skill from
https://github.com/MegumiinUwU/Dossier-Design-Skill-Creating-Visually-Stunning-PDFs/tree/main/skills/dossier-pdf
```

### Claude Code

```bash
claude plugin marketplace add MegumiinUwU/Dossier-Design-Skill-Creating-Visually-Stunning-PDFs
```

```bash
claude plugin install dossier-pdf@dossier-design
```

`dossier-design` is the marketplace name, `dossier-pdf` the plugin. In an
interactive session, `/plugin` browses the same thing.

### Cursor

Add the repo from **Settings → Customize → Plugins**, or point Cursor at the
marketplace manifest at `.cursor-plugin/marketplace.json`. The skill is
discovered automatically from `skills/dossier-pdf/SKILL.md`.

### Skill upload (claude.ai, ChatGPT, and other hosts)

Download **`dossier-pdf.zip`** from
[Releases](https://github.com/MegumiinUwU/Dossier-Design-Skill-Creating-Visually-Stunning-PDFs/releases)
and upload it as a skill.

> Do **not** use GitHub's *Code → Download ZIP*. That nests everything under a
> `repo-name-main/` folder, and skill uploaders require `SKILL.md` at the zip
> root. The release asset is built for that shape by
> [`scripts/package_skill.py`](scripts/package_skill.py).

### Manual copy

```bash
cp -r skills/dossier-pdf ~/.claude/skills/     # personal
cp -r skills/dossier-pdf .claude/skills/       # project-scoped
```

### Dependencies

```bash
pip install reportlab        # required
pip install pymupdf          # optional: PNG previews and margin checks
```

Once installed, the skill triggers on requests like *"turn this research into a
dossier PDF"*, *"make me a briefing document"*, or *"give this PDF a proper
designed cover"*.

## Use it without an agent

The Python library stands on its own:

```bash
python skills/dossier-pdf/scripts/new_dossier.py --title "Scarlet Deer Inn" \
    --preset folk-crimson --motif antlered_head --out build.py
```

```bash
python build.py
```

```bash
python skills/dossier-pdf/scripts/check_pdf.py scarlet_deer_inn_dossier.pdf
```

See every bundled motif in your own palette:

```bash
python skills/dossier-pdf/scripts/preview_cover.py --preset folk-crimson \
    --all-motifs --out motifs.pdf
```

## What is in here

```
.claude-plugin/                   Claude Code plugin + marketplace manifests
.cursor-plugin/                   Cursor plugin + marketplace manifests
scripts/
  package_skill.py                validate every manifest, build the release zip
skills/dossier-pdf/
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

## Releasing

```bash
python scripts/package_skill.py --version 1.1.0 --clean
```

Bumps the version in all four manifests, checks they agree, validates every
`SKILL.md` (frontmatter limits, body length, that linked reference files exist),
and writes `dist/dossier-pdf.zip` with `SKILL.md` at its root. Use
`--validate-only` in CI.

## License

MIT.
