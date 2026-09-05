# Biotic Interaction Trait Architecture

BITA is the **Chapter 2 / trait-differentiation** half of the SCH–BITA programme.

```text
SCH / Chapter 1 — BALANCE
multiple functions are forced onto one shared coordinate z
-> identify causal compromise geometry while architecture remains integrated

BITA / Chapter 2 — DIFFERENTIATION
allow partly independent coordinates x,y
-> test whether extra dimensionality releases the measured compromise
-> identify why the multi-trait phenotype works
```

The programme is about **trait trade-offs and architecture**, not specifically pollination versus defence. Floral shared-cue conflict is SCH's principal implementation; floral attraction × defence is BITA's detailed mechanism-identification worked case.

## The SCH -> BITA interface has two levels

The current SCH main distinguishes theory-level pure function optima from the state-specific reproductive optima directly identified by experiment. BITA must preserve that distinction.

### 1. Theory-level architecture bridge

SCH theory writes pure function objectives on one shared coordinate:

```text
z_F1* = argmax F1(z)
z_F2* = argmax F2(z)
```

with the local quadratic compromise benchmark

```text
L_compromise,theory*
  = [a b/(a+b)] (z_F1* - z_F2*)^2.
```

BITA's quadratic notation is the same theory-level architecture comparison:

```text
theta1 <-> z_F1*
theta2 <-> z_F2*
L_S*   <-> L_compromise,theory*

R = s L_S*
Delta_arch = s L_S* - K.
```

The general BITA result remains

```text
R >= 0
Delta_arch = R - K
Delta_arch > 0 <=> K < R.
```

These are architecture-theory quantities unless pure functional objectives and all compared losses/costs are identified on commensurable empirical scales.

### 2. Default empirical handoff

The multi-level SCH `z × pollinator × antagonist` experiment directly identifies state-specific reproductive surfaces

```text
W00(z), W10(z), W01(z), W11(z)
```

and the optima

```text
z_P* = argmax W10(z)
z_G* = argmax W01(z)
z_C* = argmax W11(z).
```

Critically,

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

SCH's contemporary causal-compromise target is therefore state-specific: `z_P*` and `z_G*` differ, `W11(z)` has a supported interior `z_C*`, removing each functional demand moves the combined optimum toward the corresponding state optimum, and functional-component gradients near `z_C*` oppose one another.

BITA's default empirical release question inherits that directly identified reference. If `x` is the retained function-1-facing coordinate and `y` is the added function-2-facing coordinate, test

```text
|x*(y1) - z_P*| < |x*(y0) - z_P*|.
```

This is **state-specific dimensional release**.

Only if SCH independently identifies a context-stable component / pure function optimum `z_F1*` should BITA add the stricter pure-function release test toward `z_F1*`. The state-specific and pure-function lanes must not be silently equated.

The full contract is `docs/SCH_BITA_EMPIRICAL_HANDOFF_V1.md`.

## Canonical Chapter 2 architecture result

### General nested-architecture result

If the differentiated architecture contains every shared phenotype on its diagonal before the extra fixed architecture cost is charged, optimizing over the larger phenotype space gives

```text
R >= 0
Delta_arch = R - K
Delta_arch > 0 <=> K < R
```

where `R` is recoverable shared-architecture loss and `K` is additional fixed architecture cost. If residual coupling is a non-negative scaled penalty, stronger coupling cannot increase `R`.

### Quadratic corollary

For two theory-level function-specific optima `theta1, theta2`,

```text
shared conflict load       L_S*
decoupling fraction        s = |x_opt-y_opt| / |theta1-theta2|
recoverable conflict loss  R = s L_S*
architecture gain          Delta_arch = s L_S* - K.
```

This is a theory benchmark for the value of architectural release. It is not a claim that current SCH field data already identify `theta1`, `theta2`, `L_S*`, `s`, and `K` jointly.

## Nonquadratic robustness

Registered convex-family design:

```text
300 nonzero-conflict evaluations
strict positive pre-cost recovery:                 300 / 300
recovery increases with optimum separation:         60 / 60 series
coupling monotonicity implementation check:          60 / 60 series
```

The finite sweep tests strictness and distance dependence; coupling monotonicity is already a structural consequence of the declared non-negative coupling penalty. No universality claim is made for arbitrary nonconvex, multimodal, frequency-dependent or evolutionary-dynamic landscapes.

## Empirical architecture-state anchors

- **Cichlid oral + pharyngeal jaws:** function partitioning with residual evolutionary/genetic integration; an analogue of incomplete differentiation.
- **Dalechampia:** historical redeployment, exaptation and addition of functional/defensive structures.

Neither system estimates `s`, `lambda`, `K` or `Delta_arch`, and neither proves that the modeled trade-off caused the historical transition.

## Floral BITA: local relief, dimensional release, then mechanism identification

For two focal trait axes,

```text
Delta_AD W = W11 - W10 - W01 + W00
```

with the existing nested outcome hierarchy:

```text
Level 1  positive interaction relief: Delta_AD W > 0
Level 2  constraint release:          A0 <= 0 < A1
Level 3  strict reversal:             A0 < 0 < A1.
```

These local two-level outcomes are not the same as the multi-level SCH-to-BITA dimensional-release test toward `z_P*`. They are complementary.

The total interaction also does not uniquely identify its ecological channels. The retained inference ladder is

```text
interaction detection
-> identified set
-> partial identification
-> selective A x D x antagonist x pollinator intervention
-> four-way separability / residual-coupling diagnostic
-> independent remaining-channel assay.
```

The empirical layer contains **56 source-adjudicated route records / 25 independent biological clusters** and an authoritative **17-system high-information frontier**. The result is recurrent constituent biology plus **fragmented identification**, not prevalence of trait differentiation.

A non-zero `A × D × antagonist × pollinator` four-way term is also evidence that the apparently differentiated axes retain context-dependent cross-loading; differentiation is partial rather than perfectly modular.

## Strict boundary

```text
SCH state-specific optimum
!= pure function optimum without the stronger SCH gate

SCH compromise
!= historical origin of a second trait axis

positive A x D interaction
!= dimensional release toward z_P*
!= trait differentiation history

positive Delta_arch in theory
!= evidence that the transition occurred

structural separation
!= functional independence

route recurrence
!= prevalence.
```

## Canonical manuscript graph

- `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md` — canonical scientific source
- `manuscript/TRAIT_DIFFERENTIATION_REFERENCES_V1.md` — focused reference pool
- `manuscript/TRAIT_DIFFERENTIATION_FIGURE_CAPTIONS_V1.md` — figure captions
- `manuscript/trait_differentiation_figures/` — Figures 1–5
- `manuscript/CLAIM_FREEZE.md` — scientific claim ceiling
- `docs/SUBMISSION_SCOPE.md` — canonical submission scope
- `docs/SCH_BITA_EMPIRICAL_HANDOFF_V1.md` — current sister-project empirical interface
- `scripts/build_ecology_review_package_sources.py` — canonical package builder

`manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` remains versioned as the mature mechanism-identification component/provenance source.

## Validated package state

Canonical pre-metadata package:

```text
Main Document: 30 pages
Appendix S1:   38 pages
Main figures:   5
```

Theory, robustness, manuscript, figure, identification, formatter and package regressions pass. The Main is within the standard 30-page Ecology Concepts & Synthesis target.

## Submission state

**BITA science and pre-metadata package: GO.** The new SCH main makes the next paired-programme empirical step sharper: recover `z_P*`, `z_G*`, `z_C*` in a causal Chapter-1 system, then test state-specific dimensional release in the same or a tightly matched Chapter-2 system. Pure-function release is a stricter optional lane, not the default.

Remaining BITA upload blockers are author-controlled metadata/declarations/sign-off and final post-metadata rebuild/QA.
