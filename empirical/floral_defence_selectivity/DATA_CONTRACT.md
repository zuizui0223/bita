# Floral defence selectivity data contract

## Unit

One row in the matched registry is one:

```text
independent study cluster
x flower-associated D axis
x declared ecological context
```

Repeated outcomes, doses, consumers, years, and populations do not create independent replication unless the source design establishes independence.

## Files

`matched_system_registry.csv` identifies systems and provenance.

`architecture_codes.csv` contains only information that can be coded before focal outcome inspection.

`outcome_codes.csv` contains antagonist and pollinator outcomes plus uncertainty class.

`quantitative_effects.csv` contains numeric effects only when the source scale and variance are explicitly declared.

## Domain codes

```text
SEPARATED
OVERLAPPED
BYPASS_TOLERANCE
TRANSITIONAL
UNCLEAR
```

## Uncertainty classes

```text
DIRECTION_SUPPORTED
NULL_COMPATIBLE
EQUIVALENCE_SUPPORTED
DIRECTION_ONLY
UNRESOLVED
```

A null-compatible estimate is not evidence of equivalence.

## Pollinator states

```text
PRESERVED_OR_IMPROVED
IMPAIRED
NO_DETECTED_CHANGE
MIXED
UNRESOLVED
```

`PRESERVED_OR_IMPROVED` cannot be assigned solely because a source failed to reject a pollinator effect.

## Anti-circularity

Architecture coding and outcome coding are stored separately. Architecture files must not contain focal observed-state, effect-size, p-value, or validation-result fields.

## Provenance

Every row must point to an existing, source-adjudicated repository file. New macro-analysis data never overwrite the earlier BITA route ledger, mechanism audits, identification analyses, or manuscript-facing results.
