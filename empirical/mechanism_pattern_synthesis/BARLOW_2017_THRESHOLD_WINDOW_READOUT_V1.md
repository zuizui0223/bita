# Barlow et al. (2017) — Aconitum consumer-tolerance threshold window

## Source identity

```text
article DOI: 10.1016/j.cub.2017.07.012
public data DOI: 10.6084/m9.figshare.5165350
workbook: BarlowetalCurrent Biology.xlsx
plants: Aconitum lycoctonum, A. napellus
legitimate pollinator: Bombus hortorum
nectar-robber bioassay consumer: Bombus terrestris
focal D axis: nectar alkaloid concentration
```

The primary source reports a clear biological asymmetry: nectar alkaloids deter robbers at substantially lower concentrations than those associated with the sharp decline in pollinator visitation. The public workbook permits separate reconstruction of the field pollinator lane and the laboratory robber-consumption lane.

The two endpoints are **not pooled into one effect metric**.

## Laboratory `D_to_antagonism` reconstruction

The preregistered reconstruction uses `Figure S2`, preserving every concentration as a separate within-study cell. Each test used a single experimental solution per *B. terrestris* worker, while the source experimental design also included sucrose controls by test round. Because round-level linkage is not present in this worksheet, control-versus-dose Hedges' g values are not promoted as independent meta-analytic contrasts. Aggregate dose-cell summaries are retained instead.

### A. lycoctonum mixture

| Alkaloids (ppm) | n | Mean consumed (µL) | SE | Reduction from sucrose mean |
|---:|---:|---:|---:|---:|
| 0 | 10 | 28.276 | 5.389 | reference |
| 0.2 | 12 | 21.959 | 2.639 | 22.3% |
| 2 | 14 | 18.659 | 2.756 | 34.0% |
| 20 | 9 | 3.022 | 1.278 | **89.3%** |
| 200 | 9 | 1.461 | 0.177 | **94.8%** |
| 2000 | 10 | 1.321 | 0.117 | **95.3%** |

### A. napellus mixture

| Alkaloids (ppm) | n | Mean consumed (µL) | SE | Reduction from sucrose mean |
|---:|---:|---:|---:|---:|
| 0 | 10 | 28.722 | 3.428 | reference |
| 0.2 | 10 | 24.511 | 4.196 | 14.7% |
| 2 | 15 | 16.517 | 3.430 | 42.5% |
| 20 | 10 | 3.620 | 0.877 | **87.4%** |
| 200 | 10 | 1.572 | 0.170 | **94.5%** |
| 2000 | 10 | 1.228 | 0.188 | **95.7%** |

The deposited data therefore contain the source-reported transition very clearly: by the 20-ppm checkpoint, mean consumption has already fallen by about 87–89% relative to the sucrose cell in both plant-species mixtures. Increasing concentration to 200–2000 ppm produces only a comparatively small additional decrease because consumption is already close to its lower floor.

This is stronger mechanistic information than a single pooled `alkaloids versus no alkaloids` contrast because it locates where antagonist deterrence becomes biologically large.

## Field `D_to_pollination` reconstruction

The workbook sheet `bee visits nec alks` contains paired *B. hortorum* relative visitation and total nectar-alkaloid concentration.

The source-aligned preregistered model was:

```text
ln(B. hortorum visitation) ~ ln(total nectar alkaloids ppm)
```

### A. lycoctonum deposited-data result

Using all finite positive paired values in the deposited sheet gives:

```text
n = 14
slope = -0.6520
SE = 0.2138
95% CI = [-1.0710, -0.2330]
Pearson r on log scales = -0.6608
Fisher z = -0.7943
SE(z) = 0.3015
95% z CI = [-1.3853, -0.2033]
R2 = 0.4367
adjusted R2 = 0.3898
F = 9.303
```

The deposited-data direction is therefore strongly negative and agrees with the article's biological conclusion that higher nectar-alkaloid concentrations are associated with lower pollinator visitation.

### A. napellus secondary low-power result

```text
n = 8
slope = -0.1439
SE = 0.2038
95% CI = [-0.5434, +0.2555]
Pearson r = -0.2770
adjusted R2 = -0.0771
F = 0.499
```

This remains an unresolved secondary species result and is not counted as an independent literature study.

## Field source/deposit statistical mismatch

The accepted-manuscript text route used when the protocol was written appeared to report a smaller *A. lycoctonum* regression statistic (`F≈5.8`, adjusted `R2≈0.27`) than the all-complete-pair deposited reconstruction above (`F=9.303`, adjusted `R2=0.390`, `n=14`).

The public article summary independently confirms the **direction and ecological threshold interpretation** — visits correlate negatively with nectar alkaloids and decline sharply in the approximately 200–380 ppm region — but it does not expose enough regression-table detail in its HTML summary to resolve which deposited observations were omitted, if any, from the reported field model.

No data row is removed post hoc to force the reconstruction toward the parsed manuscript statistic.

Accordingly, the field result is carried in two layers:

```text
source-primary inference:
  pollinator visitation decreases with nectar alkaloid concentration;
  sharp decline is reported around 200–380 ppm

deposited-data sensitivity:
  all finite positive pairs give r=-0.661 and a negative log-log slope;
  exact numerical meta-analytic promotion is held behind a source/subset reconciliation flag
```

## Mechanism-pattern result

The source and deposited laboratory data jointly support a **differential consumer-tolerance window**:

```text
nectar robber
  large consumption deterrence is already present around the 20-ppm checkpoint

legitimate pollinator
  the source reports the sharp field visitation decline much later, around 200–380 ppm
```

The two measurements use different species, settings and response constructs, so their coefficients cannot be subtracted to estimate `rho - iota`. What can be identified is the ordering of the response regions: antagonist deterrence becomes large at substantially lower alkaloid concentration than pronounced pollinator interference.

This pattern is directly relevant to the theory because it provides a real-system example of a parameter region where antagonist relief can arise before the pollinator-interference channel becomes strong. It is therefore a plausible empirical analogue of a **guarded-attraction-compatible concentration window**, not proof of positive `W_AD`.

## Evidence classification

```text
D_to_antagonism:         experimental dose-response, public raw data, quantitative
D_to_pollination:        field observational association, public raw data; exact source-model subset unresolved
same-system multi-route: yes
consumer threshold gap:  source-verified and raw-dose supported
strict direct A x D:     no
joint cost kappa:        not identified
independence cluster:    one Barlow-et-al.-2017 study cluster
```

## Integration rule

For the integrated meta/synthesis:

1. use the laboratory dose cells to support the within-study antagonist-deterrence threshold pattern;
2. use the source field conclusion and deposited negative slope to support pollinator interference, while flagging the exact coefficient until the model-subset discrepancy is resolved;
3. register the 20 ppm versus approximately 200–380 ppm ordering in the sign-switch/threshold ledger;
4. do not create a cross-endpoint grand effect or treat the two *Aconitum* species as independent studies.