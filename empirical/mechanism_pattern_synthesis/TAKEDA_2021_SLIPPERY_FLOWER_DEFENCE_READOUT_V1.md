# Takeda, Kadokawa & Kawakita (2021) — slippery perianths as D→antagonism

## Source

```text
article DOI: 10.1093/aob/mcaa168
plants:      Codonopsis lanceolata; Fritillaria koidzumiana
D axis:      slippery wax-crystal-covered perianth surface
antagonist:  nectar-thieving ants
```

The paper combines surface-structure observations, wax-removal assays and a field manipulation that disables the access barrier by adding a non-slippery bridge around the slippery perianth surface.

## Field barrier-disable experiment

The bridging manipulation is the cleanest synthesis-relevant contrast because it changes antagonist access without redefining the floral trait from an unrelated organ.

### *Codonopsis lanceolata*

```text
bridged / defence bypassed: 43 flowers
control / slippery intact:   40 flowers
flowers receiving ants ≥1 time:
  bridged 28%
  control 10%
source model: binomial GLMM, individual ID random effect
Wald test: P < 0.001
```

### *Fritillaria koidzumiana*

```text
bridged / defence bypassed: 40 flowers
control / slippery intact:   40 flowers
flowers receiving ants ≥1 time:
  bridged 45%
  control 5.1%
source model: binomial GLM
Wald test: P << 0.001
```

The source model analyzes frequencies of ant-present records during repeated field observations. The paper also reports the proportion of flowers that ever received ants. Because the latter percentages are rounded and are not the exact model response, the synthesis does not back-calculate an odds ratio or SE from them.

## Mechanistic chain

The same paper experimentally introduced ants into *C. lanceolata* flowers to establish why excluding ants can matter for the pollination channel. Hornet pollinators remained approximately 6.6 s in ant-present flowers compared with 10.1–10.2 s in controls; the ant-present versus thread-only duration contrast was significant (`P = 0.039`). Pollinator visitation frequency itself did not differ among treatments, and fruit/seed-set effects were not statistically resolved.

Thus the source supports the chain

```text
slippery floral access barrier
  -> less nectar-thief entry
  -> avoidance of an antagonist state that shortens legitimate-pollinator residence
```

but it does not directly estimate `D -> pollination` by manipulating slipperiness while measuring legitimate pollinator use. The second arrow is an antagonist-presence experiment, not a direct D manipulation.

## Evidence classification

```text
D_to_antagonism: direct experimental directional evidence (Tier 4)
D_to_pollination: not directly identified
same-system causal mechanism: strong, but not two of the four marginal trait routes
direct A x D: absent
```

This source is especially valuable because the defence is unambiguously **flower-specific and physical**, rather than inferred from a leaf defence or from a generic secondary metabolite. It broadens the mechanism synthesis beyond nectar chemistry while preserving the outcome and causal-design boundary.
