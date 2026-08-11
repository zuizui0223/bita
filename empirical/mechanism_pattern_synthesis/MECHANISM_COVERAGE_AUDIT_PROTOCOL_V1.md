# Mechanism-pattern coverage audit protocol v1

## Purpose

This audit turns the accumulated mechanism ledgers into a reproducible coverage state. It does **not** estimate biological prevalence, publication probability, or a pooled effect.

The input universe is fixed to the source-adjudicated records committed under:

```text
MASTER_LEDGER_V1.csv
LEDGER_BATCH_2_V1.csv
LEDGER_BATCH_3_V1.csv
LEDGER_BATCH_4_V1.csv
LEDGER_BATCH_5_V1.csv
```

Discovery-only candidate tables, abstract queues, PR #124's separate antagonist-pressure meta-analysis, and PR #125's separate D-to-pollination synthesis are not silently inserted into this ledger count. They remain independent synthesis modules and are described separately in the readout.

## Unit of counting

The primary unit is `independence_cluster`, not effect row.

Multiple:

- outcomes;
- doses;
- years;
- animal species;
- plant species inside one experiment;
- direct A×D reproductive components

from the same `independence_cluster` contribute one cluster to a route-coverage count.

## Route states

The audit reports cluster counts for:

```text
A_to_pollination
A_to_antagonism
D_to_antagonism
D_to_pollination
direct_AxD
```

A cluster is `quantitative` for a route when at least one row for that route contains finite `effect_value` and finite `standard_error`.

A cluster is `primary_quantitative` when, in addition, at least one such row has `is_primary_effect=true`.

Rows with numerical values but explicit source/deposit or source/subset mismatch flags remain quantitative **sensitivity** records and are not promoted to primary quantitative evidence merely because numbers exist.

## Sign resolution

The coverage audit does not infer biological sign from raw numeric values across different metrics. It reports whether rows contain a declared `effect_orientation` and whether quantitative uncertainty is present.

No cross-metric sign vote is generated here.

## Same-system coverage

A cluster is counted as `same_system_multi_route` when either:

1. at least one record explicitly has `is_same_system_multi_route=true`; or
2. two or more distinct marginal routes occur in the same `independence_cluster`.

Direct A×D is counted separately and does not by itself manufacture marginal-route co-occurrence.

## Data-quality flags

The audit counts clusters whose `source_verification_state` or `notes` contain any of:

```text
discrepancy
unresolved
pending
blocked
sensitivity
```

These are not exclusions. They are an explicit evidence-quality layer.

## Completion-gate interpretation

The generated readout may inform the following gates:

- Gate B: whether all four marginal mechanism families now have source-adjudicated records and quantitative/directional state;
- Gate C: how many independent quantitative clusters exist, while remembering that a true synthesis module requires compatible effects rather than a mere count;
- Gate D: sign-switch coverage is reported from `SIGN_SWITCH_LEDGER_V1.csv` separately;
- Gate E: same-system multi-route cluster count;
- Gate H: the script contains no operation that combines marginal routes into `W_AD`.

It does **not** declare Gate A (direct-search saturation), Gate F (joint-cost saturation), or Gate G (bias/robustness) passed.

## Prohibited interpretations

The following are explicitly invalid:

```text
cluster count = prevalence in nature
quantitative cluster count = meta-analysis sample size
number of positive/negative rows = universal biological sign
marginal route coverage = estimate of W_AD
same-system multi-route count = direct A x D evidence
```
