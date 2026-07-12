# Biotic Interaction Trait Architecture

Reproducible supplementary code and evidence for a conditional theory of floral attraction (A) and defence/access limitation (B).

## Submission claim

The repository supports two linked claims:

1. **Theory:** attraction and defence can be complementary or substitutable depending on the balance among antagonist suppression, pollination obstruction, and shared cost.
2. **Literature support:** verified route-level evidence shows that B can reduce pollinator use in at least some chemical-defence systems. This supports the existence of a B -> P cost; it does not estimate a universal causal parameter.

The repository does **not** claim that B -> H benefit, A -> H tracking, shared cost, or the full A x B mixed partial has been empirically estimated.

## Supplement structure

```text
configs/                         predeclared robustness configuration
theory/                          mathematical definitions and interpretation
trait_architecture/              reusable theory and evidence-validation code
scripts/                         command-line reproduction entry points
empirical/broad_reality_evidence verified route-level literature records
empirical/part_i_robustness/     locked protocols and manuscript-facing outputs
docs/                            scope, methods, claim boundaries, and readouts
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

The theory grid is a conditional model exploration, not an empirical frequency distribution. The literature layer is route-level support, not a pooled universal meta-analysis. Directional evidence for a B -> P cost narrows the plausible mechanism space but does not by itself establish complementarity or substitutability in nature.
