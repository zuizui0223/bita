# Floral defence selectivity — Stage-2 model gate v1

## Decision

```text
strict Stage-2 n:        3
model decision:          DESCRIPTIVE_EXACT_ONLY
domain vs modality:      NOT IDENTIFIED IN STRICT SET
high-dimensional model: DO NOT FIT
```

The current strict Stage-2 evidence is biologically informative but statistically too sparse for the planned domain-versus-modality model comparison.

## Strict direction-supported subset

Only systems with:

```text
D efficacy = EFFECTIVE
domain = SEPARATED or OVERLAPPED
pollinator state = PRESERVED_OR_IMPROVED or IMPAIRED
```

enter the strict table.

Observed:

```text
                         compatible   impaired
SEPARATED                     2           0
OVERLAPPED                    0           1
```

Two-sided Fisher exact:

```text
p = 0.333333
```

This exact p-value does not negate the directional pattern; it shows that three independent systems cannot support a conventional inferential claim.

## Null-compatible sensitivity

Four additional separated systems have no detected pollinator change, but none provides equivalence-supported preservation.

For a deliberately weaker sensitivity only:

```text
                         compatible-or-null   impaired
SEPARATED                           6              0
OVERLAPPED                          0              1
```

Two-sided Fisher exact:

```text
p = 0.142857
```

This analysis is not promoted to the primary result because:

```text
NO_DETECTED_CHANGE != PRESERVED_OR_IMPROVED
```

## Domain versus chemical/physical cannot yet be tested strictly

The three strict systems are currently:

```text
Thunia        SEPARATED   physical   preserved/improved
Caryopteris   SEPARATED   physical   preserved/improved
Gelsemium     OVERLAPPED  chemical   impaired
```

Therefore domain relation and broad defence modality are perfectly confounded in the strict subset.

Any current claim that:

> domain separation predicts selectivity better than chemical-versus-physical defence

would exceed the data.

The broader null-compatible set contains separated chemical, physical, and reward-access implementations, which is useful biological evidence against a simple physical-only story, but it does not solve the strict inferential comparison.

## Consequence for the paper

The matched-D result should currently be written as:

> **The strict matched systems show a directionally coherent separation-versus-overlap pattern, while additional separated systems are compatible with low pollinator cost; however, the number of direction-supported systems is too small and confounded with defence modality for a formal cross-system moderator test.**

The stronger ecological evidence therefore comes from triangulation with:

1. the 8-system within-D conditionality layer;
2. the independently reanalysed Sakhalkar community network;
3. post-rule systematic-expansion and hold-out evidence.

## Data requirement that would change the decision

The highest-value additions are not arbitrary new papers.

Priority cells:

```text
SEPARATED + chemical + direction-supported pollinator state
OVERLAPPED + physical + direction-supported pollinator state
```

Those systems directly break the current domain-modality confounding.

Second priority:

```text
any additional OVERLAPPED + direct pollinator outcome
any additional SEPARATED + direct direction-supported pollinator outcome
```

Until those cells expand, exact/descriptive analysis is the correct model class.

Machine-readable result:

`results/stage2_model_gate.json`
