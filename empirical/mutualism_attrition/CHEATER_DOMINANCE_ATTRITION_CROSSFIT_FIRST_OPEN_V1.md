# Cheater-dominance attrition cross-fit first-open receipt v1

Status: **FROZEN PRIMARY OUTCOME OPENED; FORMAL SIGN GATE PASSES, EVIDENCE STRENGTH WEAK**
Date: 2026-10-08
Branch: `analysis/cheater-dominance-attrition-crossfit-v1`

## Provenance

- preregistration commit: `d72bce0cd51c8d302affbdc618582b9fe10a359b`
- successful outcome run: https://github.com/zuizui0223/bita/actions/runs/37748167575
- run head: `20818bcfd86856a535375a87b5bfc470b6aa8210`
- artifact id: `11536133533`
- artifact digest: `sha256:3ed0da00fc47818bccce18698bc3b077ba841a13de2f75d335cf59092d573457`
- analysis script: `scripts/analyze_cheater_dominance_attrition_crossfit.py`
- permutations: 99,999; seed 20261007
- species bootstrap: 9,999
- clean waypoints: 5,254 (A=2,615; B=2,639), assigned by frozen FNV1a32 rule.

The first workflow attempt failed before reading an outcome because of a Python import-path
error. Only the import path was fixed; no scientific parameter, filter, split,
threshold, endpoint or decision rule changed.

## Primary cross-fit result

Predictor: robbery share from one waypoint fold.
Response: total route-resolved feeding events per clean camera-hour in the disjoint
fold.

| Direction | eligible plants | rho total | rho legitimate | rho robbery |
|---|---:|---:|---:|---:|
| A -> B | 168 | -0.01233 | -0.12188 | +0.65986 |
| B -> A | 170 | -0.07242 | -0.20067 | +0.67680 |
| equal-fold Fisher-z | — | **-0.04242** | **-0.16153** | **+0.66841** |

Primary total-flux inference:

~~~text
rho_X = -0.0424157
one-sided permutation p = 0.21915
two-sided permutation p = 0.43765
bootstrap 95% interval = [-0.17133, +0.08698]
~~~

Thus the predeclared *direction* is reproduced independently in both split directions,
but the total-flux association is small and statistically weak.

## Frozen promotion rule

The preregistered sign-based rule evaluates to:

~~~text
eligible directional n                    = true
rho_X(total) < 0                          = true
both directional total rho < 0            = true
rho_X(legitimate) < rho_X(robbery), < 0   = true
min-10-event sensitivity rho_X < 0         = true
formal promotion_gate_pass                 = true
~~~

This formal pass must **not** be confused with strong evidence. The preregistration
explicitly states that the permutation p-value measures evidence strength and is not
the sole promotion gate; the observed p=0.219 and CI spanning zero cap the claim.

## Prespecified sensitivities already opened

### Minimum 10 predictor events

~~~text
A -> B total rho = -0.07288
B -> A total rho = -0.13574
rho_X total      = -0.10441
rho_X legitimate = -0.22652
rho_X robbery    = +0.68992
~~~

The sign therefore survives the frozen >=10-event sensitivity.

### >=3 clean waypoints per fold

~~~text
A -> B total rho = +0.00927
B -> A total rho = -0.09162
rho_X total      = -0.04128
rho_X legitimate = -0.18200
rho_X robbery    = +0.72459
~~~

The equal-fold sign remains negative but one directional total-flux effect is slightly
positive.

### Hummingbird-only

~~~text
A -> B total rho = +0.00268
B -> A total rho = -0.07349
rho_X total      = -0.03546
rho_X legitimate = -0.15344
rho_X robbery    = +0.67109
~~~

Again, the equal-fold sign is negative while one direction is essentially zero.

### Explicit yes/no piercing only

~~~text
A -> B total rho = -0.15288
B -> A total rho = -0.23440
rho_X total      = -0.19398
rho_X legitimate = -0.39476
rho_X robbery    = +0.59970
~~~

The pattern is stronger when ambiguous/blank piercing codes are not recoded.

### Flower-hour sensitivity

No plant passed the preregistered requirement that all contributing outcome waypoints
have complete positive flower-count effort; this sensitivity is unavailable and is not
replaced.

## Current biological interpretation

The strongest replicated pattern is **route persistence**, not yet total mutualism
collapse:

- plants with high cheating share in one independent camera subset have substantially
  higher robbery flux in another subset;
- the same plants tend to have lower legitimate flux in the independent subset;
- these opposing components largely cancel in total flux, producing only a weak
  negative total-throughput association.

This means the data clearly distinguish a persistent route-composition phenotype from
a strong throughput-attrition result.

## Next locked work

Before manuscript promotion, complete the still-prespecified:
1. zero-inclusive opportunity response;
2. mismatch-conditioned residual cross-fit;
3. within-site centered-rank sensitivity.

These are diagnostics of whether the weak total-flux effect is ecological attrition
beyond morphology and site composition, versus stable plant-specific routing.

## Claim ceiling

Allowed now:
> Cheating prevalence estimated from one independent sampling subset strongly predicts
> route composition in another subset, with more robbery flux and less legitimate flux.

Not yet allowed:
> High cheating prevalence predicts lower total interaction flux.

The latter remains directionally compatible but weak under the primary cross-fit.
