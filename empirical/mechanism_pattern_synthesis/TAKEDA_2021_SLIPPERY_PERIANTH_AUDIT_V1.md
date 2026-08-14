# Takeda et al. 2021 slippery-perianth floral-defence audit v1

## Source

Takeda K, Kadokawa T, Kawakita A. **Slippery flowers as a mechanism of defence against nectar-thieving ants.** *Annals of Botany* 127:231–239. DOI `10.1093/aob/mcaa168`.

The primary article is open access (PMCID `PMC7789111`).

## Floral-D definition

The corolla of *Codonopsis lanceolata* and tepals of *Fritillaria koidzumiana* possess slippery epicuticular-wax surfaces that prevent ants from entering exposed-nectary flowers.

```text
D = slippery wax-covered perianth surface
antagonist = nectar-thieving ants
```

Hexane wiping removed wax crystals and slipperiness in behavioural assays. The field test bypassed the slippery surface using non-slippery bridges rather than treating ant presence itself as the floral defence.

## Direct field D -> antagonism evidence

Artificially bridging the slippery surfaces increased the fraction of flowers receiving ants:

```text
Codonopsis lanceolata
control flowers ever receiving ants: ~10%
bridged flowers:                     ~28%
GLMM Wald test: P < 0.001

Fritillaria koidzumiana
control:  ~5.1%
bridged: ~45%
GLM Wald test: P << 0.001
```

Thus the physical floral surface itself prevents ant access in two plant species.

Pattern state:

```text
D -> antagonism: protective
```

Both plant species remain one publication/study cluster for independence counting in the current expansion.

## Downstream pollinator pathway

The same article separately introduced live ants into *C. lanceolata* flowers to test why excluding ants could matter for pollination.

Across 269 analysable pollinator visits:

```text
ant-present flowers: mean visit duration ~6.6 s
thread-only control:                ~10.1 s
untreated control:                  ~10.2 s
ant-present vs thread-only: P = 0.039
ant-present vs untreated:   P = 0.16
```

Visitation frequency did not differ among treatments, and fruit/seed set differences were unresolved.

This establishes:

```text
D blocks nectar-thieving ants
ants can shorten pollinator handling/visit duration
```

but it does **not** directly estimate `D -> pollination`, because the pollinator experiment manipulates ant presence rather than the slippery surface itself.

## Theory-facing mapping

Admitted:

```text
physical floral defence by surface microstructure recurs in independent lineages
an antagonist-reducing D can protect a pollinator-use pathway indirectly by excluding antagonists
floral surfaces can spatially filter small antagonists while large legitimate pollinators bypass the slippery zone
```

Not admitted:

```text
ant-introduction effect = D -> pollination coefficient
6.6 vs 10.1 s = iota
fruit-set null = no pollination cost
wax slipperiness = attraction A
this study estimates W_AD
```

## Context value

The article provides a spatial filtering mechanism: large pollinating hornets can stride over the slippery portion and use a non-slippery foothold near the nectaries, whereas small ants cannot. This is another consumer-body-size/access-mode context for floral defence.

## Current adjudication

```text
primary full text:              PASS
flower-specific D:              PASS
experimental D manipulation:    PASS
D -> antagonism:                PASS
downstream ant -> pollinator:   PASS as context pathway
D -> pollination:               NOT DIRECTLY IDENTIFIED
direct A x D:                   NO
```

### Decision

**PROMOTE_D_TO_ANTAGONISM_TO_ROUTE_LEDGER; PROMOTE_ANT_TO_POLLINATOR_LINK_TO_CONTEXT_LAYER**
