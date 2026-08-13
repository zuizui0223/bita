# Theoretical Ecology submission checklist — Mechanism → Pattern paper

## Canonical manuscript architecture

- [x] Canonical manuscript exists: `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md`
- [x] Title explicitly states **Mechanistic theory and meta-analytic patterns**
- [x] Abstract asks the paired questions: what mechanism determines the sign, and what cross-system Pattern recurs?
- [x] **Part I — Mechanism** contains the mathematical theory and sensitivity analysis
- [x] **Part II — Pattern** contains meta-analysis and saturated cross-study Pattern synthesis
- [x] Section 6 explicitly integrates mechanism → Pattern
- [x] Old interleaved theory/evidence section structure is retired and regression-tested

## Part I — Mechanism

- [x] `W_AD` is a local mixed partial on declared trait/outcome coordinates
- [x] Signed identity `W_AD = M_AD - G_AD - C_AD` precedes biological orientation
- [x] Orientation gate is explicit
- [x] Oriented mechanism criterion `W_AD = rho - iota - kappa` is explicit
- [x] Proposition 1 preserves structural mechanism non-identifiability from total `W`
- [x] Environmental derivative balances and directional inequalities are explicit
- [x] Canonical endpoint-normalized sensitivity analysis retains all 2,592 evaluations
- [x] Finite-grid occupancy is never interpreted as prevalence in nature
- [x] Figure 1 communicates signed identity → orientation gate → oriented balance → inference boundary
- [x] Figure 2 is the canonical mechanistic sign-regime sensitivity figure
- [x] Tables 1–2 are explicitly assigned to Part I — Mechanism

## Part II — Pattern

- [x] Meta-analysis is used only where outcomes admit a defensible common quantitative scale
- [x] **Meta-analysis 1 — Leal et al. 2025 floral larceny** uses random-effects synthesis on oriented LRRs
- [x] Leal canonical patterns retained: female fitness `-0.210` (48 clusters), nectar `-0.483` (28), visitation `-0.291` (22)
- [x] Leal heterogeneity, dependence, influence, and sensitivity diagnostics remain explicit
- [x] Leal modern-estimator sensitivity uses the same independent-cluster inputs with REML + modified Hartung–Knapp and leaves the canonical DerSimonian–Laird estimates unchanged
- [x] Female-fitness mHK CI remains below zero: `[-0.3318, -0.0777]`
- [x] Nectar mHK CI remains below zero: `[-0.7948, -0.1840]`
- [x] Legitimate-visitation mHK CI remains below zero but **borderline to zero**: `[-0.5756, -0.00018]`
- [x] **Meta-analytic synthesis 2 — Sasidharan et al. 2023 FVOCs** retains the conservative 32-study-component topology
- [x] Sasidharan assembled RD `+0.129`, LOCO positive `32/32`, paired-role limitation, and behavioral context dependence remain explicit
- [x] Saturated route ledger is **56 records / 25 independent biological clusters**, explicitly a theory-to-Pattern scaffold rather than a grand meta-analysis
- [x] Four route families are synchronized at `5 / 8 / 18 / 10` independent clusters
- [x] 14 same-system multi-route clusters and 17 context/sign-switch clusters map recurrence/conditionality without a fabricated common effect size
- [x] Seven context-only programs are tracked separately and excluded from route-ledger N
- [x] Expansion uses a registered saturation rule; two consecutive targeted batches yielded no new admissible Pattern class
- [x] Guarded defence, spatial/temporal/attack-mode filtering, visitor functional-mode routing, lifecycle-stage role reversal, and population/trait-class dependence are explicit Pattern states
- [x] Haas-Desmarais 2026, Caruso 2019, and Junker–Blüthgen 2010 are labelled **secondary contextual/cross-synthesis modules**, not reproduced pooled analyses
- [x] Haas-Desmarais publisher supplement package was independently retrieved and hashed; no false claim of local raw-effect reanalysis
- [x] Caruso Dryad landing/API metadata and workbook identities were verified; access-layer block is not relabelled missing data or biological null
- [x] Direct `A x D` search remains one strict sign-unresolved cluster
- [x] Direct joint-cost search remains zero strict estimates; `kappa` is unidentified, not zero
- [x] Cross-system Pattern conclusion is explicit: **recurrent mechanisms plus context-dependent balance**, not a universal sign of `W_AD`
- [x] Figure 3 is generated from the saturated evidence state and preserves the identification boundary
- [x] Tables 3–4 are synchronized to the 25-system Pattern candidate
- [x] Leal/Sasidharan robustness remains Supplementary Figure S4 rather than overloading main Figure 3

## Theory ↔ Pattern inference boundary

- [x] Marginal route evidence is not called `W_AD`
- [x] Same-system evidence is not called direct `A x D`
- [x] Context-only programs are not added to route-ledger N
- [x] Secondary-synthesis study/observation counts are not added to route-ledger N
- [x] Study/publication counts are not model parameters
- [x] Screened/deposited fractions are not prevalence estimates
- [x] Incompatible outcomes are not pooled merely to manufacture a meta-analysis
- [x] Neither reproduced quantitative synthesis is presented as empirical calibration of `rho`, `iota`, `kappa`, or `W_AD`
- [x] Secondary contextual syntheses are not presented as empirical calibration of `W_AD`
- [x] REML/mHK sensitivity is not presented as a new canonical effect estimate or as stronger biological homogeneity

## Figures, tables, and reproducibility

### Main figures/tables

- [x] Figures 1–3 have canonical SVG scientific sources
- [x] Figure 2 is protected against `endpoint_normalized_grid_v2_report.json`
- [x] Expanded Figure 3 is byte-reproducible from its builder and saturated evidence inputs
- [x] Pattern-expansion readout regenerates `56 / 25 / 14 / 17` from committed ledgers
- [x] Tables 1–4 follow the Part I Mechanism / Part II Pattern split
- [x] Submission EPS filenames follow `Fig1.eps`, `Fig2.eps`, `Fig3.eps`
- [x] Submission exporter deterministically strips the visible outer title from each canonical SVG while retaining panel/scientific content
- [x] EPS output remains vector and converts text to paths to prevent font substitution
- [x] Submission-form EPS export passed from source head `fe274a91349931c08b8d820f99dc7b3ab5d8f725`
- [x] Submission-form EPS artifact provenance: run `31666278452`, artifact `9168041835`, SHA-256 `f4fb42b7421958a5a5251f24f03c666de2735b28bbded739286e65e9705090fd`
- [x] Core CI and `submission-scope` passed at that same source head

### Supplementary package

- [x] Reader-facing supplement source exists at `manuscript/supplementary/SUPPLEMENTARY_MATERIAL.md`
- [x] Figures S1–S4 are generated reproducibly
- [x] Tables S1–S6 are generated reproducibly from authoritative inputs
- [x] Fig. S1 checks analytic vs finite-difference mixed partials over all 2,592 evaluations
- [x] Fig. S2 reports scenario/response-shape sign maps without treating finite-grid occupancy as prevalence
- [x] Fig. S3 reports the saturated 14-system same-system route matrix without treating cells as effect sizes
- [x] Fig. S4 retains canonical DL LRRs/I² and Sasidharan LOCO structure
- [x] Fig. S4 is deterministically augmented from `LEAL_2025_MODERN_ESTIMATOR_SENSITIVITY_V1.json` with REML + modified Hartung–Knapp intervals
- [x] Fig. S4 augmentation is idempotent and regression-tested
- [x] Supplement build workflow reproduces Part I evaluations, Figures S1–S4, Tables S1–S6, and validates them before generated-asset commit
- [x] Current supplementary-package workflow completed successfully after modern-estimator synchronization
- [ ] Render the final reader-facing supplementary PDF after author/release metadata and archival DOI are frozen

## Theoretical Ecology / Springer structural formatting

- [x] Abstract is automatically constrained to **150–250 words**
- [x] Abstract defines “log response ratio” rather than using unexplained `LRR`
- [x] Keywords are automatically constrained to **6** (within the journal's 4–6 range)
- [x] Title-page placeholders explicitly reserve authors, affiliations, corresponding-author e-mail, and ORCID fields without inventing values
- [x] Non-copyediting LLM use is disclosed in Methods as AI-assisted code generation, structured literature triage, and manuscript drafting; authors retain responsibility
- [x] Figure captions use `**Fig. n**` outside illustrations, with no punctuation after the number or at caption end
- [x] `Statements and Declarations` follows `References`
- [x] Funding, competing interests, author contributions, and data/code availability have required post-reference headings
- [x] Funding/competing-interest text remains author-confirmation placeholders rather than fabricated declarations
- [x] Cover-letter/package templates reserve **exactly five** conflict-checked reviewer slots
- [x] House-style transformation is idempotent and regression-tested
- [ ] Render the final author-approved manuscript in the chosen journal upload format after author/title-page/declaration fields are supplied
- [ ] If submitting a Word manuscript, include the journal-requested companion PDF of the manuscript
- [ ] Package supplementary text/presentation material as final PDF and tabular supplements in appropriate CSV/XLSX files after release metadata are frozen

## Literature and references

- [x] Expanded **20-reference** scientific spine is citation-presence regression-tested
- [x] New representative Pattern references are included for Page 2014, Sun & Huang 2015, Wu & Gao 2024, and Zhou et al. 2020
- [x] Secondary-synthesis references are included for Haas-Desmarais 2026, Caruso 2019, and Junker & Blüthgen 2010
- [x] Stevenson 2017 metadata correction is preserved
- [x] Erroneous/uncited legacy references remain pruned
- [x] Bibliography is alphabetically ordered
- [x] Current name-year/DOI structure is compatible with Springer guidance and is regression-tested
- [ ] Run the final rendered-file citation/reference consistency pass after any author-controlled wording or author-list edit

## Submission support

- [x] Cover letter presents **Part I Mechanism + Part II Pattern** and the saturated 56/25 architecture
- [x] Submission scope explicitly defines the saturated Mechanism → Pattern package
- [x] Root README is synchronized to the 56/25 saturated Pattern candidate
- [x] Manuscript README explicitly defines Mechanism → Pattern
- [x] Portal title, abstract, keywords, and framing are synchronized to the saturated manuscript
- [x] Figure/Table plan assigns Figures/Tables to Mechanism versus Pattern roles and uses saturated Part II counts
- [x] Final audit, manuscript audit, supplement manifest, reference audit, figure-export receipt, and Springer upload plan are synchronized to the 25-system candidate
- [x] Current submission-form EPS export is validated and its digest recorded
- [x] Supplementary robustness display is synchronized to the modern Gate G estimator sensitivity
- [ ] Exact repository release/tag and archival DOI
- [ ] Repository licence/licence statement chosen by the author(s)

## Author-controlled portal information still required

- [ ] Final author order and publication names
- [ ] Affiliations
- [ ] Corresponding author and email
- [ ] ORCIDs
- [ ] CRediT roles
- [ ] Funding/grant information or explicit no-funding confirmation
- [ ] Acknowledgements
- [ ] Competing-interest confirmation
- [ ] Exactly five potential reviewer names, institutions, e-mails, expertise notes, and conflict checks
- [ ] Suggested reviewer exclusions if any are genuinely justified
- [ ] Confirmation that all authors approve the exact submitted version and that it is not under consideration elsewhere

## Submission decision

**Scientific structure: GO. Saturated Pattern package: GO. Evidence-expansion gate: CLOSED/SATURATED. Journal structural house style: PASS. Main submission-form EPS: GREEN. Supplementary source package: GREEN/REPRODUCIBLE. Actual journal submission remains blocked only by author-controlled metadata/declarations/reviewers/licence, final rendered manuscript/supplement files, release/archive DOI, all-author approval, and the authenticated external portal.**

Do not add another broad meta-analysis merely to make Part II look larger. The registered expansion has saturated its current theory-facing Pattern classes. The intended result remains recurrent constituent mechanisms plus context-dependent balance while preserving the direct-identification gaps.
