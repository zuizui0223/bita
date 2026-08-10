# Pre-registered extraction protocol: mutualist-interference pathway (v1)

This protocol is fixed before any numerical effect is extracted. Its purpose is to make the
quantitative layer falsifiable: the strata, the moderators, the capacity thresholds, and the
directional expectations are declared in machine-readable files that the analysis code reads,
so a later result cannot be produced by choosing the analysis after seeing the data.

Theory context, the bridge assumption, and the inference boundary are in
`docs/IOTA_PATHWAY_EMPIRICAL_TARGET.md`. This document covers only how records are found,
screened, extracted, coded, and analysed.

## 1. Target stratum

```text
stratum_id     BP_chemical_pollinator_use_lrr_manipulation
route          B_to_pollination
trait_class    chemical_barrier
outcome_class  pollinator_preference_or_foraging
design_class   manipulation
effect_metric  log_response_ratio
expected sign  negative
part_i term    c_D
```

Declared in `empirical/broad_reality_evidence/broad_meta_analysis_strata.csv`. Physical-barrier
records are screened into `BP_physical_visitation_lrr_manipulation` and are analysed separately
if and only if that stratum independently reaches capacity. Trait classes are never merged to
manufacture capacity.

## 2. Inclusion criteria

A record enters the quantitative layer only when all of the following hold.

1. **Manipulation.** The flower-associated chemical barrier trait was experimentally set or
   contrasted between a treatment and a comparator. Observational covariation between trait and
   pollinator use is coded for the direction map only.
2. **Flower-specific.** The manipulated compound is presented in a floral context — nectar,
   pollen, corolla, or an artificial flower standing in for one. Leaf or whole-plant defence
   manipulations are excluded unless the study demonstrates the floral presentation itself.
3. **Antagonist-reduction role.** The manipulated trait has an operationally defined
   antagonist-reduction role in the focal biological context, either shown in the same study or
   cited to a source recorded in `extraction_note`. A compound is not admitted as `D` merely
   because it is a secondary metabolite.
4. **Legitimate visitor.** The response is measured on a legitimate pollinating visitor.
   Responses of nectar robbers, florivores, or non-pollinating consumers are recorded separately
   and never pooled into this stratum.
5. **Recoverable effect.** A treatment and comparator response with a dispersion measure and
   sample sizes, or a reported effect with its uncertainty, is available in the article, its
   supplement, or a deposited dataset. A locator is recorded for every extracted number.

## 3. Exclusion criteria

- Concentration not reported in any form that can be compared with a natural range.
- Response pooled over legitimate visitors and robbers with no separation.
- The same experiment reported again in a later paper (the earlier report is the cluster).
- Reviews, opinion pieces, and models without primary data.
- Records whose only source is an abstract. These remain in the direction map at their existing
  evidence level and are not promoted.

## 4. Orientation

Every effect is oriented as

```text
positive_is_more_declared_trait_more_declared_outcome
```

so that a *negative* value means more barrier trait, less legitimate pollinator use. Studies
reporting the reverse contrast are sign-flipped at extraction and the flip is recorded in
`extraction_note`.

## 5. Independence and the study cluster

The unit of independence is `study_cluster_id`: one experimental system, one field season or
one assay series, one research group. Two papers reporting the same manipulation on the same
population share a cluster.

The pooled layer takes one primary effect per cluster per stratum. The moderator layer takes
one effect per cluster **per categorical moderator level**, because the declared context
contrasts are frequently manipulated within a single study, and discarding them would discard
the very comparison the analysis exists to make. Dependence among effects from one cluster is
handled by cluster-robust (CR1) standard errors and by degrees of freedom set to the number of
independent clusters minus the number of model parameters, not by pretending the effects are
independent.

## 6. Moderator coding

Declared in `iota_moderator_registry.csv`; coded values go in `iota_moderator_coding.csv`,
one row per effect per moderator, with an explicit `coding_basis`.

**`dose_realism`** — `within_natural_range` when every manipulated concentration lies at or
below the maximum concentration reported for the focal species or its congeners in a cited
source; `above_natural_range` when any manipulated concentration exceeds it. The cited source
for the natural range is the `coding_basis`. When no natural range can be cited, the effect is
left `needs_coding` and is excluded from this analysis rather than guessed.

**`log_dose_multiple_of_natural_maximum`** — natural logarithm of (manipulated concentration ÷
maximum reported natural concentration), on the same units. Requires both numbers from cited
sources.

**`assay_context`** — `free_foraging_field`, `enclosure_or_flight_cage`, or
`paired_choice_laboratory`. Coded from the reported methods.

**`pollinator_functional_group`** — `social_bee`, `solitary_bee`, `bird`, `other`. When a study
reports several groups separately, each group is one effect; when it pools them, the pooled
effect is coded `other` and the pooling is noted.

Coding is single-coder until a second coder is available. Every row carries `coder_id` and
`coding_date`, and the `coding_status` field distinguishes `coded` from `needs_coding`, so the
evidence level of the moderator layer is never overstated.

## 7. Capacity thresholds

Fixed in advance and enforced by the code, not by judgement after the fact:

```text
pooled stratum        3 independent clusters   exploratory
                      5 independent clusters   stability eligible
categorical moderator 2 levels, 3 clusters per level, 6 clusters total
continuous moderator  4 distinct values, 8 clusters total
Egger asymmetry test  10 independent clusters
```

Below a threshold the analysis reports `insufficient_moderator_capacity` and no estimate. A
withheld analysis is a result: it says the published record cannot answer the question at the
declared resolution.

## 8. Analyses that will be run

Executed by `scripts/run_context_dependence.py` over the declared registry:

1. Random-effects pooling of the stratum (DerSimonian–Laird), already implemented in
   `scripts/run_broad_meta_analysis.py`.
2. Subgroup pooling per categorical moderator level with a `Q_between` test.
3. Random-effects meta-regression per declared moderator, with model-based and cluster-robust
   standard errors and Student-*t* inference on cluster-count degrees of freedom.
4. Leave-one-cluster-out influence on the pooled direction.
5. Weighted Egger regression for funnel asymmetry, withheld below 10 clusters.

The verdict vocabulary is fixed: `context_dependent_direction_reversal`,
`context_dependent_magnitude_only`, `no_detected_context_dependence`,
`omnibus_moderator_test_not_estimable`, `not_evaluated`.

## 9. Current status and the retrieval blocker

`broad_effect_extractions.csv` contains no eligible effect rows, so every analysis above
currently returns a withheld status. The reading queue in `iota_reading_queue.csv` lists the
candidate primary studies with `retrieval_status = not_retrieved`.

The blocker is environmental, not scientific. The session that assembled this protocol had no
outbound access to bibliographic or full-text services: Crossref, OpenAlex, Europe PMC, PubMed
Central, Dryad, and publisher domains were all refused by the network egress policy. Candidate
identifiers in the reading queue were therefore recorded from search results and are marked
`unverified_from_search_result` unless the DOI appears in the source URL itself or already
matches a committed direction record. **No numerical effect has been entered, and none may be
entered from a search snippet.** Every value must come from the article, its supplement, or a
deposited dataset, with a locator.

## 10. Completion criterion

The empirical half of the project's target is met when, for this stratum:

- at least five independent study clusters carry extracted, oriented, source-located effects;
- the pooled random-effects estimate and its heterogeneity are reported;
- at least one declared moderator reaches capacity and returns a verdict, whichever verdict it is;
- leave-one-cluster-out shows whether the pooled direction depends on a single cluster.

Reaching capacity is not required for the project to be reportable. If the published record
cannot supply five clusters with recoverable uncertainty, the correct output is the withheld
statuses plus this protocol, which together specify exactly what the literature is missing.
