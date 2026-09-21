# Prospective third-network field execution gate v1

## Current state

~~~text
SCIENTIFIC_DESIGN = FROZEN
PUBLIC_THIRD_NETWORK = NOT_AVAILABLE
ACTIVE_K3_LANE = CAPE_SMALL_MAMMAL_X_PROTEA_PROSPECTIVE
ROUTE_BLIND_SITE_SELECTION = REQUIRED
PRE_VIDEO_FREEZE = REQUIRED
FIELD_EXECUTION = BLOCKED_PENDING_REAL_SITE_AND_AUTHORIZATION_RECEIPTS
K3_CLAIM = NOT_AVAILABLE
~~~

The third-network analysis, event coding, pilot exclusion, route-blind site
selection, seeds, and k=3 integration are already frozen. What remains is not
another statistical design step. It is execution readiness.

## Required chain

~~~text
route-blind presurvey
        |
        v
eligible site pool from flowering plants + mammal presence + camera operability
        |
        v
final site / plant list frozen without B/L information
        |
        v
pre-video confirmatory freeze receipt checksum-frozen
        |
        v
land / camera / plant / mammal / ethics statuses resolved
        |
        v
THIRD_NETWORK_FIELD_EXECUTION_READY
        |
        v
confirmatory route videos may be opened
~~~

No route outcome, access mismatch, or morphology value is allowed in the
route-blind presurvey.

## Route-blind presurvey

Use:

- `empirical/floral_defence_selectivity/THIRD_NETWORK_ROUTE_BLIND_PRESURVEY_SCHEMA_V1.csv`
- `scripts/evaluate_third_network_route_blind_presurvey.py`

The presurvey can use only:

- flowering plant-species presence;
- mammal-species presence from a predeclared non-route evidence method;
- camera operability.

A site is schema-eligible only if it has:

~~~text
>=5 flowering plant species
>=5 mammal species
camera operability = yes
~~~

The presurvey evaluator rejects columns that would expose:

- L/B route outcome;
- B/L counts or bypass proportion;
- access mismatch;
- plant access depth;
- mammal rostral reach.

Thus a final site cannot be selected because it already shows the desired route
pattern.

## Pre-video confirmatory freeze

Use:

- `empirical/floral_defence_selectivity/THIRD_NETWORK_CONFIRMATORY_FREEZE_RECEIPT_TEMPLATE_V1.json`
- `scripts/validate_third_network_confirmatory_freeze.py`

The receipt freezes before confirmatory route videos are opened:

- final sites;
- final intended plant list;
- route-blind site-selection basis;
- visitor-identification protocol;
- plant morphology protocol;
- mammal morphology protocol;
- route-coding manual version;
- fixed camera effort rule;
- analysis seeds;
- administrative-resolution fields.

The receipt fails if pilot B/L presence was used to choose sites or if camera
effort may be extended based on route outcomes.

## Field administrative gate

Use:

- `empirical/floral_defence_selectivity/THIRD_NETWORK_FIELD_READINESS_TEMPLATE_V1.json`
- `scripts/evaluate_third_network_field_readiness.py`

This document is an operational research gate, not legal advice.\n\nThis gate deliberately contains no legal inference engine. For every planned
action it accepts only:

~~~text
PERMITTED
NOT_REQUIRED_CONFIRMED_BY_AUTHORITY
~~~

or, for an action removed from the design:

~~~text
NOT_PLANNED
~~~

It does not infer permission from prior publications, protected-area category,
land ownership, taxon identity, or ecological precedent.

The gate separately tracks:

- land / site access;
- camera deployment;
- plant morphology measurement;
- plant tissue collection if planned;
- mammal capture / handling if planned;
- animal-ethics or institutional review;
- the predeclared source of mammal morphology;
- any other authorizations identified by the researcher / institution /
  relevant authority.

Authorization windows must cover the full planned field interval.

## Hash binding

Both the route-blind presurvey receipt and the pre-video confirmatory freeze
receipt are SHA256-bound into the field-readiness configuration.

Field readiness therefore fails if:

- the presurvey receipt changes after site selection;
- the confirmatory freeze receipt changes after approval;
- the final site list is not a subset of the route-blind eligible site pool.

## Mammal morphology path

The frozen visitor phenotype remains:

~~~text
V_i = functional rostral reach in mm
~~~

Allowed predeclared source modes are:

~~~text
LIVE_CAPTURE
EXISTING_SPECIMENS
INDEPENDENT_MORPHOMETRIC_DATA
~~~

If live capture is not planned, it does not need to be added merely to satisfy
the model. However, the alternative morphology source must be documented and
must support use for the same regional mammal assemblage.

## Current unresolved inputs

Repository logic is ready, but the following cannot be truthfully filled until
a real field collaboration/site exists:

~~~text
planned field dates
private site-location receipt
route-blind presurvey receipt
final site / plant list
land/site access evidence
camera-deployment authorization/confirmation
plant-measurement authorization/confirmation
mammal morphology source receipt
capture/handling authorization if capture is retained
animal-ethics / institutional review status
other required authorization check
~~~

Until those are resolved:

~~~text
THIRD_NETWORK_FIELD_EXECUTION_BLOCKED
~~~

## Scientific boundary

Field readiness is not a k=3 result.

Only a completed confirmatory dataset that passes the frozen biological gates
can generate `r_T`, and only then can `scripts/analyze_joint_access_routing_k3.py`
compute the equal-network three-network statistic.

If the confirmatory mammal result is null-compatible or opposite in sign, it
remains the third confirmatory network and is not replaced.
