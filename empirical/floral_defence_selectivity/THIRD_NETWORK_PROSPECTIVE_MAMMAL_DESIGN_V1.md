# Prospective third access-routing network — Cape small-mammal–Protea design v1

## Status

~~~text
DESIGN_STATUS = PRE_DATA_FROZEN_DRAFT
FAUNA = NON_FLYING_MAMMALIA
SYSTEM = CAPE_SMALL_MAMMAL_X_PROTEA
PARENT_PREREG = THIRD_ACCESS_ROUTING_NETWORK_PREREG_V1
PUBLIC_DATA_ROUTE = CLOSED_NO_ELIGIBLE_DATASET
PRIMARY_ESTIMAND = UNCHANGED
~~~

This design operationalizes the frozen third-network access-routing estimand for
a prospective non-flying mammal network. It does not change the eligibility,
analysis, or k=3 rules frozen before the public-data search.

## 1. Why this system

Existing Cape Protea studies establish feasibility of the required network
breadth and observation method without supplying a confirmatory dataset under
the frozen gate.

Published remote-camera studies have documented:

- multiple small-mammal species visiting the same Protea community;
- three co-occurring Protea species visited by eight small-mammal species;
- three to six small-mammal visitor species per Protea in a separate four-species
  camera study;
- video footage that can recover visitor identity, visit duration, reproductive
  contact, and other foraging behavior.

These facts support feasibility only. They are not third-network outcome data.

Key method precedents:

- Zoeller et al. 2016, Australian Journal of Botany,
  DOI 10.1071/BT15111;
- Kühn et al. 2017, South African Journal of Botany,
  DOI 10.1016/j.sajb.2017.08.020;
- Biccard & Midgley 2009, South African Journal of Botany,
  DOI 10.1016/j.sajb.2009.08.003;
- Melidonis & Peter 2015, South African Journal of Botany,
  DOI 10.1016/j.sajb.2014.12.009.

## 2. Prospective target

The field project should sample a **single coordinated Cape Floristic Region
programme** containing at least:

~~~text
target plant species      >= 7
target mammal species     >= 6
target realized units     >= 70 visitor x plant x site units
frozen minimum units      >= 30
frozen minimum plants     >= 5
frozen minimum visitors   >= 5
~~~

The >=70 target is a precision target, not a new eligibility threshold. A simple
Fisher-z approximation indicates that roughly 62 independent units are needed
for about 80% power to detect a correlation near the existing cross-network
effect (~0.35) with a two-sided alpha of 0.05. Clustering and heterogeneous visit
counts make that only a planning approximation; the preregistered minimum gate
remains 30 units.

Candidate Protea pool for site planning, subject to permits and actual
co-occurrence:

~~~text
P. canaliculata
P. sulphurea
P. humiflora
P. cordata
P. decurrens
P. scabra
P. subulifolia
P. nana
P. foliosa
~~~

The confirmatory plant list must be frozen **before confirmatory camera data are
opened**. Species are included for ecological feasibility, not because their
route outcomes are known to support the prediction.

## 3. Two-stage design

### Stage A — eligibility pilot, excluded from inference

Purpose:

- verify camera placement and species identification;
- verify that L/B/A/N route categories can be distinguished from image geometry
  without viewing morphology values;
- confirm from independent presurvey / trapping records that >=5 mammal species
  and >=5 plant species can plausibly be sampled;
- estimate route-blind mammal detection rates and camera uptime needed for the
  frozen design without using L/B outcomes or access morphology.

Pilot restrictions:

- pilot events are never included in the confirmatory analysis;
- access mismatch M is not calculated against pilot route outcomes;
- no M–Y correlation is computed;
- no site, plant species or mammal species is retained or dropped because B or L
  was or was not observed in pilot footage;
- pilot route frequencies are not used to choose camera effort.

Site and plant inclusion are frozen from **pre-route ecological and logistical
criteria only**: independent richness records, flowering availability, permits,
accessibility and camera operability. Pilot video may train/validate the coding
manual, but route-class presence or absence cannot determine confirmatory site
selection.

If the final confirmatory dataset contains no B or no L events, the frozen
eligibility gate fails and the system remains ineligible; the project does not
replace sites post hoc to manufacture route variation.

### Stage B — confirmatory collection

Confirmatory cameras start only after:

1. site/plant list is frozen;
2. morphology protocol is frozen;
3. route-coding manual is frozen;
4. the route-blind camera-effort planner has identified a uniform effort with
   >=0.80 planning probability of reaching the 70-unit target;
5. planner SHA256, uniform hours, qualifying fraction, target probability and
   route-blind plant x site deployment-set digest are frozen;
6. analysis seed is frozen.

## 4. Inferential unit

Frozen unit:

~~~text
mammal species x Protea species x site
~~~

Repeated clips/events are aggregated within this unit.

Individual videos are observations used to estimate B and L; they are not
treated as independent inferential replicates.

## 5. Plant access phenotype

Primary plant trait:

~~~text
P_j = legitimate nectar-access depth in mm
~~~

Operational definition:

> the straight-line distance a mammal's feeding apparatus must penetrate from
> the nearest non-destructive entrance plane of an open inflorescence to the
> nectar-access point while following the legitimate route.

Measurement:

- >=10 freshly open inflorescences per plant species per site where possible;
- digital calipers, mm;
- two repeated measurements per inflorescence;
- species x site median is the primary P_j;
- observer records P_j without access to route-outcome data.

Secondary morphology may be recorded for later sensitivity analyses but cannot
replace P_j after outcome inspection:

- entrance width;
- pollen-presenter-to-nectar distance;
- inflorescence diameter;
- flower-head height above ground.

## 6. Mammal access phenotype

Primary visitor trait:

~~~text
V_i = functional rostral reach in mm
~~~

Preferred implementation:

- live-trapped or independently available morphometric specimens from the same
  regional mammal assemblage;
- predeclared linear snout/rostrum measure directly related to penetration reach;
- >=5 individuals per species where possible;
- two repeated measurements per individual;
- species median is the primary V_i.

The exact anatomical landmarks must be frozen before confirmatory route data are
decoded.

If a direct functional reach assay is feasible under animal-care permits, it may
replace external rostrum length only through a protocol amendment committed
**before confirmatory route outcomes are opened**.

Body mass is not an admissible substitute for V_i.

## 7. Frozen access mismatch

For every visitor x plant x site unit:

~~~text
M_ij = log(P_j / V_i)
~~~

Larger M means the legitimate nectar route is more mechanically demanding for
the visitor.

M is computed by the morphology pipeline. Route coders do not receive M, P_j,
or V_i values.

## 8. Camera observation protocol

Use near-focus, no-glow infrared video units following the established
small-mammal Protea remote-camera approach.

Minimum operational specification:

- video, not still-only triggering;
- >=30 s clip per trigger; 60 s preferred;
- retrigger interval <=10 s where hardware permits;
- timestamp synchronized across cameras;
- frame contains the full inflorescence and the likely access sides;
- two camera angles for a subset used to validate route classification;
- camera position recorded before opening route data.

Sampling effort should be balanced prospectively by plant x site rather than
extended after seeing species-specific route outcomes.

### Route-blind camera-effort freeze

Use:

- `empirical/floral_defence_selectivity/THIRD_NETWORK_CAMERA_EFFORT_RATE_SCHEMA_V1.csv`;
- `scripts/plan_third_network_camera_effort.py`;
- `scripts/extract_third_network_camera_effort_freeze.py`.

The planner accepts only site, plant, mammal and route-blind mammal detection
rate. It cannot ingest L/B route outcomes, (M), plant access depth or mammal
reach.

For every retained plant x site, the selected effort is uniform. A predeclared
`qualifying_fraction` converts route-blind detections into a planning
approximation for classifiable feeding events. This parameter is a sensitivity
assumption and is never estimated from confirmatory route direction.

The camera rule can be frozen only when:

~~~text
planner status = PLANNING_TARGET_EFFORT_IDENTIFIED
target success probability >= 0.80
achieved planning-target probability >= target
~~~

The freeze receipt stores the exact planner SHA256, selected hours,
`qualifying_fraction`, success probabilities, effort-rule version, number of
plant x site deployments and SHA256 of the route-blind deployment key set.

At confirmatory input freeze, the actual PRIMARY camera table must reproduce the
same plant x site key-set digest and the same uniform camera-hours. Any mismatch
blocks the analysis rather than being repaired after route outcomes are known.

## 9. Frozen route coding

Every nectar-directed mammal event receives one of:

~~~text
L = LEGITIMATE
B = BYPASS
A = AMBIGUOUS
N = NON_NECTAR / NOT A FEEDING EVENT
~~~

### LEGITIMATE

Code L when all are visible:

1. the mammal uses the natural open access path;
2. the snout/head enters the inflorescence through that path;
3. nectar-directed feeding is visible or strongly supported by repeated licking/
   probing;
4. the approach follows the reproductive-contact pathway.

### BYPASS

Code B when all are visible:

1. the mammal obtains or attempts to obtain nectar;
2. access is lateral, destructive, or otherwise avoids the normal open pathway;
3. chewing, tearing, displacement, or side-access creates/uses an alternative
   route;
4. the event bypasses the normal reproductive-contact pathway.

Destructive tissue feeding without evidence of nectar-directed access is N, not
B.

### AMBIGUOUS

Code A whenever the access path or nectar-directed intent cannot be determined.
A events are excluded from B/(B+L), not forced into either route.

## 10. Outcome-blind coding architecture

To preserve the prospective test:

### Morphology team

May see:

- plant identity;
- mammal identity;
- morphology specimens.

May not see:

- L/B route counts;
- unit-level Y.

### Video route-coding team

May see:

- video;
- visitor identity if needed for species coding;
- plant identity if unavoidable for event bookkeeping.

May not see:

- P_j;
- V_i;
- M_ij;
- any M–Y visualization or model output.

### Integration step

Morphology and route tables are joined only after both are checksum-frozen.

## 11. Inter-rater reliability

Before confirmatory analysis:

- >=20% of confirmatory feeding events are independently double-coded;
- report raw agreement and Cohen's kappa for L/B/A/N;
- target kappa >=0.80.

If kappa <0.80:

1. adjudicate the coding manual using only disagreements;
2. freeze the revised manual;
3. recode the full confirmatory set blind to morphology;
4. do not inspect M–Y association during adjudication.

## 12. Outcome construction

For each mammal x plant x site unit:

~~~text
B = number of BYPASS events
L = number of LEGITIMATE events
Y = B / (B + L)
~~~

Eligibility requires B+L > 0 for a unit.

The network as a whole must contain at least one B and at least one L event.

No pseudocount is added to Y.

## 13. Primary third-network analysis

If multiple sites are retained:

1. rank M globally;
2. rank Y globally;
3. subtract site-specific mean rank from both;
4. compute Pearson correlation of centered ranks.

Call this effect:

~~~text
r_T
~~~

Permutation null:

- shuffle Y ranks within site;
- re-center within site;
- recompute r_T;
- 9,999 permutations;
- two-sided p-value.

The permutation seed is frozen before the first analysis run.

## 14. Confirmatory inclusion gate

Before the analysis script returns r_T, assert:

~~~text
n_units >= 30
n_mammal_species >= 5
n_plant_species >= 5
variation(M) > 0
total_B > 0
total_L > 0
~~~

Planning target:

~~~text
n_units >= 70
~~~

Failure of a frozen gate returns INELIGIBLE_CONFIRMATORY_DATASET. It does not
trigger a looser alternative analysis.

## 15. k=3 integration

Only after the third network passes all gates:

~~~text
r_J3 = tanh(
  (atanh(r_S) + atanh(r_A) + atanh(r_T)) / 3
)
~~~

Use equal network weights and the three frozen network-specific permutation
schemes.

No raw observation pooling.

## 16. Claim ceiling

A successful test licenses only:

> the same standardized access-routing association has been tested in three
> independently sampled visitor networks spanning insects, birds, and
> non-flying mammals.

It still does not license:

- universal causality;
- a network-population mean;
- estimated between-network heterogeneity;
- the claim that one mammal trait alone causes route choice;
- a claim that all non-flying-mammal pollination systems behave similarly.

## 17. Failure is informative

If the prospective mammal network passes the sampling gates but r_T is
zero-compatible or opposite in sign, that result remains the confirmatory third
network. The project must not replace it with another mammal dataset to restore
concordance.

Absence of B during the **excluded pilot** is not a site-selection rule. The
confirmatory site/plant set is determined independently of pilot route outcomes.
If the completed confirmatory dataset contains no B or no L events, the frozen
eligibility gate fails and no k=3 claim is made.

## 18. Frozen implementation assets before field analysis

Already frozen:

- `empirical/floral_defence_selectivity/THIRD_NETWORK_PROSPECTIVE_SCHEMA_V1.csv`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_EVENT_SCHEMA_V1.csv`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_ROUTE_CODING_MANUAL_V1.md`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_PILOT_SPLIT_CONTRACT_V1.md`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_SEED_RECEIPT_V1.json`
- `scripts/build_third_access_routing_units.py`
- `scripts/analyze_third_access_routing_network.py`
- `scripts/analyze_joint_access_routing_k3.py`
- `empirical/floral_defence_selectivity/THIRD_NETWORK_CAMERA_DEPLOYMENT_SCHEMA_V1.csv`\n- `scripts/freeze_third_network_confirmatory_inputs.py`\n- `empirical/floral_defence_selectivity/THIRD_NETWORK_INPUT_FREEZE_GATE_V1.md`\n
Still field-specific and therefore not yet fillable:

- source / permit / site receipt;
- exact confirmatory camera deployment receipt;
- completed checksum manifest generated from actual confirmatory morphology,
  route and camera-deployment tables;
- exact-reproduction workflow using the eventual confirmatory data.
