# Mechanism-pattern synthesis completion status v2

## Scope and source of truth

This file reconciles the gate status after the later Gate A, C, E, and F receipts superseded older intermediate status notes.

Canonical integration line at adjudication start:

```text
PR:     #126
branch: agent/mechanism-pattern-universality-v1
head:   ec8e531c82678bfb0ec895d79bf498613910ed10
```

The fixed theory and existing manuscript are not changed by this adjudication.

## A–H gate matrix

| Gate | Status | Canonical basis | Remaining scientific blocker |
|---|---|---|---|
| **A — direct `A x D` search** | **PASS** | `DIRECT_AXD_SATURATION_RECEIPT_V1.md` | none; one strict direct cluster remains unresolved, which is itself the bounded evidence state |
| **B — four marginal mechanism families** | **PASS** | `MECHANISM_COVERAGE_AUDIT_V1.md` | none; all four routes have explicit source-adjudicated empirical states |
| **C — two quantitative modules** | **PASS** | Leal 2025 larceny module pinned to PR #124 + `SASIDHARAN_2023_REPRO_READOUT_V1.md` | none; modules are biologically distinct and independently audited |
| **D — sign switching / conditionality** | **PASS** | `SIGN_SWITCH_LEDGER_V1.csv` + `CONDITIONALITY_ONTOLOGY_V1.md` | none at current evidence capacity; cross-outcome meta-regression is intentionally not manufactured |
| **E — same-system multi-route evidence** | **PASS** | `SAME_SYSTEM_REGIME_READOUT_V1.md` | none; linkage and dependence are explicit |
| **F — direct joint cost** | **PASS as documented gap** | `JOINT_COST_SATURATION_RECEIPT_V1.md` | none; `kappa` remains empirically unidentified, not zero |
| **G — synthesis robustness/bias** | **PASS** | `SYNTHESIS_ROBUSTNESS_AUDIT_V1.md` | none scientifically; module-1 assets still need final repository packaging/consolidation |
| **H — theory/empiricism boundary** | **PASS** | `THEORY_EMPIRICISM_BOUNDARY_AUDIT_V1.md` | none for current synthesis; future manuscript text must preserve the boundary |

## Overall scientific decision

```text
Gates A-H:                   PASS
scientific completion gate: PASS
manuscript resumption:      ALLOWED
PR #126 merge readiness:    NOT YET
```

The manuscript freeze condition defined in `COMPLETION_GATE_V1.md` is now scientifically satisfied. This does **not** mean PR #126 should be merged immediately or that the manuscript should be edited before repository hygiene is restored.

## What the integrated empirical result now is

The empirical half no longer rests on the claim that one marginal route has a universal sign.

Instead it supports a layered result:

1. **mechanism recurrence** — all four theory-facing marginal families are source-adjudicated across multiple systems;
2. **same-system architecture** — guarded, interference, shared-tracking, antagonist-biased, and context-switching states co-occur in linked biological systems;
3. **direct evidence scarcity** — the dedicated direct `A x D` search saturates with one strict, sign-unresolved cluster;
4. **conditionality recurrence** — 11 independent sign-switch/context clusters map onto five theory-facing classes without mixing incompatible outcomes into a grand mean;
5. **joint-cost identification gap** — the direct A+D intrinsic-cost search saturates at zero eligible estimates, so `kappa` remains unidentified;
6. **quantitative breadth** — Leal 2025 and Sasidharan 2023 provide two biologically distinct source-audited quantitative synthesis modules with appropriate dependence/influence/robustness limits.

That architecture is sufficient for the intended theory + empirical-synthesis paper because the empirical claim is now **what is general, what is context dependent, and what remains unidentified**, rather than a claim that the mixed partial itself has been meta-analytically estimated.

## Operational work still required before merging #126

These tasks are deliberately separated from the A–H scientific gate.

### 1. Restore green CI for the García 2024 appendix audit

Current head has one failing workflow, `Audit Garcia 2024 JPE appendices`. The failure is transport-level, not a failed scientific assertion:

```text
urllib: RemoteDisconnected
curl:   HTTP/2 PROTOCOL_ERROR after retries
```

The focused repair should harden transport (prefer HTTP/1.1 and bounded retry/backoff) without changing source URLs, biological filters, or adjudication logic.

### 2. Package the Leal quantitative module on the final integration line

The Leal implementation is currently pinned to PR #124. Before final merge/submission, either:

- port the canonical larceny analysis/readout assets into the final integration branch; or
- preserve the immutable source commit/path as an explicit supplemental dependency.

Do not recompute a new effect merely for packaging consistency.

### 3. Rebuild the manuscript around the completed evidence architecture

Once operational checks are green, manuscript reconstruction may resume under `THEORY_EMPIRICISM_BOUNDARY_AUDIT_V1.md`.

The new Results/Discussion spine should be:

```text
fixed sign criterion
-> mechanism recurrence
-> same-system regime structure
-> direct A x D scarcity
-> five-class conditionality map
-> quantitative module 1: antagonist-pressure gate
-> quantitative module 2: FVOC mutualist/antagonist response architecture
-> joint-cost evidence gap
-> identification boundary and empirical predictions
```

No new theory term or parameter is required for this reconstruction.

## Current stop/go decision

**GO for manuscript reconstruction after operational cleanup.**

**NO-GO for merging PR #126 while the García audit workflow is red and module-1 packaging remains unresolved.**
