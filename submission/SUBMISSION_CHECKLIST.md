# Theoretical Ecology submission checklist

## Manuscript files

- [x] Cited Introduction draft exists: `manuscript/INTRODUCTION_DRAFT.md`
- [ ] Final title page with all authors, affiliations, emails, ORCIDs, and corresponding author
- [ ] Abstract (target 200–250 words)
- [ ] Keywords
- [ ] Consolidated main manuscript with Introduction, Model and methods, Results, Discussion, Conclusions, references
- [ ] Main figures embedded or supplied separately
- [ ] Figure captions
- [ ] Supplementary methods/readout document
- [ ] Data/code availability statement
- [ ] Author contributions statement
- [ ] Competing interests statement
- [ ] Funding statement
- [ ] Acknowledgements

## Theory work required before submission

- [ ] State a formal proposition for mechanism non-identifiability from total `W`
- [ ] Give at least two explicit decompositions producing the same total `W_AD`
- [ ] State the orientation gate as assumptions, not conclusions
- [ ] Present the unrestricted environmental derivative identities before restricted corollaries
- [ ] Include examples with no sign crossing, one crossing, and multiple crossings
- [ ] Explain dependence on declared trait coordinates and outcome scale
- [ ] Keep evolutionary interpretation local; do not infer covariance, optimum, ESS, or trajectory

## Numerical analysis

- [x] Canonical run identity fixed as `endpoint_normalized_grid_v2`
- [x] 2,592 evaluations reproduced
- [x] Analytic derivatives checked against independent finite differences
- [x] Numerical neutrality convention documented
- [x] Endpoint normalization documented
- [ ] Select only manuscript-relevant sensitivity summaries
- [ ] Replace any prevalence language with finite-design sensitivity language
- [ ] Produce publication-ready vector figures and verify fonts/labels

## Literature and references

- [ ] Verify every citation against full text where it supports a central claim
- [ ] Complete DOI and bibliographic metadata
- [ ] Remove or qualify abstract-only claims
- [ ] Keep preliminary route registry out of the main Results
- [ ] Describe literature layer as biological context only

## Reproducibility and archive

- [ ] Run full test suite on final main branch
- [ ] Regenerate all committed outputs from final code
- [ ] Confirm submission-scope and theory–literature boundary tests pass
- [ ] Create a release corresponding exactly to the submitted manuscript
- [ ] Archive the release in Zenodo or another DOI-granting repository
- [ ] Replace repository placeholders in cover letter and manuscript with archived DOI

## Submission portal information still required from authors

- [ ] Full author order
- [ ] Affiliations
- [ ] Corresponding author
- [ ] ORCIDs
- [ ] Funding sources and grant numbers
- [ ] Conflicts of interest
- [ ] Suggested reviewers and exclusions
- [ ] Confirmation that all authors approve submission
- [ ] Choice of subscription publication or open access

## Submission decision

Do not press submit until every item above is complete. The current repository is scientifically coherent but does not yet contain a complete journal-ready manuscript package.
