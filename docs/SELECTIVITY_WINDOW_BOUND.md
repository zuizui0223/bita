# The selectivity window is a one-sided bound, not a universal criterion

This document answers a specific question: **is "effective-domain separation / selectivity window"
the minimal universal law governing whether attraction and defence are complementary?**

The answer is no, and the way it fails is more useful than the question assumed. The selectivity
window is a **strict upper bound** on complementarity — exact in one limit, never wrong in one
direction, and falsifiable by a single sign test on one parameter.

Reproduce every number here with `tests/test_selectivity_bound.py`.

## 1. The claim, stated precisely

For a declared point and parameter set, write the deployed mixed partial as the repository already
decomposes it in `trait_architecture/robustness.py`:

```text
W_AD = antagonism_term - pollination_obstruction_term - joint_cost_curvature_term
```

Define the **selectivity window** as the region where the antagonist channel outweighs the
pollinator channel, ignoring joint cost:

```text
inside the window   <=>   antagonism_term > pollination_obstruction_term
```

The claim under test is that being inside the window is what makes the traits complementary.

## 2. What is true: a one-sided theorem

> **Theorem.** If all three terms are non-negative, then `W_AD > 0` implies the point is inside the
> selectivity window. Equivalently: **complementarity never occurs outside the window.**

Proof, in one line. If `W_AD > 0` then
`antagonism_term - pollination_obstruction_term = W_AD + joint_cost_curvature_term > 0`,
since `joint_cost_curvature_term >= 0`. So `antagonism_term > pollination_obstruction_term`. ∎

Two things make this stronger than it looks.

**It is form-independent.** All four declared endpoint-normalized response-shape variants —
`baseline`, `saturating_attraction`, `saturating_defence`, `saturating_both_curved_cost` — preserve
the `relief − interference − cost` structure with all three terms non-negative. The proof uses only
that structure, so it holds under every variant rather than only the baseline exponential form.
This is unusual in this repository: most results here are checked across the variants and come back
`mixed_or_sensitive`. This one holds by construction.

**It is exact in the zero-joint-cost limit.** With `joint_cost_curvature_term = 0` the implication
runs both ways, so the window *is* the criterion.

## 3. Verification over the declared grid

Exhaustive: 4 parameter scenarios × 54 declared grid points × 4 response-shape variants = 2592
evaluations.

| run | complementary | **false negatives** | false positives | window precision |
|---|---|---|---|---|
| declared `c_AD` | 51.8% | **0** | 397 (15.3%) | 77.2% |
| `c_AD` forced to 0 | 67.1% | **0** | **0** | **100.0%** |

*False negative* = complementary but outside the window, the observation that would break the
theorem. *Window precision* = the share of in-window points that are genuinely complementary.

The second row is not a fit. At zero joint cost the window and the criterion are the same set, and
the 100.0% is an identity. The first row is the honest operating case: the bound never misses a
complementarity, and it over-predicts one in four times.

The looseness is concentrated exactly where it should be:

```text
high_tracking_low_obstruction_low_shared_cost   0.0 - 7.4% loose
low_tracking_low_obstruction_low_shared_cost   11.7 - 20.4% loose
high_obstruction_high_shared_cost              17.3 - 34.6% loose
```

## 4. Why it cannot be the minimal law

The criterion is a **difference of two products minus an additive constant**. The selectivity window
is a **ratio**. A ratio is scale-invariant; the additive `c_AD` destroys scale invariance. So the
criterion is not homogeneous of degree zero and **cannot be reduced to any single dimensionless
group** — not by a cleverer choice of variables, and not approximately.

Sampling the declared prior box (200 000 draws, `c_AD ~ U(0,1)`) makes the cost of pretending
otherwise concrete. Best-single-threshold classification accuracy for `sign(W_AD)`:

```text
always predict "substitutable"                                   80.3%   (base rate)
selectivity  (d_A e_F) / (b_A c_D e^{-c_D D} (1 - c_R R))        80.5%   +0.2
raw discrimination  e_F / c_D                                    80.3%   +0.0
exposure ratio  H / P                                            80.3%   +0.0
affordability  -c_AD                                             80.3%   +0.0
exposure-weighted selectivity  (H·relief)/(P·interference)       82.9%   +2.6
exposure-weighted difference, no joint cost                      90.6%  +10.3
full criterion                                                  100.0%  +19.7
```

Selectivity on its own carries essentially no information about the sign. Three independent things
are in play and the window names only the first:

1. **discrimination** — can the barrier separate the two visitor classes (`e_F` against `c_D`)
2. **exposure** — are both classes present at rates that make separation matter (`H` against `P`)
3. **affordability** — is the joint cost of holding both traits payable (`c_AD`), additive and
   therefore invisible to any ratio

Exposure is not decoration: adding it lifts the ratio form from +0.2 to +2.6, and the difference
form to +10.3. And the committed larceny synthesis shows exposure is the term that varies most
wildly in nature — 95% prediction intervals for realised antagonist cost span zero in every
stratum, with none of four declared context axes explaining it.

*(Caveat: the +0.2 figure depends on the declared prior `c_AD ~ U(0,1)`, which is itself
unmeasured. The theorem in §2 does not depend on any prior.)*

## 5. The single failure mode

The bound fails only where

```text
antagonism_term <= pollination_obstruction_term    (outside the window)
antagonism_term - pollination_obstruction_term - joint_cost_curvature_term > 0   (complementary)
```

Together these force `joint_cost_curvature_term < antagonism_term - pollination_obstruction_term <= 0`.

> **A negative joint-cost curvature is necessary for the bound to fail, and — at sufficient
> magnitude — sufficient.**

`c_AD < 0` means the two traits are *cheaper together than apart*: shared precursors, shared
regulatory machinery, one structure serving both roles. That is not an exotic possibility. The
phenylpropanoid pathway feeds both floral pigments and volatiles on the attraction side and
defensive phenolics on the defence side, so synergistic construction is a live hypothesis rather
than a formal edge case.

## 6. What this buys the empirical programme

This is the payoff, and it changes what the next experiment should be.

The general problem with testing this theory is that `W_AD` is a mixed partial: identifying it needs
a factorial design varying `A` and `D` jointly against fitness, with the channels measured
separately. Very few such studies exist. That wall stands.

**The one-sided bound routes around it.** Universality of the window reduces to a *sign test on one
parameter*:

```text
if  c_AD >= 0  for a trait pair,  the bound holds for that pair, with no factorial design required
if  c_AD <  0  is demonstrated,   the window is falsified as a universal bound
```

Measuring the **sign** of joint-cost curvature needs a 2×2 allocation design — neither trait, `A`
only, `D` only, both — scored on construction or resource cost. **No pollinators, no antagonists, no
fitness assay.** That is a greenhouse experiment, not a multi-season field factorial, and it is
enormously more tractable than measuring `W_AD` itself.

It also reframes what to claim. The defensible universal statement is one-sided:

> Complementarity does not occur outside the selectivity window.

not the two-sided

> Complementarity occurs inside the selectivity window.

The second is false on this repository's own grid 23% of the time.

## 7. Boundaries

- The theorem is about **this corollary's functional family**. It uses only that the three terms are
  non-negative and enter as `relief − interference − cost`. A model where interference can be
  negative still satisfies it (the window condition then holds automatically), but a model with a
  different additive structure is not covered.
- `c_AD >= 0` is an **assumption of the deployed parameterization**, enforced by
  `ModelParameters.__post_init__`. §5 is the statement that this assumption, not the biology, is
  what carries the bound.
- Nothing here estimates any parameter or says how often either sign occurs in nature. Grid
  fractions are unweighted occupancies of the declared finite design, per the Part I convention.
- `c_AD` currently has **zero declared strata and essentially no literature** in this repository,
  and ranks second of five by value of information. The parameter that decides whether the compact
  law holds is the one nobody has measured.
