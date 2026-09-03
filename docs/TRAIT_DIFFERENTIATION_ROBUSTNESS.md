# Trait differentiation robustness readout

## Question

Which Chapter 2 results are structural properties of a nested architecture, and which depend on the quadratic response shape?

The general theory now establishes two shape-independent statements under the declared architecture:

1. if the differentiated architecture contains the shared phenotype on its diagonal, the optimized pre-fixed-cost differentiated loss cannot exceed the best shared loss, so recoverable compromise loss `R >= 0`;
2. if residual coupling enters as `lambda c(x,y)` with `c(x,y) >= 0`, increasing `lambda` cannot increase `R`.

The numerical robustness family therefore does **not** serve as the proof of weak dominance or coupling monotonicity. It tests stricter and shape-dependent questions: whether recovery is strictly positive for nonzero functional conflict and whether larger separation between function-specific optima consistently increases the amount recoverable.

The finite family replaces quadratic losses with convex power losses:

```text
shared loss:
L_S(z) = w1 |z-theta1|^p + w2 |z-theta2|^p

differentiated pre-fixed-cost loss:
L_D0(x,y) = w1 |x-theta1|^p + w2 |y-theta2|^p
          + lambda |x-y|^q
```

where `p > 1` controls functional curvature, `q > 1` controls residual cross-talk curvature, and `lambda >= 0` is cross-talk strength. A fixed architecture cost `K` is added after optimization.

## Declared finite design

Matched-curvature grid:

```text
functional power p = 1.5, 2, 3, 4
weights (w1,w2)  = (1,1), (0.4,2), (3,0.7)
coupling lambda   = 0, 0.1, 0.5, 2, 10
optimum distance  = 0.1, 0.25, 0.5, 1, 2
architecture K    = 0 for the recoverable-loss screen
```

Total: `4 x 3 x 5 x 5 = 300` evaluations.

Additional mismatched-curvature checks use `(p,q) = (1.5,2), (2,4), (4,2)`.

The executable sweep is `scripts/analyze_trait_differentiation_robustness.py`; the machine-readable result is `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS_READOUT.json`.

## Result 1 — strict recovery throughout the declared nonzero-conflict convex family

The structural theory guarantees only `R >= 0`. The finite sweep asks whether the inequality is strict in the registered family.

At zero fixed architecture cost, all 300/300 nonzero-conflict evaluations had positive recoverable conflict loss:

```text
positive recoverable gain = 300 / 300
minimum                 ~= 4.46e-06
maximum                 ~= 2.656
```

Thus the declared convex family contains no nonzero-conflict case in which the extra trait axis is completely useless before fixed cost. This is a finite-family strictness result, not a universal theorem over arbitrary architectures.

The realized architecture decision still depends on whether the recovered amount exceeds `K`.

## Result 2 — stronger functional conflict consistently increases recoverable loss in the declared family

Across every fixed combination of response shape, functional weighting and coupling, increasing the distance between function-specific optima increased recoverable conflict loss:

```text
monotonic conflict-strength series = 60 / 60
```

Unlike weak dominance and coupling monotonicity, this optimum-distance comparison is not claimed as shape-independent. The result establishes that the intuitive quadratic prediction survives the registered convex family:

> farther-separated functional optima make differentiation more valuable, all else equal, throughout the declared design.

## Result 3 — coupling monotonicity is numerically recovered exactly where the general proposition requires it

Across every fixed combination of response shape, functional weighting and optimum distance, increasing `lambda` never increased recoverable conflict loss:

```text
monotonic coupling series = 60 / 60
```

This 60/60 result is an **implementation verification** of the structural proposition

```text
lambda2 > lambda1
=> R(lambda2) <= R(lambda1)
```

for the registered sweep. It is not the source of that proposition.

Biologically, the proposition and numerical check make the same distinction:

```text
more trait axes
!=
more functional independence.
```

A structurally differentiated phenotype can remain strongly coupled. Increasing non-negative cross-talk moves the optimum toward the shared subspace and reduces the amount available to pay for an additional module.

## Result 4 — the architecture-cost threshold is structural once recovered loss is defined

For any optimized pre-fixed-cost comparison, define

```text
R = shared optimum loss - differentiated optimum loss before K.
```

Adding a fixed architecture cost gives

```text
Delta_arch = R - K.
```

Therefore `K<R` is the exact threshold by construction. The mismatched-curvature numerical checks verify the implementation around that threshold:

```text
K = 0.9 R -> differentiated architecture preferred
K = 1.1 R -> shared architecture preferred
```

for all three `(p,q)` combinations tested.

The numerical result is a regression check; the one-for-one subtraction of a fixed `K` is algebraic.

## Claim ceiling

The combined structural and finite-family result supports:

> A nested differentiated architecture weakly enlarges the attainable phenotype set before fixed architecture cost, while non-negative residual coupling can only erode the recoverable compromise loss. In the declared convex power-loss family, nonzero functional conflict yields strictly positive recovery in every evaluated case and larger optimum separation increases that recovery in every declared series. Differentiation is favoured only when the recovered amount exceeds the additional architecture cost.

It does not support:

- strict positive recovery for every conceivable nonconvex or constrained architecture;
- optimum-distance monotonicity for arbitrary multimodal or frequency-dependent landscapes;
- a historical claim that any observed pair of traits originated by this route;
- prevalence estimates for differentiation in nature;
- the claim that two traits imply functional independence;
- a full evolutionary-dynamics result involving mutation, genetic covariance or branching.

## Consequence for manuscript architecture

The Main text should use this evidence hierarchy:

```text
GENERAL STRUCTURE
nested feasible set -> R >= 0
non-negative scaled coupling -> R nonincreasing with lambda
fixed K -> Delta_arch = R-K

QUADRATIC COROLLARY
R = s L_S*
closed-form decoupling fraction s

FINITE NONQUADRATIC ROBUSTNESS
strict R > 0: 300/300
conflict-distance monotonicity: 60/60
coupling monotonicity: 60/60 implementation check
```

This ordering prevents a numerical sweep from being mistaken for the proof of a result that follows directly from the architecture definition, while preserving the useful nonquadratic evidence for strictness and conflict-strength scaling.
