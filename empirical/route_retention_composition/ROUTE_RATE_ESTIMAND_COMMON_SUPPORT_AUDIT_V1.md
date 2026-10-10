# Estimand audit: route-specific positive-margin pruning and shared opportunity support

Date: 2026-10-11
Branch: `analysis/route-retention-composition-v1`
Status: **POST-OUTCOME SOURCE/DENOMINATOR AUDIT; NO CONFIRMATORY REINTERPRETATION**
Original research question: when robbery prevalence rises with morphological mismatch,
does absolute robbery rise or is legitimate interaction being selectively lost?

## Why this audit was necessary

The originally archived EPHI zero-inclusive opportunity matrix has 19,903
hummingbird waypoint × locally available bird-species edges (Diglossa excluded).
For Poisson fixed-effect estimation, the existing code repeatedly eliminates
zero-total waypoint and bird-group margins for the response being fitted.
This operation differs for the two routes.

As a result, the denominator of *constructed opportunities* is common before
model fitting, but the **positive-margin support actually contributing to each
fitted route-specific fixed-effect coefficient is not common**.

This distinction does not invalidate the separate fitted rate ratios or the
zero-inclusive *construction*. It limits what can be inferred from dividing
the two fitted coefficients, especially as a single-population "relative
retention" effect.

## Original source audit: same 1.8× reach partition, same observations

Source: anonymous EPHI submission archive V4; original frozen GitHub
artifact `11293379572`.
SHA256 checksums:
```text
opportunities:
685f227a2aa2c5c322e18188ba5bd6d44aa67490b31514b9c728e6e033abc14f
pair-site:
94c74386d2c304b5816653e79b552a0e79487258c5021f8791c614afdc956afa
```

At **bird species × site + camera waypoint FE (M2)**:

| Universe or response-specific positive-margin support | Opportunity edges |
|---|---:|
| Original hummingbird opportunity matrix | 19,903 |
| Legitimate M2 support | 15,352 |
| Robbery M2 support (before extended-face restriction) | 2,563 |
| Intersection of the two separately pruned supports | 2,195 |
| Robbery-only support | 368 |
| Legitimate-only support | 13,157 |
| Neither | 4,183 |

The intersection is only **11.03%** of the full hummingbird opportunity
matrix. In the robbery route M2, 6 additional opportunity cells were forced
to fitted intensity exactly zero due to boundary separation; its
extended-likelihood face had 2,557 cells. In the legitimate route M2, a
finite Poisson MLE existed on 15,352 cells.

At the original **bird-species + camera waypoint FE (M1)** used for the
Letter's binary 1.8× reach result:

| Support | Opportunity edges |
|---|---:|
| Robbery M1 | 3,371 |
| Legitimate M1 | 15,377 |
| Their positive-margin intersection | 2,900 |
| Their union | 15,848 |
| Neither | 4,055 |

Therefore the published 1.8× route RR ratio of about 5.31 comes from
two FE route-specific estimates with different positive-margin supports
even though both started from the same opportunity matrix.
It is a **ratio of separate, supported-subset rate ratios** and should
not be described as a directly observed common-risk-set route
replacement factor.

## Exploratory common-positive-margin analysis (M2)

As a descriptive sensitivity, start afresh from all 19,903 opportunities,
repeatedly intersect route-specific positive-row and positive-bird×site
margins until no further edges are dropped. This yields:

```text
iteration count = 4
joint-positive-margin opportunities = 1,986
plant species = 126 (not 288)
accessible / moderate / severe = 1,267 / 216 / 503
observed robbery records = 3,176
observed legitimate records = 5,728
```

The exact three-state Poisson model and original mismatch thresholds were
retained. Each route was fit to its own maximal finite-likelihood face
within this jointly pruned source set:

| Comparison | Robbery RR | Legitimate RR | Ratio of RRs |
|---|---:|---:|---:|
| Moderate / accessible | 0.44424 | 0.24511 | 1.81244 |
| Severe / accessible | 0.96542 | 0.07810 | 12.36179 |
| Severe / moderate | 2.17319 | 0.31863 | 6.82051 |

Full-data extended face: robbery 1,983/1,986 edges after 3 forced-zero
cells; legitimate 1,986/1,986 edges.

The **paired** delete-one-plant procedure recalculated the joint
positive-margin support and both extended fits for every leave-one
replicate, and succeeded for all 126 contributing plants.

| Relative route RR contrast | Point ratio | 95% working plant jackknife interval |
|---|---:|---:|
| Moderate / accessible | 1.812 | 0.554–5.926 |
| Severe / accessible | 12.362 | 4.124–37.053 |
| Severe / moderate | 6.821 | 1.640–28.373 |

### Crucial non-promotion boundary

**This procedure is doubly post-outcome selective.** A fixed-effect group
enters joint support only if it has positive *observed* counts in
*both* routes. As a result, 162 of the 288 original plant species do not
contribute to the full joint-support analysis.

Conditioning on observation of each route can introduce selection bias,
even if the two resulting analyses share a support set. The 126-plant
working jackknife interval is **not a population-level confirmatory
interval** for the original 288 plants and must not be used to rescue
the original 5.31 contrast or claim a causal shift in individual tactics.

## Required manuscript wording changes

- Distinguish **constructed opportunity denominator** from
  **outcome-specific FE support after zero-margin pruning**.
- Report the two route-specific rate ratios and their uncertainty
  separately as the empirical basis.
- If the ratio 5.31 is retained, identify it explicitly as a
  **descriptive ratio of separately fitted route-specific rate ratios**,
  not an identified common-risk-set substitution effect.
- Replace species-level "within-bird switching" prose with
  "within-bird-species route-composition association" (no tracked
  individual transitions).
- Preserve post-open reach correction and model diagnostics as
  sensitivities; do not present them as prospectively confirmed.
- Do not promote the exploratory 12.36 result to the main manuscript.

## Scientific claim that remains defensible

The EPHI network has a robust route-composition–mismatch association,
and in the 1.8× reach sensitivity a marked decline in the
**separately supported** legitimate feeding rate (RR 0.154,
95% CI 0.087–0.271); no statistically detected absolute robbery
increase was obtained (RR 0.816, 0.358–1.860).

A more stringent exploratory M2 analysis on its separately supported
legitimate route found severe/access RR 0.049 with
95% plant-jackknife CI 0.027–0.090. The robbery M2
required extended-likelihood boundary treatment and did not resolve
a positive or negative absolute trend, making individual behavioral
compensation or common-risk-set causal substitution unproven.

Source data alone cannot identify fitness adaptation, per-individual
switching, variation in nectar reward, or a common-risk-set
robbery/legitimate contrast without a model that retains and identifies
the full available opportunity population.

No primary paper numbers are retrospectively changed by this audit.
