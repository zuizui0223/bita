# Direct-design targeted audit v1

## Goal

Search specifically for studies that could close the strongest theory-to-data gaps:

1. direct floral `A x D` estimation on a shared experimental/observational unit;
2. direct joint-cost evidence relevant to `kappa`;
3. factorial mutualist/antagonist studies that are close to, but not equivalent to, the required trait-level design.

The admissibility rule is strict: ecological interaction manipulation, herbivory treatment, or correlational selection on multiple traits is not silently relabelled as a direct `A x D` test.

## Candidate: Helleborus foetidus pollinator × herbivore factorial

Primary source: Herrera et al., field experiment on nonadditive pollinator/herbivore fitness effects (PMCID `PMC139228`).

Design strength:

- two-way factorial weakening of pollinators and flower/fruit herbivores;
- next-generation offspring recruitment measured;
- consistent disordinal pollinator × herbivore interaction reported.

Why it is **not** direct `A x D`:

The study manipulates the strengths of the ecological interactions themselves. It does not independently manipulate a floral attraction trait `A` and a floral defence trait `D` on the same biological unit. The authors explicitly frame pollinator and herbivore exclusion as mimicking hypothetical attraction/defence phenotypes.

Adjudication:

```text
fitness nonadditivity of mutualist and antagonist effects: DIRECT SUPPORT
trait-level A x D mixed partial:                            NOT IDENTIFIED
kappa:                                                       NOT IDENTIFIED
```

Use: contextual validation that nonadditive mutualist-antagonist fitness effects can occur in nature, not a replacement for `W_AD`.

## Candidate: Fragaria vesca full-factorial herbivory × pollination experiment

Primary source: Ramos & Schiestl et al. 2021, Evolution Letters, full-factorial herbivory presence/absence × open/hand pollination.

Design strength:

- direct factorial ecological manipulation;
- nine defence/attraction-related traits measured;
- pollinator- and herbivore-mediated selection can depend on the state of the other interaction;
- conflicting selection detected on inflorescence density.

Why it is **not** direct `A x D`:

The factorial terms are ecological treatments, not independently manipulated attraction and defence traits. Trait selection gradients under different interaction environments are valuable for diffuse/context-dependent selection but do not estimate the trait mixed partial required by the model.

Adjudication:

```text
interaction-context dependence of trait selection: STRONG CONTEXT SUPPORT
shared attraction/defence trait conflict:            SUPPORT
trait-level A x D mixed partial:                      NOT IDENTIFIED
```

## Candidate: Cucurbita floral volatile factorial assays

Primary source: Theis 2007, Journal of Chemical Ecology, DOI `10.1007/s10886-007-9337-7`.

Three floral volatiles were tested in factorial combinations against a specialist pollinator and specialist herbivore. One compound attracted both roles, one only the herbivore, and one only the pollinator; no interactions among the volatiles were detected for attraction.

Why this matters:

This is unusually clean evidence that floral signal components can be role-shared or role-selective. It strengthens `A -> pollination`, `A -> antagonism`, and consumer selectivity.

Why it is **not** direct `A x D`:

The manipulated dimensions are multiple attraction/signal compounds; the study does not establish one manipulated axis as focal defence `D` with an antagonist-reducing function and independently vary it against a distinct attraction trait `A` while measuring plant fitness.

Adjudication:

```text
shared signal tracking:            DIRECT EXPERIMENTAL SUPPORT
consumer-selective signal effects: DIRECT EXPERIMENTAL SUPPORT
direct A x D fitness interaction:  NOT IDENTIFIED
```

## Candidate: Petunia floral blend decomposition

Primary source: Kessler et al. 2013, Ecology Letters, DOI `10.1111/ele.12038`.

Transgenic lines silenced specific floral volatile components. Individual compounds could reduce generalist florivore damage, whereas other components participate in host location/attraction. The work demonstrates that a complex floral blend can contain separable attractive and defensive components.

Why it matters:

This is strong mechanism-level support for modular separation of attraction and defence within a single floral signal blend.

Why it is **not yet** direct `A x D`:

The published design does not provide an independently crossed two-trait attraction × defence manipulation with plant-fitness response required to estimate the theoretical mixed partial.

## Candidate: Nicotiana benzylacetone dual function

Primary source: Kessler et al. 2019, Functional Ecology, DOI `10.1111/1365-2435.13332`.

Benzylacetone is a pollinator-attracting floral volatile and also prevents florivore establishment/damage. BA-silenced flowers suffer more florivore colonization/damage; temporal emission before dusk is sufficient for protection.

Why it matters:

One compound can simultaneously contribute to attraction and defence. This is a strong empirical demonstration that `A`-like and `D`-like biological functions need not be encoded by distinct molecular compounds.

Why it does **not** close the direct `A x D` gap:

A single dual-function compound is one phenotypic axis, not two independently varied trait dimensions. It informs overlap/pleiotropy but cannot identify the cross-partial between separate attraction and defence investments.

## Current direct-design conclusion

The targeted search substantially strengthens the **existence of nonadditivity, diffuse selection, role-shared signals, and modular/dual-function floral chemistry**, but it does not add a second strict direct `A x D` cluster and does not identify `kappa`.

This distinction is scientifically useful rather than merely negative:

> The literature repeatedly tests interaction nonadditivity and attraction/defence overlap, but rarely uses the exact crossed trait manipulation needed to identify the model's attraction × defence mixed partial.

## Updated gap classification

```text
direct A x D strict clusters: 1 (existing Impatiens; sign unresolved)
new strict A x D clusters:    0
direct joint-cost estimates:  0
near-design ecological factorials: >=2 (Helleborus, Fragaria)
shared/dual floral signal designs:  multiple (Cucurbita, Petunia, Nicotiana)
```

### Stop rule for U7/U8

Continue only targeted searching for studies with both of the following:

1. two independently varying/manipulated floral traits that map separately to attraction `A` and flower-specific defence `D`;
2. a shared-unit fitness or compatible reproductive outcome containing the explicit `A:D` interaction.

For `kappa`, require a design that isolates a joint intrinsic/resource cost beyond the ecological mutualist/antagonist pathways. Studies that merely observe lower fitness under combined ecological pressure do not qualify.
