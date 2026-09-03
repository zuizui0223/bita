# Paperization pass — SCH sister / Chapter 2

This editorial plan supersedes the earlier floral attraction–defence-only Chapter 2 framing.

## 1. Programme spine

The SCH/BITA pair should read as a single evolutionary problem with two different resolutions.

```text
conflicting functions / selective demands
               |
               v
        one shared trait axis
               |
        ------------------
        |                |
        v                v
   BALANCE            DIFFERENTIATION
   Chapter 1          Chapter 2
   SCH                BITA
```

### SCH / Chapter 1 — balance

When one trait performs or signals more than one function, opposing demands can pull the same coordinate toward different optima. Chapter 1 asks how that conflict is maintained on the shared axis: compromise, stabilizing balance, polymorphism, context dependence or directional bias.

The biological example may be a floral cue seen by mutualists and antagonists, but the chapter-level object is broader: **one trait, competing consequences, one compromise coordinate**.

### BITA / Chapter 2 — trait differentiation

Chapter 2 asks when the one-axis compromise is no longer the best architecture. A second trait axis can allow the conflicting functions to be partitioned, reducing interference at the cost of maintaining, coordinating and constructing separate modules.

The central question is:

> **When does a trait trade-off resolve by differentiation rather than compromise?**

This is the new BITA mainline.

## 2. Implemented theoretical baseline

The quadratic baseline is now implemented in `trait_architecture/differentiation.py` and tested in `tests/test_trait_differentiation.py`.

Shared architecture:

\[
W_S(z)=-w_1(z-\theta_1)^2-w_2(z-\theta_2)^2.
\]

Differentiated architecture:

\[
W_D(x,y)=
-w_1(x-\theta_1)^2
-w_2(y-\theta_2)^2
-\lambda(x-y)^2
-K.
\]

After optimization,

\[
\Delta_{arch}=W_D^*-W_S^*
=
\frac{w_1^2w_2^2(\theta_1-\theta_2)^2}
{(w_1+w_2)[w_1w_2+\lambda(w_1+w_2)]}
-K.
\]

Therefore the baseline differentiation condition is

\[
K <
\frac{w_1^2w_2^2(\theta_1-\theta_2)^2}
{(w_1+w_2)[w_1w_2+\lambda(w_1+w_2)]}.
\]

Interpretation:

```text
stronger conflict between function-specific optima -> differentiation more likely
stronger residual coupling / cross-talk          -> differentiation less likely
larger architecture cost K                       -> differentiation less likely
same functional optimum                          -> no baseline gain from splitting
```

The full derivation is frozen in `theory/TRAIT_DIFFERENTIATION_EXTENSION.md`.

## 3. Prior theory and novelty boundary

The general idea that multifunctional modules can evolve functional specialization is not new. The Introduction must explicitly position against at least:

- Rueffler, Hermisson & Wagner (2012), *Evolution of functional specialization and division of labor*, PNAS, DOI `10.1073/pnas.1110521109`;
- Guillaume & Otto (2012), *Gene Functional Trade-Offs and the Evolution of Pleiotropy*, Genetics, DOI `10.1534/genetics.112.143214`;
- Sack & Buckley (2020), *Trait Multi-Functionality in Plant Stress Response*, Integrative and Comparative Biology, DOI `10.1093/icb/icz152`.

The quadratic threshold is therefore an **operational baseline for this programme**, not a claim to have invented specialization theory.

The defensible contribution is the bridge:

```text
measured ecological balance on one trait axis
-> explicit shared-versus-differentiated architecture comparison
-> empirical identification of the channels once two trait axes interact
```

The mature BITA identification framework makes this bridge distinctive: observing a differentiated phenotype or a positive two-trait interaction still does not identify which ecological process generated the apparent release.

Detailed positioning is in `docs/TRAIT_DIFFERENTIATION_POSITIONING.md`.

## 4. Recommended title direction

### Preferred working title

**When does a trait trade-off resolve by differentiation rather than compromise?**

### More explicit alternative

**From compromise to trait differentiation: resolving conflicting functions through trait architecture**

### Empirical-case subtitle option

**From compromise to trait differentiation: a general framework with floral conflict as a mechanistic case**

Do not lead the title with pollination or defence unless the final empirical scope remains deliberately floral.

## 5. One-sentence paper claim

> **When one trait is pulled toward conflicting functional optima, a differentiated architecture becomes favourable when the fitness recoverable by allowing function-specific trait states exceeds the additional architecture cost; residual coupling reduces both the amount of differentiation and the range of costs under which it pays.**

This is established for the current quadratic baseline. The final Abstract must label its scope correctly until robustness across alternative fitness shapes is complete.

## 6. Role of the current BITA manuscript

The current `MANUSCRIPT_IDENTIFICATION_DESIGN.md` should not be discarded. It contains a strong mechanistic subproblem:

> once two trait axes exist, what does their interaction mean, and how do we identify which ecological channel produced it?

Its core objects become the mechanistic middle section of the Chapter 2 paper:

```text
Delta_AD W
identified set of channel allocations
partial identification
crossed trait × consumer intervention
separability diagnostic
independent joint-channel assay
```

This solves **how differentiated axes function**, not by itself **how the two-axis architecture historically originated**.

## 7. Floral attraction–defence is a worked case, not the scope

The existing floral evidence remains useful because it gives a concrete system in which functions can conflict and multiple traits can redistribute those consequences.

Use it as:

```text
general theory:
function 1 versus function 2 on trait architecture

worked case:
floral attraction / mutualist benefit / antagonist exposure
+ a second antagonist-reducing or access-modifying trait
```

The 56 route records across 25 clusters establish recurrence of the relevant ecological pathways in the floral case. The 17-system frontier shows that the information needed to allocate two-trait interactions is fragmented across existing experiments.

Neither result estimates the prevalence of trait differentiation or reconstructs the origin of separate trait modules.

## 8. Final manuscript architecture

### Section 1 — Why compromise is not the only solution to a trade-off

Open generally. Many traits serve multiple functions or audiences. If the functions favour different trait states, the organism can either tolerate a compromise or alter its architecture so the functions become more separable.

The key distinction is:

```text
phenotypic compromise on one coordinate
versus
functional partitioning across coordinates
```

Immediately acknowledge the division-of-labor / pleiotropy literature and state that the present paper's aim is to connect that architecture problem to measurable ecological trait interactions and their causal identification.

### Section 2 — Shared-axis model

Define `W_S(z)` and the best compromise `W_S*`.

### Section 3 — Differentiated-axis model

Define `W_D(x,y)`, residual coupling `lambda`, architecture cost `K`, and the analytic `Delta_arch` threshold.

The first major result is the baseline boundary between compromise and differentiation.

### Section 4 — Robustness beyond the quadratic baseline

Test whether the qualitative boundary survives saturating, asymmetric and otherwise non-quadratic benefit/cost mappings. Distinguish what is structural from what is quadratic-specific.

### Section 5 — What happens after two axes exist?

Bring in the current BITA interaction logic. A two-axis architecture can still fail if the traits interfere, share costs or merely move the same trade-off into a different coordinate system.

Use `Delta_AD W` and the identified set to show that a positive two-trait interaction is not a mechanism label.

### Section 6 — Mechanism identification

Use the crossed-intervention framework to allocate the biological channels in the worked floral case. Keep the current 16-cell design, four-way separability diagnostic and independent joint-channel assay.

### Section 7 — Empirical reality check

Use the floral evidence as a stress test:

- recurrent conflicting pathways exist;
- distinct trait axes can change one another's functional returns;
- existing studies occupy complementary design faces;
- direct evidence for historical trait splitting remains limited.

### Section 8 — Discussion

Organize around three outcomes:

```text
1. balance: one trait remains at a compromise
2. differentiation: functions become partitioned across traits
3. incomplete differentiation: multiple traits exist but cross-talk/costs keep the trade-off coupled
```

## 9. Sister-paper non-overlap

| Question | SCH / Chapter 1 | BITA / Chapter 2 |
|---|---|---|
| Main problem | how conflicting demands balance on a shared trait | when the shared compromise gives way to trait differentiation |
| Architecture | one focal coordinate | comparison of shared versus multi-axis architecture |
| Main outcome | compromise / maintenance / context-dependent balance | functional differentiation / modularization |
| Floral pollinator–antagonist conflict | primary empirical realization | one worked case, not the scope |
| Two-trait interaction | not required | mechanistic subproblem after differentiation |
| Mechanism allocation | secondary | important for explaining how the differentiated architecture works |
| Historical transition | may motivate conflict persistence/change | required only if claiming observed evolutionary origin of differentiation |

## 10. What is already reusable

Do not throw away the mature BITA work. Reuse:

- the two-trait interaction estimand;
- nested interaction-relief / sign-crossing distinctions;
- identified-set and partial-identification algebra;
- crossed consumer design;
- independent joint-channel assay logic;
- 56/25 recurrence synthesis;
- 17-system fragmented identification frontier;
- Kessler, Egan, *Impatiens* and *Pedicularis* as mechanistic/design case studies;
- figure infrastructure where it can be nested under the new architecture story.

## 11. Remaining scientific work

Completed in this branch:

```text
A. shared-axis quadratic model
B. differentiated-axis quadratic model
C. analytic Delta_arch threshold
D. unit/regression tests for the baseline result
E. novelty audit against the closest specialization theory
```

Still required:

```text
F. non-quadratic robustness analysis
G. decide empirical ceiling:
   - floral mechanistic worked case only, or
   - add historical/comparative/experimental-evolution differentiation evidence
H. integrate the stable theory into the canonical manuscript
I. rebuild figures and submission package
```

Until F–H are complete, the previous 29-page + 12-page package should be treated as a mature component paper, not the final SCH sister Chapter 2.

## 12. Reader takeaway

The programme should ultimately close as:

> **SCH asks how a trait under conflicting demands finds a balance. BITA asks when evolution can stop compromising on that one trait and instead divide the functions among differentiated traits—and how we can identify the ecological mechanism once that division occurs.**
