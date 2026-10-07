# Gate A first-open result — ecological stability / evolutionary transience

Status: **KILLED AT GATE A** (frozen v2 rule). Do not proceed to Gate B.
Run: https://github.com/zuizui0223/bita/actions/runs/37639638223
Artifact: https://github.com/zuizui0223/bita/actions/runs/37639638223/artifacts/11491732658
Run head SHA: `0c48b7997aa86676e345e6d9ebebb0b590590015`
Analysis: `scripts/analyze_hummingbird_clinger_speciation_gate_a.py`
Pre-outcome contract: `ECOLOGICAL_STABILITY_EVOLUTIONARY_TRANSIENCE_PREREG_V2_AMENDMENT.md`.
This is a post-result report; it must not edit or retroactively change the preregistration.

## Frozen primary results

| Check | Actual |
|---|---|
| Colwell state table | 220 species, 66 clingers, 44 bypass-capable |
| Barreto rates | 362 species |
| Species matched | 178; 64 clingers |
| Complete primary models | n=168 per estimator |
| BAMM standardized clinger coefficient | -0.019478281731294234 |
| BAMM one-sided within-clade permutation p | 0.1459 |
| ClaDS standardized clinger coefficient | -0.13311244890612906 |
| ClaDS one-sided within-clade permutation p | 0.1071 |
| Median coefficient, both estimator families | -0.07629536531871164 |
| Estimator families with negative coefficients | 2/2 |
| Median coefficient excluding Coquettes | **+0.024708379934342557** |
| Frozen gate_a_pass | **false** |
| Frozen decision | `KILL_TRANSIENCE_HYPOTHESIS_UNDER_FROZEN_GATE` |

Expected DR third family was **not available through the frozen script's published-variable eligibility filter**. Two families were analyzed. Those estimators share biological data and are not independent biological replication.

## Biological reading

Neither BAMM nor ClaDS supplies strong one-sided within-clade permutation evidence for a residual negative clinger effect. More decisively, the directional median reverses after the prespecified Coquettes exclusion. This is incompatible with a robust, clade-portable negative clinger diversification association under the frozen test. It does **not** prove that clingers and other birds have identical diversification, and it does not measure extinction or evolutionary-stability directly.

Published prior work:
- Colwell et al. 2023 (doi:10.1086/726036): repeated clinging origins and short-bill / long-hallux association; many shallow origins noted descriptively.
- Barreto et al. 2023 (doi:10.1098/rspb.2022.1793): trait correlates of hummingbird speciation including faster speciation in short-billed birds.
- Duchenne et al. 2023 (doi:10.1371/journal.pbio.3002434): innovative cheating can improve **community** persistence in specified ecological conditions, not a lineage-speciation result.

## Evidence and method boundaries

- Clinger is an observed published feeding-style state, not necessarily a robbery event: legitimate clinging, ground use and bypass are not identical biological processes.
- The main beta estimates are associations, not causal effects of robbery.
- Outcome family estimates were derived from the same macroevolutionary system.
- Missing/species-join attrition and independent evaluation of clinger state classification limit external generality.
- Group exclusions weaken the main direction, not merely its significance.
- The complete machine-generated JSON remains the workflow artifact; this markdown extracts the logged main outcomes and is not a substituted machine-readable analysis result.

## Decision

1. Keep frozen H1 as **not promoted**.
2. Do not run Gate B to rescue a killed sign prediction; no outcome-dependent substitution of a new primary endpoint.
3. Do not merge or rewrite the current Ecology Letters access-routing Letter.
4. If a separate ecological hypothesis is proposed, freeze it under its **own** analysis route with separate source audit and a discriminating prediction.

No claim of a macroevolutionary cheating paradox has been established.
