# Ecology Concepts & Synthesis submission checklist — current review-package state

This checklist tracks only the **current submission gates**. Historical workflow/source chronology remains in the audit files and Git history.

## 1. Scientific freeze — PASS

- [x] Canonical scientific manuscript: `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md`
- [x] Canonical title: **When are floral attraction and defence complementary? A one-sided mechanistic bound and cross-system patterns**
- [x] Part I → Part II logic remains **Mechanism → Pattern**, not theory → validation
- [x] `W_AD = rho - iota - kappa` remains bookkeeping rather than the novelty
- [x] One-sided theorem remains `kappa >= 0` and `W_AD > 0 => rho > iota`
- [x] Selectivity window remains necessary, not sufficient
- [x] Frozen values unchanged: 2,592 evaluations; 77.2% window precision; 56 records / 25 clusters; route counts 5 / 8 / 18 / 10; same-system 14; sign/context switch 17; context-only 7 outside route N
- [x] Leal and Sasidharan results and limitations remain unchanged
- [x] Direct total `A × D` evidence remains sparse/sign-unresolved at the strict total-outcome level
- [x] Direct joint-cost curvature remains **unidentified, not zero**
- [x] 2 × 2 allocation falsification gate remains distinct from full `A × D` calibration
- [x] Broad Pattern evidence search remains closed

## 2. Reproducibility — PASS

- [x] Normal CI passes on Python 3.10 / 3.11 / 3.12 on the Ecology packaging branch
- [x] `submission-scope` passes
- [x] Main Figures 1–3 retain canonical SVG scientific sources and deterministic export machinery
- [x] Appendix Figures S1–S4 retain reproducible builders and committed canonical sources
- [x] Canonical supplementary Tables S1–S6 remain reproducible machine-readable products
- [x] Figure 2 and Appendix figures/tables retain regeneration/diff contracts
- [x] Leal modern-estimator sensitivity remains separate from canonical pooled estimates
- [x] Sasidharan 32-component dependence topology remains fixed

## 3. Ecology Main Document — GENERATED / STRUCTURAL PASS

The review-package builder produces `MANUSCRIPT_ECOLOGY_SUBMISSION.docx` from the frozen scientific source without changing scientific claims.

- [x] Title page contains journal name `Ecology`
- [x] Title page contains manuscript type `Concepts & Synthesis`
- [x] Title page contains title, author/affiliation placeholders, corresponding-author placeholder, Open Research statement, and six alphabetized key words/phrases
- [x] Abstract begins after the title page
- [x] Backmatter is ordered for Ecology: Acknowledgments → Author Contributions → Conflict of Interest Statement → References
- [x] Tables 1–4 are in the Main Document and each begins on a new page
- [x] Main Tables 1–4 are compact journal-facing views; exhaustive parameter/ledger/audit rows are not duplicated in the Main Document
- [x] Figure captions are grouped after the tables
- [x] Figures 1–3 are embedded and each begins on a separate page
- [x] Letter size, 1-inch margins, 12-pt Times New Roman, double-spaced prose
- [x] Table bodies use compact 10-pt/single-spaced formatting
- [x] Page numbers are present from the title-page section onward
- [x] DOCX OOXML contains continuous line numbering for the Abstract-through-References section and no line numbering for title-page or post-References sections
- [x] Equations remain native Word/Pandoc math rather than raster equation images
- [x] Rendered Main Document contains four Word tables and three embedded main figures
- [x] Current Ecology-formatted review render = **48 pages**
- [x] 48 pages is within the stated 31–50-page Concepts & Synthesis range
- [x] Required two-part >30-page justification has been added to the Ecology cover letter
- [ ] Re-render and re-count after final author-controlled title-page/backmatter fields are inserted; final file must remain ≤50 pages

## 4. Ecology Supporting Information — GENERATED / STRUCTURAL PASS

- [x] Reader-facing Supporting Information is a single `Appendix S1.pdf`
- [x] Appendix begins with author placeholder, manuscript title, and journal name
- [x] Main-document callouts are converted to `Appendix S1: Figure S#` form
- [x] Appendix contains reader-facing Figures S1–S4
- [x] Appendix contains its own References section for literature cited inside the Appendix
- [x] Appendix has no spreadsheet attachment layer and no line numbering
- [x] Current Appendix render = **6 pages**

## 5. Open Research data/code package — REVIEW READY

ESA spreadsheet-format and large machine-readable records are separated from Supporting Information.

Generated deposition names:

- [x] `model_parameters_and_scaling.csv`
- [x] `finite_grid_local_cases.csv`
- [x] `mechanism_pattern_route_ledger.csv`
- [x] `conditionality_context_records.csv`
- [x] `direct_identification_audits.csv`
- [x] `pattern_expansion_screening.csv`
- [x] `OPEN_RESEARCH_DATA_MANIFEST.md` maps each deposition file to its canonical repository source
- [x] Public GitHub provides review-stage access to novel code and versioned analysis products
- [ ] At acceptance, freeze the accepted exact data/code version in a permanent versioned archive and insert the archival citation/DOI required by ESA Open Research policy

A permanent archive DOI is therefore **not an initial-submission blocker** for this Concepts & Synthesis review package; it remains an acceptance-stage publication requirement.

## 6. Cover letter — CONTENT PASS / AUTHOR SIGN-OFF PENDING

- [x] Names Ecology and Concepts & Synthesis
- [x] States the one-sided mechanistic bound without overclaiming mathematical novelty
- [x] Explains Mechanism → Pattern / constraint-before-pattern contribution
- [x] Includes two numbered length-justification sections because the review render is 48 pages
- [x] Explains that exhaustive tables/ledgers are already displaced to Open Research products
- [x] Uses review-stage GitHub / acceptance-stage permanent-archive wording
- [ ] Corresponding author signs the final letter
- [ ] All authors confirm the submission/no-simultaneous-consideration statements

## 7. Human-controlled fields — BLOCK EXTERNAL SUBMISSION

Do not infer or auto-fill:

- [ ] final author order and publication names
- [ ] affiliations / present addresses if applicable
- [ ] corresponding author and active email
- [ ] ORCIDs
- [ ] final CRediT roles
- [ ] funding/grant statement or explicit no-funding confirmation
- [ ] final acknowledgments
- [ ] final competing-interest statement
- [ ] repository/software/data licence statement where applicable
- [ ] reviewer information **only to the number/fields requested by the live ScholarOne portal**
- [ ] any justified opposed-reviewer request
- [ ] all-author approval of the exact submitted version
- [ ] confirmation that the manuscript is not under consideration elsewhere

The current published Author Guidelines do **not** justify treating “exactly five suggested reviewers” as a fixed manuscript-level blocker; follow the live portal if it requests reviewer entries.

## 8. Final review-file gate — PENDING HUMAN METADATA

After the human-controlled fields are supplied:

- [ ] build the exact review submission package again
- [ ] confirm Main Document remains ≤50 pages
- [ ] run normal CI, submission-scope, and Ecology package workflow
- [ ] visually inspect every page of the final rendered Main Document and Appendix S1
- [ ] confirm portal title/abstract/authors/declarations/files match the frozen review package
- [ ] submit through the authenticated Ecology ScholarOne portal

## Current decision

**Science: GO / FROZEN. Main and Appendix source/package engineering: PASS. Current rendered review package: Main 48 pages + Appendix S1 6 pages, within the journal's stated page ceiling with the required >30-page cover-letter justification. External submission is now blocked primarily by author-controlled metadata/declarations/sign-off and final post-metadata visual QA, not by missing science or a pre-submission archive DOI.**
