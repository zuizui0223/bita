# Cheater-dominance / mutualism-attrition cross-fit preregistration v1

Status: **FROZEN BEFORE CROSS-FIT OUTCOME OPENING**

Frozen on: 2026-10-07
Branch: `analysis/ecological-stability-evolutionary-transience-v1`

## Scientific question

Does a plant that looks "cheater dominated" actually experience more antagonistic
interaction, or can a high conditional robbery share instead mark a collapse of the
legitimate interaction channel?

A conditional route proportion,

```text
robbery share = robbery / (robbery + legitimate),
```

cannot distinguish those possibilities within the same observations. The current
BITA route-rate decomposition already establishes that point for one barrier contrast.

The new test is deliberately harder and non-algebraic:

> Does high robbery share estimated from one independent subset of a plant's camera
> sampling predict *lower absolute interaction throughput* in a disjoint subset?

If yes, high cheating prevalence can be an ecological symptom of mutualistic
attrition rather than a measure of stronger absolute exploitation.

## Prior-literature boundary

Already known and therefore not claimable:
- nectar robbery can reduce legitimate visitation in some systems;
- mismatch can increase conditional robbery;
- conditional interaction proportions can differ among species and contexts;
- cheating can create additional interaction links and can stabilize ecological
  communities under model conditions.

The target here is the cross-fitted population/network prediction that a high
conditional cheating fraction can forecast **less total interaction flux**, because
the legitimate route is selectively lost.

## Data

Primary dataset:
EPHI all-Ecuador public camera/interactions/plant/bird tables
(Zenodo 10.5281/zenodo.14185547).

Use the existing BITA source rules:
- clean camera waypoint: valid camera rows with `camera_problem=no`, positive
  sampling duration, parseable dates, unique waypoint/site/plant identity;
- resolved feeding excludes explicit `feeding_activity=no_feeding`;
- primary route coding: `piercing=yes` = robbery; `piercing=no` plus blank/NA
  piercing = legitimate; nonbinary route states excluded;
- target consumers = Trochilidae plus Diglossa for the all-bird primary ecological
  throughput, with a hummingbird-only sensitivity excluding Diglossa.

## Frozen cross-fit split

The independent sampling unit is the unique clean **waypoint**.

Assign every waypoint to exactly one fold using 32-bit FNV-1a hashing of the raw
waypoint string:

```text
hash = FNV1a32(UTF-8 waypoint)
fold A if hash mod 2 == 0
fold B if hash mod 2 == 1
```

The fold assignment depends only on waypoint identity and is fixed before route
outcomes are opened.

No waypoint contributes to both the predictor and response of the same directional
test.

## Plant eligibility

A plant species enters a directional A->B test only if:

1. it has >=2 clean waypoints in predictor fold A and >=2 in outcome fold B;
2. predictor fold A contains >=5 resolved feeding interactions for that plant;
3. outcome fold B has positive total clean sampling hours;
4. the same plant identity is represented in both folds.

The B->A swap uses the symmetric rule.

Primary cross-fit effect combines the two directional tests with equal fold weight;
a plant can contribute to one direction even if it fails the opposite direction.

Prespecified sensitivities:
- predictor-fold minimum >=10 resolved feeding events;
- >=3 clean waypoints per fold;
- hummingbird-only (Trochilidae, excluding Diglossa);
- explicit yes/no piercing only.

## Predictor: independently estimated cheater dominance

For each eligible plant in predictor fold:

```text
C_share =
N_robbery /
(N_robbery + N_legitimate)
```

This is deliberately the conventional conditional cheating prevalence.

No absolute-rate information from the outcome fold is used to construct it.

## Primary response: absolute total interaction throughput

For the same plant in the disjoint outcome fold:

```text
F_total =
(N_robbery + N_legitimate) /
sum(clean camera sampling hours)
```

Units: resolved feeding events per camera-hour.

Primary directional statistics:

```text
rho_AtoB = Spearman(C_share_A, log1p(F_total_B))
rho_BtoA = Spearman(C_share_B, log1p(F_total_A))
```

The primary equal-fold statistic is

```text
rho_X =
tanh(
  [atanh(rho_AtoB) + atanh(rho_BtoA)] / 2
)
```

Primary hypothesis:

```text
rho_X < 0
```

A negative value means that a plant's high cheating share in one independent sample
predicts lower total interaction flux in another sample.

## Route decomposition

Using the same disjoint outcome fold, calculate:

```text
F_legitimate = N_legitimate / camera_hours
F_robbery    = N_robbery / camera_hours
```

For each direction estimate:

```text
rho_L = Spearman(C_share_predictor, log1p(F_legitimate_outcome))
rho_R = Spearman(C_share_predictor, log1p(F_robbery_outcome))
```

Frozen mechanistic prediction:

```text
rho_L < 0
and
rho_L < rho_R
```

No requirement is imposed that `rho_R` itself be negative. The key prediction is
selective attrition of legitimate flux.

Combine A->B and B->A route correlations with the same equal-fold Fisher-z rule.

## Zero-inclusive secondary response

As a secondary robustness analysis, reuse the existing BITA local-availability rule:

for each clean waypoint, the local opportunity set is target bird species observed
elsewhere at the same site during that waypoint's valid camera dates.

For each plant/fold calculate:
- proportion of bird x waypoint opportunities with any resolved feeding;
- proportion with any legitimate feeding;
- proportion with any robbery.

The same cross-fit predictor must be used. This asks whether the result is robust to
an opportunity denominator rather than event counts.

## Flower-effort sensitivity

Where every clean camera row contributing to a waypoint has positive
`camera_flowers_count`, calculate flower-hours:

```text
sum(duration_sampling_hours * camera_flowers_count)
```

and repeat the absolute-rate response per flower-hour. This is sensitivity-only and
cannot replace the primary camera-hour result.

## Primary inference

The inferential unit is plant species.

For each direction separately, permute predictor plant labels relative to outcome
plants 99,999 times (seed 20261007), preserving the predictor values and the complete
outcome vector. On each permutation compute both directional correlations and the
equal-fold `rho_X`.

The primary one-sided p-value is the fraction of permuted `rho_X <= observed rho_X`
with plus-one correction. Also report a two-sided p-value.

Because a plant can occur in both directional tests, a species bootstrap resampling
plant identities globally is used for the 95% interval around `rho_X`.

If either directional test has fewer than 20 eligible plant species, the primary
cross-fit gate fails and the hypothesis is not promoted from EPHI.

## Non-independence / site sensitivity

Primary inference is plant-level and may include plants occurring at multiple sites.

Frozen sensitivity:
- first aggregate within plant x site;
- compute site-specific predictor/response values within the fixed folds;
- center ranks within site;
- estimate the pooled within-site rank association.

This is diagnostic; it cannot rescue a failed primary cross-fit.

## Mechanistic secondary: mismatch conditioning

High cheating share may be generated by access mismatch. That does not invalidate
the attrition hypothesis, but it matters mechanistically.

Using outcome-blind trait data, calculate each plant's fold-specific mean
zero-inclusive log(tube / bill) across locally available bird opportunities.

Residualize rank(C_share) and rank(F_total) separately on rank(mean mismatch) and
repeat the cross-fit correlation between residuals.

This secondary test asks whether cheating share contains information about throughput
beyond the static trait mismatch itself.

## Promotion rule

Promote the mutualism-attrition hypothesis only if:

1. primary `rho_X < 0`;
2. both directional correlations are negative;
3. the legitimate route decomposition is negative and more negative than the robbery
   route decomposition;
4. the sign survives the >=10-event sensitivity.

The permutation p-value measures evidence strength but is not the sole promotion gate.

## Allowed interpretation if supported

> A community can become more cheater dominated while interaction flux contracts.
> Conditional cheating prevalence can therefore rise because the mutualistic route is
> disappearing faster than exploitation is increasing.

A stronger conceptual formulation, allowed only if the independent cross-fit result is
supported:

> **topological or compositional expansion of cheating can coexist with quantitative
> contraction of interaction flux.**

## Prohibited claims

- that robbery never increases in absolute terms;
- that all high-cheating systems are collapsing mutualisms;
- that the cross-fit association is causal;
- that lower visitation necessarily means lower plant fitness;
- using the within-sample mathematical coupling between a proportion and its
  denominator as evidence;
- changing the waypoint split, event minimum, denominator, or route coding after
  opening the outcome.
