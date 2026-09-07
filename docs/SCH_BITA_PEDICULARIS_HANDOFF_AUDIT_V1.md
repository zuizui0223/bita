# SCH -> BITA Pedicularis handoff audit v1

## Conclusion

The current SCH `Pedicularis rex` V2 full-surface analyzer and the BITA focal dimensional-release wrapper are schema-compatible. The E1 blocker is empirical execution, not a missing software bridge.

## SCH output required by BITA

BITA requires:

```text
receipt_schema_version = SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1
status = MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE
system = Pedicularis rex
system_wrapper_schema_version = SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2
```

The SCH V2 wrapper delegates the causal surface to `analyze_sch_compromise_surface`, which emits the registered state-optimum receipt and semantics, then adds the Pedicularis wrapper fields.

## Optimum semantics

BITA state-specific mode requires:

```text
z_pollinator_context = STATE_SPECIFIC_P1G0_REPRODUCTIVE_OPTIMUM_NOT_AUTOMATICALLY_PURE_F1
z_combined = STATE_SPECIFIC_P1G1_COMBINED_REPRODUCTIVE_OPTIMUM
```

SCH exports these semantics. BITA therefore does not need to relabel a context-specific optimum as a pure function optimum.

## Non-circular antagonist definition

SCH V2 exports:

```text
G0 = SEED_PREDATOR_INDEPENDENTLY_EXCLUDED
G1 = SEED_PREDATOR_EXPOSED
water_y = HELD_FIXED_ACROSS_ALL_SCH_CELLS
```

and a readiness reference grounded in:

```text
SCH_PEDICULARIS_PREDATOR_METHOD_V3
TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_WITH_POLLINATOR_ACCESS_PRESERVED
```

This satisfies BITA's rule that the Chapter-1 antagonist intervention cannot be the same drained/protected water contrast later used as Chapter-3 y.

## Context lock

Both repositories require one population and one season per confirmatory package. BITA additionally checks that:

```text
SCH receipt population_id == BITA raw population_id
SCH receipt season_id == BITA raw season_id
frozen threshold population_id == BITA raw population_id
frozen threshold season_id == BITA raw season_id
```

## Remaining E1 blocker

```text
software/schema bridge       READY
theoretical semantics        READY
non-circular provenance rule READY
same-context empirical SCH receipt NOT YET ACQUIRED
```

No further interface redesign is required before field execution unless the SCH receipt schema itself changes.
