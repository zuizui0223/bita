# Cape collaboration route for prospective third access-routing network v1

## Status

~~~text
ACTIVE_K3_LANE = CAPE_SMALL_MAMMAL_X_PROTEA_PROSPECTIVE
SCIENTIFIC_PROTOCOL = FROZEN
FIELD_EXECUTION_GATE = IMPLEMENTED
INPUT_FREEZE_GATE = IMPLEMENTED
NEXT_EXTERNAL_ACTION = OUTCOME_BLIND_CAPE_COLLABORATION_INQUIRY
HISTORICAL_ROUTE_OUTCOME_DISCLOSURE_BEFORE_SITE_FREEZE = NOT_REQUESTED
~~~

The public-data route has been closed under the frozen third-network gates. The
next admissible path to lift the current k=2 ceiling is a prospective Cape
small-mammal × Protea network.

This collaboration route is deliberately designed so that site selection cannot
use prior knowledge of the access-routing outcome.

## What the collaboration needs

The minimum prospective system remains:

~~~text
>=5 flowering Protea species
>=5 non-flying mammal visitor species
>=30 realized mammal x plant x site units
planning target >=70 units
~~~

Primary variables are already frozen:

~~~text
M = log(legitimate nectar-access depth / functional rostral reach)
Y = bypass / (bypass + legitimate)
~~~

The collaboration therefore needs practical capacity for:

- route-blind plant and mammal presurvey;
- near-focus no-glow IR video;
- plant legitimate-access-depth measurement;
- mammal rostral-reach morphometrics from a predeclared source;
- permit / land-access / ethics routing;
- independent route coding blind to morphology.

The analysis, event schema, route manual, site-selection guard, field-readiness
gate, input checksums, and k=3 integration are already implemented in the
repository.

## Outcome-blind inquiry rule

Before final sites and plants are frozen, do **not** ask collaborators:

- which Protea species are most often robbed or destructively accessed;
- which mammal species show more bypass behavior;
- which sites have a positive access-mismatch / bypass relationship;
- for unpublished B/L event counts;
- for route-specific model coefficients or plots.

The first inquiry may ask only for route-blind feasibility:

- where >=5 candidate Protea species can be sampled in one coordinated programme;
- route-blind small-mammal species richness / presence;
- flowering overlap or sequential field windows;
- camera logistics and access;
- feasibility of measuring plant access depth;
- availability of independent mammal morphometrics;
- permit, land-manager and ethics pathways.

Historical published behavior is used only to establish that route coding is
biologically feasible, not to select the confirmatory site.

## Published feasibility anchors

### Community breadth

Kühn et al. (2017), DOI 10.1016/j.sajb.2017.08.020, documented three
co-occurring small-mammal-pollinated Protea species at Kraggashoek in the
Western Cape and a community of eight small-mammal flower visitors.

This is strong feasibility evidence for mammal richness, but three focal plant
species do not by themselves satisfy the frozen >=5-plant gate.

### Remote-camera method

Zoeller et al. (2016), DOI 10.1071/BT15111, used remote cameras on four
small-mammal-pollinated Protea species and documented typically three to six
rodent visitor species per Protea.

Melidonis & Peter (2015), DOI 10.1016/j.sajb.2014.12.009, independently
demonstrated modified camera traps for in-situ rodent-flower interactions in
Protea foliosa.

### Route-class feasibility

Biccard & Midgley (2009), DOI 10.1016/j.sajb.2009.08.003, documented legitimate
pollination behavior in several rodent species visiting Protea nana and also
destructive behavior by Rhabdomys pumilio.

That publication supports the biological observability of distinct access
routes. It is **not** used to choose a confirmatory plant, mammal, or site.

## Current contact shortlist

Verified from official institutional pages on 2026-09-21.

### 1. Prof Sandy-Lynn Steenhuisen — University of the Free State

Official contact:

~~~text
SteenhuisenS@ufs.ac.za
~~~

Current UFS profile describes research on pollination-system shifts and floral
traits, explicitly including mammal pollination in Protea. She coauthored both
the remote-camera Protea work and the three-species community study.

Official source:
https://www.ufs.ac.za/aru/aru-team/aru-team/dr-sandy-lynn-steenhuisen

### 2. Emeritus Prof Jeremy Midgley — University of Cape Town

Official contact:

~~~text
jeremy.midgley@uct.ac.za
~~~

UCT currently lists rodent pollination among his active research interests. He
coauthored the Protea nana study and the co-occurring Protea community work.

Official source:
https://science.uct.ac.za/department-biological-sciences/staff-academic-staff/emeritus-professor-jeremy-midgley

### 3. Prof Craig Peter — Rhodes University

Official contact:

~~~text
c.peter@ru.ac.za
~~~

Rhodes lists him as Head of Botany and a pollination biologist. He coauthored
the Protea foliosa modified-camera study.

Official sources:
https://www.ru.ac.za/botany/staff/craigpeter/
https://www.ru.ac.za/botany/prospectivestudents/postgraduates/botanyhonours/

### 4. Prof Steven D. Johnson — University of KwaZulu-Natal

Official contact:

~~~text
JohnsonSd@ukzn.ac.za
~~~

UKZN lists his research focus as plant-pollinator interactions and pollination
biology. He coauthored the 2016 remote-camera Protea study.

Official source:
https://agriculture-science.ukzn.ac.za/staff-profile/prof-steve-johnson/

## Contact sequence

Recommended operational order:

~~~text
1. Steenhuisen + Midgley
   -> system/site feasibility + Protea/mammal expertise

2. Peter
   -> camera method + Eastern Cape feasibility / backup system

3. Johnson
   -> pollination design / morphology / broader South African network support
~~~

This ordering is based on direct relevance to the prospective Protea mammal
system, not on any observed route outcome.

## First-response gate

A positive reply is useful only if it can address route-blind feasibility.

Record:

~~~text
candidate region/site
candidate Protea richness
route-blind mammal richness evidence
flowering window
camera feasibility
plant morphology feasibility
mammal morphology source
land/permit/ethics route
interest in prospective collaboration
~~~

Do not record historical B/L frequencies in the site-selection receipt.

## Repository handoff

If a collaborator identifies a viable route-blind site pool:

1. populate the route-blind presurvey schema;
2. evaluate it with
   `scripts/evaluate_third_network_route_blind_presurvey.py`;
3. freeze final sites/plants in the pre-video receipt;
4. close the field-readiness gate;
5. deploy confirmatory cameras;
6. keep route and morphology streams separate;
7. freeze all confirmatory inputs with SHA256;
8. build analysis units;
9. run r_T once;
10. run equal-network k=3 once.

If no collaboration can satisfy the frozen richness/schema gates, retain k=2
rather than relaxing the estimand.
