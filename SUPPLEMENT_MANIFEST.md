# Supplement manifest — canonical trait-differentiation Chapter 2

Canonical target:

> **When does a trait trade-off resolve by differentiation rather than compromise? Linking trait architecture to mechanism identification**

Target journal/type: **Ecology — Concepts & Synthesis**.

## 1. Canonical sources

- Main scientific source: `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md`
- focused references: `manuscript/TRAIT_DIFFERENTIATION_REFERENCES_V1.md`
- figure captions: `manuscript/TRAIT_DIFFERENTIATION_FIGURE_CAPTIONS_V1.md`
- Main figures: `manuscript/trait_differentiation_figures/`
- architecture derivation: `theory/TRAIT_DIFFERENTIATION_EXTENSION.md`
- nonquadratic robustness: `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS.md`
- empirical architecture bridges: `docs/TRAIT_DIFFERENTIATION_EMPIRICAL_BRIDGES.md`
- retained floral identification supplement: `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md`
- canonical package builder: `scripts/build_ecology_review_package_sources.py`

`manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` remains a mature mechanistic component/provenance source; it is no longer the canonical article.

## 2. Scientific core

General nested-architecture result:

```text
recoverable shared-compromise loss  R >= 0
architecture gain                   Delta_arch = R - K
differentiation favoured            K < R
```

When residual coupling is a non-negative scaled penalty, stronger coupling cannot increase `R`.

Quadratic corollary:

```text
shared conflict load  L_S*
decoupling fraction   s
R = s L_S*
Delta_arch = s L_S* - K
```

The paper therefore distinguishes **balance on one axis**, **partial differentiation across axes**, and **mechanism identification after several axes exist**.

## 3. Robustness layer

Registered finite convex-family results:

```text
strict positive pre-cost recovery:         300 / 300
optimum-distance monotonic series:           60 / 60
coupling monotonicity implementation check:  60 / 60
```

These counts do not prove universality across arbitrary fitness landscapes.

## 4. Empirical architecture-state layer

- cichlid oral/pharyngeal jaws: structural functional partitioning with residual evolutionary/genetic integration;
- *Dalechampia*: repeated functional redeployment/exaptation and addition of structures.

These are bounded architecture-state anchors, not estimates of `s`, `lambda`, `K`, `Delta_arch`, or causal reconstructions of trait splitting.

## 5. Retained floral identification layer

The detailed worked case retains:

```text
Delta_AD W = W11 - W10 - W01 + W00
I(delta) = {(rho,iota,kappa): rho-iota-kappa=delta}
```

plus partial identification, the selective `A x D x antagonist x pollinator` design, `m0` handling, the four-way separability diagnostic, and an independent remaining-channel assay.

Empirical coverage:

```text
56 route records
25 independent biological clusters
17 high-information systems
```

This establishes recurrent constituent biology plus fragmented identification. It does not establish prevalence or historical differentiation.

## 6. Main figures

1. Figure 1 — shared-axis balance versus differentiated architecture; general `Delta_arch = R-K`, with the quadratic `R=sL_S*` corollary.
2. Figure 2 — quadratic architecture boundary `K=sL_S*` and the effect of incomplete decoupling.
3. Figure 3 — registered nonlinear robustness plus bounded cichlid/*Dalechampia* architecture-state anchors.
4. Figure 4 — once several axes exist, trait interaction still requires mechanism identification.
5. Figure 5 — floral recurrence and the 17-system fragmented identification frontier.

## 7. Appendix S1

The canonical Appendix combines:

- general shared-versus-differentiated architecture derivation;
- nonquadratic robustness design/readout;
- cross-system architecture-state evidence;
- the retained floral mechanism-identification supplement;
- Kessler reconstruction and *Impatiens* retrofit;
- 17-system identification frontier;
- 56/25 recurrence provenance;
- the historical 2,592 / 77.2% exercise as technical sensitivity only;
- continuous-limit and response-shape implementation checks.

Leal/Sasidharan and the theorem-led manuscript remain reproducible historical provenance, not Main Chapter 2 evidence.

## 8. Open Research package

Canonical exports include:

- `trait_differentiation_robustness_readout.json`;
- authoritative V2 `high_information_identification_coverage.csv`;
- aggregate `impatiens_identification_retrofit.json`.

The broader route corpus and source receipts remain in the public repository. A permanent archive of the accepted exact version is an acceptance-stage task.

## 9. Validated rendered state

```text
Main Document: 30 pages
Appendix S1:   38 pages
Main figures:   5
```

The promoted Chapter 2 candidate has passed CI and package builds and is within the standard 30-page Main target. Full visual QA found and corrected a LibreOffice OMML superscript-star fallback; optimized quantities are now rendered explicitly with `opt` superscripts. No intentional blank figure pages remain.

## 10. External-submission boundary

Remaining fields are author-controlled: author list/order, affiliations, corresponding author/e-mail, ORCIDs, CRediT, funding, acknowledgments, competing interests, licence and any portal-requested reviewer information. After insertion, rebuild and visually inspect the exact submitted files again.
