# Route-corrected visit-number sensitivity for the 2019 nectar synthesis

## Status

**The published visit-number lane is negative at the broad paper-summary level, but that sign is not statistically stable after correcting the three known route-mixing decisions. The manuscript remains frozen.**

This analysis does not introduce a new model, parameter, mechanism, or theory bridge. It returns to the recovered Parachnowitsch, Manson and Sletvold (2019; doi: `10.1093/aob/mcy132`) worksheet and applies the evidence rules already fixed in `ANALYSIS_COMPLETION_GATE.md`.

## 1. Why the previous exploratory result needed correction

The outcome-lane reanalysis previously separated visit number from visit length and volume consumed. Its visit-number result was:

```text
independent papers             3
random-effects Hedges g       -0.315
95% CI                        -0.592 to -0.038
I²                             64.2%
```

That estimate still inherited three paper-level mixtures:

1. **Adler and Irwin (2005)** pooled a supra-natural 2002 treatment year with the source-audited natural-range 2004 year.
2. **Jones and Agrawal (2016)** pooled the legitimate bumblebee response with a Lepidoptera antagonist response.
3. **Manson et al. (2013)** collapsed four dose contrasts into one paper effect even though pollinator responses change strongly across the reported dose order.

The present analysis corrects the first two choices and exposes the third as a sensitivity rather than hiding it inside one estimate.

## 2. Fixed route corrections

The three independent papers are retained, but their roles are restricted as follows:

- **Adler and Irwin (2005):** only the 2004 natural-range visit-number row is used.
- **Jones and Agrawal (2016):** only the legitimate Bee visit-number row is used; the Lepidoptera antagonist row is excluded from the pollinator pathway.
- **Manson et al. (2013):** the four visit-number rows remain one study cluster. Four separate three-paper syntheses are reported, one for each source-order contrast. A fifth all-dose within-paper summary is retained only as a diagnostic comparison.

No Manson dose row is counted as an independent replication.

## 3. Results

| Manson choice | Random-effects Hedges g | 95% CI | I² |
|---|---:|---:|---:|
| Source-order contrast 1 | +0.030 | -0.218 to +0.279 | 0.0% |
| Source-order contrast 2 | -0.183 | -0.456 to +0.090 | 15.6% |
| Source-order contrast 3 | -0.307 | -0.882 to +0.269 | 80.4% |
| Source-order contrast 4 | -0.354 | -1.037 to +0.328 | 86.0% |
| All four Manson rows, fixed within paper (diagnostic) | -0.242 | -0.636 to +0.152 | 69.4% |

Every corrected interval includes zero.

The direction becomes more negative as the selected Manson contrast moves through the source order, while the lower-source-order contrast produces a pooled estimate near zero. This agrees with the primary-source audit: the Manson response is weak at the lower treatments and becomes strongly negative at the higher treatments. It is therefore not defensible to represent that study by one universal negative pollinator-cost effect without carrying dose choice explicitly.

## 4. What changed scientifically

The earlier negative visit-number estimate was not fabricated, but its nominal exclusion of zero depended on biologically consequential aggregation:

- mixing one antagonist response into the Jones pollinator effect;
- retaining the supra-natural Adler year;
- averaging dose-dependent Manson contrasts.

After those decisions are corrected or exposed, the three-paper evidence supports **heterogeneous, context-dependent pollinator interference**, not a stable negative mean for legitimate-pollinator visit number.

This does not imply that floral defence never reduces pollinator use. Adler and Irwin provide a same-system weak negative field contrast, and the higher Manson contrasts are negative. It means that the current three-study lane cannot yet identify a general direction independently of dose and route coding.

## 5. Consequence for the empirical completion gate

```text
outcome-compatible independent papers        3
exploratory threshold                         reached
stable direction after route correction       no
stability threshold                           not reached
canonical pathway estimate                    not yet justified
```

The next useful evidence is another independent, source-audited legitimate-pollinator effect in the same response construct, not another moderator or power analysis. Priority remains:

1. recover a source-complete Gegear et al. (2007) pollinator-use contrast;
2. recover Jones, Warburton and Martin (2023) supporting data or an exact reported model contrast;
3. identify a source-reported primary contrast for Köhler et al. (2012) without treating its dependent dose-by-sugar rows as replication;
4. keep consumption, residence time, pollen transfer and reproduction outside the visit-number lane.

## Interpretation boundary

This analysis is a route-correction sensitivity of a published broad synthesis. It is not an estimate of `iota`, `rho`, `kappa`, or `W_AD`. The all-dose Manson summary is dependence-limited and diagnostic only. No manuscript text, figure, theorem, or journal framing is changed.
