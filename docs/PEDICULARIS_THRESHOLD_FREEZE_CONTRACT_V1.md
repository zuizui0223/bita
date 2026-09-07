# Pedicularis prospective threshold-freeze contract v1

## Purpose

BITA focal execution requires numerical gates, but those numbers must not be chosen after inspecting the focal `x × y` outcome surface. This contract defines how E0 is frozen before C1-C3 execution.

## Rule

The focal Pedicularis outcome data may not be used to select or relax any of:

```text
min_dimensional_release
min_within_bita_fitness_gain
min_y_function2_gain
max_y_function1_penalty
min_y1_interior_bootstrap_fraction
```

Thresholds must come from pre-focal information with explicit provenance.

## Allowed calibration sources

1. instrument / manipulation resolution measured before the focal outcome analysis;
2. independent pilot data that do not contain the focal confirmatory treatment surface;
3. independent published or SCH-stage measurements on the same biological scale;
4. an explicit design criterion chosen before focal data collection.

The source type, units, value and justification must be recorded for every threshold.

## Required calibration receipt

A freeze input must identify:

```text
system = Pedicularis rex
population_id
season_id
freeze_date
focal_data_inspected = false
calibration_sources[]
thresholds{}
```

Each threshold record contains:

```text
value
unit
source_type
source_reference
biological_interpretation
```

## Scale rules

`min_dimensional_release` is on the SCH reference x-scale after the declared `x_to_sch_multiplier` and `x_to_sch_offset` transform.

`min_within_bita_fitness_gain` is in undamaged mature seeds per focal flower unless the focal contract is prospectively changed before data collection.

`min_y_function2_gain` is an absolute increase in the undamaged fraction of initiated seeds.

`max_y_function1_penalty` is an absolute pollen-grain penalty on the registered function-1 scale; it is an equivalence/tolerance bound, not a nonsignificance rule.

`min_y1_interior_bootstrap_fraction` is a design confidence gate in [0,1].

## Freeze output

The freezer writes a runnable config only if:

```text
focal_data_inspected == false
all five threshold values are finite
required sign/range constraints hold
all provenance fields are non-empty
```

It also records a SHA-256 hash of the calibration receipt. The frozen config must be committed before focal `x × y` outcome analysis.

## Fail closed

Missing provenance, placeholder strings, a claim that focal data have already been inspected, or invalid threshold ranges returns no runnable config.

No default biological thresholds are supplied by the repository. This prevents a software default from becoming an accidental biological claim.
