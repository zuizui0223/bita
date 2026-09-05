# Biotic Interaction Trait Architecture

BITA is the **Chapter 2 / trait-differentiation** half of the SCH–BITA programme.

```text
SCH / Chapter 1 — BALANCE
one shared coordinate z is loaded by conflicting functions
-> identify contemporary compromise geometry on that one axis

BITA / Chapter 2 — DIFFERENTIATION
add or strengthen a second preferentially loaded coordinate y
-> test whether retained coordinate x is released from the Chapter-1 compromise
-> identify why the multi-trait phenotype works
```

The programme is about **trait trade-offs and architecture**, not specifically pollination versus defence. Floral shared-cue conflict is SCH's main implementation; floral attraction × defence is BITA's detailed mechanism-identification worked case.

## SCH -> BITA symmetry has a theory lane and an empirical lane

### Theory lane

SCH's idealized pure-function benchmark distinguishes

```text
z_F1* = argmax F1(z)
z_F2* = argmax F2(z)
```

and the local quadratic shared-coordinate mismatch cost

```text
L_compromise,theory*
  = [a b/(a+b)] (z_F1* - z_F2*)^2.
```

BITA's quadratic architecture model is the same theory-level comparison in different notation:

```text
theta1 <-> z_F1*
theta2 <-> z_F2*
L_S*   <-> L_compromise,theory*

R = s L_S*
Delta_arch = s L_S* - K.
```

The general architecture result remains

```text
R >= 0
Delta_arch = R - K
Delta_arch > 0 <=> K < R.
```

These are theory-level architecture quantities unless the pure objectives, shared loss, realized decoupling and additional costs are all identified on commensurable empirical scales.

### Default empirical lane

The current SCH multi-level `z × P × G` experiment directly identifies **state-specific reproductive optima**:

```text
z_P* = argmax W10(z)   # pollinator present, antagonist suppressed
z_G* = argmax W01(z)   # pollinator suppressed, antagonist present
z_C* = argmax W11(z)   # combined state
```

with the critical boundary

```text
z_P* != automatically z_F1*
z_G* != automatically z_F2*.
```

The direct Chapter-2 continuation therefore uses the SCH state-specific reference by default. For a retained coordinate `x` and added/strengthened coordinate `y`, BITA estimates

```text
x0* = optimum of x under y0
x1* = optimum of x under y1

R_state
  = |x0*_SCH - z_P*|
  - |x1*_SCH - z_P*|.
```

Positive `R_state` means that the second coordinate moves the retained optimum toward the intervention-defined Chapter-1 function-1-facing reference.

Only when SCH independently identifies a pure `z_F1*` may BITA switch to the stricter `pure_function` reference mode. State-specific and pure-function release are reported separately.

Canonical implementation:

- `docs/BITA_EMPIRICAL_DIMENSIONAL_RELEASE_ANALYSIS_V1.md`
- `trait_architecture/dimensional_release.py`
- `scripts/analyze_bita_dimensional_release.py`
- `empirical/identification_design/BITA_DIMENSIONAL_RELEASE_TEMPLATE_V1.csv`
- `empirical/identification_design/BITA_DIMENSIONAL_RELEASE_CONFIG_TEMPLATE_V1.json`

## Canonical Chapter 2 architecture result

### General nested-architecture result

If the differentiated architecture contains every shared phenotype on its diagonal before the extra fixed architecture cost is charged, optimizing over the larger phenotype space gives

```text
R >= 0
Delta_arch = R - K
Delta_arch > 0 <=> K < R
```

where `R` is the shared-compromise loss recoverable by the differentiated architecture and `K` is its additional fixed cost. If residual coupling is represented by a non-negative scaled penalty, stronger coupling cannot increase `R`.

### Quadratic corollary

For two theory-level function-specific optima `theta1` and `theta2`,

```text
shared conflict load       L_S*
decoupling fraction        s = |x_opt-y_opt| / |theta1-theta2|
recoverable conflict loss  R = s L_S*
architecture gain          Delta_arch = s L_S* - K.
```

This is not a claim that current SCH field data automatically identify `theta1`, `theta2`, `L_S*`, `s` and `K` jointly.

## Nonquadratic robustness

Registered convex-family design:

```text
300 nonzero-conflict evaluations
strict positive pre-cost recovery:                 300 / 300
recovery increases with optimum separation:         60 / 60 series
coupling monotonicity implementation check:          60 / 60 series
```

The finite sweep tests strictness and distance dependence; coupling monotonicity is already a structural consequence of the declared non-negative coupling penalty. No universality claim is made for arbitrary nonconvex, multimodal, frequency-dependent or evolutionary-dynamic landscapes.

## Current empirical Chapter-2 evidence

### Peucedanum multivittatum — positive real-world partial differentiation anchor

Published 2021/2025 results support a **partial functional differentiation** interpretation:

- perfect-flower production is positively loaded on female reproductive opportunity;
- perfect flowers increase predation exposure in the high-predation system;
- male-flower allocation directly reduces predation risk in the 2025 selection model;
- the value of the differentiated sex-function architecture varies along a strong predation/phenology mosaic.

This is a positive architecture-state result, but

```text
causal R_state:                    NOT_IDENTIFIED
historical origin of andromonoecy: NOT_IDENTIFIED.
```

Canonical receipt:
`empirical/identification_design/PEUCEDANUM_PUBLISHED_NUMERIC_RECEIPT_V1.json`.

### Pedicularis rex — same-species SCH -> BITA execution candidate

Pedicularis is the strongest current route for a direct paired experiment because shared-conflict biology and a function-2-facing water-retention/defence state are both recoverable. The repository now contains:

- an independent-antagonist SCH reference-surface contract;
- a Chapter-2 `x × y` dimensional-release experiment;
- a structural-`y` promotion gate;
- a downstream crossed mechanism-allocation plan.

The current ceiling remains **implemented / not yet executed**. The water treatment itself cannot be reused circularly as the SCH antagonist manipulation that defines the Chapter-1 reference.

### Nicotiana and other anchors

*Nicotiana attenuata* retains the strongest local positive attraction × defence reproductive-interaction anchor, but source/design uncertainty and systemic manipulation scope prevent treating it as a complete dimensional-release result. Petunia provides component-function partitioning evidence rather than a full common-fitness release test.

## Local cross-trait relief is not dimensional release

The local two-trait interaction remains explicitly defined as

```text
Delta_AD W = W11 - W10 - W01 + W00
```

with the existing hierarchy:

```text
Level 1  positive interaction relief: Delta_AD W > 0
Level 2  constraint release:          A0 <= 0 < A1
Level 3  strict reversal:             A0 < 0 < A1.
```

But

```text
positive A x D interaction
!= movement of x* toward z_P*
!= pure-function release
!= historical trait splitting.
```

The multi-level dimensional-release analysis is the direct empirical sister-paper test; the two-level hierarchy is a complementary local outcome analysis.

## Mechanism identification after release

A positive dimensional-release result still does not identify why the second axis works. The retained BITA mechanism ladder is

```text
interaction / dimensional-release detection
-> identified set
-> partial identification
-> selective x x y x antagonist x pollinator intervention
-> four-way separability / residual-coupling diagnostic
-> independent remaining-channel assay.
```

The existing empirical synthesis contains **56 source-adjudicated route records / 25 independent biological clusters** and an authoritative **17-system high-information frontier**. These show recurrent constituent biology plus **fragmented identification**, not prevalence of trait differentiation.

A non-zero four-way trait × trait × consumer × consumer interaction is also evidence that the nominally differentiated coordinates remain context-dependent/cross-loaded rather than perfectly modular.

## Current SCH–BITA completion status

```text
THEORY SYMMETRY
SCH one-axis compromise benchmark       PASS
BITA differentiation benchmark          PASS

EMPIRICAL ESTIMAND SYMMETRY
SCH state-specific compromise analyzer  IMPLEMENTED
BITA state-specific release analyzer    IMPLEMENTED

CAUSAL EXECUTION
positive full SCH z x P x G receipt     NOT YET EXECUTED
positive paired BITA R_state receipt    NOT YET EXECUTED

REAL-WORLD ARCHITECTURE EVIDENCE
SCH compromise cases                    RECOVERED
BITA partial differentiation cases      RECOVERED

HISTORICAL INTEGRATED -> MODULARIZED
                                        NOT IDENTIFIED
```

The pair is therefore **conceptually and analytically symmetric but not yet causally closed in one biological system**.

## Strict boundary

```text
SCH state-specific optimum
!= pure function optimum without the stronger SCH gate

SCH causal compromise
!= historical origin of a second trait axis

positive BITA R_state
!= historical modularization

positive theoretical Delta_arch
!= evidence that the transition occurred

structural separation
!= functional independence

case/route recurrence
!= prevalence.
```

## Canonical manuscript graph

- `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md` — canonical scientific source
- `manuscript/TRAIT_DIFFERENTIATION_REFERENCES_V1.md` — focused reference pool
- `manuscript/TRAIT_DIFFERENTIATION_FIGURE_CAPTIONS_V1.md` — figure captions
- `manuscript/trait_differentiation_figures/` — Figures 1–5
- `manuscript/CLAIM_FREEZE.md` — scientific claim ceiling
- `docs/SUBMISSION_SCOPE.md` — canonical submission scope
- `scripts/build_ecology_review_package_sources.py` — canonical package builder

The newer empirical execution spine lives alongside the canonical pre-metadata manuscript and sharpens the prospective SCH-to-BITA test without retroactively promoting existing literature to `R_state`.

## Validated package state

Canonical pre-metadata package:

```text
Main Document: 30 pages
Appendix S1:   38 pages
Main figures:   5
```

Theory, robustness, manuscript, figure, identification, formatter and package regressions pass. The Main is within the standard 30-page Ecology Concepts & Synthesis target.

## Submission state

**Science and pre-metadata package: GO.** The new empirical spine identifies the next decisive paired result: obtain a positive SCH causal-compromise receipt, freeze its state-specific reference, then test BITA dimensional release and mechanism allocation without circular reuse of the same intervention.

Remaining journal-upload blockers remain author-controlled metadata/declarations/sign-off and final post-metadata rebuild/QA.
