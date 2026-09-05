# Balance–differentiation critical gap v1

## Result

Overlaying SCH and BITA reveals two distinct thresholds on the shared-conflict-load axis.

### SCH intrinsic conflict onset

```text
C0: L_S* = 0.
```

Above C0, forcing two functions onto one coordinate creates a positive compromise loss.

### BITA architecture-switch threshold

For positive decoupling `s`,

```text
C2: L_S* = K/s.
```

Above C2, the recoverable fraction of the compromise loss exceeds the extra architecture cost.

Therefore, whenever `K>0` and `s>0`, there is a nonzero interval

```text
0 < L_S* < K/s
```

in which

```text
functional conflict exists
+
one-axis compromise is real
+
differentiation is still not worth its cost.
```

This is the **balance-only domain**.

## Critical-gap width

On the conflict-load scale,

```text
Delta_L,critical = C2-C0 = K/s.
```

Thus:

- increasing architecture cost widens the balance-only domain linearly;
- weaker decoupling widens it as `1/s`;
- efficient low-cost decoupling collapses it;
- `s=0, K>0` sends C2 to infinity: no finite conflict load can pay for a completely non-releasing second axis.

## When do the two thresholds coincide?

For finite positive `s`,

```text
C0 = C2
<=> K=0.
```

At zero extra architecture cost, the projected architecture threshold collapses onto conflict onset. Any strictly positive recoverable conflict puts the differentiated architecture on the favourable side, subject to accessibility and the nesting assumptions.

This is a limiting case, not the generic biology.

## Why this matters for the chapter pair

SCH is not merely a preliminary version of BITA. It occupies a genuine parameter region.

```text
no conflict
L_S*=0
    |
    v
BALANCE DOMAIN
0 < L_S* < K/s
    |
    v
CRITICAL SURFACE
L_S*=K/s
    |
    v
DIFFERENTIATION DOMAIN
L_S*>K/s.
```

The dissertation-level transition is therefore not

```text
trade-off present -> differentiation.
```

It is

```text
trade-off present
-> compromise load accumulates
-> recoverable load crosses architecture cost
-> differentiation becomes worthwhile.
```

## Parallel-world extension

The formula above is the shared/null architecture model. In real differentiated systems, the appearance of a second axis may alter the function optima, weights, costs, or ecological interactions themselves. Then the direct BITA critical context can shift away from the SCH-projected context.

Define

```text
Delta_e_c = e_c,D - e_c,S.
```

A nonzero `Delta_e_c` after the cross-world fitness offset has been identified is evidence for **effective parallel-world criticality**: the architecture change modifies the critical landscape rather than merely moving the organism through one fixed landscape.

## Claim ceiling

This gap is an exact consequence of the declared `Phi=sL_S*-K` model. Its numerical width in nature is not identified until `L_S*`, `s`, and `K` are estimated on compatible scales in a paired system.
