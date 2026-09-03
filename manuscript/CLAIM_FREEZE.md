# Manuscript claim freeze

This file is the editorial guardrail for the SCH/BITA chapter programme after the Chapter 2 reframe.

## Chapter boundary

The programme is not defined by pollination versus defence. It is defined by how organisms resolve conflicting functional demands on trait architecture.

### SCH / Chapter 1 — BALANCE

A single trait coordinate `z` contributes to two functions or selective demands with different preferred states.

> **Chapter 1 asks how opposing demands are balanced while they remain coupled on one trait axis.**

Pollinator–antagonist shared-cue conflict is one empirical realization of this shared-axis problem.

### BITA / Chapter 2 — DIFFERENTIATION

The second chapter asks whether the conflict remains on one axis or is partitioned across distinct trait coordinates.

> **Chapter 2 asks when a shared-trait compromise becomes inferior to functional differentiation across two or more trait axes.**

The architecture contrast is

```text
W_S* = max_z W_S(z)
W_D* = max_{x,y} W_D(x,y)
Delta_arch = W_D* - W_S*
```

with differentiation favoured only when `Delta_arch > 0` after accounting for residual coupling and the additional cost of maintaining a differentiated architecture.

## Frozen Chapter 2 theory result

For the quadratic baseline,

```text
W_S(z) = -w1 (z-theta1)^2 - w2 (z-theta2)^2
W_D(x,y) = -w1 (x-theta1)^2 - w2 (y-theta2)^2
           - lambda (x-y)^2 - K
```

where `theta1` and `theta2` are function-specific optima, `lambda >= 0` is residual cross-talk/coupling and `K >= 0` is the additional fixed architecture cost.

The optimized architecture gain is

```text
Delta_arch = R - K
```

with recoverable conflict loss

```text
R = w1^2 w2^2 (theta1-theta2)^2
    / ((w1+w2) * (w1*w2 + lambda*(w1+w2))).
```

Therefore, within this baseline,

```text
differentiation is favoured  <=>  K < R.
```

The biological content is not that specialization is newly discovered. It is that the one-axis compromise creates a measurable loss budget, only part of that budget remains recoverable when differentiated traits retain cross-talk, and the recovered amount must pay for the extra architecture.

Immediate comparative statics are frozen:

- larger distance between function-specific optima increases `R`;
- stronger residual coupling `lambda` decreases `R`;
- larger architecture cost `K` shifts the system toward the shared compromise;
- `theta1 = theta2` gives `R = 0`, so differentiation cannot be favoured by this conflict-relief mechanism when there is no functional conflict.

## Frozen nonquadratic robustness result

The same qualitative boundary survives the declared convex power-loss family

```text
L_S(z) = w1 |z-theta1|^p + w2 |z-theta2|^p
L_D(x,y) = w1 |x-theta1|^p + w2 |y-theta2|^p
           + lambda |x-y|^q + K,
```

for the registered finite design.

The matched-curvature sweep contains 300 evaluations spanning `p = 1.5, 2, 3, 4`, three asymmetric/equal weighting pairs, five coupling strengths and five optimum distances. Results:

```text
positive recoverable conflict loss at K=0: 300 / 300
optimum-distance monotonic series:          60 / 60
coupling monotonic series:                  60 / 60
```

Additional mismatched `(p,q)` checks preserve the same cost-threshold logic. This is a finite robustness result for a convex family, not a theorem covering arbitrary nonconvex, frequency-dependent or multimodal fitness landscapes.

## Prior-art boundary

Do not claim novelty for the general idea that functional trade-offs can favour specialization, division of labor, modularity or reduced pleiotropy.

The closest positioning anchors include:

- Rüffler, Hermisson & Wagner (2012), *Evolution of functional specialization and division of labor*;
- Guillaume & Otto (2012), *Gene functional trade-offs and the evolution of pleiotropy*;
- Sack & Buckley (2020), *Trait Multi-Functionality in Plant Stress Response*.

The defensible BITA contribution is the bridge

```text
shared-axis ecological balance
-> explicit architecture-gain boundary
-> incomplete differentiation with residual cross-talk
-> mechanism identification once multiple axes exist.
```

## Current empirical ceiling

The current evidence supports **architecture-state plausibility and mechanism identification**, not a causal reconstruction of the origin of differentiated traits.

### Cross-system architecture-state anchors

- Cichlid oral and pharyngeal jaws show that structurally separate functional modules can relax a single-system trade-off while retaining appreciable evolutionary/genetic integration. This is a biological analogue of partial differentiation with `lambda > 0`, not an estimate of BITA parameters.
- Dalechampia comparative history shows repeated functional redeployment, exaptation and addition of new defensive lines. This demonstrates historical reorganization of trait-function architecture, not a direct test that `Delta_arch > 0` caused those transitions.

### Existing BITA floral mechanism module

The mature floral work remains frozen and reusable:

- the discrete two-trait interaction `Delta_AD W` and nested outcome distinctions;
- identified-set and partial-identification logic for compatible mechanism allocations;
- the crossed `A×D×consumer` intervention design and separability diagnostic;
- the independent joint-channel assay requirement;
- 56 source-adjudicated route records across 25 independent biological clusters;
- the 17-system fragmented identification frontier;
- floral attraction–defence and mutualist–antagonist systems as a worked ecological case.

These results show how to determine what a multi-axis architecture is doing once the axes exist. They do **not** by themselves establish the historical transition

```text
one shared trait -> two differentiated traits.
```

## Role of the floral A×D module

The attraction–defence framework is one worked case, not the universal scope.

In that case:

```text
A = one trait axis contributing mainly to one function
D = a second trait axis capable of modifying the cost/benefit structure of A
```

A positive `A×D` interaction can show functional relief inside a two-axis architecture and the intervention framework can identify why that relief occurs.

But:

```text
positive A×D interaction
!= trait differentiation
!= origin of D
!= historical modularization
!= population divergence
```

## Claims that must not appear

Do not claim any of the following:

- pollination and defence define the general theory;
- this is the first general theory showing that trade-offs can favour specialization;
- the 300-condition robustness grid proves universality across all fitness surfaces;
- trait differentiation has been historically reconstructed by the current BITA floral analyses;
- two interacting traits necessarily evolved by splitting one ancestral trait;
- positive cross-trait curvature is evidence of differentiation;
- the 56/25 recurrence corpus estimates the prevalence of differentiated architectures;
- the 17-system frontier reconstructs historical trait splitting;
- a local `A×D` fitness interaction predicts an evolutionary endpoint without an explicit architecture/dynamics model;
- structural separation of traits implies zero residual functional, developmental or genetic coupling;
- population differentiation and within-organism functional trait differentiation are the same object.

Retain the current identification ceilings for the floral worked case: marginal pathway recurrence is not total interaction identification, an unmeasured residual is not automatically cost, and direct joint-channel curvature remains unidentified where not independently measured.

## Scientific state

The following Chapter 2 gates are now closed for the current claim ceiling:

1. shared-axis optimum `W_S*` implemented;
2. differentiated-axis optimum `W_D*` implemented;
3. closed-form quadratic `Delta_arch` boundary derived and tested;
4. nonquadratic convex-family robustness implemented and registered;
5. empirical ceiling fixed as cross-system architecture-state evidence plus a floral mechanism-identification worked case.

A stronger historical claim that the one-axis conflict *caused the origin* of differentiated trait modules would require comparative ancestral-state, developmental, experimental-evolution or equivalent transition evidence and is not required for the present paper.

## Remaining manuscript work

1. Promote the architecture comparison to the beginning of the canonical manuscript.
2. Recast the existing floral identification framework as the mechanistic middle/empirical case rather than the paper's universal scope.
3. Add the prior specialization/multifunctionality literature before the novelty paragraph.
4. Add the cichlid and Dalechampia architecture-state anchors with the evidence ceiling above.
5. Rebuild figures so the paper reads `BALANCE -> DIFFERENTIATION -> IDENTIFICATION`.
6. Run final claim, reference, scope and rendered-page QA before merge/submission.

## Editorial test

Every Chapter 2 claim should pass five questions:

1. Is the general object a conflict between functions on trait architecture rather than a pollination/defence label?
2. Does the text distinguish compromise on one trait from differentiation across traits?
3. Does it distinguish evidence that two traits interact from evidence that a differentiated architecture evolved?
4. Does it preserve residual cross-talk rather than equating structural separation with independence?
5. Are historical transition claims kept below the current empirical ceiling?

If any answer is no, revise before submission.
