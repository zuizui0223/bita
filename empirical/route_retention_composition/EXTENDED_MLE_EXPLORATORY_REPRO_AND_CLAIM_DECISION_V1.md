# Exploratory extended-MLE robbery rate: fully reproduced and not promoted

Status: **COMPLETED EXPLORATORY NUMERICAL RESOLUTION; NO CONFIRMATORY ROBBERY DIRECTION**
Date: 2026-10-10
Branch: `analysis/route-retention-composition-v1`

## Why this analysis was performed

The original preregistered three-state, zero-inclusive bird×site and
waypoint fixed-effect Poisson robbery model (M2) failed to converge.
A separately audited linear program proved that the published sufficient
statistics lie on a boundary: exactly six otherwise eligible zero-count
opportunities are forced to fitted expectation zero when the row and
column count margins are matched. Ordinary finite nuisance fixed-effect
coefficients therefore do not exist for that full design.

The scientific question left unresolved was whether the two **mismatch
coefficients themselves** have identifiable limiting values, even though
some nuisance intercepts diverge.

This is a *post-outcome diagnostic*, not a modification of the
original preregistration or proof of an ecological mechanism.

## Exact data and model

- Source: frozen anonymous BITA access-routing Letter archive V4,
  GitHub artifact `11293379572`.
- Source SHA256:
  - opportunity table `685f227a2aa2c5c322e18188ba5bd6d44aa67490b31514b9c728e6e033abc14f`
  - bird×plant×site companion `94c74386d2c304b5816653e79b552a0e79487258c5021f8791c614afdc956afa`
- Eligible zero-inclusive hummingbird opportunities: **19,903**,
  bird species **49**, plant species **288**.
- Exact frozen categories: `m=log[tube/(1.8×culmen)]`;
  accessible `m<=0`, moderate `0<m<=log(1.25)`,
  severe `m>log(1.25)`.
- Model: `log(E[robbery_count_wb]) = waypoint_FE + bird×site_FE + θ_moderate I_m + θ_severe I_s`.
- Data coding, opportunity denominator and fixed effects were not changed.

## Mathematical repair: maximal likelihood face

For each positive-margin waypoint×bird-site opportunity network:

1. Find a feasible transportation flow that exactly reproduces the
   route-specific waypoint and bird×site observed count totals.
2. Form its bipartite residual directed graph and identify which
   opportunity cells can carry strictly positive intensity in *some*
   feasible flow using strongly connected components.
3. Identify cells forced to zero by the observed sufficient-statistic
   margins. In full data, **6/2,563** positive-margin cells are forced
   zero; all six have zero observed robbery and lie within
   `site_07`, accessible mismatch.
4. On the **2,557-cell maximal face**, fit the original
   3-category loglinear Poisson model using iterative proportional
   fitting. Check its margins and rank of the two category predictors
   after projecting out the nuisance fixed effects.
5. For **every** leave-one-plant replicate, recompute the
   positive-margin graph and maximal feasible face from scratch; do
   not recycle the six full-data forced zeros.

This is an extended-likelihood fit that can have meaningful category
coefficients even though the original full finite nuisance-parameter
MLE cannot exist. It is **not** a different ecological model or a new
source dataset, but its method was chosen after inspecting a failed
analysis and is therefore exploratory.

## Full-data estimate and joint identifiability

| Quantity | Result |
|---|---:|
| Forced-zero cells in full data | 6 |
| Remaining face cells | 2,557 |
| Waypoint FE groups | 818 |
| Bird×site FE groups | 100 |
| IPF iterations to convergence | 300 |
| Maximum margin relative error | 3.84 × 10⁻¹⁰ |
| Rank of joint residualized mismatch predictors | 2 |
| Residualized design singular values | 14.0462, 8.1122 |

Both mismatch effects survive nuisance FE projection jointly; they
are not exact aliases of the waypoint and bird×site identifiers.

## Plant-level uncertainty (exploratory)

All **288/288** delete-one-plant refits converged after rederiving
the maximal face. Forced-zero cell count across refits ranged 0–20,
median 6.

| Robbery count rate contrast | Extended-MLE RR | 95% plant-jackknife CI |
|---|---:|---:|
| Moderate / accessible | 0.503873 | 0.200678–1.265150 |
| Severe / accessible | **1.027760** | **0.380445–2.776458** |
| Severe / moderate | 2.039721 | 0.762067–5.459445 |

All three intervals include **1**, and hence this exploratory
method does not resolve an absolute robbery-rate increase or decrease.

These are log-coefficient delete-one-plant jackknife working intervals
under boundary-selected support. They should not be misrepresented
as preregistered confirmatory confidence intervals.

## Additional independent group sensitivity

The exact same maximal-face procedure was rerun after excluding each
of the 18 sites or 49 bird species in turn:

| Group deleted | Successful fits | Moderate/access RR range | Severe/access RR range |
|---|---:|---:|---:|
| Site | 18/18 | 0.3827–0.6347 | 0.8011–1.3360 |
| Bird species | 49/49 | 0.4288–1.0882 | **0.5641–2.9995** |

The *one* site hosting all six originally forced-zero cells
(`site_07`) can be removed without changing the full
estimated severe/access RR at reported precision:
`1.027760228674` versus `1.027760228598`.
Thus the estimated rate ratio is not driven by the site that creates
the finite-MLE boundary.

However, deleting `bird_001` changes the severe/access point RR
from 1.028 to 3.000, and moderate/access from 0.504 to 1.088.
The *direction* of the latter effect can reverse under a bird-species
deletion. This further prevents a universal biological interpretation.

These ranges are NOT confidence intervals, nor multiple independent
network replications.

## Fully reproducible execution

Initial successful GitHub Actions run:
[38061289615](https://github.com/zuizui0223/bita/actions/runs/38061289615)
(head `e811b5895d166d87debcc549fd56c5c0adbc37df`).
Independent site/bird sensitivity workflow:
[38061499222](https://github.com/zuizui0223/bita/actions/runs/38061499222)
(head `b44d086760e575bc9b26d101f3fed06d795a23d8`).

Both workflows succeeded, including source checksums,
minimal-face/identifiability unit tests, full 288-plant refits,
and explicit result-expectation assertions.

Scripts:
- `scripts/analyze_route_retention_extended_mle.py`
- `scripts/audit_route_retention_extended_cluster_sensitivity.py`
- `tests/test_route_retention_extended_mle.py`

Official GitHub artifact `11673381415`
(`route-retention-extended-mle-exploratory`) contains the exact full
coefficient/CI receipt plus site/bird deletion-level JSON.

## Ecological result and manuscript decision

**Supported (previous independently reproduced route analysis):**
Strong severe-mismatch reduction in **legitimate** feeding persists
with bird×site and camera-waypoint FE:
RR = **0.0489769**, 95% plant-jackknife CI **0.026546–0.090360**
(288/288 converged leave-one-plant fits).

**Exploratory and unresolved (this analysis):**
Absolute **robbery** rate has severe/access RR ≈ **1.028**,
95% exploratory jackknife CI **0.380–2.776**;
rate direction is uncertain and bird-species deletion is influential.

**Not identifiable with these data:**
Same individual switching from legitimate to robbery,
adaptive payoff or rewards, a causal effect of morphology,
or the relative contributions of changing bird–flower pairing
and individual behavioral compensation.

Therefore preserve the existing Ecology Letters Letter's
source-backed *conditional robbery prevalence versus absolute
route frequency* message. Do **not** promote the new numerical
repair as a new confirmatory effect or imply increased robbery.
Keep the original frozen finite-Poisson M2 as `NOT_FIT` and retain
this document as exploratory Supplementary Methods / audit evidence.
