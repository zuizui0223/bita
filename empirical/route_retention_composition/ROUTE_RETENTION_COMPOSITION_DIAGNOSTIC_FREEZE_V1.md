# Route retention: species sorting versus within-type mismatch V1

STATUS: FROZEN BEFORE THE NEW COMPOSITION DIAGNOSTIC OUTPUT
DATE: 2026-10-08
BRANCH: analysis/route-retention-composition-v1

## Existing observations, not new tests

The separate frozen bypass rescue-window test was rejected.
At 1.8× effective hummingbird reach, zero-inclusive legitimate feeding
rates declined as mismatch moved accessible → moderate → severe, while
robbery had uncertain absolute differences and no intermediate maximum.

We are NOT re-testing that rejected window by shifting boundaries. We are asking
why the existing differential retention occurs and what observational evidence
can distinguish consumer-species sorting from within-consumer-type responses.

## Existing theory and novelty boundary

Santamaría & Rodríguez-Gironés (2007) already distinguish trait-complementarity,
exploitation-barrier and neutral abundance mechanisms of network assembly.
Aubert et al. (2026, Oikos, doi:10.1002/oik.11552) already document
trait-mismatch association with nectar robbery among *observed* interactions.
Sakhalkar et al. (2023, Ecosphere, doi:10.1002/ecs2.4696) already demonstrate
spatiotemporal changes in cheating composition.

We do not claim the first consumer-switching, species-turnover or forbidden-link result.

## Question

Could the apparent persistence of robbery under severe mismatch arise
entirely because birds with high baseline robbery rates contribute
disproportionately to severe-mismatch opportunity edges?

Two distinguishable observational accounts:

- Sorting-only: within a bird species (and, more strictly, within bird × site),
  the route-specific mean recorded visits per eligible camera opportunity is
  constant across mismatch categories. Differences arise from who is
  available in each category.
- Pair-context response: even after fixing both bird × site baselines and
  waypoint baselines, route-specific use differs across mismatch categories.

A "pair-context" residual CANNOT by itself establish active individual tactic
switching, causal behavioral plasticity or reward optimization. It can also
arise from plant identity × bird identity matching, differential flower rewards,
observation or unmeasured pair attributes.

## Locked data and categories

Input: original public Aubert/EPHI source tables from
Zenodo DOI 10.5281/zenodo.14185547, under the existing exact
`build_opportunity_edges` and `split_route_counts` functions.

Population: Trochilidae (hummingbirds) only, excluding Diglossa.

Primary mismatch (m = \log(T/(1.8B))).
Categories: accessible (m\le0); moderate (0<m\le\log(1.25));
severe (m>\log(1.25)). No threshold scan.

Opportunity unit: clean camera waypoint × bird species locally observed
in the corresponding site and deployment-date interval, including
zero-visit edges. A bird species is not an identified individual.

## Two nested models, fixed before diagnostic opening

For each route separately (robbery, legitimate), estimate:

M1:
  log E[y_wb] = α_waypoint + γ_bird + θ_moderate I_m + θ_severe I_s

M2:
  log E[y_wb] = α_waypoint + γ_(bird × site)
                + θ_moderate I_m + θ_severe I_s

Both retain the original zero-inclusive opportunity denominator.
Existing Poisson IPF code is used unchanged except that for M2 the
column fixed-effect key is bird × site.

Primary diagnostic contrast:
  RR(severe / accessible) for legitimate and robbery in M1 and M2.

Secondary:
  moderate / accessible and severe / moderate for both routes.

No new p-value will be interpreted as confirmatory. This is
post-outcome model discrimination on the SAME Ecuador dataset.
No additional biological network replicate is implied.

## A direct sorting-only expectation

Conditioning on each bird×site stratum, calculate its observed total
route count Y_bs and available opportunity edges N_bs. Under the
sorting-only null, its category-specific expected count is

  E_bs,g = Y_bs * N_bs,g / N_bs.

Aggregate observed O_g and expected E_g across strata.
Report O_g/E_g, with both:
1. all strata, including single-state strata; and
2. only informative strata containing accessible AND severe opportunity
   edges.

This is a descriptive exchangeability null, not a causal fit:
camera hours, floral abundance and differential detectability per
waypoint are not identical and this null does not adjust for them.
The two-way Poisson M2, which includes waypoint effects, is the
stronger observational control.

## Precommitted decision vocabulary

- SORTING_COMPATIBLE: both within-bird×site severe/access RR estimates
  are close to unity (defined 0.8 to 1.25), or M2 is not identifiable.
  This means the data do not reject fixed consumer-type baselines; it
  does NOT establish species sorting as the cause.
- CONTEXT_ASSOCIATION_ONLY: M2 severe/access contrasts differ from 1
  for either route but do not satisfy stricter evidence conditions.
- CONTEXT_DIFFERENTIATION_STRONG: M2 legitimate severe/access RR has
  a plant-cluster jackknife 95% upper bound below 1 and at least 80%
  of leave-one-plant refits are below 1; AND the severe/access
  robbery point estimate in M2 is not lower than in M1.
  This is STILL observational; there is no claim of individual
  route switching.

If the Poisson M2 cannot be estimated stably, stop with
M2_NOT_IDENTIFIABLE. Never change categories or drop unhelpful
species to rescue the result.

## Before opening coefficients: mandatory support audit

Report:
- source-edge route count reconstruction;
- total edges and 3 category supports;
- total bird and bird×site groups;
- number of bird×site groups spanning accessible and severe;
- groups with ≥1 robbery record and ≥1 legitimate record;
- zero-margin row/column attrition by route;
- all model-fit convergence flags.

## Stronger limitations and next identification step

Even significant M2 residuals cannot distinguish individual behavioral
switching from bird×flower sorting, because identities are observed
at species level, not individual level, and the focal flowers/waypoints
are not randomized. Measuring within-individual tactic transitions
requires individual tracking, or randomized legitimate-/bypass-route
cost manipulations with rewards held constant.

Main Ecology Letters Letter remains untouched. This is an
independent analysis branch and cannot retrospectively change
previously reported first-open results.
