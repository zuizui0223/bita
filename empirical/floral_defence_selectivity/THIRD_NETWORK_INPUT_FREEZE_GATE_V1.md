# Third-network confirmatory input-freeze gate v1

## Purpose

This gate prevents the prospective third-network route outcome and morphology
tables from being edited after their independent collection/coding and before
integration.

The only supported confirmatory sequence is:

~~~text
field readiness = READY
        |
        v
confirmatory camera deployment fixed
        |
        v
route events coded blind to P, V and M
plant morphology completed without route outcomes
mammal morphology completed without route outcomes
        |
        v
all four input files checksum-frozen
        |
        v
BITA_THIRD_NETWORK_INPUT_FREEZE_V1
        |
        v
checksum-verifying unit builder
        |
        v
M = log(P/V), Y = B/(B+L)
        |
        v
r_T
        |
        v
equal-network k=3 test
~~~

No route/morphology join is permitted before the manifest exists.

## Frozen input files

The manifest binds:

1. confirmatory event/route table;
2. plant morphology table;
3. mammal morphology table;
4. confirmatory camera-deployment table;
5. pre-video confirmatory freeze receipt;
6. field-readiness receipt.

Every bound file receives a SHA256 digest.

## Camera deployment contract

Use:

- `empirical/floral_defence_selectivity/THIRD_NETWORK_CAMERA_DEPLOYMENT_SCHEMA_V1.csv`

Every row must be confirmatory and must declare:

~~~text
route_outcome_adaptive = false
~~~

The deployment plan must cover every frozen confirmatory site and every frozen
plant species. Pilot camera deployments remain separate.

The manifest rejects post-outcome extension of camera effort.

## Route events

The event file must satisfy the frozen event schema and contain:

~~~text
dataset_role = CONFIRMATORY
~~~

only.

Pilot rows are rejected rather than silently dropped.

Every event site and plant must belong to the pre-video frozen site/plant list.

## Plant morphology

Plant morphology remains separate from route coding until the manifest is
created.

Primary trait:

~~~text
P_j = access_depth_mm
~~~

Rows outside the frozen site or plant list are rejected.

## Mammal morphology

Mammal morphology remains separate from route coding until the manifest is
created.

Primary trait:

~~~text
V_i = rostral_reach_mm
~~~

Repeated measures are allowed; duplicate replicate keys are rejected.

## Manifest

Create the manifest with:

~~~bash
python scripts/freeze_third_network_confirmatory_inputs.py \
  confirmatory_events.csv \
  plant_traits.csv \
  mammal_traits.csv \
  camera_deployment.csv \
  confirmatory_freeze_receipt.json \
  field_readiness_receipt.json \
  input_freeze_manifest.json
~~~

The script returns only:

~~~text
INPUTS_FROZEN_READY_FOR_JOIN
~~~

when all contracts pass.

## Join gate

The confirmatory unit builder now requires the manifest:

~~~bash
python scripts/build_third_access_routing_units.py \
  confirmatory_events.csv \
  plant_traits.csv \
  mammal_traits.csv \
  input_freeze_manifest.json \
  analysis_units.csv \
  build_audit.json
~~~

Before reading the rows into the integrated analysis, the builder recomputes the
SHA256 of route, plant-morphology and mammal-morphology inputs.

Any difference after freezing returns:

~~~text
FROZEN_INPUT_HASH_MISMATCH
~~~

and no analysis units are produced.

## Claim boundary

A valid input-freeze receipt establishes only that the preregistered data streams
were frozen before integration.

It does not establish:

- that the confirmatory sample passes the >=30 / >=5 / >=5 biological gate;
- that r_T is positive;
- that the third network is statistically supported;
- that k=3 is significant.

Those claims remain downstream of the frozen third-network analysis.
