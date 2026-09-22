# Third independent access-routing network preregistration v1

## Status

~~~text
FREEZE_STATUS = PRE_OUTCOME_CONFIRMATORY
TARGET = THIRD_INDEPENDENT_VISITOR_NETWORK
TARGET_FAUNA = NON_INSECTA_NON_AVES
PRIMARY_GOAL = LIFT_CURRENT_K2_GENERALITY_CEILING
OUTCOME_DIRECTION_MUST_NOT_BE_USED_FOR_DATASET_SELECTION
~~~

This document freezes the third-network estimand and eligibility rules before
inspection of any new candidate's route-outcome values.

The existing two-network result remains unchanged:

> **greater constraint on the legitimate floral access route -> greater bypass / robbing propensity**

The third network must test the same directional construct on an independently
sampled visitor fauna.

## 1. Independence gate

A confirmatory third network must satisfy all of the following:

1. visitor fauna is outside **Insecta** and **Aves**;
2. data come from a field project independent of both Sakhalkar et al. (2023)
   and Aubert/EPHI;
3. raw or minimally processed public data are available before analysis;
4. visitor identity and plant identity are both retained at the level needed to
   construct the inferential unit;
5. route outcome is recorded independently of the access-trait construction.

Subsets of Sakhalkar or EPHI are not independent third networks.

## 2. Frozen inferential unit

Preferred unit:

~~~text
visitor species x plant species x site/context stratum
~~~

A single-site dataset may use visitor species x plant species if all other gates
pass.

Repeated visits are aggregated before inference. Individual visits are not
treated as independent replicates.

## 3. Frozen access-constraint variable

The third network must permit a **pre-outcome, monotone access-constraint score**
M in which larger values mean greater difficulty using the legitimate route.

Preferred construction, when positive commensurate reach/depth traits exist:

~~~text
M_ij = log(P_j / V_i)
~~~

where:

- P_j = plant legitimate-route depth / access distance;
- V_i = visitor reach phenotype measured in the same physical dimension.

Examples of admissible visitor reach phenotypes include tongue, rostrum, snout,
or another directly relevant pre-existing access trait. Body size alone is not
accepted as a substitute unless the source study explicitly establishes it as
the mechanical access phenotype before route outcomes are inspected.

If the public dataset uses another source-defined mechanical mismatch score, its
formula must be frozen in a protocol amendment **before** route-outcome values
are inspected.

Outcome-derived categories, robber identity, or observed route choice may not be
used to construct M.

## 4. Frozen bypass outcome

For each inferential unit:

~~~text
Y = B / (B + L)
~~~

where:

- B = bypass / nectar-robbing / nectar-theft interactions that avoid the
  legitimate access route;
- L = legitimate access interactions.

The source coding must distinguish bypass from legitimate use at event or
aggregated-count level.

If a source distinguishes primary robbery, secondary robbery and theft, all
predeclared non-legitimate access categories are combined into B, unless a
protocol amendment specifying a narrower definition is committed before outcome
inspection.

## 5. Primary third-network effect

Primary effect:

> rank association between access constraint M and bypass propensity Y.

If one sampling stratum:

~~~text
r_T = Spearman(M, Y)
~~~

If multiple sites/context strata:

1. rank M and Y globally;
2. remove stratum-specific rank means from both variables;
3. calculate Pearson correlation of the centered ranks.

This matches the site-adjusted Aubert/EPHI construction.

The expected direction is:

~~~text
r_T > 0
~~~

Primary test is two-sided; the direction is interpreted only after the frozen
test is computed.

## 6. Permutation null

If one stratum:

- shuffle Y across inferential units.

If multiple strata:

- shuffle Y within strata only;
- re-center ranks within strata;
- recompute r_T.

Primary permutation count:

~~~text
9,999
~~~

A fixed seed must be recorded before the first confirmatory run.

## 7. Minimum data gate

The confirmatory third network must have, after trait matching:

- at least **30** inferential units;
- at least **5 visitor species**;
- at least **5 plant species**;
- non-zero variation in M;
- at least one legitimate and one bypass interaction in the analysis dataset.

These are eligibility gates, not post-hoc power filters. A dataset failing a gate
is ineligible even if its visible outcome is strongly supportive.

## 8. Frozen k=3 synthesis

If an eligible third network is identified, it contributes one standardized
rank effect r_T.

The existing effects remain frozen:

~~~text
r_S = Sakhalkar insect network
r_A = Aubert/EPHI bird network
~~~

Primary three-network statistic:

~~~text
r_J3 = tanh(
  (atanh(r_S) + atanh(r_A) + atanh(r_T)) / 3
)
~~~

Each network has equal weight.

The joint null independently applies the frozen network-specific permutation
scheme within all three networks and recomputes r_J3 on every iteration.

No raw observations are pooled.

## 9. Claim rule after the third test

If a third independent network passes the eligibility gate and is analysed under
this preregistration, the current statement

~~~text
generality beyond two network systems remains untested
~~~

may be replaced only by:

> the same standardized access-routing association has now been tested in three
> independently sampled visitor networks spanning three major visitor faunas.

Even at k=3, do not claim a population-level mean across all ecological networks,
universal causality, or estimated between-network heterogeneity.

## 10. Outcome-blind search rule

Candidate discovery may inspect only:

- title / abstract for broad system identity;
- repository metadata;
- file names;
- README / variable dictionary;
- Methods needed to determine unit, trait, route-code and sampling structure.

Before eligibility is decided, do **not** inspect:

- Results sections;
- figures or tables reporting access-routing direction;
- route-outcome model coefficients;
- route-outcome p-values;
- candidate raw outcome values.

If a search snippet or prior reading exposes the relevant direction, that
candidate is permanently labelled:

~~~text
DISCOVERY_EXPOSED_NOT_CONFIRMATORY
~~~

and cannot be used as the confirmatory third network.

## 11. Search stopping rule

Search continues until the first candidate that passes all frozen gates is
identified from metadata/schema alone.

At that point:

1. record source DOI / repository version;
2. record file hashes if retrievable;
3. freeze any source-specific field mapping;
4. stop searching for a more favorable dataset;
5. run the confirmatory analysis once.

If no eligible public dataset is found after a bounded search across Dryad,
Zenodo, OSF, Figshare and article-linked public repositories, record:

~~~text
PUBLIC_THIRD_NETWORK = NOT_AVAILABLE
~~~

rather than relaxing the estimand.

## 12. Discovery-exposed systems

The systems listed in
`THIRD_NETWORK_CANDIDATE_REGISTRY_V1.csv` that are marked
`DISCOVERY_EXPOSED_NOT_CONFIRMATORY` were encountered before this freeze or
had direction-revealing search snippets. They may be used as biological context
or future sensitivity analyses only.

## Reproducibility target

Implemented before real confirmatory data:

- `scripts/analyze_third_access_routing_network.py`;
- `scripts/analyze_joint_access_routing_k3.py`;
- `scripts/evaluate_third_network_route_reliability.py`;
- `scripts/freeze_third_network_confirmatory_inputs.py`;
- `scripts/build_third_access_routing_units.py`;
- `scripts/load_frozen_access_routing_archive.py`;
- `scripts/run_third_network_confirmatory_pipeline.py`;
- `scripts/verify_third_network_confirmatory_bundle.py`;
- `scripts/plan_third_network_claim_transition.py`;
- SHA256-bound confirmatory input and output receipts;
- synthetic positive / null / opposite end-to-end validation.

The production runner first validates the exact frozen Letter analysis archive
for the two existing networks against the committed k=2 receipt, then creates
the dedicated third-network and k=3 result JSONs plus
`confirmatory_analysis_receipt.json` in one transactional non-overwriting run.
No live redownload of the existing two networks is permitted in production.

Manuscript claim update remains separate and may occur only after a real
confirmatory bundle passes independent SHA256/source-input verification and the
frozen claim-transition planner has produced a reporting contract.
