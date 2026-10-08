# Route retention: source-frozen composition sensitivity and M2 convergence audit

Date: 2026-10-08
Branch: `analysis/route-retention-composition-v1`
Status: **POST-OPEN DESCRIPTIVE; NO CONFIRMATORY CHEATING MECHANISM CLAIM**

## Verified input

Original public-author data are *not* fetched in this audit. Reuse the existing
archive artifact `11293379572`, archive schema
`BITA_ACCESS_ROUTING_LETTER_ARCHIVE_V4`, containing anonymous event count tables.

SHA-256:
- `aubert_ephi_participation_opportunities.csv`:
  `685f227a2aa2c5c322e18188ba5bd6d44aa67490b31514b9c728e6e033abc14f`
- `aubert_ephi_pair_site_analysis.csv`:
  `94c74386d2c304b5816653e79b552a0e79487258c5021f8791c614afdc956afa`

Frozen mismatch, no data-driven bin movement:
`m=log(tube/(1.8*culmen))`;
accessible `m<=0`, moderate `0<m<=log(1.25)`, severe `m>log(1.25)`.
Hummingbirds only (Diglossa excluded).

19,903 opportunity edges; bins 14,770 / 1,847 / 3,286,
246 bird×site strata. Observed route counts:

| Category | legitimate | robbery |
|---|---:|---:|
| Accessible | 34,354 | 1,709 |
| Moderate | 3,350 | 540 |
| Severe | 1,710 | 1,885 |

## Strict sorting-only *descriptive* standardization

For each bird×site stratum with both accessible and severe opportunity
support, hold the observed total route count fixed and allocate expected
counts among the three bins in proportion to zero-inclusive opportunity
edge counts. This controls **species and site composition** but NOT
camera-hour effort, flower abundance, plant×bird interaction specificity,
reward, or detectability.

Observed / expected counts:

| State | legitimate | robbery |
|---|---:|---:|
| Accessible | 1.2213381 | 0.6963107 |
| Moderate | 0.8949030 | 1.0692085 |
| Severe | 0.2626756 | 1.5870725 |

The severe/access ratio of these observed-to-expected ratios is:
- Legitimate: `0.21507`
- Robbery: `2.27926`

### Leave-one-cluster descriptive stability

The following are **ranges of leave-one-cluster point statistics**,
not a bootstrap CI or independent replication:

| Excluded unit | n | legitimate severe/access O/E ratio range | robbery severe/access O/E ratio range |
|---|---:|---:|---:|
| plant species | 288 | 0.18410–0.23109 | 2.13463–2.53936 |
| bird species | 49 | 0.19010–0.24289 | 2.06051–2.43644 |
| site | 18 | 0.19162–0.23695 | 2.16118–2.52114 |

All leave-one estimates retain the same direction. This supports the
stability of a *descriptive discrepancy* from the simplest
bird×site sorting-only expectation. It cannot establish a causal
bird-behavior or bypass-rescue mechanism.

## The stricter model and its unresolved robbery outcome

The two-way Poisson M2 uses waypoint and bird×site fixed effects.
The legitimate route converged and its independent 288/288 plant
jackknife was recorded in
`LEGITIMATE_M2_JACKKNIFE_INDEPENDENT_CROSSCHECK_V1.md`:
severe/access RR `0.0489769` with 95% CI `0.0265463–0.0903604`.

Robbery M2 did not satisfy the original strict IPF convergence criterion
after 10,000 iterations. A purely numerical convergence diagnostic,
with the data, factors and model held constant, returned:

| Iterations | Maximum margin error | Moderate/access coefficient RR | Severe/access coefficient RR |
|---|---:|---:|---:|
| 2,000 | 0.00042193164 | 0.503873882 | 1.027761920 |
| 10,000 | 0.00008445274 | 0.503873112 | 1.027760550 |
| 25,000 | 0.00003379572 | 0.503873001 | 1.027760354 |

**These are numerical iterates, not accepted model estimates.**
The category coefficients have almost stopped moving, while
nuisance-margin agreement improves slowly. At iteration 10,000, one
worst waypoint, `waypoint_1341`, contains two supported
bird opportunities and only one robbery event, illustrating sparse
route-specific support. This makes slow fixed-effect convergence
plausible, not a proof of formal nonidentifiability.

Do not change the preregistered tolerance, fit another post-open model
as if confirmatory, or report these numerical iterates as evidence
of an increased robbery rate.

## Reproduction and boundaries

Source point workflow: https://github.com/zuizui0223/bita/actions/runs/37783945027
- point job passed;
- first full jackknife job failed *before input opening* because Zenodo
  returned HTTP 504;
- a frozen-anonymous-archive-input variant is committed and was queued
  for GitHub Actions reproduction, separate from the completed local
  independent numerical cross-check.

Allowed biological claim:
> Strong legitimate-route suppression with increasing mismatch survives
> bird×site and waypoint fixed effects; the simple species×site
> sorting-only expectation leaves a stable descriptive route-composition
> discrepancy.

Not allowed:
> Individual birds switch their tactics due to mismatch, or robbery
> causally rescues ecological interaction.

A stronger claim would require independent individual-level or
manipulative measurements, not additional threshold scanning of
the same network.
