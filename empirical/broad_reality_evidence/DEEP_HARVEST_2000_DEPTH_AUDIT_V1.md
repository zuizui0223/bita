# Deep Crossref retrieval: rank-binned depth diagnostic v1

## Scope

This receipt evaluates the first 2,000-record-per-query run of the pre-existing
21-query Crossref registry. It asks a narrow retrieval question:

> Do the last 400 retrieved ranks still produce enough plausible candidates to
> justify a deeper retrieval, or should source coding return to the current corpus?

It is a metadata-only diagnostic. No result below establishes a direct biological
arrow, effect direction, effect size, causal effect, or meta-analytic inclusion.

## Run receipt

```text
repository:            zuizui0223/bita
workflow:              Harvest broad reality evidence
workflow run:          28636148544
run date:              2026-07-03
source commit:         f5963fa4692128ae6953acc095c58052a7d9c2f9
artifact:              broad-reality-evidence-corpus
artifact SHA-256:      4f1cf18ff13bdc3d543d9151ca71b7aa9b6ac96605b95a3fead7ca104340aa2a
query registry:        unchanged, 21 query routes
requested depth:       2,000 journal-article records per query
raw records returned:  42,000
unique candidates:     22,678
metadata-priority:     1,765 unique candidates
```

The small difference from the earlier 2,000-depth receipt is expected because
Crossref is a live provider. This file records the exact artifact used for the
rank-binned decision.

## Overall rank yield

| Query-rank band | Candidate memberships | Metadata-priority memberships | Priority rate |
|---|---:|---:|---:|
| 1–200 | 4,200 | 1,254 | 29.86% |
| 201–400 | 4,200 | 923 | 21.98% |
| 401–600 | 4,200 | 945 | 22.50% |
| 601–800 | 4,196 | 851 | 20.28% |
| 801–1000 | 4,189 | 529 | 12.63% |
| 1001–1200 | 4,173 | 431 | 10.33% |
| 1201–1400 | 4,161 | 341 | 8.20% |
| 1401–1600 | 4,164 | 285 | 6.84% |
| 1601–1800 | 4,164 | 211 | 5.07% |
| 1801–2000 | 4,154 | 156 | 3.76% |

The final 400 ranks have **367 / 8,318 = 4.41%** metadata-priority memberships,
compared with **1,254 / 4,200 = 29.86%** in ranks 1–200. Thus, metadata yield
falls sharply but does not vanish.

## Head-versus-tail yield by route family

The head is ranks 1–200. The tail is ranks 1,601–2,000.

| Route family | Head priority | Head rate | Tail priority | Tail rate |
|---|---:|---:|---:|---:|
| attraction → antagonism | 138 / 600 | 23.00% | 19 / 1,132 | 1.68% |
| attraction → pollination | 533 / 1,200 | 44.42% | 92 / 2,387 | 3.85% |
| barrier → antagonism | 117 / 800 | 14.63% | 52 / 1,599 | 3.25% |
| barrier → pollination | 173 / 400 | 43.25% | 25 / 800 | 3.13% |
| joint channels | 293 / 1,200 | 24.42% | 179 / 2,400 | 7.46% |

## Decision

**Do not deepen to 5,000 records per query yet.** The tail still has candidates,
but its metadata-priority yield is 4.41% overall and only 1.68% for the current
`A_to_antagonism` crux. A larger retrieval now would multiply screening work
without evidence that it adds direct-route studies.

Instead, run a small, deterministic source-coding audit:

```text
head: ranks 1–200
tail: ranks 1,601–2,000
screen strata: priority and biological_nonpriority
sampling: up to 10 rows per route × rank stratum × screen stratum
within-route rule: exclude a tail candidate if it already occurred in the head
```

The audit reads source-level metadata and, where available, full text to code only
whether the requested direct route is actually present. It will compare direct-route
yield in head and tail within each screen stratum. Only after that comparison can a
5,000-record expansion be justified or rejected.

## Boundary

This diagnostic is not a meta-analysis result. It does not change the verified
Part B effect table, moderator models, effect estimates, arrow signs, or the
support-not-proof claim boundary.
