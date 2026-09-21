# Third independent access-routing network bounded search v1

## Decision

~~~text
SEARCH_DATE = 2026-09-21
FREEZE_COMMIT = ae98e496a99fa7f5b333bbe7881025d13a8d8768
PUBLIC_THIRD_NETWORK = NOT_AVAILABLE
REASON = NO_PUBLIC_DATASET_PASSED_ALL_FROZEN_ELIGIBILITY_GATES
ESTIMAND_RELAXATION = PROHIBITED
~~~

This is the preregistered stopping outcome of the public-data search defined in
`THIRD_ACCESS_ROUTING_NETWORK_PREREG_V1.md`.

It does **not** mean that no mammal or reptile flower-visitor dataset exists.
It means that the bounded repositories searched on 2026-09-21 did not yield one
public dataset that simultaneously satisfied the frozen confirmatory contract.

## Frozen contract applied

A candidate had to provide, before route-outcome inspection:

1. a visitor fauna outside Insecta and Aves;
2. an independent field project;
3. public raw or minimally processed data;
4. visitor identity and plant identity;
5. an outcome-independent mechanical access phenotype on both visitor and plant
   sides, or a source-defined equivalent frozen before outcome inspection;
6. event/count coding that distinguishes legitimate access from bypass/robbing;
7. at least 30 visitor x plant x stratum units;
8. at least 5 visitor species;
9. at least 5 plant species;
10. non-zero mismatch variation and both legitimate and bypass interactions.

No gate was relaxed after candidate discovery.

## Bounded repositories searched

The post-freeze search covered public records discoverable from:

- Dryad;
- Zenodo;
- OSF;
- Figshare;
- article-linked repository records surfaced through those services.

Searches were restricted to repository metadata, file lists, README/variable
descriptions, and Methods needed to establish schema. When a search result or
prior reading exposed the relevant biological outcome, that candidate was
removed from the confirmatory lane and recorded as
`DISCOVERY_EXPOSED_NOT_CONFIRMATORY`.

## Main failure modes

### A. Morphology + multi-species network, but no bypass route outcome

Examples include bat-flower interaction or trait-matching archives with multiple
bat and plant species. These can identify which plant species a bat used, and in
some cases contain tongue length and flower depth, but they do not encode the
same legitimate-versus-bypass response required by the frozen BITA estimand.

Representative public records screened:

- 10.7291/D1QX26 — bat-flower trait matching;
- 10.5061/dryad.v9s4mw6w7 — Caatinga bat-flower interaction networks;
- 10.5061/dryad.b5mkkwhs0 — Pantanal bat-flower interaction networks;
- 10.5281/zenodo.13468732 — NeoBat interaction compilation.

### B. Route-resolved flower use, but only one or too few plant species

Several mammal/reptile systems contain direct behavioral observations that can
distinguish kinds of flower use, but they are focal-species studies and cannot
supply the frozen >=5 plant-species visitor x plant mismatch network.

Representative records screened:

- 10.5061/dryad.05qfttf1v — *Kigelia africana* visitor observations;
- 10.5061/dryad.9s4mw6mqc — Yungas bat-pollination observations (three focal
  plant species);
- 10.5061/dryad.2ngf1vhj1 — *Cneorum tricoccon* / *Podarcis lilfordi*;
- 10.5061/dryad.gtht76hsq — one squirrel species feeding across plants, without
  the frozen floral bypass coding.

### C. Multiple plants / animals, but wrong ecological response

Large mammal, bat, lemur, or mixed flower-visitor datasets can have sufficient
taxonomic breadth but measure interaction occurrence, diet/frugivory, pollen
loads, or resource use rather than bypass of the legitimate floral access route.

Representative records screened:

- 10.5061/dryad.sxksn03b4 — plant-lemur frugivory;
- 10.5061/dryad.1vhhmgqqs — ring-tailed lemur diet;
- 10.5061/dryad.pg4f4qrv5 — multi-taxon flower eDNA detections.

## Why near-matches were not promoted

The purpose of the third network is to lift the current k=2 ceiling by adding
**one more independent realization of the same estimand**.

Replacing bypass propensity with generic interaction frequency, diet choice,
pollen presence, or pollination success would create a different estimand.
Replacing visitor x plant mismatch with one-plant treatment contrasts would
also create a different estimand.

Either move could manufacture k=3 numerically while failing to add a third test
of the original access-routing claim. The frozen protocol therefore rejects
those substitutions.

## Current scientific conclusion

~~~text
EXISTING_CONFIRMATORY_NETWORKS = 2
PUBLIC_SCHEMA_ELIGIBLE_THIRD_NETWORK = 0
JOINT_NETWORK_K = 2
K3_PUBLIC_REANALYSIS = NOT_CURRENTLY_AVAILABLE
~~~

The current k=2 ceiling remains scientifically real.

## Next admissible routes

Only three routes can now lift the ceiling without weakening the claim:

1. a newly released public dataset that passes the frozen contract;
2. recovery of an existing but currently unavailable raw dataset that passes
   the same contract;
3. a prospective third-fauna field dataset collected under the frozen estimand.

The next BITA scientific task is therefore **not** another search for a favorable
near-match. It is either monitoring for a schema-eligible release or designing
the prospective third-fauna data collection so that M and Y are measured before
analysis.

## Search reopening rule

This bounded search may be reopened only when a new repository record or newly
released raw file can be assessed against the unchanged frozen gates.

Do not reopen merely to relax:

- the >=5 visitor-species gate;
- the >=5 plant-species gate;
- the >=30-unit gate;
- the requirement for mechanical access mismatch;
- the legitimate-versus-bypass outcome.

