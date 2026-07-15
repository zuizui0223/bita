# Part I sensitivity readout v2

## Run identity

```text
config:  configs/part_i_robustness_grid.json
runner:  scripts/run_part_i_robustness.py
run id:  endpoint_normalized_grid_v2
```

The declared finite design contains 162 local cases:

```text
A = 0.2, 0.5, 0.8
D = 0.2, 0.5, 0.8
R = 0.0, 0.5   # auxiliary background moderator only
P = 0.2, 0.5, 0.8
H = 0.2, 0.5, 0.8
```

Each local case is evaluated under four biological parameter scenarios and four endpoint-normalized response-shape variants, yielding **2,592 local mixed-partial evaluations**.

`R` is not a third focal trait. It is retained only as an auxiliary moderator of the pollination-mediated channel in the implemented corollary.

## Numerical zero convention

```text
neutral_tolerance = 1e-10
neutral_tolerance_scale = absolute_on_declared_score_scale
minimum_absolute_mixed_partial = 1.7318900435991935e-06
neutral_evaluation_count = 0
near_tolerance_evaluation_count = 0
```

The tolerance is a floating-point classification threshold on the declared score scale, not a biologically invariant neutrality band.

## Endpoint normalization

The four tested response shapes share the declared endpoint scales on `A,D in [0,1]`:

```text
attraction response at A=1       matched across variants
defence response at D=1          matched across variants
joint-cost scale at A=D=1        matched across variants
```

This reduces confounding between response-shape sensitivity and a simple change in endpoint effect magnitude. It does not prove structural robustness.

## Overall sign counts

```text
1342  complementary  (51.8%)
1250  substitutable  (48.2%)
   0  neutral
```

These percentages are **unweighted occupancy fractions of the declared finite grid**. They are not empirical probabilities or estimates of prevalence in nature. Changing the grid measure can change the percentages.

## Response-shape agreement within fixed biological scenarios

Across 648 `case × parameter scenario` summaries:

```text
480  tested_set_unanimous
168  mixed_or_sensitive
```

`modal_sign_agreement` remains available as a continuous descriptive quantity. No arbitrary majority threshold is promoted into a separate robustness class.

## Agreement across the full finite tested set

Across the 162 local cases after combining all four deliberately contrasting biological scenarios and all four response shapes:

```text
  0  tested_set_unanimous
162  mixed_or_sensitive
```

This is expected for a conditional-regime theory: changing the biologically decisive route strengths can change the local sign.

## Scenario-specific signatures

Exact complementary/substitutable ties across the four response shapes are reported as `mixed`.

### High antagonism tracking, low pollination obstruction, low joint cost

```text
149 / 162 cases have complementary modal sign
 13 / 162 are mixed ties
144 / 162 are unanimous across the four tested response shapes
617 / 648 individual evaluations are complementary (95.2%)
```

### High pollination obstruction and high joint cost

```text
150 / 162 cases have substitutable modal sign
  2 / 162 have complementary modal sign
 10 / 162 are mixed ties
138 / 162 are unanimous across the four tested response shapes
610 / 648 individual evaluations are substitutable (94.1%)
```

### Baseline

```text
65 complementary modal cases
56 substitutable modal cases
41 mixed ties
97 tested_set_unanimous cases
344 / 648 individual evaluations are complementary
304 / 648 individual evaluations are substitutable
```

### Low-tracking, low-obstruction, low-joint-cost scenario

```text
66 complementary modal cases
58 substitutable modal cases
38 mixed ties
101 tested_set_unanimous cases
343 / 648 individual evaluations are complementary
305 / 648 individual evaluations are substitutable
```

## Manuscript-facing interpretation

The implemented corollary permits the following claim:

> Within the declared model family and score parameterisation, local complementarity occurs when antagonist relief exceeds mutualist interference and direct joint-cost curvature, whereas local substitutability occurs when the opposing contributions dominate. The boundary is conditional and parameter sensitive.

It does not permit the claims that attraction and defence universally trade off, universally coevolve positively, or have a sign that is invariant to all model formulations or arbitrary outcome transformations.

## Literature boundary

The retained literature registry is preliminary context only. The current abstract-level records do not identify the focal `M_AD` curvature, estimate the complete focal-pair mixed partial, calibrate the model parameters, or validate the regime map in nature.
