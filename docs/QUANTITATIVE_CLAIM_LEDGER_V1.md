# BITA quantitative claim ledger V1

## Purpose

This ledger separates directly measured or reconstructed quantities from literature-audit counts, algebraic identification results, conditional model bounds, and quantities that remain unidentified. It does not change the active thesis: **trait interaction is not ecological mechanism**.

## Claim classes

- `EMPIRICAL` — a quantity estimated or bounded from a biological dataset under declared reconstruction assumptions.
- `LITERATURE-AUDIT` — a count or classification of screened route records, clusters, or systems; not a prevalence estimate.
- `THEORETICAL-WITNESS` — a constructive algebraic/non-identification object used to show what the observed interaction does or does not identify.
- `MODEL-PREDICTION` — a quantitative consequence conditional on an explicit biological restriction or intervention model.
- `NOT-ESTIMATED` — a scientifically meaningful quantity not point-estimated by the current evidence.

## Registered quantitative objects

| Object | Class | Frozen quantitative statement | Interpretation ceiling |
|---|---|---|---|
| route recurrence ledger | `LITERATURE-AUDIT` | `56 directional route records` from `25 independent biological clusters` | establishes recurrence capacity of constituent marginal pathways; not natural prevalence |
| high-information frontier | `LITERATURE-AUDIT` | `17 systems` | maps where experimental identification dimensions occur; not a literature-prevalence estimator |
| complete mechanism-allocation closure | `LITERATURE-AUDIT` | `0 systems` close the full allocation design plus an independent remaining-channel assay | demonstrates fragmentation in the screened high-information frontier only |
| Kessler defended attraction effect | `EMPIRICAL` | `A1 approximately +0.200 to +0.240` under the registered aggregate constraints | sign-identified positive aggregate anchor; exact source/design uncertainty remains unresolved |
| Kessler undefended attraction effect | `EMPIRICAL` | `A0 approximately -0.030 to +0.030` | remains zero-compatible; strict Level-2/3 release is not identified |
| total interaction | `EMPIRICAL` | `Delta_AD W = A1-A0` remains positive under the registered aggregate constraints | supports Level-1 positive interaction relief only |
| identified set | `THEORETICAL-WITNESS` | `I(delta) = {(rho,iota,kappa): rho-iota-kappa=delta}` | a total interaction defines a set of compatible allocations rather than a unique mechanism |
| conditional channel bound | `MODEL-PREDICTION` | if independently justified `kappa_delta >= 0`, then `rho_delta-iota_delta = Delta_AD W + kappa_delta >= Delta_AD W` | conditional partial-identification bound; validity depends on the biological restriction |
| crossed consumer intervention | `MODEL-PREDICTION` | selective `A x D x antagonist x pollinator` intervention plus baseline handling and separability diagnostics can add independent identifying contrasts | design prediction; point identification still requires the declared assumptions and an independent remaining-channel assay |

## Quantities explicitly not estimated or not point identified

```text
NATURAL_PREVALENCE = NOT_ESTIMATED
CHANNEL_ALLOCATION = NOT_POINT_IDENTIFIED_FROM_TOTAL_INTERACTION
RHO_DELTA_POPULATION_DISTRIBUTION = NOT_ESTIMATED
IOTA_DELTA_POPULATION_DISTRIBUTION = NOT_ESTIMATED
KAPPA_DELTA_POPULATION_DISTRIBUTION = NOT_ESTIMATED
STRICT_LEVEL2_PREVALENCE = NOT_ESTIMATED
STRICT_LEVEL3_PREVALENCE = NOT_ESTIMATED
```

The `56/25/17` counts are literature-structure quantities, not ecological effect sizes. The Kessler ranges are the strongest system-level aggregate anchor in the current paper, but they do not recover the ecological channel allocation.

## Promotion rule

Precision in `Delta_AD W` alone never promotes the result to mechanism identification. A mechanism-resolved numerical claim requires independent information that shrinks the compatible allocation set: explicit restrictions, selective interventions, separability support, and an independent remaining-channel assay. A residual by subtraction is not automatically a measured `kappa_delta`.
