# Post-open support diagnostic for non-converged robbery M2

Date: 2026-10-08
Status: **DESCRIPTIVE ONLY — DOES NOT REDEFINE THE FROZEN MODEL**
Branch: `analysis/route-retention-composition-v1`

## Input provenance

The frozen anonymously labelled `BITA_ACCESS_ROUTING_LETTER_ARCHIVE_V4`
GitHub Actions artifact ID `11293379572` was downloaded and inspected
without retrieving new EPHI observations.

SHA256:
- `aubert_ephi_participation_opportunities.csv`:
  `685f227a2aa2c5c322e18188ba5bd6d44aa67490b31514b9c728e6e033abc14f`
- `aubert_ephi_pair_site_analysis.csv`:
  `94c74386d2c304b5816653e79b552a0e79487258c5021f8791c614afdc956afa`

The companion pair-site `bird_group` was mapped without using visit outcomes.
Hummingbirds only; `Diglossa` excluded. Frozen mismatch:
`log(T / (1.8 * culmen))`; state boundary `log(1.25)`.

## Source-level support, prior to dropping zero-count margins

| Measure | Value |
|---|---:|
| Zero-inclusive opportunity edges | 19,903 |
| Bird x site strata | 246 |
| Accessible / moderate / severe edges | 14,770 / 1,847 / 3,286 |
| Robbery counts across accessible / moderate / severe | 1,709 / 540 / 1,885 |
| Legitimate counts across accessible / moderate / severe | 34,354 / 3,350 / 1,710 |
| Strata containing accessible and severe opportunities | 171 |
| Strata with any robbery event | 100 |
| Strata with any legitimate event | 242 |
| Strata with both routes observed | 98 |
| Accessible+severe support and any robbery | 82 |
| Accessible+severe support and both routes | 82 |
| **Robbery events in both accessible and severe** | **29** |
| **Legitimate events in both accessible and severe** | **76** |

Counts are descriptive and not effort-adjusted rate estimates.

## Diagnosis

The full robbery model with bird×site and waypoint fixed effects
did not converge at its preregistered algorithm tolerance within
10,000 cycles (last margin residual around 8.45e-5).
The limited number of strata with positive robbery in both extreme
mismatch bins is **compatible with sparse effective within-stratum
information**, but the count audit alone does not prove separability
or establish the precise numerical obstruction.

Do not infer from algorithmic non-convergence that the ecological
effect is zero or absent; do not promote a threshold or route-switch
claim using post hoc relaxed tolerance. Legitimate M2 converged,
but its plant-cluster jackknife is not complete yet.

The independent archived-input pipeline includes SHA256 guards
and verifies exact reproduction of the prior point estimates
before full plant sensitivity is attempted. A 504 error prevented
the earlier full run from retrieving the original Zenodo file.
The archive-only pipeline changes **data transport**, not scientific
definitions or estimands.

## Interpretation boundary

Despite strong adjusted suppression of legitimate interactions,
the present observations do not distinguish a tracked individual's
tactic change from plant-selection differences and unmeasured
pairwise reward properties. No cause of robbery retention is
confirmed at this point.
