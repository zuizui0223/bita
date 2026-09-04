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

> **Chapter 2 asks when a shared-trait compromise becomes inferior to functional differentiation across two or more trait axes, and how the mechanism of the resulting multi-trait phenotype can be identified.**

## Frozen general architecture results

Use a loss representation for the shared architecture,

```text
L_S(z) = l1(z) + l2(z)
L_S*   = min_z L_S(z)
```

and a differentiated pre-fixed-cost architecture

```text
L_D0(x,y; lambda) = l1(x) + l2(y) + lambda c(x,y)
```

with the declared nesting conditions

```text
lambda >= 0
c(x,y) >= 0
c(z,z) = 0.
```

The last condition makes the one-axis phenotype a diagonal special case of the two-axis architecture before the additional fixed architecture cost is charged.

Define

```text
L_D0*(lambda) = min_{x,y} L_D0(x,y; lambda)
R(lambda)      = L_S* - L_D0*(lambda)
K >= 0         = additional fixed architecture cost.
```

### Claim A — nested-architecture weak dominance

Because the differentiated optimizer can always choose `x=y=z*`,

```text
L_D0*(lambda) <= L_S*
R(lambda) >= 0.
```

This is a feasible-set result and does not require quadratic, convex or smooth losses.

It is a **weak** statement. `R=0` remains possible when the additional axes cannot exploit a beneficial off-diagonal state, when the functions share the same optimum, or when other declared restrictions eliminate the release opportunity.

After adding `K`,

```text
Delta_arch = W_D* - W_S* = R - K
```

and therefore

```text
differentiation is favoured  <=>  K < R.
```

This exact cost threshold is structural within the declared additive fixed-cost architecture; it is not evidence that evolution can necessarily reach the higher-fitness architecture.

### Claim B — residual-coupling monotonicity

When coupling enters as `lambda c(x,y)` with `c >= 0`, increasing `lambda` raises or leaves unchanged the loss of every fixed `(x,y)` state. Therefore

```text
lambda2 > lambda1
=> L_D0*(lambda2) >= L_D0*(lambda1)
=> R(lambda2) <= R(lambda1).
```

Thus stronger declared non-negative residual coupling cannot increase the recoverable compromise loss. This is also shape-independent within the declared architecture.

The paper must distinguish these structural statements from shape-dependent strictness and comparative statics.

## Frozen quadratic corollary

For the quadratic baseline,

```text
L_S(z) = w1 (z-theta1)^2 + w2 (z-theta2)^2
L_D0(x,y) = w1 (x-theta1)^2 + w2 (y-theta2)^2
             + lambda (x-y)^2
```

where `theta1` and `theta2` are function-specific optima, `w1,w2 > 0`, and `lambda >= 0` is residual cross-talk/coupling.

The best shared-axis conflict load is

```text
L_S* = w1 w2 (theta1-theta2)^2 / (w1+w2).
```

Define the optimized decoupling fraction

```text
s = |x* - y*| / |theta1 - theta2|
  = w1*w2 / (w1*w2 + lambda*(w1+w2)).
```

Then

```text
R = s L_S*
Delta_arch = s L_S* - K.
```

Therefore, within this baseline,

```text
differentiation is favoured  <=>  K < s L_S*.
```

The biological content is that the one-axis compromise creates a measurable loss budget, only a fraction `s` remains recoverable when differentiated traits retain cross-talk, and that recovered amount must pay for the extra architecture.

Frozen quadratic comparative statics:

- larger distance between function-specific optima increases `L_S*` and `R`;
- stronger residual coupling `lambda` decreases `s` and `R`;
- larger architecture cost `K` shifts the system toward the shared compromise;
- `theta1 = theta2` gives `L_S*=R=0`, so this conflict-relief mechanism provides no differentiation advantage when there is no functional conflict;
- structural differentiation does not imply independence: finite positive `lambda` gives `0 < s < 1`.

## Frozen nonquadratic robustness result

The registered convex power-loss family is

```text
L_S(z) = w1 |z-theta1|^p + w2 |z-theta2|^p
L_D0(x,y) = w1 |x-theta1|^p + w2 |y-theta2|^p
             + lambda |x-y|^q.
```

The matched-curvature sweep contains 300 evaluations spanning `p = 1.5, 2, 3, 4`, three asymmetric/equal weighting pairs, five coupling strengths and five nonzero optimum distances. Results:

```text
strictly positive recoverable conflict loss: 300 / 300
optimum-distance monotonic series:             60 / 60
coupling monotonic series:                     60 / 60
```

Interpretation of these three lines is different:

- `R>0` in 300/300 establishes strict recovery throughout the declared nonzero-conflict convex family;
- optimum-distance monotonicity in 60/60 is a finite-family shape-robust comparative result;
- coupling monotonicity in 60/60 is an implementation check of frozen Claim B, not the proof of Claim B.

Additional mismatched `(p,q)` checks preserve the exact additive-cost threshold: costs just below recovered loss favour differentiation and costs just above it favour the shared architecture.

This is **not** a theorem that arbitrary nonconvex, frequency-dependent, multimodal or dynamically changing evolutionary landscapes produce strict differentiation advantages.

## Prior-art boundary

Do not claim novelty for the general idea that functional trade-offs can favour specialization, division of labor, modularity or reduced pleiotropy.

Closest positioning anchors include:

- Rüffler, Hermisson & Wagner (2012), *Evolution of functional specialization and division of labor*;
- Guillaume & Otto (2012), *Gene functional trade-offs and the evolution of pleiotropy*;
- Sack & Buckley (2020), *Trait Multi-Functionality in Plant Stress Response*.

The defensible BITA contribution is the bridge

```text
shared-axis ecological balance
-> recoverable compromise loss under partial decoupling
-> explicit architecture-cost threshold
-> mechanism identification once multiple axes exist.
```

The nested-feasible-set inequality itself is mathematically elementary and must not be sold as sophisticated mathematical novelty. Its value is as the inference bridge that makes the chapter sequence measurable.

## Current empirical ceiling

The current evidence supports **architecture-state plausibility and mechanism identification**, not a causal reconstruction of the origin of differentiated traits.

### Cross-system architecture-state anchors

- Cichlid oral and pharyngeal jaws show that structurally separate functional modules can relax a feeding trade-off while retaining appreciable evolutionary/genetic integration. This is a biological analogue of partial differentiation, not an estimate of `s`, `lambda`, `K` or `Delta_arch`.
- *Dalechampia* comparative history shows repeated functional redeployment, exaptation and addition of new defensive lines. This demonstrates historical reorganization of trait-function architecture, not a direct test that the BITA threshold caused those transitions.

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
!= population divergence.
```

## Claims that must not appear

Do not claim any of the following:

- pollination and defence define the general theory;
- this is the first general theory showing that trade-offs can favour specialization;
- adding any second trait necessarily improves realized fitness after its full costs are included;
- `R>0` is universal when the differentiated architecture does not contain the shared architecture as a zero-variable-cost special case;
- coupling monotonicity holds for signed/synergistic coupling terms outside the declared `c>=0` architecture;
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

The following Chapter 2 gates are closed for the current claim ceiling:

1. general nested-architecture weak-dominance and coupling-monotonicity propositions fixed;
2. shared-axis and differentiated quadratic optima implemented;
3. closed-form `R=sL_S*` and `Delta_arch=sL_S*-K` corollary derived and regression-tested;
4. nonquadratic convex-family robustness implemented and registered;
5. prior-theory novelty boundary audited;
6. empirical ceiling fixed as cross-system architecture-state evidence plus a floral mechanism-identification worked case;
7. integrated Chapter 2 manuscript, focused references and five Main figures drafted;
8. independent candidate Ecology package builder/workflow added.

A stronger historical claim that the one-axis conflict *caused the origin* of differentiated trait modules would require comparative ancestral-state, developmental, experimental-evolution or equivalent transition evidence and is not required for the present paper.

## Remaining manuscript work

1. Make the general propositions visible in the candidate Main before the quadratic corollary.
2. Complete the independent Chapter 2 DOCX/PDF candidate build and page-limit check.
3. Synchronize canonical manuscript/reference/figure/build pointers only after that candidate is green.
4. Rebuild Main + Appendix under the canonical path.
5. Perform final page-by-page visual QA and author-controlled metadata/sign-off.

## Editorial test

Every Chapter 2 claim should pass six questions:

1. Is the general object a conflict between functions on trait architecture rather than a pollination/defence label?
2. Does the text distinguish the general nested-architecture statements from the quadratic `R=sL_S*` corollary?
3. Does it distinguish compromise on one trait from differentiation across traits?
4. Does it distinguish evidence that two traits interact from evidence that a differentiated architecture evolved?
5. Does it preserve residual cross-talk rather than equating structural separation with independence?
6. Are historical transition claims kept below the current empirical ceiling?

If any answer is no, revise before submission.
