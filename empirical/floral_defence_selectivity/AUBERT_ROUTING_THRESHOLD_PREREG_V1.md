# Aubert / EPHI routing-threshold preregistration v1

## Status

~~~text
STATUS = FROZEN_BEFORE_THRESHOLD_EFFECT
PRIMARY_DATA = AUBERT_EPHI_259_PLANT_SPECIES
PRIMARY_UNIT = PLANT_SPECIES
ROUTING_DIRECTION = ALREADY_FROZEN_POSITIVE
THRESHOLD_RESULT = NOT_YET_OPENED
~~~

This analysis asks whether the already established positive mismatch-routing
association contains a **location prediction**: does the steepest change in robbery
occur near tube length = bill length?

No pair-site or raw interaction row is promoted back to an inferential replicate.
The same 259 plant-species points used in the robust cross-network routing analysis
are used here with equal plant-species weight.

## 1. Primary sigmoid threshold

For plant species (i), let:

~~~text
M_i = mean log(tube / bill) across its pair-site rows
Y_i = mean robbery rate across its pair-site rows
~~~

Fit the bounded four-parameter sigmoid:

[
hat Y_i
=
L + (U-L)
left[
1+exp{-k(M_i-x^*)}
ight]^{-1},
]

with:

~~~text
0 <= L <= U <= 1
k > 0
~~~

The primary estimand is (x^*), the mismatch value at maximum slope.

The fit uses unweighted least squares across plant species so the threshold analysis
retains the current plant-species inferential grain.

The search for (x^*) is restricted to the observed 5th-95th percentile mismatch
interval. The slope search is restricted to:

~~~text
0.25 <= k <= 20
~~~

A transition is considered meaningful only if:

~~~text
U - L >= 0.10
~~~

If the optimum is at the threshold-search boundary, the result is classified as
support-boundary limited rather than as an interior threshold.

## 2. Equality-location prediction

The point prediction is tube length approximately equal to bill length:

~~~text
M = log(tube / bill) = 0
~~~

Before opening the result, define a practical proximity margin corresponding to
tube/bill ratios between 0.8 and 1.25:

[
|x^*| le log(1.25) = 0.22314355.
]

Uncertainty is a 999-replicate nonparametric bootstrap over plant species.
The primary location decision uses the 90% percentile bootstrap interval.

Frozen classes:

~~~text
THRESHOLD_NEAR_EQUALITY
    90% CI(x*) lies wholly inside [-log(1.25), +log(1.25)]

THRESHOLD_BELOW_EQUALITY
    90% CI upper bound < -log(1.25)

THRESHOLD_ABOVE_EQUALITY
    90% CI lower bound > +log(1.25)

THRESHOLD_LOCATION_UNRESOLVED
    stable interior sigmoid fit, but none of the above

THRESHOLD_AT_SUPPORT_BOUNDARY
    optimum lies at the 5th/95th percentile search boundary

NO_MEANINGFUL_SIGMOID_TRANSITION
    fitted amplitude U-L < 0.10
~~~

A CI that merely includes zero is **not** treated as evidence that the threshold is
near equality.

The linear and sigmoid residual SSE and Gaussian working AIC are reported as model
adequacy diagnostics only; model comparison does not alter the frozen location
classification.

## 3. Secondary upper-turnover diagnostic

The proposed ecological window predicts that extreme mismatch could eventually make
the flower unprofitable even through bypass.

This is tested separately from the sigmoid threshold.

Fit equal-weight plant-species models:

~~~text
linear:    Y = a + b M
quadratic: Y = a + b M + c M^2
~~~

Calculate the SSE improvement of the quadratic over the linear model. Test that
improvement with 9,999 permutations of plant-species robbery rates across fixed
mismatch values.

Define an interior upper-turnover signal only when all are true:

1. quadratic curvature (c<0);
2. curvature-improvement permutation (p<0.05);
3. the quadratic vertex lies between the observed 10th and 90th percentiles of
   mismatch;
4. the fitted derivative at the 90th percentile is negative.

Classes:

~~~text
INTERIOR_UPPER_TURNOVER_SUPPORTED
CURVATURE_WITHOUT_INTERIOR_TURNOVER
NO_DETECTED_UPPER_TURNOVER
~~~

This diagnostic is secondary and cannot override the already established positive
routing association.

## 4. Bootstrap and computation rules

~~~text
bootstrap replicates = 999
curvature permutations = 9,999
random seed = 20261003
plant species = resampling/permutation unit
~~~

The sigmoid fit is deterministic for a fixed dataset. A coarse grid is followed by
bounded local pattern refinement. Bootstrap fits start from the frozen full-data
solution and use the same parameter bounds.

At least 90% of bootstrap replicates must yield finite threshold fits. Otherwise the
location class is withheld as `BOOTSTRAP_THRESHOLD_UNSTABLE`.

## 5. Manuscript language gate

If `THRESHOLD_NEAR_EQUALITY` is recovered, the Letter may state that the steepest
observed routing transition is localized near tube-bill equality under the frozen
sigmoid model.

If the threshold is displaced, report its direction and interval without redefining
the proximity margin.

If location is unresolved or boundary-limited, retain the monotonic routing result
and state that the data do not localize a threshold.

If upper turnover is supported, describe it as evidence for an interior peak in the
observed robbery-mismatch relation, not as proof of abandonment or causal mechanism.

If no turnover is detected, state only that the upper boundary of the proposed
window was not detected over the observed mismatch range.

## 6. Claim boundary

This is an observational shape analysis of the same Ecuadorian routing dataset.
Even a threshold near zero does not establish that morphology causally switches
behaviour. The prospective artificial-flower experiment remains the causal test.
