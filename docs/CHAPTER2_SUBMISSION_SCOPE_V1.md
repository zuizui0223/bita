# Chapter 2 submission scope v1

## Status

This is the promotion contract for the SCH sister Chapter 2 reframe. It does not replace `docs/SUBMISSION_SCOPE.md` until the integrated manuscript passes all promotion gates.

Active integration candidate:

```text
manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
```

Preserved mature component/canonical source for the old validated package:

```text
manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md
```

## Paper-level question

> **When does a trait trade-off resolve by differentiation rather than compromise, and how can the ecological mechanism of a multi-trait architecture be identified once differentiation exists?**

The paper is general at the trait-architecture level. Floral attraction/defence is the detailed mechanism-identification worked case, not the definition of the general theory.

## Main result ceiling

### Architecture layer

Quadratic baseline:

```text
shared conflict load       L_S*
decoupling fraction        s
extra architecture cost    K

recoverable conflict loss  R = s L_S*
architecture gain          Delta_arch = s L_S* - K
```

Promotable claim:

> Within the quadratic baseline, differentiation is favoured exactly when the fraction of shared-axis conflict loss recoverable under residual coupling exceeds the extra architecture cost.

### Robustness layer

Promotable claim:

> The qualitative boundary persists across the declared finite convex power-loss family: 300/300 nonzero-conflict evaluations have positive pre-cost recoverable loss, conflict-distance monotonicity holds in 60/60 declared series, and coupling monotonicity in 60/60 series.

Prohibited expansion:

- no universality claim over arbitrary nonconvex or frequency-dependent landscapes;
- no evolutionary-dynamics claim from optimized-state comparison alone.

### Architecture-state empirical layer

Promotable claim:

- cichlid oral/pharyngeal jaws demonstrate structural/function partitioning with residual evolutionary/genetic integration;
- *Dalechampia* demonstrates historical redeployment/exaptation and addition of functional lines.

Prohibited expansion:

- neither system estimates `s`, `lambda`, `K` or `Delta_arch`;
- neither is treated as a direct causal test that the modeled trade-off generated the historical transition.

### Mechanism-identification layer

Promotable existing results:

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
!= prevalence of modular architectures
```

## Novelty ceiling

Do not claim novelty for:

- multifunctionality;
- functional specialization;
- division of labour;
- pleiotropy versus specialization;
- modularity as a solution to functional trade-offs.

The intended contribution is the integration:

```text
measured one-axis compromise
-> architecture gain with explicit partial decoupling
-> channel-resolved inference after multiple axes exist.
```

## Main figure ceiling

Target five figures:

1. shared balance versus differentiated architecture + `Delta_arch = s L_S* - K`;
2. architecture boundary `K = s L_S*`;
3. registered nonquadratic robustness + bounded empirical architecture-state anchors;
4. multi-trait interaction -> identified set -> crossed intervention -> joint-channel assay;
5. floral recurrence + 17-system fragmented identification frontier.

The old five identification figures remain provenance sources and may be compressed/relegated to Appendix S1 rather than deleted.

## Promotion gates

The integrated manuscript becomes canonical only after all of the following are true:

```text
[ ] integrated manuscript narrative regression tests pass
[ ] trait differentiation theory/unit tests pass
[ ] robustness tests pass
[ ] new SVG figures parse and narrative guards pass
[ ] source-checked Chapter 2 bibliography is complete
[ ] every in-text named source resolves to the focused bibliography or Supporting Information
[ ] Figures 4-5 are integrated from the old identification assets
[ ] old and new inference ceilings are reconciled in one claim-freeze file
[ ] submission-scope docs and checklist are synchronized atomically
[ ] Main + Appendix rebuild succeeds
[ ] every rendered page is visually inspected
```

Until then, do not repoint the existing submission build to the integrated draft.

## Merge rule

PR #157 can be merged to `main` as a **scientific development reframe** before final submission packaging if CI and scope tests are green, because the old canonical manuscript remains preserved. However, merging the PR must not be interpreted as declaring the integrated Chapter 2 manuscript submission-ready.

## Reader takeaway

> **Chapter 1 asks how conflicting functions balance on one trait. Chapter 2 asks when enough of that compromise can be released by partial trait differentiation to pay for a new architecture, then asks what ecological mechanism makes the multi-trait phenotype work.**
