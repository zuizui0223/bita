# Direct access-geometry route-rate identifiability audit — freeze v1

STATUS = POST_HOC_DESIGN_AUDIT_FROZEN_BEFORE_FULL_33_PROGRAM_CLASSIFICATION

## Question

Among the 33 independent direct access-geometry study programs in the frozen formal
bibliographic frame, how often does the reported design identify **which absolute
interaction route changed**, rather than only a conditional robbery probability,
robbed-flower prevalence, or route composition?

This audit does **not** change eligibility, effect direction, the standardized-network
replication count, or the primary Ecuadorian estimates.

## Unit

One independent biological study program from the frozen 33-program direct frame.

## Classification variable

Each program receives exactly one primary identifiability class:

1. `ZERO_INCLUSIVE_BOTH_ROUTE_RATES`
   - a common opportunity/exposure denominator is available;
   - legitimate and robbing/bypass events can each be zero on an opportunity unit;
   - absolute rates/counts for both routes can therefore be compared across the focal
     geometry state.

2. `BOTH_ROUTE_COUNTS_NO_ZERO_INCLUSIVE_DENOMINATOR`
   - legitimate and robbing/bypass counts or frequencies are reported separately;
   - however the design does not expose a common zero-inclusive opportunity
     denominator sufficient to distinguish interaction loss from non-observation.

3. `CONDITIONAL_ROUTE_CHOICE_ONLY`
   - response is robbery versus legitimate conditional on an observed interaction,
     or an equivalent route-choice probability/proportion.

4. `ROBBERY_PREVALENCE_ONLY`
   - response is robbed/not robbed, fraction of flowers robbed, holes per flower,
     robbery probability/frequency, or another robbery-only outcome without a
     separately estimable legitimate route rate.

5. `OTHER_ROUTE_RESOLVED_NOT_RATE_IDENTIFIABLE`
   - route-resolved outcome is direct and eligible but does not fit 1–4 and cannot
     identify both absolute route-rate changes.

6. `UNRESOLVED_SOURCE`
   - accessible source evidence is insufficient to classify conservatively.

## Secondary fields

For every program record:

- geometry manipulation: YES / NO;
- legitimate route separately reported: YES / NO / UNCLEAR;
- robbery route separately reported: YES / NO / UNCLEAR;
- explicit no-interaction opportunity state: YES / NO / UNCLEAR;
- common effort/exposure denominator for both routes: YES / NO / UNCLEAR;
- source basis and locator;
- concise classification rationale.

## Strict rule for class 1

A study is **not** class 1 merely because it reports both legitimate and robbing
percentages among visits. It must permit zero legitimate and zero robbery counts on
the same predefined opportunity/exposure units or otherwise provide absolute
route-specific rates against a common effort denominator.

Artificial-flower arrays or focal flowers count as zero-inclusive only if all offered
opportunities are part of the denominator, including unvisited opportunities.

## Interpretation

The audit is descriptive and post hoc.

If class 1 is rare, the manuscript may state that most direct geometry–robbery
studies do not identify whether higher robbery prevalence reflects more robbery,
less legitimate interaction, or both.

If class 1 is common, that novelty claim must be weakened accordingly.

No p-value, prevalence estimate for all ecology literature, or network-k increment is
permitted.

## Frozen source set

The source set is exactly the 33 programs in:

`formal_bibliographic_frame_v2/DIRECT_ACCESS_GEOMETRY_ELIGIBILITY_DECISIONS_V23.csv`

with `decision_status` equal to `ELIGIBLE_DIRECT` or
`ELIGIBLE_DIRECT_NETWORK_OVERLAP`.

No new study enters the denominator during this audit.
