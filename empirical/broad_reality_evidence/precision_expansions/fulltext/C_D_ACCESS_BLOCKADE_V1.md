# c_D public-access blockade v1

## Scope

This receipt covers the fixed four-study `c_D` full-text reading queue only. No new
query, candidate, trait class, or effect was added.

```text
queue:      B_TO_P_FULLTEXT_READING_QUEUE_v1.csv
route:      B_to_pollination (c_D)
trait:      chemical barrier
outcomes:   pollinator preference/foraging or visitation
purpose:    determine whether a B2-compatible numerical extraction is possible
```

## Reproducible probe receipt

```text
workflow:              Resolve c_D full-text sources
workflow run:          28640941928
run date:              2026-07-03
artifact:              c-d-source-receipts
artifact SHA-256:      6f98fd65f1b72aa6dd79c70d825169691c7b388fa95655de0a5767a2264b9427
providers queried:     Crossref, OpenAlex, Unpaywall, DataCite, Dryad, Zenodo
file handling:         temporary PDF inspection only; no article PDFs/text retained
```

## Outcome by registered study

| Queue | Study | DOI | DOI-exact public/repository result | Readable public PDF result | C4 state |
|---|---|---|---|---|---|
| BPPFT_Q001 | Gelsemium nectar alkaloid | `10.1111/j.1461-0248.2007.01027.x` | No OpenAlex or Unpaywall public location; no exact repository relation | Wiley publisher PDF returned HTTP 403 | access blocked |
| BPPFT_Q002 | Bird nicotine | `10.1111/j.1600-048x.2013.00079.x` | No OpenAlex or Unpaywall public location; no exact repository relation | Wiley publisher PDF returned HTTP 403 | access blocked |
| BPPFT_Q003 | Delphinium alkaloid | `10.1111/1365-2745.12144` | OpenAlex and Unpaywall both point to the same publisher `pdfdirect` URL; no exact repository relation | Wiley `pdfdirect` returned HTTP 403 | access blocked |
| BPPFT_Q004 | Toxicoscordion zygacine | `10.1093/biolinnean/blaa159` | OpenAlex and Unpaywall both point to the same OUP PDF; no exact repository relation | OUP PDF returned HTTP 403 | access blocked |

## Inference boundary

The access result does not weaken the existing B1 direction result. It only means
that, from the currently registered public routes, the project cannot recover the
dose, response unit, denominator, variance, and experimental-unit information
required for B2.

```text
B1: retained — c_D direction is supported in the registered manipulation stratum.
B2: unchanged — no compatible numerical effect is added.
B3: unchanged — no moderator test is created.
B4: unchanged — remains a declared sensitivity map.
```

## Next allowed action

The next action is **not** broader search. It is a bounded access task on these
same four DOI-identified studies: obtain a lawful full-text source through
institutional access or author-provided material, then use
`C_D_C4_MANUAL_READING_SHEET_v1.csv` under `C_D_EXTRACTION_GATE_v1.md`.

A received PDF, accepted manuscript, supplement, or data file must be recorded as
a distinct source version. No result enters `broad_effect_extractions.csv` until
all C4 gate fields are traceable to the source.
