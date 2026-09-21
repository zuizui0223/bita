# Third-network collaboration response quarantine v1

## Purpose

The first collaboration inquiry requests only route-blind feasibility, but a
collaborator may voluntarily mention unpublished historical route outcomes.

Those disclosures must not influence confirmatory site/species selection.

## Raw-response rule

The raw e-mail or message is correspondence provenance. It is **not** the
site-selection table.

Only a route-blind extraction following:

- `THIRD_NETWORK_COLLABORATION_RESPONSE_SCHEMA_V1.csv`

may enter the candidate-pool workflow.

Do not copy route direction, route counts, coefficients, p-values or plots into
the extraction table.

## Exposure classes

~~~text
CLEAN
  no route-specific historical outcome disclosed

GENERIC_ONLY
  generic statement that multiple access routes can occur, with no candidate
  site/plant/mammal-specific direction or value

SITE_EXPOSED
  route-specific information was disclosed for a named candidate site

PLANT_EXPOSED
  route-specific information was disclosed for a named candidate plant species

MAMMAL_EXPOSED
  route-specific information was disclosed for a named candidate mammal species

SYSTEM_EXPOSED
  disclosure is broad enough to reveal the route pattern across the intended
  candidate system before site freeze
~~~

## Exclusion rule

Before confirmatory site freeze:

- SITE_EXPOSED -> named site cannot enter the confirmatory pool;
- PLANT_EXPOSED -> named plant cannot be used to choose the confirmatory pool;
- MAMMAL_EXPOSED -> named mammal cannot be used to choose the confirmatory pool;
- SYSTEM_EXPOSED -> the current collaboration/site pool is not confirmatory.

Exposure exclusions are permanent for the current preregistered test.

A favorable or unfavorable disclosed outcome is treated identically.

## Generic feasibility

A statement such as:

> small mammals sometimes use destructive or lateral nectar access in Protea

does not identify a candidate site/species and is already part of the published
feasibility basis. It can be recorded as GENERIC_ONLY.

It cannot be used to rank candidate sites or species.

## Structured response intake

Use:

~~~bash
python scripts/evaluate_third_network_collaboration_response.py response_extract.csv
~~~

The evaluator:

1. rejects any non-schema columns;
2. rejects fields named like route outcomes, mismatch values or B/L counts;
3. records exposed sites/plants/mammals only as exclusion identifiers;
4. removes exposed entities from the route-blind candidate pool;
5. blocks the Cape confirmatory lane if SYSTEM_EXPOSED appears;
6. never computes M, Y, r_T, or any route association.

## Handoff

Only the clean candidate pool may be used to construct the later route-blind
field presurvey.

The field presurvey remains separately frozen and still must establish:

~~~text
>=5 flowering plant species
>=5 mammal species
camera operability
~~~

Thus collaboration advice cannot replace the presurvey or biological eligibility
gate.
