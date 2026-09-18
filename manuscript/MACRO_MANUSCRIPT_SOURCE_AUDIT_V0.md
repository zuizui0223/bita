# BITA macro manuscript source-and-claim audit v0

Candidate manuscript: `manuscript/MANUSCRIPT_FLORAL_DEFENCE_SELECTIVITY_V0.md`

Purpose: map each headline statement to a reproducible source-of-record and freeze its current inference ceiling.

## Claim 1 — matched-D corpus size

Claim:

> 17 independent matched systems; 15 have an effective focal antagonist-reduction route.

Authoritative sources:

- `empirical/floral_defence_selectivity/results/corpus_audit.json`
- `empirical/floral_defence_selectivity/results/premodel_pattern_summary.json`
- `empirical/floral_defence_selectivity/results/analysis_ready_matched_systems.csv`

Status: **REPRODUCIBLE**.

Boundary: this is a screened evidence corpus, not natural prevalence.

## Claim 2 — strict Stage-2 state pattern

Claim:

~~~text
SEPARATED:  2 compatible, 0 impaired
OVERLAPPED: 0 compatible, 1 impaired
Fisher two-sided p = 0.333333
~~~

Authoritative sources:

- `empirical/floral_defence_selectivity/results/stage2_model_gate.json`
- `scripts/run_floral_defence_selectivity_models.py`
- `tests/test_floral_defence_selectivity_models.py`

Status: **REPRODUCIBLE / DESCRIPTIVE_EXACT_ONLY**.

Boundary: n=3. No universal effect and no significant cross-system claim.

## Claim 3 — null-compatible sensitivity

Claim:

~~~text
SEPARATED compatible-or-null = 6
OVERLAPPED impaired = 1
Fisher two-sided p = 0.142857
~~~

Authoritative source:

- `empirical/floral_defence_selectivity/results/stage2_model_gate.json`

Status: **REPRODUCIBLE SENSITIVITY**.

Boundary: `NO_DETECTED_CHANGE != PRESERVED_OR_IMPROVED`; never use the sensitivity table as evidence of equivalence.

## Claim 4 — domain versus modality remains unidentified

Claim:

> the strict systems perfectly confound domain relation and broad defence modality.

Source:

- `empirical/floral_defence_selectivity/STAGE2_MODEL_GATE_V1.md`

Strict rows:

~~~text
Thunia        SEPARATED   physical   compatible
Caryopteris   SEPARATED   physical   compatible
Gelsemium     OVERLAPPED  chemical   impaired
~~~

Status: **REPRODUCIBLE NEGATIVE IDENTIFICATION RESULT**.

Boundary: do not claim domain structure outperforms chemical/physical modality.

## Claim 5 — defence-side conditionality

Claim:

> eight independent D-side systems change realised state across dose/expression, exposure/reward context, consumer identity, response stage, or temporal expression.

Sources:

- `empirical/floral_defence_selectivity/d_side_conditionality_registry.csv`
- `empirical/floral_defence_selectivity/D_SIDE_CONDITIONALITY_READOUT_V1.md`
- `empirical/mechanism_pattern_synthesis/SIGN_SWITCH_LEDGER_V1.csv`

Status: **SOURCE-ADJUDICATED RECURRENCE**.

Boundary: heterogeneous outcomes are not pooled; no universal numerical threshold ratio.

## Claim 6 — Sakhalkar community-scale route switching

Claim:

~~~text
raw workbook rows = 18,440
source-script filtered rows = 14,383
visited species = 183
trait-matched species = 182
cheating species with tube length = 57
rho = 0.3467862681
permutation p = 0.0086
~~~

Sources:

- `empirical/floral_defence_selectivity/results/sakhalkar2023_network_result.json`
- `scripts/analyze_sakhalkar2023_network.py`
- public data DOI `10.5281/zenodo.8398202`
- source paper DOI `10.1002/ecs2.4696`

Status: **PUBLIC-DATA REANALYSIS REPRODUCED IN CI**.

Boundary: observational species-level association, not a causal defence manipulation. The deposited workbook gives 14,383 after the source-script filter, eight fewer than the 14,391 visits stated in the publication summary.

## Claim 7 — route-specific tube-length contrast

Claim:

~~~text
robber-only median tube length = 2.0892833335
thief-only median tube length = 0.6766
~~~

Source:

- `empirical/floral_defence_selectivity/results/sakhalkar2023_network_result.json`

Status: **REPRODUCIBLE DESCRIPTIVE CONTRAST**.

Boundary: approximately threefold is descriptive only, not a second inferential test.

## Claim 8 — post-rule evidence

Claim:

> two systematic-expansion systems, one registered hold-out, and one independently assembled network provide post-rule evidence without being pooled into a success rate.

Source:

- `empirical/floral_defence_selectivity/POST_RULE_VALIDATION_READOUT_V1.md`

Status: **AUDITED**.

Boundary: Caryopteris supportive; Phlox null-compatible; Erica directionally supportive but unresolved; Sakhalkar independent access-routing evidence.

## Claim 9 — Kessler 2015 bridge

Claim:

> consumer identity changes the mutualist cost of the same nectar-restriction architecture; the historical source-mean A×D sign also changes among pollinator contexts.

Sources:

- `empirical/floral_defence_selectivity/KESSLER_2015_LEGACY_RESULT_BRIDGE_V1.md`
- `empirical/mechanism_pattern_synthesis/KESSLER_2015_DIRECT_AXD_ACCESS_LIMITATION_AUDIT_V1.md`

Status: **PRESERVED LEGACY BRIDGE**.

Boundary: no increment to matched-D N; nectar absence remains a reward/access restriction and is not silently redefined as a conventional defence.

## Claim 10 — effective-exposure theory

Claim:

> a selective window exists in the model when tau_H/q_H < x < tau_P/q_P.

Source:

- `docs/EFFECTIVE_EXPOSURE_SELECTIVITY_THEORY_V1.md`

Status: **THEORETICAL DERIVATION / QUALITATIVE PREDICTION**.

Boundary: q_H, q_P, tau_H and tau_P are not estimated as universal empirical constants.

## Claim 11 — legacy BITA preservation

Preserved source-of-record objects include:

- 56 directional route records / 25 independent biological clusters;
- 17-system high-information identification frontier;
- Kessler 2008 bounds and direct-factorial work;
- identified sets and partial-identification logic;
- crossed-intervention and separability framework;
- larceny quantitative synthesis.

Sources remain under `empirical/mechanism_pattern_synthesis/`, `manuscript/supplementary/`, and the unchanged canonical manuscript.

Status: **PRESERVED, NOT SUPERSEDED**.

## Manuscript promotion decision

Current candidate status:

~~~text
science spine:                 PRESENT
public network result:         REPRODUCED
Stage-2 exact gate:            REPRODUCED
focused search expansion:      BOUNDED / strict increment 0
focused references:            PRESENT
four-figure plan:              PRESENT
candidate manuscript v0:       PRESENT
canonical replacement:         NOT YET
~~~

Remaining promotion decisions are editorial: final figure QA, target-journal selection, final bibliography/style normalization, and explicit promotion of the candidate manuscript. None licenses altering the frozen scientific claim ceilings above.
