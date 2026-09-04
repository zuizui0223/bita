# Paperization pass — SCH sister / Chapter 2

This file tracks the active paperization state after the balance-to-differentiation reframe. The general theory, finite nonquadratic robustness and first integrated manuscript now exist; the remaining work is integration/QA rather than reopening the central architecture question.

## 1. Programme spine

```text
conflicting functions / selective demands
               |
               v
        one shared trait axis
               |
        ------------------
        |                |
        v                v
     BALANCE        DIFFERENTIATION
     SCH / Ch.1     BITA / Ch.2
```

### SCH / Chapter 1 — BALANCE

Ask how opposing functional demands are resolved while they remain coupled on one trait axis: compromise, stabilizing balance, polymorphism, directional bias or context-dependent shifts.

### BITA / Chapter 2 — DIFFERENTIATION

Ask when the best shared compromise is inferior to partitioning the conflicting functions across partially independent trait axes.

The reader-facing question is:

> **When does a trait trade-off resolve by differentiation rather than compromise?**

Pollinator-antagonist floral conflict is one worked ecological realization, not the programme definition.

## 2. Main theoretical payoff

Shared quadratic architecture:

\[
W_S(z)=-w_1(z-\theta_1)^2-w_2(z-\theta_2)^2.
\]

The optimized shared-axis conflict loss is

\[
L_S^*=\frac{w_1w_2}{w_1+w_2}(\theta_1-\theta_2)^2.
\]

Differentiated architecture with residual coupling \(\lambda\) and additional fixed architecture cost \(K\):

\[
W_D(x,y)=
-w_1(x-\theta_1)^2
-w_2(y-\theta_2)^2
-\lambda(x-y)^2-K.
\]

Define the optimized **decoupling fraction**

\[
s=\frac{|x^*-y^*|}{|\theta_1-\theta_2|}
=\frac{w_1w_2}{w_1w_2+\lambda(w_1+w_2)}.
\]

The same fraction gives the proportion of the original shared-axis conflict loss that the differentiated architecture can recover before paying \(K\):

\[
R=sL_S^*.
\]

Therefore

\[
\boxed{\Delta_{arch}=sL_S^*-K}
\]

and

\[
\boxed{\Delta_{arch}>0\iff K<sL_S^*.}
\]

This is the preferred reader-facing form. It decomposes the architecture decision into:

```text
conflict load on the shared trait
x actual degree of functional decoupling
- extra architecture cost.
```

The older expanded threshold expression remains useful in Methods/Supplement, but the compact identity should lead the Results and Discussion.

## 3. Robustness gate — CLOSED

The nonquadratic robustness analysis is implemented in `trait_architecture/differentiation_robustness.py`, tested in `tests/test_trait_differentiation_robustness.py`, reproduced by `scripts/analyze_trait_differentiation_robustness.py`, and frozen in `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS_READOUT.json`.

Declared matched-curvature grid:

```text
functional power p = 1.5, 2, 3, 4
weights            = (1,1), (0.4,2), (3,0.7)
residual coupling  = 0, 0.1, 0.5, 2, 10
optimum distance   = 0.1, 0.25, 0.5, 1, 2
K                  = 0 for the recoverable-loss screen
N                  = 300
```

Results:

```text
positive recoverable loss:        300 / 300
conflict-distance monotonicity:     60 / 60
coupling monotonicity:              60 / 60
```

Additional mismatched `(p,q)` checks preserve the below/above cost-threshold switch.

Claim ceiling:

> Within the declared convex power-loss family, stronger conflict raises the value potentially recoverable through differentiation, residual cross-talk lowers it, and differentiation pays only if the recovered amount exceeds the extra architecture cost.

Do not call this a universal theorem across nonconvex, multimodal or frequency-dependent landscapes.

## 4. Prior theory / novelty boundary — CLOSED

The Introduction must explicitly acknowledge that specialization and division of labour under functional trade-offs are established theory. At minimum position against:

- Rüffler, Hermisson & Wagner (2012), *Evolution of functional specialization and division of labor*;
- Guillaume & Otto (2012), *Gene Functional Trade-Offs and the Evolution of Pleiotropy*;
- Sack & Buckley (2020), *Trait Multi-Functionality in Plant Stress Response*.

Do not claim:

```text
first theory of trait differentiation
first demonstration that trade-offs favour specialization
new discovery of division of labour
```

Defensible novelty:

```text
measurable shared-axis compromise
-> architecture gain with explicit incomplete decoupling
-> causal mechanism identification after multiple axes exist.
```

This bridge is where the mature BITA identification framework adds something that generic specialization theory does not supply.

## 5. Empirical ceiling — CLOSED FOR CURRENT PAPER

### Architecture-state reality checks

Use non-floral systems sparingly to establish that the modeled states are biologically real.

**Cichlid oral/pharyngeal jaws** — structural partitioning of prey capture and processing can relax a force-motion trade-off, yet the jaw systems retain evolutionary/genetic integration. This supports incomplete differentiation / residual coupling, not an estimate of `s`, `lambda` or `Delta_arch`.

**Dalechampia** — comparative history shows repeated functional redeployment, exaptation and addition of defensive lines. This supports historical reorganization of function-structure architecture, not a direct causal test that the BITA threshold generated those transitions.

### Floral BITA worked case

Retain the existing identification machinery as the answer to the next question:

> once multiple axes exist, what does their interaction mean and how can the responsible ecological channel be identified?

Keep:

- `Delta_AD W` and the Level 1/2/3 outcome hierarchy;
- identified-set and partial-identification geometry;
- crossed `A x D x antagonist x pollinator` intervention;
- four-way separability diagnostic;
- independent remaining-channel assay;
- Kessler/Egan/*Impatiens* reconstruction logic;
- 56 route records / 25 biological clusters;
- 17-system fragmented identification frontier.

Strict boundary:

```text
positive A x D interaction
!= trait differentiation
!= historical origin of a second axis.
```

## 6. Integrated manuscript — FIRST PASS COMPLETE

`MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md` now joins the programme into one article.

Working title:

> **When does a trait trade-off resolve by differentiation rather than compromise? Linking trait architecture to mechanism identification**

Current architecture:

```text
1. multifunctionality and the shared-trait compromise
2. analytic balance-to-differentiation boundary
3. nonquadratic robustness
4. incomplete differentiation / architecture-state evidence
5. floral BITA mechanism-identification worked case
6. implications, predictions and limits
7. conclusions
```

This file is the active integration candidate, **not yet the canonical submission source**. `MANUSCRIPT_IDENTIFICATION_DESIGN.md` remains preserved as the mature component/provenance source and current canonical source for the old validated package until the integrated draft passes the remaining QA gates.

## 7. Abstract architecture

The final Abstract should make five moves in this order:

1. multifunctional traits can face conflicting optima and therefore a compromise cost;
2. architecture may resolve the conflict by differentiating functions across axes, but structural separation can remain incomplete;
3. analytic payoff: `Delta_arch = s L_S* - K`;
4. robustness: 300/300 positive recoverable-loss cases, 60/60 conflict and coupling monotonic series within the declared convex family;
5. mechanism payoff: once multiple axes exist, their total interaction still does not identify why the architecture works; the floral BITA case supplies the identification design and fragmented empirical frontier.

End on the bridge from architecture choice to mechanism identification, not on “more data are needed.”

## 8. Introduction architecture

1. Open with multifunctionality and conflicting functional optima, not flowers.
2. Introduce shared compromise as one architecture.
3. Acknowledge specialization/division-of-labour/pleiotropy theory before presenting novelty.
4. Introduce incomplete differentiation: two structures can remain coupled.
5. State the unresolved empirical bridge: measured conflict -> architecture gain -> mechanism identification.
6. Use flowers only after the general problem is clear, as the high-resolution worked case.

## 9. Results order

### Result 1 — the shared compromise has a measurable conflict load

Lead with `L_S*`.

### Result 2 — differentiation pays only for the conflict it actually decouples

Lead with

```text
R = s L_S*
Delta_arch = s L_S* - K.
```

This is the main reader payoff.

### Result 3 — the qualitative boundary survives the declared nonquadratic family

Report 300/300 and both 60/60 monotonicity results with the finite-family ceiling.

### Result 4 — differentiation can remain incomplete

Use cichlid jaws as the biological reality check for residual coupling and *Dalechampia* as historical architecture-reorganization evidence.

### Result 5 — after multiple axes exist, total fitness does not identify mechanism

Bring in `Delta_AD W`, the identified set and crossed intervention.

### Result 6 — existing experiments form a fragmented identification frontier

Report Kessler/Egan/*Impatiens*, 56/25 recurrence and 17-system frontier without promoting them to evidence for historical trait splitting.

## 10. Discussion structure

Organize around four questions:

1. **Why compromise?** — one shared axis can remain optimal if the conflict load is low, coupling is high or extra architecture is costly.
2. **Why differentiation?** — differentiation pays when enough shared-axis loss is actually recoverable.
3. **Why incomplete differentiation?** — residual developmental, genetic, biomechanical or ecological coupling means `0 < s < 1` is biologically important, not a nuisance case.
4. **Why mechanism identification after differentiation?** — structural architecture does not label the causal pathway producing fitness.

Return explicitly to the SCH/BITA pair:

```text
SCH: what balance is maintained on the shared trait?
BITA: when is that balance costly enough and decouplable enough to justify a second axis, and what mechanism makes the resulting multi-trait architecture work?
```

## 11. Sister-paper non-overlap

| Question | SCH / Chapter 1 | BITA / Chapter 2 |
|---|---|---|
| Focal architecture | one shared trait axis | shared vs differentiated axes |
| Core problem | balance under conflicting demands | architecture transition / functional partitioning |
| Main object | compromise state and its ecological loading | conflict load, decoupling fraction, architecture cost |
| Floral shared-cue conflict | primary empirical realization | motivation + worked-case antecedent |
| Multi-trait interaction | not required | mechanistic subproblem after differentiation |
| Mechanism allocation | secondary | central second-stage inference problem |
| Historical origin | not required for balance claim | not claimed unless direct transition evidence is added |

## 12. Remaining work

Closed in this branch:

```text
A. shared-axis model
B. differentiated-axis model
C. analytic Delta_arch boundary
D. decoupling-fraction / recoverable-loss identity
E. baseline regression tests
F. nonquadratic convex-family robustness
G. robustness readout and claim ceiling
H. closest-prior-theory positioning
I. empirical ceiling and non-floral architecture-state anchors
J. first integrated Chapter 2 manuscript draft
```

Remaining mainline tasks:

```text
K. regression-test MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
L. merge/verify the full source-checked floral reference spine
M. update figures for BALANCE -> DIFFERENTIATION -> IDENTIFICATION
N. synchronize repository/submission-scope docs
O. promote integrated manuscript to canonical after K-N pass
P. rebuild Main + Appendix and page-by-page QA
Q. merge PR only after CI/scope checks are green or diagnosed
```

## 13. Final reader takeaway

> **SCH asks how conflicting functions find a balance on one trait. BITA asks when the cost of that compromise, multiplied by how much a new architecture can actually decouple the functions, is large enough to pay for trait differentiation—and how to identify the mechanism once multiple axes exist.**
