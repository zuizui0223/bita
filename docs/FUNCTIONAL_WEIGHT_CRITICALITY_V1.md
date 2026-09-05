# Functional-weight criticality v1

## Purpose

This note converts an ecological control variable that changes the relative importance of function 2 into an explicit Chapter-1/Chapter-2 architecture threshold.

Write

```text
a = fixed function-1 weight > 0
b = context-dependent function-2 weight >= 0
lambda = residual coupling >= 0
d = |theta1-theta2|
K = added architecture cost >= 0.
```

Under the quadratic SCH/BITA bridge,

```text
L_S*(b) = a b d^2 / (a+b)

s(b) = a b / [a b + lambda(a+b)]

R(b) = s(b)L_S*(b)
     = a^2 b^2 d^2 /
       [(a+b){a b + lambda(a+b)}].
```

The common architecture margin is

```text
Phi(b) = R(b) - K.
```

## Monotonicity

For `b>0` and `d>0`,

```text
d log R / db
 = a[a b + 2a lambda + 2b lambda]
   / {b(a+b)[a b + a lambda + b lambda]}
 > 0.
```

Thus strengthening function 2 increases the amount of shared-trait compromise that a differentiated architecture could recover under this model.

This does **not** imply that differentiation eventually becomes favored.

## Upper bound

As function-2 weight becomes arbitrarily large,

```text
R_infinity
 = lim_{b->infinity} R(b)
 = a^2 d^2 / (a + lambda).
```

Therefore:

```text
K > R_infinity
-> no amount of function-2 pressure can make differentiation pay.

K = R_infinity
-> the architecture boundary is approached only as b -> infinity;
   there is no finite crossing.

0 < K < R_infinity
-> one unique finite b_crit exists.

K = 0, d > 0
-> b_crit = 0;
   the differentiation boundary collapses onto conflict onset.
```

This yields a stronger statement than "greater conflict promotes differentiation": sufficiently expensive or tightly coupled architectures remain in the BALANCE domain even under arbitrarily strong function-2 pressure.

## Closed-form critical weight

Set `R(b)=K`. Define

```text
A = a^2 d^2 - K(a+lambda).
```

In the finite-crossing regime `A>0`, the positive root is

```text
b_crit
 = a { K(a+2lambda)
       + sqrt[K^2(a+2lambda)^2 + 4K lambda A] }
   / (2A).
```

The other quadratic root is non-positive and is not the biological threshold for `b>=0`.

## Interpretation across the two chapters

From the SCH side, `b` can represent a changing ecological loading of function 2, such as antagonist pressure. The shared optimum moves continuously as `b` changes, and the one-axis conflict load grows toward a finite limit.

From the BITA side, the same change in `b` moves the system toward or away from the common architecture boundary `Phi=0`. The threshold is therefore a **cross-architecture critical context**, not an intrinsic discontinuity inside the SCH one-axis model.

The model partitions context into three regions:

```text
b = 0 (or d=0)
-> no focal conflict load

0 < b < b_crit
-> conflict exists but BALANCE still pays

b > b_crit
-> differentiated architecture pays
```

when a finite `b_crit` exists.

If `K >= R_infinity`, the third region is absent.

## Empirical use

Natural antagonist pressure should not be substituted directly for `b` without calibration. A biological test requires a prospectively declared mapping

```text
e -> b(e)
```

or direct context-specific estimates of the focal functional weighting on a common fitness scale.

The Pedicularis paired critical-context programme can use this result as a prior/model layer, but its final `e_c` comparison still requires the cross-world fitness bridge already registered in `CROSS_WORLD_CRITICALITY_IDENTIFICATION_V1.md`.

## Claim ceiling

This is a closed-form result of the declared quadratic architecture model. It does not establish that natural functional weights are scalar, that `lambda` and `K` remain constant with environment, or that a lineage can evolve the differentiated architecture once the fitness boundary is crossed.
