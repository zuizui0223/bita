# Initial Part I qualitative sensitivity-grid readout

## Run identity

```text
config:  configs/part_i_robustness_grid.json
runner:  scripts/run_part_i_robustness.py
run id:  initial_qualitative_grid_v1
```

The grid contains 162 local phenotype/regime cases:

```text
A = 0.2, 0.5, 0.8
D = 0.2, 0.5, 0.8
R = 0.0, 0.5
P = 0.2, 0.5, 0.8
H = 0.2, 0.5, 0.8
```

Each case is evaluated under four biological parameter scenarios and four endpoint-normalized response-shape variants, yielding **2,592 local mixed-partial evaluations**.

The numerical zero rule is:

```text
neutral_tolerance = 1e-10
neutral_tolerance_scale = absolute_on_declared_score_scale
```

This is a floating-point classification threshold on the declared score scale, not a biologically invariant neutrality band.

## Why two sensitivity summaries are needed

A different response shape is not the same uncertainty as a different biological scenario. The run therefore separates:

```text
within scenario:
  does the sign remain the same across four endpoint-normalized response shapes?

across scenarios:
  does the sign remain the same after changing interaction tracking,
  pollination obstruction, and direct joint-cost scale?
```

The response-shape variants share the same declared endpoint scales on `A,D in [0,1]`. This reduces the earlier confounding between changing curve shape and simply changing endpoint effect magnitude. Neither sensitivity summary is a proof of mathematical structural robustness.

## Result 1: tested response-shape agreement within a fixed scenario

Across the 648 `case × parameter scenario` summaries:

```text
480  tested_set_unanimous across all four tested response shapes
168  mixed_or_sensitive across response shapes
  0  conditional_majority
```

For many fixed biological parameter settings, the local sign is preserved when attraction and defence responses saturate and joint cost curves while endpoint scales are held comparable. This supports stability across the four predeclared response shapes only; it does not establish invariance to every admissible biological function.

## Result 2: the full biological parameter envelope remains conditional

Across the 162 local cases after combining all four deliberately contrasting biological scenarios:

```text
  0  tested_set_unanimous across the full tested envelope
 42  conditional_majority
120  mixed_or_sensitive
```

The model therefore does **not** support an unconditional claim that floral attraction and floral barrier traits are generally complementary or generally substitutable. The sign changes when the biologically decisive route strengths change.

## Overall evaluation counts

```text
1342  complementary  (51.8%)
1250  substitutable  (48.2%)
```

Both regimes remain well represented after endpoint normalization.

## Scenario-specific signatures

Exact complementary/substitutable ties across the four response shapes are reported as `mixed`, not assigned to complementarity.

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
```

### Low-tracking, low-obstruction, low-joint-cost scenario

```text
66 complementary modal cases
58 substitutable modal cases
38 mixed ties
101 tested_set_unanimous cases
```

These explicit tie counts correct the earlier implementation bias that resolved exact modal ties in favour of complementarity.

## What this permits in the manuscript

It permits the claim:

> Within the declared model family and score parameterisation, complementarity occurs when antagonist relief exceeds mutualist interference and direct joint-cost curvature, whereas substitutability occurs when the opposing contributions dominate. The boundary is conditional and parameter sensitive.

It does not permit the claims:

> Floral attraction and defence universally trade off, universally coevolve positively, or have a sign that is structurally robust to all possible model formulations or invariant to arbitrary trait and fitness transformations.

## Empirical boundary

The retained literature layer currently provides only abstract-level route evidence. One predeclared three-cluster manipulation stratum is directionally consistent with flower-associated chemical barriers reducing pollinator preference or foraging. Those records do not identify the focal `M_AD` curvature, estimate the complete focal-pair mixed partial, or calibrate the parameter magnitudes used in this sensitivity grid.

The direct joint-cost term therefore remains a scenario quantity unless independent allocation or construction-cost evidence is supplied for a concrete focal trait pair and outcome scale.
