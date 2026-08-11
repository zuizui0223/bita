# Supplement manifest — theory + mechanism-pattern synthesis

This manifest is the canonical map for the integrated theory + empirical-synthesis line in PR #126 (`agent/mechanism-pattern-universality-v1`). It supersedes the older manifest framing in which the literature layer was only preliminary collateral context.

## 1. Fixed theoretical core

Primary local sign criterion, assumptions, and positioning:

- `docs/GENERAL_SIGN_CRITERION.md`
- `docs/NOVELTY_POSITIONING.md`
- `docs/BACKGROUND_NOVELTY_GAP_REVIEW.md`
- `theory/README.md`
- `trait_architecture/sign_criterion.py`
- `tests/test_sign_criterion.py`

Implemented corollary and finite-set sensitivity:

- `trait_architecture/model.py`
- `trait_architecture/robustness.py`
- `configs/part_i_robustness_grid.json`
- `scripts/run_part_i_robustness.py`
- `docs/PART_I_ROBUSTNESS_PROTOCOL.md`
- `empirical/part_i_robustness/PART_I_SENSITIVITY_READOUT_V2.md`

Boundary: finite-grid occupancies are declared-set sensitivities, not probabilities or prevalence in nature.

## 2. Mechanism-pattern empirical protocol and completion gate

Canonical empirical architecture:

- `empirical/mechanism_pattern_synthesis/PROTOCOL_V1.md`
- `empirical/mechanism_pattern_synthesis/COMPLETION_GATE_V1.md`
- `empirical/mechanism_pattern_synthesis/COMPLETION_STATUS_V2.md`
- `empirical/mechanism_pattern_synthesis/SEARCH_REGISTRY_V1.csv`
- `empirical/mechanism_pattern_synthesis/LEDGER_SCHEMA_V1.csv`
- `empirical/mechanism_pattern_synthesis/MECHANISM_COVERAGE_AUDIT_V1.md`

The scientific completion gate is A–H PASS. The empirical endpoint is a map of what is recurrent, what is context dependent, and what remains unidentified; it is not a meta-analytic estimate of the mixed partial.

## 3. Direct interaction and same-system evidence

Direct `A x D` search and bounded evidence gap:

- `empirical/mechanism_pattern_synthesis/DIRECT_AXD_AUDIT_V1.csv`
- `empirical/mechanism_pattern_synthesis/DIRECT_AXD_SATURATION_RECEIPT_V1.md`

Same-system architecture:

- `empirical/mechanism_pattern_synthesis/SAME_SYSTEM_REGIME_READOUT_V1.md`

The one strict current direct cluster (`Impatiens capensis`) is direct but sign-unresolved across reproductive components. Same-system marginal co-occurrence is never relabelled as direct interaction evidence.

## 4. Conditionality / sign-switch layer

- `empirical/mechanism_pattern_synthesis/SIGN_SWITCH_LEDGER_V1.csv`
- `empirical/mechanism_pattern_synthesis/CONDITIONALITY_ONTOLOGY_V1.md`

Eleven independent study clusters are mapped into five theory-facing classes: trait intensity/expression, resource/exposure context, consumer identity/role, response definition/stage/scale, and compound identity/mechanism partition. The project does not manufacture a cross-outcome moderator coefficient.

## 5. Direct joint-cost evidence state

- `empirical/mechanism_pattern_synthesis/JOINT_COST_SEARCH_PROTOCOL_V1.md`
- `empirical/mechanism_pattern_synthesis/JOINT_COST_AUDIT_V1.csv`
- `empirical/mechanism_pattern_synthesis/JOINT_COST_SATURATION_RECEIPT_V1.md`

Strict simultaneous A+D intrinsic-cost estimates: zero under the saturated registered search. `kappa` is therefore unidentified, not estimated as zero.

## 6. Quantitative synthesis module 1 — Leal et al. 2025 floral larceny

To avoid silently reimplementing a completed analysis, the exact canonical module is pinned to an immutable commit in this repository:

```text
PR:                 #124
branch at creation: claude/attraction-defense-conditional-olom0x
canonical commit:   ed33b25593c0d90ad6657753f6f5501d9efc7b82
preregistration:    0e36eac
first results:      965d657
source synthesis:   Leal et al. 2025, Ecology, doi:10.1002/ecy.70036
```

Canonical files at commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`:

- `empirical/broad_reality_evidence/larceny_gate/LARCENY_GATE_PROTOCOL_V1.md`
- `empirical/broad_reality_evidence/larceny_gate/LARCENY_GATE_READOUT_V1.md`
- `empirical/broad_reality_evidence/larceny_gate/larceny_effect_rows.csv`
- `empirical/broad_reality_evidence/larceny_gate/larceny_ingest_diagnostics.json`
- `empirical/broad_reality_evidence/larceny_gate/larceny_recomputation_audit.csv`
- `empirical/broad_reality_evidence/larceny_gate/larceny_moderator_registry.csv`
- `empirical/broad_reality_evidence/larceny_gate/larceny_moderator_coding.csv`
- `empirical/broad_reality_evidence/larceny_gate/results/`
- `scripts/ingest_deposited_larceny_dataset.py`
- `scripts/run_larceny_gate.py`
- `scripts/run_context_dependence.py`
- `trait_architecture/deposited_effect_ingest.py`
- `trait_architecture/context_dependence.py`
- `tests/test_deposited_effect_ingest.py`
- `tests/test_context_dependence.py`
- `tests/test_larceny_gate_declaration.py`

Reproduction is intentionally pinned to that commit so later changes on PR #126 cannot alter the completed module by accident.

Key admitted results are summarized, with limitations, in `empirical/mechanism_pattern_synthesis/SYNTHESIS_ROBUSTNESS_AUDIT_V1.md` and registered in `SECONDARY_SYNTHESIS_MODULES_V1.csv`.

## 7. Quantitative synthesis module 2 — Sasidharan et al. 2023 FVOCs

Canonical current-branch readout:

- `empirical/mechanism_pattern_synthesis/SASIDHARAN_2023_REPRO_READOUT_V1.md`
- `empirical/mechanism_pattern_synthesis/SECONDARY_SYNTHESIS_MODULES_V1.csv`

Canonical audit/reconstruction code:

- `scripts/audit_sasidharan2023_pmc_supplement.py`
- `scripts/audit_sasidharan2023_s1_domains.py`
- `scripts/audit_sasidharan2023_citation_topology.py`
- `scripts/reconstruct_sasidharan2023_fvoc.py`
- `scripts/adjudicate_sasidharan2023_gate_c.py`
- `.github/workflows/audit-sasidharan2023-pmc-supplement.yml`

Canonical adjudication: `PASS_AS_DEPOSITED_REANALYSIS`. The 32-component citation topology is the dependence source of record; current-deposit vs printed-source discrepancies remain explicit.

## 8. Robustness and theory–empiricism boundary

- `empirical/mechanism_pattern_synthesis/SYNTHESIS_ROBUSTNESS_AUDIT_V1.md`
- `empirical/mechanism_pattern_synthesis/THEORY_EMPIRICISM_BOUNDARY_AUDIT_V1.md`

Required boundaries:

- marginal routes do not estimate `W_AD`;
- module counts do not estimate model parameters;
- screened-set/deposit proportions are not prevalence;
- the single direct interaction is not generalized;
- incompatible outcomes are not averaged into a grand mean;
- absence of a joint-cost study does not imply `kappa = 0`.

## 9. Source-specific public-data audits

The integration branch contains bounded source audits/reconstructions for high-information systems including `Impatiens`, `Aconitum`, `Nicotiana`, `Cucurbita`, García 2024, and others under `empirical/mechanism_pattern_synthesis/` plus matching scripts/workflows.

A failed external download is treated as source availability, not as biological evidence. The García 2024 JPE appendix workflow showed one transient transport failure on run `31485544283` and then passed unchanged on run `31537763971`, so no scientific or transport-code change was made in response to that one-off failure.

## 10. Deliberately not promoted

The following are not primary submission claims:

- abstract-only broad-route directional fractions from the earlier preliminary literature layer;
- publication counts as biological parameter estimates;
- finite-grid regime percentages as empirical frequencies;
- cross-organ defence substituted for flower-specific D;
- dual-function single traits substituted for an independently varied A+D design;
- unrelated marginal studies algebraically combined into a mixed partial.

Raw third-party observation files that are not licensed or necessary to retain are not committed merely for convenience. Source-audit workflows prefer aggregate/schema products and immutable external/source identifiers where appropriate.
