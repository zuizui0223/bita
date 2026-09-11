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

## Result 3 — explicit switching costs create a persistence / hysteresis band

The static BITA margin `Phi=W_D-W_S` already includes ordinary maintenance costs. Add distinct **one-time** switching costs:

```text
C_SD = shared -> differentiated switching/origination cost
C_DS = differentiated -> shared reversal cost
T    = effective duration over which the current environment persists.
```

Over that horizon, a currently shared system switches only if

```text
T Phi > C_SD,
```

whereas a currently differentiated system switches back only if

```text
-T Phi > C_DS.
```

Therefore both current architectures persist without switching in

```text
-C_DS/T <= Phi <= C_SD/T.
```

The history-dependent band has exact width

```text
Delta_Phi,hyst = (C_SD+C_DS)/T.
```

If `Phi(e)` is locally monotone near the static boundary, first-order environmental width is

```text
Delta_e,hyst
~= (C_SD+C_DS) / {T |dPhi/de|}.
```

Thus:

- switching costs generate genuine path dependence that is absent from the static `K` model;
- longer environmental persistence shrinks the band toward the static `Phi=0` boundary;
- zero switching costs recover the static SCH–BITA architecture threshold exactly.

This result clears the minimum theoretical novelty gate for treating BALANCE persistence as an independent research task, but **not yet** the empirical or manuscript-readiness gate.

## Empirical programme

Phase 1 uses systems with an ordered environmental gradient and independent estimates or calibrated proxies for `L`, `s`, and `K`.

Primary tests:

1. estimate the topology of BALANCE occupancy along `e`;
2. test whether the monotone no-reentry sufficient condition holds;
3. compare `q`, `rho`, `W_e`, and `A_rho` among systems that remain multifunctional versus systems showing differentiated traits;
4. where repeated directional transitions are observable, estimate whether forward and reverse architecture changes occupy distinct environmental brackets as predicted by explicit switching costs.

Peucedanum currently supplies an observational critical bracket but not identified `L`, `s`, and `K` on a common scale. Pedicularis is the cleaner paired causal candidate once SCH and BITA receipts are executed.

## Claim ceiling for dynamics

The switching-cost result is a finite-horizon decision model, not a full population-genetic theory of architectural evolution. `T`, `C_SD`, and `C_DS` must be biologically defined before empirical hysteresis is claimed. Static `K` cannot substitute for either switching cost.

## Standalone novelty gate

The programme now passes the **minimum theory-task gate** because it has:

- a static topology result (monotone no-reentry), and
- a separate dynamic persistence result with explicit switching costs.

It should still be promoted to a separate repository/paper only after at least one stronger gate is met:

- a general topology result beyond the one-dimensional monotone sufficient condition;
- empirical forward/reverse hysteresis or re-entry;
- a resilience statistic with comparative predictive power;
- or a multi-system result showing that balance-domain geometry predicts real architecture persistence.

Until then it remains an incubator and must not enlarge the SCH or BITA claims.

## Registered implementation

`trait_architecture/balance_domain.py` provides the static path analyzer returning:

- pointwise `R`, `Phi`, `q`, and reserve;
- zero crossings;
- topology classification;
- approximate BALANCE width and integrated reserve;
- the monotone no-reentry sufficient-condition flag.

`trait_architecture/balance_domain_dynamics.py` provides the separate finite-horizon switching model returning:

- forward and reverse `Phi` thresholds;
- exact persistence-band width;
- history-dependent stay/switch decisions;
- first-order environmental hysteresis width.

Both implementations fail closed on invalid scales or undeclared architecture states.
