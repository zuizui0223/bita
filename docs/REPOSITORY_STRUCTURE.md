# Repository structure and source-of-truth policy

This repository is in **Chapter 2 integration mode**. The mature identification manuscript and package remain preserved while a broader SCH-sister manuscript is validated around the transition from shared-trait balance to trait differentiation.

## 1. Two source states during the reframe

### Preserved canonical source for the old validated package

Until promotion gates are complete, the existing submission build continues to point to:

- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md` — mature two-trait mechanism-identification article;
- `manuscript/IDENTIFICATION_DESIGN_REFERENCES.md` — its focused reference spine;
- `manuscript/identification_figures/` — its five validated Main figures;
- `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md` — its active Appendix S1.

This package is preserved as a scientifically valid component/provenance source. It is **not** the final SCH sister Chapter 2 after the balance-to-differentiation reframe.

### Active Chapter 2 integration candidate

The new programme-level manuscript state is defined by:

- `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md` — integrated draft: balance -> differentiation -> mechanism identification;
- `manuscript/TRAIT_DIFFERENTIATION_REFERENCES_V1.md` — merged architecture + floral reference spine;
- `manuscript/TRAIT_DIFFERENTIATION_FIGURE_PLAN_V1.md` — five-figure integrated argument;
- `manuscript/TRAIT_DIFFERENTIATION_FIGURE_CAPTIONS_V1.md` — caption draft;
- `manuscript/trait_differentiation_figures/` — five integrated SVG sources;
- `manuscript/CLAIM_FREEZE.md` — active scientific claim ceiling for the reframe;
- `docs/CHAPTER2_SUBMISSION_SCOPE_V1.md` — promotion contract that must pass before canonical repointing.

`manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md`, earlier tables/figures and historical Leal/Sasidharan products remain versioned for provenance and lower-ceiling supporting analyses. They do not override the active claim freeze.

## 2. SCH / BITA scientific spine

The programme is defined at the trait-architecture level:

```text
SCH / Chapter 1 — BALANCE
conflicting functions remain coupled on one trait axis
-> characterize the maintained compromise

BITA / Chapter 2 — DIFFERENTIATION
compare the best shared compromise with a partially decoupled multi-axis architecture
-> determine when differentiation pays
-> identify the mechanism once multiple axes exist
```

Pollinator-antagonist floral conflict is one empirical realization, not the general definition of either chapter.

## 3. Chapter 2 theory implementation

Primary new theory modules:

- `trait_architecture/differentiation.py` — analytic quadratic shared-versus-differentiated architecture model;
- `trait_architecture/differentiation_robustness.py` — deterministic convex power-loss robustness model;
- `theory/TRAIT_DIFFERENTIATION_EXTENSION.md` — derivation and inference limits;
- `scripts/analyze_trait_differentiation_robustness.py` — registered finite sweep;
- `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS_READOUT.json` — machine-readable registered result;
- `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS.md` — result interpretation and claim ceiling.

The reader-facing quadratic identity is

```text
shared conflict load       L_S*
decoupling fraction        s
architecture cost          K

recoverable conflict loss  R = s L_S*
architecture gain          Delta_arch = s L_S* - K
```

where

```text
s = |x* - y*| / |theta1 - theta2|
  = w1*w2 / [w1*w2 + lambda*(w1+w2)].
```

The same factor `s` is both the retained function-specific trait separation and the fraction of shared-axis compromise loss recovered before paying `K` in the quadratic baseline.

## 4. Robustness and empirical architecture-state layers

The registered convex-family robustness layer contains 300 matched-curvature evaluations and additional mismatched-curvature checks. Its finite claim ceiling is documented in `docs/TRAIT_DIFFERENTIATION_ROBUSTNESS.md`.

Non-floral architecture-state anchors are documented in:

- `docs/TRAIT_DIFFERENTIATION_POSITIONING.md` — prior specialization/multifunctionality theory and novelty boundary;
- `docs/TRAIT_DIFFERENTIATION_EMPIRICAL_BRIDGES.md` — cichlid partial differentiation and *Dalechampia* historical role redeployment.

These empirical systems establish biological reality of partial differentiation/reorganization. They are not estimates of `s`, `lambda`, `K`, or `Delta_arch` and are not causal reconstructions of the origin of a second trait axis.

## 5. Existing BITA mechanism-identification layer

The mature identification implementation remains active because it answers the second-stage question after multiple axes exist.

Primary modules:

- `identification.py` — discrete crossed-intervention estimands and causal gates;
- `partial_identification.py` — identified sets and assumption-indexed bounds;
- `model.py` — declared biological parameterization and parameter constraints;
- `sign_criterion.py` — local sign logic and orientation-facing quantities;
- `robustness.py` — historical mixed-partial decomposition and response-shape robustness;
- `theory_evidence_interface.py` / `theory_meta_validation.py` — theory-to-evidence boundary checks.

Reusable scientific results include:

- `Delta_AD W` and the interaction-relief / functional-release / strict-reversal hierarchy;
- identified-set and partial-identification geometry;
- crossed `A x D x antagonist x pollinator` channel allocation;
- four-way separability diagnostic;
- independent joint-channel assay;
- 56 route records / 25 independent biological clusters;
- 17-system fragmented identification frontier.

These results identify how a multi-trait architecture functions; they do not establish its historical origin.

## 6. Empirical evidence directories

### `empirical/mechanism_pattern_synthesis/`

Retained recurrence/provenance layer: route ledgers, system audits, context/sign-switch records, saturation receipts, direct-design audits and quantitative-module receipts. Marginal routes establish recurrence and do not identify channel interactions or prevalence of differentiated architectures.

### `empirical/identification_design/`

Active floral identification layer: high-information system audit, direct interaction anchors, public-data retrofit and source-package receipts.

### External SCH companion

The first-order shared-axis balance/shared-cue programme lives in [SCH](https://github.com/zuizui0223/sch). BITA uses that problem as the Chapter 1 antecedent but does not duplicate SCH's one-trait estimands or historical shared/private-cue ladder.

### `empirical/broad_reality_evidence/`

Source recovery, screening, extraction and provenance products required by historical or retained synthesis modules. This is provenance/supporting infrastructure rather than a competing manuscript source of truth.

## 7. Tests and regression graph

New Chapter 2 guards include:

- `tests/test_trait_differentiation.py` — analytic architecture identities and comparative statics;
- `tests/test_trait_differentiation_robustness.py` — nonquadratic robustness and quadratic/numerical agreement;
- `tests/test_trait_differentiation_manuscript.py` — integrated manuscript claim/narrative ceiling;
- `tests/test_trait_differentiation_figures.py` — integrated SVG validity and message ceiling;
- updated `tests/test_claim_freeze.py` — preserves historical theorem checks while guarding the new balance-to-differentiation mainline.

Historical identification/theorem regressions remain active because the integrated paper reuses those analyses at a lower or worked-case claim level.

## 8. Workflow policy

Keep workflows active when they validate:

1. active or preserved core theory;
2. a manuscript/supplement asset on either the preserved canonical graph or Chapter 2 promotion graph;
3. an admitted empirical reconstruction/source receipt;
4. a submission-facing reproducibility contract.

Do not repoint the existing submission builder to `MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md` until the explicit promotion gates in `docs/CHAPTER2_SUBMISSION_SCOPE_V1.md` are closed.

## 9. Graph-integrity policy

During the reframe there are two intentional graphs:

```text
PRESERVED PACKAGE
MANUSCRIPT_IDENTIFICATION_DESIGN
    <- existing figures/builders
    <- identification + empirical inputs
    <- regression tests / provenance

CHAPTER 2 PROMOTION GRAPH
MANUSCRIPT_TRAIT_DIFFERENTIATION_V1
    <- new architecture figures + focused references
    <- differentiation theory + robustness
    <- preserved identification module
    <- cross-system architecture-state evidence
    <- new + historical regression tests
```

The graphs converge only after promotion QA. This avoids destroying a validated paper while the broader sister-paper integration is still being checked.

## 10. Change policy

Classify changes before implementation:

- **Editorial:** wording, flow, titles, captions, reference formatting.
- **Reproducibility:** tests, deterministic builders, provenance receipts, graph documentation.
- **Scientific correction:** changed estimate, derivation, admitted evidence or inference ceiling; requires downstream revalidation.
- **New discovery:** new model family or empirical programme; admissible only when it directly advances the Chapter 2 question and its claim ceiling is explicit.

The present branch is a substantive scientific reframe because it adds an architecture comparison and robustness layer. It deliberately preserves the old manuscript until the new graph is validated.

## 11. Current endpoint

The current Chapter 2 integration supports the staged claim:

```text
shared-axis compromise
-> architecture gain = recoverable conflict loss - extra architecture cost
-> partial differentiation under residual coupling
-> multi-trait interaction detection
-> identified set / partial identification
-> selective mechanism identification.
```

It does not claim that every multifunctional trade-off evolves toward modularity or that the floral two-trait corpus reconstructs a historical splitting event.
