# Trait differentiation robustness readout

## Question

Does the Chapter 2 boundary depend on assuming quadratic functional losses and quadratic residual coupling?

The closed-form baseline compares a one-axis compromise with a two-axis architecture. The robustness family replaces the quadratic losses with convex power losses:

```text
shared loss:
L_S(z) = w1 |z-theta1|^p + w2 |z-theta2|^p

differentiated loss:
L_D(x,y) = w1 |x-theta1|^p + w2 |y-theta2|^p
         + lambda |x-y|^q + K
```

where `p > 1` controls functional curvature, `q > 1` controls residual cross-talk curvature, `lambda` is cross-talk strength, and `K` is the fixed architecture cost.

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

## Result 1 — differentiation recovers some shared-axis conflict loss throughout the declared grid

At zero fixed architecture cost, all 300/300 nonzero-conflict evaluations had positive recoverable conflict loss:

```text
positive recoverable gain = 300 / 300
minimum                 ~= 4.46e-06
maximum                 ~= 2.656
```

This does not mean differentiated architectures are universally favoured in nature. It means that within this convex family, allowing two coordinates weakly enlarges the attainable phenotype set, so some loss from the forced shared compromise can be recovered whenever the function-specific optima differ and residual coupling is finite.

The evolutionary decision still depends on whether that recovered amount exceeds the architecture cost `K`.

## Result 2 — stronger functional conflict consistently increases the amount worth recovering

Across every fixed combination of response shape, functional weighting and coupling, increasing the distance between function-specific optima increased recoverable conflict loss:

```text
monotonic conflict-strength series = 60 / 60
```

Thus the qualitative prediction from the quadratic baseline survives the declared nonquadratic family:

> farther-separated functional optima make differentiation more valuable, all else equal.

## Result 3 — residual coupling consistently erodes the value of differentiation

Across every fixed combination of response shape, functional weighting and optimum distance, increasing `lambda` never increased the recoverable conflict loss:

```text
monotonic coupling series = 60 / 60
```

This establishes an important distinction for the Chapter 2 story:

```text
more trait axes
!=
more functional independence
```

A structurally differentiated phenotype can remain strongly coupled. Large cross-talk moves the two-axis optimum back toward the shared compromise and reduces the amount available to pay for an additional module.

## Result 4 — the architecture-cost threshold is not specific to equal curvatures

When the functional and coupling losses used different powers, the same threshold logic held in the declared checks. For each case, let

```text
R = shared optimum loss - differentiated optimum loss before K
```

Then:

```text
K = 0.9 R -> differentiated architecture preferred
K = 1.1 R -> shared architecture preferred
```

for all three `(p,q)` combinations tested.

This is not surprising algebraically: once the two architectures have been optimized, a fixed architecture cost subtracts one-for-one from the differentiated architecture. The useful biological quantity is therefore the **recoverable conflict loss before the fixed cost is paid**.

## Claim ceiling

The robustness result supports:

> Within the declared convex power-loss family, the balance-to-differentiation transition retains the same qualitative structure as the quadratic baseline: conflict strength raises the potential value of differentiation, residual cross-talk lowers it, and differentiation is favoured only when recoverable compromise loss exceeds the additional architecture cost.

It does not support:

- universality across all nonconvex, multimodal or frequency-dependent fitness surfaces;
- a historical claim that any observed pair of traits originated by this route;
- prevalence estimates for differentiation in nature;
- the claim that two traits imply functional independence;
- a full evolutionary-dynamics result involving mutation, genetic covariance or branching.

## Consequence for manuscript architecture

The quadratic expression can remain the analytic first result because it provides a closed-form threshold. The nonquadratic family should appear immediately after it as a finite robustness result, preventing the paper from being read as an artifact of parabolic stabilizing selection.

The empirical Discussion can then use partially decoupled systems, rather than perfectly modular systems, as the relevant biological comparison. This matches both the explicit `lambda` term and the external cichlid evidence that structurally separate functional modules may retain evolutionary/genetic integration.
