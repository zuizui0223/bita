# Publication status

## Primary submission paper

> **Access constraints reroute floral exploitation across bird and insect visitor networks**

Article type: **Ecology Letters Letter**.

## Inferential spine

```text
PRIMARY:
Aubert / EPHI all-Ecuador bird–flower network
1,378 pair-site units
barrier robbery 0.307 vs accessible 0.081
site-adjusted rho = 0.351
within-site permutation p = 0.0001
15 / 17 comparable sites same direction

CORROBORATION:
Sakhalkar Afrotropical insect–flower network
57 plant species
rho = 0.347
permutation p = 0.0086
multitrait sensitivity does not isolate tube length uniquely

JOINT:
equal network weight
rho_J = 0.349
p = 0.0001
k = 2 independent networks
```

The joint statistic tests recurrence across these two networks only. It does not estimate between-network heterogeneity, a network-population mean, or generality beyond the two systems.

## Mechanistic boundary

The current routing claim is now expressed as a **relative-route-cost** condition.

~~~text
D(x) = C_legitimate(x) - C_bypass(x)

dD/dx > 0  -> bypass propensity increases
dD/dx ≈ 0  -> weak / null routing response
dD/dx < 0  -> bypass propensity can decrease
~~~

Thus the paper no longer implies a universal “longer flower = more robbery” rule.
Access constraints promote rerouting when they penalize legitimate access more than
the bypass route. Null, mixed and opposite direct studies define boundary conditions
for this mechanism.

## Direct empirical and mechanistic context

The standardized joint network statistic remains **k = 2**.

A separate bounded discovery corpus now contains **24 independent direct
access-geometry → nectar-robbery study programs** outside the two standardized
network datasets:

~~~text
POSITIVE = 16
NULL = 5
OPPOSITE = 1
MIXED = 2
NETWORK_K_CONTRIBUTION = 0
~~~

This layer includes experiments, population studies and community studies. It is
used to show that the biological relation has been directly tested beyond the two
standardized networks, while the retained null, mixed and opposite systems expose
boundary conditions. Because the discovery search is not a systematic-review
denominator, these counts are not a success rate, prevalence estimate, sign test or
pooled effect.

A stricter formal-recurrence lane uses the **56 distinct Leal et al. (2025)
`study`-field labels** as an outcome-independent historical anchor. They are not
assumed to be 56 independent studies: source audit found two labels that combine
rows from different source programs. Current label-level screening is 50
geometry-ineligible, 4 eligible, and 2 provenance-conflicted. Only 4 of the 24
direct programs overlap the Leal frame. The two source conflicts do not affect geometry eligibility: all verified/plausible
source components are geometry-ineligible, so the historical direct-eligible set is
stable at four. The deterministic bibliographic-frame builder, frozen Q1–Q8 query contract, provider-export normalizer, one-command Q1–Q8 intake, and post-freeze 24-program screening bootstrap are implemented. The remaining gate before any formal recurrence statistic is one complete Q1–Q8 export from a single bibliographic database; normalization, deterministic deduplication and frame freezing are then automated.

The floral-defence corpus and effective-access / exposure framework are retained as
mechanistic context for why route switching is biologically plausible. They are not
the Letter's primary statistical evidence.

Matched effective-domain coding is author-derived and has not yet undergone
outcome-blind independent recoding. Therefore the Letter does not use the 11-system
state alignment as independent validation.

## Extended paper preserved

The broader manuscript remains available as a reserve Synthesis / full research architecture:

> **Access and exposure domains organize floral defence selectivity and interaction routing across plant–visitor systems**

It contains the 17-program defence corpus, matched-system state recovery, eight within-D conditionality systems, and the two network analyses. It is no longer the first external submission.

## Preserved identification paper

> **Trait interaction is not ecological mechanism.**

The identification framework remains supporting provenance and claim discipline.

## Initial-submission readiness gate

The scientific and package layers are ready, but Ecology Letters requires an externally archived analysis-data/code package with a persistent DOI at initial submission.

Current blockers:

~~~text
ACCESS_ROUTING_ARCHIVE = STAGING_READY
ACCESS_ROUTING_ARCHIVE_DOI = RESERVE_IN_ZENODO_DRAFT_BEFORE_FINAL_PACKAGE_BUILD
RESERVED_DOI_APPLICATOR = scripts/apply_reserved_archive_doi.py
AUTHOR_METADATA_CONTRACT = submission/ECOLOGY_LETTERS_LETTER_AUTHOR_METADATA_V1.json
FINAL_AUTHOR_LIST_AND_AFFILIATIONS = REQUIRED
AUTHORSHIP_STATEMENT = REQUIRED
CONFLICT_OF_INTEREST = REQUIRED
FUNDING_ACKNOWLEDGMENTS = REQUIRED
AUTHOR_RELATIVE_NOVELTY_STATEMENT = REQUIRED
EXTERNAL_SUBMISSION = BLOCKED_UNTIL_THESE_ARE_COMPLETE
~~~

The archive contract contains the exact 57-species and 1,378-pair-site analysis tables, metadata, reproduction code and frozen outputs. The remaining data sequence is: reserve the Zenodo DOI first, insert it into the submission files, freeze that DOI-bearing commit, build the exact final ZIP from that commit, upload it to the same draft, and publish the DOI record.

## Journal route

```text
1. Ecology Letters — Letter
2. Functional Ecology — Research Article fallback
3. Oikos — Research fallback
4. extended Synthesis retained for later use
```

```text
STATUS = SCIENTIFIC_PACKAGE_READY
ACTIVE_PAPER = ACCESS_ROUTING_LETTER
ROUTING_MECHANISM = RELATIVE_ROUTE_COST
ROUTE_COST_BOUNDARY = dC_LEGITIMATE_MINUS_dC_BYPASS
DIRECT_ACCESS_GEOMETRY_PROGRAMS = 24
DIRECT_EVIDENCE_DIRECTIONS = 16_POSITIVE_5_NULL_1_OPPOSITE_2_MIXED
FORMAL_HISTORICAL_FRAME = LEAL2025_56_STUDY_FIELD_LABELS
FORMAL_HISTORICAL_SOURCE_PROGRAMS = NOT_YET_FINAL
FORMAL_HISTORICAL_PROVENANCE_CONFLICTS = 2
HISTORICAL_DIRECT_ELIGIBLE_SET = RESOLVED_AT_4_INVARIANT_TO_CONFLICT_SPLIT
STAGE_U_BATCHES_1_2 = 23_CANDIDATES_9_ELIGIBLE_1_DUPLICATE_13_INELIGIBLE
STAGE_U_SEARCH = FINAL_SYNONYM_PASS_COMPLETE_BOUNDED_SEARCH_STILL_NOT_FORMAL
FORMAL_BIBLIOGRAPHIC_FRAME_BUILDER = IMPLEMENTED
BIBLIOGRAPHIC_EXPORT_NORMALIZER = IMPLEMENTED_SCOPUS_WOS_CROSSREF_OPENALEX
BIBLIOGRAPHIC_Q1_Q8_ONE_COMMAND_INTAKE = IMPLEMENTED
BIBLIOGRAPHIC_SINGLE_ZIP_INTAKE = IMPLEMENTED_SAFE_ROOT_ONLY_COUNT_VERIFIED_FRAME_FREEZE_SCREEN_BOOTSTRAP
BIBLIOGRAPHIC_POST_FREEZE_SCREEN_BOOTSTRAP = IMPLEMENTED_DOI_AND_TITLE_YEAR_ALIAS
BIBLIOGRAPHIC_KNOWN_CORPUS_RECALL_AUDIT = IMPLEMENTED_24_PROGRAMS
BIBLIOGRAPHIC_SINGLE_ZIP_ONE_COMMAND = IMPLEMENTED_FRAME_FREEZE_AND_PENDING_SCREEN
FORMAL_BIBLIOGRAPHIC_FRAME = AWAITING_ONE_COMPLETE_SINGLE_DB_Q1_Q8_EXPORT_ZIP
FORMAL_RECURRENCE_RESULT = NOT_YET_OPENED
EXTENDED_SYNTHESIS = PRESERVED_RESERVE
LEGACY_IDENTIFICATION_PAPER = PRESERVED_SUPPORT
DATA_CODE_ARCHIVE = STAGING_READY_RESERVED_DOI_THEN_FINAL_BUILD
DOI_APPLICATION_GATE = IMPLEMENTED_RECEIPT_RENDER_ARCHIVE_CHECKS
AUTHOR_METADATA = MACHINE_READABLE_CONTRACT_READY_VALUES_REQUIRED
NEXT_EXTERNAL_ACTION = CREATE_ZENODO_DRAFT_AND_RESERVE_DOI
EXTERNAL_SUBMISSION = BLOCKED_PENDING_RESERVED_DOI_FINAL_ARCHIVE_AND_AUTHOR_CONTROLLED_VALUES
```
