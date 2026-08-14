# Kessler, Bing, Haverkamp & Baldwin (2019) — defensive function of benzyl acetone

## Source identity

```text
article DOI: 10.1111/1365-2435.13332
plant:       Nicotiana attenuata
focal trait: benzyl acetone (BA), a floral volatile
mutant:      CHAL — floral BA emission silenced
control:     EV — empty-vector control emitting BA
public data: EDMOND DOI 10.17617/3.24, declared by the article
```

## Role assignment

BA is a **dual-function single floral trait**. Prior work in this system establishes its pollinator-attracting role, while this study experimentally tests a defensive function against floral herbivory.

This architecture is important for the synthesis but must not be transformed into a direct `A x D` record: one volatile molecule does not create two independent trait axes simply because it has two ecological functions.

The eligible route here is therefore:

```text
BA defensive expression -> floral antagonist colonization / damage
```

## Field evidence reported by the article

The paper compares BA-silenced CHAL and BA-emitting EV plants across multiple field seasons:

```text
2011
  CHAL: 52.9% infested
  EV:   17.6% infested
  Fisher exact P = 0.035

2014
  CHAL: 37.1% infested
  EV:   10.3% infested
  Fisher exact P = 0.013

2016
  CHAL: 23.1% infested
  EV:    0.0% infested
  Fisher exact P = 0.098
```

The same direction appears across years: removing BA increases colonization by the chrysomelid florivore *Diabrotica undecimpunctata*. The source also reports greater floral damage on CHAL plants.

## Deposited Figure-1 reconstruction

The article-declared EDMOND repository contains the workbook:

```text
FIGURE 1. Diabrotica presence 2011. 2014. 2016.xlsx
```

A preregistered reconstruction reads the plant-level `presence` outcome in memory and writes only aggregate 2 x 2 tables. The field seasons are repeated observations inside one study cluster, not independent studies.

### 2011

```text
EV:    3 infested / 14 not infested, n=17, 17.65%
CHAL:  9 infested /  8 not infested, n=17, 52.94%

log odds ratio, EV versus CHAL = -1.658
SE                               =  0.801
95% CI                           = [-3.227, -0.089]
one-sided Fisher, EV < CHAL      =  0.03536
two-sided Fisher                 =  0.07073
```

The deposited proportions reproduce the article exactly. The article's `P=0.035` is also reproduced by the directional one-sided Fisher test.

### 2014 — source/deposit discrepancy

The deposit contains:

```text
EV:    4 infested / 25 not infested, n=29, 13.79%
CHAL: 13 infested / 22 not infested, n=35, 37.14%

log odds ratio, EV versus CHAL = -1.306
SE                               =  0.642
95% CI                           = [-2.565, -0.048]
one-sided Fisher, EV < CHAL      =  0.03261
two-sided Fisher                 =  0.04780
```

The article instead reports `EV=10.3%` and `P=0.013`. With `n=29`, 10.3% corresponds exactly to 3 infested EV plants. The table

```text
EV:    3 / 26
CHAL: 13 / 22
```

would yield a one-sided Fisher probability of approximately `0.01317`, reproducing the article.

A second bounded structural audit was therefore performed before any effect was promoted. It found:

```text
2014 worksheet rows below the header: 64
column B: 64 nonempty entries, text values only EV / CHAL, header blank
column C: plant number, 64 numeric entries
column D: number of beetles, 64 numeric entries
column E: presence 0/1, 64 numeric entries
additional exclusion / omission / note column: none
```

Thus there is no source-justified rule in the deposited table for deleting one of the four EV-positive rows. No row is silently removed to force agreement with the article.

This is classified as a **source–deposit discrepancy**: the published 2014 percentage/P value imply one fewer infested EV plant than the deposited Figure-1 table.

### 2016

```text
EV:    0 infested / 14 not infested, n=14, 0.0%
CHAL:  3 infested / 10 not infested, n=13, 23.08%

Haldane-corrected log odds ratio = -2.269
SE                                =  1.565
95% CI                            = [-5.337, +0.799]
Fisher exact P                    =  0.09778
```

The deposited proportions and Fisher test reproduce the article's `0%`, `23.1%`, and `P=0.098`.

## Study-level quantitative status

The deposited-data reconstruction gives a descriptive repeated-season summary:

```text
all three deposited seasons
  inverse-variance log OR = -1.521
  SE                      =  0.477
  95% CI                  = [-2.456, -0.586]

2011 + 2014 only
  inverse-variance log OR = -1.444
  SE                      =  0.501
  95% CI                  = [-2.426, -0.462]
```

These are labelled **within-study season summaries**, not a three-study meta-analysis. Because one year's deposited contingency table disagrees with the publication, this combined number is not silently promoted as the sole canonical effect. Downstream synthesis should preserve two layers:

```text
source-primary direction: BA emission reduces D. undecimpunctata colonization in all three reported field seasons
repository sensitivity:   exact deposited counts and uncertainty, with 2014 discrepancy flag
```

If a route-level quantitative meta-analysis requires one Kessler-cluster effect, its inclusion must be accompanied by a sensitivity analysis that either excludes the discrepant 2014 season or contrasts publication-implied and deposited-data versions.

## Temporal mechanism

The defensive phenotype is temporally aligned with BA emission. During the early part of the night, when EV flowers emit BA, scent-silenced CHAL flowers receive more feeding damage. During the second half of the night, when EV flowers cease BA emission, the damage difference disappears.

This is registered separately in `SIGN_SWITCH_LEDGER_V1.csv` because it identifies **trait-expression timing** as a mechanism moderator rather than treating an all-night aggregate as the only defensible response.

## Sensory / bioassay support

The study also shows that *D. undecimpunctata* can detect BA and that behavioural/physiological responses depend on concentration. These experiments strengthen the interpretation that the field phenotype is mediated by the floral volatile rather than by an unrelated constitutive difference between transformed lines.

They are not counted as independent study replications of the field result.

## Evidence classification

```text
D_to_antagonism:               experimental, source-verified
flower-specific defence:       yes
single-trait dual function:    yes
same-system A x D:             no — one biological trait axis
field quantitative data:       recovered for 2011 / 2014 / 2016
2014 source-data agreement:     failed by one EV-positive observation
study-level quantitative use:  eligible only with explicit discrepancy sensitivity
context switch:                time of night / BA emission state
independence cluster:          one Kessler-et-al.-2019 study cluster
```

## Mechanistic implication

This study adds an important mechanism class to the synthesis: an attractive floral signal can itself be defensive against a floral antagonist. That does **not** imply universal functional synergy. Instead it shows why trait-role orientation must be separated from trait identity: the same molecule can occupy different ecological channels, and its net evolutionary effect depends on who encounters it, at what concentration, and when it is expressed.

The source–deposit discrepancy is also retained as part of the evidence-quality result. Reproducibility auditing is not treated as a nuisance step that can be bypassed when the biological direction is attractive.