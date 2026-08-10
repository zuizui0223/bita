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

Within a neighbourhood where the orientation gate remains valid, let

```text
rho(P,H)  = antagonist-relief contribution
iota(P,H) = mutualist-interference contribution
```

Then

```text
W_AD(P,H) = rho(P,H) - iota(P,H) - C_AD(P,H)
```

and

```text
dW_AD/dH = d rho/dH - d iota/dH - dC_AD/dH
dW_AD/dP = d rho/dP - d iota/dP - dC_AD/dP
```

The separable and linear expressions used in the implemented corollary are special cases, not universal environmental laws.

See `docs/GENERAL_SIGN_CRITERION.md` and `docs/NOVELTY_POSITIONING.md` for assumptions, derivations, prior-art positioning, and inference boundaries.

## Sensitivity analysis

The active numerical sweep evaluates the implemented corollary across:

- declared local `A` and `D` coordinates;
- exogenous pollinator-service (`P`) and floral-antagonist-pressure (`H`) regimes;
- biological parameter scenarios;
- endpoint-normalized nonlinear response-shape variants.

Reproductive assurance `R` is retained only as an **auxiliary background moderator** of the pollination-mediated channel in the implemented corollary. It is not a third focal trait and is not part of the primary submission claim.

The response-shape variants are normalized on the declared 0–1 focal-trait domain so that endpoint effect scales match while local derivatives may differ. `tested_set_unanimous` means unanimity only across the finite tested set; it is not proof of mathematical structural robustness. All other cases are `mixed_or_sensitive`, while `modal_sign_agreement` remains a continuous descriptive quantity. No arbitrary majority threshold is converted into a separate robustness class.

The canonical committed run is `endpoint_normalized_grid_v2`. Its reported percentages are unweighted occupancy fractions over the declared finite grid, not empirical probabilities or estimates of prevalence in nature.

## Preliminary literature context

The repository also retains an abstract-level route registry as **preliminary mechanism context**. It is not a second independent submission claim.

The current records are machine-assisted, single-coder abstract-level classifications. They have not yet undergone the full-text verification and independent duplicate coding or documented adjudication required for promotion to a manuscript-level evidence synthesis.

The literature layer therefore does not:

- identify the focal `M_AD` curvature;
- estimate antagonist relief or direct joint-cost curvature;
- calibrate model parameters;
- estimate the complete local `A`–`D` mixed partial;
- validate environmental derivatives or the regime map in nature.

## Declared empirical target

The preliminary literature layer above is context, not the project's empirical target. The target
is a quantitative meta-analysis, over multiple independent studies, of **one constituent pathway**
of the three-channel balance, reporting its realised direction and whether that direction is
context dependent.

The declared pathway is `D -> legitimate pollinator use`, which feeds the mutualist-interference
magnitude `iota`. Within the implemented corollary the pollinator-access term is multiplicatively
separable in `D`, so an oriented log response ratio of this route identifies `sign(c_D)` and
therefore `sign(iota)` — under a declared bridge assumption stated in
`docs/IOTA_PATHWAY_EMPIRICAL_TARGET.md`. The stratum, the four context moderators, the capacity
thresholds, and the extraction rules are pre-registered before any number is extracted.

The extraction table is currently empty, so every declared moderator analysis returns
`insufficient_moderator_capacity`. Nothing about direction or context dependence in this pathway
has been estimated yet. See
`empirical/broad_reality_evidence/iota_pathway/IOTA_PATHWAY_STATUS_READOUT_V1.md`.

## Supplement structure

```text
configs/                         declared sensitivity configuration
theory/                          mathematical definitions and interpretation
trait_architecture/              active theory, sensitivity, and validation code
scripts/                         command-line reproduction entry points
empirical/part_i_robustness/     canonical theory outputs
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
  artifacts/supplement/part_i/part_i_sensitivity_evaluations.csv \
  artifacts/supplement/part_i/part_i_response_shape_summary.csv \
  artifacts/supplement/part_i/part_i_full_tested_set_summary.csv \
  artifacts/supplement/part_i/PART_I_SENSITIVITY_READOUT_V2.md

python scripts/build_part_i_regime_figure_svg.py \
  artifacts/supplement/part_i/part_i_sensitivity_evaluations.csv \
  artifacts/supplement/part_i/FIGURE_2_THEORY_REGIME_MAP.svg

python scripts/run_broad_meta_analysis.py \
  empirical/broad_reality_evidence/broad_route_records.csv \
  empirical/broad_reality_evidence/broad_effect_extractions.csv \
  empirical/broad_reality_evidence/broad_meta_analysis_strata.csv \
  artifacts/supplement/literature

python scripts/run_context_dependence.py \
  empirical/broad_reality_evidence/broad_effect_extractions.csv \
  empirical/broad_reality_evidence/iota_pathway/iota_moderator_coding.csv \
  empirical/broad_reality_evidence/broad_meta_analysis_strata.csv \
  empirical/broad_reality_evidence/iota_pathway/iota_moderator_registry.csv \
  artifacts/supplement/iota_pathway
```

The canonical committed Part I metadata are in:

```text
empirical/part_i_robustness/endpoint_normalized_grid_v2_report.json
empirical/part_i_robustness/PART_I_SENSITIVITY_READOUT_V2.md
```

## Data policy

Only derived, aggregate, or bibliographic material required for the active theory claim or its preliminary context belongs in the submission tree. Exploratory discovery machinery, raw third-party observations, former case-study pipelines, optimum/covariance analyses, network/trait-coverage audits, and superseded manuscript-planning material remain outside the active supplement. Git history is the archive for those earlier branches.
