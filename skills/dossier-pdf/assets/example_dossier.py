"""example_dossier.py - a complete, runnable dossier using every component.

Read this to see how the pieces fit together in a real document; run it to get
a PDF you can look at.

    python assets/example_dossier.py

The subject here is invented. What matters is the shape: a cover whose colours
and motif come from the subject, a contents table that lists purposes rather
than page numbers, sections that each open with kicker / H1 / rule / lead, and
a closing sources table.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "scripts"))

import motifs                          # noqa: E402
from dossier import Dossier, Theme     # noqa: E402

# The subject is a lighthouse-keeping service: night, sea, and a warm lamp.
theme = Theme.from_seeds(deep="#12202B", accent="#3E86A0", alt="#D08A2C")

doc = Dossier(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "example_dossier.pdf"),
    theme=theme,
    motif=motifs.get("compass"),
    cover=dict(
        kicker="Two hundred years of keeping the light",
        title="The Last Keepers",
        subtitle="A research dossier for a twenty minute documentary",
        blurb=["Nineteen stations, four generations, one automation order.",
               "Everything worth saying about the keepers, in one place."],
        meta=["Northern Lights Board", "1824 to 1998", "Compiled from 31 sources"],
    ),
    header_left="The Last Keepers / research dossier",
    header_right="Northern Lights Board / 1824-1998",
    footer_left="Prepared as source material for a twenty minute documentary.",
)

# --------------------------------------------------------------- front matter
doc.section(
    "Front matter", "How to use this dossier",
    lead="Six sections. The first two give you the service and the people. The "
         "middle two give you the work itself and the night it went wrong. The "
         "last two give you ammunition: a fact bank and every source.")
doc.contents([
    ("01", "The Service", "Who ran the lights, and on whose money."),
    ("02", "The Keepers", "Four families, and what the job did to them."),
    ("03", "A Working Night", "The watch, hour by hour."),
    ("04", "The Braemar Wreck", "The night the light failed, and why."),
    ("05", "Quick Fire Facts", "Standalone one-liners. Drop them anywhere."),
    ("06", "Method And Sources", "What is confirmed, what is my reading."),
])
doc.box(
    ["Two keepers died in service and both are named in section 04. Their "
     "descendants are living people.",
     "Nothing here is graphic, but the framing is what needs care."],
    title="Sensitive material", kind="warn")
doc.page_break()

# --------------------------------------------------------------- section 01
doc.section(
    "Part 1", "The Service",
    lead="The Board was a private trust with a public duty, which is the whole "
         "reason the automation fight took eleven years.")
doc.h2("Founding and funding")
doc.p("Established by statute in 1824 and funded by light dues levied on "
      "tonnage passing the northern approaches. The dues were never popular "
      "and the Board never once raised them without a court case.")
doc.bullets([
    "Nineteen stations at the peak, 1911.",
    "Three keepers per rock station, two per shore station.",
    "Relief by boat every fourteen days, weather permitting &#8212; and it "
    "frequently did not permit.",
])
doc.h3("What the money actually bought")
doc.table([
    ("Line", "Share of budget", "Notes"),
    ("Wages", "41%", "Keepers, boatmen, and the two engineers."),
    ("Oil and later acetylene", "23%", "Halved after the 1932 conversion."),
    ("Boats and relief", "19%", "The line the Board most wanted to cut."),
    ("Buildings", "17%", "Almost entirely the four rock towers."),
], widths=[26, 20, 54])
doc.say("Say it as: the service was a charity with a navy's problems.")
doc.page_break()

# --------------------------------------------------------------- section 02
doc.section(
    "Part 2", "The Keepers",
    lead="Four families supplied most of the roll for a century. That is the "
         "human spine of the film.")
doc.profile(
    "Margaret Nairn", "principal keeper, Sgeir Mor 1948-1971",
    points=[
        "First woman appointed principal keeper in the service, and the Board "
        "spent two years pretending the appointment was temporary.",
        "Kept the only complete weather log of the 1953 surge.",
    ],
    takeaway="Her log is the best single primary source in the whole dossier.")
doc.profile(
    "Thomas Nairn", "assistant keeper, her son",
    points=[
        "Left the service in 1969 and gave the only long interview about "
        "relief-boat conditions.",
    ])
doc.box("\"You do not get lonely. You get very, very used to your own "
        "opinions.\" &#8212; Thomas Nairn, 1988",
        kind="quote")
doc.page_break()

# --------------------------------------------------------------- section 05
doc.section(
    "Part 5", "Quick Fire Facts",
    lead="Standalone one-liners. None of them needs setup, so drop them "
         "wherever the edit sags.")
doc.fact_bank([
    "The lamp burned 1.4 litres of paraffin an hour.",
    "A rock relief was cancelled 31 times in the winter of 1962.",
    "The service issued keepers a cat allowance until 1957.",
    "The last manned watch ended at 06:00 on 31 March 1998.",
])
doc.spacer()
doc.box("Claims marked <b>[theory]</b> are my reading of the evidence, not "
        "something a source states outright. Claims marked <b>[estimate]</b> "
        "are numbers I derived rather than found.",
        title="Confidence flags")
doc.page_break()

# --------------------------------------------------------------- sources
doc.section(
    "Part 6", "Method And Sources",
    lead="Everything above came from these. Multiple pages from one site are "
         "grouped into a single row.")
doc.sources([
    ("Board minute books, 1824-1998", "national archive"),
    ("Nairn weather logs (digitised)", "maritime museum"),
    ("Thomas Nairn interview, 1988", "oral history project"),
])
doc.small("Compiled for demonstration. The subject of this example is invented.")

if __name__ == "__main__":
    doc.build()
