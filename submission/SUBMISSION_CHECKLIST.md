# Theoretical Ecology submission checklist — canonical paperization state

This checklist tracks only the **current submission gates**. Historical workflow IDs, source-recovery chronology, and superseded manuscript states belong in the audit/receipt files and Git history rather than in this live checklist.

## 1. Scientific freeze — PASS

- [x] Canonical manuscript: `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md`
- [x] Canonical title: **When are floral attraction and defence complementary? A one-sided mechanistic bound and cross-system patterns**
- [x] Part I and Part II remain inferentially distinct: **Mechanism → Pattern**, not theory → validation
- [x] `W_AD = rho - iota - kappa` is presented as bookkeeping rather than the novelty
- [x] One-sided theorem is explicit: under non-negative joint-cost curvature, `W_AD > 0 => rho > iota`
- [x] Selectivity window is necessary, not sufficient
- [x] 2,592 finite evaluations and 77.2% window precision are retained as design/implementation results, not natural prevalence
- [x] Pattern architecture is fixed at 56 route-level records / 25 independent biological clusters
- [x] Four marginal route families remain `5 / 8 / 18 / 10`
- [x] Same-system multi-route state remains 14 clusters
- [x] Context/sign-switch state remains 17 clusters
- [x] Seven context-only programs remain excluded from route-ledger N
- [x] Leal H-gate interpretation remains: female-fitness LRR about `-0.210`, 48 clusters, 35/48 negative, prediction interval about `-1.13` to `+0.71`, declared moderators 0–8%
- [x] Reward → visitation → female-fitness sequence remains constituent-path evidence, not a demonstrated mechanism chain
- [x] Direct total `A × D` evidence remains sparse and does not establish a universal sign
- [x] Direct joint-cost curvature remains **unidentified, not zero**
- [x] Sufficiently negative joint-cost curvature remains the unique escape route from the one-sided bound in the declared family
- [x] Next tests are separated: 2 × 2 allocation applicability/falsification gate versus full `A × D` calibration factorial
- [x] `manuscript/CLAIM_FREEZE.md` guards allowed and prohibited claims

## 2. Reproducibility and package — PASS / final-release rerun pending

- [x] Core theory and claim-freeze regression tests are in normal CI discovery
- [x] Python 3.10 / 3.11 / 3.12 CI passes on the paperization line
- [x] `submission-scope` passes on the paperization line
- [x] Main Figures 1–3 retain canonical SVG scientific sources
- [x] Deterministic submission EPS export exists
- [x] Supplementary Figures S1–S4 and Tables S1–S6 retain reproducible builders
- [x] Leal modern-estimator sensitivity remains separate from canonical DL estimates
- [x] Sasidharan 32-component dependence topology remains fixed
- [x] Source-adjudication/provenance products remain versioned
- [ ] Re-run all final manuscript/figure/supplement checks from the exact release commit after author-controlled fields are frozen
- [ ] Generate final reader-facing manuscript and supplementary files from that exact release commit

## 3. Reader-facing manuscript — ACTIVE PAPERIZATION

- [x] Title foregrounds the one-sided mechanistic bound
- [x] Abstract is synchronized between manuscript and portal metadata
- [x] Abstract stays within the current repository-enforced journal word limit and defines “log response ratio”
- [x] Introduction is shortened while retaining prior-art and inference boundaries
- [x] Conclusion ends on a concrete falsification/calibration programme rather than generic “more data are needed” language
- [x] Cover letter foregrounds the one-sided bound and does not present the route ledger as a grand meta-analysis
- [x] Six keywords remain synchronized
- [x] AI-assisted workflow disclosure remains in Methods with author responsibility explicit
- [ ] Final human read for repetition, notation, transitions, and figure/table callouts
- [ ] Final visual QA of the rendered manuscript and supplement

## 4. Inference boundaries — MUST REMAIN TRUE

- [x] Marginal route evidence != `W_AD`
- [x] Same-system evidence != direct total `A × D`
- [x] Route counts != prevalence
- [x] Finite-grid occupancy != prevalence
- [x] Leal pooled effects != `rho`, `iota`, `kappa`, or `W_AD`
- [x] Sasidharan assembled contrast != causal within-study consumer-role effect
- [x] No strict joint-cost estimate != `kappa = 0`
- [x] `W_AD` alone != trait covariance, genetic correlation, evolutionary trajectory, or stable optimum
- [x] A 2 × 2 cost experiment tests the focal trait-pair applicability gate; it does not prove global universality

## 5. References and journal-facing structure — PASS / final check pending

- [x] Current scientific reference spine is citation-presence regression-tested
- [x] Statements and Declarations follow References
- [x] Funding, competing interests, author contributions, and data/code availability headings are present
- [x] Figure captions use journal-compatible `Fig. n` structure
- [x] Exactly five reviewer slots are reserved without inventing identities
- [ ] Final rendered-file citation/reference consistency check after all author-controlled edits

## 6. Human-controlled fields — BLOCK EXTERNAL SUBMISSION

Do not infer or auto-fill these fields.

- [ ] Final author order and publication names
- [ ] Affiliations
- [ ] Corresponding author and active email
- [ ] ORCIDs
- [ ] CRediT roles
- [ ] Funding/grant statement or explicit no-funding confirmation
- [ ] Acknowledgements
- [ ] Competing-interest confirmation
- [ ] Repository licence and licence statement
- [ ] Exactly five reviewer names, institutions, emails, expertise notes, and conflict checks
- [ ] Any justified opposed-reviewer request
- [ ] All-author approval of the exact submitted version
- [ ] Confirmation that the manuscript is not under consideration elsewhere

## 7. Release and portal — BLOCK EXTERNAL SUBMISSION

- [ ] Freeze exact final commit
- [ ] Create immutable release/tag
- [ ] Archive release and insert DOI
- [ ] Re-run final CI / submission-scope / figure / supplement workflows from the release commit
- [ ] Insert exact release commit, tag, DOI, and licence into Data and code availability
- [ ] Render and visually inspect final upload files
- [ ] Upload through authenticated journal portal
- [ ] Confirm portal title, abstract, authors, declarations, reviewers, figures, supplement, and data/code fields match the frozen files

## Current decision

**Scientific conclusion: GO / FROZEN. Repository paperization: ACTIVE. External journal submission: NOT YET — blocked only by final reader-facing QA, author-controlled metadata/declarations/reviewers/licence, exact release/archive DOI, rendered-file QA, all-author approval, and authenticated portal submission.**

Do not reopen broad evidence searching or add another synthesis merely to enlarge Part II unless a specific manuscript claim is falsified, a reviewer identifies a concrete provenance gap, or the frozen inference boundary must be corrected.
