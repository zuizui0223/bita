# Submission scope — BITA access-routing Letter

Primary forward route: **Ecology Letters — Letter**.

Primary manuscript:

`manuscript/MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md`

## Canonical question

> **When legitimate access becomes more constrained, does exploitation simply decline, or does it reroute toward bypass?**

## 1. Primary prediction

```text
access mismatch increases
        ->
legitimate route becomes less usable
        ->
if bypass remains available:
bypass / robbing propensity increases
```

The prediction is ordinal and does not require one common mechanistic coefficient across taxa.

## 2. Primary empirical test — Ecuador birds

```text
n = 1,378 bird × plant × site units
18 Ecuador sites
barrier robbery     = 0.30698
accessible robbery  = 0.08139
difference          = +0.22560
global mismatch rho = 0.41826
site-adjusted rho   = 0.3505
within-site permutation p = 0.0001
15 / 17 comparable sites in same direction
min >= 5 interactions:
  n = 702
  difference = +0.264
  rho = 0.505
  p = 0.0001
```

This is an observational all-Ecuador extension, not an exact replication of the source three-transect GLMM.

## 3. Independent corroboration — Sakhalkar insects

```text
n = 57 plant species
rho = 0.346786
permutation p = 0.0086
full multitrait model p = 0.2016
tube-length block p = 0.2110
```

The licensed claim is access-geometry association, not a unique causal tube-length effect.

## 4. Joint network test

```text
r_A = 0.3505
r_S = 0.3468
equal-network Fisher-z rho_J = 0.3487
joint permutation p = 0.0001
independent network contributions k = 2
```

Raw observations are never pooled. The joint test does not estimate between-network heterogeneity, a population mean across networks, or generality beyond the two systems.

Both analyses are observational and are not pooled onto one effect scale.

## 5. Third independent network priority

The current \(k=2\) ceiling is the highest-priority unresolved scientific limit.

The frozen confirmatory protocol and completed public-data search are:

- `empirical/floral_defence_selectivity/THIRD_ACCESS_ROUTING_NETWORK_PREREG_V1.md`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_CANDIDATE_REGISTRY_V1.csv`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_BOUNDED_SEARCH_V1.md`

The bounded Dryad / Zenodo / OSF / Figshare search found no public dataset that
passed all frozen gates. The estimand was not relaxed.

The active lane is now one prospective **non-flying-mammal × Protea** network:

- `empirical/floral_defence_selectivity/THIRD_NETWORK_PROSPECTIVE_MAMMAL_DESIGN_V1.md`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_PROSPECTIVE_SCHEMA_V1.csv`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_EVENT_SCHEMA_V1.csv`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_ROUTE_CODING_MANUAL_V1.md`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_PILOT_SPLIT_CONTRACT_V1.md`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_SEED_RECEIPT_V1.json`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_CONFIRMATORY_FREEZE_RECEIPT_TEMPLATE_V1.json`
- `scripts/validate_third_network_confirmatory_freeze.py`
- `scripts/evaluate_third_network_route_reliability.py`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_ROUTE_BLIND_PRESURVEY_SCHEMA_V1.csv`
- `scripts/evaluate_third_network_route_blind_presurvey.py`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_FIELD_READINESS_TEMPLATE_V1.json`
- `scripts/evaluate_third_network_field_readiness.py`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_FIELD_EXECUTION_GATE_V1.md`
- `scripts/build_third_access_routing_units.py`
- `scripts/analyze_third_access_routing_network.py`
- `scripts/analyze_joint_access_routing_k3.py`
- `scripts/run_third_network_confirmatory_pipeline.py`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_CONFIRMATORY_ANALYSIS_RUNNER_V1.md`
- `scripts/run_third_network_synthetic_e2e.py`
- `scripts/run_third_network_release_rehearsal.py`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_RELEASE_REHEARSAL_V1.md`
- `scripts/package_third_network_confirmatory_release.py`
- `scripts/reproduce_third_network_confirmatory_release.py`
- `scripts/verify_third_network_release_package.py`
- `scripts/ingest_third_network_release_archive.py`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_RELEASE_CODE_MANIFEST_V1.txt`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_CONFIRMATORY_RELEASE_PACKAGE_V1.md`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_SYNTHETIC_E2E_V1.md`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_CAPE_COLLABORATION_ROUTE_V1.md`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_CAPE_CONTACT_VERIFICATION_V1.md`
- `submission/THIRD_NETWORK_CAPE_COLLABORATION_EMAIL_V1.md`
- `submission/THIRD_NETWORK_CAPE_FIRST_CONTACT_PACKET_V1.md`
- `submission/THIRD_NETWORK_CAPE_FEASIBILITY_FORM_V1.md`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_COLLABORATION_RESPONSE_SCHEMA_V1.csv`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_COLLABORATION_RESPONSE_QUARANTINE_V1.md`
- `scripts/evaluate_third_network_collaboration_response.py`
- `scripts/verify_third_network_confirmatory_bundle.py`
- `scripts/plan_third_network_claim_transition.py`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_CLAIM_TRANSITION_GATE_V1.md`
- `trait_architecture/existing_k3_inputs.py`
- `empirical/floral_defence_selectivity/EXISTING_K3_INPUT_FINGERPRINTS_V1.json`

The same predeclared estimand remains:

~~~text
greater legitimate-route access constraint
        ->
greater bypass / robbing propensity
~~~

Prospective safeguards:

- eligibility pilot data are excluded from confirmatory inference;
- pilot B/L presence or absence cannot select/drop confirmatory sites;
- morphology and route coding are frozen separately;
- a fail-closed pre-video freeze receipt must pass before confirmatory route videos are opened;
- route coders do not receive P, V, or M values;
- the reliability subset is the frozen SHA256(seed:event_id) lowest 20% sample
  with seed 20260922;
- route/morphology integration requires Cohen's kappa for L/B/A/N >=0.80;
- the confirmatory planning target is >=70 realized mammal × plant × site units;
- the frozen eligibility minimum remains >=30 units, >=5 mammal species and
  >=5 plant species;
- if the third effect is null-compatible or opposite in sign, it remains the
  confirmatory third network.

~~~text
JOINT_NETWORK_K = 2
PUBLIC_THIRD_NETWORK = NOT_AVAILABLE_UNDER_FROZEN_GATES
ACTIVE_K3_LANE = CAPE_SMALL_MAMMAL_X_PROTEA_PROSPECTIVE
PLANNING_TARGET_UNITS = 70
FIELD_EXECUTION_GATE = IMPLEMENTED_FAIL_CLOSED
FIELD_EXECUTION_STATUS = BLOCKED_PENDING_REAL_SITE_AND_AUTHORIZATION_RECEIPTS
CONFIRMATORY_INPUT_FREEZE = IMPLEMENTED_MANIFEST_REQUIRED
ROUTE_RELIABILITY_GATE = IMPLEMENTED_KAPPA_LBAN_GE_0_80
SYNTHETIC_E2E = IMPLEMENTED_DEVELOPMENT_ONLY
RELEASE_REHEARSAL = IMPLEMENTED_BUNDLE_VERIFY_CLAIM_PLAN_MATRIX
CONFIRMATORY_RELEASE_PACKAGE = IMPLEMENTED_DETERMINISTIC_OFFLINE_REPLAY
RELEASE_PACKAGE_VERIFIER = IMPLEMENTED_READ_ONLY_DIR_ZIP_SHA256
ZIP_METADATA_GUARD = STRICT_REGULAR_0644_NO_SYMLINK_NO_COMMENT_NO_EXTRA
ZIP_RESOURCE_ENVELOPE = IMPLEMENTED_PREEXTRACTION_SIZE_COUNT_STREAMING_LIMITS
SEMANTIC_INPUT_RESOURCE_ENVELOPE = IMPLEMENTED_ROWS_BYTES_MANIFEST_VERIFIED
PRODUCTION_PERMUTATIONS = FROZEN_9999
RELEASE_ARCHIVE_INGEST = IMPLEMENTED_PREEXTRACTION_CHECKSUM_ATOMIC_PUBLISH
CROSS_PYTHON_ARCHIVE_DETERMINISM = VERIFIED_BYTE_IDENTICAL_3_10_3_11_3_12
CONFIRMATORY_RUNNER = IMPLEMENTED_ONE_COMMAND_TRANSACTIONAL_COMMIT_BOUND
CONFIRMATORY_BUNDLE_VERIFIER = IMPLEMENTED_READ_ONLY_SHA256
EXISTING_NETWORK_K3_INPUTS = CANONICAL_PUBLIC_ROWS_FROZEN_AND_PRODUCTION_ENFORCED
EXISTING_NETWORK_CANONICAL_REBUILD = SAKHALKAR_57_AND_AUBERT_EPHI_1378_MATCH_FROZEN_DIGESTS
CLAIM_TRANSITION_GATE = IMPLEMENTED_RETAINED_RESULT_NO_PVALUE_SELECTION
REAL_THIRD_NETWORK_DATA = NOT_COLLECTED
NEXT_EXTERNAL_ACTION = OUTCOME_BLIND_CAPE_COLLABORATION_INQUIRY
COLLABORATION_EMAIL = SEND_READY_AUTHOR_SEND_APPROVAL_REQUIRED
COLLABORATION_FEASIBILITY_FORM = READY
COLLABORATION_RESPONSE_QUARANTINE = IMPLEMENTED
K3_GENERALITY_TEST = PROSPECTIVE_MAMMAL_DESIGN_FROZEN_PENDING_DATA
~~~

## 6. Mechanistic and direct empirical context only

The broader floral-defence evidence package remains useful for interpretation:

```text
17 unique D-side study programs
10 same-defence pollinator follow-ups
8 independent within-D state-switch systems
```

A separate bounded discovery corpus now records direct empirical tests of
access geometry -> nectar robbery outside the two standardized network datasets:

```text
DIRECT_ACCESS_GEOMETRY_STUDY_PROGRAMS = 18
POSITIVE = 12
NULL = 4
OPPOSITE = 1
MIXED = 1
NETWORK_K_CONTRIBUTION = 0
PRIMARY_STANDARDIZED_NETWORK_K = 2
```

This direct corpus includes experimental, population-level and community-level
studies, including an 88-species four-community study, a 13-species Cape sunbird
guild, a 16-species Andean flowerpiercer community, a retained 2025 null test,
a three-population mixed result, and a 2026 `Erica` boundary-condition study in
which longer corollas predicted lower robbery in the primary model.
It is a discovery corpus, not a systematic-review denominator: no prevalence,
sign-test, pooled effect or extra network replicate is licensed from these counts.

Contract and ledger:

- `empirical/floral_defence_selectivity/DIRECT_ACCESS_GEOMETRY_ROBBERY_CONTRACT_V1.md`
- `empirical/floral_defence_selectivity/DIRECT_ACCESS_GEOMETRY_ROBBERY_CORPUS_V1.csv`
- `empirical/floral_defence_selectivity/DIRECT_ACCESS_GEOMETRY_ROBBERY_SEARCH_V1.md`
- `scripts/summarize_direct_access_geometry_corpus.py`

Formal-recurrence scaffolding is now frozen but **not yet opened for inference**:

```text
HISTORICAL_FRAME = LEAL_2025_ROBBER_STUDY_FIELD
HISTORICAL_STUDY_FIELD_LABELS = 56
HISTORICAL_SOURCE_RESOLVED_PROGRAMS = NOT_YET_FINAL
PROVENANCE_CONFLICT_LABELS = 2
DIRECT_DISCOVERY_PROGRAMS = 18
DISCOVERY_OVERLAP_WITH_HISTORICAL_FRAME = 4
DISCOVERY_NOT_IN_HISTORICAL_FRAME = 14
HISTORICAL_SCREEN = 50_INELIGIBLE_4_ELIGIBLE_2_PROVENANCE_CONFLICT
STAGE_U_BATCH_1 = 12_CANDIDATES_3_ELIGIBLE_1_DUPLICATE_8_INELIGIBLE
STAGE_U_SEARCH = CONTINUES
FORMAL_RECURRENCE_RESULT = NOT_YET_OPENED
```

Assets:

- `empirical/floral_defence_selectivity/LEAL2025_ROBBER_STUDY_FRAME_V1.csv`
- `empirical/floral_defence_selectivity/DIRECT_ACCESS_GEOMETRY_LEAL2025_CROSSWALK_V1.csv`
- `empirical/floral_defence_selectivity/DIRECT_ACCESS_GEOMETRY_FORMAL_RECURRENCE_FRAME_V1.md`
- `scripts/validate_direct_access_geometry_formal_frame.py`
- `empirical/floral_defence_selectivity/LEAL2025_STUDY_LABEL_PROVENANCE_AUDIT_V1.md`
- `empirical/floral_defence_selectivity/LEAL2025_DIRECT_GEOMETRY_SCREEN_V1.csv`
- `empirical/floral_defence_selectivity/DIRECT_ACCESS_GEOMETRY_STAGE_U_REGISTRY_V1.csv`
- `scripts/validate_direct_access_geometry_stage_u.py`

The Leal `study` field is an outcome-independent historical anchor, but its 56
distinct labels are not automatically 56 independent biological programs. A
provenance audit identified two split-required labels. Of the 56 labels, current
screening has 50 ineligible geometry labels, 4 eligible direct tests, and 2
provenance conflicts. Only 4 of the 18 current direct programs overlap the frame.
Both source-level repair and a separate systematic geometry-specific update/gap-fill
search must be completed before any directional recurrence test.

Matched effective-domain classifications are author-coded and have not yet undergone outcome-blind independent recoding. They are therefore not treated as independent validation in the Letter, and the 11/11 state alignment is not a headline or confirmatory result.

These counts describe evidence structure, not natural prevalence, and they are not pooled into one grand meta-analytic effect.

## 7. Required claim boundaries

Do not claim:

- either network establishes causality;
- Sakhalkar uniquely identifies tube length;
- the two networks estimate a universal effect;
- `k=2` demonstrates network-wide generality;
- source-audited domain coding is independently validated;
- matched-domain alignment estimates prevalence or a confirmatory success rate;
- the access-routing result identifies evolutionary origin of floral barriers.

## 8. Ecology Letters initial-submission archive gate

Before external upload, deposit the CI-built analysis-data/code archive in a DOI-bearing repository.

Required archive contents:

~~~text
57-row anonymous Sakhalkar species analysis table
1,378-row anonymous Aubert/EPHI pair-site analysis table
column metadata
exact reproduction code
frozen aggregate outputs
repository commit receipt
~~~

The archive DOI must appear in the manuscript Data accessibility statement and title page. Public source DOIs alone do not replace this submission-stage archive.

Current state:

~~~text
ARCHIVE_STAGING = READY
ARCHIVE_DOI = RESERVE_IN_ZENODO_DRAFT_BEFORE_FINAL_PACKAGE_BUILD
DOI_APPLICATION_GATE = IMPLEMENTED_RECEIPT_RENDER_ARCHIVE_CHECKS
AUTHOR_METADATA_CONTRACT = submission/ECOLOGY_LETTERS_LETTER_AUTHOR_METADATA_V1.json
~~~

## 9. Preserved reserve papers

Extended Synthesis:

- `manuscript/MANUSCRIPT_FLORAL_DEFENCE_SELECTIVITY_V0.md`
- `manuscript/CLAIM_FREEZE_MACRO_V0.md`
- `submission/ECOLOGY_LETTERS_SYNTHESIS_PROPOSAL_V0.md`
- `submission/FUNCTIONAL_ECOLOGY_ADAPTATION_V0.md`

Mechanism-identification foundation:

The preserved inference principle remains `trait interaction != ecological mechanism`; it constrains interpretation but is not the Letter headline.
The mechanism-identification manuscript is preserved support and is no longer the primary submission identity.

- `manuscript/MANUSCRIPT_TRAIT_DIFFERENTIATION_V1.md`
- `manuscript/MANUSCRIPT_IDENTIFICATION_DESIGN.md`
- `manuscript/CLAIM_FREEZE.md`

## 10. Current state

```text
PRIMARY_FORWARD_PAPER = ACCESS_ROUTING_LETTER
PRIMARY_DATASET = AUBERT_EPHI_ALL_ECUADOR
INDEPENDENT_CORROBORATION = SAKHALKAR_INSECTS
JOINT_NETWORK_K = 2
EXTENDED_SYNTHESIS = PRESERVED_RESERVE
REPRODUCIBLE_ANALYSES = READY
LETTER_PACKAGE = READY
DATA_CODE_ARCHIVE = STAGING_READY_RESERVED_DOI_THEN_FINAL_BUILD
AUTHOR_CONTROLLED_METADATA = MACHINE_READABLE_CONTRACT_READY_VALUES_REQUIRED
NEXT_EXTERNAL_ACTION = CREATE_ZENODO_DRAFT_AND_RESERVE_DOI
EXTERNAL_SUBMISSION = BLOCKED_PENDING_RESERVED_DOI_FINAL_ARCHIVE_AND_AUTHOR_CONTROLLED_VALUES
```
