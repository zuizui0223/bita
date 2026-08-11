# Mechanism-pattern synthesis completion status v2

## Scope and source of truth

This file records the completed scientific and manuscript-integration state of PR #126 after the later Gate A, C, D, E, F, G, and H receipts superseded older intermediate status notes.

Canonical integration line:

```text
PR:     #126
branch: agent/mechanism-pattern-universality-v1
```

First A–H scientific adjudication occurred before manuscript reconstruction. The theory was kept fixed to obtain those gate decisions. Manuscript reconstruction then proceeded only after the freeze rule in `COMPLETION_GATE_V1.md` was satisfied.

## A–H gate matrix

| Gate | Status | Canonical basis | Remaining scientific blocker |
|---|---|---|---|
| **A — direct `A x D` search** | **PASS** | `DIRECT_AXD_SATURATION_RECEIPT_V1.md` | none; one strict direct cluster remains sign-unresolved, which is itself the bounded evidence state |
| **B — four marginal mechanism families** | **PASS** | `MECHANISM_COVERAGE_AUDIT_V1.md` | none; all four routes have explicit source-adjudicated empirical states |
| **C — two quantitative modules** | **PASS** | Leal 2025 larceny module pinned to immutable commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82` + `SASIDHARAN_2023_REPRO_READOUT_V1.md` | none |
| **D — sign switching / conditionality** | **PASS** | `SIGN_SWITCH_LEDGER_V1.csv` + `CONDITIONALITY_ONTOLOGY_V1.md` | none at current evidence capacity; cross-outcome meta-regression is intentionally not manufactured |
| **E — same-system multi-route evidence** | **PASS** | `SAME_SYSTEM_REGIME_READOUT_V1.md` | none; linkage and dependence are explicit |
| **F — direct joint cost** | **PASS as documented gap** | `JOINT_COST_SATURATION_RECEIPT_V1.md` | none; `kappa` remains empirically unidentified, not zero |
| **G — synthesis robustness/bias** | **PASS** | `SYNTHESIS_ROBUSTNESS_AUDIT_V1.md` | none |
| **H — theory/empiricism boundary** | **PASS** | `THEORY_EMPIRICISM_BOUNDARY_AUDIT_V1.md` | none for current synthesis; manuscript and submission materials preserve the boundary |

## Overall scientific decision

```text
Gates A-H:                   PASS
scientific completion gate: PASS
additional evidence search: NOT A DEFAULT BLOCKER
```

The empirical endpoint is a map of **what is recurrent, what is context dependent, and what remains empirically unidentified**, rather than an attempt to estimate the mixed partial by pooling marginal studies.

## Integrated empirical result

1. **mechanism recurrence** — all four theory-facing marginal families have source-adjudicated states across multiple systems;
2. **same-system architecture** — guarded, interference, shared-tracking, antagonist-biased, unresolved, and context-switching states occur in linked systems;
3. **direct evidence scarcity** — the dedicated direct `A x D` search saturates with one strict, sign-unresolved cluster;
4. **conditionality recurrence** — 11 independent context/sign-switch clusters map onto five theory-facing classes without mixing incompatible outcomes into a grand mean;
5. **joint-cost identification gap** — the direct A+D intrinsic-cost search saturates at zero eligible estimates, so `kappa` remains unidentified;
6. **quantitative breadth** — Leal 2025 and Sasidharan 2023 provide two biologically distinct source-audited quantitative synthesis modules with module-appropriate dependence, influence, and robustness checks.

The mechanism-coverage architecture contains 38 source-adjudicated effect/directional records across 14 independent biological study clusters, including ten same-system multi-route clusters. These are evidence-capacity counts within the screened architecture, not prevalence estimates.

## Quantitative-module packaging

### Leal et al. 2025 — immutable dependency

`SUPPLEMENT_MANIFEST.md` fixes the completed larceny module to repository commit:

```text
ed33b25593c0d90ad6657753f6f5501d9efc7b82
```

and enumerates the canonical protocol, readout, effect rows, recomputation audit, results, scripts, modules, and tests. The integration line does not silently recompute or alter that completed module for directory consistency.

### Sasidharan et al. 2023 — canonical current-branch reconstruction

The canonical dependence structure is the conservatively recovered 32-study-component citation topology. The admitted module retains the current-deposit versus printed-source discrepancies, 32/32 leave-one-component-out positive direction for the assembled physiological contrast, the three paired both-role zero differences, and repeated behavioral `+/0` discordance.

## Manuscript reconstruction — completed

The freeze condition has been released and the canonical manuscript has been rebuilt:

- `manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md`
- `manuscript/TABLES_THEORETICAL_ECOLOGY.md`
- `manuscript/README.md`

The reconstructed paper preserves the fixed theory equations, Proposition 1, environmental derivative identities, and all canonical 2,592-evaluation finite-sensitivity numbers. It replaces the obsolete statement that the literature layer is abstract-only preliminary context with the completed source-adjudicated mechanism-pattern synthesis.

The manuscript-facing Results/Discussion spine is now:

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

No new theorem, trait, mechanism, or model parameter was introduced to perform the reconstruction.

## Submission-support integration — completed for scientific narrative

The following have been updated from theory-only / preliminary-literature framing to the integrated paper:

- root `README.md`;
- `SUPPLEMENT_MANIFEST.md`;
- `docs/SUBMISSION_SCOPE.md`;
- `docs/FINAL_SUBMISSION_AUDIT.md`;
- `submission/COVER_LETTER_THEORETICAL_ECOLOGY.md`;
- `submission/FIGURE_AND_TABLE_PLAN.md`;
- `submission/SUBMISSION_CHECKLIST.md`;
- `submission/MANUSCRIPT_AUDIT_V2.md` (content now audit v3);
- `submission/TARGET_JOURNAL_STRATEGY.md`;
- narrative and submission-spine regression tests.

The first journal target remains *Theoretical Ecology*, with the theory kept as the organizing contribution and the empirical synthesis presented as a theory-facing identification/evidence architecture rather than a prevalence survey.

## CI and external-source transport

### Validated manuscript-integration checkpoint

At integration head

```text
c3a6f12b1ac4a6b92414150ec87db35455ffc5f9
```

all **13/13** pull-request workflows completed successfully.

Key successful runs at that checkpoint:

```text
CI                                      31540017238
submission-scope                        31540017288
Build mechanism coverage audit          31540017212
Build same-system regime readout         31540017240
Audit Sasidharan 2023 PMC supplement     31540017244
Audit Garcia 2024 JPE appendices         31540017250
```

Core CI passed on Python 3.10, 3.11, and 3.12.

### García 2024 transport hardening

The JPE/OJS endpoint repeatedly produced the same failure pattern on GitHub-hosted runners:

```text
urllib: RemoteDisconnected
curl:   HTTP/2 PROTOCOL_ERROR
```

Because this recurred after an earlier transient success, `scripts/audit_garcia2024_appendices.py` was hardened at the transport layer only: curl fallback is forced to HTTP/1.1, closes connections, and uses bounded retries. Article-declared source URLs, parsed content, and scientific adjudication logic were not changed. The audit then passed at the validated checkpoint above.

## Theory/empiricism boundary after manuscript reconstruction

The integrated manuscript and repository tests enforce that:

```text
marginal route evidence != W_AD
same-system multi-route evidence != direct A x D
publication/study counts != model parameters
deposit or screened-set fractions != prevalence in nature
finite-grid occupancy != prevalence in nature
one direct A x D cluster != universal interaction sign
zero direct joint-cost studies != kappa = 0
```

The two quantitative synthesis modules support the biological reality and conditionality of constituent mechanisms; they do not empirically calibrate the complete mixed partial.

## Remaining work before portal submission

Scientific evidence hunting is no longer the default next task. Remaining work is presentation/reproducibility packaging:

1. build the manuscript-facing Figure 3 empirical mechanism-pattern architecture;
2. regenerate final Figure 2 and produce final vector exports for Figures 1-3;
3. complete primary-source/reference metadata verification and journal formatting;
4. supply author order, affiliations, ORCIDs, CRediT, funding, acknowledgements, and conflict confirmation;
5. create the exact submission release and archival DOI;
6. run final CI on the final figure/reference/archive-preparation commit.

If final source verification exposes a specific material evidence error or a genuinely new strict direct-design candidate, the corresponding evidence gate can be reopened. Otherwise, additional broad searching should not displace final manuscript preparation.

## Merge decision

```text
scientific A-H gate:        PASS
manuscript reconstruction:  COMPLETE
submission narrative:       INTEGRATED
validated CI checkpoint:    GREEN 13/13
PR #126:                    KEEP DRAFT during final figure/reference packaging
merge to main:              technically defensible after final package check
portal submission:          not yet; author metadata + figures + references + archive DOI remain
```

Keeping PR #126 draft is now a workflow choice for final package consolidation, not an unresolved scientific gate.
