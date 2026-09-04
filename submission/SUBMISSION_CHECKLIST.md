# Ecology Concepts & Synthesis submission checklist — canonical Chapter 2

## 1. Scientific architecture — PASS

- [x] Canonical scientific source: `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md`
- [x] Canonical title: **When does a trait trade-off resolve by differentiation rather than compromise? Linking trait architecture to mechanism identification**
- [x] SCH / Chapter 1 = BALANCE on a shared trait axis
- [x] BITA / Chapter 2 = DIFFERENTIATION across partially decoupled trait axes
- [x] pollination/defence is a worked case, not the programme definition
- [x] general nested-architecture weak dominance is explicit: `R >= 0`
- [x] architecture decision is explicit: `Delta_arch = R-K`, differentiation iff `K<R`
- [x] stronger non-negative residual coupling cannot increase `R`
- [x] quadratic `R=sL_S*` is labelled a corollary, not a universal identity
- [x] optimized-state comparison is not presented as an evolutionary-dynamics or historical-transition model

## 2. Nonquadratic robustness — PASS

- [x] registered convex power-loss design implemented
- [x] strict positive pre-cost recovery = 300/300 nonzero-conflict evaluations
- [x] recoverable loss increases with optimum separation = 60/60 declared series
- [x] coupling monotonicity = 60/60 implementation check of the structural proposition
- [x] mismatched-curvature cost-threshold checks retained
- [x] no universality claim over arbitrary nonconvex/frequency-dependent/multimodal landscapes

## 3. Empirical architecture-state layer — PASS

- [x] cichlid oral/pharyngeal jaws used as partial-differentiation/residual-integration anchor
- [x] *Dalechampia* used as historical redeployment/exaptation/addition anchor
- [x] neither system is assigned BITA parameter estimates
- [x] neither is treated as causal proof that the modeled shared-axis conflict generated the transition

## 4. Floral mechanism-identification worked case — PASS

- [x] `Delta_AD W = W11-W10-W01+W00` retained
- [x] total interaction separated from channel allocation
- [x] identified set `I(delta)` retained
- [x] partial identification is explicit and assumption-indexed
- [x] selective `A x D x antagonist x pollinator` design retained
- [x] `m0` baseline and four-way separability diagnostic retained
- [x] remaining joint channel requires independent evidence
- [x] recurrence synthesis = 56 route records / 25 independent biological clusters
- [x] high-information frontier = 17 systems using authoritative V2 coverage matrix
- [x] route counts are not prevalence estimates
- [x] positive `A x D` interaction is not trait differentiation or historical splitting

## 5. Main Document — GENERATED / STRUCTURAL PASS

- [x] output: `MANUSCRIPT_ECOLOGY_SUBMISSION.docx`
- [x] Journal = Ecology; manuscript type = Concepts & Synthesis
- [x] abstract <= 350 words and keywords present
- [x] author/affiliation/corresponding-author fields remain author-controlled placeholders
- [x] review-stage Open Research statement present
- [x] five Chapter 2 Main figures embedded
- [x] Figures 1–3 carry balance/differentiation theory and reality checks
- [x] Figures 4–5 carry mechanism identification and fragmented empirical frontier
- [x] validated pre-metadata render = **30 pages**
- [x] Main is within the standard 30-page target
- [x] redundant blank figure pages removed
- [x] LibreOffice broken superscript `*` glyph fixed by explicit `opt` superscripts
- [x] visual inspection of representative equation, body and figure pages PASS
- [ ] re-render/re-count after final author metadata insertion

## 6. Supporting Information — GENERATED / STRUCTURAL PASS

- [x] one integrated Appendix S1
- [x] architecture derivation included
- [x] nonquadratic robustness included
- [x] cichlid/*Dalechampia* evidence ceiling included
- [x] retained floral identification supplement included
- [x] Kessler reconstruction / *Impatiens* retrofit / 17-system frontier retained
- [x] 56/25 recurrence provenance retained
- [x] 2,592 / 77.2% historical exercise remains technical Appendix material only
- [x] validated pre-metadata Appendix render = **38 pages**
- [x] no obvious blank/clipped pages in pre-metadata visual audit

## 7. Reproducibility / Open Research — PASS FOR REVIEW

- [x] `trait_architecture/differentiation.py`
- [x] `trait_architecture/differentiation_robustness.py`
- [x] `trait_architecture/identification.py`
- [x] `trait_architecture/partial_identification.py`
- [x] theory/robustness/manuscript/figure/formatter regression tests
- [x] authoritative V2 high-information coverage export
- [x] aggregate *Impatiens* retrofit export
- [x] registered robustness readout export
- [x] public GitHub provides review-stage access
- [ ] archive the accepted exact data/code version and insert DOI at acceptance stage

## 8. Cover letter / portal synchronization

- [x] target journal = Ecology
- [x] article type = Concepts & Synthesis
- [x] cover letter uses balance -> differentiation -> identification framing
- [x] title synchronized to canonical Chapter 2
- [x] 30-page Main + 38-page Appendix stated correctly
- [x] prior specialization theory acknowledged; novelty is the bridge, not specialization itself
- [ ] corresponding author signs final letter
- [ ] all authors approve the exact submitted version and no-simultaneous-consideration statement

## 9. Human-controlled fields — EXTERNAL-SUBMISSION BLOCKER

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
- [ ] all-author approval of the exact submitted version
- [ ] confirmation that the manuscript is not under consideration elsewhere

## 10. Final review-file gate — PENDING HUMAN METADATA

After author-controlled fields are supplied:

- [ ] rebuild exact canonical package
- [ ] confirm Main remains at or below 30 pages, or document any justified change
- [ ] rerun CI, submission-scope and canonical package workflows
- [ ] visually inspect every Main and Appendix page
- [ ] confirm portal title/abstract/authors/declarations/files match generated package
- [ ] obtain all-author approval of that exact version

## Current decision

**Science: GO for the Chapter 2 claim set. Canonical pre-metadata package: Main 30 pages + Appendix S1 38 pages, five Main figures. The paper now asks when a shared-trait compromise is worth replacing with partial trait differentiation and then shows why the mechanism of a multi-trait phenotype still requires explicit identification. External submission remains blocked only by author-controlled metadata/declarations/sign-off and final post-metadata QA.**
