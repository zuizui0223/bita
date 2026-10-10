# Model-support qualification for the access-routing Letter (author/reviewer note)

Status: **PROVISIONAL SUBMISSION-DRAFT QUALIFICATION — not a new result**
Branch: `paper/route-rate-riskset-qualification-v1`

## Why this note accompanies the revised draft

The primary Letter distinguishes robbery **prevalence among observed
interactions** from zero-inclusive **route-specific feeding rates**. The
public-data construction itself uses the same camera-waypoint × locally
available bird opportunity matrix for both response types.

However, the route-specific Poisson fixed-effect estimator iteratively
removes a waypoint or bird-group margin if it has zero **observed
counts for that route**. This differs for legitimate and robbery
responses, so the effective fitted positive-margin supports are not
the same. Thus dividing separately fitted RRs is not a single
common-opportunity replacement estimand.

## Source-fixed numbers

At the post-open 1.8× effective hummingbird reach threshold:

- 19,903 hummingbird opportunities constructed (49 bird species;
  288 plant species).
- Original Letter model uses **bird-species + camera-waypoint** FE.
- Robbery model positive-margin support: **3,371** opportunity edges.
- Legitimate model positive-margin support: **15,377** edges.
- The separate supported sets share **2,900** edges.
- Model-specific RR: legitimate **0.1537**
  (95% plant-jackknife CI 0.0872–0.2710);
  robbery **0.8164** (0.3583–1.8602).
- The reported **5.311** (1.923–14.672) is the descriptive ratio
  of those **separately supported** route-model RRs, not an
  unconditional or individually tracked substitution ratio.

A stricter post-open analysis fixing **bird × site + camera-waypoint**
FE retained 15,352 legitimate and 2,563 robbery opportunity edges;
their positive-margin intersection was 2,195. Repeated joint pruning
retained 1,986 cells (126 plant species). A paired joint-support
jackknife gives a descriptive severe/access ratio-of-RRs of
12.36 (working 95% interval 4.12–37.05). Because support is selected
by observed outcomes, that value is **not** promoted to this Letter.

These are support diagnostics, **not** a revision of frozen
dataset results or a new biological independent replicate.

## Source and reproduction links

- Frozen anonymous public-data archive GitHub Actions artifact
  `11293379572` (underlying EPHI Zenodo DOI
  `10.5281/zenodo.14185547`).
- [Support code and receipt](https://github.com/zuizui0223/bita/blob/analysis/route-retention-composition-v1/empirical/route_retention_composition/ROUTE_RATE_ESTIMAND_COMMON_SUPPORT_AUDIT_V1.md).
- [Verified source-support sensitivity](https://github.com/zuizui0223/bita/actions/runs/38062435342).
- [Original finite/extended robbery MLE diagnosis](https://github.com/zuizui0223/bita/blob/analysis/route-retention-composition-v1/empirical/route_retention_composition/EXTENDED_MLE_EXPLORATORY_REPRO_AND_CLAIM_DECISION_V1.md).

## Claim ceiling

Permitted: mismatch is associated with a high robbery **share** in
Ecuador and a strong **separately estimated** reduction in
legitimate feeding under the literature-based 1.8× effective-reach
sensitivity. No statistically resolved increase of the separately
estimated robbery rate was found.

Not permitted: equal opportunity support for the two fitted RR
coefficients; a causal behavioral replacement factor of 5.31; no
change at all in robbery rates; individual birds switching between
legitimate and robbery on recorded visits; adaptive fitness rescue.

The title remains descriptive: higher conditional robbery prevalence
**need not** imply higher absolute robbery frequency.

External submission remains blocked until Zenodo DOI reservation and
author-controlled metadata/approval are completed; no external
journal submission is implied by this branch.
