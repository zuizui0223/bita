# C0 layered evidence-capacity readout v1

## Scope

This note records the expected baseline of the C0 diagnostic on the current
committed Part B input files. It is a registry-state statement, not a conclusion
about the full published literature.

## Current registered inputs

```text
primary route-direction records: 13
verified eligible primary numerical effects: 5
configured quantitative compatibility strata: 18
```

The five numerical effects come from the verified effect registry and do not yet
have matching primary route-direction records in `broad_route_records.csv`; C0
therefore retains them as `quantitative_without_directional_record` rather than
dropping or double-counting them.

## Expected C0 output

```text
quantitative effect cells:                 5
directional-only cells:                    13
exploratory synthesis candidate cells:      0
stable synthesis candidate cells:           0
direct interaction identification:          not assessed by marginal-route inputs
recommended primary synthesis:              multilayer evidence map + individual-effect inventory
```

This is the expected output tested in `tests/test_part_b_evidence_capacity.py` and
`tests/test_part_b_pipeline.py`.

## Interpretation

The current database supports a reproducible directional map and individual
quantitative estimates. It does not support a four-arrow pooled meta-analysis or a
direct `A × D` empirical interaction claim. Subsequent source extraction can change
this readout only by adding verified, compatible records; it cannot change it by
relabeling heterogeneous effects as one common stratum.
