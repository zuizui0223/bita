# Ecology Concepts & Synthesis submission checklist — BITA mechanism-identification paper

## 1. Scientific architecture — PASS

- [x] canonical scientific source = `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md`
- [x] canonical active title = **Trait interaction is not ecological mechanism: an identification framework for multifunctional traits**
- [x] active thesis = `trait interaction != ecological mechanism`
- [x] outcome hierarchy separates Level 1 interaction relief, Level 2 constraint release, and Level 3 strict reversal
- [x] total interaction is separated from channel allocation
- [x] identified-set logic is explicit
- [x] partial identification is explicit and assumption-indexed
- [x] selective `A x D x antagonist x pollinator` design retained
- [x] pollinator-absent baseline handling retained
- [x] four-way separability diagnostic retained
- [x] remaining joint channel requires independent evidence
- [x] SLK owns `L -> R -> Phi -> accessibility -> invasion -> fixation -> occupancy`
- [x] older BITA architecture derivations demoted to provenance / technical support

## 2. Empirical synthesis — PASS

- [x] recurrence synthesis = 56 route records / 25 independent biological clusters
- [x] high-information frontier = 17 systems
- [x] route counts are not prevalence estimates
- [x] strongest Kessler aggregate anchor remains bounded to Level 1 + asymmetric partial identification
- [x] no screened system is claimed to close full mechanism allocation
- [x] empirical conclusion = recurrent constituent biology + fragmented identification

## 3. Main manuscript — PASS

- [x] canonical Markdown Main rewritten around the mechanism-identification thesis
- [x] architecture-value derivation removed from Main novelty spine
- [x] programme ownership section added
- [x] claim ceiling updated
- [x] cover letter synchronized to the active thesis and validated package
- [x] five-figure caption sequence frozen
- [x] figure rebuild plan registered

## 4. Rendered Main figures — PASS

- [x] Figure 1 = outcome hierarchy
- [x] Figure 2 = identified-set geometry
- [x] Figure 3 = crossed intervention + separability
- [x] Figure 4 = fragmented empirical frontier
- [x] Figure 5 = SCH -> SLK transport plus orthogonal BITA mechanism-identification track and BITA promotion ladder
- [x] manuscript callouts synchronized with rebuilt files
- [x] visual QA completed for all rendered Main pages
- [x] Figure 5 no longer implies `SLK -> BITA`
- [x] final BITA mechanism ladder fits within the SVG/PDF canvas

## 5. Supporting Information — PASS

- [x] old architecture derivation retained as provenance/background rather than active Main support
- [x] detailed identification supplement retained
- [x] Kessler reconstruction and public-data retrofit retained
- [x] 56/25 recurrence provenance retained
- [x] 17-system coverage matrix retained
- [x] Appendix regenerated around the refocused Main
- [x] Appendix visual QA completed

## 6. Reproducibility / Open Research — PASS FOR REVIEW PACKAGE

Existing code and evidence products remain retained. No scientific result was deleted by the publication split.

- [x] identification code retained
- [x] partial-identification code retained
- [x] source-adjudicated route ledger retained
- [x] high-information coverage products retained
- [x] historical architecture derivations retained as provenance
- [x] active package workflow rebuilds source-backed evidence and candidate sources
- [x] active reader-facing package is PR-gated by `Build BITA mechanism review package`
- [x] narrative / formatter / identification guards rerun on the active package
- [x] five embedded Main figures validated in DOCX
- [x] Main PDF active-title and empirical-count guards pass
- [x] Open Research statement appears on the journal-facing title page
- [x] review artifact retains Open Research QA products without treating them as ordinary journal Supporting Information data files
- [ ] archive accepted exact version and insert DOI at acceptance stage

## 7. Active reader-facing package — PASS

The authoritative reader-facing artifact is:

```text
ACTIVE_ARTIFACT = bita-mechanism-identification-review-package
ACTIVE_RECEIPT = PACKAGE_QA_RECEIPT.txt
```

`PACKAGE_QA_RECEIPT.txt` is the source of truth for current Main/Appendix page counts, source commit, embedded media count and active-package role. The latest independently checked render recorded:

```text
MAIN_PDF = 21 pages
APPENDIX_PDF = 10 pages
MAIN_FIGURES = 5 embedded
LENGTH_STATE = WITHIN_30_PAGE_TARGET
ECOLOGY_APR2026_TITLE_PAGE = PASS
VISUAL_QA = PASS
```

The historical/older candidate workflow is retained only for provenance and regression:

```text
LEGACY_ARTIFACT = legacy-identification-candidate-package
LEGACY_ARTIFACT_ACTIVE_SUBMISSION = false
```

Its page counts must not be substituted for the active package counts. The final active render has one centered page number per page; manuscript line numbering remains active where intended.

## 8. Ecology April 2026 automated compliance — PASS

The active builder/workflow now fails closed on the current journal-facing contract:

- [x] Concepts & Synthesis Main is within the standard 30-page target: 21 pages
- [x] title = 101 characters, within the 120-character limit
- [x] Abstract = 282 words under the repository counting rule, within the 350-word limit
- [x] 8 keywords, within the 6–12 range and alphabetized in journal-facing output
- [x] title page includes journal/type, title, author/affiliation placeholder, corresponding-author placeholder, Open Research statement, and keywords
- [x] Main format = Word DOCX
- [x] page geometry = US Letter portrait with 1-inch margins
- [x] font/spacing = 12-pt Times New Roman, double-spaced prose/references/captions
- [x] continuous line numbering and centered page numbering validated
- [x] Appendix is separately rendered and available as PDF
- [x] active receipt records `ecology_apr2026_title_page=PASS`
- [ ] re-check the live author instructions / upload portal immediately before actual upload

## 9. Cover letter / portal synchronization

- [x] target class = Ecology Concepts & Synthesis / comparable conceptual-methodological ecology
- [x] cover letter rewritten around `trait interaction != ecological mechanism`
- [x] obsolete 30+38 internal package history removed from the editor-facing cover letter
- [x] cover letter states current 21-page Main is within the standard 30-page target; no over-length justification requested
- [x] final journal-facing Main/Appendix/figures regenerated as a coherent review package
- [ ] corresponding author signs final letter
- [ ] all authors approve exact submitted version and no-simultaneous-consideration statement

## 10. Human-controlled fields — EXTERNAL BLOCKER

- [ ] final author order and publication names
- [ ] affiliations / present addresses
- [ ] corresponding author and active email
- [ ] ORCIDs
- [ ] final CRediT roles
- [ ] funding/grant statement
- [ ] acknowledgments
- [ ] competing-interest statement
- [ ] repository/software/data licence statement where applicable
- [ ] reviewer information if requested by the portal
- [ ] final author-approved AI-use disclosure wording and placement, if required by the live ESA policy; synchronize relevant manuscript section, Acknowledgments, and submission form
- [ ] all-author approval

These are now the remaining blockers after scientific-package and automated journal-compliance closure. They must not be guessed or auto-filled from repository context.

## 11. Final upload gate

Before submission:

- [x] rebuild canonical Main DOCX/PDF from the refocused science source
- [x] rebuild Appendix
- [x] rerun CI / focused scientific, narrative and Ecology-compliance guards
- [x] visually inspect every Main and Appendix page
- [x] validate April 2026 Ecology author-guideline contract in the automated review package
- [ ] re-confirm live portal/file-format requirements at the moment of upload
- [ ] confirm portal metadata and uploaded files match the active `PACKAGE_QA_RECEIPT.txt`
- [ ] confirm required AI disclosure is present in all required locations or explicitly determine that no additional disclosure is required
- [ ] obtain all-author approval of that exact version

## Current decision

```text
SCIENCE_THESIS = FROZEN
CANONICAL_MARKDOWN_MAIN = REFOCUSED
ACTIVE_ARTIFACT = bita-mechanism-identification-review-package
ACTIVE_RECEIPT = PACKAGE_QA_RECEIPT.txt
ACTIVE_MAIN = PASS_21_PAGES_AT_LAST_CHECK
ACTIVE_APPENDIX = PASS_10_PAGES_AT_LAST_CHECK
ACTIVE_FIGURES = PASS_5
ECOLOGY_APR2026_AUTOMATED_COMPLIANCE = PASS
LEGACY_ARTIFACT = legacy-identification-candidate-package
VISUAL_QA = PASS
SCIENTIFIC_PACKAGE = READY_FOR_AUTHOR_METADATA_AND_FINAL_UPLOAD_CHECK
AI_DISCLOSURE = BLOCKED_AUTHOR_APPROVAL_IF_REQUIRED
EXTERNAL_SUBMISSION = NOT_YET_COMPLETED
```

The bottleneck is no longer scientific packaging or routine journal formatting. It is the author-controlled layer: live portal confirmation, final metadata/declarations/disclosure, author approvals, and upload.
