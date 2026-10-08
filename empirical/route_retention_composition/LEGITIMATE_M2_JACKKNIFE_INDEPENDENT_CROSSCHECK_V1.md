# Route-retention composition: independent numerical jackknife cross-check

Status: **LEGITIMATE M2 JACKKNIFE COMPUTED; ROBBERY M2 UNRESOLVED**
Date: 2026-10-08
Branch: `analysis/route-retention-composition-v1`
Frozen protocol: `ROUTE_RETENTION_COMPOSITION_DIAGNOSTIC_FREEZE_V1.md`

## Why a separate numerical cross-check was made

The initial full GitHub Actions plant-jackknife job failed **before
reading the outcome**, when Zenodo returned HTTP 504 retrieving
`Interactions_data_Ecuador.txt`. The first point job had already
succeeded and shown that legitimate M2 converged whereas robbery M2
did not converge in 10,000 fixed IPF iterations.

A separately written, NumPy-vectorized implementation of the same
three-state Poisson iterative proportional fitting equations was run
directly against the immutable anonymous `BITA_ACCESS_ROUTING_LETTER_ARCHIVE_V4`.
The version of the observation matrix, three mismatch bins, fixed effects,
zero margins pruning, plant deletions, and 95% jackknife formula were unchanged.
The new implementation is a **numerical cross-check**, not a post-outcome
substitute for a different scientific model or a second data replication.

Both source-CSV SHA-256 hashes were checked:
- opportunity CSV: `685f227a2aa2c5c322e18188ba5bd6d44aa67490b31514b9c728e6e033abc14f`
- pair-site CSV: `94c74386d2c304b5816653e79b552a0e79487258c5021f8791c614afdc956afa`

## Exact point-fit agreement

The independently vectorized IPF reproduced, to reported numerical precision:

| Route and fixed effects | Moderate/access RR | Severe/access RR | Iterations |
|---|---:|---:|---:|
| Legitimate M1: waypoint + bird | 0.3149269413590195 | 0.05330046808306707 | 183 |
| Legitimate M2: waypoint + bird×site | 0.3070430221430995 | 0.04897687680739414 | 56 |
| Robbery M1: waypoint + bird | 0.7460151316049396 | 1.2173212224518681 | 216 |

The robbery M2 again failed the exact original convergence criterion
after 10,000 iterations; final maximum relative margin error
`8.445273606494386e-05`. Its incomplete coefficients are **not estimates**.

## Legitimate M2: delete-one-plant jackknife

All **288/288** plant deletions returned finite converged M2 estimates.

| Comparison | RR | 95% jackknife CI | Fraction of leave-one fits with RR < 1 |
|---|---:|---:|---:|
| Moderate/access | 0.3070430 | 0.1960140–0.4809627 | 288/288 |
| Severe/access | 0.0489769 | 0.0265463–0.0903604 | 288/288 |
| Severe/moderate | 0.1595114 | 0.0914561–0.2782090 | 288/288 |

This strengthens the descriptive inference that legitimate interaction
is selectively reduced by greater access mismatch **even when fixed
bird×site and waypoint baselines are included**.

Do not infer active behavioral switching, adaptive cost, individual
identity persistence, or a causal floral-geometry effect.

## Remaining identification limit

Robbery M2 remains nonconvergent. Only 29/246 bird×site groups
have positive robbery events at both accessible and severe
mismatch levels; this suggests sparse within-group information but
does not mathematically prove the cause of nonconvergence.

Neither route's results demonstrate whether a given individual
switches tactics. The archive contains bird *species* identities,
not a tracked individual identifier. Pair-specific plant reward
and detection heterogeneity remain open.

## Workflow state

Archive-input support was committed to
`scripts/analyze_route_retention_composition.py` with checksum
checks and point-estimate reproduction assertions.
A GitHub Actions run was queued to test that transport-only change.
The independent numerical result is fully computed but should be
compared to the frozen original IPF workflow if and when that
run finishes. No claim of GitHub Actions jackknife success is
being made here.
