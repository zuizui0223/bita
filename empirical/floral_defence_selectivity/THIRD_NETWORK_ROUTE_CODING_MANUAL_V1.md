# Third-network route-coding manual v1

## Status

~~~text
CODING_MANUAL_STATUS = FROZEN_BEFORE_CONFIRMATORY_DATA
SYSTEM = CAPE_SMALL_MAMMAL_X_PROTEA
PRIMARY_CODES = L_B_A_N
MORPHOLOGY_BLIND = REQUIRED
~~~

This manual governs event-level route classification for the prospective
small-mammal third network. It is frozen before confirmatory video decoding.


Frozen code meanings:

~~~text
L = LEGITIMATE
B = BYPASS
A = AMBIGUOUS
N = NON_NECTAR / NOT A FEEDING EVENT
~~~

Route coders must not receive:

- plant access depth P_j;
- mammal reach V_i;
- mismatch M_ij;
- unit-level B/(B+L);
- any M-Y plot, coefficient or p-value.

## Unit of coding

One **feeding event** is one continuous bout by one identified mammal at one
focal inflorescence, ending when the animal leaves the flower head or clearly
switches to a non-feeding activity.

Multiple contacts within one continuous bout are one event unless the animal
leaves and returns.

## Primary decision tree

### Step 1 — Is this a nectar-directed feeding event?

Code **N** if the animal:

- only crosses the frame;
- sniffs without feeding;
- grooms;
- eats non-floral tissue without evidence of nectar access;
- handles the inflorescence for a purpose that cannot reasonably be linked to
  nectar intake.

If nectar-directed feeding is visible or strongly supported by repeated licking
or probing, continue.

### Step 2 — Is the natural legitimate entrance route visible?

If the camera angle cannot distinguish the access path, code **A**.

Do not infer a route from plant or mammal identity.

### Step 3 — Did the animal use the natural open pathway?

Code **L = LEGITIMATE** only when:

1. the approach uses the natural non-destructive entrance;
2. the snout/head enters through that opening;
3. the feeding apparatus follows the normal floral access corridor;
4. no tissue tearing, lateral hole, displaced bract/tepal, or alternate
   side-access is used to obtain nectar.

Contact with pollen presenters is recorded separately but is **not required**
for L. The route definition concerns access geometry, not pollination success.

### Step 4 — Did the animal avoid the natural route to obtain nectar?

Code **B = BYPASS** only when:

1. nectar-directed feeding is visible or strongly supported;
2. access occurs from a lateral, basal, destructive, or otherwise alternative
   route;
3. that route avoids the normal open access corridor;
4. the alternative route is used to reach the reward rather than merely damage
   tissue.

Qualifying behaviors can include:

- chewing or tearing floral tissue to reach nectar;
- widening or displacing a barrier and feeding through the new opening;
- lateral probing through a pre-existing or newly created opening;
- repeated use of a destructive access point created by another visitor.

Secondary use of a pre-existing bypass opening is still B because the event
uses the bypass route.

### Step 5 — Ambiguity rule

Code **A = AMBIGUOUS** whenever:

- nectar-directed intent is plausible but not clear;
- the animal obscures the access path;
- the route begins outside the camera field;
- the clip ends before the route can be resolved;
- the coder is deciding between L and B based on species knowledge rather than
  visible behavior.

A is excluded from B/(B+L). It is never reassigned statistically.

## Auxiliary fields

Each event should also record, without changing the primary route code:

- visitor species confidence: HIGH / MEDIUM / LOW;
- route visibility: FULL / PARTIAL / POOR;
- tissue damage visible: YES / NO / UNCLEAR;
- pollen-presenter contact: YES / NO / UNCLEAR;
- nectar-directed behavior confidence: HIGH / MEDIUM / LOW;
- pre-existing bypass opening used: YES / NO / UNCLEAR;
- clip quality: PASS / FAIL.

Only clip_quality=PASS and visitor identification above the frozen minimum
confidence threshold enter confirmatory aggregation.

## Species identification

Species identity may be assigned by:

- diagnostic video morphology;
- a paired camera angle;
- a validated site-specific identification key.

If two mammal species cannot be distinguished reliably on video, they cannot be
silently pooled into one synthetic species after route outcomes are known.
Before confirmatory collection, either:

1. establish a reliable identification rule; or
2. remove that indistinguishable taxon pair from the intended confirmatory
   visitor set.

## Double coding

At least 20% of reliability-eligible confirmatory events are independently
coded by a second coder. The reliability-eligible frame is fixed as
`dataset_role=CONFIRMATORY`, `clip_quality=PASS`, and visitor identity
confidence HIGH or MEDIUM.

The double-coded subset is outcome-blind and deterministic. Using frozen seed
`20260922`, score every eligible event by SHA256(`seed:event_id`), sort by
that score, and select the lowest `ceil(0.20 * n_eligible)` event IDs. Route
code, plant identity, mammal identity, P, V and M are not used to choose the
subset.

The event table's `double_coded` flags must match this exact subset. A selected
event must contain an independent `second_route_code`.

Report:

- raw four-class agreement for L/B/A/N;
- Cohen's kappa for L/B/A/N;
- a secondary L/B-only agreement among events both coders classify as L or B.

Target:

~~~text
kappa_LBAN >= 0.80
~~~

If the target is missed, adjudication may use only disagreement examples and
this manual. Coders may not inspect P, V, M or M-Y results during revision.

## Adjudication

A final adjudicated route code may be produced for double-coded disagreements,
but:

- adjudicator is blind to morphology-derived mismatch;
- original coder values remain archived;
- rule changes are versioned;
- all confirmatory videos are recoded under a revised manual if the definition
  changes materially.

## Exclusions

Exclude from primary Y construction:

- A events;
- N events;
- failed-quality clips;
- visitor identities below the frozen confidence threshold.

Do not exclude a valid L or B event because it conflicts with the predicted
direction.

## Frozen output mapping

~~~text
L -> L_count += 1
B -> B_count += 1
A -> excluded from numerator and denominator
N -> excluded from numerator and denominator

Y = B_count / (B_count + L_count)
~~~

No pseudocount is added.
