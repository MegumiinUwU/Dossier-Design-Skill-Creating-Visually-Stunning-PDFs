"""dossier.py - builder library for the Dossier PDF style.

A dark themed cover with one geometric motif, then dense editorial body pages.
Built on ReportLab Platypus. Uses the built-in Helvetica family by default, so
no font files are required.

    import sys; sys.path.insert(0, "<skill>/scripts")
    from dossier import Dossier, Theme
    import motifs

    doc = Dossier("out.pdf",
                  theme=Theme.from_seeds("#1B1A30", "#3B7EA1", "#C98A2E"),
                  motif=motifs.stopwatch,
                  cover=dict(kicker="...", title="...", subtitle="..."),
                  header_left="SUBJECT / DOCUMENT TYPE")
    doc.section("Part 1", "Heading", lead="One paragraph.")
    doc.p("Body text.")
    doc.build()

See references/api.md for the full API and references/style-spec.md for the
visual rules this file implements.
"""

from __future__ import annotations

import colorsys
from dataclasses import dataclass, replace

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, LETTER  # noqa: F401  (LETTER re-exported)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import HRFlowable

__all__ = ["Dossier", "Theme", "PRESETS", "tint", "scale", "mix", "use_font_family"]


# --------------------------------------------------------------------------
# colour helpers
# --------------------------------------------------------------------------

def _hex2rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def _rgb2hex(rgb) -> str:
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(c * 255))) for c in rgb)


def tint(seed: str, l=None, s=None, s_mul=None) -> str:
    """Recolour `seed` keeping its hue. `l`/`s` are absolute 0-1, `s_mul` scales."""
    H, L, S = colorsys.rgb_to_hls(*_hex2rgb(seed))
    if s_mul is not None:
        S = min(1.0, S * s_mul)
    if s is not None:
        S = s
    if l is not None:
        L = l
    return _rgb2hex(colorsys.hls_to_rgb(H, L, S))


def scale(seed: str, k: float) -> str:
    """Multiply each RGB channel. Good for lifting very dark colours."""
    return _rgb2hex(tuple(min(1.0, c * k) for c in _hex2rgb(seed)))


def mix(a: str, b: str, t: float) -> str:
    """Linear blend: t=0 gives `a`, t=1 gives `b`."""
    ra, rb = _hex2rgb(a), _hex2rgb(b)
    return _rgb2hex(tuple(ra[i] + (rb[i] - ra[i]) * t for i in range(3)))


def _c(h: str):
    return colors.HexColor(h)


# --------------------------------------------------------------------------
# theme
# --------------------------------------------------------------------------

@dataclass
class Theme:
    """Every colour the style uses.

    Build one with `Theme.from_seeds(deep, accent, alt)` and only override what
    you actually want to hand-pick. The derived neutrals are deliberately
    tinted toward `deep`'s hue - that is what makes a plum dossier read plum
    all the way down to its hairlines.
    """

    deep: str        # cover background, H1s, table header fill
    accent: str      # cool accent: H2s, rules, page numbers
    alt: str         # warm accent: kickers, box left bars
    band: str        # lighter tint of deep, cover top band
    say: str         # third accent, italic pull / suggested lines only
    ink: str         # near black, lead paragraphs
    body: str        # all body text
    grey: str        # captions, running header and footer
    rule: str        # hairlines, table borders
    boxbg: str       # neutral callout fill
    quotebg: str     # quote / info callout fill
    warnbg: str      # caution / sensitive callout fill
    cover_title: str      # cover title colour
    cover_sub: str        # cover subtitle colour
    cover_blurb: str      # cover blurb and meta colour
    motif_fill: str       # motif body colour
    motif_stroke: str     # motif outline colour

    @classmethod
    def from_seeds(cls, deep: str, accent: str, alt: str, **overrides) -> "Theme":
        """Derive a full palette from three subject colours.

        deep   very dark, the subject's "night" colour
        accent mid-tone cool colour, used structurally
        alt    warmer or brighter colour, used as the single spot of heat
        """
        deep_l = colorsys.rgb_to_hls(*_hex2rgb(deep))[1]
        _, _, as_ = colorsys.rgb_to_hls(*_hex2rgb(accent))
        _, _, ls = colorsys.rgb_to_hls(*_hex2rgb(alt))
        t = cls(
            deep=deep,
            accent=accent,
            alt=alt,
            band=scale(deep, 1.38),
            say=tint(accent, l=0.36),
            ink=tint(deep, l=max(0.05, deep_l * 0.72)),
            body=tint(deep, l=0.16, s_mul=0.55),
            grey=tint(deep, l=0.44, s_mul=0.25),
            rule=tint(deep, l=0.851, s_mul=0.55),
            boxbg=tint(deep, l=0.969, s_mul=1.40),
            quotebg=tint(accent, l=0.955, s=min(1.0, as_ * 0.65)),
            warnbg=tint(alt, l=0.963, s=min(1.0, ls * 1.15)),
            cover_title="#FFFFFF",
            cover_sub=tint(deep, l=0.81, s_mul=0.75),
            cover_blurb=tint(deep, l=0.62, s_mul=0.55),
            motif_fill=tint(deep, l=0.955, s_mul=1.15),
            motif_stroke=tint(deep, l=0.72, s_mul=0.50),
        )
        return replace(t, **overrides) if overrides else t

    @classmethod
    def preset(cls, name: str, **overrides) -> "Theme":
        """One of the shipped palettes in PRESETS."""
        if name not in PRESETS:
            raise KeyError(f"unknown preset {name!r}; have {sorted(PRESETS)}")
        seeds = PRESETS[name]
        return cls.from_seeds(seeds["deep"], seeds["accent"], seeds["alt"],
                              **{**{k: v for k, v in seeds.items()
                                    if k not in ("deep", "accent", "alt", "note")},
                                 **overrides})


# Palettes lifted from real dossiers plus a few general purpose starts.
# `note` records the subject the palette was cut from.
PRESETS = {
    "midnight-ink": {  # blue / rose, the baseline
        "deep": "#1E1B2E", "accent": "#2E7DB8", "alt": "#C4577F", "say": "#2E8B87",
        "note": "psychological horror game, cool default",
    },
    "clockwork-amber": {  # indigo / steel blue / amber
        "deep": "#1B1A30", "accent": "#3B7EA1", "alt": "#C98A2E",
        "note": "clockpunk platformer, warm metal",
    },
    "folk-crimson": {  # plum / moss / crimson
        "deep": "#2A1B28", "accent": "#3E6B52", "alt": "#B0304A", "say": "#9C6B22",
        "motif_fill": "#F2ECE4", "motif_stroke": "#A9989F",
        "note": "embroidered folk horror, warm cream motif",
    },
    "boardroom-slate": {
        "deep": "#151A22", "accent": "#3E7CA6", "alt": "#C46B3A",
        "note": "business / market research",
    },
    "lab-teal": {
        "deep": "#101F24", "accent": "#2A8C8A", "alt": "#D0604A",
        "note": "science, medicine, technical briefs",
    },
    "archive-sepia": {
        "deep": "#241C16", "accent": "#7A6A4F", "alt": "#B24A2E",
        "note": "history, archives, long form journalism",
    },
    "signal-violet": {
        "deep": "#1A1526", "accent": "#6A5ACD", "alt": "#D98324",
        "note": "software, AI, systems",
    },
}


def use_font_family(regular: str, bold: str, italic: str,
                    family: str = "Dossier") -> tuple:
    """Register a TTF family and return (regular, bold, italic) font names.

    Pass the result to Dossier(fonts=...). Only do this when the subject really
    needs it - the built-in Helvetica family needs no files and never fails to
    embed. Any font you register must cover every glyph you use.
    """
    names = (family, family + "-Bold", family + "-Italic")
    for name, path in zip(names, (regular, bold, italic)):
        pdfmetrics.registerFont(TTFont(name, path))
    pdfmetrics.registerFontFamily(family, normal=names[0], bold=names[1],
                                  italic=names[2], boldItalic=names[1])
    return names


# --------------------------------------------------------------------------
# document
# --------------------------------------------------------------------------

class Dossier:
    """Builds one dossier PDF.

    Geometry (A4 default): 20mm left/right margins, 22mm top, 20mm bottom.
    The body frame width is exposed as `self.frame_w` in points; table columns
    are normalised to it automatically.
    """

    def __init__(
        self,
        path: str,
        theme: Theme,
        cover: dict,
        motif=None,
        pagesize=A4,
        header_left: str = "",
        header_right: str = "",
        footer_left: str = "",
        margins=(20 * mm, 20 * mm, 22 * mm, 20 * mm),  # l, r, t, b
        fonts=("Helvetica", "Helvetica-Bold", "Helvetica-Oblique"),
        motif_box=None,          # (w, h) in points; default 62mm x 72mm
        cover_text_top=118 * mm,  # gap above the cover text block
        title="", author="",
    ):
        self.path = path
        self.theme = theme
        self.cover = cover
        self.motif = motif
        self.pagesize = pagesize
        self.header_left = header_left or cover.get("title", "")
        self.header_right = header_right
        self.footer_left = footer_left
        self.fonts = fonts
        self.motif_box = motif_box or (62 * mm, 72 * mm)
        self.cover_text_top = cover_text_top
        self._meta = (title or cover.get("title", ""), author)

        ml, mr, mt, mb = margins
        self.margins = margins
        pw, ph = pagesize
        self.frame_w = pw - ml - mr
        self.story = []

        self.doc = BaseDocTemplate(
            path, pagesize=pagesize,
            leftMargin=ml, rightMargin=mr, topMargin=mt, bottomMargin=mb,
            title=self._meta[0], author=self._meta[1],
        )
        cover_frame = Frame(ml, mb, self.frame_w, ph - mt - mb, id="cover",
                            leftPadding=0, rightPadding=0,
                            topPadding=0, bottomPadding=0)
        body_frame = Frame(ml, mb, self.frame_w, ph - 42 * mm, id="body",
                           leftPadding=0, rightPadding=0,
                           topPadding=0, bottomPadding=0)
        self.doc.addPageTemplates([
            PageTemplate(id="cover", frames=[cover_frame], onPage=self._paint_cover),
            PageTemplate(id="body", frames=[body_frame], onPage=self._paint_body),
        ])

        self.styles = _build_styles(theme, fonts)
        self._lay_cover()

    # -- page painters ----------------------------------------------------

    def _paint_cover(self, c, doc):
        t, (pw, ph) = self.theme, self.pagesize
        c.saveState()
        c.setFillColor(_c(t.deep))
        c.rect(0, 0, pw, ph, stroke=0, fill=1)
        c.setFillColor(_c(t.band))
        c.rect(0, ph * 0.60, pw, ph * 0.40, stroke=0, fill=1)
        if self.motif:
            mw, mh = self.motif_box
            self.motif(c, (pw - mw) / 2.0, ph * 0.765 - mh / 2.0, mw, mh, t)
        c.setStrokeColor(_c(t.accent))
        c.setLineWidth(2)
        c.line(28 * mm, ph * 0.585, pw - 28 * mm, ph * 0.585)
        c.restoreState()

    def _paint_body(self, c, doc):
        t, (pw, ph) = self.theme, self.pagesize
        reg, bold, _ = self.fonts
        ml, mr = self.margins[0], self.margins[1]
        c.saveState()
        c.setStrokeColor(_c(t.rule))
        c.setLineWidth(0.4)
        c.line(ml, ph - 16 * mm, pw - mr, ph - 16 * mm)
        c.line(ml, 14 * mm, pw - mr, 14 * mm)
        c.setFont(reg, 7.2)
        c.setFillColor(_c(t.grey))
        c.drawString(ml, ph - 14 * mm, self.header_left.upper())
        if self.header_right:
            c.drawRightString(pw - mr, ph - 14 * mm, self.header_right.upper())
        if self.footer_left:
            c.drawString(ml, 10.5 * mm, self.footer_left)
        c.setFont(bold, 8)
        c.setFillColor(_c(t.accent))
        c.drawRightString(pw - mr, 10.5 * mm, str(doc.page - 1))
        c.restoreState()

    # -- cover text -------------------------------------------------------

    def _lay_cover(self):
        s, cv = self.styles, self.cover
        self.story.append(Spacer(1, self.cover_text_top))
        if cv.get("kicker"):
            self.story.append(Paragraph(cv["kicker"].upper(), s["cover_kicker"]))
            self.story.append(Spacer(1, 8))
        self.story.append(Paragraph(cv["title"], s["cover_title"]))
        if cv.get("subtitle"):
            self.story.append(Spacer(1, 6))
            self.story.append(Paragraph(cv["subtitle"], s["cover_sub"]))
        if cv.get("blurb"):
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph(_join(cv["blurb"], "<br/>"), s["cover_blurb"]))
        if cv.get("meta"):
            self.story.append(Spacer(1, 9))
            self.story.append(Paragraph(_join(cv["meta"], " &#183; "), s["cover_blurb"]))
        self.story.append(NextPageTemplate("body"))
        self.story.append(PageBreak())

    # -- content ----------------------------------------------------------

    def add(self, flowable):
        """Escape hatch: append any Platypus flowable."""
        self.story.append(flowable)
        return self

    def spacer(self, height=4 * mm):
        return self.add(Spacer(1, height))

    def page_break(self):
        return self.add(PageBreak())

    def section(self, kicker: str, heading: str, lead: str = ""):
        """Kicker, H1, accent rule, then one lead paragraph. Opens every part."""
        s = self.styles
        if kicker:
            self.story.append(Paragraph(kicker.upper(), s["h1k"]))
        self.story.append(Paragraph(heading, s["h1"]))
        self.story.append(HRFlowable(width="100%", thickness=1.6, spaceAfter=8,
                                     color=_c(self.theme.accent)))
        if lead:
            self.story.append(Paragraph(lead, s["lead"]))
        return self

    def h2(self, text):
        return self.add(Paragraph(text, self.styles["h2"]))

    def h3(self, text):
        return self.add(Paragraph(text, self.styles["h3"]))

    def lead(self, text):
        return self.add(Paragraph(text, self.styles["lead"]))

    def p(self, text):
        return self.add(Paragraph(text, self.styles["p"]))

    def small(self, text):
        return self.add(Paragraph(text, self.styles["small"]))

    def say(self, text):
        """Italic accent line: a suggested phrasing or a pull quote."""
        return self.add(Paragraph(text, self.styles["say"]))

    def bullets(self, items, numbered=False):
        s = self.styles["bullet"]
        kw = dict(bulletType="1", leftIndent=15, bulletFontName=self.fonts[1]) if numbered \
            else dict(bulletType="bullet", leftIndent=13, bulletFontSize=8)
        self.story.append(ListFlowable(
            [ListItem(Paragraph(i, s), leftIndent=kw["leftIndent"]) if isinstance(i, str)
             else ListItem(i, leftIndent=kw["leftIndent"]) for i in items],
            spaceBefore=2, spaceAfter=4, **kw))
        return self

    def box(self, body, title: str = "", kind: str = "note"):
        """Callout box. kind: note | quote | warn.

        The 2.6pt warm accent bar on the left edge is the signature detail -
        do not drop it.
        """
        t, s = self.theme, self.styles
        fill = {"note": t.boxbg, "quote": t.quotebg, "warn": t.warnbg}[kind]
        inner = []
        if title:
            inner.append(Paragraph(title, s["boxtitle"]))
        style = s["quote"] if kind == "quote" else s["p"]
        for para in _as_list(body):
            inner.append(para if not isinstance(para, str) else Paragraph(para, style))
        tbl = Table([[inner]], colWidths=[self.frame_w])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), _c(fill)),
            ("BOX", (0, 0), (-1, -1), 0.6, _c(t.rule)),
            ("LINEBEFORE", (0, 0), (0, -1), 2.6, _c(t.alt)),
            ("LEFTPADDING", (0, 0), (-1, -1), 9),
            ("RIGHTPADDING", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        self.story.append(Spacer(1, 4))
        self.story.append(KeepTogether(tbl) if title else tbl)
        self.story.append(Spacer(1, 6))
        return self

    def table(self, rows, widths=None, header=True, bold_first_col=True,
              zebra=True, align=None):
        """Dossier table. `rows[0]` is the header row when header=True.

        `widths` are relative weights (or points); they are normalised to the
        frame width so a table can never overhang the margin. Every cell is
        wrapped in a Paragraph so text wraps instead of overflowing.
        """
        t, s = self.theme, self.styles
        ncols = max(len(r) for r in rows)
        w = list(widths) if widths else [1] * ncols
        if len(w) != ncols:
            raise ValueError(f"widths has {len(w)} entries, rows have {ncols} columns")
        total = float(sum(w))
        col_widths = [self.frame_w * (x / total) for x in w]

        data = []
        for ri, row in enumerate(rows):
            row = list(row) + [""] * (ncols - len(row))
            out = []
            for ci, cell in enumerate(row):
                if not isinstance(cell, str):
                    out.append(cell)
                    continue
                if header and ri == 0:
                    st = s["th"]
                elif bold_first_col and ci == 0:
                    st = s["td_key"]
                else:
                    st = s["td"]
                out.append(Paragraph(cell, st))
            data.append(out)

        cmds = [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
            ("BOX", (0, 0), (-1, -1), 0.6, _c(t.rule)),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, _c(t.rule)),
        ]
        first = 1 if header else 0
        if header:
            cmds.append(("BACKGROUND", (0, 0), (-1, 0), _c(t.deep)))
        if zebra:
            for i in range(first, len(data)):
                if (i - first) % 2 == 1:
                    cmds.append(("BACKGROUND", (0, i), (-1, i), _c(t.boxbg)))
        if align:
            for ci, a in enumerate(align):
                if a:
                    cmds.append(("ALIGN", (ci, 0), (ci, -1), a.upper()))
        tbl = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
        tbl.setStyle(TableStyle(cmds))
        self.story.append(Spacer(1, 4))
        self.story.append(tbl)
        self.story.append(Spacer(1, 7))
        return self

    def profile(self, name: str, role: str = "", points=(), takeaway: str = ""):
        """A repeated entity block - person, character, product, location.

        Kept together so a profile never splits across a page break.
        """
        s = self.styles
        block = []
        head = name if not role else (
            f"{name} <font face='{self.fonts[0]}' size=8.4 "
            f"color='{self.theme.grey}'>&#183; {role}</font>")
        block.append(Paragraph(head, s["h3"]))
        for pt in points:
            block.append(Paragraph("&#8226;&nbsp;&nbsp;" + pt, s["profile_pt"]))
        if takeaway:
            block.append(Paragraph(takeaway, s["say"]))
        self.story.append(KeepTogether(block))
        self.story.append(Spacer(1, 3))
        return self

    def contents(self, rows, headings=("#", "Section", "What it gives you")):
        """The menu-of-purposes table that opens every dossier."""
        return self.table([list(headings)] + [list(r) for r in rows], widths=[6, 28, 66])

    def sources(self, rows, headings=("Source", "Domain")):
        """Closing sources table: name in the bold first column, bare domain second."""
        return self.table([list(headings)] + [list(r) for r in rows], widths=[46, 54])

    def fact_bank(self, facts, numbered=True):
        """The quick-fire one-liner section. 25-35 standalone facts."""
        return self.bullets(list(facts), numbered=numbered)

    # -- output -----------------------------------------------------------

    def build(self, verbose=True):
        self.doc.build(self.story)
        if verbose:
            print(f"wrote {self.path}")
        return self.path


# --------------------------------------------------------------------------
# styles
# --------------------------------------------------------------------------

def _build_styles(t: Theme, fonts) -> dict:
    reg, bold, ital = fonts
    S = {}

    def st(name, **kw):
        S[name] = ParagraphStyle(name, **kw)

    # cover
    st("cover_kicker", fontName=bold, fontSize=10, leading=13,
       textColor=_c(t.alt), alignment=TA_CENTER)
    st("cover_title", fontName=bold, fontSize=40, leading=42,
       textColor=_c(t.cover_title), alignment=TA_CENTER)
    st("cover_sub", fontName=reg, fontSize=13, leading=18,
       textColor=_c(t.cover_sub), alignment=TA_CENTER)
    st("cover_blurb", fontName=reg, fontSize=8.6, leading=12.6,
       textColor=_c(t.cover_blurb), alignment=TA_CENTER)

    # body
    st("h1k", fontName=bold, fontSize=8, leading=10, textColor=_c(t.alt),
       spaceBefore=0, spaceAfter=2)
    st("h1", fontName=bold, fontSize=19, leading=22, textColor=_c(t.deep),
       spaceAfter=4)
    st("h2", fontName=bold, fontSize=12.4, leading=15, textColor=_c(t.accent),
       spaceBefore=11, spaceAfter=3)
    st("h3", fontName=bold, fontSize=10.2, leading=13, textColor=_c(t.deep),
       spaceBefore=7, spaceAfter=2)
    st("lead", fontName=reg, fontSize=11, leading=15.5, textColor=_c(t.ink),
       spaceAfter=7)
    st("p", fontName=reg, fontSize=9.6, leading=13.6, textColor=_c(t.body),
       spaceAfter=5)
    st("bullet", fontName=reg, fontSize=9.5, leading=13.2, textColor=_c(t.body),
       spaceAfter=2.5)
    st("profile_pt", fontName=reg, fontSize=9.5, leading=13.2,
       textColor=_c(t.body), leftIndent=10, spaceAfter=2.5)
    st("say", fontName=ital, fontSize=9.4, leading=13, textColor=_c(t.say),
       leftIndent=10, spaceBefore=2, spaceAfter=6)
    st("quote", fontName=ital, fontSize=9.8, leading=14, textColor=_c(t.deep),
       leftIndent=8, rightIndent=8, spaceAfter=4)
    st("small", fontName=reg, fontSize=8.4, leading=11.6, textColor=_c(t.grey),
       spaceAfter=4)
    st("boxtitle", fontName=bold, fontSize=9.4, leading=12.6, textColor=_c(t.alt),
       spaceAfter=3)
    st("th", fontName=bold, fontSize=8.4, leading=11, textColor=colors.white)
    st("td", fontName=reg, fontSize=8.4, leading=11.4, textColor=_c(t.body))
    st("td_key", fontName=bold, fontSize=8.4, leading=11.4, textColor=_c(t.deep))
    return S


def _as_list(x):
    return x if isinstance(x, (list, tuple)) else [x]


def _join(x, sep):
    return sep.join(x) if isinstance(x, (list, tuple)) else x
