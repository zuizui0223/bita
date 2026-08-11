# Theoretical Ecology submission checklist — integrated theory + mechanism-pattern synthesis

## Canonical manuscript package

- [x] Canonical manuscript exists: `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md`
- [x] Integrated title reflects theory + mechanism-pattern synthesis
- [x] Abstract and keywords are present
- [x] Introduction states the ecological inference gap and conditional biological hypothesis
- [x] Model/analytical framework contains the signed decomposition, orientation gate, local sign criterion, Proposition 1, and environmental derivative identities
- [x] Finite sensitivity-analysis Methods and canonical numerical Results are integrated
- [x] Mechanism-pattern synthesis Methods are integrated
- [x] Empirical Results include mechanism recurrence, same-system architecture, conditionality, direct `A x D` scarcity, joint-cost evidence gap, and two quantitative modules
- [x] Discussion keeps constituent-path evidence separate from estimation of `W_AD`
- [x] Figure captions for Figures 1-3 are drafted
- [x] Main manuscript tables 1-4 are drafted in `manuscript/TABLES_THEORETICAL_ECOLOGY.md`
- [x] Data/code availability statement is drafted
- [x] Competing-interests statement placeholder is present
- [ ] Final title page with all authors, affiliations, emails, ORCIDs, and corresponding author
- [ ] Final CRediT author-contributions statement
- [ ] Funding statement with grant identifiers
- [ ] Acknowledgements
- [ ] Final author-approved competing-interests confirmation

## Theory and inference contract

- [x] `W_AD` is defined as a local mixed partial on declared trait/outcome coordinates
- [x] Signed identity `W_AD = M_AD - G_AD - C_AD` is separated from biological interpretation
- [x] Orientation gate is stated as an assumption/condition, not inferred from labels
- [x] Oriented criterion `W_AD = rho - iota - kappa` is explicit
- [x] `W_AD > 0` is distinguished from positive first derivatives
- [x] Proposition 1 states structural mechanism non-identifiability from total `W`
- [x] The proposition is explicitly limited: channel-specific interventions/structural restrictions can add identification
- [x] Unrestricted environmental derivative identities and directional inequalities are explicit
- [x] Evolutionary interpretation remains local; no covariance, optimum, ESS, or trajectory is inferred from the mixed partial alone
- [x] Direct joint-cost curvature is used consistently as the mathematical `kappa` target
- [x] `kappa` is carried as unidentified rather than zero

## Finite sensitivity analysis

- [x] Canonical run identity fixed as `endpoint_normalized_grid_v2`
- [x] 2,592 evaluations reproduced
- [x] Analytic derivatives checked against independent finite differences
- [x] Numerical neutrality convention documented
- [x] Endpoint normalization documented
- [x] Manuscript-relevant sensitivity summaries selected
- [x] Finite-grid occupancy language replaces prevalence/probability language
- [ ] Regenerate final Figure 2 export from the final submission commit
- [ ] Produce publication-ready vector PDF/EPS and verify final fonts/labels

## Mechanism-pattern empirical synthesis

- [x] Completion gate A-H adjudicated PASS
- [x] All four marginal mechanism families have explicit source-adjudicated states
- [x] Same-system multi-route linkage/dependence is retained
- [x] Direct `A x D` search is saturated to the registered stopping rule
- [x] Direct joint-cost search is saturated to the registered stopping rule
- [x] Eleven independent context/sign-switch clusters are mapped to five theory-facing classes
- [x] No incompatible cross-outcome grand moderator coefficient is manufactured
- [x] Leal et al. 2025 quantitative module is pinned to immutable commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`
- [x] Sasidharan et al. 2023 quantitative module uses the canonical 32-study-component dependence topology
- [x] Module-specific independence/influence/heterogeneity/source-discrepancy limitations are reported
- [x] Marginal and same-system evidence are explicitly prevented from being called `W_AD`
- [x] Study/publication counts and deposited-data fractions are prevented from being called prevalence or parameters
- [ ] Build final Figure 3 empirical mechanism-pattern architecture from committed evidence states
- [ ] Decide whether robustness panels belong in main Figure 3 or Supplementary Figure S4

## Literature and references

- [x] Central quantitative modules have explicit DOI/source identities and reproducibility boundaries
- [x] High-information mechanism studies used in the source-adjudicated ledger retain source verification state/locators in repository evidence products
- [x] Obsolete manuscript claim that the literature layer is abstract-only with zero quantitative effects has been removed
- [ ] Verify every citation used for a central manuscript claim against the primary source / source-adjudication record
- [ ] Complete final author/title/journal/year/pages/DOI metadata for every reference
- [ ] Check that every empirical study named in main text appears in References and vice versa where appropriate
- [ ] Apply journal-specific reference formatting after scientific reference audit

## Repository narrative and reproducibility

- [x] Root `README.md` describes the integrated theory+synthesis paper
- [x] `docs/SUBMISSION_SCOPE.md` reflects the integrated evidence architecture
- [x] `docs/FINAL_SUBMISSION_AUDIT.md` records A-H PASS and the theory/empiricism boundary
- [x] `SUPPLEMENT_MANIFEST.md` pins both quantitative modules and correct canonical paths
- [x] Submission narrative regression test migrated away from the obsolete preliminary-literature-only contract
- [x] Submission-scope regression test protects the integrated manuscript/evidence spine
- [ ] Full CI green on the final manuscript-integration head
- [ ] Regenerate all final committed/generated outputs from the final submission commit
- [ ] Create a release corresponding exactly to the submitted manuscript
- [ ] Archive the release in Zenodo or another DOI-granting repository
- [ ] Replace repository/archive placeholders in cover letter and manuscript with the archival DOI

## Figures and tables

- [x] Figure 1 conceptual/mechanistic source exists
- [x] Figure 2 generation script and canonical numerical source exist
- [x] Figure 3 design/specification is fixed in `submission/FIGURE_AND_TABLE_PLAN.md`
- [x] Tables 1-4 are drafted
- [ ] Produce Figure 3 reproducibly
- [ ] Produce final vector exports of all main figures
- [ ] Check figure-panel labels against final manuscript citations
- [ ] Decide final supplementary figure/table set and numbering
- [ ] Verify captions are self-contained and repeat all non-prevalence/inference boundaries needed to avoid misreading

## Submission support

- [x] Cover letter updated to the integrated theory+synthesis paper
- [x] Figure/table plan updated to Figures 1-3 and Tables 1-4
- [ ] Re-run final manuscript audit after CI and reference/figure completion
- [ ] Update target-journal strategy if journal choice changes
- [ ] Complete portal metadata template

## Submission portal information still required from authors

- [ ] Full author order
- [ ] Affiliations
- [ ] Corresponding author
- [ ] ORCIDs
- [ ] Funding sources and grant numbers
- [ ] Conflicts of interest
- [ ] Suggested reviewers and exclusions
- [ ] Confirmation that all authors approve submission
- [ ] Choice of subscription publication or open access if applicable at submission

## Submission decision

**Scientific theory+synthesis architecture: GO. Portal submission: NOT YET.**

Do not press submit until final CI, figures, reference verification, author-controlled metadata, and archival DOI/release are complete. Additional literature searching is not a default blocker unless final source verification exposes a specific coverage problem or a new direct-design candidate that materially changes a registered evidence gap.
