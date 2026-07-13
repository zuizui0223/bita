# Theory and simulation specification

## Objective

Identify when floral attraction and flower-specific defence/access limitation are **locally complementary versus locally substitutable in fitness**, without assuming a trade-off in advance and without treating the first model as an empirically calibrated evolutionary prediction.

## Active empirical interpretation

```text
A = A_flower: floral display, nectar guide, flower size, nectar reward, orientation
D = B_flower: flower-specific defence or pollinator-access restriction
```

Examples of `D` include floral chemical deterrents, trichomes, spines, sticky structures, and other barriers measured on the attacked or visited flowering organ. Leaf toughness, LDMC, leaf chemistry, and stem resistance are not automatically observations of `D` in the active A--D result.

The current score retains reproductive assurance `R` as a theoretical sensitivity term. It is varied in sensitivity analyses, but it is not part of the theorem-level novelty and no active empirical module calibrates it.

## Theorem-level sign criterion

The primary result is the general local decomposition

\[
W(A,D)=M(A,D)-G(A,D)-C(A,D),
\]

so that

\[
W_{AD}=M_{AD}-G_{AD}-C_{AD}.
\]

Under the biological orientation used here, this becomes

```text
local A x D interaction
= antagonist relief
- mutualist interference
- direct joint cost.
```

Therefore attraction and defence are locally complementary only when the antagonist-relief contribution exceeds the sum of mutualist interference and direct joint cost.

This criterion is implemented in `trait_architecture/sign_criterion.py` and documented in `docs/GENERAL_SIGN_CRITERION.md`.

## Baseline model as a corollary

For the implemented score,

\[
\frac{\partial^2 W}{\partial A\,\partial D}
=
H d_A e_F
- P b_A c_D e^{-c_DD}(1-c_RR)
- c_{AD}.
\]

The terms map directly onto the general criterion:

```text
H d_A e_F                                  antagonist relief
P b_A c_D exp(-c_D D) (1 - c_R R)         mutualist interference
c_AD                                       direct joint cost
```

A positive value is **local fitness complementarity**: increasing defence raises the marginal fitness return to attraction. A negative value is **local fitness substitutability**: increasing defence lowers that marginal return.

These are curvature statements about the score surface. They are not empirical covariance predictions, genetic correlations, or evolutionary endpoints.

## Robustness analysis

The numerical sweep varies selected response-function curvature and parameter values around the baseline corollary. Its purpose is to ask whether the sign of the local mixed partial is stable within a declared family of models.

The grid is therefore a sensitivity analysis, not the proof of the general criterion and not an empirical frequency distribution over nature.

## Falsifiable model-family predictions

1. Mutualist interference pushes the local interaction toward substitutability when defence reduces the pollination return to attraction.
2. Antagonist relief pushes the local interaction toward complementarity when antagonists track attraction and defence reduces the resulting damage.
3. Direct shared cost pushes the local interaction toward substitutability independently of mutualist interference.
4. A sign switch occurs at the explicit break-even boundary where antagonist relief equals mutualist interference plus joint cost.
5. Positive or negative covariance among simulated optima is a separate, model-dependent result and must not be inferred directly from the mixed partial.

## Link to literature evidence

The literature layer currently supports a narrower statement: a defence/access -> pollination cost exists in at least some systems. That evidence supports the biological existence of the mutualist-interference pathway.

It does not establish the complete sign of `W_AD` in those systems because antagonist relief and direct joint cost are not jointly estimated on a common scale.
