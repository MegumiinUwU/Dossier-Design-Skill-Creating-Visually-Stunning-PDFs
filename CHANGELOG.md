# Changelog

## 1.2.0

**Fixed**

- Callout fills no longer collapse into each other. `quotebg` and `warnbg` are
  derived from `accent` and `alt`, and when either seed was low in saturation
  the resulting tint came out indistinguishable from the neutral `boxbg`, so
  note, quote and caution boxes all read as the same box. Both derivations now
  carry a saturation floor. Saturated seeds sit well above it and are
  unaffected; of the seven bundled palettes only `archive-sepia` and
  `folk-crimson` move at all, by 2 and 1 total RGB units.
- The packaging script now tracks every version field in every manifest rather
  than one per file. The Cursor marketplace carries a version on the
  marketplace itself as well as on the plugin entry, and the second one was
  going stale on each bump without anything noticing.

**Added**

- The distributed skill carries its own `LICENSE`. The zip is uploaded on its
  own and detaches from the repository, so the licence now travels with it.
- A CI workflow that validates every manifest and `SKILL.md`, builds the
  bundled example, scaffolds and builds a fresh dossier, renders every motif,
  verifies the output PDFs, and uploads the packaged zip as an artifact. The
  packaging script was already a gate; now something actually runs it.
- This changelog.

## 1.0.0

First release.

- `SKILL.md` with the five step workflow, the non-negotiables, and a map of the
  reference files.
- Six reference documents: theming, cover motifs, the API, the full style spec,
  dossier content conventions, and symptom-first troubleshooting.
- `dossier.py`, a ReportLab builder library. Table column widths are normalised
  to the frame width and every cell is wrapped in a `Paragraph`, so the two
  layout failures this style used to produce cannot happen.
- `motifs.py` with 21 cover motifs and a recipe for drawing new ones.
- Seven subject palettes, each derived from three seed colours, with neutrals
  tinted toward the subject hue rather than kept grey.
- `preview_cover.py` for a single cover or a contact sheet of every motif,
  `new_dossier.py` to scaffold a build script, and `check_pdf.py` to catch
  margin overhang, undrawable characters, blank pages and missing content.
- Plugin and marketplace manifests for both Claude Code and Cursor, plus
  `package_skill.py` to validate them and build the upload zip.
