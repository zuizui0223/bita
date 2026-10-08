# Bypass rescue-window first-open result v1

Status: **PRIMARY HYPOTHESIS KILLED**
Date opened: 2026-10-08
Branch: `analysis/bypass-rescue-window-v1`
Freeze: `BYPASS_RESCUE_WINDOW_PREREG_V1.md`

The outcome was opened only after the three-state boundaries and promotion rule
were committed.

## Reproduction source

The first-open calculation used the already frozen anonymous access-routing
archive artifact:

- GitHub artifact id: `11293379572`
- archive schema: `BITA_ACCESS_ROUTING_LETTER_ARCHIVE_V4`
- opportunity table: `aubert_ephi_participation_opportunities.csv`
- 19,909 original opportunity edges.

The V4 opportunity table does not itself carry `bird_group`, but the companion
pair-site table provides a one-to-one anonymous bird-unit -> group mapping:
49 hummingbird units and 1 flowerpiercer unit. Restricting by this frozen mapping
leaves 19,903 hummingbird opportunity edges. No taxon identities were restored.

Primary effective mismatch and bins exactly follow the preregistration:

~~~text
M_eff = log[tube / (1.8 * culmen)]
ACCESSIBLE:        M_eff <= 0
MODERATE_MISMATCH: 0 < M_eff <= log(1.25)
SEVERE_MISMATCH:   M_eff > log(1.25)
~~~

Opportunity support before outcome modelling:

~~~text
accessible edges = 14,770
moderate edges   = 1,847
severe edges     = 3,286
birds            = 49
plants           = 288
waypoints         = 4,933
~~~

The frozen support gate therefore passes.

## Primary route results

The model is the frozen two-way fixed-effect Poisson model with mismatch state
added as a three-level factor. Plant-species delete-one jackknife intervals are
reported on rate ratios.

### Robbery-only absolute feeding rate

| Contrast | Rate ratio | 95% plant-jackknife CI |
|---|---:|---:|
| MODERATE / ACCESSIBLE | 0.7460 | 0.3134–1.7757 |
| SEVERE / ACCESSIBLE | 1.2173 | 0.4805–3.0840 |
| SEVERE / MODERATE | 1.6318 | 0.9446–2.8187 |

The intermediate state was the robbery-rate maximum in **0/288** leave-one-plant
fits.

### Legitimate/non-robbing absolute feeding rate

| Contrast | Rate ratio | 95% plant-jackknife CI |
|---|---:|---:|
| MODERATE / ACCESSIBLE | 0.3149 | 0.2053–0.4831 |
| SEVERE / ACCESSIBLE | 0.05330 | 0.02971–0.09561 |
| SEVERE / MODERATE | 0.1692 | 0.09581–0.29898 |

Legitimate feeding therefore declines strongly already in the moderate mismatch
state and declines again under severe mismatch.

## Frozen decision

~~~text
FULL_BYPASS_RESCUE_WINDOW = false
DIRECTIONAL_WINDOW_ONLY   = false
NO_BYPASS_RESCUE_WINDOW   = true
PROMOTION_ELIGIBLE        = false
~~~

The preregistered prediction that absolute robbery peaks at intermediate mismatch
is rejected in this dataset.

## Unexpected pattern revealed by the failed test

The failed window exposes a different descriptive ordering:

~~~text
legitimate:
ACCESSIBLE  >> MODERATE >> SEVERE

robbery:
ACCESSIBLE ~ MODERATE < SEVERE   (point ordering; uncertainty remains broad)
~~~

This is compatible with a **delayed bypass** pattern: modest mismatch first removes
legitimate interaction without an accompanying increase in absolute robbery; bypass
becomes relatively more prominent only under severe mismatch.

This interpretation is post-outcome and is **not confirmatory evidence for a new
threshold hypothesis**. It must receive a separate prior-art audit and independent
validation before promotion.

## Claim boundary

- Do not describe the rejected intermediate rescue-window hypothesis as supported.
- Do not infer a causal behavioral threshold from these observational bins.
- Do not alter the current Ecology Letters Letter on this result alone.
- Preserve the zero-inclusive distinction: conditional robbery share can rise while
  absolute robbery rate does not.
