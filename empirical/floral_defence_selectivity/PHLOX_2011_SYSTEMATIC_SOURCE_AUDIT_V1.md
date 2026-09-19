# Phlox paniculata 2011 matched floral-defence audit v1

## Source

Junker RR, Gershenzon J, Unsicker SB. 2011.
**Floral odor bouquet loses its ant repellent properties after inhibition of terpene biosynthesis.**
*Journal of Chemical Ecology* 37:1323–1331.
DOI: `10.1007/s10886-011-0043-0`.

Source checked from the PubMed record and an accessible full-text copy on 2026-09-18.

## Why it enters the systematic-expansion corpus

The study directly manipulates one flower-specific chemical axis and measures responses from both an antagonist-like floral exploiter and flying flower visitors.

The manipulation uses fosmidomycin and mevinolin to reduce mono- and sesquiterpene biosynthesis in *Phlox paniculata* flowers.

For BITA the focal D axis is:

```text
higher D = intact floral terpene emission / intact ant-repellent scent component
```

This is not inferred from compound identity alone: the experiment directly shows that intact floral odor repels *Lasius niger* ants, whereas terpene-inhibited bouquets lose that repellent function.

## Architecture code

This system was discovered after formulation of the effective-domain rule, so it is not a prospective hold-out.

The source provides a mechanistic consumer-selectivity interpretation:

```text
pre_outcome_domain_code = SEPARATED
separating_coordinate   = susceptibility
defence_modality        = chemical
architecture_code_origin = source_mechanistic_posthoc
```

This code is useful for systematic synthesis but must not be treated as independent preregistered confirmation.

## Antagonist-side result

Natural floral odors were strongly repellent to *Lasius niger*. After inhibition of terpene biosynthesis, the floral bouquet was no longer repellent. The source attributes much of this change to reduced linalool emission.

Thus:

```text
D -> antagonist
status = EFFECTIVE
```

## Pollinator / visitor-side result

The outdoor flower-visitor experiment was dominated by hoverflies (*Episyrphus balteatus*).

Source-reported visitation:

```text
control flowers: 7.96 ± 1.65 visits h-1
terpene-inhibited flowers: 5.71 ± 1.36 visits h-1
t7 = 1.65, P = 0.14
```

Visit duration also did not differ detectably:

```text
control: 13.56 ± 5.51 s
treated: 17.88 ± 6.34 s
t34 = 0.51, P = 0.61
```

This is therefore coded conservatively as:

```text
pollinator/visitor state = NO_DETECTED_CHANGE
uncertainty              = NULL_COMPATIBLE
```

It is **not** coded as equivalence-supported preservation.

## Ecological value

This study adds an experimentally manipulated chemical example to the matched-D corpus:

```text
intact floral terpenes
-> ant repellence
-> no detected change in flying visitor frequency or visit duration
```

It therefore complements the existing physical-access systems without requiring a chemical-versus-physical explanation.

## Boundaries

- The flying visitor assemblage was mainly hoverflies; the study is not a direct seed-set or pollen-transfer experiment.
- A non-significant visitor contrast is not proof of zero pollinator cost.
- Architecture coding is post hoc relative to BITA's rule discovery.
- This publication contributes one independent matched system, not separate replications for visitation and duration.

## Adjudication

```text
primary empirical source:       PASS
flower-specific D manipulation: PASS
same-system antagonist result:  PASS
same-system visitor result:     PASS
Stage-1 route:                  EFFECTIVE
Stage-2 state:                  NO_DETECTED_CHANGE
cohort:                         SYSTEMATIC_EXPANSION
independent cluster count:      1
```
