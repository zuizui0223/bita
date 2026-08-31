# Kessler-type strict Level-2/3 replication planning receipt v2

## Decision

Strict outcome release is much harder to identify than a positive total interaction when the undefended attraction effect `A0` is near zero.

Registered sufficient rules:

```text
Level 2: upper95(A0) <= 0 and lower95(A1) > 0
Level 3: upper95(A0) <  0 and lower95(A1) > 0
```

Under the continuous normal planning approximation these have the same prospective decision probability for fixed true cell probabilities.

## Boundary scenario

For the historical central planning state

```text
A0 = 0.00
A1 = +0.22
```

the asymptotic maximum joint decision probability is

```text
0.025
```

because the A0 component can satisfy a two-sided 95% upper-bound-at-zero rule with probability at most `alpha/2` when the true value lies exactly on the boundary.

Decision:

```text
TARGET_POWER_NOT_ATTAINABLE_UNDER_STRICT_ZERO_CI_RULE
```

Thus 80% or 90% strict Level-2/3 power cannot be obtained merely by increasing `n` under this true boundary state.

## Negative-A0 sensitivity

These are prospective sensitivity scenarios, not historical effect estimates.

For `A1=+0.22`:

| A0 scenario | joint target | effective n/cell | planned n/cell at DE=1.5, retention=.90 | four-cell total |
|---|---:|---:|---:|---:|
| -0.03 | .80 | 1772 | 2954 | 11816 |
| -0.03 | .90 | 2372 | 3954 | 15816 |
| -0.05 | .80 | 587 | 979 | 3916 |
| -0.05 | .90 | 785 | 1309 | 5236 |

As `A0` approaches zero from below, the strict-release sample requirement increases rapidly. The dominant difficulty is closing the upper bound on `A0`; the positive `A1=+0.22` component is comparatively easy.

## Consequence

The existing Level-1 replication targets of hundreds of observations are valid for `Delta_AD > 0` but are not valid power claims for Level 2/3.

If the scientific target is a strict release claim, the efficient empirical strategy is to prioritize a system or contrast in which the attraction effect without defence is expected to be clearly negative. If the biological target instead permits a practical noninferiority margin `epsilon>0`, that margin must be justified prospectively and the claim must be labelled practical/approximate release rather than strict Level 2.

The historical Kessler aggregate identified-set width of about ±0.03 is not itself a valid post-hoc epsilon justification.

## Provenance

```text
workflow run: 33358087717
source head:  2febf4d0aa8518a73c2c7627c8ddf1b21ff21978
analysis:     kessler_type_replication_power_v2
```
