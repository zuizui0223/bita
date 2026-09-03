# Manuscript directory

## Current source state

The SCH/BITA Chapter 2 reframe now has an integrated manuscript candidate:

- `MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md` — **active Chapter 2 integration draft**. It joins the new shared-versus-differentiated architecture theory to the mature BITA mechanism-identification work.
- `MANUSCRIPT_IDENTIFICATION_DESIGN.md` — **mature component manuscript / provenance source** for the existing two-trait identification analyses. It remains the current canonical source for the old validated submission package until the integrated draft completes QA; it is not the final SCH sister Chapter 2.
- `MANUSCRIPT_THEORETICAL_ECOLOGY.md` — historical theorem-led manuscript retained for provenance only.

Do not submit the old 29-page identification package unchanged as the SCH sister paper. Do not promote the integrated draft to canonical submission source until reference, figure, regression and rendered-page QA are complete.

## SCH / BITA programme

The chapter pair is fixed at the level of trait architecture, not at pollinator/antagonist or attraction/defence labels.

### SCH / Chapter 1 — BALANCE

One trait coordinate contributes to multiple functions or selective demands whose preferred states differ.

```text
function 1  ->
              shared trait z -> compromise / balance
function 2  ->
```

Chapter 1 asks:

> **When conflicting demands remain coupled on one trait, where and how is the compromise maintained?**

Pollinator-antagonist shared-cue conflict is one empirical realization of this shared-axis problem.

### BITA / Chapter 2 — DIFFERENTIATION

Chapter 2 asks whether the conflict must remain on one axis.

```text
shared compromise z
       |
       v
recoverable conflict loss worth paying for a second axis?
       |
       +-- no  -> retain shared architecture
       |
       +-- yes -> partition functions across x and y
                 -> partial or strong trait differentiation
```

Chapter 2 asks:

> **When does a trait trade-off resolve by differentiation rather than compromise?**

## Frozen architecture result

For the quadratic baseline,

```text
W_S(z) = -w1(z-theta1)^2 - w2(z-theta2)^2
W_D(x,y) = -w1(x-theta1)^2 - w2(y-theta2)^2
           - lambda(x-y)^2 - K
```

The best shared architecture carries conflict loss

```text
L_S* = w1*w2*(theta1-theta2)^2/(w1+w2).
```

Residual coupling leaves only the decoupling fraction

```text
s = w1*w2 / [w1*w2 + lambda*(w1+w2)]
  = |x* - y*| / |theta1 - theta2|.
```

In this baseline, the same `s` is the fraction of shared-axis conflict loss that the differentiated architecture can recover before paying its extra fixed cost. Therefore

```text
recoverable conflict loss R = s * L_S*
Delta_arch                 = s * L_S* - K
```

and

```text
Delta_arch > 0  <=>  K < s * L_S*.
```

Reader-facing interpretation:

> **The value of differentiation equals the cost of the shared compromise, multiplied by how much functional decoupling the new axes actually achieve, minus the cost of maintaining the new architecture.**

This explicitly allows incomplete differentiation: more structures do not imply full functional independence.

## Nonquadratic robustness

The qualitative result has been stress-tested in `trait_architecture/differentiation_robustness.py` using convex power losses with functional powers `1.5, 2, 3, 4`, asymmetric and equal functional weights, five residual-coupling levels and five optimum distances.

Registered matched-curvature grid:

```text
300 evaluations
positive recoverable conflict loss at nonzero conflict, K=0: 300/300
optimum-distance monotonic series:                       60/60
residual-coupling monotonic series:                     60/60
```

Additional mismatched functional/coupling curvature checks preserve the same architecture-cost threshold logic. This is a finite convex-family robustness result, not a universal theorem for arbitrary fitness landscapes.

Sources:

- `theory/TRAIT_DIFFERENTIATION_EXTENSION.md`
- `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS.md`
- `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS_READOUT.json`
- `scripts/analyze_trait_differentiation_robustness.py`

## Prior-art and novelty boundary

Functional specialization, division of labour and reduced pleiotropy under trade-offs are established theoretical topics. The Chapter 2 paper therefore does **not** claim that specialization is newly discovered here.

Closest positioning anchors include Rüffler, Hermisson & Wagner (2012), Guillaume & Otto (2012), and Sack & Buckley (2020).

The defensible contribution is the three-layer bridge:

```text
1. shared-axis ecological balance / measurable compromise
2. architecture gain with explicit partial decoupling
3. mechanism identification after multiple trait axes exist
```

Detailed positioning is frozen in `docs/TRAIT_DIFFERENTIATION_POSITIONING.md`.

## Empirical ceiling

The current Chapter 2 uses two empirical layers with different roles.

### Architecture-state reality checks

- cichlid oral and pharyngeal jaws show structural/function partitioning with residual evolutionary and genetic integration: a real analogue of incomplete differentiation rather than perfect modular independence;
- *Dalechampia* comparative history shows repeated functional redeployment, exaptation and addition of functional/defensive lines.

These systems show that the architecture states represented by the theory exist. They do not estimate `Delta_arch` or prove that the modeled shared-axis conflict caused the historical origin of the second axis.

### Floral mechanism-identification worked case

The existing BITA floral analyses now answer the next question:

> once multiple axes exist, what does their joint fitness effect mean and which ecological pathway generated it?

Reusable results include:

- `Delta_AD W = W11 - W10 - W01 + W00`;
- nested interaction-relief / functional-release / strict-reversal claims;
- identified-set and partial-identification algebra;
- crossed `A x D x antagonist x pollinator` interventions;
- the four-way separability diagnostic;
- independent joint-channel assay logic;
- 56 route records across 25 independent biological clusters;
- 17-system fragmented identification frontier.

These results do not reconstruct the historical origin of trait differentiation.

## Integrated Chapter 2 draft

`MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md` now implements the intended narrative:

```text
1. multifunctional trade-off and shared compromise
2. analytic balance-to-differentiation boundary
3. nonquadratic robustness
4. incomplete differentiation in cichlid jaws + historical architecture change in Dalechampia
5. floral BITA as the mechanism-identification case after multiple axes exist
6. implications, predictions and strict historical claim ceiling
```

Working title:

> **When does a trait trade-off resolve by differentiation rather than compromise? Linking trait architecture to mechanism identification**

## Claim boundary

Do not equate:

```text
positive A x D interaction
!= trait differentiation
!= origin of a second trait axis
!= historical modularization
!= population differentiation
```

Likewise:

```text
two structures
!= complete functional independence.
```

Historical causation remains outside the present claim ceiling unless direct transition evidence is added.

## Submission state

Scientific integration is now substantially advanced. The remaining mainline work is:

```text
1. regression-test the integrated Chapter 2 draft
2. merge the full source-checked floral reference spine into it
3. design/update figures for BALANCE -> DIFFERENTIATION -> IDENTIFICATION
4. remove obsolete submission-scope text that still treats the old floral manuscript as the final paper
5. promote the integrated draft to canonical only after those checks pass
6. rebuild Main + Appendix and visually inspect every page
```

The narrower identification manuscript remains preserved, so the reframe does not destroy the mature work while the new Chapter 2 package is being validated.
