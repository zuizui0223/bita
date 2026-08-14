# Catalpa 1982 matched selectivity effects v1

## Purpose

Reconstruct a same-study, same-defence matched quantitative anchor for the mechanism-first selectivity test.

Source: Stephenson AG (1982), *Journal of Chemical Ecology* 8:1025–1034, DOI `10.1007/BF00987883`.

Focal defence:

```text
Catalpa speciosa nectar iridoid glycosides
0.4% catalpol + 0.4% catalposide
```

The source reports sucrose-only and sucrose+iridoid group means, SDs and sample sizes for two potential nectar-thief assays and one legitimate-pollinator assay.

## Effect metric

For each assay, compute an oriented log response ratio:

```text
LRR = ln(mean iridoid / mean sucrose)
```

Negative LRR means less resource exploitation/consumption in the iridoid treatment.

Sampling variance uses the standard delta-method approximation for independent group means:

```text
Var(LRR) = SD_iridoid^2 / (n_iridoid * mean_iridoid^2)
         + SD_sucrose^2 / (n_sucrose * mean_sucrose^2)
```

This gives a dimensionless within-assay treatment response while preserving consumer identity.

## Reconstructed effects

### Potential nectar thief: ants

Source Table 2:

```text
sucrose:           n=38, mean=118 s, SD=73
sucrose+iridoids:  n=52, mean=33 s,  SD=49
```

Reconstruction:

```text
LRR = -1.2742
SE  =  0.2291
```

The source also reports sucrose versus sucrose+iridoids `t=6.62`, `df=88`, `P<0.001`.

### Potential nectar thief: Poanes hobomok

Source Table 3:

```text
sucrose:           n=21, mean=9.5 µl, SD=6.3
sucrose+iridoids:  n=22, mean=3.7 µl, SD=3.2
```

Reconstruction:

```text
LRR = -0.9430
SE  =  0.2344
```

The source reports sucrose versus sucrose+iridoids `t=3.8`, `df=41`, `P<0.001`.

### Legitimate pollinators: bumblebees and carpenter bees

Source Table 4:

```text
sucrose:           n=54 wells, mean=19.7, SD=1.4
sucrose+iridoids:  n=20 wells, mean=19.5, SD=1.4
```

Reconstruction:

```text
LRR = -0.0102
SE  =  0.0187
```

The source reports no significant difference among the three reward types (`Kruskal-Wallis H=0.43`, `df=2`, `P≈0.20`).

## Selectivity interpretation

The two antagonist assays are separate consumer assays inside one study cluster and must **not** be counted as two independent biological replications. Their LRRs are both strongly negative, whereas the legitimate-pollinator consumption LRR is approximately zero.

This therefore supplies a quantitative same-study guarded-defence state:

```text
antagonist exploitation: strongly suppressed
legitimate-pollinator consumption: approximately preserved
```

The effect difference is not promoted to a universal `selectivity` parameter because the antagonist assays differ in consumer and response implementation and there is no shared-unit covariance linking them to the pollinator assay.

For descriptive orientation only, an inverse-variance average of the two antagonist LRRs would be approximately `-1.112` (naive SE `0.164`), but this is **not** an independent-study meta-analytic estimate and is not used for inference.

## Theory-facing result

Catalpa provides a direct quantitative example of **consumer-selective defence**: the focal floral chemical strongly reduces exploitation by potential thieves while leaving tested legitimate-pollinator reward consumption essentially unchanged.

This supports U5 as one quantitative anchor, not as proof of universal complementarity and not as an estimate of `W_AD`, `rho`, `iota`, or `kappa`.

## Boundary

```text
same-study matched routes != direct A x D
consumer selectivity != W_AD
pollinator null != iota = 0 universally
one study cluster != prevalence
```
