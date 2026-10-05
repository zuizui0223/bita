# Aubert effective-reach and grain sensitivity — frozen post-open plan

## Status

```text
ANALYSIS_TIMING = POST_OPEN_SENSITIVITY
PRIMARY_RESULTS_ALREADY_OPENED = YES
PURPOSE = DIAGNOSE_CULMEN_ONLY_ACCESS_PROXY_AND_P1_P2_GRAIN_DIFFERENCE
CONFIRMATORY_STATUS = NO
```

This analysis was motivated after the pooled participation effect and the
route-specific decomposition were known. It cannot be promoted to a preregistered
confirmatory result.

## Why this sensitivity is needed

The active Letter currently uses culmen length alone in

[
M = \log(T/B)
]

and defines a binary barrier as (T>B).

That convention follows Aubert et al. (2026), but hummingbirds can protrude the
tongue beyond the bill tip. Grant & Temeles (1992; PNAS
10.1073/pnas.89.20.9400) found in *Selasphorus rufus* that maximum tongue
extension was approximately one bill length, implying maximum reach close to
twice bill length in narrow tubes; the same experiment showed that reach declines
with tube width and that efficient feeding occurs at shallower protrusion.
Vizentin-Bugoni, Maruyama & Sazima (2014; Proc. R. Soc. B
10.1098/rspb.2013.2397) used (4/3) bill length as a pragmatic hummingbird
effective-reach correction when species-specific tongue data were unavailable.

The literature therefore does **not** justify one universal tongue multiplier.
We use two fixed multipliers only as sensitivity bounds:

```text
k = 1.00   original culmen-only definition
k = 4/3    published network correction when tongue lengths are unavailable
k = 2.00   maximum-reach stress test motivated by S. rufus
```

## Taxonomic scope

Reach sensitivities are restricted to **Trochilidae**.

`Diglossa` is excluded from the reach-corrected sensitivity because
flowerpiercers use a different feeding apparatus and commonly access nectar by
piercing the corolla. A hummingbird tongue multiplier is not assigned to
flowerpiercers.

## Algebraic consequence for the continuous mismatch and threshold fit

For a fixed multiplier (k),

[
M_k = \log\{T/(kB)\}=M-\log k.
]

Therefore a fixed multiplier cannot change:

- the rank ordering of mismatch;
- a Spearman correlation using the same hummingbird observations;
- sigmoid shape or goodness of fit;
- whether the fitted midpoint lies at the 5–95% support boundary.

It only translates the mismatch coordinate. Accordingly, the threshold analysis
will **not** be rerun and reinterpreted as a newly localized transition. Instead,
the frozen first-open midpoint, support and bootstrap interval will be translated
by (-\log k) as an exact diagnostic.

## Quantities that can change

The binary classification

[
I(T>kB)
]

does change with (k). For each multiplier, using hummingbirds only, we will
recompute:

1. zero-inclusive pooled resolved-feeding RR under the existing waypoint + bird
   fixed-effect Poisson model;
2. legitimate/non-robbing RR under the same model;
3. robbery-only RR under the same model;
4. the number and fraction of opportunity edges classified as barriers;
5. the plant-level paired barrier-minus-accessible robbery contrast;
6. the hummingbird-only plant-level continuous mismatch–robbery Spearman
   association as a guardrail. Under a constant multiplier its value must be
   invariant across (k).

Uncertainty for participation RRs remains the existing delete-one-plant-species
jackknife. No new multiplicity-adjusted confirmatory p-values are claimed.

## Grain interpretation frozen before opening this sensitivity

The two headline analyses condition on different dimensions.

- **P1 plant / within-bird routing:** compares flowers used by a given bird and
  asks whether route composition changes as the bird–flower relation changes.
- **P2 waypoint + bird fixed effects:** one waypoint corresponds to one plant.
  The waypoint fixed effect absorbs the plant/tube main effect, so the binary
  barrier varies within waypoint through bird bill length. Its coefficient asks
  whether locally available birds on the short-bill side of the threshold differ
  in feeding rate relative to their own bird baseline.

P2 is therefore **not** a second estimate of the same plant-level barrier
contrast as P1. Opposite route-specific directions across P1 and P2 are not
algebraically contradictory; they describe different conditional grains.

## Decision rules

This sensitivity can change the biological interpretation only if the
route-specific P2 result changes materially under a literature-grounded reach
multiplier.

It cannot, by itself:

- convert the observational analysis into a causal test;
- identify a universal hummingbird reach allometry;
- convert the support-boundary sigmoid midpoint into an interior threshold;
- override the original frozen culmen-based estimands.

All results are retained regardless of direction.
