# Balance-domain ecology — standalone programme v1

## Status

Cross-project incubator. **Not in the SCH or BITA manuscript scopes.**

The programme exists only if the interior of the BALANCE regime has structure that is not exhausted by the inequality `0<L_S*<K/s`.

## Separation from the two chapters

```text
SCH
fixed shared architecture
-> where does compromise settle?

BALANCE-DOMAIN PROGRAMME
both architectural alternatives are conceptually available
but the shared architecture still wins
-> how broad, resilient, connected, and persistent is that regime?

BITA
alternative axes are present/available
-> when does differentiation win, and why?
```

The third programme therefore studies the **interior geometry and persistence of the compromise regime**, not either boundary estimand itself.

## Static state variable

Let

```text
L(e) = shared-axis conflict load
s(e) = recoverable fraction / decoupling
K(e) = added architecture cost
R(e) = s(e)L(e)
Phi(e) = R(e)-K(e).
```

For positive conflict,

```text
Phi < 0 -> BALANCE
Phi = 0 -> architecture critical surface
Phi > 0 -> DIFFERENTIATION.
```

For `K>0`, define the dimensionless position inside BALANCE

```text
q(e)=R(e)/K(e),     0<q<1,
```

and the critical reserve

```text
rho(e)=K(e)-R(e)>0.
```

`q` compares systems with different absolute fitness units only after `R` and `K` have been identified on a compatible scale.

## Domain-level observables

For an ordered environmental control axis `e`:

```text
W_e   = total environmental width occupied by BALANCE
A_rho = integral of positive critical reserve across e
N_B   = number of connected BALANCE intervals
N_0   = number of Phi=0 crossings.
```

These are domain properties rather than SCH or BITA point estimands.

## Result 1 — monotone no-reentry condition

Assume along increasing `e`:

```text
L(e) is nondecreasing,
s(e) is nondecreasing,
K(e) is nonincreasing,
```

with all three non-negative. Then

```text
Phi(e)=s(e)L(e)-K(e)
```

is nondecreasing. Therefore `Phi` can cross zero at most once.

Consequences:

- BALANCE is a single connected interval (possibly empty or extending to the end of the observed path);
- once DIFFERENTIATION becomes favourable, BALANCE cannot re-enter;
- an observed BALANCE→DIFFERENTIATION→BALANCE sequence falsifies at least one of the monotonicity conditions or the common-scale static model.

This is the first result that makes the balance domain more than the algebraic gap `0<L_S*<K/s`.

## Result 2 — what re-entry implies

Under the same common fitness scale, re-entry requires at least one of the following along the environmental trajectory:

- effective conflict load falls,
- effective decoupling falls,
- architecture cost rises,
- or the mapping itself changes so that the single-world `Phi=sL-K` representation no longer applies.

The last case connects directly to BITA's registered parallel-world criticality.

## Empirical programme

Phase 1 uses systems with an ordered environmental gradient and independent estimates or calibrated proxies for `L`, `s`, and `K`.

Primary tests:

1. estimate the topology of BALANCE occupancy along `e`;
2. test whether the monotone no-reentry sufficient condition holds;
3. compare `q`, `rho`, `W_e`, and `A_rho` among systems that remain multifunctional versus systems showing differentiated traits.

Peucedanum currently supplies an observational critical bracket but not identified `L`, `s`, and `K` on a common scale. Pedicularis is the cleaner paired causal candidate once SCH and BITA receipts are executed.

## Phase 2 — dynamic persistence

Do not infer hysteresis from the static model. A separate dynamic model must distinguish at least:

```text
maintenance cost of the differentiated architecture,
origination/switching cost shared -> differentiated,
reversal cost differentiated -> shared.
```

Only then can distinct forward and reverse thresholds, path dependence, or hysteresis be claimed.

## Standalone novelty gate

This programme warrants a separate repository/paper only if it produces at least one of:

- a general topology theorem beyond the monotone result above;
- a dynamic hysteresis theorem with explicit switching costs;
- a useful resilience statistic with comparative predictive power;
- or a multi-system empirical result showing that balance-domain geometry predicts real architecture persistence.

Until then it remains an incubator and must not enlarge the SCH or BITA claims.

## Registered implementation

`trait_architecture/balance_domain.py` provides an incubator path analyzer returning:

- pointwise `R`, `Phi`, `q`, and reserve;
- zero crossings;
- topology classification;
- approximate BALANCE width and integrated reserve;
- the monotone no-reentry sufficient-condition flag.

The implementation fails closed on negative conflict/cost, invalid decoupling, or unordered environmental contexts.
