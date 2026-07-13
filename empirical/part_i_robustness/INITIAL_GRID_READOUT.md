# Initial Part I qualitative sensitivity-grid readout

## Run identity

```text
config:  configs/part_i_robustness_grid.json
runner:  scripts/run_part_i_robustness.py
run id:  initial_qualitative_grid_v1
```

The initial grid contains 162 local phenotype/regime cases:

```text
A = 0.2, 0.5, 0.8
D = 0.2, 0.5, 0.8
R = 0.0, 0.5
P = 0.2, 0.5, 0.8
H = 0.2, 0.5, 0.8
```

Each case is evaluated under four biological parameter scenarios and four functional-form variants, yielding **2,592 local mixed-partial evaluations**.

## Why two sensitivity summaries are needed

A different response curve is not the same uncertainty as a different biological scenario. The run therefore separates:

```text
within scenario:
  does the sign remain the same across the four tested response curves?

across scenarios:
  does the sign remain the same after changing interaction tracking,
  pollination obstruction, and direct joint cost?
```

The first is sensitivity to the selected functional-form family. The second is a broad biological parameter envelope. Neither is a proof of mathematical structural robustness.

## Result 1: tested functional-form agreement within a fixed scenario

Across the 648 `case × parameter scenario` summaries:

```text
395  tested_set_unanimous across all four tested functional forms
253  mixed_or_sensitive across functional forms
  0  conditional_majority
```

For many fixed biological parameter settings, the local sign is preserved when attraction benefit saturates, defence efficacy saturates, and joint cost curves. This supports stability across the four predeclared forms only; it does not establish invariance to every admissible response function.

## Result 2: the full biological parameter envelope remains conditional

Across the 162 local cases after combining all four deliberately contrasting biological scenarios:

```text
  0  tested_set_unanimous across the full tested envelope
 27  conditional_majority
135  mixed_or_sensitive
```

This is the central first result. The model does **not** support an unconditional claim that floral attraction and floral barrier traits are generally complementary or generally substitutable. The sign changes when the biologically decisive quantities change.

## Scenario-specific signatures

### High antagonism tracking, low pollination obstruction, low joint cost

```text
162 / 162 cases have complementary modal sign
130 / 162 are unanimous across the four tested functional forms
```

This is the expected complementarity regime within the tested model family: attraction carries antagonism risk, barrier efficacy suppresses that risk, and the barrier imposes little pollination cost.

### High pollination obstruction and high joint cost

```text
147 / 162 cases have substitutable modal sign
135 / 162 are unanimous across the four tested functional forms
```

This is the expected substitutability regime within the tested model family: any floral barrier benefit is overwhelmed by access obstruction and direct joint cost.

### Baseline and low-tracking scenarios

Both produce mixed complementary/substitutable regions and many functional-form-sensitive cases. These are regions where empirical information about channel magnitudes would be especially consequential, but the current route-level literature layer does not calibrate those magnitudes.

## What this permits in the manuscript

It permits the claim:

> Within the declared model family, complementarity occurs when antagonist relief exceeds mutualist interference and direct joint cost, whereas substitutability occurs when the opposing contributions dominate. The boundary is conditional and parameter sensitive.

It does not permit the claims:

> Floral attraction and defence universally trade off, universally coevolve positively, or have a sign that is structurally robust to all possible model formulations.

## Empirical boundary

The retained literature layer currently supports only route-level mechanism plausibility. In particular, flower-associated defence/barrier traits can reduce pollinator use in some systems. Those records do not estimate the complete focal-pair mixed partial, its environmental derivative, or the parameter magnitudes used in this sensitivity grid.

The direct joint-cost term `c_AD` therefore remains a scenario parameter unless independent allocation or construction-cost evidence is supplied for a concrete focal trait pair.
