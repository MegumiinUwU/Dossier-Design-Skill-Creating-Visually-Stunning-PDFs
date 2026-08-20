# Content structure

The visual style makes a document look researched. These conventions make it
actually be researched. They are what separates a dossier from a report.

## Contents

- The governing idea
- The standard section order
- The contents table
- Confidence flags
- Profiles
- The quick-fire fact bank
- The sources table
- Sensitive material
- Writing rules
- Adapting the shape to other document types

## The governing idea

A dossier is written so the reader always knows **the next true thing they could
say**. Not "here is what I found" but "here is what you can now assert, and how
sure you can be." That single reframing changes what goes in: fewer summaries,
more concrete facts, explicit confidence, and a source for everything.

Nothing in a dossier is written to be read aloud word for word. It is written to
be raided.

## The standard section order

Twelve to eighteen sections works well for a substantial subject. The order:

1. **Front matter** - how to use this dossier, the contents table, any content
   note.
2. **Origin** - who made / did / caused the thing, and the shape of the story.
3. **The fact sheet** - every hard number in one place: dates, prices, sizes,
   specs, personnel. The section people come back to.
4. **How it actually works** - the mechanics, in the reader's terms.
5. **The middle sections** - the subject's own structure: story, craft, method,
   chronology, whatever the material demands. This is most of the document.
6. **Reception and aftermath** - how it landed, the split verdict, the one
   complaint everyone shares.
7. **Caveats** - what is disputed, what the bad sources say and how to spot
   them.
8. **Quick-fire fact bank** - the penultimate section, always.
9. **Method and sources** - what is confirmed, what is interpretation, and where
   every claim came from.

Each is a `doc.section(kicker, heading, lead=...)` followed by a
`doc.page_break()`.

## The contents table

Up front, mapping section number -> name -> **"what it gives you"**. Not a table
of contents with page numbers: a menu of purposes. The third column is the one
that matters, and it is written from the reader's point of view.

```python
doc.contents([
    ("01", "The Studio That Failed First", "Why this is a comeback story."),
    ("02", "The Fact Sheet", "Every hard number: dates, price, platforms."),
    ("03", "How It Actually Plays", "Movement, gadgets, the economy."),
])
```

Write "What it gives you" entries as promises, not descriptions. "Every hard
number" beats "an overview of the specifications."

## Confidence flags

Mark unverified or interpretive claims inline, in bold, and explain the
convention in a box near the front or in the closing section:

- `<b>[theory]</b>` - your reading of the evidence, not something a source
  states.
- `<b>[estimate]</b>` - a number you derived rather than found.
- `<b>[unconfirmed]</b>` - a claim from a single weak source.

```python
doc.box("Claims marked <b>[theory]</b> are my reading of the evidence, not "
        "something a source states outright.", title="Confidence flags")
```

This is the highest-value convention in the whole format. It costs one bracket
and it is the difference between research and assertion.

## Profiles

For any entity that recurs - people, characters, products, locations, factions -
use the profile block rather than prose. Name, role, two to four bullets,
optional takeaway line:

```python
doc.profile("Margaret Nairn", "principal keeper, 1948-1971",
            points=["First woman appointed principal keeper in the service.",
                    "Kept the only complete log of the 1953 surge."],
            takeaway="Her log is the best primary source in the dossier.")
```

Consistent shape means the reader can scan twenty of them and find the same
thing in the same place each time.

## The quick-fire fact bank

25 to 35 short standalone one-liners as the penultimate section. Each must stand
completely alone - no setup, no dependency on anything above it - so it can be
dropped anywhere.

```python
doc.fact_bank([
    "The lamp burned 1.4 litres of paraffin an hour.",
    "A rock relief was cancelled 31 times in the winter of 1962.",
])
```

Extremely useful, costs nothing, and it is usually the section people quote
back at you.

## The sources table

Last section. Source name in the bold first column, bare domain in the second.
Group many pages from one site into a single row - a table with forty rows from
one wiki is noise.

```python
doc.sources([
    ("Board minute books, 1824-1998", "national archive"),
    ("Developer interviews (4 pieces)", "example.com"),
])
```

Pair it with a short lead paragraph saying what kind of sources these are and
which you trust least. If the subject has a known bad-source problem - content
farms, AI-generated wikis, a widely copied error - give it its own section
earlier and name the tell.

## Sensitive material

If the subject warrants it, put a `warn` box near the front, before the reader
has committed:

```python
doc.box(["Everything past this page assumes you have finished the game. "
         "Section 05 describes the ending in full.",
         "The story is built on grief and a death in the family. Nothing here "
         "is graphic; the framing is what needs care."],
        title="Full spoilers, and a content note", kind="warn")
```

State what is disclosed and what the reader should be careful with, in that
order, without moralising.

## Writing rules

- **Lead paragraphs frame, they do not summarise.** One paragraph, 11pt, saying
  why this section exists.
- **Prefer the concrete.** "Fourteen people, three years" over "a small team
  worked for several years."
- **One claim per bullet.** If a bullet needs a semicolon it is two bullets.
- **Numbers in the fact sheet, not in prose.** Prose that lists five numbers is
  a table that has not been made yet.
- **Say lines are optional.** `doc.say()` is for a phrasing worth stealing, not
  a summary of the paragraph above it.
- **Do not pad to fill a page.** Short sections are fine; the page break after
  each section makes them look intentional.

## Adapting the shape to other document types

The visual style works far beyond research dossiers. The content conventions
that travel with it:

| Document | Keep | Replace |
|---|---|---|
| Technical brief | contents-as-purposes, fact sheet, sources | profiles -> component blocks |
| Field guide | profiles, fact bank | reception -> field notes |
| Post-mortem | confidence flags, sources | fact bank -> timeline |
| Pitch document | contents-as-purposes, fact sheet | sources -> appendix |
| Onboarding pack | contents-as-purposes, profiles | confidence flags -> ownership |

Keep the contents table of purposes and the sources table in almost every case:
they are cheap and they are what make a document feel accountable.
