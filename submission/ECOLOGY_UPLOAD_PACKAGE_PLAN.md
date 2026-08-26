# Ecology Concepts & Synthesis upload package plan — identification design

Target: **Ecology — Concepts & Synthesis**

The canonical review package now uses the identification-design manuscript rather than the historical theorem-led submission source.

## 1. Main Document

Canonical scientific source:

- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- focused bibliography: `manuscript/IDENTIFICATION_DESIGN_REFERENCES.md`
- figures: `manuscript/identification_figures/FIGURE_1_IDENTIFICATION_DESIGN.svg` through `FIGURE_5_IDENTIFICATION_DESIGN.svg`

Standard generated filename remains:

- `submission/ecology/generated/MANUSCRIPT_ECOLOGY_SUBMISSION.docx`

Formatting target:

- Word `.docx`;
- Letter 8.5 × 11 in, portrait;
- 1-inch margins;
- 12-pt Times New Roman;
- double-spaced prose and references;
- page numbers;
- continuous line numbering for the review-text section;
- native Word/Pandoc equations;
- five embedded Main figures.

The current validated pre-metadata identification candidate renders to **27 Main Document pages**, within the standard 30-page Concepts & Synthesis target. The former 48-page package and its >30-page cover-letter justification are historical and no longer define the intended submission.

## 2. Main scientific sequence

The five Main figures now follow the identification argument:

1. **Figure 1 — interaction detection versus mechanism allocation.** A measured `Delta_AD W` does not identify its channel decomposition.
2. **Figure 2 — crossed intervention design.** `A × D × antagonist × pollinator` creates the 16-cell identification structure and the four-way separability diagnostic.
3. **Figure 3 — independent joint-cost assay.** The unallocated residual is kept distinct from `kappa` until an independent `A×D` assay constrains interpretation.
4. **Figure 4 — existing-data stress tests.** Kessler 2008 supplies the closest trait-factorial anchor, Egan 2021 the complementary consumer-factorial anchor, and the Impatiens public-data retrofit shows how far a rich existing dataset can reach.
5. **Figure 5 — executable experimental roadmap.** The proposed sequence moves from interaction detection to channel identification and explicit failure diagnostics.

The Main argument deliberately does **not** use the 2,592 finite-grid evaluations, 77.2% window precision, 56-route ledger, Leal synthesis, or Sasidharan synthesis as headline results. Those analyses remain available for provenance, technical sensitivity, or separate synthesis work.

## 3. Supporting Information

Canonical source:

- `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md`

Standard review file remains Appendix S1. The current validated pre-metadata render is **11 pages**.

Appendix S1 retains:

- the former 2,592-evaluation exercise as implementation/model-family sensitivity rather than empirical validation;
- the 77.2% finite-design window precision with its grid-dependence made explicit;
- Kessler 2008 aggregate reconstruction and uncertainty boundary;
- Impatiens retrofit details;
- the sixteen-system high-information identification coverage audit;
- continuous-limit implementation and response-shape sensitivity figures.

## 4. Open Research package

The standard review-package builder retains historical machine-readable products for reproducibility and additionally exports:

- `high_information_identification_coverage.csv`;
- `impatiens_identification_retrofit.json`.

The public GitHub repository supplies review-stage access to code, source audits, and derived products. Permanent archival deposition of the accepted exact data/code version remains an acceptance-stage requirement rather than an initial-submission blocker.

## 5. Human-controlled fields still required

The builder intentionally does not infer:

- final author list/order/publication names;
- affiliations and present addresses;
- corresponding author and active email;
- ORCIDs;
- final CRediT roles;
- funding/grant statement or explicit no-funding confirmation;
- final acknowledgments;
- final competing-interest statement;
- repository/software/data licence statement where applicable;
- portal-only reviewer fields if requested by ScholarOne;
- any justified opposed-reviewer request;
- all-author approval of the exact submitted version;
- confirmation that the manuscript is not under consideration elsewhere.

A permanent archive DOI is **not** an initial-submission blocker.

## 6. Canonical automated build

Run:

```bash
python scripts/build_ecology_review_package_sources.py
```

The wrapper promotes the already validated identification candidate into the standard `submission/ecology/generated/` filenames while leaving the historical theorem-led manuscript in the repository for provenance.

The workflow `.github/workflows/build-ecology-submission-package.yml` must verify:

1. identification-design source contract and focused references;
2. Main and Appendix DOCX generation;
3. native equations, line-number/page formatting, and five embedded identification figures;
4. Main title and identification framing;
5. absence of `Theorem 1` and `77.2%` from Main;
6. presence of `2,592` and `77.2%` only in Appendix technical material;
7. exact Main and Appendix page counts;
8. Main page-limit compliance;
9. Open Research export of identification-era products;
10. upload of the standard review artifact.

Submission-ready EPS export likewise uses the five identification-design SVGs as Fig1–Fig5.

## 7. Current package boundary

**Current machine-validated target before author metadata: Main 27 pages + Appendix S1 11 pages.** The old 48+5 Mechanism → Pattern package remains reproducible history but is no longer the intended submission narrative.
