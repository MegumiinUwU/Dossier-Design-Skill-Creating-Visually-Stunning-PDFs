"""motifs.py - cover motifs for the Dossier PDF style.

A motif is one recognisable silhouette drawn from canvas primitives, 8-14 of
them, no images. Every motif here has the same signature:

    def name(c, x, y, w, h, t) -> None

    c  reportlab canvas
    x, y  bottom-left of the motif box, in points
    w, h  size of the motif box, in points
    t  the Theme; use t.motif_fill, t.motif_stroke, t.alt, t.deep only

Colour discipline: the silhouette is `motif_fill` outlined in `motif_stroke`,
and exactly ONE element is `alt`. That single warm spot is what makes the
cover read as designed rather than decorated. Do not add a third colour.

Pick one with MOTIFS["key"], or write your own - see
references/cover-motifs.md for the recipe.
"""

from __future__ import annotations

import math

__all__ = ["MOTIFS", "get"]


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

def _prep(c):
    c.setLineJoin(1)
    c.setLineCap(1)


def _fill(c, t):
    c.setFillColor(t.motif_fill)
    c.setStrokeColor(t.motif_stroke)


def _poly(c, pts, close=True, fill=1, stroke=1):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    c.drawPath(p, stroke=stroke, fill=fill)


def _teardrop(c, cx, top, bot, half_top, half_bot, fill=1, stroke=1):
    """A rounded shape wide at the top, narrow and rounded at the bottom."""
    mid = bot + (top - bot) * 0.45
    p = c.beginPath()
    p.moveTo(cx - half_bot, mid)
    p.curveTo(cx - half_top, mid + (top - mid) * 0.45,
              cx - half_top, top - (top - mid) * 0.25, cx, top)
    p.curveTo(cx + half_top, top - (top - mid) * 0.25,
              cx + half_top, mid + (top - mid) * 0.45, cx + half_bot, mid)
    p.curveTo(cx + half_bot, bot + (mid - bot) * 0.25,
              cx + half_bot * 0.6, bot, cx, bot)
    p.curveTo(cx - half_bot * 0.6, bot,
              cx - half_bot, bot + (mid - bot) * 0.25, cx - half_bot, mid)
    p.close()
    c.drawPath(p, stroke=stroke, fill=fill)


# --------------------------------------------------------------------------
# motifs
# --------------------------------------------------------------------------

def stopwatch(c, x, y, w, h, t):
    """Clocks, deadlines, time loops, speedruns, anything about a countdown."""
    _prep(c)
    cx, cy = x + w / 2, y + h * 0.58
    r = min(w * 0.44, h * 0.30)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(2)
    c.line(cx, cy + r, cx, cy + r + h * 0.09)
    _fill(c, t)
    c.roundRect(cx - w * 0.09, cy + r + h * 0.09, w * 0.18, h * 0.030,
                h * 0.012, stroke=1, fill=1)
    c.setLineWidth(1.6)
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.setLineWidth(0.8)
    c.circle(cx, cy, r * 0.86, stroke=1, fill=1)
    c.setLineWidth(1.1)
    c.setStrokeColor(t.motif_stroke)
    for i in range(12):
        a = math.radians(i * 30)
        c.line(cx + math.sin(a) * r * 0.70, cy + math.cos(a) * r * 0.70,
               cx + math.sin(a) * r * 0.78, cy + math.cos(a) * r * 0.78)
    c.setStrokeColor(t.deep)
    c.setLineWidth(2.4)
    c.line(cx, cy, cx - r * 0.34, cy - r * 0.36)
    c.setStrokeColor(t.alt)
    c.setLineWidth(2.2)
    tipx, tipy = cx + r * 0.52, cy + r * 0.52
    c.line(cx, cy, tipx, tipy)
    c.setFillColor(t.alt)
    c.circle(tipx, tipy, w * 0.035, stroke=0, fill=1)
    c.setFillColor(t.deep)
    c.circle(cx, cy, w * 0.042, stroke=0, fill=1)
    _fill(c, t)
    c.setLineWidth(1.2)
    c.setStrokeColor(t.motif_stroke)
    c.line(cx, cy - r, cx, cy - r - h * 0.09)
    c.circle(cx, cy - r - h * 0.12, w * 0.05, stroke=1, fill=1)


def antlered_head(c, x, y, w, h, t):
    """Folk horror, forests, hunting, myth, rural dread."""
    _prep(c)
    cx = x + w / 2
    top, bot = y + h * 0.58, y + h * 0.06
    c.setStrokeColor(t.motif_fill)
    c.setLineWidth(1.7)
    for side in (-1, 1):
        bx, by = cx + side * w * 0.14, y + h * 0.60
        c.line(bx, by, bx + side * w * 0.10, y + h * 0.86)
        c.line(bx + side * w * 0.10, y + h * 0.86,
               bx + side * w * 0.22, y + h * 0.95)
        c.line(bx + side * w * 0.035, y + h * 0.69,
               bx + side * w * 0.19, y + h * 0.74)
        c.line(bx + side * w * 0.065, y + h * 0.77,
               bx + side * w * 0.21, y + h * 0.855)
        c.line(bx + side * w * 0.10, y + h * 0.86,
               bx + side * w * 0.045, y + h * 0.97)
    _fill(c, t)
    c.setLineWidth(1.0)
    for side in (-1, 1):
        c.ellipse(cx + side * w * 0.25 - w * 0.095, y + h * 0.41,
                  cx + side * w * 0.25 + w * 0.095, y + h * 0.545,
                  stroke=1, fill=1)
    _teardrop(c, cx, top, bot, w * 0.20, w * 0.105)
    c.setFillColor(t.alt)
    _teardrop(c, cx, y + h * 0.83, y + h * 0.62, w * 0.055, w * 0.030,
              fill=1, stroke=0)
    c.setFillColor(t.deep)
    for side in (-1, 1):
        c.circle(cx + side * w * 0.075, y + h * 0.475, w * 0.022, stroke=0, fill=1)
        c.circle(cx + side * w * 0.030, y + h * 0.115, w * 0.013, stroke=0, fill=1)


def stitched_mask(c, x, y, w, h, t):
    """Psychological horror, identity, masks, hidden faces."""
    _prep(c)
    cx, cy = x + w / 2, y + h * 0.55
    fw, fh = w * 0.58, h * 0.56
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.6)
    for dy in (fh * 0.28, -fh * 0.16):
        c.line(cx - fw * 0.95, cy + dy, cx - fw * 0.52, cy + dy)
        c.line(cx + fw * 0.52, cy + dy, cx + fw * 0.95, cy + dy)
    _fill(c, t)
    c.setLineWidth(1.1)
    c.roundRect(cx - fw / 2, cy - fh / 2, fw, fh, fw * 0.44, stroke=1, fill=1)
    c.setFillColor(t.alt)
    c.roundRect(cx + fw * 0.05, cy + fh * 0.10, fw * 0.34, fh * 0.30,
                fw * 0.09, stroke=0, fill=1)
    c.setFillColor(t.deep)
    c.circle(cx - fw * 0.17, cy + fh * 0.26, fw * 0.055, stroke=0, fill=1)
    c.circle(cx + fw * 0.22, cy + fh * 0.25, fw * 0.055, stroke=0, fill=1)
    c.setStrokeColor(t.deep)
    c.setLineWidth(1.2)
    c.line(cx - fw * 0.25, cy - fh * 0.16, cx + fw * 0.25, cy - fh * 0.16)
    for i in range(7):
        sx = cx - fw * 0.25 + i * (fw * 0.50 / 6)
        c.line(sx, cy - fh * 0.10, sx, cy - fh * 0.22)


def monitor(c, x, y, w, h, t):
    """Software, media, screens, surveillance, anything watched."""
    _prep(c)
    cx = x + w / 2
    sw, sh = w * 0.86, h * 0.52
    sy = y + h * 0.34
    _fill(c, t)
    c.setLineWidth(1.2)
    c.roundRect(cx - sw / 2, sy, sw, sh, w * 0.035, stroke=1, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.4)
    for i, frac in enumerate((0.74, 0.56, 0.38)):
        c.line(cx - sw * 0.36, sy + sh * frac,
               cx - sw * 0.36 + sw * (0.60 - i * 0.13), sy + sh * frac)
    c.setFillColor(t.alt)
    c.rect(cx - sw * 0.36, sy + sh * 0.16, sw * 0.30, sh * 0.10, stroke=0, fill=1)
    _fill(c, t)
    c.setLineWidth(1.2)
    _poly(c, [(cx - w * 0.10, y + h * 0.14), (cx + w * 0.10, y + h * 0.14),
              (cx + w * 0.06, sy), (cx - w * 0.06, sy)])
    c.roundRect(cx - w * 0.22, y + h * 0.09, w * 0.44, h * 0.05,
                h * 0.02, stroke=1, fill=1)


def key(c, x, y, w, h, t):
    """Secrets, access, unlocks, investigations, keys to a mystery."""
    _prep(c)
    cx = x + w / 2
    by = y + h * 0.76
    r = w * 0.24
    _fill(c, t)
    c.setLineWidth(2.6)
    c.circle(cx, by, r, stroke=1, fill=0)
    c.setLineWidth(1.4)
    c.setFillColor(t.alt)
    c.circle(cx, by, r * 0.34, stroke=0, fill=1)
    c.setStrokeColor(t.motif_fill)
    c.setLineWidth(3.6)
    c.line(cx, by - r, cx, y + h * 0.14)
    c.line(cx, y + h * 0.16, cx + w * 0.17, y + h * 0.16)
    c.line(cx, y + h * 0.28, cx + w * 0.12, y + h * 0.28)
    c.line(cx + w * 0.17, y + h * 0.16, cx + w * 0.17, y + h * 0.075)


def flask(c, x, y, w, h, t):
    """Science, medicine, chemistry, experiments, anything measured."""
    _prep(c)
    cx = x + w / 2
    neck_top, body_top, bot = y + h * 0.88, y + h * 0.52, y + h * 0.10
    hw = w * 0.36
    _fill(c, t)
    c.setLineWidth(1.4)
    _poly(c, [(cx - w * 0.09, neck_top), (cx + w * 0.09, neck_top),
              (cx + w * 0.09, body_top), (cx + hw, bot),
              (cx - hw, bot), (cx - w * 0.09, body_top)])
    c.setFillColor(t.alt)
    lz = bot + (body_top - bot) * 0.42
    frac = (lz - bot) / (body_top - bot)
    lw_ = hw - (hw - w * 0.09) * frac
    _poly(c, [(cx - lw_, lz), (cx + lw_, lz), (cx + hw, bot), (cx - hw, bot)],
          fill=1, stroke=0)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.4)
    c.line(cx - w * 0.13, neck_top, cx + w * 0.13, neck_top)
    c.setFillColor(t.motif_fill)
    for dx, dy, rr in ((-0.10, 0.60, 0.028), (0.07, 0.68, 0.022), (0.01, 0.78, 0.017)):
        c.circle(cx + w * dx, bot + (body_top - bot) * dy + h * 0.02,
                 w * rr, stroke=0, fill=1)


def book(c, x, y, w, h, t):
    """History, archives, lore, literature, long-form research."""
    _prep(c)
    cx, cy = x + w / 2, y + h * 0.50
    hw, hh = w * 0.44, h * 0.26
    _fill(c, t)
    c.setLineWidth(1.3)
    for side in (-1, 1):
        p = c.beginPath()
        p.moveTo(cx, cy + hh * 0.86)
        p.curveTo(cx + side * hw * 0.45, cy + hh, cx + side * hw * 0.8, cy + hh,
                  cx + side * hw, cy + hh * 0.80)
        p.lineTo(cx + side * hw, cy - hh * 0.86)
        p.curveTo(cx + side * hw * 0.8, cy - hh, cx + side * hw * 0.45, cy - hh,
                  cx, cy - hh * 0.94)
        p.close()
        c.drawPath(p, stroke=1, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(0.9)
    for side in (-1, 1):
        for i in range(4):
            yy = cy + hh * (0.48 - i * 0.30)
            c.line(cx + side * hw * 0.16, yy, cx + side * hw * 0.84, yy)
    c.setStrokeColor(t.alt)
    c.setLineWidth(3.0)
    c.line(cx, cy + hh * 0.90, cx, cy - hh * 1.30)


def camera(c, x, y, w, h, t):
    """Film, video, photography, documentaries, anything recorded."""
    _prep(c)
    cx, cy = x + w / 2, y + h * 0.50
    bw, bh = w * 0.88, h * 0.40
    _fill(c, t)
    c.setLineWidth(1.2)
    c.roundRect(cx - bw * 0.20, cy + bh * 0.50, bw * 0.34, bh * 0.16,
                w * 0.02, stroke=1, fill=1)
    c.roundRect(cx - bw / 2, cy - bh / 2, bw, bh, w * 0.05, stroke=1, fill=1)
    c.setLineWidth(2.0)
    c.circle(cx, cy, bh * 0.34, stroke=1, fill=0)
    c.setFillColor(t.alt)
    c.circle(cx, cy, bh * 0.19, stroke=0, fill=1)
    c.setFillColor(t.motif_fill)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.0)
    c.circle(cx + bw * 0.34, cy + bh * 0.22, w * 0.033, stroke=1, fill=1)
    c.rect(cx - bw * 0.42, cy + bh * 0.18, bw * 0.14, bh * 0.10, stroke=1, fill=1)


def compass(c, x, y, w, h, t):
    """Exploration, navigation, strategy, direction, orientation guides."""
    _prep(c)
    cx, cy = x + w / 2, y + h * 0.55
    r = min(w * 0.44, h * 0.30)
    _fill(c, t)
    c.setLineWidth(2.0)
    c.circle(cx, cy, r, stroke=1, fill=0)
    c.setLineWidth(1.0)
    c.circle(cx, cy, r * 0.84, stroke=1, fill=1)
    c.setStrokeColor(t.motif_stroke)
    for i in range(8):
        a = math.radians(i * 45)
        c.line(cx + math.sin(a) * r * 0.68, cy + math.cos(a) * r * 0.68,
               cx + math.sin(a) * r * 0.78, cy + math.cos(a) * r * 0.78)
    c.setFillColor(t.alt)
    _poly(c, [(cx, cy + r * 0.62), (cx + r * 0.20, cy), (cx - r * 0.20, cy)],
          fill=1, stroke=0)
    c.setFillColor(t.deep)
    _poly(c, [(cx, cy - r * 0.62), (cx + r * 0.20, cy), (cx - r * 0.20, cy)],
          fill=1, stroke=0)
    c.circle(cx, cy, r * 0.07, stroke=0, fill=1)


def cog(c, x, y, w, h, t):
    """Industry, engineering, process, systems, how a thing is built."""
    _prep(c)
    cx, cy = x + w / 2, y + h * 0.55
    r = min(w * 0.38, h * 0.26)
    _fill(c, t)
    c.setLineWidth(1.2)
    n = 9
    for i in range(n):
        a = math.radians(i * 360.0 / n)
        c.saveState()
        c.translate(cx + math.sin(a) * r * 1.10, cy + math.cos(a) * r * 1.10)
        c.rotate(-i * 360.0 / n)
        c.roundRect(-r * 0.17, -r * 0.20, r * 0.34, r * 0.40, r * 0.06,
                    stroke=1, fill=1)
        c.restoreState()
    c.circle(cx, cy, r, stroke=1, fill=1)
    c.setFillColor(t.alt)
    c.circle(cx, cy, r * 0.34, stroke=0, fill=1)


def skyline(c, x, y, w, h, t):
    """Cities, companies, institutions, real estate, urban subjects."""
    _prep(c)
    base = y + h * 0.16
    _fill(c, t)
    c.setLineWidth(1.1)
    towers = ((0.06, 0.30, 0.44), (0.38, 0.26, 0.62), (0.66, 0.28, 0.38))
    for tx, tw, th in towers:
        c.rect(x + w * tx, base, w * tw, h * th, stroke=1, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(0.8)
    for tx, tw, th in towers:
        cols, rows = 3, max(2, int(th * 9))
        for r_ in range(rows):
            for cidx in range(cols):
                wx = x + w * (tx + tw * (0.20 + cidx * 0.30))
                wy = base + h * th * (0.82 - r_ * (0.72 / max(1, rows - 1)))
                c.rect(wx, wy, w * 0.045, h * 0.024, stroke=1, fill=0)
    c.setFillColor(t.alt)
    c.rect(x + w * (0.38 + 0.26 * 0.20), base + h * 0.62 * 0.82,
           w * 0.045, h * 0.024, stroke=0, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.6)
    c.line(x, base, x + w, base)


def envelope(c, x, y, w, h, t):
    """Correspondence, leaks, communications, letters, anything sent."""
    _prep(c)
    cx, cy = x + w / 2, y + h * 0.52
    ew, eh = w * 0.86, h * 0.40
    _fill(c, t)
    c.setLineWidth(1.3)
    c.rect(cx - ew / 2, cy - eh / 2, ew, eh, stroke=1, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.3)
    c.line(cx - ew / 2, cy + eh / 2, cx, cy - eh * 0.10)
    c.line(cx + ew / 2, cy + eh / 2, cx, cy - eh * 0.10)
    c.line(cx - ew / 2, cy - eh / 2, cx - ew * 0.16, cy + eh * 0.04)
    c.line(cx + ew / 2, cy - eh / 2, cx + ew * 0.16, cy + eh * 0.04)
    c.setFillColor(t.alt)
    c.circle(cx, cy - eh * 0.10, w * 0.055, stroke=0, fill=1)


def shield(c, x, y, w, h, t):
    """Security, defence, law, protection, risk and safety briefs."""
    _prep(c)
    cx = x + w / 2
    top, bot = y + h * 0.84, y + h * 0.12
    hw = w * 0.34
    _fill(c, t)
    c.setLineWidth(1.4)
    p = c.beginPath()
    p.moveTo(cx - hw, top)
    p.lineTo(cx + hw, top)
    p.lineTo(cx + hw, top - (top - bot) * 0.42)
    p.curveTo(cx + hw, bot + (top - bot) * 0.22, cx + hw * 0.55, bot + (top - bot) * 0.10,
              cx, bot)
    p.curveTo(cx - hw * 0.55, bot + (top - bot) * 0.10, cx - hw, bot + (top - bot) * 0.22,
              cx - hw, top - (top - bot) * 0.42)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    c.setStrokeColor(t.alt)
    c.setLineWidth(3.4)
    c.line(cx - hw * 0.52, top - (top - bot) * 0.34, cx, top - (top - bot) * 0.58)
    c.line(cx, top - (top - bot) * 0.58, cx + hw * 0.52, top - (top - bot) * 0.34)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.0)
    c.line(cx - hw, top - (top - bot) * 0.14, cx + hw, top - (top - bot) * 0.14)


def waveform(c, x, y, w, h, t):
    """Music, audio, podcasts, voice, sound design."""
    _prep(c)
    cy = y + h * 0.55
    heights = [0.20, 0.42, 0.66, 0.34, 0.86, 1.00, 0.74, 0.44, 0.62, 0.28, 0.16]
    n = len(heights)
    gap = w / (n + 1.0)
    for i, hv in enumerate(heights):
        bx = x + gap * (i + 1.0)
        bh = h * 0.30 * hv
        c.setFillColor(t.alt if i == 5 else t.motif_fill)
        c.roundRect(bx - gap * 0.30, cy - bh, gap * 0.60, bh * 2,
                    gap * 0.30, stroke=0, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.0)
    c.line(x + gap * 0.4, cy, x + w - gap * 0.4, cy)


def leaf(c, x, y, w, h, t):
    """Nature, agriculture, climate, sustainability, growth stories."""
    _prep(c)
    cx = x + w / 2
    top, bot = y + h * 0.88, y + h * 0.24
    _fill(c, t)
    c.setLineWidth(1.3)
    p = c.beginPath()
    p.moveTo(cx, top)
    p.curveTo(cx + w * 0.42, top - (top - bot) * 0.30,
              cx + w * 0.34, bot + (top - bot) * 0.18, cx, bot)
    p.curveTo(cx - w * 0.34, bot + (top - bot) * 0.18,
              cx - w * 0.42, top - (top - bot) * 0.30, cx, top)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.1)
    c.line(cx, top, cx, bot)
    for i in range(4):
        f = 0.20 + i * 0.18
        yy = bot + (top - bot) * f
        sp = w * (0.26 - i * 0.045)
        c.line(cx, yy, cx - sp, yy + (top - bot) * 0.10)
        c.line(cx, yy, cx + sp, yy + (top - bot) * 0.10)
    c.setStrokeColor(t.alt)
    c.setLineWidth(3.2)
    c.line(cx, bot, cx, y + h * 0.08)


def chart_bars(c, x, y, w, h, t):
    """Markets, metrics, performance, analytics, anything measured over time."""
    _prep(c)
    base, left = y + h * 0.18, x + w * 0.12
    heights = (0.22, 0.38, 0.30, 0.54, 0.70)
    bw = w * 0.13
    for i, hv in enumerate(heights):
        c.setFillColor(t.alt if i == len(heights) - 1 else t.motif_fill)
        c.rect(left + i * (bw * 1.42), base, bw, h * hv, stroke=0, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.6)
    c.line(left - w * 0.05, base, x + w * 0.95, base)
    c.line(left - w * 0.05, base, left - w * 0.05, y + h * 0.92)
    c.setLineWidth(1.4)
    pts = [(left + i * (bw * 1.42) + bw / 2, base + h * hv + h * 0.05)
           for i, hv in enumerate(heights)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1])
    c.setFillColor(t.motif_fill)
    for px, py in pts:
        c.circle(px, py, w * 0.018, stroke=0, fill=1)


def globe(c, x, y, w, h, t):
    """Geopolitics, international subjects, travel, global markets."""
    _prep(c)
    cx, cy = x + w / 2, y + h * 0.55
    r = min(w * 0.42, h * 0.29)
    _fill(c, t)
    c.setLineWidth(1.6)
    c.circle(cx, cy, r, stroke=1, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.0)
    for f in (0.0, 0.45, -0.45, 0.78, -0.78):
        yy = cy + r * f
        half = r * math.sqrt(max(0.0, 1 - f * f))
        c.line(cx - half, yy, cx + half, yy)
    for f in (0.40, 0.80):
        c.ellipse(cx - r * f, cy - r, cx + r * f, cy + r, stroke=1, fill=0)
    c.line(cx, cy - r, cx, cy + r)
    c.setFillColor(t.alt)
    c.circle(cx + r * 0.34, cy + r * 0.40, w * 0.035, stroke=0, fill=1)


def microphone(c, x, y, w, h, t):
    """Interviews, oral history, broadcasting, testimony."""
    _prep(c)
    cx = x + w / 2
    cap_w, cap_h = w * 0.30, h * 0.38
    cap_y = y + h * 0.50
    _fill(c, t)
    c.setLineWidth(1.2)
    c.roundRect(cx - cap_w / 2, cap_y, cap_w, cap_h, cap_w / 2, stroke=1, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(0.9)
    for i in range(5):
        yy = cap_y + cap_h * (0.20 + i * 0.15)
        c.line(cx - cap_w * 0.34, yy, cx + cap_w * 0.34, yy)
    c.setStrokeColor(t.motif_fill)
    c.setLineWidth(2.2)
    p = c.beginPath()
    p.moveTo(cx - cap_w * 0.86, cap_y + cap_h * 0.30)
    p.curveTo(cx - cap_w * 0.86, cap_y - cap_h * 0.28,
              cx + cap_w * 0.86, cap_y - cap_h * 0.28,
              cx + cap_w * 0.86, cap_y + cap_h * 0.30)
    c.drawPath(p, stroke=1, fill=0)
    c.line(cx, cap_y - cap_h * 0.22, cx, y + h * 0.16)
    c.setFillColor(t.alt)
    c.roundRect(cx - w * 0.16, y + h * 0.11, w * 0.32, h * 0.05,
                h * 0.02, stroke=0, fill=1)


def doorway(c, x, y, w, h, t):
    """Thresholds, transitions, horror interiors, "what is inside" stories."""
    _prep(c)
    cx = x + w / 2
    dw, dh = w * 0.52, h * 0.66
    base = y + h * 0.14
    _fill(c, t)
    c.setLineWidth(1.3)
    c.roundRect(cx - dw / 2 - w * 0.07, base, dw + w * 0.14, dh + h * 0.055,
                dw * 0.34, stroke=1, fill=1)
    # the opening, and the light coming out of it - the door stands ajar
    c.setFillColor(t.deep)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.0)
    c.roundRect(cx - dw / 2, base, dw, dh, dw * 0.28, stroke=1, fill=1)
    c.setFillColor(t.alt)
    _poly(c, [(cx - dw * 0.16, base), (cx + dw * 0.06, base),
              (cx + dw * 0.02, base + dh * 0.86), (cx - dw * 0.10, base + dh * 0.86)],
          fill=1, stroke=0)
    c.setFillColor(t.motif_fill)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.0)
    c.roundRect(cx + dw * 0.06, base, dw * 0.44, dh * 0.94, dw * 0.10,
                stroke=1, fill=1)
    c.setFillColor(t.deep)
    c.circle(cx + dw * 0.16, base + dh * 0.46, w * 0.022, stroke=0, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.6)
    c.line(x + w * 0.04, base, x + w * 0.96, base)


def crown(c, x, y, w, h, t):
    """Power, monarchy, market leaders, championships, "the best of" briefs."""
    _prep(c)
    cx = x + w / 2
    base, top = y + h * 0.34, y + h * 0.78
    hw = w * 0.40
    _fill(c, t)
    c.setLineWidth(1.3)
    _poly(c, [(cx - hw, base), (cx - hw, top - h * 0.10),
              (cx - hw * 0.5, base + h * 0.14), (cx, top),
              (cx + hw * 0.5, base + h * 0.14), (cx + hw, top - h * 0.10),
              (cx + hw, base)])
    c.roundRect(cx - hw, y + h * 0.22, hw * 2, h * 0.12, w * 0.02,
                stroke=1, fill=1)
    c.setFillColor(t.alt)
    c.circle(cx, top + h * 0.025, w * 0.035, stroke=0, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.0)
    for dx in (-0.55, 0.0, 0.55):
        c.circle(cx + hw * dx, y + h * 0.28, w * 0.028, stroke=1, fill=0)


def eye(c, x, y, w, h, t):
    """Observation, conspiracy, oversight, obsession, being watched."""
    _prep(c)
    cx, cy = x + w / 2, y + h * 0.55
    hw, hh = w * 0.46, h * 0.19
    _fill(c, t)
    c.setLineWidth(1.4)
    p = c.beginPath()
    p.moveTo(cx - hw, cy)
    p.curveTo(cx - hw * 0.45, cy + hh * 1.5, cx + hw * 0.45, cy + hh * 1.5, cx + hw, cy)
    p.curveTo(cx + hw * 0.45, cy - hh * 1.5, cx - hw * 0.45, cy - hh * 1.5, cx - hw, cy)
    p.close()
    c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(t.alt)
    c.circle(cx, cy, hh * 0.82, stroke=0, fill=1)
    c.setFillColor(t.deep)
    c.circle(cx, cy, hh * 0.36, stroke=0, fill=1)
    c.setStrokeColor(t.motif_stroke)
    c.setLineWidth(1.4)
    for f in (-0.72, -0.36, 0.0, 0.36, 0.72):
        sx = cx + hw * f
        sy = cy + hh * (1.35 - abs(f) * 0.85)
        c.line(sx, sy, sx + hw * f * 0.14, sy + hh * 0.55)


MOTIFS = {
    "stopwatch": stopwatch,
    "antlered_head": antlered_head,
    "stitched_mask": stitched_mask,
    "monitor": monitor,
    "key": key,
    "flask": flask,
    "book": book,
    "camera": camera,
    "compass": compass,
    "cog": cog,
    "skyline": skyline,
    "envelope": envelope,
    "shield": shield,
    "waveform": waveform,
    "leaf": leaf,
    "chart_bars": chart_bars,
    "globe": globe,
    "microphone": microphone,
    "doorway": doorway,
    "crown": crown,
    "eye": eye,
}


def get(name: str):
    """Look up a motif by name, with a helpful error listing what exists."""
    if name not in MOTIFS:
        raise KeyError(f"no motif {name!r}; have {', '.join(sorted(MOTIFS))}")
    return MOTIFS[name]
