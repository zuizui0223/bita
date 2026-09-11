# Ecology Concepts & Synthesis upload package plan — BITA mechanism identification

Target: **Ecology — Concepts & Synthesis**

The active review package is now built from the refocused BITA paper:

> **Trait interaction is not ecological mechanism: an identification framework for multifunctional traits**

The previously validated architecture-plus-mechanism and older identification-only page counts are historical. They must not be used as current submission evidence.

## 1. Main Document

Canonical science source:

```text
manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md
```

Focused bibliography:

```text
manuscript/IDENTIFICATION_DESIGN_REFERENCES.md
```

Active figure builder and output:

```text
scripts/build_mechanism_identification_figures_svg.py
manuscript/mechanism_identification_figures/
```

Active package builder:

```text
scripts/build_bita_mechanism_candidate_sources.py
```

Generated review source directory:

```text
submission/ecology/mechanism_identification_candidate/generated/
```

Formatting remains Word `.docx`, Letter portrait, 1-inch margins, 12-pt Times New Roman, double-spaced prose/references, review line numbering, native equations, and five embedded Main figures.

## 2. Scientific sequence

```text
four-cell A×D interaction
→ outcome promotion
   Level 1 interaction relief
   Level 2 constraint release
   Level 3 strict reversal
→ identified set of compatible channel allocations
→ assumption-indexed partial identification
→ selective A×D×antagonist×pollinator intervention
→ m0 handling + four-way separability diagnostic
→ consumer-channel allocation
→ independent remaining-channel assay
→ mechanism-resolved interpretation
```

Core accounting identity:

```text
Delta_AD W = rho_delta - iota_delta - kappa_delta
```

A measured total interaction defines an identified set, not a unique mechanism. Under an explicit restriction such as `kappa_delta >= 0`, the framework yields a partial-identification bound; the restriction is not a universal theorem.

## 3. Main figures

1. **Outcome promotion.** Positive interaction relief vs functional constraint release vs strict reversal.
2. **Identified-set geometry.** Total interaction, compatible allocations, and partial-identification shrinkage.
3. **Crossed intervention.** Selective consumer toggles, baseline correction, four-way separability, and independent remaining-channel assay.
4. **Fragmented empirical frontier.** Source-backed 56-route / 25-cluster recurrence, 17-system V2 identification audit, and public-data retrofit.
5. **Inference boundaries.** SCH identifies conflict; SLK transports evolutionary value; BITA identifies mechanism.

Figure 4 is data-driven. The build fails if the authoritative 17-system V2 audit or 56/25 route-ledger state drifts.

## 4. Supporting Information

Active source:

```text
manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md
```

Appendix S1 retains the detailed identification algebra, Kessler reconstruction, *Impatiens* retrofit, 17-system frontier, recurrence provenance, and technical design diagnostics. Architecture-value derivations remain repository provenance and are not part of the active BITA Main spine.

## 5. Open Research package

The active candidate exports at minimum:

```text
high_information_identification_coverage_v2.csv
impatiens_2018_identification_retrofit_v1.json
pattern_expansion_readout_v1.json
```

These products document evidence capacity and identification status. Route counts are overlapping recurrence diagnostics, not prevalence estimates.

## 6. Automated review-package gate

Workflow:

```text
.github/workflows/build-bita-mechanism-review-package.yml
```

The workflow must:

1. run focused identification, partial-identification, figure, package, and formatter tests;
2. regenerate the 56/25 evidence receipt and all five SVG figures;
3. build candidate Main + Appendix + Open Research sources;
4. render Main and Appendix DOCX;
5. verify line numbering and at least five embedded Main media objects;
6. convert both DOCX files to PDF;
7. measure fresh Main/Appendix page counts;
8. reject stale architecture-paper tokens from the active Main;
9. rasterize every PDF page to PNG for visual QA;
10. upload the complete review artifact.

## 7. Current package boundary

Current status:

```text
ACTIVE_SCIENCE_SOURCE_REFOCUSED
FIVE_FIGURE_PIPELINE_GREEN
CANDIDATE_MARKDOWN_PACKAGE_GREEN
DOCX_PDF_REBUILD_IN_PROGRESS
OLD_29_PLUS_12_PAGE_COUNT_STALE
OLD_30_PLUS_38_PAGE_COUNT_STALE
```

No old generated package is submission-current. The first green run of the new review-package workflow defines the new measured page-count baseline.

## 8. Human-controlled fields required before external upload

Final author list/order/names; affiliations/present addresses; corresponding author/e-mail; ORCIDs; CRediT; funding or no-funding statement; acknowledgments; competing interests; licence; portal-only reviewer fields if requested; all-author approval; and no-simultaneous-consideration confirmation.