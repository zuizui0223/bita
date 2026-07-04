# Phlox `d_A` abstract-route readout v1

## Fixed source

```text
candidate:  dA_cand_phlox_hirsuta
DOI:        10.1093/aob/mcu007
PubMed ID:  24557879
```

## Public abstract routes

```text
publisher abstract HTML: HTTP 403 for the reproducible no-auth client
PubMed DOI lookup + EFetch XML: recovered
```

The screen stored structural term signals only, not abstract prose or numerical
results.

## Regression structure recovered

```text
response term:                 fruit set / percentage fruit set
regression context:            multiple linear regressions
trait predictor term:          floral display size
antagonist predictor term:     florivorous beetle density
```

The public abstract describes variation in fruit set as the regression target while
floral display size and florivorous beetle density are assessed explanatory factors.
It does **not** establish a model in which floral display is the predictor and
florivory is the outcome.

## Decision

```text
direct display -> florivory model: not located
C4 numerical extraction:        stop
new B2 effect row:               0
new B3 cluster:                  0
candidate status:                candidate_screened_context_only
```

This does not imply that floral display never affects florivory in *Phlox hirsuta*.
It is a source-contract decision: the accessible abstract supports parallel effects
on fruit set, not the marginal `d_A` route required by Part B. Any later
reconsideration requires a separately located model with florivory as the response,
floral display as an independent predictor, and an outcome definition plus
uncertainty.
