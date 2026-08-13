# Leal et al. 2025 modern-estimator sensitivity v1

**Decision: ROBUSTNESS_PASS**

The preregistered canonical Leal module remains the DerSimonian–Laird analysis pinned at `ed33b25593c0d90ad6657753f6f5501d9efc7b82`. This sensitivity reuses the same one-effect-per-independent-cluster inputs and asks whether the three informative directions survive REML heterogeneity estimation plus modified Hartung–Knapp inference. It does not replace the canonical estimates.

Method motivation: Hartung–Knapp-type intervals account for uncertainty in the mean under random effects; the modified form avoids counterintuitively narrow intervals when the Hartung–Knapp scale factor falls below one. See Röver, Knapp & Friede (2015, DOI `10.1186/s12874-015-0091-1`) and Partlett & Riley (2017, DOI `10.1002/sim.7140`) for coverage-focused evaluations.

| outcome | k | canonical DL pooled (recomputed) | REML pooled | REML tau² | mHK 95% CI | negative interval retained? | boundary flag |
|---|---:|---:|---:|---:|---:|---|---|
| female reproductive success | 48 | -0.210 | -0.205 | 0.143 | [-0.3318, -0.0777] | yes | not borderline |
| nectar standing crop | 28 | -0.483 | -0.489 | 0.525 | [-0.7948, -0.1840] | yes | not borderline |
| legitimate visitation | 22 | -0.291 | -0.288 | 0.346 | [-0.5756, -0.0002] | yes | borderline to zero |

## Interpretation

All three pooled directions remain negative under REML plus modified Hartung–Knapp inference. Female reproductive success and nectar standing crop retain clearly negative intervals. Legitimate visitation also remains below zero, but its upper limit lies within 0.001 of zero and is therefore treated as **borderline estimator robustness**, not as a strong exclusion of zero.

The decision is deliberately limited to robustness: if an interval crosses zero, the canonical DL estimate is retained but the corresponding manuscript claim must be qualified as estimator-sensitive. An interval that technically excludes zero but approaches it within the declared margin is flagged rather than rounded into an apparently stronger result.

This sensitivity does **not** estimate `rho`, `iota`, `kappa`, or `W_AD`; does not reduce the extreme heterogeneity; and does not turn the Leal deposit into an independent systematic review.
