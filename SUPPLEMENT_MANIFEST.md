# Supplement manifest — canonical identification-design paper

This manifest maps the current main-line submission target:

> **From floral trait interactions to mechanism identification: a crossed-intervention framework for attraction and defence**

The historical theorem-led Mechanism → Pattern manuscript and its analyses remain versioned in the repository for provenance, but they no longer define the intended Main Document.

## 1. Canonical reader-facing sources

- Main scientific source: `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- focused references: `manuscript/IDENTIFICATION_DESIGN_REFERENCES.md`
- figure captions: `manuscript/IDENTIFICATION_DESIGN_FIGURE_CAPTIONS.md`
- Supplement: `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md`
- canonical review-package wrapper: `scripts/build_ecology_review_package_sources.py`
- standard output directory: `submission/ecology/generated/`

Primary identification implementation:

- `trait_architecture/identification.py`
- associated identification regression tests
- `empirical/identification_design/HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv`
- `empirical/identification_design/IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json`
- `empirical/identification_design/IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.md`

## 2. Canonical scientific core

The primary experimental estimand is the two-level secant interaction

```text
Delta_AD W = W11 - W10 - W01 + W00
```

The Main contribution is not the algebraic identity itself. It is the identification sequence:

```text
trait interaction detection
→ observational non-identifiability of channel allocation
→ crossed A × D × antagonist × pollinator interventions
→ pollinator-absent baseline correction
→ A×D×G×P separability diagnostic
→ independent A×D joint-cost assay
→ hidden/unallocated-channel sign diagnostic
```

Required boundaries:

- a total `Delta_AD W` does not identify rho, iota, or kappa;
- the 16-cell design is not sufficient unless consumer interventions are selective and A/D coordinates remain comparable across cells;
- the rho- and iota-invariance views are one four-way contrast up to sign;
- a non-zero four-way contrast rejects the simple separable-channel representation;
- the pollinator-dependent increment is not total iota until the pollinator-absent `m0_delta` term is handled;
- `U_delta = rho_delta - iota_delta - Delta_AD W` is an unallocated residual, not kappa by definition;
- kappa requires an independent allocation/construction-cost assay;
- the elementary inequality is used only as a post-measurement consistency/sign diagnostic.

## 3. Existing-data identification stress tests

### Kessler et al. 2008 — trait-factorial anchor

The source experimentally crosses floral benzylacetone and nicotine production. Published aggregate female-outcrossing constraints imply:

```text
probability-scale Delta_AD: approximately +0.19 to +0.25
logit interaction:          approximately +1.019 to +1.551
interaction OR:             approximately 2.77 to 4.71
```

The sign is robust within the published aggregate constraints, but formal interaction uncertainty is unrecovered and nicotine silencing is systemic. This is therefore the closest current trait-factorial anchor, not full mechanism allocation.

### Egan et al. 2021 — consumer-factorial anchor

Herbivory and pollination environment are crossed, but the focal floral attraction and defence traits are not independently manipulated as the required A×D factorial. This supplies the complementary design half rather than full identification.

### Soper Gorden & Adler 2018 — public-data retrofit

The Dryad-backed Impatiens analysis estimates observational A×D plus randomized Robbing/Florivory/Pollination modification. All eight targeted HC3 95% intervals cross zero. The analysis reaches total-interaction/context-modification estimation but not rho/iota/kappa identification because A/D are observational and the randomized treatments are intensity additions rather than selective consumer exclusions.

### Other near misses

- Kessler et al. 2015: genuine floral 2×2 phenotype, but nectar reward is not independently justified D; publisher supplementary ZIP contains three TIFFs and no obvious machine-readable source table.
- Sun & Huang 2015, *Pedicularis rex*: useful selective-access/physical-defence system anchor, but no independent A manipulation.

Across the current **16-system high-information screened set**:

```text
independent joint-cost assay:   0
full rho/iota/kappa identification: 0
```

These are coverage statements for the screened set, not literature-prevalence estimates.

## 4. Canonical Main figures

Reader-facing numbering is now:

1. `manuscript/identification_figures/FIGURE_1_IDENTIFICATION_DESIGN.svg` — total trait interaction versus mechanism allocation.
2. `manuscript/identification_figures/FIGURE_2_IDENTIFICATION_DESIGN.svg` — 16-cell crossed design and separability diagnostic.
3. `manuscript/identification_figures/FIGURE_3_IDENTIFICATION_DESIGN.svg` — independent joint-cost assay and hidden-channel diagnostic.
4. `manuscript/identification_figures/FIGURE_4_IDENTIFICATION_DESIGN.svg` — Kessler 2008 / Egan 2021 / Impatiens / identification-coverage evidence.
5. `manuscript/identification_figures/FIGURE_5_IDENTIFICATION_DESIGN.svg` — executable experiment roadmap.

The historical mechanism/regime/Pattern/quantitative/same-system figures remain versioned but are not the intended canonical Main figure set.

## 5. Canonical Supplement boundary

`manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md` retains technical and provenance material that no longer belongs in the Main narrative, including:

- 2,592 finite evaluations as implementation/model-family sensitivity only;
- 77.2% finite-design window precision, explicitly grid-dependent and not ecological prevalence;
- continuous-limit / finite-difference implementation checks;
- response-shape sensitivity maps;
- Kessler 2008 aggregate reconstruction and uncertainty boundary;
- Impatiens retrofit details;
- the high-information identification coverage audit;
- historical Mechanism → Pattern records needed for provenance.

Leal and Sasidharan quantitative modules remain reproducible repository analyses but are not Main results in the identification-design paper.

## 6. Historical quantitative provenance retained

The Leal et al. 2025 floral-larceny module remains pinned to immutable provenance even though it is no longer a Main identification-design result:

```text
canonical commit:   ed33b25593c0d90ad6657753f6f5501d9efc7b82
preregistration:    0e36eac
first results:      965d657
source synthesis:   Leal et al. 2025, Ecology, doi:10.1002/ecy.70036
```

Historical reproduced values remain:

```text
female reproductive success  LRR -0.210  48 independent clusters
nectar standing crop          LRR -0.483  28
legitimate visitation         LRR -0.291  22
```

These records are preserved for reproducibility and possible companion synthesis; they are not used to validate the current identification framework.

The Sasidharan et al. 2023 FVOC reconstruction is likewise retained with its original dependence and causal-interpretation boundaries, but is not a Main identification-design result.

## 7. Mechanism → Pattern recurrence layer retained in the Main argument

The previous synthesis is now reused in a deliberately bounded role: it establishes cross-system recurrence of the constituent ecological pathways before the stricter identification-coverage audit. It does not validate the algebra or identify the channel interactions. Full provenance remains available:

```text
56 source-adjudicated route records
25 independent biological clusters
A -> pollination: 5 clusters
A -> antagonism:  8
D -> antagonism: 18
D -> pollination: 10
same-system: 14
context/sign switch: 17
context-only programs: 7 outside route N
```

These overlapping counts are not added as independent-study prevalence. Their Main-text role is limited to constituent-channel recurrence; the empirical endpoint remains whether recurrent pathways are jointly identified on common attraction-by-defence coordinates.

## 8. Open Research package

The canonical package retains historical machine-readable provenance products and additionally exports:

- `high_information_identification_coverage.csv`
- `impatiens_identification_retrofit.json`

Review-stage access is supplied by the public GitHub repository. A permanent archive DOI is **not an initial-submission blocker**. At acceptance, freeze the accepted exact data/code version in a permanent versioned archive and insert the archival citation/DOI required for publication.

## 9. Current rendered state

The fully tested identification candidate rendered as:

```text
Main Document: 27 pages
Appendix S1:   11 pages
Main figures:   5 embedded identification-design figures
```

Full-page visual QA found no blank figure-leading page, clipping, overlap, or broken glyphs. `Theorem 1` and `77.2%` are absent from Main; 2,592 and 77.2% remain in Supplement technical material.

The canonical-switch workflow must reproduce this content under the standard Ecology filenames before merge.

## 10. External-submission boundary

Science and machine-controlled identification-package engineering are complete for the current claim set. External submission remains blocked by author-controlled metadata and sign-off only:

- final author order/publication names;
- affiliations, corresponding author/email, ORCIDs;
- final CRediT roles, funding, acknowledgments, and competing-interest statement;
- repository/software/data licence statement where applicable;
- all-author approval and no-simultaneous-consideration confirmation;
- reviewer/opposed-reviewer fields only if requested by the live ScholarOne portal.

After those fields are supplied, rebuild the exact package, rerun validation and figure export, inspect every Main and Appendix page, and confirm portal fields match the frozen files before submission.
