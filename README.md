# Biotic Interaction Trait Architecture

Reproducible supplementary code and evidence for a conditional theory of floral attraction (A) and flower-specific defence/access limitation (D).

## Submission claim

The repository supports two linked claims:

1. **Theory:** attraction and defence are not assumed to be intrinsically traded off. Their local fitness interaction is determined by a sign criterion balancing antagonist relief against mutualist interference and direct joint cost.
2. **Literature support:** verified route-level evidence shows that defence/access traits can reduce pollinator use in at least some systems. This establishes the biological existence of one sign-changing pathway in the criterion; it does not identify the complete mixed partial in nature.

The theorem-level result is a statement about the local mixed partial `d2W / dA dD`. A positive value means local fitness complementarity and a negative value local fitness substitutability. Neither sign, by itself, predicts population-level trait covariance, genetic correlation, or an evolutionary endpoint.

The repository does **not** claim that the complete attraction -> antagonism, defence -> antagonism, shared-cost, or full A x D mixed-partial terms have been jointly estimated empirically.

## Core theoretical result

For a broad local decomposition

```text
W(A,D) = mutualist contribution - antagonist loss - direct joint cost,
```

the A x D mixed partial can be written as

```text
antagonist relief - mutualist interference - joint cost.
```

The sign switches when antagonist relief crosses the sum of the two opposing terms. The implemented exponential/linear score is one explicit corollary; the robustness grid tests selected nonlinear alternatives rather than serving as the proof itself.

See `docs/GENERAL_SIGN_CRITERION.md` for the theorem-level statement and inference boundary.

## Supplement structure

```text
configs/                         predeclared robustness configuration
theory/                          mathematical definitions and interpretation
trait_architecture/              theorem, robustness, and evidence-validation code
scripts/                         command-line reproduction entry points
empirical/broad_reality_evidence verified route-level literature records
empirical/part_i_robustness/     locked protocols and manuscript-facing outputs
docs/                            theorem, scope, methods, claim boundaries, and readouts
tests/                           regression and integrity tests
.github/workflows/               automated reproduction and validation
```

See `SUPPLEMENT_MANIFEST.md` for the claim-to-file map.

## Reproduce the core supplement

Python 3.11 is the reference environment.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'

python -m pytest

python scripts/run_part_i_robustness.py \
  configs/part_i_robustness_grid.json \
  artifacts/supplement/part_i

python scripts/build_part_i_manuscript_readout.py \
  artifacts/supplement/part_i/part_i_robustness_cases.csv \
  artifacts/supplement/part_i/part_i_functional_form_summary.csv \
  artifacts/supplement/part_i/part_i_robustness_envelope.csv \
  artifacts/supplement/part_i/PART_I_MANUSCRIPT_READOUT.md

python scripts/build_part_i_regime_figure_svg.py \
  artifacts/supplement/part_i/part_i_robustness_cases.csv \
  artifacts/supplement/part_i/FIGURE_2_THEORY_REGIME_MAP.svg

python scripts/run_broad_meta_analysis.py \
  empirical/broad_reality_evidence/broad_route_records.csv \
  empirical/broad_reality_evidence/broad_effect_extractions.csv \
  empirical/broad_reality_evidence/broad_meta_analysis_strata.csv \
  artifacts/supplement/literature

python scripts/validate_part_b_integrity.py
```

The GitHub Actions workflows run the same theory, evidence, and boundary checks automatically.

## Data policy

Only derived, aggregate, or bibliographic evidence required for the stated claims is committed. Exploratory search queues, abandoned linked-system analyses, transient repository probes, and raw third-party observations are excluded from the active tree. Git history remains the archive of earlier exploration.

## Interpretation boundary

The theory grid is a conditional sensitivity analysis, not an empirical frequency distribution. The literature layer is route-level support, not a pooled universal meta-analysis. Evidence for a defence -> pollination cost narrows the plausible mechanism space but does not by itself establish local complementarity, local substitutability, or an observed attraction--defence correlation in nature.
