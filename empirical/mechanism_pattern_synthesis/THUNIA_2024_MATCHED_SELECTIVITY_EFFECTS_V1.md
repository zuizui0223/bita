# Thunia alba 2024 matched defence-selectivity reconstruction v1

## Source and design

Wu S-M, Gao J-Y. 2024. The conspicuously large bracts influence reproductive success in *Thunia alba* (Orchidaceae). *Journal of Plant Ecology* 17:rtad036. DOI `10.1093/jpe/rtad036`.

The field experiment removed the large spur-enclosing bract. The same floral manipulation therefore supplies both antagonist and legitimate-pollination responses for one flower-specific physical/access defence axis.

## Source-reported means

For intact versus bract-removed flowers, the source reports:

```text
robbed flowers:       15.43 ± 3.13% vs 90.25 ± 1.88%
pollinia removal:     56.50 ± 2.65% vs 15.47 ± 3.85%
pollinia deposition:  30.79 ± 2.13% vs  9.73 ± 3.37%
fruit set:             28.71 ± 2.08% vs  8.18 ± 3.39%
hourly visit rate:      2.48 ± 0.31  vs  2.39 ± 0.25
```

The intact and removed reproductive samples are reported as `n=40` and `n=43`, respectively. The article also reports that the only pollinator, *Bombus breviceps*, shifts toward nectar robbery after bract removal.

## Reconstructed log response ratios

For positive-valued source-reported group means, use

`LRR = ln(mean_intact / mean_removed)`

with delta-method standard error

`SE(LRR) = sqrt[(SE_intact/mean_intact)^2 + (SE_removed/mean_removed)^2]`.

This is a reconstruction from reported means and SEs, not a replacement for the source's GLM/chi-square inference.

```text
outcome                 LRR       SE
robbed-flower fraction -1.7663   0.2039
pollinia removal       +1.2953   0.2532
pollinia deposition    +1.1520   0.3532
fruit set              +1.2556   0.4207
hourly visit rate      +0.0370   0.1630
```

Orientation:

- negative robbery LRR = intact bract suppresses antagonistic robbery;
- positive pollinia/fruit LRR = intact bract preserves or increases legitimate pollination/reproductive function;
- near-zero visit-rate LRR = the effect is not explained by attracting more visitors.

## Mechanism-first interpretation

This is stronger than a simple `D -> antagonism` example. The same defence manipulation produces:

```text
antagonist use:              strongly lower
visitor arrival frequency:   approximately unchanged
legitimate pollination mode: strongly higher
reproductive success:        strongly higher
```

The source therefore supports **functional-mode selectivity**: the bract changes what the same visitor does, rather than which visitor arrives.

This is a quantitative anchor for the mechanism-first prediction that selective defence can increase antagonist relief without a corresponding pollinator-arrival penalty.

## Inference boundary

Do not subtract or pool the robbery, pollinia, and fruit-set LRRs as if they were independent estimates. They are dependent outcomes from one experiment and their covariance is unavailable. Do not call any of these effects `W_AD`, `rho`, `iota`, or `kappa`.

### Adjudication

```text
D -> antagonism:                quantitative strong support
D -> pollination arrival:       quantitative null-compatible
D -> pollination function:      quantitative positive support
selectivity class:              FUNCTIONAL_MODE_SELECTIVE
universality role:              MATCHED_QUANTITATIVE_ANCHOR
formal cross-study moderator:   pending additional matched systems
```
