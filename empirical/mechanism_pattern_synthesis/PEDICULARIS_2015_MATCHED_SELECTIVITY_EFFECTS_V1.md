# Pedicularis rex 2015 matched defence-selectivity audit v1

## Source and design

Sun S-G, Huang S-Q. 2015. Rainwater in cupulate bracts repels seed herbivores in a bumblebee-pollinated subalpine flower. *AoB PLANTS* 7:plv019. DOI `10.1093/aobpla/plv019`.

The experiment drained rainwater from cupulate bracts and measured legitimate pollinator visits, nectar-robber visits, seed predation, and seed set. One flower-associated physical barrier is therefore tested against multiple consumer/attack modes.

## Source-reported treatment coefficients

The primary article reports the following bract-treatment coefficients and SEs:

```text
pollinator visit rate:  beta +0.012, SE 0.224, P=0.958
nectar robber visit:    beta -0.014, SE 0.225, P=0.951
seed predation:         beta -0.072, SE 0.007, P<0.0001
final seed set:         beta +0.025, SE 0.006, P<0.0001
```

Seed predation increased significantly after water removal in five of six populations. Nectar robbers pierced the corolla above the water and therefore bypassed the barrier, whereas legitimate pollinator visitation was not detectably changed.

## Why these coefficients are not collapsed into one contrast

Although the study reports GLM treatment coefficients for each response, the response variables have different biological meanings, sampling structures, and in the seed-predation analysis a significant site x treatment interaction. Subtracting the coefficients would create a synthetic scale that the source design does not identify.

The valid matched-state readout is instead:

```text
seed-predator attack:  strongly reduced by intact water barrier
nectar-robbing visits: no detected barrier effect
pollinator visits:     no detected barrier effect
final seed set:        higher with intact barrier
```

## Mechanism-first interpretation

This study provides a clean **attack-mode selective guarded-defence** state. The same physical barrier strongly blocks the pre-dispersal seed-predator pathway while failing to block robbers that can bypass the barrier, and it does not detectably suppress legitimate pollinator visitation.

That structure is theory-facing because it shows that the ecological effect of `D` is determined not only by defence magnitude but by whether a consumer's attack path actually intersects the defence.

## Cross-system universality role

Together with the chemically selective Catalpa state and the functional-mode selective Thunia state, Pedicularis supplies an independent physical mechanism for the same higher-level prediction:

> antagonist relief can be preserved without pollinator interference when defence is selective in consumer identity, attack route, access geometry, or visitor function.

The implementations are different, so recurrence is not merely repeated evidence for one compound or one pollinator guild.

## Inference boundary

This study does not estimate `W_AD`, a direct attraction x defence interaction, or `kappa`. The strong seed-predator result cannot be generalized to all antagonist guilds because the same study directly shows a nectar-robber bypass state.

### Adjudication

```text
D -> antagonism seed predators:  quantitative strong support
D -> antagonism nectar robbers:  quantitative null-compatible
D -> pollination visitation:     quantitative null-compatible
selectivity class:               ATTACK_MODE_SELECTIVE
universality role:               MATCHED_SOURCE_MODEL_ANCHOR
formal cross-study moderator:    pending scale-harmonized matched dataset
```
