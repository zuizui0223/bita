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

The bounded direct evidence corpus currently contains:

~~~text
24 independent study programs
16 positive
5 null
1 opposite
2 mixed
~~~

These counts are descriptive and are not a prevalence estimate.

Their value for the model is qualitative: all four direction classes are possible
under one relative-route-cost mechanism. The positive majority is compatible with
many systems lying in the rerouting regime, whereas the retained null, opposite and
mixed studies identify the boundary conditions that an absolute-barrier model would
otherwise treat as failures.

## Stronger ecological conclusion

The supported mechanistic statement is therefore:

> Access constraints reroute exploitation when they penalize the legitimate route
> more strongly than the bypass route. If the bypass route is equally or more
> constrained, rerouting can disappear or reverse.

This is more general than a corolla-length rule and more precise than saying that
barriers simply increase robbery.

## Claim ceiling

This proposition is a mechanistic interpretation and prospective prediction.

The current evidence does not estimate population frequencies of the three regimes.
The direct-study corpus is bounded rather than an exhaustive systematic denominator,
and the standardized cross-network statistic still contains only two independent
networks.
