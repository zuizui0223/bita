# Third access-routing network bounded search audit v1

## Decision

~~~text
SEARCH_STATUS = COMPLETE
FREEZE_COMMIT = ae98e496a99fa7f5b333bbe7881025d13a8d8768
PUBLIC_THIRD_NETWORK = NOT_AVAILABLE
CURRENT_JOINT_NETWORK_K = 2
K3_PROTOCOL = FROZEN_FOR_FUTURE_DATA
~~~

The search was performed after the outcome-blind preregistration was merged.
No candidate passed all frozen eligibility gates. The estimand was not relaxed.

## Frozen gates applied

A confirmatory third network had to provide all of:

1. non-Insecta / non-Aves visitor fauna;
2. an independent field project;
3. public raw or minimally processed data;
4. visitor × plant inferential units;
5. a pre-outcome monotone access-constraint phenotype;
6. a legitimate-versus-bypass route outcome;
7. at least 30 matched units, 5 visitor species and 5 plant species.

Primary estimand remained:

~~~text
M = log(plant legitimate-route depth / visitor reach)
Y = bypass / (bypass + legitimate)
r_T = rank association(M, Y)
~~~

## Bounded repository sweep

Search surfaces:

- Dryad;
- Zenodo;
- Figshare;
- OSF;
- article-linked public supplements/repositories.

Query families were restricted to metadata/schema discovery and covered:

- mammal / bat floral interaction networks + morphology;
- mammal nectar robbing / nectar theft datasets;
- camera-trap flower visitor behavior;
- reptile / lizard flower visitor networks;
- non-Insecta/non-Aves public pollination datasets with route coding.

Candidates were adjudicated from repository metadata, README/variable dictionaries,
and Methods needed to establish the frozen gates. If a relevant access-routing
direction was exposed in discovery, the candidate was excluded from the
confirmatory lane as preregistered.

## Closest near miss

### Bat-flower trait matching — Dryad 10.7291/D1QX26

This is the closest structural match.

~~~text
fauna: Mammalia
sites: 8
visitor trait: bat tongue length
plant trait: flower depth
multi-visitor: yes
multi-plant: yes
public data: yes
frozen access mismatch: constructible
frozen route outcome: absent
~~~

The public interaction table records pollen presence/diet association, not
legitimate-versus-bypass handling. It therefore cannot produce
`Y = B/(B+L)` without changing the preregistered estimand.

## Other high-value near misses

- Caatinga bat-flower network, Dryad `10.5061/dryad.v9s4mw6w7`:
  five nectar-feeding bat species × 30 plants, but no route outcome.
- Pantanal bat-flower network, Dryad `10.5061/dryad.b5mkkwhs0`:
  12 bats × 8 plants, but no mechanical mismatch / route outcome pair.
- Neotropical bat-plant niche-overlap archive, Dryad
  `10.5061/dryad.cvdncjt76`: broad multi-network data and coarse flower
  accessibility, but no legitimate-versus-bypass response and no commensurate
  visitor reach trait.
- Central Mexico bat-flower networks, Dryad
  `10.5061/dryad.tht76hfb5`: community breadth passes, route outcome absent.
- Mucuna mammal camera-trap systems: route/handling categories can be rich, but
  available studies are single-plant systems and fail the >=5 plant gate.

## Interpretation

The bounded search identifies a real data gap rather than a negative biological
result:

> public mammal/bat pollination networks commonly preserve visitor × plant
> interactions and sometimes preserve access traits, while route-resolved
> legitimate-versus-bypass handling is rarely retained at the same community
> scale.

Therefore the correct current paper boundary remains `k=2`.

The next admissible paths are:

1. wait for a new public third-fauna dataset satisfying the frozen contract; or
2. prospectively collect a third-fauna network under the already frozen field
   data schema.

Do not substitute interaction occurrence, pollen presence, or coarse flower
accessibility for the frozen bypass outcome simply to reach k=3.
