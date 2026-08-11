# Mechanism-pattern synthesis completion status v2

## Scope and source of truth

This file reconciles the gate status after the later Gate A, C, E, and F receipts superseded older intermediate status notes.

Canonical integration line at first A–H adjudication:

```text
PR:     #126
branch: agent/mechanism-pattern-universality-v1
head:   5b4b877bf3c601f0f4ccad8fb35c65f1b99bc605
```

The fixed theory and existing manuscript were not changed to obtain the gate decisions.

## A–H gate matrix

| Gate | Status | Canonical basis | Remaining scientific blocker |
|---|---|---|---|
| **A — direct `A x D` search** | **PASS** | `DIRECT_AXD_SATURATION_RECEIPT_V1.md` | none; one strict direct cluster remains unresolved, which is itself the bounded evidence state |
| **B — four marginal mechanism families** | **PASS** | `MECHANISM_COVERAGE_AUDIT_V1.md` | none; all four routes have explicit source-adjudicated empirical states |
| **C — two quantitative modules** | **PASS** | Leal 2025 larceny module pinned to immutable commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82` + `SASIDHARAN_2023_REPRO_READOUT_V1.md` | none |
| **D — sign switching / conditionality** | **PASS** | `SIGN_SWITCH_LEDGER_V1.csv` + `CONDITIONALITY_ONTOLOGY_V1.md` | none at current evidence capacity; cross-outcome meta-regression is intentionally not manufactured |
| **E — same-system multi-route evidence** | **PASS** | `SAME_SYSTEM_REGIME_READOUT_V1.md` | none; linkage and dependence are explicit |
| **F — direct joint cost** | **PASS as documented gap** | `JOINT_COST_SATURATION_RECEIPT_V1.md` | none; `kappa` remains empirically unidentified, not zero |
| **G — synthesis robustness/bias** | **PASS** | `SYNTHESIS_ROBUSTNESS_AUDIT_V1.md` | none |
| **H — theory/empiricism boundary** | **PASS** | `THEORY_EMPIRICISM_BOUNDARY_AUDIT_V1.md` | none for current synthesis; future manuscript text must preserve the boundary |

## Overall scientific decision

```text
Gates A-H:                   PASS
scientific completion gate: PASS
manuscript resumption:      ALLOWED
```

The empirical endpoint is now a map of **what is recurrent, what is context dependent, and what remains empirically unidentified**, rather than an attempt to estimate the mixed partial by pooling marginal studies.

## Integrated empirical result

1. **mechanism recurrence** — all four theory-facing marginal families have source-adjudicated states across multiple systems;
2. **same-system architecture** — guarded, interference, shared-tracking, antagonist-biased, unresolved, and context-switching states occur in linked systems;
3. **direct evidence scarcity** — the dedicated direct `A x D` search saturates with one strict, sign-unresolved cluster;
4. **conditionality recurrence** — 11 independent context/sign-switch clusters map onto five theory-facing classes without mixing incompatible outcomes into a grand mean;
5. **joint-cost identification gap** — the direct A+D intrinsic-cost search saturates at zero eligible estimates, so `kappa` remains unidentified;
6. **quantitative breadth** — Leal 2025 and Sasidharan 2023 provide two biologically distinct source-audited quantitative synthesis modules with module-appropriate dependence, influence, and robustness checks.

## Operational cleanup status

### CI — resolved

At head `5b4b877bf3c601f0f4ccad8fb35c65f1b99bc605`, all 13 pull-request workflow runs completed successfully, including:

- core `CI` run `31537763981`;
- `submission-scope` run `31537764053`;
- `Build mechanism coverage audit` run `31537764032`;
- `Build same-system regime readout` run `31537763969`;
- `Audit Sasidharan 2023 PMC supplement` run `31537763989`;
- `Audit Garcia 2024 JPE appendices` run `31537763971`.

The preceding García run `31485544283` failed only because the external JPE host closed the connection / produced an HTTP/2 protocol error. The unchanged audit passed on the next PR run, so the failure is treated as transient external transport rather than a code or scientific-audit defect. No transport workaround is added solely to make a one-off network failure disappear.

### Leal module packaging — resolved by immutable pin

`SUPPLEMENT_MANIFEST.md` now fixes the completed Leal larceny module to repository commit:

```text
ed33b25593c0d90ad6657753f6f5501d9efc7b82
```

and enumerates its canonical protocol, readout, effect rows, recomputation audit, results, scripts, modules, and tests. This avoids duplicating or silently changing the completed analysis while making its exact dependency auditable from the #126 integration line.

## Manuscript-entry decision

The original freeze condition in `COMPLETION_GATE_V1.md` is satisfied.

```text
scientific A-H gate:       PASS
CI state:                  GREEN at adjudicated head
quantitative-module pin:   FIXED
manuscript reconstruction: GO
```

The next task is therefore no longer additional evidence hunting by default. It is manuscript reconstruction around the completed evidence architecture, while retaining the Gate H claim boundary.

Recommended Results/Discussion spine:

```text
fixed sign criterion
-> mechanism recurrence
-> same-system regime structure
-> direct A x D scarcity
-> five-class conditionality map
-> quantitative module 1: antagonist-pressure gate
-> quantitative module 2: FVOC mutualist/antagonist response architecture
-> direct joint-cost evidence gap
-> identification boundary and empirical predictions
```

No new theory term or parameter is required for this reconstruction.

## Merge decision

PR #126 remains draft while manuscript reconstruction begins on the integration line. This is a workflow choice, not an unresolved scientific gate. Merging the empirical integration alone would now be technically defensible, but keeping the PR draft avoids splitting the final theory+synthesis narrative across another branch before the manuscript is rebuilt.
