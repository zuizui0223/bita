# Route-retention composition diagnostic — first point readout

Date: 2026-10-08
Status: **POINT DIAGNOSTIC COMPLETE; M2 ROBBERY NOT CONVERGED**
Branch: `analysis/route-retention-composition-v1`
Frozen protocol: `ROUTE_RETENTION_COMPOSITION_DIAGNOSTIC_FREEZE_V1.md`

## Provenance
Successful point job:
https://github.com/zuizui0223/bita/actions/runs/37783945027
Point artifact ID: `11553820728`
Source: Aubert / EPHI DOI 10.5281/zenodo.14185547
Program: `scripts/analyze_route_retention_composition.py`
Classification and denominator unit tests: PASS.

19,903 zero-inclusive hummingbird x waypoint opportunities, 49 bird
species, 288 plant species, 4,933 waypoints.

State supports:
- accessible 14,770 edges
- moderate mismatch 1,847
- severe mismatch 3,286

All original pooled, legitimate, and robbery route edge counts reconstruct exactly.

## Sorting-only expectation (bird x site fixed average rate)

The prediction holds the pooled route count fixed within each bird x site,
then allocates counts across mismatch bins in proportion to eligible
opportunity-edge counts.

Among bird x site strata with both accessible and severe support:

| State | Legitimate observed/expected | Robbery observed/expected |
|---|---:|---:|
| Accessible | 1.22134 | 0.69631 |
| Moderate | 0.89490 | 1.06921 |
| Severe | 0.26268 | 1.58707 |

This descriptive count discrepancy is **not** a randomization test, not a
camera-hour-adjusted rate ratio, and cannot be promoted as evidence of
individual tactics or individual flexibility. Plant selection within a
bird x site and differential camera opportunity effort remain possible.

## Three-state fixed-effect Poisson point estimates

| Route / contrast | Bird FE + waypoint FE (M1) | Bird x site FE + waypoint FE (M2) |
|---|---:|---:|
| Legitimate moderate/access | 0.31493 | 0.30704 |
| Legitimate severe/access | 0.05330 | 0.04898 |
| Legitimate severe/moderate | 0.16925 | 0.15951 |
| Robbery moderate/access | 0.74602 | NOT_FIT |
| Robbery severe/access | 1.21732 | NOT_FIT |
| Robbery severe/moderate | 1.63176 | NOT_FIT |

The M2 robbery IPF routine did not satisfy its convergence check after
10,000 iterations (remaining max margin relative error
`8.445273606494386e-05`). We have **not** replaced the frozen estimator
with one selected after opening the result, nor treated a failure to
converge as a biological zero or negative effect.

The M2 legitimate model converged after 56 iterations, with max margin
relative error `7.502298436811039e-09`. It used 15,352
positive-margin supported edges, 3,645 waypoint fixed-effect groups
and 242 bird x site fixed-effect groups.

**No complete causal partition of consumer sorting versus behavioral
rerouting is identified by these results.**

## Claim ceiling

Allowed:
- The observed legitimate suppression under severe mismatch is not
  explained away by replacing bird FE with bird x site FE in point fits.
- A simplistic within-bird x site constant route-frequency expectation
  disagrees descriptively with the observed route composition.

Not allowed:
- "robbery increases under mismatch after controlling bird x site"
  (the M2 robbery model is not stable);
- "individual birds switch to robbery";
- "bypass rescues individual feeding success";
- "sorting is ruled out" at the flower-selection or observation level.

The remaining full plant jackknife is a separate computational
uncertainty diagnostic, not an opportunity to revise the model after
the failed robbery fit. Its status must be reported explicitly.
