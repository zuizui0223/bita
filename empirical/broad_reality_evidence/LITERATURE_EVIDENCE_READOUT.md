# Literature evidence readout

## Scope

This evidence layer is a **mechanism-plausibility check**, not a full empirical test of the attraction–defence mixed partial.

The active registered inputs are:

- `broad_route_records.csv`: directional route records coded from the source basis declared in each row;
- `broad_effect_extractions.csv`: quantitative effects eligible for compatible within-stratum synthesis;
- `broad_meta_analysis_strata.csv`: predeclared compatibility strata and directional expectations.

The current quantitative extraction table contains no eligible effect rows, so no pooled effect magnitude is estimated.

## Evidence level of the current registry

All 13 active direction records currently have

```text
source_basis = crossref_deposited_abstract
```

and were coded by abstract screening. They have **not** been promoted to full-text-confirmed effect records. The direction map must therefore be described as **abstract-level directional coding**, not as a full-text systematic review, a quantitative meta-analysis, or direct validation of a model parameter.

## Current route-level result relevant to the manuscript

The predeclared stratum

```text
route         B_to_pollination
trait class   chemical_barrier
outcome       pollinator_preference_or_foraging
design        manipulation
```

contains **three independent primary study clusters**, and all three abstract-level records are coded with a negative direction. Under the predeclared direction-map rule, this stratum is directionally consistent with the channel expectation that a flower-associated chemical defence/barrier can reduce pollinator preference or foraging in some systems.

A fourth chemical-barrier manipulation record is coded as `mixed`, but its outcome class is `visitation_rate`. It belongs to a **different predeclared stratum** and is not pooled into the three-cluster `pollinator_preference_or_foraging` directional fraction.

Thus the correct statement is not “four studies give 75% support” and not “three of four were negative in one pooled stratum.” The correct statement is:

> one abstract-coded, three-cluster manipulation stratum is uniformly negative, while a separate abstract-coded visitation-rate stratum is mixed/context-dependent.

## What this supports

This provides **restricted abstract-level directional consistency** with one biological premise: flower-associated defence/barrier chemistry can reduce pollinator preference or foraging in some systems.

It supports mechanism plausibility only. It does not establish that the focal trait in the theory has a negative mutualist mixed curvature `M_AD`, because a negative `D -> pollinator use` response does not by itself show that `D` reduces the **marginal mutualist return to the particular focal attraction trait `A`**.

## What this does not support

The current evidence does not estimate:

- the full local mutualist curvature `M_AD` for one focal `A`–`D` pair;
- antagonist relief for that same pair;
- direct attraction–defence joint cost;
- the complete `W_AD` mixed partial;
- the derivative of `W_AD` with respect to pollinator service or antagonist pressure;
- trait covariance, an optimum, or an evolutionary trajectory.

Records from different taxa and different defence/barrier traits can show that a route occurs. They must not be combined as though they measured one common system-specific `D` axis.

## Quantitative readiness

`broad_effect_extractions.csv` currently has only its schema header. Therefore the quantitative synthesis layer is **not ready for parameter-magnitude calibration**. Any future calibration must first add full, compatible effect estimates within a predeclared trait × outcome × metric × design stratum and retain independent study-cluster accounting.

## Next evidence upgrade required

Before the literature layer is described as stronger than abstract-level mechanism plausibility, the relevant primary studies should be checked at full text for:

- exact manipulation and comparator;
- whether the chemical trait is demonstrably defensive in the focal biological context;
- pollinator outcome definition and denominator;
- concentration or dose realism;
- independence of study clusters;
- numerical effect and uncertainty, when recoverable.

Until then, the abstract-coded direction map remains a transparent preliminary evidence layer rather than a parameter-validation result.
