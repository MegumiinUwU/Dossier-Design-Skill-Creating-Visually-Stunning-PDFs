# Theming

How to turn a subject into a palette, what gets derived from what, and three
worked examples.

## Contents

- Choosing the three seeds
- What gets derived, and the exact rules
- Overriding a derived colour
- Worked example: clockpunk platformer
- Worked example: folk horror
- Worked example: psychological horror
- Presets
- Checks before you commit to a palette

## Choosing the three seeds

Look at the subject and answer three questions.

**`deep` - what colour is this subject at night?** Very dark, lightness around
0.12 to 0.16, and almost never neutral black. A forest horror game is plum. A
maritime story is navy. An archive story is bitumen brown. This colour fills the
cover, sets every H1 and every table header, and its hue leaks into every
neutral in the document, so it decides more than any other choice.

**`accent` - what is the subject's structural colour?** Mid-tone, usually cooler
than `alt`, and it must read clearly as text on white because H2s are set in it.
Aim for lightness 0.35 to 0.50. This is the colour of rules, page numbers and
sub-headings: it is the document's skeleton, not its jewellery.

**`alt` - what is the one warm or bright thing in the subject?** The blood, the
lamp, the neon sign, the brand red. This appears in exactly three places -
kickers, the left bar on callout boxes, and one element of the cover motif - and
it is what stops the document reading as merely tidy.

Two failure modes, both common:

- **`accent` and `alt` too close in hue.** They stop being two colours and the
  document flattens. Keep them at least 60 degrees apart on the wheel, or make
  one clearly warmer.
- **`accent` too light.** It is used for 12.4pt sub-heading text on white. Below
  a 3:1 contrast ratio it turns to mush. Darken it rather than making it bigger.

## What gets derived, and the exact rules

`Theme.from_seeds()` produces fourteen more colours. All hues follow a seed, so
the palette can never disagree with itself. `tint(seed, l=, s_mul=)` keeps the
seed's hue and changes lightness / saturation.

| Derived | Rule | Used for |
|---|---|---|
| `band` | `scale(deep, 1.38)` | the lighter top 40% of the cover |
| `ink` | `deep` at 72% of its lightness | lead paragraphs |
| `body` | `deep` at L 0.16, S x0.55 | all body text |
| `grey` | `deep` at L 0.44, S x0.25 | captions, running header and footer |
| `rule` | `deep` at L 0.851, S x0.55 | hairlines, table borders |
| `boxbg` | `deep` at L 0.969, S x1.40 | neutral callout fill, table zebra stripe |
| `quotebg` | `accent` at L 0.955 | quote and info callout fill |
| `warnbg` | `alt` at L 0.963 | caution and sensitive-material fill |
| `say` | `accent` at L 0.36 | italic pull lines and suggested phrasings |
| `cover_sub` | `deep` at L 0.81, S x0.75 | cover subtitle |
| `cover_blurb` | `deep` at L 0.62, S x0.55 | cover blurb and meta line |
| `motif_fill` | `deep` at L 0.955, S x1.15 | the motif silhouette |
| `motif_stroke` | `deep` at L 0.72, S x0.50 | the motif outline |

The important consequence: **neutrals are not neutral.** A plum dossier's
hairlines are `#DBD4DA`, not `#D6D2E0`. Nobody notices individually and everyone
notices in aggregate. Do not "fix" this by substituting true greys.

## Overriding a derived colour

Pass any field as a keyword. Override sparingly - each one is a chance to break
the internal agreement.

```python
theme = Theme.from_seeds("#2A1B28", "#3E6B52", "#B0304A",
                         say="#9C6B22",          # a third subject colour
                         motif_fill="#F2ECE4")   # warm cream, not cool white
```

The two worth overriding in practice:

- **`say`** when the subject has a genuine third colour. The derived default is
  a deeper version of `accent`, which is safe but says nothing.
- **`motif_fill`** when the cover wants warm cream rather than cool off-white.
  A linen or embroidery subject reads wrong in blue-white.

## Worked example: clockpunk platformer

Sunset over Madrid rooftops, brass clockwork, a stolen sun.

```python
Theme.from_seeds(deep="#1B1A30", accent="#3B7EA1", alt="#C98A2E")
```

`deep` is the night sky the game is set under. `accent` is the cold steel-blue
of the machinery. `alt` is brass, and it is the only warm thing on the cover -
one dot at the tip of the stopwatch hand. Motif: `stopwatch`.

## Worked example: folk horror

Czech countryside, embroidery, a mother walking into the dark.

```python
Theme.from_seeds(deep="#2A1B28", accent="#3E6B52", alt="#B0304A",
                 say="#9C6B22", motif_fill="#F2ECE4", motif_stroke="#A9989F")
```

`deep` is plum, not black - the palette of a dim interior. `accent` is moss
green: the forest, and cool enough to hold sub-heading text. `alt` is the red
thread, used once on the cover as a flame between the antlers. `say` is ochre,
a third colour the subject actually has. `motif_fill` is overridden to warm
cream so the deer reads as linen rather than porcelain. Motif: `antlered_head`.

## Worked example: psychological horror

A prosthetic face, blue pigtails, ninety-nineties cartoon palette over a very
dark story.

```python
Theme.from_seeds(deep="#1E1B2E", accent="#2E7DB8", alt="#C4577F", say="#2E8B87")
```

Indigo, the cartoon's own blue, and the character's pink. The pink appears once
on the cover, as the patch over one eye. Motif: `stitched_mask`.

## Presets

`Theme.preset(name)` - all take the same overrides as `from_seeds`.

| Name | Fits |
|---|---|
| `midnight-ink` | the cool default; horror, mystery, general research |
| `clockwork-amber` | machinery, time, craft, retro technology |
| `folk-crimson` | folklore, rural dread, textiles, ritual |
| `boardroom-slate` | business, markets, competitive research |
| `lab-teal` | science, medicine, technical subjects |
| `archive-sepia` | history, archives, long-form journalism |
| `signal-violet` | software, AI, systems, infrastructure |

Treat presets as a starting point when the subject has no obvious colours, not
as a substitute for looking at it.

## Checks before you commit to a palette

1. Render the cover and a body page to PNG and look at both.
2. Is `accent` legible as 12.4pt bold text on white? If you squint and it
   greys out, darken it.
3. Is there exactly one warm spot on the cover?
4. Do the callout fills read as three distinguishable tints, or has one of them
   collapsed to white? `warnbg` collapses when `alt` is very desaturated -
   override it with a stronger tint if so.
5. Would someone who knows the subject recognise the palette as belonging to
   it? If not, the seeds are generic. Go back to the source material.
