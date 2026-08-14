# Kessler et al. 2008 direct A x D candidate audit v1

## Source

Kessler D, Gase K, Baldwin IT. 2008. Field experiments with transformed plants reveal the sense of floral scents. Science 321:1200-1202. DOI `10.1126/science.1160072`.

## Why this source matters

This study is substantially closer to the Part I identification target than the previously catalogued agent-factorial and trait-selection near misses.

The authors generated four transformed `Nicotiana attenuata` states by blocking the dominant floral attractant benzylacetone (BA; `Nachal1`) and nicotine production (`Napmt1/2`) in all combinations:

```text
EV:   BA present, nicotine present
PMT:  BA present, nicotine suppressed
CHAL: BA suppressed, nicotine present
CP:   BA suppressed, nicotine suppressed
```

The source measured floral visitation, nectar removal, florivory, nectar robbing, female outcross capsule production, and male seed siring in the plant's native habitat.

## Focal-axis mapping

### Attraction axis A

BA has a directly validated floral-attraction role. Plants lacking BA received fewer hummingbird and hawkmoth visits than BA-producing flowers.

Candidate mapping:

```text
A = floral benzylacetone emission
```

### Defence/access axis D candidate

Nicotine in floral nectar is a directly validated floral repellent and the source reports that nicotine reduces florivory and nectar robbing. Earlier and linked experiments show that nectar nicotine changes visitor handling/removal.

Candidate mapping:

```text
D = floral-nectar nicotine / nicotine-associated repellent state
```

This passes the **functional role** part of the flower-specific D gate at the floral phenotype level.

## Shared-outcome 2 x 2 result

Female outcrossing was measured after antherectomy so capsule maturation required cross-pollination. Across four informative experimental days, the source reports average capsule production of approximately:

```text
A+, D+  (EV):    35%
A+, D-  (PMT):   12-14%
A-, D+  (CHAL):  12-14%
A-, D-  (CP):    12-14%
```

The three transformed states lacking either BA, nicotine, or both were significantly lower than EV.

Using only the source-reported rounded range, the descriptive discrete factorial interaction

```text
Delta_AD = W11 - W10 - W01 + W00
```

lies approximately between +0.19 and +0.25 if all three low states fall inside the reported 12-14% band. A central 13% illustration gives:

```text
0.35 - 0.13 - 0.13 + 0.13 = +0.22
```

This is a **descriptive reconstruction**, not a source-reported interaction coefficient and not a local mixed derivative `W_AD`.

Male fitness also shows joint dependence: across the season EV plants sired 1.9x more seeds than CHAL, 2.2x more than PMT, and 4.7x more than CP. This pattern is compatible with nonadditivity but cannot be converted into a common interaction estimate from the published ratios alone.

## Why it is not automatically promoted to a strict second W_AD cluster

Two identification issues remain.

### 1. Intervention specificity

The focal empirical traits are floral BA and floral-nectar nicotine, but the genetic interventions are not obviously flower-exclusive.

- `Nachal1` is reported as expressed in flowers and leaves, even though BA is operationally treated as the dominant floral attractant.
- `Napmt1/2` silencing suppresses nicotine biosynthesis systemically; nicotine is a whole-plant antiherbivore defence as well as a floral nectar repellent.

Therefore a plant-level fitness difference could in principle contain non-floral consequences of the transformations. The shared-outcome interaction is much closer to the target than a pollinator x herbivore agent factorial, but intervention-level organ specificity is not perfect.

### 2. Published interaction inference

The main article reports genotype means/post-hoc groups rather than an explicit BA x nicotine factorial interaction coefficient with uncertainty. The four cells are present, but a formal uncertainty-bearing interaction must be reconstructed from the supporting/raw data before it can replace the descriptive rounded contrast.

## Adjudication

```text
independent A manipulation:             YES
independent D-candidate manipulation:   YES
same 2 x 2 experimental plants:         YES
shared reproductive outcome:            YES
A role validation:                       STRONG
floral D role validation:                STRONG
intervention flower specificity:         IMPERFECT / SYSTEMIC-NICOTINE CAVEAT
source-reported A x D coefficient:       NO
reconstructable 2 x 2 contrast:          YES, pending exact cell data
current registry state:                  DIRECT_AXD_HIGH_PRIORITY_CANDIDATE
strict W_AD promotion:                   PENDING
kappa identification:                    NO
```

## Theory-facing interpretation

This study materially narrows the U7 field-design gap. It shows that a true attraction-like axis and a defence/repellent-like floral chemistry axis have been crossed experimentally on the same plants and evaluated on shared male/female reproductive outcomes.

The current evidence is compatible with a **positive discrete attraction x nicotine interaction** on female outcross capsule set: the joint A+,D+ state has substantially higher outcross capsule production than any state missing either component.

However, the evidence must not be described as a clean estimate of the local theoretical `W_AD` until the systemic nicotine intervention and exact factorial uncertainty are resolved.

## Boundary

```text
discrete 2 x 2 interaction != local mixed partial automatically
floral nicotine function != flower-exclusive genetic intervention
positive rounded factorial contrast != formal interaction significance
A x D candidate != kappa
```

## Next action

1. Recover Science supporting material / exact day-by-genotype capsule counts if lawfully available.
2. Reconstruct a binomial or day-stratified BA x nicotine interaction with uncertainty.
3. Audit whether transformed lines changed vegetative nicotine/defence in ways capable of contributing to the specific antherectomized-flower outcome.
4. If the shared reproductive contrast remains positive and non-floral confounding is bounded, promote as the second direct A x D cluster with a discrete-factorial label rather than pretending it is a continuous local derivative.
