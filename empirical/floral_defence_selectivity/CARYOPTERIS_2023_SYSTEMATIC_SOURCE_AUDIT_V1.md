# Caryopteris divaricata 2023 systematic-expansion source audit v1

## Source

Tie S, He Y-D, Lázaro A, Inouye DW, Guo Y-H, Yang C-F. 2023.
**Floral trait variation across individual plants within a population enhances defense capability to nectar robbing.**
*Plant Diversity* 45:315-325.
DOI: `10.1016/j.pld.2022.11.002`.

Source checked: open primary full text on 2026-09-18.

## Role in BITA

This is a new **systematic-expansion** system, not a hold-out validation system and not part of the historical derivation set.

The same natural population links:

- corolla tube length;
- nectar robbing intensity;
- legitimate pollinator visitation;
- pollen transfer;
- seed production;
- experimental protection from nectar robbing.

The source explicitly frames floral-trait variation as variation in defence capability against nectar robbing.

## Focal D orientation

For BITA, orient the focal access-filter state as:

```text
higher D = shorter corolla tube / stronger exclusion of the primary robber
```

This orientation is chosen because the primary robber, the larger *Bombus nobilis*, handled short-tubed flowers less efficiently, while the main legitimate visitor *B. picipes* is smaller.

Source morphology:

```text
high-robbing group corolla length: 11.08 ± 0.037 mm
low-robbing group corolla length:  10.29 ± 0.044 mm
group difference: chi-square = 20.55, p < 0.001
```

Within the low-robbing group, robbing rate also increased with corolla length:

```text
chi-square = 10.87, df = 1, p < 0.001
```

## Architecture code

This is not a prospectively coded hold-out, so its architecture code is treated as source-mechanistic rather than confirmatory.

```text
pre_outcome_domain_code = SEPARATED
separating_coordinate   = geometry
defence_modality        = physical/access
mechanistic basis       = body-size / handling-space asymmetry
```

The source reports that short tubes create space limitation for the large primary robber while favoring the relatively smaller legitimate visitor.

## Matched outcomes

Antagonist side:

```text
shorter tubes -> lower robbing intensity
D -> antagonist = effective
```

Pollinator side:

In 2016, legitimate visitation was significantly higher in the low-robbing group than the high-robbing group:

```text
chi-square = 150.20, df = 1, p < 0.001
```

The low-robbing group is the group with shorter corollas.

The source also reports that nectar robbing itself reduced legitimate visitation and seed production.

Critically, when nectar robbers were excluded, legitimate visitation / reproductive differences associated with the floral-trait groups were not maintained. This supports a context-dependent indirect benefit rather than a simple constitutive pollinator attraction effect of short tubes.

## BITA interpretation

The source supports a matched selective-access state:

```text
shorter corolla / stronger robber filter
-> lower antagonist use
-> higher legitimate visitation under natural robbing pressure
-> little trait-associated reproductive difference when robbers are experimentally excluded
```

This is especially valuable because it links floral architecture, antagonist pressure, pollinator behavior, and reproductive consequence in one biological system.

## Boundaries

- natural corolla-length variation is observational, not randomized;
- the low/high robbing groups differ in additional reward traits;
- the mechanistic geometry code is source-supported but not BITA-prospectively blinded;
- this system counts as one independent study cluster;
- it is systematic-expansion evidence and must not be scored as independent hold-out confirmation.

## Adjudication

```text
primary empirical source:        PASS
matched antagonist response:     PASS
matched pollinator response:     PASS
antagonist exclusion component:  PASS
architecture code:               SEPARATED / geometry
Stage-1 route:                   EFFECTIVE
Stage-2 state:                   PRESERVED_OR_IMPROVED in natural robbing context
cohort:                          SYSTEMATIC_EXPANSION
independent cluster count:       1
```
