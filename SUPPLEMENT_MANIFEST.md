# Supplement manifest — canonical identification-design paper

This manifest maps the current Main submission target:

> **From floral trait interactions to mechanism identification: a crossed-intervention framework for attraction and defence**

The historical theorem-led manuscript and analyses remain versioned for provenance, but the canonical Main Document is the identification-design manuscript with a bounded Mechanism → Pattern recurrence layer.

## 1. Canonical reader-facing sources

- Main scientific source: `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- focused references: `manuscript/IDENTIFICATION_DESIGN_REFERENCES.md`
- figure captions: `manuscript/IDENTIFICATION_DESIGN_FIGURE_CAPTIONS.md`
- Supplement: `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md`
- review-package wrapper: `scripts/build_ecology_review_package_sources.py`
- standard output directory: `submission/ecology/generated/`

Primary implementation/products:

- `trait_architecture/identification.py`
- `empirical/identification_design/HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv`
- `empirical/identification_design/IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json`
- `empirical/mechanism_pattern_synthesis/`

## 2. Canonical scientific core

Primary experimental estimand:

```text
Delta_AD W = W11 - W10 - W01 + W00
```

Identification sequence:

```text
trait interaction detection
→ non-identifiability of channel allocation
→ crossed A × D × antagonist × pollinator interventions
→ pollinator-absent baseline correction
→ A×D×G×P separability diagnostic
→ independent A×D joint-cost assay
→ hidden/unallocated-channel sign diagnostic
```

Required boundaries:

- total `Delta_AD W` does not identify rho, iota, or kappa;
- the 16-cell design is insufficient unless consumer interventions are selective and A/D coordinates remain comparable;
- rho- and iota-invariance views are one four-way contrast up to sign;
- a non-zero four-way contrast rejects the simple separable-channel representation;
- total iota requires handling the pollinator-absent `m0_delta` term;
- `U_delta = rho_delta - iota_delta - Delta_AD W` is unallocated, not kappa by definition;
- kappa requires an independent allocation/construction-cost assay;
- the elementary inequality is only a post-measurement consistency/sign diagnostic.

## 3. Mechanism → Pattern recurrence layer

The source-adjudicated synthesis is used in one bounded Main-text role: establishing cross-system recurrence of the constituent ecological pathways before the stricter identification audit.

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

These overlapping counts are not independent-study prevalence. They do not estimate `Delta_AD W`, `rho_delta`, `iota_delta`, or `kappa_delta` and do not validate the algebra.

The Main Pattern conclusion is therefore only:

> **The constituent channels recur across systems.**

## 4. Existing-data identification stress tests

### Kessler et al. 2008 — trait-factorial anchor

Published aggregate female-outcrossing constraints imply approximately:

```text
probability-scale Delta_AD: +0.19 to +0.25
logit interaction:          +1.019 to +1.551
interaction OR:             2.77 to 4.71
```

The sign is robust within the published aggregate constraints, but formal interaction uncertainty is unrecovered and nicotine silencing is systemic. This is a trait-factorial anchor, not full mechanism allocation.

### Egan et al. 2021 — consumer-factorial anchor

Herbivory and pollination environment are crossed, but the focal floral A/D traits are not independently manipulated as the required factorial. This supplies the complementary design half.

### Soper Gorden & Adler 2018 — public-data retrofit

The *Impatiens* reanalysis estimates observational A×D plus randomized robbing/florivory/pollination modification. All eight targeted HC3 intervals cross zero. It reaches total-interaction/context-modification estimation, not rho/iota/kappa identification.

### Other near misses

- Kessler et al. 2015: genuine floral 2×2 phenotype, but nectar reward is not independently justified D.
- Sun & Huang 2015, *Pedicularis rex*: useful selective-access/physical-defence anchor, but no independent A manipulation.

Across the current 16-system high-information screened set:

```text
independent joint-cost assay:       0
full rho/iota/kappa identification: 0
```

These are screened-set coverage statements, not literature prevalence.

The integrated empirical conclusion is:

> **The constituent channels recur, but their joint allocation remains unidentified.**

## 5. Canonical Main figures

1. `FIGURE_1_IDENTIFICATION_DESIGN.svg` — total trait interaction versus mechanism allocation.
2. `FIGURE_2_IDENTIFICATION_DESIGN.svg` — 16-cell crossed design and separability diagnostic.
3. `FIGURE_3_IDENTIFICATION_DESIGN.svg` — independent joint-cost assay and hidden-channel diagnostic.
4. `FIGURE_4_IDENTIFICATION_DESIGN.svg` — 56/25 recurrence layer plus Kessler 2008 / Egan 2021 / *Impatiens* / 16-system identification gap.
5. `FIGURE_5_IDENTIFICATION_DESIGN.svg` — executable experiment roadmap.

Historical mechanism/regime/Pattern/quantitative/same-system figures remain versioned but are not the canonical Main figure set.

## 6. Canonical Supplement boundary

`manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md` retains:

- 2,592 finite evaluations as implementation/model-family sensitivity only;
- 77.2% finite-design window precision, explicitly grid-dependent and not ecological prevalence;
- continuous-limit / finite-difference implementation checks;
- response-shape sensitivity maps;
- Kessler 2008 reconstruction;
- *Impatiens* retrofit details;
- 16-system identification audit details;
- full source-level Mechanism → Pattern route records and their recurrence-only interpretation.

Leal and Sasidharan quantitative modules remain reproducible historical analyses and are not Main identification results.

## 7. Historical quantitative provenance retained

Leal et al. 2025 provenance remains pinned:

```text
canonical commit: ed33b25593c0d90ad6657753f6f5501d9efc7b82
preregistration:  0e36eac
first results:    965d657
source synthesis: Leal et al. 2025, Ecology, doi:10.1002/ecy.70036
```

Historical reproduced values remain approximately:

```text
female reproductive success  LRR -0.210  48 independent clusters
nectar standing crop          LRR -0.483  28
legitimate visitation         LRR -0.291  22
```

They are preserved for reproducibility/possible companion synthesis and do not validate the identification framework. The Sasidharan et al. 2023 FVOC reconstruction is likewise retained with its dependence and causal-interpretation boundaries.

## 8. Open Research package

The canonical package retains historical machine-readable provenance products and exposes:

- `mechanism_pattern_route_ledger.csv`
- `high_information_identification_coverage.csv`
- `impatiens_identification_retrofit.json`

Review-stage access is supplied by the public GitHub repository. A permanent archive DOI is an acceptance-stage requirement, not an initial-submission blocker.

## 9. Current rendered state

Fully tested pre-metadata package:

```text
Main Document: 29 pages
Appendix S1:   11 pages
Main figures:   5
```

Full-page visual QA of all 40 pages found no blank pages, clipping, overlap, broken glyphs, or missing figure content. Figure 4 remains readable after adding the recurrence counts. `Theorem 1` and 77.2% are absent from Main; 2,592 and 77.2% remain Supplement technical material.

## 10. External-submission boundary

Science and machine-controlled package engineering are complete for the current claim set. External submission remains blocked only by author-controlled metadata/sign-off:

- final authors/order/affiliations;
- corresponding author/email and ORCIDs;
- CRediT, funding, acknowledgments, competing interests;
- repository/software/data licence statement;
- reviewer/opposed-reviewer fields only if requested;
- all-author approval and no-simultaneous-consideration confirmation.

After those fields are supplied, rebuild the exact package, rerun validation and figure export, inspect every Main and Appendix page, and confirm portal fields match the frozen files.