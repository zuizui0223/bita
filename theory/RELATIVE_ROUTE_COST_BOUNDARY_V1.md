# Relative-route-cost boundary for access-induced exploitation routing v1

## Claim

The routing prediction is not that larger or longer flowers universally receive more
nectar robbery.

The minimal mechanistic object is the **relative cost of the legitimate route versus
the bypass route**.

Let

~~~text
C_L(x) = cost of using the legitimate route under trait state x
C_B(x) = cost of using the bypass route under trait state x
~~~

and let the consumer choose between the two routes.

Define the relative legitimate-route disadvantage

~~~text
D(x) = C_L(x) - C_B(x).
~~~

If rewards and all non-geometric route utilities are held fixed, any smooth
two-route choice model in which higher route utility increases use implies

~~~text
bypass propensity increases with D(x).
~~~

For a logistic choice model,

~~~text
logit P(B | x) = alpha + beta [C_L(x) - C_B(x)],   beta > 0.
~~~

Therefore

~~~text
d logit P(B | x) / dx
    = beta [dC_L/dx - dC_B/dx].
~~~

The sign of the geometry–robbery association is consequently determined by the
**difference in how strongly the trait constrains the two routes**, not by the
absolute magnitude of the trait.

## Three regimes

### 1. Rerouting regime

~~~text
dC_L/dx > dC_B/dx
~~~

The trait disproportionately makes legitimate access harder. Bypass becomes
relatively more attractive.

Prediction:

~~~text
geometry -> robbery association = POSITIVE
~~~

Examples compatible with this regime include long-corolla / short-reach mismatches
and experimental corolla shortening.

### 2. Neutral-routing regime

~~~text
dC_L/dx ~= dC_B/dx
~~~

The trait changes both route costs similarly, or geometry is not the limiting
component of route choice.

Prediction:

~~~text
geometry -> robbery association = NULL
~~~

This accommodates direct nulls without abandoning the routing mechanism.

### 3. Bypass-hardening regime

~~~text
dC_L/dx < dC_B/dx
~~~

The trait makes bypass disproportionately difficult, or increases a component of
the barrier that the bypass route must itself overcome.

Prediction:

~~~text
geometry -> robbery association = OPPOSITE
~~~

A trait can therefore be a genuine access barrier while reducing robbery.

## Mixed systems

If route costs depend on context z,

~~~text
D(x,z) = C_L(x,z) - C_B(x,z),
~~~

then the same trait can have different signs across morphs, sites, visitor guilds or
other contexts:

~~~text
sign[dD/dx] changes with z -> MIXED result.
~~~

Thus mixed studies are not necessarily noise. They can identify a change in which
route is more strongly constrained.

## General utility form

If legitimate and bypass rewards also change with x, define

~~~text
U_L = R_L - C_L
U_B = R_B - C_B
~~~

and

~~~text
logit P(B | x) = alpha + beta (U_B - U_L).
~~~

Then

~~~text
d logit P(B | x) / dx
  = beta [
      d(R_B - R_L)/dx
      + d(C_L - C_B)/dx
    ].
~~~

The geometry-only prediction is therefore strongest when reward differences are
held fixed or measured separately. This is why experimental manipulations of access
geometry with constant reward are particularly diagnostic.

## Connection to the current evidence

The frozen outcome-blind OpenAlex frame currently resolves:

~~~text
33 independent direct study programs
22 positive
5 null
4 opposite
2 mixed
~~~

These counts are a finite provider-defined evidence distribution, not a prevalence
estimate or pooled effect.

Their value for the model is qualitative: all four direction classes are possible
under one relative-route-cost mechanism. The positive programs are compatible with
rerouting, whereas null, opposite and mixed programs identify boundary conditions
that an absolute-barrier rule would otherwise treat as failures. A post hoc audit
found direct bypass-hardening evidence in two opposite programs; because those cases
were selected after direction coding, this is mechanism partitioning rather than an
independent prediction test.

## Stronger ecological conclusion

The supported mechanistic statement is therefore:

> Access constraints reroute exploitation when they penalize the legitimate route
> more strongly than the bypass route. If the bypass route is equally or more
> constrained, rerouting can disappear or reverse.

This is more general than a corolla-length rule and more precise than saying that
barriers simply increase robbery.

## Evidence ladder

The present evidence supports four nested claims at different strengths:

1. **Observed recurrence:** stronger constraint on the legitimate route is associated
   with greater bypass use in two independently assembled bird and insect networks.
2. **Relational routing:** the Ecuadorian signal persists within bird species, so the
   pattern is not reducible to fixed differences among consumer species.
3. **Mechanistic interpretation:** relative route cost unifies positive, null,
   opposite and mixed directions, but bypass cost has not yet been independently
   manipulated in the network datasets.
4. **General principle:** route choice should respond to relative, not absolute,
   access cost across other ecological systems. This remains a prospective
   prediction rather than an established universal law.

## Decisive prospective falsification

A direct test should manipulate the two route costs independently while holding
reward constant:

~~~text
raise C_L, hold C_B fixed      -> bypass increases
hold C_L fixed, raise C_B      -> bypass decreases
raise C_L and C_B similarly    -> little route-composition shift
~~~

The third outcome is especially diagnostic because an absolute-barrier model predicts
suppression from a stronger barrier, whereas the relative-route-cost model predicts
little rerouting if both routes are penalized similarly. A factorial manipulation can
therefore prospectively generate positive, null and opposite signs rather than
classifying them after observation.

### Implemented prospective test

The causal test is now implemented before outcome collection in:

- `empirical/floral_defence_selectivity/RELATIVE_ROUTE_COST_FACTORIAL_PREREG_V1.md`;
- `empirical/floral_defence_selectivity/RELATIVE_ROUTE_COST_CALIBRATION_SCHEMA_V1.csv`;
- `empirical/floral_defence_selectivity/RELATIVE_ROUTE_COST_FACTORIAL_EVENT_SCHEMA_V1.csv`;
- `empirical/floral_defence_selectivity/RELATIVE_ROUTE_COST_FACTORIAL_FREEZE_TEMPLATE_V1.json`;
- `scripts/validate_relative_route_cost_calibration.py`;
- `scripts/analyze_relative_route_cost_factorial.py`.

Stage 0 calibrates the high-minus-low cost increments for the two routes with
route-isolated flowers. Stage 1 then uses a randomized 2 x 2 route-choice experiment.
The protocol is implemented but no confirmatory route-choice data have been opened.

## Claim ceiling

This proposition is a mechanistic interpretation and prospective prediction.

The current evidence does not estimate population frequencies of the three regimes.
The direct-study corpus is bounded rather than an exhaustive systematic denominator,
and the standardized cross-network statistic still contains only two independent
networks.
