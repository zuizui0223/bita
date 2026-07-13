# Biotic Interaction Trait Architecture

Reproducible supplementary code and supporting context for a local theory of one focal floral attraction trait (`A`) and one focal flower-specific barrier/defence trait (`D`) on one declared outcome scale (`W`).

## Primary submission claim

The repository has **one primary theory claim**.

For a declared `A`–`D` pair and declared `W` scale, the local mixed partial

```text
W_AD = d2W / dA dD
```

measures how one focal trait changes the other's local marginal effect on that declared outcome scale.

The signed bookkeeping identity

```text
W_AD = M_AD - G_AD - C_AD
```

is not itself a novelty claim and does not uniquely identify biological mechanisms from total `W` alone. Channel-specific curvatures require operational definitions, channel-specific measurements or manipulations, or additional structural assumptions.

After the relevant orientation conditions have been established for a focal model, the local balance can be described as

```text
local A x D marginal interaction
= antagonist relief
- mutualist interference
- direct joint-cost curvature
```

The result is local. It does not by itself imply trait covariance, genetic correlation, an evolutionary trajectory, a stable optimum, or an evolved environmental cline.

## Environmental comparative statics

Allow the oriented channel contributions to depend on both exogenous regime variables `P` and `H`:

```text
W_AD(P,H) = R(P,H) - I(P,H) - C_AD(P,H)
```

Then

```text
dW_AD/dH = dR/dH - dI/dH - dC_AD/dH
dW_AD/dP = dR/dP - dI/dP - dC_AD/dP
```

The separable and linear expressions used in the implemented corollary are special cases, not universal environmental laws.

See `docs/GENERAL_SIGN_CRITERION.md` and `docs/NOVELTY_POSITIONING.md` for assumptions, derivations, prior-art positioning, and inference boundaries.

## Sensitivity analysis

The active numerical sweep evaluates the implemented corollary across:

- declared local `A` and `D` coordinates;
- exogenous pollinator-service and floral-antagonist-pressure regimes;
- biological parameter scenarios;
- endpoint-normalized nonlinear response-shape variants.

Reproductive assurance `R` is retained only as an **auxiliary background moderator** of the pollination-mediated channel in the implemented corollary. It is not a third focal trait and is not part of the primary submission claim.

The response-shape variants are normalized on the declared 0–1 focal-trait domain so that endpoint effect scales match while local derivatives may differ. `tested_set_unanimous` means unanimity only across the finite tested set; it is not proof of mathematical structural robustness. The configured neutral tolerance is an absolute numerical zero threshold on the declared score scale, not a biologically invariant neutrality band.

## Preliminary literature context

The repository also retains an abstract-level route registry as **preliminary mechanism context**. It is not a second independent submission claim.

The current records are machine-assisted, single-coder abstract-level classifications. They have not yet undergone the full-text verification and independent duplicate coding or documented adjudication required for promotion to a manuscript-level evidence synthesis.

The literature layer therefore does not:

- identify the focal `M_AD` curvature;
- estimate antagonist relief or direct joint-cost curvature;
- calibrate model parameters;
- estimate the complete local `A`–`D` mixed partial;
- validate environmental derivatives or the regime map in nature.

## Supplement structure

```text
configs/                         declared sensitivity configuration
theory/                          mathematical definitions and interpretation
trait_architecture/              active theory, sensitivity, and validation code
scripts/                         command-line reproduction entry points
empirical/part_i_robustness/     manuscript-facing theory outputs
empirical/broad_reality_evidence preliminary route-level literature context
docs/                            scope, assumptions, methods, and claim boundaries
tests/                           regression and integrity tests
.github/workflows/               automated reproduction and validation
```

See `SUPPLEMENT_MANIFEST.md` for the claim-to-file map and `docs/SUBMISSION_SCOPE.md` for the retention boundary.

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
```

## Data policy

Only derived, aggregate, or bibliographic material required for the active theory claim or its preliminary context belongs in the submission tree. Exploratory discovery machinery, raw third-party observations, former case-study pipelines, optimum/covariance analyses, network/trait-coverage audits, and superseded manuscript-planning material remain outside the active supplement. Git history is the archive for those earlier branches.
