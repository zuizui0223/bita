# Third-network pilot / confirmatory split contract v1

## Rule

~~~text
PILOT_DATA = ELIGIBILITY_ONLY
PILOT_EVENTS_IN_CONFIRMATORY_ANALYSIS = FORBIDDEN
CONFIRMATORY_DATA_ROLE = CONFIRMATORY
~~~

The pilot exists only to verify that the field system can supply the frozen
schema. It is not an early portion of the confirmatory sample.

## Pilot may be used for

- camera placement;
- species-identification feasibility;
- training and validating whether the frozen L/B/A/N decision tree can be
  applied to visible access paths;
- checking plant and mammal richness from route-blind presurvey information;
- estimating camera uptime, storage requirements and non-outcome field logistics.

Pilot B/L frequencies are never eligibility criteria for a site.

## Pilot may not be used for

- estimating r_T;
- calculating an M-Y plot;
- choosing or dropping sites because B or L is present/absent in pilot footage;
- choosing sites because the observed association is positive;
- choosing plant or mammal species because they support the prediction;
- changing the frozen M or Y definitions;
- adding events later to increase confirmatory significance.

## Physical separation

Store pilot and confirmatory event tables separately.

Required event-table field:

~~~text
dataset_role
~~~

Allowed values:

~~~text
PILOT
CONFIRMATORY
~~~

The confirmatory unit builder accepts **CONFIRMATORY only** and raises an error
if any PILOT row is supplied.

## Transition from pilot to confirmatory collection

The confirmatory phase may begin only after a receipt records:

1. final sites;
2. final intended plant list;
3. final visitor-identification protocol;
4. plant morphology protocol;
5. mammal morphology protocol;
6. route-coding manual version;
7. camera effort rule;
8. permutation seeds.

The receipt is frozen before confirmatory videos are opened.

## Failed pilot

A pilot may fail only for **route-blind operational reasons**, for example:

- visitor identity cannot be resolved to species;
- the camera geometry cannot distinguish the natural entrance from lateral /
  destructive access;
- independent presurvey information cannot plausibly reach the frozen species-
  richness gates;
- equipment or permit constraints make the frozen effort impossible.

Observed absence of B or L in pilot footage is **not** a pilot-failure criterion.

If an operational criterion fails, the system is marked:

~~~text
PILOT_FAIL_SCHEMA
~~~

The pilot result is not a confirmatory null and is not combined with Sakhalkar
or Aubert/EPHI.

If confirmatory collection proceeds and the completed confirmatory dataset later
contains no B or no L, the confirmatory eligibility gate fails. A new site is not
substituted after seeing that result.
