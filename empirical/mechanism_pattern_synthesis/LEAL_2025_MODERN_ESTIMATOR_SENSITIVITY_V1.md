# Leal et al. 2025 modern-estimator sensitivity v1

**Decision: ROBUSTNESS_PASS**

The preregistered canonical Leal module remains the DerSimonian–Laird analysis pinned at `ed33b25593c0d90ad6657753f6f5501d9efc7b82`. This sensitivity reuses the same one-effect-per-independent-cluster inputs and asks whether the three informative directions survive REML heterogeneity estimation plus modified Hartung–Knapp inference. It does not replace the canonical estimates.

Method motivation: Hartung–Knapp-type intervals account for uncertainty in the mean under random effects; the modified form avoids counterintuitively narrow intervals when the Hartung–Knapp scale factor falls below one. See Röver, Knapp & Friede (2015, DOI `10.1186/s12874-015-0091-1`) and Brockwell & Gordon (2016, DOI `10.1002/sim.7140`) for coverage-focused evaluations.

| outcome | k | canonical DL pooled (recomputed) | REML pooled | REML tau² | mHK 95% CI | negative interval retained? |
|---|---:|---:|---:|---:|---:|---|
| female reproductive success | 48 | -0.210 | -0.205 | 0.143 | [-0.332, -0.078] | yes |
| nectar standing crop | 28 | -0.483 | -0.489 | 0.525 | [-0.795, -0.184] | yes |
| legitimate visitation | 22 | -0.291 | -0.288 | 0.346 | [-0.576, -0.000] | yes |

## Interpretation

The decision is deliberately binary only at the robustness level: if all three modified Hartung–Knapp intervals remain below zero, the directional conclusions are robust to a more conservative random-effects inferential convention. If any interval crosses zero, the canonical DL estimate is retained but the corresponding manuscript claim must be qualified as estimator-sensitive.

This sensitivity does **not** estimate `rho`, `iota`, `kappa`, or `W_AD`; does not reduce the extreme heterogeneity; and does not turn the Leal deposit into an independent systematic review.
