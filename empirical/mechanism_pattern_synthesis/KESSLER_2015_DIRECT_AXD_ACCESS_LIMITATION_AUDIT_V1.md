# Kessler et al. 2015 direct A x D access-limitation audit v1

## Source

Kessler D, Kallenbach M, Diezel C, Rothe E, Murdock M, Baldwin IT. 2015. *How scent and nectar influence floral antagonists and mutualists*. eLife 4:e07641. DOI `10.7554/eLife.07641`.

## Why this source is theory-facing

The study independently manipulated two flower-specific axes in all four combinations:

```text
A = benzylacetone floral scent emission
D = floral reward/access restriction, operationalized as absence of floral nectar
```

Genotypes:

```text
EV             A+, D-   scent present; nectar present
CHAL           A-, D-   scent absent;  nectar present
SWEET9         A+, D+   scent present; nectar absent
CHALxSWEET9    A-, D+   scent absent;  nectar absent
```

Here `D+` is deliberately oriented as **greater antagonist-reducing reward/access restriction**, not as greater nectar production.

This orientation is admissible because the source independently shows that absence of nectar reduces `Manduca sexta` oviposition, a future-herbivory proxy, while the manipulation is floral and the source reports no differences in leaf volatile profile, plant morphology, flower size, or hand-pollinated seed capacity among the four lines.

Thus this is cleaner than Kessler 2008 for intervention specificity.

## Antagonist-reduction gate for D

Relative to EV, field oviposition was reported as:

```text
CHAL           43.1%
SWEET9         10.8%
CHALxSWEET9     6.5%
```

and in the single-moth tent experiment:

```text
CHAL           81.9%
SWEET9         52.5%
CHALxSWEET9    48.4%
```

Therefore nectar restriction (`D+`) has a directly demonstrated antagonist-reducing role in the focal floral system. It is not being relabelled as defence merely because it is a floral trait.

## Shared reproductive outcome

The source reports seed production from antherectomized flowers pollinated by WT donors, so reproductive differences are pollinator-mediated rather than caused by intrinsic seed-production defects. A hand-pollination control found no genotype difference in seed production (`F3,36 = 1.19`, `p = 0.33`, `n = 10`).

The four-cell source states therefore permit a discrete A x D interaction contrast on the same reproductive outcome.

## Direct factorial signs

For each pollinator context, normalize EV seed production to `1.0` and define

```text
Delta_AD = W(A+,D+) - W(A+,D-) - W(A-,D+) + W(A-,D-)
```

with `D+ = nectar absent / greater reward restriction`.

### Native visitor community

Source-normalized seed production:

```text
EV             1.000
CHAL           0.229
SWEET9         0.097
CHALxSWEET9    0.116
```

Discrete interaction:

```text
Delta_AD = 0.097 - 1.000 - 0.116 + 0.229 = -0.790
```

Direction: **substitution-compatible / negative**.

### Manduca sexta

Source-normalized seed production:

```text
EV             1.000
CHAL           0.174
SWEET9         0.446
CHALxSWEET9    0.052
```

Discrete interaction:

```text
Delta_AD = 0.446 - 1.000 - 0.052 + 0.174 = -0.432
```

Direction: **substitution-compatible / negative**.

### Hyles lineata

Source-normalized seed production:

```text
EV             1.000
CHAL           0.966
SWEET9         1.1169
CHALxSWEET9    0.213
```

Discrete interaction:

```text
Delta_AD = 1.1169 - 1.000 - 0.213 + 0.966 = +0.8699
```

Direction: **complementarity-compatible / positive**.

The sign therefore reverses across pollinator contexts **within the same plant genotype architecture and the same A/D manipulations**.

## Statistical boundary

The paper analyzed the four treatments with Friedman signed-rank tests and post-hoc comparisons. It did not report a dedicated A-by-D interaction coefficient for these normalized outcome panels. Peer review explicitly cautioned against treating the double manipulation as formally additive/nonadditive without an interaction test.

Therefore the reconstructed `Delta_AD` values are exact arithmetic translations of the source-reported normalized means, but they are **not source-tested interaction coefficients with standard errors**.

Adjudication:

```text
strict crossed floral A and antagonist-reducing D:  PASS
shared reproductive outcome:                         PASS
intervention specificity:                            PASS
intrinsic reproduction control:                      PASS
discrete factorial sign:                             IDENTIFIED DESCRIPTIVELY
formal A x D interaction uncertainty:                NOT IDENTIFIED
local derivative W_AD:                               NOT IDENTIFIED
```

## Theory-facing interpretation

This source changes U7 materially.

Direct floral A x D evidence is no longer restricted to one unresolved `Impatiens` cluster or the intervention-confounded Kessler 2008 candidate. Kessler 2015 provides a cleaner crossed floral design and demonstrates that the **direct discrete A x D sign itself changes with pollinator identity**:

```text
native community  negative
M. sexta          negative
H. lineata        positive
```

This is unusually strong evidence for the manuscript's mechanism-first conclusion that the repeatable object is a switching architecture rather than one universal attraction-defence sign.

It does not establish prevalence, a universal sign, or a universal numerical `W_AD`.

## Boundary

```text
discrete factorial interaction != local mixed partial derivative
nectar restriction D != all forms of floral defence
source-normalized means != formal interaction meta-analysis
sign reversal across pollinator contexts != estimate of rho/iota/kappa
```