# Retired probe scripts v1

## Purpose

This is the second cleanup pass after retiring exploratory workflows. It removes
script entry points whose active workflow triggers were already removed and whose
repository search results showed no current manuscript-path references beyond the
retired route.

This pass intentionally remains conservative. It does not remove historical modules,
readouts, evidence tables, or scripts still referenced by documentation.

## Removed scripts

```text
scripts/probe_web_of_life.py
scripts/probe_bien_floral_traits.R
scripts/probe_bien_wol_leaf_coverage.R
scripts/probe_globi_antagonist_contract.py
scripts/probe_bien_wol_attraction_coverage.R
scripts/inspect_dryad_version_payload.py
scripts/inspect_dryad_dataset_payload.py
scripts/inspect_title_validated_dryad_csv_headers.py
scripts/inspect_title_validated_dryad_archive_headers.py
```

## Rationale

These scripts were one-off source-contract, public-data feasibility, or early Dryad
inspection entry points. The current manuscript path no longer uses them:

```text
active empirical route: .github/workflows/run-impatiens-empirical-core.yml
active evidence guard:  .github/workflows/part-b-integrity.yml
active writing layer:   docs/MANUSCRIPT_*.md and docs/IMPATIENS_RESULTS_LOCK_V1.md
```

## Preserved scripts/modules

The following categories were not deleted in this pass:

```text
1. scripts still referenced by documentation, such as TRY request materials;
2. Impatiens empirical-core scripts;
3. Part A theory and robustness scripts;
4. Part B integrity and current evidence-map scripts;
5. historical source-screen modules whose readout documents still explain stopping decisions.
```

## Next safe cleanup

The next cleanup should be narrower and should either:

```text
A. update or archive the old TRY/functional-trait documentation before removing
   the remaining TRY/Web-of-Life request script; or
B. run a module-level import/reference audit for Dalechampia and Gymnadenia helper
   modules before deleting historical code.
```
