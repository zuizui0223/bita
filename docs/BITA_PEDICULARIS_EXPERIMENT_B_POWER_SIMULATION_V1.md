# Pedicularis Experiment-B power simulation v1

## Purpose

Power the single `x × water-y` experiment that is shared by Chapter 2 / BALANCE and Chapter 3 / BITA.

The design being powered is:

```text
>=5 exsertion x levels
x 2 water-y states
= >=10 cells
```

The same raw surface supplies:

```text
BALANCE
  direct W_S* versus W_D*
  direct Delta_W sign / interval

BITA
  x0*, x1*
  R_state
  y preferential loading
  optimum fitness gain
  released-surface interior support
```

## Why both BALANCE and BITA scenarios are simulated

The second axis can produce some dimensional release while the optimized differentiated-accessible worldline still remains below the shared worldline. That is a genuine Chapter-2 BALANCE scenario, not a failed BITA experiment.

Therefore `target_worldline_state` is prospectively frozen as either:

```text
BALANCE
BITA
```

and the power simulator asks whether the 95% interval of the production optimum-fitness gap resolves the intended side:

```text
BALANCE: upper bound < 0
BITA:    lower bound > 0.
```

## Production pipeline

For each candidate number of independent plant clusters per cell:

1. simulate one complete x-by-y raw dataset from frozen pilot parameters;
2. run `scripts/analyze_pedicularis_dimensional_release.py` unchanged;
3. score release, preferential loading and released-surface interior gates from the production receipt;
4. score the direct worldline order from the production bootstrap interval of `within_bita_optimum_fitness_gain`;
5. repeat and report gate-specific and joint power.

The current v1 generator is a balanced complete-block planning model: each independent plant contributes one focal flower to every x-by-y cell. If the field design is incomplete-block, extend the generator before accepting an n recommendation.

## Generating inputs

The fail-closed template freezes, from pilot data or explicit sensitivity scenarios:

- x levels;
- SCH state-specific pollination-facing and combined references;
- y0/y1 fitness optima, peaks and curvatures;
- plant and residual variation;
- damaged-seed distributions under y0/y1;
- pollen-response curve and any y cross-effect;
- water-depth separation and manipulation damage;
- all production BITA thresholds.

Do not tune these parameters after viewing a preferred sample-size result.

## Output

For each candidate n:

```text
release_gate_power
preferential_loading_power
released_surface_interior_power
direct_worldline_order_power
joint_primary_gate_power
registered_bita_positive_gate_power
analysis_failure_fraction
```

`joint_primary_gate_power` deliberately differs by the registered worldline scenario only through direct order. A BALANCE scenario may have positive release/loading while total optimized fitness still favours the shared state.

## Claim ceiling

This is planning analysis only. It neither establishes a BALANCE middle world nor a BITA differentiated state until the real Experiment-B data pass the corresponding production gates on the frozen SCH context and fitness scale.
