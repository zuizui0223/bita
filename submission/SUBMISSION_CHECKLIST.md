# Ecology Concepts & Synthesis submission checklist — partial-identification canonical candidate

## 1. Scientific core — PASS

- [x] Canonical manuscript: `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- [x] Canonical title: **From floral trait interactions to mechanism identification: a crossed-intervention framework for attraction and defence**
- [x] Primary estimand is `Delta_AD W = W11 - W10 - W01 + W00`
- [x] Total interaction is separated from channel allocation
- [x] Total interaction defines `I(delta) = {(rho,iota,kappa): rho-iota-kappa=delta}` rather than a unique mechanism
- [x] Partial identification is explicit and assumption-indexed
- [x] `kappa_delta >= 0 => rho_delta - iota_delta >= Delta_AD W` is retained as a biotic-balance bound, not a universal theorem
- [x] Point-identification design crosses `A × D × antagonist × pollinator` in 16 cells
- [x] Selective intervention and comparable A/D-coordinate requirements are explicit
- [x] `m0_delta` is measured/corrected rather than silently set to zero
- [x] rho/iota invariance views are one `A×D×G×P` four-way contrast up to sign
- [x] non-zero four-way coupling rejects the simple separable-channel representation
- [x] `U_delta` remains unallocated and is not defined as kappa
- [x] kappa requires an independent A×D allocation/construction assay
- [x] continuous mixed-partial theory is only a limiting/technical layer

## 2. Mechanism → Pattern and empirical stress tests — PASS

- [x] recurrence synthesis = 56 route records / 25 independent biological clusters
- [x] all four constituent pathway families recur: A→pollination 5; A→antagonism 8; D→antagonism 18; D→pollination 10
- [x] same-system multi-route = 14; context/sign-switch = 17
- [x] route counts overlap and are not natural-prevalence estimates
- [x] marginal recurrence is not relabelled as Delta_AD W, rho, iota, or kappa
- [x] 17-system audit is interpreted as a **fragmented identification frontier**, not only a binary 0/16 result
- [x] Kessler 2008 = closest trait-factorial anchor; aggregate Delta_AD sign positive, formal interaction uncertainty unresolved, systemic-D caveat retained
- [x] Egan 2021 = complementary consumer-factorial anchor, not a manipulated floral A×D design
- [x] *Impatiens capensis* = observational A×D + randomized context modification; all eight target HC3 intervals cross zero
- [x] *Pedicularis rex* = selective-defence system anchor, not full identification
- [x] independent joint-cost assay in screened set = 0
- [x] full rho/iota/kappa point identification in screened set = 0
- [x] no study-specific rho/iota/kappa numerical bounds are invented from near-miss studies

## 3. Historical analyses — correctly demoted

- [x] 2,592 finite evaluations are technical implementation/model-family sensitivity only
- [x] 77.2% is absent from Main and retained only in Appendix
- [x] Leal and Sasidharan modules remain reproducible but are not Main identification evidence
- [x] historical theorem-led manuscript remains versioned and is not canonical

## 4. Main Document — GENERATED / STRUCTURAL PASS

- [x] standard output: `MANUSCRIPT_ECOLOGY_SUBMISSION.docx`
- [x] Journal = Ecology; manuscript type = Concepts & Synthesis
- [x] author/affiliation/corresponding-author/ORCID fields remain author-controlled placeholders
- [x] review-stage Open Research statement present
- [x] Acknowledgments / Author Contributions / Funding / Conflict of Interest fields present
- [x] five identification-design Main figures embedded
- [x] Figure 1 = total interaction defines an identified set rather than a unique mechanism
- [x] Figure 2 = 16-cell crossed design + separability diagnostic
- [x] Figure 3 = independent joint-cost assay + hidden-channel diagnostic
- [x] Figure 4 = 56/25 recurrence + fragmented identification frontier / empirical anchors
- [x] Figure 5 = executable roadmap from interaction detection through partial to point identification
- [x] Main contains no `Theorem 1` headline and no `77.2%` headline result
- [x] validated pre-metadata render = **29 pages**
- [x] 29 pages is within the standard 30-page target with one-page headroom
- [x] full-page visual QA of all 29 Main pages PASS
- [ ] re-render/re-count after final author metadata insertion

## 5. Supporting Information — GENERATED / STRUCTURAL PASS

- [x] one Appendix S1
- [x] source: `manuscript/supplementary/SUPPLEMENT_IDENTIFICATION_DESIGN.md`
- [x] exact identified-set projection algebra and partial-identification examples included
- [x] structural identified-set intervals are distinguished from sampling uncertainty intervals
- [x] Kessler 2008 reconstruction and *Impatiens* retrofit documented
- [x] 17-system identification frontier documented
- [x] 56/25 recurrence source layer and non-identification boundary documented
- [x] 2,592 / 77.2% remain technical Appendix material
- [x] validated pre-metadata Appendix render = **12 pages**
- [x] full-page visual QA of all 12 Appendix pages PASS

## 6. Reproducibility / Open Research — REVIEW READY

- [x] `trait_architecture/identification.py`
- [x] `trait_architecture/partial_identification.py`
- [x] identification and partial-identification regression tests
- [x] `mechanism_pattern_route_ledger.csv`
- [x] `high_information_identification_coverage.csv`
- [x] `impatiens_identification_retrofit.json`
- [x] historical provenance products retained
- [x] public GitHub supplies review-stage access
- [ ] archive the accepted exact data/code version in a permanent repository and insert DOI/citation at acceptance

A permanent archive DOI is not an initial-submission blocker.

## 7. Cover letter — CONTENT PASS / AUTHOR SIGN-OFF PENDING

- [x] names Ecology and Concepts & Synthesis
- [x] uses the identification-design title
- [x] presents partial identification as an assumption-indexed middle layer, not a general invention
- [x] presents Mechanism → Pattern recurrence without treating it as theorem validation
- [x] describes design fragmentation / minimum-augmentation opportunity
- [x] does not sell the elementary inequality as mathematical novelty
- [x] current package = 29-page Main + 12-page Appendix
- [x] no >30-page justification required
- [ ] corresponding author signs final letter
- [ ] all authors confirm submission / no simultaneous consideration elsewhere

## 8. Human-controlled fields — ONLY EXTERNAL-SUBMISSION BLOCKER

- [ ] final author order and publication names
- [ ] affiliations / present addresses
- [ ] corresponding author and active email
- [ ] ORCIDs
- [ ] final CRediT roles
- [ ] funding/grant statement or explicit no-funding confirmation
- [ ] final acknowledgments
- [ ] final competing-interest statement
- [ ] repository/software/data licence statement where applicable
- [ ] reviewer information only if requested by the live portal
- [ ] any justified opposed-reviewer request
- [ ] all-author approval of the exact submitted version
- [ ] confirmation that the manuscript is not under consideration elsewhere

## 9. Final review-file gate — PENDING HUMAN METADATA

After author-controlled fields are supplied:

- [ ] rebuild exact canonical package
- [ ] confirm Main remains within page limit
- [ ] rerun CI, submission-scope, canonical package build, figure export, and identification regressions
- [ ] visually inspect every Main and Appendix page
- [ ] confirm portal title/abstract/authors/declarations/files match generated package
- [ ] obtain all-author approval of that exact version

## Current decision

**Science: GO on the partial-identification claim set with a bounded Mechanism → Pattern recurrence layer. Canonical pre-metadata package: Main 29 pages + Appendix S1 12 pages, five Main figures. The constituent channels recur; current studies constrain complementary parts of the allocation problem; total interaction supports assumption-indexed partial bounds; full point allocation still requires the crossed intervention design and independent joint-channel evidence. External submission remains blocked only by author-controlled metadata/declarations/sign-off and final post-metadata QA.**