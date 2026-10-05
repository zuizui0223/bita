# Publication status

## Primary submission paper

> **Access constraints predict interaction routing across bird and insect visitor networks**

Article type: **Ecology Letters Letter**.

## Inferential spine

```text
PRIMARY:
Aubert / EPHI all-Ecuador bird–flower network
missing piercing -> legitimate/no per source metadata
2,265 pair-site aggregation units -> 259 plant-species inferential units
plant-level mismatch rho = 0.503
species permutation p = 0.0001
paired barrier contrast: 130 plant species, mean difference +0.0915, p = 0.0001
descriptive pair-site robbery: barrier 0.147 vs accessible 0.020
18 / 18 comparable sites same direction
complete-case yes/no sensitivity retains plant-level direction
within-bird paired barrier: 36 bird species, mean difference +0.0933, p = 0.0001
within-bird continuous: 28 bird species / 1,285 dyads, rho = 0.340, p = 0.0001
24 / 28 bird-specific correlations positive; median rho = 0.338
between-bird mean diagnostic: rho = 0.086, p = 0.551

CORROBORATION:
Sakhalkar Afrotropical insect–flower network
57 plant species
rho = 0.347
permutation p = 0.0086
multitrait sensitivity does not isolate tube length uniquely

JOINT:
plant-species effects, equal network weight
rho_J = 0.428
p = 0.0001
k = 2 independent networks
```

The joint statistic tests recurrence across these two networks only. It does not estimate between-network heterogeneity, a network-population mean, or generality beyond the two systems.

## Novelty boundary

The Letter does **not** claim first discovery of a flower-trait mismatch–robbery
association, behavioral switching between legitimate and robbing tactics, or
relative handling-cost explanations of tactic choice. The manuscript-facing
contribution is now narrower and more biological: **relational mismatch robustly
predicts route composition, whereas whether mismatch becomes an occurrence filter
depends on functional reach rather than raw trait equality**. The within-consumer
test and cross-fauna routing estimand carry the routing result; the hummingbird
reach sensitivity shows that culmen equality is not a defensible universal access
threshold. Relative route cost remains an organizing interpretation, not a novel
foraging theory. The complete guard is
`docs/ACCESS_ROUTING_NOVELTY_BOUNDARY_V1.md`.

## Participation and routing-shape updates

The frozen zero-inclusive analysis used the source-defined binary barrier
`tube > culmen`:

~~~text
trait-matched opportunity edges = 19,909
barrier/access pooled resolved-feeding RR = 1.772
95% plant-jackknife CI = 1.105–2.841
POST_OPEN legitimate/non-robbing RR = 1.883 (1.111–3.190)
POST_OPEN robbery-only RR = 0.463 (0.147–1.461)
~~~

That **culmen-only no-filtering interpretation is no longer the biological claim**.
Hummingbirds extend their tongues beyond the bill, so a second post-open analysis
tested functional-reach definitions in Trochilidae only. The initial sensitivity
froze one-third and 2× multipliers; after opening those results, a deeper literature
audit recovered the 80% extension used as the primary morphology correction by
Vizentin-Bugoni et al. (2016), which is retained explicitly as a post-open
literature-anchored extension.

~~~text
reach multiplier k = 4/3
barrier fraction = 0.413
pooled feeding RR = 0.435 (0.255–0.741)
legitimate RR = 0.354 (0.197–0.635)
robbery RR = 0.851 (0.328–2.207)
P1 paired robbery contrast = +0.191; n = 129; p = 0.0001

reach multiplier k = 1.8
barrier fraction = 0.258
pooled feeding RR = 0.229 (0.147–0.355)
legitimate RR = 0.154 (0.087–0.271)
robbery RR = 0.816 (0.359–1.857)
P1 paired robbery contrast = +0.259; n = 105; p = 0.0001
~~~

The hummingbird-only continuous P1 mismatch–robbery correlation is
`rho = 0.5029` under every fixed multiplier because multiplying reach by a
constant only translates log mismatch. Thus the routing signal is robust while the
binary participation inference changes qualitatively once the barrier is tied to
functional reach. Absolute robbery counts remain imprecise; the higher robbery
share can arise through suppression of legitimate feeding rather than an increase
in robbery events.

The preregistered routing-shape analysis remains a negative localization result:

~~~text
sigmoid midpoint x* = 0.9197
x* at upper 95% mismatch-support boundary = YES
bootstrap 90% CI = 0.1177–0.9197
post-open bootstrap upper-boundary mass = 585/999 (58.6%)
quadratic curvature permutation p = 0.0049
interior upper turnover supported = NO
THRESHOLD_CLASS = THRESHOLD_AT_SUPPORT_BOUNDARY
~~~

Fixed reach multipliers translate the midpoint and mismatch support by the same
`-log(k)`, so they cannot convert this support-boundary midpoint into an interior
threshold. Species-specific tongue extension, corolla opening and nectar depth
remain unresolved.

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

### Prospective causal sign-reversal test

The decisive factorial mechanism test is now implemented but **not run**:

~~~text
CAUSAL_ROUTE_COST_PROTOCOL = IMPLEMENTED_PRE_OUTCOME
CALIBRATION_ROUTE_CHOICE_OUTCOME = NOT_AVAILABLE
CONFIRMATORY_COMPLETED_BEES_TARGET = 60
PRIMARY_CONTRAST_1 = raise C_L only -> bypass increases
PRIMARY_CONTRAST_2 = raise C_B only -> bypass decreases
MATCHED_HIGH_HIGH_DIAGNOSTIC = route share approximately returns to baseline
CAUSAL_SIGN_REVERSAL_RESULT = NOT_YET_AVAILABLE
~~~

The experimental preregistration, schemas, freeze template and fail-closed analysis
code live under `empirical/floral_defence_selectivity/RELATIVE_ROUTE_COST_*` and
`scripts/*relative_route_cost*`. This prospective test is a future mechanism layer
and does not change the current Letter's observational claim ceiling.

## Formal direct empirical recurrence and mechanistic context

The standardized joint network statistic remains **k = 2**. No literature study is
added to that standardized-network replication count.

Case et al. (2026; DOI 10.1111/1365-2435.70415) provide a third independent
multispecies Hawaiian bird–lobelioid dataset with a published direction concordant
with the routing prediction. The deposited interaction schema spans 11 plant and
7 bird species. Because the direction was already public and this is another Aves
dataset, it is directional corroboration rather than a standardized or third-fauna
confirmatory contribution.

~~~text
PUBLISHED_DIRECTIONAL_MULTISPECIES_DATASET_RECURRENCE = 3
PRIMARY_STANDARDIZED_NETWORK_K = 2
CASE_STANDARDIZED_EFFECT = NOT_COMPUTED
CASE_CONFIRMATORY_THIRD_FAUNA = NO
~~~

The outcome-blind OpenAlex Q1–Q8 frame is now **complete and open for finite-frame
directional summary**:

~~~text
FORMAL_BIBLIOGRAPHIC_FRAME_RECORDS = 857
ELIGIBLE_DIRECT_STUDY_PROGRAMS = 33
POSITIVE = 22
NULL = 5
OPPOSITE = 4
MIXED = 2
DUPLICATE_BIBLIOGRAPHIC_RECORDS = 6
INELIGIBLE_BIBLIOGRAPHIC_RECORDS = 818
PENDING_FULLTEXT = 0
NETWORK_K_CONTRIBUTION = 0
PRIMARY_STANDARDIZED_NETWORK_K = 2
~~~

Of the 33 eligible programs, **23 are pre-existing direct-corpus programs recovered
inside OpenAlex** and **10 are newly eligible programs recovered by the formal
frame**. The 10 newly eligible programs comprise **7 positive and 3 opposite**
directions. Thus opposite cases occur in **1/23 (4.3%)** of the pre-existing
programs recovered inside the frame versus **3/10 (30%)** of newly recovered
programs. This contrast is descriptive only; it is not a test of publication or
search bias. One pre-existing program
(`Urcelay_Morales_Chalcoff_2006`) was independently verified as absent from
OpenAlex and is reported outside the formal denominator rather than injected into
it.

The historical Leal et al. (2025) anchor remains outcome-independent: its 56
distinct `study` labels were screened against the same geometry contract, with
four direct eligible programs. Those historical programs are already contained in
the formal eligible set and are not double counted.

The finite-frame result is descriptive. It is **not** a natural-prevalence estimate,
sign test, pooled meta-analytic effect, or additional standardized-network
replication count. Its role is stronger and narrower: the access-geometry →
nectar-robbery relation formally recurs beyond the two standardized networks while
retaining null, mixed and opposite systems as mechanism boundary conditions.

The complete formal artifacts are:

- `empirical/floral_defence_selectivity/formal_bibliographic_frame_v2/DIRECT_ACCESS_GEOMETRY_ELIGIBILITY_DECISIONS_V23.csv`
- `empirical/floral_defence_selectivity/formal_bibliographic_frame_v2/DIRECT_ACCESS_GEOMETRY_FULLTEXT_COMPLETE_RECEIPT_V1.json`
- `empirical/floral_defence_selectivity/formal_bibliographic_frame_v2/DIRECT_ACCESS_GEOMETRY_FORMAL_RECURRENCE_SUMMARY_V1.json`
- `empirical/floral_defence_selectivity/formal_bibliographic_frame_v2/DIRECT_ACCESS_GEOMETRY_BOUNDARY_MECHANISM_AUDIT_V1.csv`
- `empirical/floral_defence_selectivity/formal_bibliographic_frame_v2/DIRECT_ACCESS_GEOMETRY_BOUNDARY_MECHANISM_SUMMARY_V1.json`

The floral-defence corpus and effective-access / exposure framework remain
mechanistic context for why route switching is biologically plausible. Matched
effective-domain coding is still author-derived and has not undergone outcome-blind
independent recoding, so the 11-system state alignment is not treated as independent
validation.

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
ACCESS_ROUTING_ARCHIVE = V4_FULL_CURRENT_RESULT_REPRODUCTION_READY
ARCHIVE_ONLY_POOLED_PARTICIPATION = PASS
ARCHIVE_ONLY_ROUTE_SPECIFIC_POSTOPEN = PASS
ARCHIVE_ONLY_THRESHOLD_FIRST_OPEN = PASS
ARCHIVE_ONLY_THRESHOLD_BOUNDARY_AUDIT = PASS_585_OF_999_UPPER_BOUNDARY
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

The archive contract is now V4 and covers the **current manuscript rather than only the earlier frozen spine**. In addition to the exact 57-species Sakhalkar table and 2,265-row Aubert/EPHI pair-site table, the anonymous participation-opportunity table carries pooled, robbing and legitimate/non-robbing counts. The package workflow reconstructs the pooled participation estimate, the post-open route-specific RRs (legitimate/non-robbing 1.883; robbery-only 0.463), the preregistered threshold result and the post-open 585/999 upper-boundary bootstrap mass using archived tables and archived code only, then checks them against frozen/retained receipts. Source taxon names are not required. The remaining data sequence is therefore external only: reserve the Zenodo DOI, insert it into the submission files, freeze that DOI-bearing commit, build the exact final ZIP from that commit, upload it to the same draft, and publish the DOI record.

## Journal route

```text
1. Ecology Letters — Letter
   route only on the network-scale filtering-versus-routing distinction;
   do not pitch first mismatch→robbery, first tactic switching, or first route-cost theory
2. Functional Ecology — Research Article fallback
   strongest mechanism/trait fit if Ecology Letters judges k=2 reanalysis insufficiently broad
3. Oikos — Research fallback
4. extended Synthesis retained for later use
```

```text
STATUS = SCIENTIFIC_PACKAGE_REBUILT_AROUND_SPECIES_LEVEL_ROBUST_INFERENCE
ACTIVE_PAPER = ACCESS_ROUTING_LETTER
ROUTING_MECHANISM = RELATIVE_ROUTE_COST
ROUTE_COST_PRIOR_THEORY = ACKNOWLEDGED_NOT_CLAIMED_AS_NOVEL
NOVELTY_CORE = ROBUST_ROUTING_VS_FUNCTIONAL_REACH_DEPENDENT_FILTERING
ROUTE_COST_BOUNDARY = dC_LEGITIMATE_MINUS_dC_BYPASS
DIRECT_ACCESS_GEOMETRY_BOUNDED_CORPUS_PROGRAMS = 24
FORMAL_DIRECT_ACCESS_GEOMETRY_PROGRAMS = 33
BOUNDED_CORPUS_DIRECTIONS = 16_POSITIVE_5_NULL_1_OPPOSITE_2_MIXED
FORMAL_FRAME_DIRECTIONS = 22_POSITIVE_5_NULL_4_OPPOSITE_2_MIXED
FORMAL_HISTORICAL_FRAME = LEAL2025_56_STUDY_FIELD_LABELS
FORMAL_HISTORICAL_SOURCE_PROGRAMS = RESOLVED
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
BIBLIOGRAPHIC_FULLTEXT_DECISION_TEMPLATE = IMPLEMENTED_KNOWN_PREFILL_UNKNOWN_PENDING
BIBLIOGRAPHIC_FULLTEXT_DECISION_GATE = IMPLEMENTED_REQUIRE_COMPLETE_FAIL_CLOSED
FORMAL_RECURRENCE_SUMMARY_GATE = IMPLEMENTED_FINITE_FRAME_DIRECTION_COUNTS
FORMAL_RECURRENCE_PVALUE = NOT_COMPUTED_BY_V1
FORMAL_RECURRENCE_POOLED_EFFECT = NOT_COMPUTED_BY_V1
FORMAL_BIBLIOGRAPHIC_FRAME = COMPLETE_OPENALEX_857_RECORDS
FORMAL_RECURRENCE_RESULT = COMPLETE_33_ELIGIBLE_PROGRAMS
EXTENDED_SYNTHESIS = PRESERVED_RESERVE
LEGACY_IDENTIFICATION_PAPER = PRESERVED_SUPPORT
DATA_CODE_ARCHIVE = V5_REACH_SENSITIVITY_INTEGRATION_IN_PROGRESS
ARCHIVE_SCHEMA = BITA_ACCESS_ROUTING_LETTER_ARCHIVE_V5
POSTOPEN_DIAGNOSTIC_PROVENANCE = RECEIPT_AND_HASHES_RECORDED
DOI_APPLICATION_GATE = IMPLEMENTED_RECEIPT_RENDER_ARCHIVE_CHECKS
AUTHOR_METADATA = MACHINE_READABLE_CONTRACT_READY_VALUES_REQUIRED
NEXT_EXTERNAL_ACTION = CREATE_ZENODO_DRAFT_AND_RESERVE_DOI
EXTERNAL_SUBMISSION = BLOCKED_PENDING_RESERVED_DOI_FINAL_ARCHIVE_AND_AUTHOR_CONTROLLED_VALUES
```
