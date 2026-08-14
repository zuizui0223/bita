# Kessler 2008 direct-factorial sign robustness audit v1

## Purpose

Determine how far the published aggregate information in Kessler et al. 2008 (`10.1126/science.1160072`) can identify the sign of an attraction-by-defence factorial effect without inventing unavailable cell-level uncertainty.

This is a **sensitivity reconstruction**, not a replacement analysis of the original data.

## Published design facts

The field experiment independently blocked the dominant floral attractant benzylacetone (`A`) and nicotine production (`D` candidate) in all four combinations:

```text
EV    A+, D+
PMT   A+, D-
CHAL  A-, D+
CP    A-, D-
```

For female outcrossing, the source reports:

```text
601 antherectomized flowers across 5 experimental days
127 flowers on one wind-only day -> 0 capsules and no active pollinators
474 flowers on the remaining 4 informative days
87 mature capsules from those 474 flowers before later losses
EV capsule production averaged ~35%
PMT, CHAL, CP each averaged ~12-14%
```

The source also states that the number of seeds per matured capsule did not differ among genotypes, making capsule maturation from pollinator-mediated outcrossing the relevant female-function contrast.

## Discrete interaction on the probability scale

For cell probabilities `p11, p10, p01, p00`, define the descriptive 2x2 interaction contrast

```text
Delta = p11 - p10 - p01 + p00
```

Using `p11 = 0.35` and allowing each low cell independently anywhere in the source-reported `0.12-0.14` range gives:

```text
minimum Delta = 0.19
maximum Delta = 0.25
```

Thus the sign of the rounded probability-scale interaction is positive throughout the published low-cell range.

## Logit-scale interaction sensitivity

For a binomial factorial model, the corresponding cell-probability interaction is

```text
beta_AD = logit(p11) - logit(p10) - logit(p01) + logit(p00)
```

Again using `p11 = 0.35` and independently varying the three low cells from `0.12` to `0.14` gives:

```text
beta_AD range      +1.019 to +1.551
interaction OR     2.77 to 4.71
all-low-at-0.13    beta_AD = +1.282; OR = 3.60
```

Therefore the **published rounded aggregate state is sign-robustly positive on both the probability and logit scales**.

## Integer-allocation stress test

The exact day-by-genotype denominators are not available in the accessible main article. To test whether plausible integer allocation can reverse the logit interaction, enumerate integer cell denominators constrained to:

```text
sum n = 474 informative flowers
sum successes = 87 capsules
EV success proportion rounds to ~35%
PMT/CHAL/CP success proportions each lie within ~12-14%
cell denominators remain in a broad balanced-field range compatible with the reported design
```

Across all feasible allocations under these deliberately broad constraints, the fitted four-cell logit interaction remains positive. The minimum reconstructed coefficient is still positive. However, the corresponding Wald z statistic varies enough that formal statistical significance is **not allocation-robust**.

This means:

```text
factorial sign:          robustly positive given published aggregate constraints
formal significance:    unresolved without exact denominators / day structure
source interaction SE:  unavailable
```

The enumeration is a robustness diagnostic only. It must not be presented as recovered original data.

## Biological gate

The source independently establishes that:

- benzylacetone increases pollinator visitation;
- nicotine in flowers/nectar changes floral visitor behaviour and reduces nectar robbery / florivory;
- both axes were crossed in one field experiment;
- female outcrossing and male siring were jointly highest in the `A+,D+` state.

But `Napmt1/2` silencing is systemic, even though nectar nicotine is a focal floral phenotype. Thus the intervention is not cleanly restricted to a flower-specific `D` coordinate, and non-floral nicotine effects cannot be excluded from plant-level fitness.

## Adjudication

Kessler 2008 is promoted one step from a generic near miss:

```text
DIRECT_FACTORIAL_SIGN_POSITIVE
SIGN_ROBUST_TO_PUBLISHED_AGGREGATE_RANGE
FORMAL_INTERACTION_UNCERTAINTY_UNRESOLVED
FLOWER_SPECIFIC_INTERVENTION_GATE_NOT_FULLY_CLEAN
```

It is valid evidence that a direct attraction-by-defence-like factorial can produce a positive joint reproductive response. It is **not yet** a clean local estimate of the manuscript's `W_AD`, and it does not identify `rho`, `iota`, or `kappa` separately.

## Inference boundary

```text
positive 2x2 factorial contrast != universal W_AD > 0
rounded aggregate sign robustness != source-reported interaction test
systemic nicotine silencing != perfectly isolated floral D intervention
joint reproductive response != kappa
```