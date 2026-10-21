# Integration update: distinguish informational limits from physical limits of shared traits

Date: 2026-10-20. Status: **newly executed mathematical robustness analysis; no new empirical or historical-origin evidence**. Companion to `TRADEOFF_TO_EVOLVED_ARCHITECTURE_CAUSAL_SYNTHESIS_V1.md`. The active BITA Letter, empirical data, and independent BALANCE V4 coding are unchanged.

## Current conclusion

The central question remains whether functional trade-offs historically caused new trait structures to originate. Today's result improves the *architecture-value* step, not the historical-origin step:

> A fixed differentiated structure can appear advantageous merely because the shared phenotype was denied realistic memory. But irreducible simultaneous functional demands plus physical switching costs can also make differentiation intrinsically advantageous even against an arbitrarily informed shared phenotype.

The complete proof, implementation and reproducible synthetic results are in [PAYOFF's history robustness note](https://github.com/zuizui0223/payoff/blob/9073d44be94f0ffcfb8a856e05f1c0dc97958c11/theory/HISTORY_AWARE_COMPROMISE_ROBUSTNESS_V1.md), on [PAYOFF PR #338](https://github.com/zuizui0223/payoff/pull/338).

## What changed and what did not

The earlier `rho*=0.65625` threshold is still correct for its original memoryless cue-response policy. It is **not** a general threshold for all reversible responses or for structural evolution. The original example at `rho=.9, K=3.8` still favors fixed modules over all calculated deterministic cue-window mappings up to six cues; the unrestricted comparison is bracketed but **unresolved**, not disproved.

The new analysis uses two complementary objects, with opposite inequality directions:

1. An explicit finite-history plastic policy supplies an **upper bound** on the best possible shared-coordinate loss. Every deterministic mapping of up to six cues is optimized as a convex problem; primal–dual gaps verify finite-class numerical precision.
2. A pointwise two-period relaxation supplies a **lower bound** even when the controller knows the complete future. No limited-memory assumption is used for that inequality.

### A true memory counterexample, separately labeled synthetic parameters

At `rho=.1, K=3.55`, holding `a=3, b=1, Delta=2, q=.9, B=.05, c=1` fixed, the original one-cue loss is `3.590316`, which would favor fixed modules. A simple two-cue posterior policy has loss `3.499824220`; optimizing all two-cue mappings improves it to `3.493508431`. Both beat the fixed architecture. Even the simpler policy can pay an additional memory cost below `0.050175780` and retain its advantage.

These are invented model parameters, not a claim about measured animal cognition or plant memory costs. The new K is not silently substituted for the original K=3.8 witness.

### A stronger positive result, not dependent on poor plastic control

In the same quadratic physics, write `C` for the simultaneous shared-coordinate conflict floor, `T` for cross-environment mismatch of the constant phenotype, and `psi(c)` for the minimum pairwise mismatch-plus-switching cost when the environmental target changes. For every admissible dynamic shared phenotype,

```
J_dynamic >= C+B+rho*psi(c).
J_best_nonmodule >= min(C+T, C+B+rho*psi(c)).
```

This is a model-conditional **all-action-sequence bound**, including perfect prediction; it is not the result of searching a finite policy library.

A separate witness uses `K=3.6`. At `rho=.1`, a known plastic response costs `3.590316 < 3.6`. At `rho=.9`, all shared-coordinate responses cost at least `3.725`, whereas fixed modules cost `3.6`. Therefore turnover can reverse the ranking even after removing the artificial memory restriction. For this witness `rho>11/15` is a sufficient bound, not an exact universal transition point.

### Switching frequency is different from unpredictability

At `rho=1`, environments alternate deterministically. Informative noisy cues can reveal the phase through accumulated observations. Under zero additional memory cost, the unrestricted asymptotic plastic loss equals `3.8` in the original witness and therefore ties the module. The memoryless value `3.8979` is not the unrestricted optimum.

## Implications for the four-repository research design

| Role | Required distinction after this update |
|---|---|
| SCH | Identify actual simultaneous opposing functional demands on one trait, rather than substituting environmental contrasts or multifunctionality. |
| BALANCE | Compare differentiation with the best admissible fixed **or reversibly adjustable** shared phenotype, not only a rigid compromise. |
| PAYOFF / SLK | Separate bounds on intrinsic architecture value from genetic accessibility, rare invasion, fixation and occupancy. SLK retains canonical value ownership. |
| BITA | Determine which ecological pathways generate the demand and switching burden. A statistical interaction residual is not automatically the physical switching cost. |

Independent macroecological pattern recovery remains the primary empirical direction. The quantities to distinguish are concurrent functional demand, cue reliability/predictability, physical switching burden, and actual structural organization. Different population sex labels or a plastid haplotype are not substitutes for those variables. Wurmbea's phenotypic reversibility motivates the comparator question, but its published 66%/42% responses and 3.7/1.4 seed ratios are **not fitted parameters here**.

## Remaining causal boundary

Fixed modules in this model simultaneously perform both functions within one individual. This is not automatically a model of dioecy, collective division of labor, or fixed male/female genetic inheritance. No mutation process, developmental realization, nuclear inheritance, population establishment or dated origin was estimated. The historical claim that trade-offs caused new structures remains untested.

Thirty new local tests passed before committing the extension; GitHub checks independently run them together with the original model's tests. Neither local nor CI success is biological validation. The earlier theoretical result is preserved, and this note supplies its stronger robustness test and explicit limits.
