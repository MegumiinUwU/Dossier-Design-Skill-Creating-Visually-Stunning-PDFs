# Cover motifs

The motif is the single graphic on the cover. It is what makes a reader believe
the document was made for this subject specifically.

## Contents

- The rules
- The bundled motifs
- Choosing one
- Writing a custom motif
- The signature: geometry of the cover
- Common mistakes

## The rules

1. **One object.** The subject's most iconic single thing. Not a scene, not a
   composition, not two objects side by side.
2. **8 to 14 primitives.** `circle`, `rect`, `roundRect`, `ellipse`, `line`, and
   bezier paths. A recognisable silhouette, not an illustration. If you are
   drawing a fifteenth shape, you are rendering, not signalling.
3. **Three colours, and only three.** The silhouette is `t.motif_fill` outlined
   in `t.motif_stroke`. Exactly **one** element is `t.alt` - the flame between
   the antlers, the dot on the stopwatch hand, the patch over the eye. `t.deep`
   may be used for holes and eyes because it is the background colour.
4. **It sits in the band.** The motif occupies the lighter top 40% of the cover.
   Bleeding slightly past the motif box is fine and often looks better (the mask
   motif's straps run wider than its box on purpose).

## The bundled motifs

Twenty-one ship in `scripts/motifs.py`. Render them all in your own palette
before choosing:

```bash
python scripts/preview_cover.py --preset folk-crimson --all-motifs --out motifs.pdf
```

| Motif | Fits |
|---|---|
| `stopwatch` | time, deadlines, speedruns, loops, anything counted down |
| `antlered_head` | folklore, forests, hunting, rural dread, myth |
| `stitched_mask` | identity, masks, psychological horror, hidden faces |
| `monitor` | software, media, screens, surveillance |
| `key` | secrets, access, unlocks, investigations |
| `flask` | science, medicine, chemistry, experiments |
| `book` | history, archives, lore, literature, long-form research |
| `camera` | film, video, photography, documentaries |
| `compass` | exploration, navigation, strategy, orientation |
| `cog` | industry, engineering, process, systems |
| `skyline` | cities, companies, institutions, real estate |
| `envelope` | correspondence, leaks, communications |
| `shield` | security, defence, law, risk and safety |
| `waveform` | music, audio, podcasts, voice, sound design |
| `leaf` | nature, agriculture, climate, sustainability |
| `chart_bars` | markets, metrics, performance, analytics |
| `globe` | geopolitics, international subjects, travel |
| `microphone` | interviews, oral history, broadcasting, testimony |
| `doorway` | thresholds, transitions, interiors, "what is inside" |
| `crown` | power, monarchy, market leaders, championships |
| `eye` | observation, conspiracy, oversight, being watched |

## Choosing one

Ask what object the reader would picture if they had to draw the subject from
memory in five seconds. If a bundled motif is that object, use it. If it is
only *adjacent* to that object, write a custom one - a generic `book` on a
dossier about a specific building is worse than a rough outline of the building.

## Writing a custom motif

Signature, always:

```python
def my_motif(c, x, y, w, h, t):
    """One line saying what subjects this fits."""
```

`c` is the ReportLab canvas. `(x, y)` is the bottom-left of the motif box in
points, `(w, h)` its size (62mm x 72mm by default). `t` is the Theme; use only
`t.motif_fill`, `t.motif_stroke`, `t.alt` and `t.deep`.

Work in fractions of `w` and `h` so the motif survives a different box size:

```python
import math

def lighthouse(c, x, y, w, h, t):
    """Maritime subjects, isolation, warning, guidance."""
    cx = x + w / 2
    base, top = y + h * 0.14, y + h * 0.78
    c.setLineJoin(1)
    c.setFillColor(t.motif_fill)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.3)

    # tower: a tapering quad
    p = c.beginPath()
    p.moveTo(cx - w * 0.20, base); p.lineTo(cx + w * 0.20, base)
    p.lineTo(cx + w * 0.11, top);  p.lineTo(cx - w * 0.11, top)
    p.close()
    c.drawPath(p, stroke=1, fill=1)

    # gallery and lamp room
    c.rect(cx - w * 0.16, top, w * 0.32, h * 0.035, stroke=1, fill=1)
    c.setFillColor(t.deep)
    c.rect(cx - w * 0.10, top + h * 0.035, w * 0.20, h * 0.10, stroke=1, fill=1)

    # the one warm element: the light itself
    c.setFillColor(t.alt)
    c.circle(cx, top + h * 0.085, w * 0.055, stroke=0, fill=1)
    for side in (-1, 1):                       # two beams
        c.setLineWidth(2.2)
        c.setStrokeColor(t.alt)
        c.line(cx + side * w * 0.12, top + h * 0.085,
               cx + side * w * 0.38, top + h * 0.15)

    # bands and ground line
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.0)
    for f in (0.30, 0.60):
        yy = base + (top - base) * f
        half = w * (0.20 - 0.09 * f)
        c.line(cx - half, yy, cx + half, yy)
    c.setLineWidth(1.6)
    c.line(x + w * 0.05, base, x + w * 0.95, base)
```

Then pass it directly - it does not need to be registered:

```python
doc = Dossier(..., motif=lighthouse)
```

To preview it, drop the function into a scratch file that imports `Dossier` and
render the cover. Iterate on the PNG; nobody gets a silhouette right first try.

Two techniques that carry most custom motifs:

- **Tapered shapes** come from a four-point path, not a rectangle. Wide at one
  end, narrow at the other.
- **Rounded organic shapes** come from `beginPath` + `curveTo`. The
  `_teardrop()` helper in `motifs.py` draws the wide-top / narrow-bottom form
  used for the deer's head; it works for faces, leaves, flames and drops.

## The signature: geometry of the cover

Drawn by `Dossier._paint_cover`, in case you need to match it by hand:

1. Fill the whole page `deep`.
2. Fill the top 40% (`y` from `0.60H` to `H`) with `band`.
3. Draw the motif centred at `(W/2, 0.765H)` in a 62mm x 72mm box.
4. A 2pt `accent` line at `0.585H`, inset 28mm each side. This is the band's
   edge and the page's spine, and it is the single most recognisable element of
   the style - never omit it.
5. The text block starts 118mm down from the top margin: centred kicker (10pt
   bold `alt`, all caps), title (40/42 bold white), subtitle (13/18), blurb
   (8.6/12.6, two lines), meta (same, facts joined by `&#183;`).

The lower third of the cover stays empty. That negative space is deliberate -
filling it is the fastest way to make the cover look like a template.

## Common mistakes

- **Two accent colours in the motif.** It stops being a signal and becomes
  clip art.
- **Too much detail.** At A4 the motif is about 60mm wide. Anything finer than
  ~1mm disappears in print and muddies on screen.
- **Centring the motif on the whole page** rather than in the band. It then
  collides with the accent rule.
- **Using an image instead.** Photographs and logos break the style completely -
  the flat geometric silhouette is what makes the dark cover work.
