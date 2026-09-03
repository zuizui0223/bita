# Biotic Interaction Trait Architecture

BITA is the **Chapter 2 / trait-differentiation** half of the SCH–BITA programme.

```text
SCH / Chapter 1 — BALANCE
conflicting functions remain coupled on one trait
-> where/how is the compromise maintained?

BITA / Chapter 2 — DIFFERENTIATION
compare the best shared compromise with a partially decoupled multi-trait architecture
-> when does differentiation pay?
-> once multiple axes exist, what mechanism makes them work?
```

The general programme is about **trait trade-offs and architecture**, not specifically pollination versus defence. Floral mutualist–antagonist conflict remains BITA's most developed mechanism-identification worked case.

## Current Chapter 2 result

Let two functions prefer states `theta1` and `theta2` of one shared trait. In the quadratic baseline,

```text
W_S(z) = -w1(z-theta1)^2 - w2(z-theta2)^2
```

and the optimized shared architecture carries conflict loss

```text
L_S* = w1*w2*(theta1-theta2)^2/(w1+w2).
```

Allow a differentiated architecture with two trait axes, residual coupling `lambda`, and additional architecture cost `K`:

```text
W_D(x,y) = -w1(x-theta1)^2 - w2(y-theta2)^2
           - lambda*(x-y)^2 - K.
```

The optimized **decoupling fraction** is

```text
s = |x* - y*| / |theta1 - theta2|
  = w1*w2 / [w1*w2 + lambda*(w1+w2)].
```

In this baseline, the same `s` is the fraction of the one-trait compromise loss that the differentiated architecture can recover before paying the extra architecture cost:

```text
recoverable conflict loss  R = s * L_S*
architecture gain          Delta_arch = s * L_S* - K
```

Therefore

```text
Delta_arch > 0  <=>  K < s * L_S*.
```

Reader-facing interpretation:

> **Trait differentiation pays when the fitness cost of the shared compromise, multiplied by how much the new architecture actually decouples the functions, is large enough to cover the cost of maintaining the extra architecture.**

This makes incomplete differentiation explicit. Two structures or trait axes do not imply complete functional independence.

## Nonquadratic robustness

The architecture result is stress-tested in a deterministic convex power-loss family:

```text
functional power p = 1.5, 2, 3, 4
weights            = 3 equal/asymmetric pairs
residual coupling  = 5 levels
optimum distance   = 5 levels
matched-grid N     = 300
```

Registered results:

```text
positive pre-cost recoverable loss at nonzero conflict: 300 / 300
recoverable loss increases with optimum distance:        60 / 60 series
recoverable loss never increases with coupling:           60 / 60 series
```

Additional mismatched functional/coupling curvature checks preserve the same below/above architecture-cost threshold switch.

This is a finite robustness result for the declared convex family, not a universal theorem over arbitrary nonconvex, multimodal, frequency-dependent or evolutionary-dynamic landscapes.

Core files:

- `trait_architecture/differentiation.py`
- `trait_architecture/differentiation_robustness.py`
- `theory/TRAIT_DIFFERENTIATION_EXTENSION.md`
- `scripts/analyze_trait_differentiation_robustness.py`
- `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS.md`
- `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS_READOUT.json`

## Novelty boundary

BITA does **not** claim to invent functional specialization, division of labour, modularity, or reduced pleiotropy under trade-offs. The closest theoretical literature includes Rüffler, Hermisson & Wagner (2012), Guillaume & Otto (2012), and the multifunctionality framework of Sack & Buckley (2020).

The intended contribution is the bridge:

```text
measurable shared-axis ecological compromise
-> architecture gain with explicit partial decoupling
-> mechanism identification after multiple trait axes exist.
```

Positioning is documented in `docs/TRAIT_DIFFERENTIATION_POSITIONING.md`.

## Empirical architecture-state anchors

The current paper uses cross-system examples to establish that the modeled states are biologically realistic without pretending that those systems estimate BITA parameters.

- **Cichlid oral and pharyngeal jaws:** structural partitioning of prey capture and processing can relax a mechanical trade-off while evolutionary/genetic integration remains. This motivates residual coupling and partial differentiation.
- **Dalechampia:** comparative history documents repeated functional redeployment, exaptation and addition of defensive lines. This shows that trait-function architecture can be historically reorganized.

Neither system is treated as a direct estimate of `s`, `lambda`, `K`, or `Delta_arch`, nor as proof that the modeled conflict caused the historical origin of a second trait axis.

See `docs/TRAIT_DIFFERENTIATION_EMPIRICAL_BRIDGES.md`.

## Floral BITA: mechanism identification after multiple axes exist

The mature floral analysis is retained as the detailed second-stage worked case. For two experimentally meaningful trait levels,

```text
Delta_AD W = W11 - W10 - W01 + W00.
```

A total `Delta_AD W` does not identify its ecological allocation. If `Delta_AD W = delta`, compatible antagonist-relief, mutualist-interference and remaining-joint-channel allocations form an identified set rather than one mechanism.

The inference ladder remains:

```text
interaction detection
-> identified set
-> partial identification under declared bounds
-> crossed A x D x antagonist x pollinator intervention
-> four-way separability diagnostic
-> independent validation of the remaining joint channel.
```

The empirical recurrence layer contains:

```text
56 route records
25 independent biological clusters
```

and the high-information audit contains **17 systems** occupying complementary design faces. No screened system closes the full allocation design plus independent joint-channel assay. The empirical result is **fragmented identification**, not absence of relevant biology.

Strict boundary:

```text
positive A x D interaction
!= trait differentiation
!= historical origin of a second trait axis
!= prevalence of modular architectures.
```

## Integrated manuscript state

Active Chapter 2 integration candidate:

- `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md`
- `manuscript/TRAIT_DIFFERENTIATION_REFERENCES_V1.md`
- `manuscript/TRAIT_DIFFERENTIATION_FIGURE_PLAN_V1.md`
- `manuscript/TRAIT_DIFFERENTIATION_FIGURE_CAPTIONS_V1.md`
- `manuscript/trait_differentiation_figures/` — integrated Figures 1–5
- `manuscript/CLAIM_FREEZE.md`
- `docs/CHAPTER2_SUBMISSION_SCOPE_V1.md`

Working title:

> **When does a trait trade-off resolve by differentiation rather than compromise? Linking trait architecture to mechanism identification**

The intended narrative is

```text
BALANCE
-> shared-axis conflict load
-> DIFFERENTIATION
-> partial decoupling and architecture cost
-> IDENTIFICATION
-> causal allocation once multiple trait axes exist.
```

## Preserved old package

`manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` remains the mature source for the narrower identification paper and the existing validated package. The old package consists of **29 Main pages + 12 Appendix pages** and five identification figures.

It is preserved deliberately while the broader Chapter 2 integration is tested. It should **not** be described or submitted unchanged as the final SCH sister Chapter 2.

The repository therefore temporarily has two intentional manuscript graphs:

```text
preserved validated component package
and
active Chapter 2 promotion graph.
```

They converge only after the promotion contract in `docs/CHAPTER2_SUBMISSION_SCOPE_V1.md` is satisfied.

## Reproducibility / regression core

New Chapter 2 guards:

- `tests/test_trait_differentiation.py`
- `tests/test_trait_differentiation_robustness.py`
- `tests/test_trait_differentiation_manuscript.py`
- `tests/test_trait_differentiation_figures.py`
- updated `tests/test_claim_freeze.py`

Existing identification regressions remain active because the integrated manuscript reuses the older BITA work as its mechanistic case.

## Inference boundaries

```text
one-trait compromise
!= evidence that differentiation evolved

structural separation
!= functional independence

multi-trait interaction
!= mechanism allocation

route recurrence
!= prevalence
!= total A x D interaction
!= historical trait splitting.
```

## Submission state

The **preserved identification package** has previously passed its own build and visual QA. The **integrated trait-differentiation Chapter 2 is not yet declared submission-ready**.

Current promotion gates are:

```text
integrated narrative regressions
+ theory/robustness regressions
+ five-figure SVG guards
+ focused reference integration
+ synchronization of submission-scope docs
+ rebuilt Main/Appendix
+ page-by-page visual QA.
```

Until those gates close, the old package remains the build target and the new Chapter 2 remains the active scientific development target.
