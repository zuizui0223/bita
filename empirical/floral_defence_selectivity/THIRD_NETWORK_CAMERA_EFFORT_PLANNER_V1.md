# Third-network route-blind camera-effort planner v1

## Purpose

The prospective third network already freezes the biological eligibility gates:

~~~text
minimum confirmatory units = 30
minimum mammal species     = 5
minimum plant species      = 5
planning target units      = 70
~~~

What was missing was a route-blind way to choose a **fixed camera-effort rule**
before confirmatory route outcomes are opened.

Use:

- `empirical/floral_defence_selectivity/THIRD_NETWORK_CAMERA_EFFORT_RATE_SCHEMA_V1.csv`
- `scripts/plan_third_network_camera_effort.py`

## Input boundary

The planner accepts exactly four columns:

~~~text
site_id
plant_species
mammal_species
route_blind_detection_rate_per_camera_hour
~~~

It rejects route outcome and access-geometry fields. In particular, the effort
planner cannot ingest:

- L/B route codes;
- bypass or robbery proportions;
- B/L counts;
- floral access depth;
- mammal reach;
- access mismatch (M);
- confirmatory (Y=B/(B+L)).

The final site/plant pool must already have been selected under the route-blind
presurvey gate.

## Uniform-effort rule

The planner never allocates more effort to a particular plant or mammal because
of its expected route response.

For each candidate effort level (h):

~~~text
every retained plant x site receives h camera-hours
~~~

The rate table is used only to estimate whether that **same uniform h** is likely
to recover enough mammal x plant x site units.

## Planning model

For candidate unit (i):

~~~text
lambda_i = route-blind mammal detection rate per camera-hour
q        = predeclared qualifying fraction
lambda_i* = lambda_i q
~~~

The planner treats classifiable-event arrival as a Poisson planning
approximation. It draws one exponential waiting time per simulation and
candidate unit.

The same waiting-time draws are reused across the complete hours grid, so
coverage is exactly monotone with increasing effort within a simulation.

## Qualifying fraction

`qualifying_fraction` is **not** estimated from confirmatory B/L outcomes.

It is a planning sensitivity parameter representing the fraction of route-blind
detections expected to become usable classifiable feeding events.

Recommended development use is to run a sensitivity grid, for example:

~~~text
q = 0.25
q = 0.50
q = 0.75
~~~

and freeze the camera rule before confirmatory route videos are opened.

Do not choose q after inspecting the confirmatory route distribution.

## Outputs

For every uniform camera-hour value the planner reports:

- probability of passing the frozen 30-unit / 5-mammal / 5-plant minimum;
- probability of reaching the 70-unit planning target while retaining richness;
- mean / median / 10th / 90th percentile realized units;
- total equivalent camera-hours;
- optional approximate elapsed hours for a specified number of cameras.

The first effort level reaching the predeclared planning-success probability is
returned as `recommended_uniform_effort`.

## Structural failure

If the route-blind candidate pool itself contains fewer than 70 positive-rate
visitor x plant x site units, the planner returns:

~~~text
PLANNING_TARGET_STRUCTURALLY_IMPOSSIBLE
~~~

Increasing camera hours cannot repair a structurally undersized candidate pool.

That status is a design result, not a biological access-routing result.

## Example

~~~bash
python scripts/plan_third_network_camera_effort.py \
  route_blind_rates.csv \
  camera_effort_plan.json \
  --hours-grid 24,48,72,96,120,168,240,336 \
  --qualifying-fraction 0.50 \
  --simulations 10000 \
  --target-success-probability 0.80 \
  --camera-count 10
~~~

## Claim boundary

This planner does not compute (M), (Y), (r_T), or (r_{J3}).

It exists only to freeze a non-outcome-adaptive camera-effort rule before the
confirmatory third-network dataset is opened.
