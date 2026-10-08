# Costa Rica topology–intensity validation first-open result v1

Status: **NOT REPLICATED — HYPOTHESIS KILLED**
Date opened: 2026-10-08
Branch: `analysis/costarica-topology-intensity-decoupling-v1`

## Provenance

- preregistration:
  `empirical/mutualism_attrition/COSTARICA_TOPOLOGY_INTENSITY_DECOUPLING_PREREG_V1.md`
- prereg commit: `446cdbe7bbf834095df455b02639b8b11ca84d10`
- workflow: https://github.com/zuizui0223/bita/actions/runs/37749048428
- artifact id: `11537435513`
- artifact SHA256:
  `5ad45862f3c3e24a729fa972a48c6ccc6212a05458baecbe74464855daa07601`

Costa Rica support:
- 3,006 clean waypoints (A=1,498, B=1,508)
- 8,211 trait-matched zero-inclusive opportunity edges
- 24 hummingbird species
- 132 plant species
- 12 sites
- 2,753 positive and 5,458 zero opportunity edges

## Frozen primary result

| quantity | observed |
|---|---:|
| A->B eligible plants | 88 |
| B->A eligible plants | 85 |
| rho_OX, zero-inclusive occupancy | **-0.04635** |
| rho_FX, total event flux | **+0.11527** |
| rho legitimate flux | **-0.15639** |
| rho robbery flux | **+0.82402** |
| D, Fisher-z occupancy minus flux | **-0.16217** |

The primary prediction required `rho_OX>0`, `rho_FX<0`, and `D>0`.
All three have the opposite sign.

Permutation inference, 99,999 permutations:

~~~text
p(occupancy >= observed) = 0.72781
p(flux <= observed)      = 0.93251
p(D >= observed)         = 0.98948
~~~

Bootstrap 95% intervals:

~~~text
rho_OX: [-0.23911, +0.15056]
rho_FX: [-0.07482, +0.29811]
D:      [-0.32804, +0.00775]
~~~

Frozen classification:

~~~text
NOT_REPLICATED
promotion_eligible = false
~~~

## Prespecified sensitivities

Minimum 10 predictor events:

~~~text
rho_OX = -0.07268
rho_FX = +0.09563
rho legitimate = -0.23462
rho robbery = +0.85615
~~~

Minimum three waypoints per fold:

~~~text
rho_OX = -0.08251
rho_FX = +0.11563
rho legitimate = -0.19822
rho robbery = +0.86629
~~~

Within-site centered ranks:

~~~text
rho_OX = -0.07989
rho_FX = +0.05590
~~~

Thus the failed primary signs are not explained by broad site composition.

## Cross-country result that survives

The topology/intensity hypothesis does not generalize, and the Ecuador weak
total-attrition association also does not generalize. What replicates strongly is
**route replacement**:

~~~text
                     Ecuador          Costa Rica
legitimate flux       -0.162            -0.156
robbery flux          +0.668            +0.824
total flux             -0.042            +0.115
~~~

The route-specific signs are replicated while the total-flux sign changes between
countries.

## Biological implication and boundary

This supports a narrower conclusion:

> Cheating prevalence is a reproducible marker of route replacement, but route
> replacement has no universal implication for total interaction throughput.

The next scientific question is therefore not whether cheating increases or
decreases total visitation universally, but what determines whether robbery
**compensates for** lost legitimate interaction.

Do not promote:
- universal topology–intensity decoupling;
- universal mutualism attrition;
- direct effects on community/species persistence;
- a critique of binary networks based on Ecuador alone.

The independent-country failure is retained as a boundary result.
