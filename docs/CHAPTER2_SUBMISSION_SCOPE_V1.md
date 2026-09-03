# Chapter 2 submission scope v1

## Status

This is the promotion contract for the SCH sister Chapter 2 reframe. It does not replace `docs/SUBMISSION_SCOPE.md` until the integrated candidate passes the promotion gates.

Active integration source:

```text
manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
```

Candidate review artifact is assembled by:

```text
scripts/build_trait_differentiation_candidate_package_sources.py
.github/workflows/build-trait-differentiation-candidate.yml
```

Preserved mature canonical source for the old validated package:

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

with

```text
lambda >= 0
c(x,y) >= 0
c(z,z) = 0,
```

the differentiated architecture contains the shared phenotype as a diagonal special case. Therefore

```text
R(lambda) = L_S* - L_D0*(lambda) >= 0.
```

With an additional fixed architecture cost `K >= 0`,

```text
Delta_arch = R - K
```

and differentiation is favoured exactly when `K < R`.

If coupling enters as the non-negative scaled penalty `lambda c(x,y)`, then

```text
lambda2 > lambda1
=> R(lambda2) <= R(lambda1).
```

Promotable claim:

> A nested differentiated architecture weakly enlarges the attainable phenotype set before its additional fixed cost is charged, and stronger declared non-negative residual coupling cannot increase the amount of shared-axis compromise loss that can be recovered.

Claim ceiling:
- weak dominance, not universal strict improvement;
- applies only when the differentiated architecture genuinely contains the shared state under the declared variable-cost parameterization;
- signed/synergistic coupling outside `c>=0` is not covered;
- optimized-state comparison is not an evolutionary trajectory.

### Layer 2 — quadratic corollary

Quadratic baseline:

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

Prohibited expansion:
- no strict-universality claim over arbitrary nonconvex, frequency-dependent or multimodal landscapes;
- no universal optimum-distance theorem outside the declared family;
- no evolutionary-dynamics claim from optimized-state comparison alone.

### Layer 4 — architecture-state empirical anchors

Promotable claim:

- cichlid oral/pharyngeal jaws demonstrate structural/function partitioning with residual evolutionary/genetic integration;
- *Dalechampia* demonstrates historical redeployment/exaptation and addition of functional structures.

Prohibited expansion:

- neither system estimates `s`, `lambda`, `K`, `R` or `Delta_arch`;
- neither is treated as a direct causal test that the modeled one-axis conflict generated the historical transition.

### Layer 5 — mechanism identification after multiple axes exist

Promotable existing BITA results:

- discrete two-trait `Delta_AD W` and Level 1/2/3 outcome distinctions;
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

Do not claim novelty for:

- multifunctionality;
- functional specialization;
- division of labour;
- pleiotropy versus specialization;
- modularity as a solution to functional trade-offs;
- the elementary fact that a larger feasible set weakly improves an optimum.

The intended contribution is the empirical/inferential integration:

```text
measured one-axis compromise
-> recoverable loss under partial decoupling
-> architecture-cost threshold
-> channel-resolved inference after multiple axes exist.
```

## Main figure ceiling

Target five figures:

1. shared balance versus differentiated architecture; general `Delta_arch=R-K`, with quadratic `R=sL_S*` explicitly labelled as a corollary;
2. quadratic boundary `K=sL_S*`, explicitly not a universal linear boundary;
3. registered nonquadratic strictness/conflict-distance results + coupling-proposition implementation check + bounded architecture-state anchors;
4. multi-trait interaction -> identified set -> crossed intervention -> joint-channel assay;
5. floral recurrence + 17-system fragmented identification frontier.

The old five identification figures remain provenance sources and may be compressed/relegated to Appendix S1 rather than deleted.

## Promotion gates

The integrated manuscript becomes canonical only after all of the following are true:

```text
[ ] candidate narrative/package regression tests execute green
[ ] trait differentiation theory/unit tests execute green
[ ] robustness tests execute green
[ ] new SVG figures parse and narrative guards execute green
[ ] focused Main bibliography resolves exactly to the admitted source set
[ ] candidate uses authoritative V2 identification-coverage matrix
[ ] Main + Appendix candidate DOCX/PDF build succeeds
[ ] Main page count is recorded against Ecology C&S 30-page target / 50-page ceiling
[ ] rendered candidate Main and Appendix receive page-by-page visual QA
[ ] canonical manuscript/reference/figure/build pointers are synchronized atomically
[ ] post-promotion canonical package rebuild succeeds
[ ] post-promotion rendered pages receive final visual QA
```

GitHub Actions execution is currently an external gate; static source integration continues while those jobs remain queued.

## Journal target

Primary target remains **Ecology — Concepts & Synthesis**. Current rationale is recorded in `docs/CHAPTER2_TARGET_JOURNAL_STRATEGY_V1.md`.

The manuscript should first target the standard 30-page Main limit. If the integrated candidate exceeds 30 but remains at or below the 50-page C&S maximum, the cover letter must justify both broad ecological contribution and the need for the additional Main-text length.

## Merge rule

PR #157 can be merged to `main` as a scientific development reframe only after the branch-level CI/scope regressions are green. Merging the development PR does not itself declare the new Chapter 2 review artifact submission-ready unless the promotion gates above are also closed.

## Reader takeaway

> **Chapter 1 asks how conflicting functions balance on one trait. Chapter 2 asks how much of that compromise becomes recoverable when functions can separate only partially, whether the recovered amount pays for the extra architecture, and what ecological mechanism makes the resulting multi-trait phenotype work.**
