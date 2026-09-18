# BITA floral-defence selectivity macro-analysis — design

Date: 2026-09-18  
Status: design approved in chat; implementation not started  
Branch: `design/bita-floral-defence-selectivity-macro`

## 1. Scientific goal

Refocus BITA from an identification-warning paper into a macro-ecological evidence-synthesis paper that asks:

> **When does a flower-associated defence suppress antagonists while preserving pollination?**

The paper should deliver a substantive ecological result about the conditions governing defence selectivity across floral systems.

The identification framework remains useful as a claim-discipline layer, but it is no longer the headline result.

## 2. Core ecological hypothesis

The leading mechanism is **effective-domain separation**.

For one flower-associated antagonist-reducing trait (D):

- if the antagonist encounters (D) but the legitimate pollinator does not, or is less susceptible to it, defence should reduce antagonist use while preserving pollination;
- if antagonist and pollinator experience the same effective domain, defence should more often carry a pollinator cost;
- if the antagonist bypasses or tolerates the effective domain, the focal defence route should fail or weaken.

“Effective domain” may be separated by:

- consumer susceptibility;
- dose / exposure threshold;
- cumulative exposure;
- attack route;
- spatial geometry;
- developmental time;
- visitor functional mode;
- response stage.

The primary ecological alternative is that selectivity is explained more simply by broad defence class, especially chemical versus physical defence.

## 3. Existing empirical assets

The repository already contains the main derivation assets:

- 18 independent `D -> antagonism` clusters;
- 10 independent `D -> pollination` clusters embedded in systems with antagonist evidence;
- matched quantitative anchors for `Catalpa speciosa`, `Pedicularis rex`, and `Thunia alba`;
- independent physical implementations in `Codonopsis` and `Chrysothemis`;
- overlap / interference examples such as `Bejaria`;
- dose or exposure transitions in `Polemonium`, `Aconitum`, `Asclepias`, and `Gelsemium`;
- bypass / failed-defence boundaries such as the `Salvia`-type cases;
- outcome-blind moderator coding already committed in `OUTCOME_BLIND_DOMAIN_MODERATOR_MATRIX_V1.csv`;
- a registered 2020–2026 hold-out validation protocol.

These assets are presently dispersed across mechanism-first audits. The implementation goal is to promote them into one systematic matched-defence dataset and one primary analysis.

## 4. Unit of analysis

The primary biological unit is a **matched defence contrast**:

```text
one independent study cluster
× one flower-associated D axis
× one declared ecological context
```

A row may contain several dependent response records, but those records do not create independent biological replication.

Required identifiers:

```text
study_cluster_id
publication_id
plant_taxon
D_axis_id
context_id
derivation_or_holdout
```

Repeated doses, consumers, years, populations, or outcomes remain nested within the same cluster unless the source design establishes independence.

## 5. Data contract

### 5.1 Architecture fields — coded before focal outcomes

```text
pre_outcome_domain_code
    = SEPARATED
    | OVERLAPPED
    | BYPASS_TOLERANCE
    | TRANSITIONAL
    | UNCLEAR

separating_coordinate
    = susceptibility
    | dose
    | cumulative_exposure
    | attack_route
    | geometry
    | space
    | time
    | functional_mode
    | response_stage
    | other_declared

defence_modality
    = chemical
    | physical
    | reward_access
    | mixed
    | other

antagonist_guild
pollinator_guild
experimental_manipulation
observational_or_experimental
source_verification_state
```

Outcome information must not be used to back-fill the architecture code.

### 5.2 State-coding discipline

State labels must not be created by a simple `P < 0.05` rule.

For every outcome, preserve three separate pieces of information when available:

```text
estimated_direction
uncertainty_class
source_inference
```

Use:

```text
uncertainty_class
    = DIRECTION_SUPPORTED
    | NULL_COMPATIBLE
    | EQUIVALENCE_SUPPORTED
    | DIRECTION_ONLY
    | UNRESOLVED
```

A failure to reject zero is not coded as proof of biological preservation. `PRESERVED_OR_IMPROVED` requires a positive/preserved functional result, an explicit equivalence/non-inferiority basis, or a source-supported biological comparison strong enough to justify that label. Otherwise use `NO_DETECTED_CHANGE` or `UNRESOLVED` and carry that distinction into sensitivity analyses.

### 5.3 Outcome fields

For the antagonist side:

```text
antagonist_outcome_type
antagonist_effect_direction
antagonist_effect_metric
antagonist_effect_value
antagonist_effect_se
antagonist_effect_ci_low
antagonist_effect_ci_high
antagonist_effect_numeric_eligible
```

For the pollinator side:

```text
pollinator_outcome_type
pollinator_response_stage
pollinator_effect_direction
pollinator_effect_metric
pollinator_effect_value
pollinator_effect_se
pollinator_effect_ci_low
pollinator_effect_ci_high
pollinator_effect_numeric_eligible
```

All directions are oriented so that the biological meaning is explicit rather than hidden in coefficient coding.

### 5.4 Derived state fields

Derived only after the architecture code is frozen:

```text
defence_efficacy_state
    = EFFECTIVE
    | NULL_OR_WEAK
    | MIXED
    | UNRESOLVED

pollinator_cost_state
    = PRESERVED_OR_IMPROVED
    | IMPAIRED
    | NO_DETECTED_CHANGE
    | MIXED
    | UNRESOLVED

selectivity_state
    = GUARDED_SELECTIVE
    | BROAD_INTERFERENCE
    | BYPASS_FAILURE
    | TRANSITION
    | UNRESOLVED
```

## 6. Primary analysis: two-stage ecological model

A single synthetic selectivity effect is **not** the primary estimand because antagonist and pollinator outcomes often differ in scale, sampling unit, and biological construct.

The macro-analysis is therefore split into two ecological gates.

### Stage 1 — Does the defence actually affect antagonists?

Response:

```text
Y_H = 1 if antagonist route is EFFECTIVE
      0 if NULL_OR_WEAK
```

Primary predictor:

```text
antagonist_domain_intersection
    = intersects
    | bypass_or_tolerance
```

Primary ecological test:

> Defence should fail more often when the antagonist bypasses or tolerates the effective domain.

Where sample size permits, fit a cluster-level hierarchical logistic model. If sparse cells remain, use exact / penalized logistic estimation and report the limitation rather than forcing asymptotics.

### Stage 2 — Conditional on an effective antagonist route, is pollination preserved?

Analysis universe: matched systems in which the focal D route is operationally effective against at least one antagonist channel.

Primary response for the strict analysis:

```text
Y_P = 1 if pollinator function is PRESERVED_OR_IMPROVED
      0 if IMPAIRED
```

`NO_DETECTED_CHANGE` is not silently merged with `PRESERVED_OR_IMPROVED`. It is handled in a predeclared sensitivity analysis and, where sample size permits, in a three-state ordinal/multinomial version of the model.

Primary predictor:

```text
domain_relation = SEPARATED vs OVERLAPPED
```

Competing predictors:

```text
defence_modality
pollinator_guild
antagonist_guild
observational_or_experimental
response_stage
```

Primary ecological test:

> Effective-domain separation predicts preserved pollination better than broad labels such as chemical versus physical defence.

The main model should compare:

```text
M0: intercept only
M1: defence_modality
M2: domain_relation
M3: domain_relation + defence_modality
```

Model comparison should use information criteria or leave-one-cluster-out predictive performance appropriate to the selected estimator. The paper must not claim a universal rule merely because one coefficient has the desired sign.

## 7. Quantitative sub-lanes

Compatible numeric effects are retained, but no grand mean is manufactured across incompatible response constructs.

A quantitative lane is eligible only when studies share:

1. biological route;
2. effect orientation;
3. effect metric or a defensible transformation;
4. comparable outcome construct;
5. sampling variance;
6. dependence handling.

Candidate lanes include:

- log response ratios for resource use / consumption;
- visitation or handling effects where metric compatibility is established;
- robbery / antagonist-use proportions;
- reproductive outcomes when the same construct is available across systems.

Within a compatible lane, fit a multilevel random-effects model and test whether `domain_relation × consumer_role` or equivalent matched contrasts explain heterogeneity.

The existing `Catalpa` and `Thunia` reconstructions are anchors, not independent substudies.

## 8. Hold-out validation

Derivation systems and hold-out systems remain explicitly separated.

The already registered 2020–2026 hold-out protocol is preserved.

Primary confirmatory reporting:

1. freeze architecture codes without focal outcome use;
2. reveal antagonist and pollinator outcomes;
3. score Stage-1 and Stage-2 predictions;
4. compare domain-based predictions with the fixed competing rules;
5. report derivation and hold-out performance separately;
6. only then fit an optional combined model with a `cohort = derivation | holdout` term.

Hold-out evidence must never be rewritten as if the domain rule was preregistered before its discovery.

## 9. Corpus construction and systematic expansion

The final paper must not rely only on the historically accumulated derivation examples.

Build a focused systematic matched-defence corpus whose search target is fixed **before** outcome screening:

> primary empirical studies in which one flower-associated defence/access trait or manipulation is evaluated against an antagonist response and a legitimate-pollinator or pollination-function response in the same biological system.

The search is narrow by design: do not reopen generic floral-trait literature harvesting, but do run a reproducible matched-D search to saturation.

### 9.1 Retrieval sources

Use reproducible public bibliographic sources where possible, plus backward/forward citation chasing from admitted seed studies. Record database, query, date, returned count, deduplicated count, and eligibility disposition.

The existing broad Crossref/OpenAlex-style harvest infrastructure may be reused, but the new matched-D query registry must be separate from the older broad route search.

### 9.2 Fixed concept families

Queries should combine:

```text
flower / floral / nectar
× defence / defense / secondary metabolite / barrier / sticky / slippery / hair / bract / calyx / access
× pollinator / pollination / visitation / pollen transfer
× herbivore / florivore / robber / thief / seed predator / oviposition / antagonist
```

Equivalent database syntax is allowed; biological concept families are frozen before outcome inspection.

### 9.3 Search saturation

Continue targeted expansion until:

1. all fixed query families have been exhausted at the declared retrieval depth;
2. backward and forward chasing of newly admitted systems yields no new eligible matched-D system in two consecutive expansion rounds;
3. unresolved candidate records have an explicit disposition.

This is literature-search saturation, not a claim of natural prevalence.

### 9.4 Priority order

1. recode the existing matched-D systems into the new contract;
2. recover any unextracted pollinator or antagonist side from already admitted D clusters;
3. execute the registered 2020–2026 hold-out search unchanged;
4. run the new focused all-years matched-D systematic search;
5. perform citation chasing;
6. extract quantitative effects only after biological eligibility is established.

Every new study must pass the same D-role gate. Defence-like chemistry or morphology is not admitted merely because its outcome is convenient.

## 10. Analysis thresholds

No arbitrary “significance” gate defines whether the project proceeds.

Instead:

- if fewer than 4 independent hold-out systems are architecture-classifiable, hold-out verdict = `INSUFFICIENT_HOLDOUT_CAPACITY`;
- if fewer than 15 independent matched systems are available for the primary Stage-2 model, report the main inference as a structured comparative synthesis plus exact / penalized contrasts, not a high-dimensional meta-regression;
- moderator models may add only predictors supported by the available independent cluster count;
- no interaction term is fitted solely because it is theoretically attractive.

## 11. Robustness and anti-circularity checks

Required sensitivity analyses:

- derivation systems only;
- hold-out systems only;
- combined with cohort term;
- experimental studies only;
- strict flower-specific D definition;
- chemical-only and physical-only subsets where informative;
- leave-one-cluster-out;
- collapse dependent outcomes within cluster;
- alternate coding of borderline `TRANSITIONAL` cases;
- exclude systems whose pollinator response is only a reproductive proxy rather than a direct pollination measure.

The architecture code and outcome code should be stored in separate source files so accidental leakage is detectable.

## 12. Main ecological conclusions the paper is allowed to make

If supported, the target conclusion is:

> **Floral defence selectivity is organized by ecological domain separation: defences are most likely to suppress antagonists while preserving pollination when antagonist and pollinator exposure, access, timing, or susceptibility are separated. Broad chemical-versus-physical classification alone is insufficient.**

A second supported result may be:

> Selectivity is not a fixed property of a defence trait; dose, cumulative exposure, response stage, or consumer identity can move the same system between guarded and interfering states.

If the data do not support the domain rule, the paper reports which competing predictor performs better. Failure of the favored hypothesis is a valid ecological result.

## 13. Claims explicitly removed from the main line

The refocused paper does not use these as its headline conclusions:

- `trait interaction != mechanism`;
- no existing study closes full channel allocation;
- residual-by-subtraction warnings;
- absence of a universal `W_AD` sign;
- prevalence of natural floral-defence states;
- historical evolution of trait differentiation.

These remain methodological boundaries or discussion material.

## 14. Manuscript architecture after the refocus

### Introduction

1. flowers face simultaneous mutualists and antagonists;
2. defence can be beneficial yet costly to pollination;
3. existing work lacks a general explanation for when defence is selective;
4. effective-domain separation yields a cross-system prediction;
5. test that prediction with matched floral-defence systems.

### Methods

1. systematic matched-system evidence construction;
2. outcome-blind architecture coding;
3. two-stage ecological model;
4. quantitative compatible-effect sub-lanes;
5. hold-out validation;
6. robustness and dependence handling.

### Results

1. corpus structure;
2. Stage-1 defence efficacy;
3. Stage-2 pollinator preservation;
4. comparison against defence modality;
5. quantitative sub-lanes;
6. hold-out performance;
7. state transitions / switching cases.

### Discussion

Lead with the ecological rule, not with an inference warning.

Identification material is reduced to the paragraph explaining why matched same-defence evidence and outcome-blind coding were required.

## 15. Implementation topology

Create a new focused module:

```text
empirical/floral_defence_selectivity/
    README.md
    DATA_CONTRACT.md
    matched_system_registry.csv
    architecture_codes.csv
    outcome_codes.csv
    quantitative_effects.csv
    holdout_registry.csv
    analysis/
    results/
```

Scripts:

```text
scripts/build_floral_defence_selectivity_dataset.py
scripts/run_floral_defence_selectivity_models.py
scripts/run_floral_defence_selectivity_sensitivity.py
```

Tests:

```text
tests/test_floral_defence_selectivity_data_contract.py
tests/test_floral_defence_selectivity_orientation.py
tests/test_floral_defence_selectivity_independence.py
tests/test_floral_defence_selectivity_no_outcome_leakage.py
tests/test_floral_defence_selectivity_models.py
```

The current mechanism-pattern files remain provenance inputs; do not delete or rewrite them during the first implementation pass.

## 16. First implementation milestone

Milestone 1 is complete when:

1. all currently admitted matched-D systems are represented in `matched_system_registry.csv`;
2. architecture and outcome coding are physically separated;
3. every row traces back to an existing source-adjudicated file;
4. current system counts are reproduced from the new registry;
5. Stage-1 and Stage-2 analysis-ready sample sizes are reported;
6. no manuscript claims are changed yet.

Only after Milestone 1 passes should the statistical model and manuscript refocus proceed.
