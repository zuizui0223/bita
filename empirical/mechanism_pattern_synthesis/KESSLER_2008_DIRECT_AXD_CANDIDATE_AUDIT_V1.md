# Kessler et al. 2008 direct A x D candidate audit v1

## Source

Kessler D, Gase K, Baldwin IT. 2008. Field experiments with transformed plants reveal the sense of floral scents. *Science* 321:1200-1202. DOI `10.1126/science.1160072`.

## Why this source matters

This study is the strongest direct trait-factorial anchor currently recovered for the BITA outcome question. The authors generated four transformed *Nicotiana attenuata* states by blocking the dominant floral attractant benzylacetone (`Nachal1`) and nicotine production (`Napmt1/2`) in all combinations:

```text
EV:   BA present, nicotine present
PMT:  BA present, nicotine suppressed
CHAL: BA suppressed, nicotine present
CP:   BA suppressed, nicotine suppressed
```

The source measured floral visitation, nectar removal, florivory, nectar robbing, female outcross capsule production, and male seed siring in the plant's native habitat.

## Focal-axis mapping

### Attraction axis A

BA has a directly validated floral-attraction role. Candidate mapping:

```text
A = floral benzylacetone emission
```

### Defence/access axis D candidate

Nicotine in floral nectar is a directly validated floral repellent and the source reports reduced florivory and nectar robbing when nicotine is present. Candidate mapping:

```text
D = floral-nectar nicotine / nicotine-associated repellent state
```

This passes the functional-role gate at the floral phenotype level, with an intervention-scope caveat because `Napmt1/2` silencing is systemic.

## Shared-outcome 2 x 2 result

Female outcrossing was measured after antherectomy so capsule maturation required cross-pollination. The article provides these aggregate constraints:

```text
601 antherectomized flowers across five days
127 flowers on a wind-only day -> zero capsules
474 informative flowers on the remaining four days
87 capsules before later losses
A+,D+ EV mean near 35%
A+,D- / A-,D+ / A-,D- means near 12-14%
```

The source-reported rounded range gives a positive descriptive discrete factorial interaction. Earlier sensitivity work placed the probability-scale contrast around +0.19 to +0.25 and the logit interaction around +1.019 to +1.551.

Male fitness also shows joint dependence: across the season EV plants sired 1.9x more seeds than CHAL, 2.2x more than PMT, and 4.7x more than CP. These ratios support a joint reproductive phenotype but are not converted into a common interaction coefficient.

## Registered uncertainty recovery

The previous audit left two actions open: recover Fig. S8A and quantify how much the aggregate constraints alone identify. Both have now been executed.

### Publisher supplement probe

A registered GitHub Actions probe tested five current and legacy Science supporting-material routes. All returned HTTP 403. Exact Fig. S8A day-by-genotype values and the original factorial uncertainty therefore remain inaccessible from the declared public routes.

Receipt: `empirical/identification_design/KESSLER_2008_SUPPLEMENT_ACCESS_RECEIPT_V1.md`.

### Aggregate integer-allocation bounds

A separate registered analysis enumerated integer allocations satisfying the published 474-flower / 87-capsule totals while allowing EV to vary from 34.5–35.5%, each low cell from 11.5–14.5%, and maximum denominator ratios from 1.25 to 3.0.

Across the declared profiles:

```text
feasible allocations per profile:     137,477 to 3,052,260
minimum probability Delta:             +0.1731 to +0.1710
minimum naive probability z:           2.461 to 2.296
minimum logit beta:                     +0.891 to +0.876
minimum logit z:                        1.763 to 1.593
minimum logit CI lower bound:           -0.100 to -0.205
```

Thus the interaction **sign** is robust to every declared aggregate-compatible allocation. Formal uncertainty is not. The logit auxiliary interval can cross zero and modest variance inflation from the unavailable day/plant clustering can erase nominal independent-flower probability significance.

Receipt: `empirical/identification_design/KESSLER_2008_AGGREGATE_BOUNDS_V1.md`.

## Why this is not automatically a strict escape confirmation

Two gates remain.

### 1. Source/design-based uncertainty

The registered aggregate bounds deliberately treat flowers as an auxiliary pooled binomial sensitivity. They do not reproduce the source day-stratified analysis or plant-level clustering. Consequently:

```text
positive aggregate sign:              YES
source/design interval wholly > 0:    NOT ESTABLISHED
```

### 2. Intervention specificity

The focal empirical traits are floral BA and floral/nectar nicotine, but the genetic interventions are not perfectly flower-exclusive. `Napmt1/2` silencing suppresses nicotine biosynthesis systemically. Plant-level consequences outside flowers cannot be excluded from every fitness component.

## Adjudication

The candidate is now promoted beyond a generic high-priority near miss:

```text
independent A manipulation:                    YES
independent D-candidate manipulation:          YES
same 2 x 2 experimental plants:                YES
shared reproductive outcome:                   YES
A role validation:                              STRONG
floral D role validation:                       STRONG
intervention flower specificity:                IMPERFECT / SYSTEMIC-NICOTINE CAVEAT
aggregate discrete A x D sign:                  POSITIVE
aggregate sign robustness:                      ACHIEVED
source/design interaction uncertainty:          UNRESOLVED
current registry state:                         DIRECT_FACTORIAL_SIGN_POSITIVE_FORMAL_UNCERTAINTY_UNRESOLVED
kappa identification:                           NO
```

## Theory-facing interpretation

Kessler 2008 materially changes the outcome-level BITA gap. A true attraction-like axis and a defence/repellent-like axis have been crossed experimentally on the same plants and evaluated on common reproductive outcomes. The positive interaction direction is robust to millions of aggregate-compatible allocations.

What is still not identified is the strict uncertainty-bearing escape decision or its mechanism allocation. The correct ordering is:

```text
manipulated factorial existence:  ACHIEVED
positive aggregate sign:          ACHIEVED
formal source interaction CI:     UNRESOLVED
rho/iota/kappa allocation:        UNRESOLVED
```

## Boundary

```text
discrete 2 x 2 interaction != local mixed partial automatically
aggregate sign robustness != source day-stratified interaction test
floral nicotine function != flower-exclusive genetic intervention
positive total sign != rho/iota/kappa allocation
A x D candidate != kappa
```

## Next action

Do not restart a broad search for the first manipulated A×D surface; it already exists. Target either lawful recovery of Kessler's source-scale uncertainty or an independent manipulated A×D reproductive factorial with complete uncertainty and cleaner floral D scope. Mechanism recovery then requires selective consumer interventions and an independent cost assay.
