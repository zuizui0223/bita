# Participation versus routing decomposition — preregistration v1

## Status

~~~text
STATUS = PRE_EFFECT_DESIGN
PRIMARY_DATA = EPHI_ECUADOR_PUBLIC_MIRROR
CURRENT_LETTER_ROUTE_RESULT = FROZEN_EXISTING_RESULT
NEW_PARTICIPATION_EFFECT = NOT_YET_OPENED
DENOMINATOR_AUDIT = REQUIRED_BEFORE_EFFECT
~~~

## 1. Question

The current Letter establishes that, conditional on observed exploitation, greater
legitimate-route mismatch is associated with greater bypass use. That does not by
itself establish whether access constraints leave total exploitation unchanged,
reduce it, or increase it.

This analysis separates:

~~~text
PARTICIPATION:
    how much target-bird floral interaction occurs per camera effort,
    including defensible zero opportunities

ROUTING:
    among interactions that occur, what fraction uses bypass/robbery
~~~

The decomposition is observational.

## 2. Opportunity denominator

No global bird × plant cross-product is allowed.

The primary potential opportunity is:

~~~text
unique camera waypoint
×
target bird species observed somewhere in the same site
during at least one valid camera interval for that waypoint
~~~

Target birds are Trochilidae plus *Diglossa*, matching the Letter.

Bird availability is defined from any target-bird observation at the site during
the camera interval, regardless of piercing/route outcome. Thus route outcome is
not used to decide whether a consumer belongs to the local opportunity pool.

Repeated camera rows for one waypoint are aggregated before interaction counts are
formed. This prevents one interaction row from being assigned repeatedly to
multiple camera-deployment rows.

## 3. Camera-effort gate

Source metadata define `duration_sampling_hours` as daylight sampling hours.
Ecuador does not provide `camera_flowers_count`, so flower-hours cannot be the
primary exposure denominator.

Primary camera-row eligibility:

1. nonblank waypoint, site and plant species;
2. parseable start and end dates;
3. positive finite `duration_sampling_hours`;
4. known compromised camera states `yes`, `maybe` and `flower_problem` are
   excluded;
5. `no`, blank and `NA` camera-problem states are retained because no definite
   malfunction is recorded.

`duration_from_pics` is not used as a fallback because it is derived from
interaction pictures and would make sampling effort outcome-dependent.

A strict sensitivity retains only `camera_problem = no`.

## 4. Interaction-count rule

Consumer availability and exploitation count are different objects.

Availability uses any target-bird observation.

The primary exploitation count uses the Letter's missing-as-no route policy:

- piercing/robbery `yes` -> robbery;
- explicit `no` -> legitimate;
- blank/NA/N/A missing status -> legitimate;
- `maybe`, `thief`, `not_interacting`, and other nonbinary states -> excluded.

In addition, rows explicitly coded `feeding_activity = no_feeding` are excluded
from the participation numerator because they are definite nonfeeding observations.

A Letter-aligned sensitivity omits this extra `no_feeding` exclusion. This
sensitivity cannot replace the primary rule after effects are opened.

## 5. Trait matching

For each opportunity:

~~~text
M = log(flower_tube_cm / bird_culmen_cm)
barrier = M > 0
~~~

Plant tube length uses the site-specific mean when available, otherwise the species
mean fallback already used by the Letter. Bird culmen uses the species mean divided
by 10 to convert mm to cm.

Only trait-matched potential opportunities enter effect estimation.

## 6. Aggregation before inference

Waypoint × bird opportunities are first collapsed to:

~~~text
bird species × plant species × site
~~~

For each row:

- total camera hours = sum eligible waypoint hours;
- total interaction count = robbery + legitimate counts;
- total interaction rate = total count / camera hours;
- robbery count and legitimate count are retained separately;
- robbery proportion is defined only where total count > 0;
- mismatch is the plant-site × bird mismatch.

For the continuous primary statistics, site rows are then collapsed to one
bird × plant dyad, matching the current within-bird routing check:

- dyad participation rate = total interactions / total eligible camera hours
  across sites;
- dyad robbery proportion = total robbery / total interactions across sites,
  when total interactions > 0;
- dyad mismatch = unweighted mean mismatch across contributing sites.

No pair-site, waypoint or raw interaction row is treated as an independent
biological replicate.

## 7. Primary statistics

### 7.1 Participation

For each bird species with at least three trait-matched plant dyads and variation in
both mismatch and participation rate:

1. rank mismatch within bird;
2. rank zero-inclusive interaction rate within bird;
3. center both rank vectors within bird.

Pool the centered ranks across eligible birds and calculate the Pearson correlation:

~~~text
rho_participation
~~~

Inference uses 9,999 permutations that shuffle participation ranks only within each
bird species.

Interpretation:

~~~text
rho_participation < 0  -> mismatch is associated with reduced exploitation rate
rho_participation ≈ 0 -> no monotonic participation association detected
rho_participation > 0  -> mismatch is associated with increased exploitation rate
~~~

The test is two-sided. Lack of significance is **not** equivalence.

### 7.2 Routing on the same reconstructed opportunity system

For bird × plant dyads with at least one counted interaction, apply the same
within-bird rank-centering procedure to mismatch and robbery proportion:

~~~text
rho_routing_reconstructed
~~~

This is a bridge/sensitivity analysis. It must be reported alongside, not substituted
for, the currently frozen Letter routing result.

## 8. Binary barrier decomposition

As a magnitude-oriented secondary analysis, calculate within each bird species:

~~~text
total_rate_difference
    = mean(total interaction rate | barrier)
      - mean(total interaction rate | accessible)

legitimate_rate_difference
    = mean(legitimate interaction rate | barrier)
      - mean(legitimate interaction rate | accessible)

robbery_rate_difference
    = mean(robbery interaction rate | barrier)
      - mean(robbery interaction rate | accessible)
~~~

Only birds observed in both barrier states contribute.

Report the mean and median bird-level differences. Use whole-bird sign flips with
9,999 permutations for the total-rate contrast. Legitimate and robbery components
are decomposition terms and remain secondary.

When legitimate loss < 0 and robbery gain > 0, also report the descriptive
compensation ratio:

~~~text
robbery gain / abs(legitimate loss)
~~~

Do not interpret this ratio as causal mediation.

## 9. Outcome classification frozen before effect opening

Use alpha = 0.05, two-sided, for the two centered-rank permutation tests.

~~~text
ROUTING_WITHOUT_DETECTED_PARTICIPATION_LOSS
    rho_routing_reconstructed > 0 and p_route < 0.05
    AND NOT (rho_participation < 0 and p_participation < 0.05)

SUPPRESSION_PLUS_REROUTING
    rho_routing_reconstructed > 0 and p_route < 0.05
    AND rho_participation < 0 and p_participation < 0.05

FILTERING_DOMINANT
    NOT (rho_routing_reconstructed > 0 and p_route < 0.05)
    AND rho_participation < 0 and p_participation < 0.05

MIXED_OR_UNRESOLVED
    all other outcomes
~~~

The first class does **not** prove unchanged total exploitation. It licenses only
"no detected monotonic participation decline."

## 10. Manuscript language gate

If the result is `SUPPRESSION_PLUS_REROUTING`, wording such as

> reroute rather than eliminate exploitation

must be removed or replaced by wording such as

> access constraints can simultaneously suppress and reroute exploitation.

If the result is `FILTERING_DOMINANT`, the present routing-first title/story must
be reconsidered.

If the result is `ROUTING_WITHOUT_DETECTED_PARTICIPATION_LOSS`, the manuscript
may state that route composition shifted without a detected monotonic decline in
total interaction rate, but may not claim statistical equivalence unless a separate
equivalence margin is preregistered before effect opening.

## 11. Activation gate

No mismatch-participation effect may be computed until the denominator audit shows:

1. parseable camera dates and positive camera-hours support a waypoint denominator;
2. a nonempty temporal local bird pool exists;
3. both positive and zero potential dyads exist;
4. trait matching is available for both positive and zero dyads;
5. source camera metadata are recorded;
6. the final camera-problem handling rule above is executable.

If any gate fails, record the denominator failure and do not search alternative
zero definitions after seeing mismatch effects.

## 12. Claim boundary

This analysis tests whether the **observed pattern** is primarily participation
filtering, route composition change, or both. It does not establish why birds
choose routes and does not replace the prospective factorial causal experiment.
