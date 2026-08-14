# Novelty and positioning boundary

## Current positioning

The manuscript should be positioned as a **mechanism-first focal-trait theory plus theory-structured empirical Pattern synthesis**. The novelty is not that pollinators and antagonists interact, that floral defence can carry pollination costs, that attraction can expose flowers to antagonists, that cross-trait curvature exists, or that ecological context changes interaction outcomes. Those ideas all have clear precedents.

The current contribution is narrower and stronger: for one declared floral attraction trait `A`, one declared flower-specific antagonist-reducing trait `D`, and one declared outcome scale `W`, the framework separates local attraction-defence curvature into antagonist relief, pollinator interference, and direct joint-cost curvature; imposes an explicit orientation gate; states the additional comparative-static conditions required for environmental predictions; derives a one-sided selectivity-window bound; and then uses a source-adjudicated empirical synthesis to ask which constituent mechanisms recur, which channels switch with context, and which quantities remain unidentified.

## Prior art that must be acknowledged

At minimum, the paper must explicitly acknowledge:

1. **Cross-trait fitness curvature and correlational selection are established.** Lande & Arnold (1983) and later multivariate-selection work already provide cross-trait quadratic and fitness-surface concepts. `W_AD` is not a new mathematical object.
2. **Defence can have ecological costs through pollination.** Strauss et al. (1999) directly predates any claim that resistance or defence-associated traits can reduce pollinator use or pollination-mediated fitness.
3. **Mutualists and antagonists can have nonadditive fitness effects.** Herrera et al. (2002) experimentally demonstrated nonadditive pollinator-herbivore fitness effects relevant to correlated evolution.
4. **Attraction can recruit antagonists as well as mutualists.** Floral signal and reward studies, including Theis & Adler and the Kessler programmes, establish shared or conflicting consumer tracking.
5. **Ecological context can change the balance between mutualism and antagonism.** This is established both empirically and in explicit ecological models; context dependence itself is not novel.

## What is explicitly not claimed as novel

Do not claim novelty for:

- multivariate fitness surfaces or correlational selection;
- a mixed partial or trait-interaction coefficient by itself;
- pollinator-herbivore nonadditivity;
- attraction increasing antagonist exposure;
- defence carrying a pollination cost;
- ecological context dependence;
- trade-offs or correlated evolution in general;
- the bookkeeping identity `W_AD = M_AD - G_AD - C_AD`;
- a universal positive or negative sign of `W_AD`;
- the statement that being inside a selective/guarded regime guarantees complementarity.

## Novel contribution 1 — mechanism-facing decomposition and inference boundary

After the focal orientation gate,

```text
W_AD = rho - iota - kappa
```

where `rho` is antagonist relief, `iota` is pollinator/mutualist interference, and `kappa` is direct joint-cost curvature.

The novelty claim is not the algebra. It is the **inference architecture**: the same total `W_AD` can arise from different channel allocations, so total fitness alone does not identify mechanism; marginal route evidence does not estimate the mixed partial; and environmental predictions require explicit derivative inequalities rather than verbal assumptions such as “more antagonists favour defence”.

## Novel contribution 2 — one-sided selectivity-window theorem

Define the selectivity window as the region where antagonist relief exceeds pollinator interference before joint cost is charged. Under the declared non-negative `relief - interference - cost` family,

```text
W_AD > 0  =>  rho > iota
```

so **complementarity cannot occur outside the window**.

This is a necessary-region result, not a two-sided criterion. Across the declared 2,592 evaluations and all four endpoint-normalized response-shape variants there are zero counterexamples, while 397 in-window evaluations are substitutable and window precision is 77.2%. With `kappa = 0`, the window and the sign criterion coincide exactly.

The reviewer-facing claim should therefore be: **the selectivity architecture defines a permissive region for complementarity, not a universal sign rule**.

## Novel contribution 3 — the unique escape route is negative joint-cost curvature

Outside the selectivity window, complementarity requires

```text
kappa < rho - iota <= 0
```

Therefore a negative joint-cost curvature is **necessary** for the one-sided bound to fail, and is sufficient when negative enough.

This gives `c_AD` a sharper role than an ordinary missing parameter. Its sign is the minimal empirical applicability/falsification gate for the strongest theorem in the declared family. A negative value means the focal attraction and defence traits are cheaper together than additivity predicts, for example through shared precursors, regulation, or multifunctional construction.

## Novel contribution 4 — theory converts a hard field test into a cheap falsification test

Estimating total `W_AD` still requires a joint `A x D` design on a common outcome, ideally with channel-specific measurements. The one-sided theorem creates a cheaper first test: a 2 x 2 allocation experiment (`neither`, `A only`, `D only`, `A + D`) can estimate the sign of the joint direct-cost interaction without pollinators, antagonists, or a total-fitness assay.

The methodological contribution is therefore a reduction of a difficult full-calibration problem to a simpler **falsification gate** for the strongest structural claim.

## Novel contribution 5 — Mechanism → Pattern synthesis

Part II does not manufacture a grand effect across incompatible outcomes. Instead, the theory defines the empirical evidence architecture.

Current saturated Pattern state:

```text
56 source-adjudicated route-level records
25 independent biological study clusters
A -> pollination: 5 clusters
A -> antagonism: 8
D -> antagonism: 18
D -> pollination: 10
same-system multi-route: 14
context/sign-switch: 17
context-only programs: 7, excluded from route-ledger N
direct total-outcome A x D: very sparse / unresolved
direct joint cost kappa: 0 strict estimates
```

The cross-system result is **recurrent constituent mechanisms + context-dependent balance**, with recurrent guarded states, attack-mode and spatial/temporal filtering, consumer functional-mode routing, lifecycle-stage role reversal, and other channel switching. This is a theory-structured recurrence synthesis, not an estimate of natural prevalence.

## Empirical H-gate result and its limit

The floral-larceny synthesis establishes that realised antagonist pressure is biologically non-zero on average: female reproductive success has pooled LRR about -0.210 across 48 independent clusters, with nectar standing crop and legitimate visitation also negative on average. But 35/48 female-fitness clusters are negative, the 95% prediction interval spans approximately -1.13 to +0.71, and the declared moderator set explains only 0-8% of the extreme heterogeneity.

Therefore the empirical result is:

> the antagonist-pressure gate can be open on average, but its realised magnitude and even sign are system dependent, and the tested coarse moderators do not yet locate that variation.

The pooled nectar -> visitation -> female-fitness sequence must not be presented as a demonstrated within-study mechanism chain. Only five clusters measure all three outcomes, only two show all three arrows negative, and the shared nectar-visitation subset gives `r = -0.17`.

## Direct-factorial evidence boundary

The Kessler floral factorials show that crossed floral-trait interaction signs can change with consumer context on pollination-channel outcomes. They do not identify total `W_AD`, and published summaries do not provide formal interaction uncertainty for the reconstructed finite contrasts. The `Impatiens` total reproductive-outcome candidate remains sign-unresolved.

Thus direct evidence supports **context-dependent channel interaction**, not a universal total curvature sign.

## Reviewer-facing novelty statement

A defensible concise formulation is:

> Building on multivariate selection theory and established pollinator-antagonist interactions, we develop a mechanism-facing local attraction-defence framework that separates antagonist relief, mutualist interference, and direct joint cost. The framework yields a one-sided selectivity-window theorem: under non-negative joint-cost curvature, complementarity is confined to a permissive region where antagonist relief exceeds pollinator interference, although being inside that region is not sufficient. A sufficiently negative joint-cost curvature is the unique escape from that bound in the declared family, reducing its biological falsification to the sign of a joint allocation interaction. A theory-structured cross-system synthesis then shows recurrent constituent mechanisms and recurrent context-dependent channel switching while leaving total `W_AD` and direct joint cost empirically unresolved.

Avoid “first general theory”, “novel universal criterion”, “universal attraction-defence sign”, or claims that the empirical synthesis validates the complete mixed partial.

## Evolutionary and parameterisation boundaries

`W_AD` is a local mixed partial on declared trait coordinates and outcome scale. Positive affine rescaling preserves the sign; arbitrary nonlinear transformation need not. The sign therefore belongs to a declared biological parameterisation.

`W_AD` alone does not imply population-level covariance, genetic correlation, an evolved cline, a trajectory, equilibrium, or optimum. Those require additional genetic and dynamical assumptions.

Every application must declare one focal `A` and one flower-specific antagonist-reducing `D`. A trait that only obstructs pollinators is not sufficient to instantiate the defence axis, and a marginal `D -> pollinator use` or `D -> antagonist damage` effect does not by itself identify the corresponding cross-curvature.
