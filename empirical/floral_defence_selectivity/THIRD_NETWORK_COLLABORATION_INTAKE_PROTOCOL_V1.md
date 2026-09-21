# Cape collaboration reply intake and contamination quarantine v1

## Purpose

A collaborator may volunteer historical route-outcome information even when the
initial inquiry explicitly asks only for route-blind feasibility.

That disclosure cannot be undone. This protocol prevents it from becoming a
site-selection advantage.

~~~text
COLLABORATOR_REPLY_OUTCOME_EXPOSURE
!=
PERMISSION_TO_USE_EXPOSED_OUTCOME_FOR_SITE_SELECTION
~~~

The direction or magnitude of an exposed historical route outcome is never
stored in the collaboration registry.

## Structured route-blind intake

Use:

- `THIRD_NETWORK_COLLABORATION_RESPONSE_INTAKE_SCHEMA_V1.csv`
- `scripts/evaluate_third_network_collaboration_intake.py`

Allowed feasibility fields are limited to:

- candidate site / region;
- route-blind flowering Protea richness;
- route-blind mammal richness;
- flowering window;
- camera feasibility;
- plant access-depth feasibility;
- mammal rostral-morphometric feasibility;
- permit / land / ethics pathway;
- collaboration interest.

Forbidden fields include:

- B/L counts or proportions;
- robbing / bypass rate;
- route-specific coefficients or p-values;
- access-mismatch × route association;
- plant- or mammal-specific route direction;
- site-specific route direction.

The evaluator rejects intake files containing such outcome columns.

## Exposure flag

Every reply must be classified:

~~~text
NONE
EXPOSED
~~~

If EXPOSED, create one or more rows in:

`THIRD_NETWORK_COLLABORATION_EXPOSURE_REGISTRY_V1.csv`

Allowed exposure scopes:

~~~text
SITE
PLANT
MAMMAL
GENERAL
~~~

Do not record whether the historical direction was positive, negative, strong,
weak, significant, or null.

## Quarantine rules

### SITE exposure

If a reply exposes site-specific legitimate/bypass behavior before the
confirmatory site list is frozen:

~~~text
required_action = QUARANTINE_SITE
~~~

That site cannot enter the prospective confirmatory site pool.

This is intentionally conservative. A different route-blind site may be used,
but the exposed site cannot be restored because its historical route outcome
looked convenient or inconvenient.

### PLANT exposure

If a reply exposes plant-specific route behavior but not a site-specific
association:

~~~text
required_action = NO_TAXON_CHERRY_PICKING
~~~

The plant may enter only under a predeclared route-blind inclusion rule that
retains **all** eligible flowering plants in the frozen site pool (or another
non-outcome rule frozen before route data are opened). It cannot be selected or
dropped because of the exposure.

### MAMMAL exposure

Use the same rule:

~~~text
required_action = NO_TAXON_CHERRY_PICKING
~~~

Mammal taxa are not retained/dropped because of the historical disclosure.
Observed confirmatory visitors follow the frozen identification and eligibility
rules.

### GENERAL exposure

General statements such as “destructive feeding has been observed in this
pollination system” establish coding feasibility only.

~~~text
required_action = FEASIBILITY_CONTEXT_ONLY
~~~

They cannot determine site or taxon inclusion.

## First feasible collaboration stopping rule

The collaboration search is not a competition for the most promising historical
outcome.

Once one collaboration route yields a candidate site pool that:

- is not site-quarantined;
- plausibly supports >=5 flowering Protea species;
- plausibly supports >=5 mammal visitor species;
- supports camera deployment;
- supports P and V measurement;
- has an identifiable access / permit / ethics pathway;

the project stops shopping for a biologically more favorable collaborator and
moves to the route-blind presurvey.

## Handoff

~~~text
structured collaboration intake
        |
        v
exposure quarantine applied
        |
        v
first route-blind feasible collaboration
        |
        v
route-blind presurvey
        |
        v
pre-video site freeze
~~~

No collaboration reply itself contributes an event to B, L, Y, M, r_T, or the
k=3 statistic.
