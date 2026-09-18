# BITA Floral-Defence Selectivity Milestone 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a provenance-preserving, analysis-ready matched floral-defence dataset that reuses all existing BITA evidence while adding a separate macro-analysis layer.

**Architecture:** Add `empirical/floral_defence_selectivity/` as a new module. Existing `mechanism_pattern_synthesis`, identification, route-ledger, Kessler bounds, 56/25/17 synthesis, and manuscript files remain untouched in Milestone 1 and are treated as immutable provenance inputs. Architecture codes and outcome codes are stored separately, joined only by a deterministic build script that validates independence and reports Stage-1/Stage-2 sample sizes.

**Tech Stack:** Python 3, stdlib `csv`/`dataclasses`/`pathlib`, pytest, existing BITA package conventions.

**Spec:** `docs/superpowers/specs/2026-09-18-bita-floral-defence-selectivity-macro-design.md`

## Global Constraints

- Do not delete, rewrite, or demote existing BITA empirical/theory/manuscript provenance in Milestone 1.
- New science lives under `empirical/floral_defence_selectivity/`; old evidence files remain source-of-record.
- Architecture coding and outcome coding must be physically separate.
- Outcome information must never be required to construct `pre_outcome_domain_code`.
- Repeated doses, outcomes, years, populations, and consumers do not become independent clusters automatically.
- `NO_DETECTED_CHANGE` must not be silently promoted to `PRESERVED_OR_IMPROVED`.
- Every registry row must cite at least one existing repository provenance path.
- No manuscript claim changes until Milestone 1 dataset and audits are green.

---

### Task 1: Add the selectivity module contract and schema validator

**Files:**
- Create: `empirical/floral_defence_selectivity/README.md`
- Create: `empirical/floral_defence_selectivity/DATA_CONTRACT.md`
- Create: `trait_architecture/floral_defence_selectivity.py`
- Create: `tests/test_floral_defence_selectivity_data_contract.py`

**Interfaces:**
- Produces: `load_csv_rows(path: Path) -> list[dict[str, str]]`
- Produces: `validate_registry(rows) -> list[str]`
- Produces: `validate_architecture_codes(rows) -> list[str]`
- Produces: `validate_outcome_codes(rows) -> list[str]`
- Produces: frozen value sets `DOMAIN_CODES`, `COHORTS`, `UNCERTAINTY_CLASSES`, `POLLINATOR_STATES`

- [ ] **Step 1: Write failing schema tests**

Test that:
- a registry row missing `study_cluster_id` fails;
- an architecture row with an unsupported domain code fails;
- an outcome row using `PRESERVED_OR_IMPROVED` with `NULL_COMPATIBLE` uncertainty fails unless an explicit equivalence/source-supported preservation flag is present;
- valid minimal rows pass.

- [ ] **Step 2: Run the focused test**

Run:
```bash
pytest tests/test_floral_defence_selectivity_data_contract.py -v
```

Expected: FAIL because `trait_architecture.floral_defence_selectivity` does not yet exist.

- [ ] **Step 3: Implement the minimal validator**

Use explicit required-column sets and controlled vocabularies. Return human-readable validation errors; do not mutate input rows.

- [ ] **Step 4: Run the focused test again**

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add empirical/floral_defence_selectivity trait_architecture/floral_defence_selectivity.py tests/test_floral_defence_selectivity_data_contract.py
git commit -m "feat: add floral defence selectivity data contract"
```

---

### Task 2: Create provenance-preserving matched-system and architecture registries

**Files:**
- Create: `empirical/floral_defence_selectivity/matched_system_registry.csv`
- Create: `empirical/floral_defence_selectivity/architecture_codes.csv`
- Create: `tests/test_floral_defence_selectivity_no_outcome_leakage.py`
- Modify: `trait_architecture/floral_defence_selectivity.py`

**Interfaces:**
- Produces: `registry_key(row) -> tuple[str, str, str]`
- Produces: `validate_no_outcome_leakage(architecture_rows) -> list[str]`

- [ ] **Step 1: Seed the registry from already-adjudicated systems**

Include at minimum:
`Catalpa_speciosa`, `Pedicularis_rex`, `Thunia_alba`, `Codonopsis_lanceolata`, `Chrysothemis_friedrichsthaliana`, `Bejaria_resinosa`, `Polemonium_viscosum`, `Aconitum_lycoctonum`, `Asclepias_spp`, `Gelsemium_sempervirens`, `Nicotiana_attenuata_2007`, and `Salvia_boundary`.

Each row must include:
```text
study_cluster_id,publication_id,plant_taxon,D_axis_id,context_id,
derivation_or_holdout,source_provenance_path
```

- [ ] **Step 2: Add architecture-only fields**

Populate `architecture_codes.csv` from the committed outcome-blind moderator matrix and source-method audits only:
```text
study_cluster_id,D_axis_id,context_id,pre_outcome_domain_code,
separating_coordinate,defence_modality,antagonist_guild,pollinator_guild,
observational_or_experimental,architecture_basis_path
```

- [ ] **Step 3: Write failing anti-leakage tests**

Fail if architecture rows contain any forbidden outcome fields or tokens:
`observed_state`, `effect_value`, `effect_direction`, `validation_result`, `p_value`, `pollinator_cost_state`, `selectivity_state`.

- [ ] **Step 4: Implement leakage validation and run tests**

Run:
```bash
pytest tests/test_floral_defence_selectivity_no_outcome_leakage.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add empirical/floral_defence_selectivity/architecture_codes.csv empirical/floral_defence_selectivity/matched_system_registry.csv trait_architecture/floral_defence_selectivity.py tests/test_floral_defence_selectivity_no_outcome_leakage.py
git commit -m "data: register outcome-blind floral defence architectures"
```

---

### Task 3: Add outcome codes without collapsing old results

**Files:**
- Create: `empirical/floral_defence_selectivity/outcome_codes.csv`
- Create: `empirical/floral_defence_selectivity/quantitative_effects.csv`
- Create: `tests/test_floral_defence_selectivity_orientation.py`
- Modify: `trait_architecture/floral_defence_selectivity.py`

**Interfaces:**
- Produces: `derive_defence_state(row) -> str`
- Produces: `derive_pollinator_state(row) -> str`
- Produces: `orient_effect(role: str, raw_value: float, raw_orientation: str) -> float`

- [ ] **Step 1: Encode source-supported outcome states**

For each registry key, preserve:
```text
antagonist_outcome_type,antagonist_effect_direction,antagonist_uncertainty_class,
pollinator_outcome_type,pollinator_response_stage,pollinator_effect_direction,
pollinator_uncertainty_class,source_inference,outcome_basis_path
```

Use `NO_DETECTED_CHANGE` where the source supports only a null-compatible result; do not call it equivalence.

- [ ] **Step 2: Populate compatible numeric effects only**

Seed `quantitative_effects.csv` with already reconstructed effects such as Catalpa LRRs and Thunia LRRs. Keep Pedicularis source coefficients on their original declared scales with a metric label; do not subtract incompatible coefficients.

- [ ] **Step 3: Write orientation tests**

Verify that:
- antagonist suppression is oriented plant-beneficial positive in analysis-ready output;
- pollinator impairment is oriented plant-detrimental;
- raw source coefficients remain recoverable;
- incompatible metrics are never pooled by the orientation helper.

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_floral_defence_selectivity_orientation.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add empirical/floral_defence_selectivity/outcome_codes.csv empirical/floral_defence_selectivity/quantitative_effects.csv trait_architecture/floral_defence_selectivity.py tests/test_floral_defence_selectivity_orientation.py
git commit -m "data: add floral defence outcome and quantitative codes"
```

---

### Task 4: Build the deterministic analysis-ready dataset

**Files:**
- Create: `scripts/build_floral_defence_selectivity_dataset.py`
- Create: `tests/test_floral_defence_selectivity_independence.py`
- Create: `empirical/floral_defence_selectivity/results/.gitkeep`

**Interfaces:**
- CLI:
```bash
python scripts/build_floral_defence_selectivity_dataset.py \
  --input-dir empirical/floral_defence_selectivity \
  --output-dir empirical/floral_defence_selectivity/results
```
- Produces:
  - `results/analysis_ready_matched_systems.csv`
  - `results/corpus_audit.json`
  - `results/provenance_audit.csv`

- [ ] **Step 1: Write failing independence tests**

Verify:
- keys are unique at `study_cluster_id × D_axis_id × context_id`;
- multiple outcomes never increase independent cluster count;
- every joined row has an architecture provenance path and outcome provenance path;
- derivation/holdout cohort is preserved.

- [ ] **Step 2: Run the focused test**

Expected: FAIL because the builder does not exist.

- [ ] **Step 3: Implement the builder**

Join by exact key only. Refuse partial-key joins. Emit an audit with:
```json
{
  "registry_rows": 0,
  "independent_study_clusters": 0,
  "stage1_eligible_clusters": 0,
  "stage2_strict_eligible_clusters": 0,
  "stage2_null_compatible_clusters": 0,
  "derivation_clusters": 0,
  "holdout_clusters": 0
}
```
with actual computed values.

- [ ] **Step 4: Run tests and builder**

```bash
pytest tests/test_floral_defence_selectivity_independence.py -v
python scripts/build_floral_defence_selectivity_dataset.py --input-dir empirical/floral_defence_selectivity --output-dir empirical/floral_defence_selectivity/results
```

Expected: both succeed and audit counts are generated from data, not hard-coded.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_floral_defence_selectivity_dataset.py tests/test_floral_defence_selectivity_independence.py empirical/floral_defence_selectivity/results
git commit -m "feat: build matched floral defence analysis dataset"
```

---

### Task 5: Add Milestone-1 scientific readout and provenance compatibility audit

**Files:**
- Create: `empirical/floral_defence_selectivity/MILESTONE1_READOUT.md`
- Create: `tests/test_floral_defence_selectivity_provenance.py`
- Modify: `empirical/floral_defence_selectivity/README.md`

**Interfaces:**
- Consumes: `results/corpus_audit.json`, old source files, new registries.
- Produces: no new scientific inference beyond corpus readiness.

- [ ] **Step 1: Write provenance tests**

Assert that new files reference, rather than replace, existing:
- `manuscript/supplementary/tables/TABLE_S3_MECHANISM_PATTERN_LEDGER.csv`;
- `empirical/mechanism_pattern_synthesis/OUTCOME_BLIND_DOMAIN_MODERATOR_MATRIX_V1.csv`;
- Catalpa, Pedicularis, and Thunia matched-effect audits;
- hold-out protocol;
- existing identification/manuscript evidence remains untouched by this branch.

- [ ] **Step 2: Run focused provenance tests**

Expected: PASS after references are present.

- [ ] **Step 3: Write the Milestone-1 readout**

Report:
- how many existing matched systems were migrated;
- Stage-1 and Stage-2 eligible independent cluster counts;
- which systems are strict quantitative anchors;
- which old BITA results remain preserved and how they map into the new analysis;
- missing cells that require focused search.

Do not claim the effective-domain hypothesis is supported until statistical/hold-out analysis is run.

- [ ] **Step 4: Run all new tests**

```bash
pytest tests/test_floral_defence_selectivity_*.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add empirical/floral_defence_selectivity tests/test_floral_defence_selectivity_provenance.py
git commit -m "docs: audit BITA selectivity milestone one"
```

---

### Task 6: Full regression check without rewriting the manuscript

**Files:**
- Modify only if a real compatibility bug is found; otherwise no source changes.

**Interfaces:** none.

- [ ] **Step 1: Run the new test set**

```bash
pytest tests/test_floral_defence_selectivity_*.py -v
```

- [ ] **Step 2: Run existing non-prose tests**

```bash
pytest -m "not prose_contract"
```

- [ ] **Step 3: Run existing prose-contract tests separately**

```bash
pytest -m prose_contract
```

Treat wording-only failures as advisory unless they expose a genuine old/new synchronization break. Do not “fix” old manuscript language in Milestone 1.

- [ ] **Step 4: Confirm branch diff scope**

Expected changed paths:
```text
docs/superpowers/specs/
docs/superpowers/plans/
empirical/floral_defence_selectivity/
trait_architecture/floral_defence_selectivity.py
scripts/build_floral_defence_selectivity_dataset.py
tests/test_floral_defence_selectivity_*.py
```

No deletion or rewrite of previous BITA science assets is permitted.

- [ ] **Step 5: Commit any test-only correction if needed**

Use a narrowly scoped message and document the reason in `MILESTONE1_READOUT.md`.
