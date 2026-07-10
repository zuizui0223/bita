# *Impatiens capensis* empirical results lock v1

## Purpose

This file freezes the empirical interpretation after PR #103. It is a writing and
claim-boundary document, not a new analysis. No new definitions, parameters, or
post-hoc hypotheses are introduced here.

```text
primary empirical system:  Impatiens capensis
primary role:              single-system empirical core / case-study constraint
literature synthesis role: evidence map and generalisation boundary
not claimed:               universal pooled parameter values
not claimed:               direct empirical estimate of the Part A mixed partial
not claimed:               c_AD calibration
```

## Fixed empirical readout

### Response-scale channel map

The response-scale models use the archived measurement units rather than forcing all
responses into a standardized Gaussian screen.

```text
P: 60-minute-standardized pollinator visit count/rate
H: individual-flower natural tissue-loss fraction
seed component: individual CH-fruit seed count
```

Main channel results:

```text
A: early flower redness -> pollinator use
  RR 0.981 [0.626, 1.539]
  status: unresolved observational association

D candidate: log1p early floral tannins -> pollinator use
  RR 0.682 [0.479, 0.972]
  status: directionally consistent observational pollination cost

A: early flower redness -> natural floral damage
  OR 1.064 [0.933, 1.213]
  status: unresolved observational association

D candidate: log1p early floral tannins -> natural floral damage
  OR 1.121 [0.990, 1.269]
  status: no resolved protective association

A × D candidate -> seeds per CH fruit
  RR 1.008 [0.968, 1.049]
  status: unresolved component surface
```

### Pollinator-rate adequacy sensitivity

The primary pollinator-rate model has many zero observations and high overdispersion
(52 zero-visit plants among 81 complete plants; Pearson dispersion 23.18). The
post-primary hurdle sensitivity is therefore used only to diagnose whether the
pollinator association is concentrated in visit presence, positive intensity, or
both.

```text
Any visit observed, D candidate:
  OR 0.780 [0.511, 1.191]
  status: unresolved

Positive visit intensity conditional on at least one visit, D candidate:
  RR 0.515 [0.332, 0.799]
  status: directionally consistent among visited plants
```

Interpretation: the primary `D -> P` cost signal is compatible with lower positive
visit intensity among plants that receive at least one visit. This sensitivity does
not replace the primary model and must not be used for selective reporting.

### Randomized downstream reproductive effects

The randomized supplemental `Robbing × Florivory × Pollination` design is complete:
all eight assignment cells have 25 plants in the processed table. The factorial
models retain all main effects, all pairwise interactions, the three-way
interaction, and pre-treatment phenology.

```text
Supplemental florivory -> CH fruits per plant per day
  standardized factorial coefficient -0.290 [-0.540, -0.040]
  status: directionally consistent randomized reproductive-component cost

Supplemental florivory -> seeds per CH fruit
  standardized factorial coefficient -0.142 [-0.622, 0.338]
  status: unresolved component effect

Phenology -> CH fruits per plant per day
  standardized coefficient -0.493 [-0.617, -0.369]
  status: strong phenology association with fruit production
```

Interpretation: the experiment supports a downstream cost of imposed florivory on CH
fruit production. It does not show that early flower redness or floral tannins cause
that cost.

## Theory mapping

The current *Impatiens* evidence maps onto Part A as follows.

```text
b_A: A -> pollinator use
  unresolved in this panel.

c_D: D candidate -> pollinator use
  supported as an observational cost-like association.
  Not a causal tannin manipulation.

d_A: A -> floral antagonism
  unresolved in this panel.

e_F: D candidate -> floral antagonism suppression
  not supported/resolved for this D candidate.
  The point estimate is not protective.

A × D reproductive component
  unresolved for seeds per CH fruit.

H -> reproductive component
  supported experimentally only for imposed florivory -> CH fruits/day.
```

Therefore, this system does **not** empirically establish complementarity or
substitutability. It constrains the theory by showing that one cost-like side
(`D -> P`) is visible in the observational channel map, while the corresponding
protective benefit (`D -> H suppression`) is not resolved; separately, experimentally
imposed florivory reduces a reproductive component.

## Manuscript-ready result statement

A concise Results paragraph can say:

> In the *Impatiens capensis* panel, the floral-tannin candidate showed a negative
> association with pollinator use on the response scale of the archived observation
> data (RR = 0.682, 95% CI 0.479–0.972 per 1 SD increase in log1p tannins). This
> association was not matched by a resolved protective association with natural
> floral damage (OR = 1.121, 95% CI 0.990–1.269). Flower redness was not resolved as
> a predictor of either pollinator use or natural floral damage, and the A × D
> candidate surface for seeds per chasmogamous fruit was also unresolved (RR = 1.008,
> 95% CI 0.968–1.049). In contrast, the randomized factorial treatment analysis
> showed that imposed florivory reduced chasmogamous fruit production (standardized
> coefficient = -0.290, 95% CI -0.540 to -0.040), while phenology showed a strong
> association with fruit production (standardized coefficient = -0.493, 95% CI
> -0.617 to -0.369).

## Manuscript-ready interpretation statement

A concise Discussion paragraph can say:

> The *Impatiens* case study supports an asymmetric constraint on the attraction–
> defence framework. The floral-tannin candidate is associated with a pollination
> cost, but the expected antagonism-suppression benefit is not resolved. Thus, the
> system provides empirical support for one side of the theoretical trade-off but
> does not identify the full complementarity/substitutability regime. The randomized
> treatment result confirms that floral damage can reduce a reproductive component,
> but it does not imply that naturally varying tannins or flower colour caused that
> damage gradient. The safest interpretation is therefore a single-system empirical
> constraint: defence-like chemistry may carry a pollination cost, but its defensive
> benefit and its interaction with attraction require direct manipulation or stronger
> linked observational evidence.

## Claims that must not be made

```text
Do not claim that floral tannins causally reduce pollinator visitation.
Do not claim that floral tannins protect against natural florivory in this panel.
Do not claim a total lifetime-fitness result.
Do not claim an empirical estimate of the Part A mixed partial.
Do not claim complementarity or substitutability was directly observed.
Do not multiply coefficients across pollinator, florivory, and fitness models.
Do not use the hurdle sensitivity to replace the primary pollinator-rate model.
```

## Next writing target

The next step should be a manuscript skeleton that uses this lock as the Results and
Discussion source of truth:

```text
1. Theory: fixed Part A condition.
2. Evidence map: literature synthesis explains why universal pooled parameters are not available.
3. Empirical core: Impatiens response-scale channel map and randomized downstream cost.
4. General conclusion: conditional framework remains plausible, but empirical identification is partial.
```
