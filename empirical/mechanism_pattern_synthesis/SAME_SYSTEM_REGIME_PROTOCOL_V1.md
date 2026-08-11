# Same-system mechanism regime classification protocol v1

## Purpose

The source-adjudicated ledger now contains multiple studies in which two or more theory-relevant routes are measured in the same biological system. This protocol converts that structure into study-level **mechanism regimes** without subtracting incompatible effect metrics.

The target is not a numerical estimate of `W_AD`. The target is:

> Which qualitative combinations of mutualist and antagonist responses recur within the same biological system, and which systems switch regime with ecological context?

## Unit

One `independence_cluster` = one classification unit.

Multiple doses, species, years, response constructs and reproductive components remain nested evidence inside that cluster.

## A-side regime

For clusters containing `A_to_pollination` and/or `A_to_antagonism`, classify the source-adjudicated state as one of:

```text
shared_tracking
    A is associated with increased mutualist use/service and increased antagonist use/damage.

mutualist_biased
    A increases mutualist use/service while no antagonist increase is detected in the eligible same-system evidence.

antagonist_biased
    A increases antagonist use/damage while no mutualist increase is detected in the eligible same-system evidence.

opposed_or_defensive_signal
    the declared attraction signal is associated with increased mutualist use/service but reduced antagonist use/damage,
    or otherwise shows opposite signs across the two consumer roles.

context_switching
    consumer identity, compound identity, dose or another source-declared context changes which A-side state is expressed.

unresolved
    same-system effects are estimated but uncertainty/direction does not support a stable qualitative state.

not_applicable
    the cluster contains no eligible A-side pair.
```

A source-reported null is different from missing evidence. `antagonist_biased` or `mutualist_biased` is assigned only when the other route was actually tested in the same biological study/panel.

## D-side regime

For clusters containing `D_to_antagonism` and/or `D_to_pollination`, classify as:

```text
guarded
    D reduces antagonist use/damage while legitimate pollinator use/service shows no detected cost in the eligible context.

guarded_window_then_interference
    D reduces antagonist use/damage at a lower dose/expression/time scale than the context in which a pollinator cost becomes detectable.

pollinator_interference
    D reduces antagonist use/damage and also reduces legitimate pollinator use/service in the eligible context.

response_construct_mixed
    D reduces antagonism but the pollinator state changes sign or interpretation across distinct response constructs
    (for example visit number versus residence/consumption).

context_switching
    D alternates between guarded and interference-compatible states across reward, consumer, exposure-duration or other declared context,
    without a single ordered dose/expression window being the main source result.

unresolved
    the same-system D routes are measured but their direction/uncertainty does not establish one of the above states.

not_applicable
    the cluster contains no eligible D-side pair.
```

## Evidence requirement

A regime must be supported by at least Tier 1–4 source-adjudicated records already present in the mechanism ledger/readouts. Candidate-only evidence is not sufficient.

`guarded_window_then_interference` requires a source-verified ordering of contexts (for example, antagonist deterrence at lower concentration than pollinator interference). It does **not** require subtracting coefficients across outcomes.

## Confidence

Each classification receives:

```text
high
    both routes are directly source-verified and the regime follows without relying on unresolved numerical estimates.

moderate
    the qualitative source pattern is clear but one route is based on a source-reported null, threshold, or metric-specific result.

low
    the source-adjudicated same-system records are individually unresolved or contradictory.
```

Confidence is evidence quality, not posterior probability.

## Theory-facing interpretation

The classifications map onto the theory only as compatibility statements:

```text
guarded or guarded_window_then_interference
    compatible with contexts in which antagonist-relief can arise before strong pollinator interference.

pollinator_interference
    demonstrates simultaneous defence benefit and mutualist cost, but does not show whether rho exceeds iota.

shared_tracking
    establishes an A-side route through which stronger attraction can increase antagonist exposure as well as mutualist use.

context_switching
    directly supports the paper's central empirical claim that route state depends on ecological context.
```

No regime is called `complementarity` or `substitutability` unless a direct A×D reproductive interaction identifies that sign.

## Independence and prevalence guardrail

The frequency of regime labels in the current ledger is a **coverage description of the source-adjudicated study set**, not an estimate of how frequent each regime is in nature.

Search strategy is deliberately information-rich rather than representative. Regime counts may be used to show recurrence across independent systems, not prevalence.