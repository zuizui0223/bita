# Broad Crossref deep-harvest receipt v1

## Purpose

This is the registered receipt for the first expanded retrieval of the existing
21-query broad evidence registry. It changes **retrieval depth only**: the query
texts, route families, metadata screen, and priority rule are unchanged from the
initial 200-record-per-query seed.

## Immutable run receipt

```text
workflow:              Harvest broad reality evidence
workflow run:          28635506290
run date:              2026-07-03
source commit:         fcd5adfad79a149b391b0fd11a0970a82efb816a
artifact:              broad-reality-evidence-corpus
artifact SHA-256:      40b7f416918665b31d28f1feadcbed8bde2ca5e17d723424c1097cc0f26f9c81
source:                Crossref REST API
query routes:          21
requested depth:       2,000 journal-article records per query
raw query memberships: 42,000
unique DOI/title candidates: 22,924
abstract metadata available: 7,180
priority metadata screen: 1,771
```

All 21 query reports reached the 2,000-record cap, and every report indicated
that Crossref reported more works than requested. Therefore, this run is an
expanded **retrieval cap**, not an exhaustive census of the literature.

## Role of this receipt

```text
initial 200-per-query seed
    -> 2,896–2,898 unique candidates and 650–657 priority candidates

expanded 2,000-per-query retrieval
    -> 22,924 unique candidates and 1,771 priority candidates
```

The expanded corpus replaces the old seed as the current discovery universe for
route-balanced source coding. It does **not** itself add any verified effect,
change an arrow sign, establish study eligibility, or update Part B parameter
estimates.

## Next decision boundary

The fact that every query still hits the 2,000-record cap is insufficient by
itself to justify a 5,000-record expansion. The companion rank-binned depth
saturation diagnostic records metadata-screen yield every 200 ranked records on
subsequent runs. Its purpose is to compare the head and tail of each existing
query before deciding whether deeper pages remain a useful source of direct-route
studies.

That diagnostic remains metadata-only. A route-balanced human source-coding audit
of tail pages is required before any decision about further deepening, and before
any candidate can enter the verified Part B effect table.
