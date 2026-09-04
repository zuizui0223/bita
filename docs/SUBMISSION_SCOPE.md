# Submission scope — canonical SCH sister Chapter 2

Primary target: **Ecology — Concepts & Synthesis**.

Canonical question:

> **When does a trait trade-off resolve by differentiation rather than compromise, and how can the ecological mechanism of the resulting multi-trait architecture be identified?**

The programme is defined by trait architecture, not by pollination versus defence.

```text
SCH / Chapter 1 — BALANCE
conflicting functions remain coupled on one trait axis
-> characterize the maintained compromise

BITA / Chapter 2 — DIFFERENTIATION
compare that shared compromise with a partially decoupled multi-axis architecture
-> determine when differentiation pays
-> identify the mechanism once multiple axes exist
```

Floral attraction/defence is the detailed mechanism-identification worked case, not the general scope.

## 1. General architecture result

Let `L_S*` be the minimum loss attainable when two functions must share one trait. Let the differentiated architecture contain every shared phenotype on its diagonal before an extra fixed architecture cost is charged. Define `R` as the loss recovered by optimizing over the larger differentiated phenotype space.

Then, structurally,

```text
R >= 0
Delta_arch = R - K
Delta_arch > 0  <=>  K < R
```

where `K >= 0` is the additional fixed architecture cost.

If residual coupling enters as a non-negative scaled penalty `lambda*c(x,y)`, increasing `lambda` cannot increase `R`. These weak-dominance and coupling-monotonicity results are not quadratic-specific.

## 2. Quadratic corollary

For the declared quadratic baseline,

```text
shared conflict load       L_S*
decoupling fraction        s = |x_opt-y_opt| / |theta1-theta2|
recoverable loss           R = s L_S*
architecture gain          Delta_arch = s L_S* - K
```

so the decision boundary is

```text
K = s L_S*.
```

This closed form makes incomplete differentiation explicit: two trait axes can relax a conflict while retaining residual functional, developmental, genetic or ecological coupling.

## 3. Nonquadratic robustness ceiling

The registered convex power-loss design contains 300 nonzero-conflict evaluations across four functional powers, three weighting schemes, five optimum distances and five residual-coupling strengths, plus mismatched-curvature checks.

Current finite-family results:

```text
strict positive pre-cost recovery:                 300 / 300
recovery increases with optimum separation:         60 / 60 declared series
coupling monotonicity implementation check:          60 / 60 declared series
```

The first and optimum-distance results establish strictness only for the declared convex family. The coupling result numerically verifies the structural proposition. No claim is made for arbitrary nonconvex, multimodal, frequency-dependent or evolutionary-dynamic landscapes.

## 4. Empirical architecture-state ceiling

- Cichlid oral/pharyngeal jaws anchor partial differentiation with residual evolutionary/genetic integration.
- *Dalechampia* anchors historical functional redeployment, exaptation and addition of functional structures.

These systems demonstrate biologically real architecture states. They do not estimate `s`, `lambda`, `K` or `Delta_arch`, and they do not prove that a measured shared-axis trade-off caused the historical transition.

## 5. Floral mechanism-identification worked case

Once multiple axes exist, their total fitness interaction still does not identify mechanism. For the focal floral traits `A` and `D`,

```text
Delta_AD W = W11 - W10 - W01 + W00
Delta_AD W = rho_delta - iota_delta - kappa_delta
```

and a measured total `delta` defines

```text
I(delta) = {(rho,iota,kappa): rho-iota-kappa=delta}
```

rather than a unique mechanism.

The retained inference ladder is:

```text
interaction detection
-> identified set
-> partial identification under declared restrictions
-> selective A x D x antagonist x pollinator intervention
-> m0 handling + four-way separability diagnostic
-> independent assay of the remaining joint channel
```

Existing evidence contributes 56 source-adjudicated route records across 25 independent biological clusters and a 17-system high-information frontier. The pathways recur, but the required identification dimensions remain fragmented across experiments. These numbers do not estimate the prevalence or historical origin of differentiated architectures.

## 6. Required boundaries

```text
one-trait compromise
!= proof that differentiation evolved

structural separation
!= functional independence

positive A x D interaction
!= trait differentiation
!= historical splitting

route recurrence
!= prevalence
!= total cross-trait mechanism
```

The current paper compares optimized architecture states; it does not model mutation, inheritance, transition time or evolutionary accessibility. A causal historical claim that one shared-axis conflict produced a particular new module requires additional transition evidence.

## 7. Canonical source graph

- Main scientific source: `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md`
- focused reference pool: `manuscript/TRAIT_DIFFERENTIATION_REFERENCES_V1.md`
- captions: `manuscript/TRAIT_DIFFERENTIATION_FIGURE_CAPTIONS_V1.md`
- Figures 1–5: `manuscript/trait_differentiation_figures/`
- theory derivation: `theory/TRAIT_DIFFERENTIATION_EXTENSION.md`
- robustness: `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS.md`
- canonical package builder: `scripts/build_ecology_review_package_sources.py`
- retained identification supplement: `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md`

`manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` remains versioned as the mature mechanistic component/provenance source; it is no longer the canonical submitted article.

## 8. Validated pre-metadata package

The promoted candidate has passed theory, manuscript, figure, identification and packaging regressions and renders as:

```text
Main Document: 30 pages
Appendix S1:   38 pages
Main figures:   5
```

The Main is within the standard 30-page Ecology Concepts & Synthesis target. The renderer-specific superscript-star failure has been normalized to explicit `opt` notation in OMML math before PDF export.

## 9. Remaining external-submission boundary

Only author-controlled metadata/declarations and final post-metadata QA remain: final author list/order, affiliations, corresponding author/e-mail, ORCIDs, CRediT, funding, acknowledgments, competing interests, licence, portal-requested reviewer fields if any, all-author approval and no-simultaneous-submission confirmation. After those fields are inserted, rebuild and visually inspect the exact submitted package again.
