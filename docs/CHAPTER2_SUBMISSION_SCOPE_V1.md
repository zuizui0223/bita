# Chapter 2 submission scope v1

## Status — PROMOTION GATES CLOSED

This document is now the promotion receipt for the SCH sister Chapter 2 reframe. The integrated trait-differentiation manuscript has passed the promotion gates and `docs/SUBMISSION_SCOPE.md` is the canonical live submission scope.

Canonical integration source:

```text
manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
```

Canonical review artifact is assembled by:

```text
scripts/build_ecology_review_package_sources.py
.github/workflows/build-ecology-submission-package.yml
```

The independent pre-promotion validator remains:

```text
scripts/build_trait_differentiation_candidate_package_sources.py
.github/workflows/build-trait-differentiation-candidate.yml
```

Preserved mature component/provenance source:

```text
manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md
```

## Paper-level question

> **When does a trait trade-off resolve by differentiation rather than compromise, and how can the ecological mechanism of a multi-trait architecture be identified once multiple axes exist?**

The paper is general at the trait-architecture level. Floral attraction/defence is the detailed mechanism-identification worked case, not the definition of the general theory.

## Main result ceiling

### Layer 1 — structural architecture results

For a shared loss

```text
L_S(z) = l1(z) + l2(z)
L_S*   = min_z L_S(z)
```

and a differentiated pre-fixed-cost loss

```text
L_D0(x,y;lambda) = l1(x) + l2(y) + lambda c(x,y)
```

with `lambda >= 0`, `c(x,y) >= 0`, and `c(z,z) = 0`, the differentiated architecture contains the shared phenotype as a diagonal special case. Therefore

```text
R(lambda) = L_S* - L_D0*(lambda) >= 0.
Delta_arch = R - K.
```

Differentiation is favoured exactly when `K < R`. If coupling enters as the non-negative scaled penalty `lambda c(x,y)`, then stronger coupling cannot increase `R`.

Claim ceiling:
- weak dominance, not universal strict improvement;
- applies only when the differentiated architecture genuinely contains the shared state under the declared variable-cost parameterization;
- signed/synergistic coupling outside `c>=0` is not covered;
- optimized-state comparison is not an evolutionary trajectory.

### Layer 2 — quadratic corollary

```text
shared conflict load       L_S*
decoupling fraction        s
extra architecture cost    K
recoverable conflict loss  R = s L_S*
architecture gain          Delta_arch = s L_S* - K
```

Promotable claim:

> In the quadratic baseline, the fraction of function-specific phenotypic separation that survives residual coupling is also the fraction of shared-axis conflict loss that remains recoverable; differentiation is favoured exactly when `K < s L_S*`.

Do not present `R=sL_S*` or the linear boundary `K=sL_S*` as a shape-independent identity.

### Layer 3 — finite nonquadratic robustness

Registered matched-curvature design:

```text
300 nonzero-conflict convex power-loss evaluations
60 conflict-distance series
60 coupling series
```

Promotable finite-family results:
- strict `R > 0` in 300/300 evaluations;
- larger optimum separation increases `R` in 60/60 declared series;
- coupling monotonicity is recovered in 60/60 series as an implementation check of Layer 1, not its proof;
- mismatched-curvature checks switch architecture preference immediately below/above the fixed-cost threshold.

No strict universality is claimed over arbitrary nonconvex, frequency-dependent or multimodal landscapes.

### Layer 4 — architecture-state empirical anchors

- cichlid oral/pharyngeal jaws demonstrate structural/function partitioning with residual evolutionary/genetic integration;
- *Dalechampia* demonstrates historical redeployment/exaptation and addition of functional structures.

Neither system estimates `s`, `lambda`, `K`, `R` or `Delta_arch`, and neither is treated as a direct causal test that the modeled one-axis conflict generated the historical transition.

### Layer 5 — mechanism identification after multiple axes exist

Promotable existing BITA results:
- discrete two-trait `Delta_AD W` and nested outcome distinctions;
- identified-set / partial-identification logic;
- crossed trait-by-consumer allocation design;
- four-way separability diagnostic;
- independent remaining-channel assay requirement;
- 56 route records / 25 independent biological clusters;
- 17-system fragmented identification frontier;
- registered Kessler/Egan/*Impatiens* bounded reconstructions.

Prohibited expansion:

```text
positive A x D interaction
!= origin of differentiation
!= historical splitting
!= prevalence of modular architectures.
```

## Novelty ceiling

Do not claim novelty for multifunctionality, functional specialization, division of labour, pleiotropy versus specialization, modularity as a solution to functional trade-offs, or the elementary feasible-set weak-dominance fact.

The intended contribution is the empirical/inferential integration:

```text
measured one-axis compromise
-> recoverable loss under partial decoupling
-> architecture-cost threshold
-> channel-resolved inference after multiple axes exist.
```

## Main figure ceiling

1. shared balance versus differentiated architecture; general `Delta_arch=R-K`, with quadratic `R=sL_S*` explicitly labelled as a corollary;
2. quadratic boundary `K=sL_S*`, explicitly not a universal linear boundary;
3. registered nonquadratic strictness/conflict-distance results + coupling-proposition implementation check + bounded architecture-state anchors;
4. multi-trait interaction -> identified set -> crossed intervention -> joint-channel assay;
5. floral recurrence + 17-system fragmented identification frontier.

The old five identification figures remain provenance sources and are not deleted.

## Promotion gates — CLOSED

```text
[x] candidate narrative/package regression tests execute green
[x] trait differentiation theory/unit tests execute green
[x] robustness tests execute green
[x] new SVG figures parse and narrative guards execute green
[x] focused Main bibliography resolves to the admitted source set
[x] candidate uses authoritative V2 identification-coverage matrix
[x] Main + Appendix candidate DOCX/PDF build succeeds
[x] Main page count recorded against Ecology C&S target / ceiling
[x] rendered candidate Main and Appendix receive page-by-page visual QA
[x] canonical manuscript/reference/figure/build pointers synchronized
[x] post-promotion canonical package rebuild succeeds
[x] post-promotion rendered pages receive final visual QA
```

Validated pre-metadata canonical package:

```text
Main Document: 30 pages
Appendix S1:   38 pages
Main figures:   5
full visual QA: 68/68 pages PASS
```

## Journal target

Primary target is **Ecology — Concepts & Synthesis**. Current rationale is recorded in `docs/CHAPTER2_TARGET_JOURNAL_STRATEGY_V1.md` and `submission/TARGET_JOURNAL_STRATEGY.md`.

## Merge rule

PR #157 is eligible to merge to `main` once the branch-level final CI/scope/package checks are green. Canonical promotion itself is complete; the remaining pre-upload blockers are human-controlled metadata/declarations and a final post-metadata rebuild.

## Reader takeaway

> **Chapter 1 asks how conflicting functions balance on one trait. Chapter 2 asks how much of that compromise becomes recoverable when functions can separate only partially, whether the recovered amount pays for the extra architecture, and what ecological mechanism makes the resulting multi-trait phenotype work.**
