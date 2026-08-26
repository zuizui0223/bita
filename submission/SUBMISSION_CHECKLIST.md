# Ecology Concepts & Synthesis submission checklist — identification-design canonical candidate

This checklist tracks the current submission gates after the identification-design rewrite. Historical theorem-led sources remain in Git history and repository archival paths but no longer define the intended submission narrative.

## 1. Scientific core — PASS

- [x] Canonical submission manuscript: `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- [x] Canonical title: **From floral trait interactions to mechanism identification: a crossed-intervention framework for attraction and defence**
- [x] Primary estimand is the measurable discrete interaction `Delta_AD = W11 - W10 - W01 + W00`
- [x] Total trait interaction is explicitly separated from mechanism allocation
- [x] Identification design crosses `A × D × antagonist × pollinator` in 16 cells
- [x] Selective antagonist and pollinator intervention assumptions are explicit
- [x] Pollinator-absent `A×D` baseline (`m0_delta`) is measured/corrected rather than assumed zero
- [x] The rho- and iota-invariance diagnostics are recognized as one `A×D×G×P` four-way contrast up to sign
- [x] A non-zero four-way contrast is treated as evidence against the simple separable-channel representation
- [x] The residual joint channel is retained as unallocated `U_delta`; it is not defined as `kappa`
- [x] `kappa` requires an independent `A×D` allocation/construction-cost assay
- [x] The simple sign identity is diagnostic after measurement, not the headline theorem or novelty claim
- [x] Continuous mixed-partial theory is retained only as a small-contrast/theoretical limit

## 2. Existing-data stress tests — PASS

- [x] *Impatiens capensis* Dryad retrofit reaches observational `A×D` plus randomized interaction-treatment modification, but not rho/iota/kappa identification
- [x] All eight targeted Impatiens HC3 intervals cross zero
- [x] Kessler et al. 2008 is the closest current trait-factorial anchor
- [x] Published aggregate Kessler 2008 female-outcrossing constraints imply a positive discrete interaction of approximately `+0.19` to `+0.25`; logit interaction OR approximately `2.77` to `4.71`
- [x] Kessler 2008 formal interaction uncertainty remains unrecovered and systemic nicotine remains a D-scope caveat
- [x] Egan et al. 2021 is the complementary consumer-factorial anchor, not a full manipulated `A×D` design
- [x] Kessler et al. 2015 remains a factorial-phenotype near miss because the second axis is reward rather than independently justified antagonist-reducing D
- [x] *Pedicularis rex* remains a selective-system anchor rather than a complete identification design
- [x] Sixteen-system high-information coverage matrix is explicitly a screened-set audit, not literature prevalence
- [x] Independent joint-cost assay in screened set = 0
- [x] Full rho/iota/kappa identification in screened set = 0

## 3. Demoted / preserved analyses — PASS

- [x] 2,592 finite evaluations are technical implementation/model-family sensitivity only
- [x] 77.2% window precision is absent from Main and retained only in Supplement
- [x] Historical 56-route / 25-cluster mechanism ledger is preserved for provenance/background, not presented as validation of the algebra
- [x] Leal and Sasidharan quantitative modules remain reproducible in the repository but are not part of the new Main argument
- [x] Historical theorem-led manuscript remains in the repository and is not deleted

## 4. Main Document — GENERATED / STRUCTURAL PASS

The canonical review-package builder now promotes the validated identification-design source to standard Ecology output filenames.

- [x] Standard output remains `MANUSCRIPT_ECOLOGY_SUBMISSION.docx`
- [x] Journal = Ecology; manuscript type = Concepts & Synthesis
- [x] Author/affiliation, corresponding-author, and ORCID fields remain author-controlled placeholders
- [x] Review-stage Open Research statement is present
- [x] Acknowledgments, Author Contributions, Funding, and Conflict of Interest remain explicit author-controlled fields
- [x] Five identification-design Main figures are embedded
- [x] Figure 1 = total interaction versus mechanism allocation
- [x] Figure 2 = 16-cell crossed design and separability
- [x] Figure 3 = independent joint-cost assay and hidden-channel diagnostic
- [x] Figure 4 = Kessler 2008 / Egan 2021 / Impatiens / coverage comparison
- [x] Figure 5 = executable experimental roadmap
- [x] Main contains no `Theorem 1` headline
- [x] Main contains no `77.2%` headline result
- [x] Full-page candidate visual QA found no clipping, overlap, broken glyphs, or blank figure-leading page
- [x] Validated pre-metadata candidate render = **27 pages**
- [x] 27 pages is within the standard 30-page Concepts & Synthesis target; no >30-page justification is required
- [ ] Re-render and re-count after final author-controlled metadata is inserted

## 5. Supporting Information — GENERATED / STRUCTURAL PASS

- [x] Reader-facing Supporting Information remains a single Appendix S1
- [x] Canonical identification Supplement source: `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md`
- [x] Technical 2,592-grid material and 77.2% design-specific precision are Supplement only
- [x] Kessler 2008 aggregate reconstruction / sign sensitivity is documented
- [x] Impatiens retrofit details and identification boundaries are documented
- [x] Sixteen-system identification coverage is documented
- [x] Continuous-limit implementation and response-shape sensitivity figures are retained as supporting figures
- [x] Validated pre-metadata Supplement render = **11 pages**
- [x] Supplement has no line numbering

## 6. Open Research package — REVIEW READY

Legacy machine-readable provenance products are retained, and the canonical package additionally exposes identification-era outputs:

- [x] `high_information_identification_coverage.csv`
- [x] `impatiens_identification_retrofit.json`
- [x] historical parameter/grid/route/context/direct-audit products retained for reproducibility
- [x] public GitHub supplies review-stage code and derived-output access
- [ ] at acceptance, archive the accepted exact data/code version in a permanent versioned repository and insert its citation/DOI

A permanent archive DOI is **not** an initial-submission blocker.

## 7. Cover letter — CONTENT PASS / AUTHOR SIGN-OFF PENDING

- [x] Names Ecology and Concepts & Synthesis
- [x] Uses the identification-design title and contribution
- [x] Does not sell the elementary inequality as mathematical novelty
- [x] States current 27-page Main and 11-page Supplement
- [x] Removes the obsolete >30-page length justification
- [x] Uses review-stage GitHub / acceptance-stage permanent-archive wording
- [ ] corresponding author signs final letter
- [ ] all authors confirm submission and no simultaneous consideration elsewhere

## 8. Human-controlled fields — ONLY EXTERNAL-SUBMISSION BLOCKER

Do not infer or auto-fill:

- [ ] final author order and publication names
- [ ] affiliations / present addresses
- [ ] corresponding author and active email
- [ ] ORCIDs
- [ ] final CRediT roles
- [ ] funding/grant statement or explicit no-funding confirmation
- [ ] final acknowledgments
- [ ] final competing-interest statement
- [ ] repository/software/data licence statement where applicable
- [ ] reviewer information only as requested by the live ScholarOne portal
- [ ] any justified opposed-reviewer request
- [ ] all-author approval of the exact submitted version
- [ ] confirmation that the manuscript is not under consideration elsewhere

## 9. Final review-file gate — PENDING HUMAN METADATA

After the author-controlled fields are supplied:

- [ ] rebuild the exact canonical review package
- [ ] confirm Main Document remains within the applicable page limit
- [ ] rerun CI, submission-scope, canonical package build, figure export, and identification regression tests
- [ ] visually inspect every page of Main and Appendix S1
- [ ] confirm portal title/abstract/authors/declarations/files match the generated package
- [ ] obtain all-author approval of that exact version

## Current decision

**Science: GO on the identification-design claim set. Canonical pre-metadata target: Main 27 pages + Appendix S1 11 pages, five identification-design Main figures, with the old finite-grid headline demoted to Supplement. External submission remains blocked only by author-controlled metadata/declarations/sign-off and final post-metadata QA.**
