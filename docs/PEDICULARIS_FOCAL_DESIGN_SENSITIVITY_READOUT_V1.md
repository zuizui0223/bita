# Pedicularis focal synthetic design sensitivity readout v1

## Purpose

This readout stress-tests the registered `x x y` geometry before focal outcomes exist. It is **not empirical evidence** and is **not a biological power analysis** because the effect size, curvature and noise values are synthetic.

Registered simulator:

```text
scripts/simulate_pedicularis_focal_design_sensitivity.py
empirical/identification_design/PEDICULARIS_FOCAL_DESIGN_SENSITIVITY_CONFIG_V1.json
```

## Synthetic geometry

```text
SCH reference z_ref = 1.0
true y0 optimum     = 0.0
true y1 optimum     = 0.5
true R_state        = 0.5
quadratic curvature = 1.0
y1 peak gain        = 0.2
plant SD            = 0.25
one flower per plant x x-level x y cell
x range             = [-1, 1]
```

Grid:

```text
plants       = 10, 20, 30, 40
x levels     = 5, 7
residual SD  = 0.5, 1.0, 1.5
1000 simulations per cell
```

## Main design result

Under this synthetic geometry, increasing plant replication is more consequential than increasing the x grid from 5 to 7 levels.

At the hardest registered noise level (`residual_sd=1.5`):

```text
                    sign recovery   both optima interior
10 plants, 5 levels      0.951              0.784
20 plants, 5 levels      0.985              0.919
30 plants, 5 levels      0.996              0.953
40 plants, 5 levels      0.998              0.968

10 plants, 7 levels      0.959              0.814
20 plants, 7 levels      0.993              0.920
30 plants, 7 levels      0.999              0.978
40 plants, 7 levels      1.000              0.978
```

The sign of release is therefore relatively easy to recover in this favorable synthetic scenario, whereas stable interior-optimum recovery is the more demanding design target.

## Prospective field implication

This simulation supports the following **design priority**, not a frozen biological threshold:

```text
first protect independent plant replication;
retain >=5 x levels as the minimum registered surface;
use 7 x levels when field capacity allows, especially if curvature or optimum location is uncertain;
do not trade many independent plants for a denser x grid without a pilot-based reason.
```

A practical pre-field target of roughly `>=30 independent plants` is defensible for the current synthetic stress test because it pushes interior-optimum recovery above ~0.95 even at residual SD 1.5 for the 5-level grid. This is not a universal required sample size. The number must be revisited using pilot-only variance and manipulation-feasibility information before confirmatory field execution.

## What this does not justify

The simulation must not be used to:

```text
claim Pedicularis dimensional release;
select E0 biological thresholds after focal outcomes are observed;
replace Stage-G / SCH empirical receipts;
claim 30 plants is sufficient under unknown field variance;
claim the quadratic surface is true in nature.
```

## Next calibration gate

Once a protocol-only or independent pilot supplies plausible variance and x-manipulation fidelity without exposing the confirmatory focal outcome surface, rerun the same grid with those pilot-only nuisance estimates. Freeze the final allocation before the confirmatory `x x y` dataset is inspected.
