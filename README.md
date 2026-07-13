# Biotic Interaction Trait Architecture

Reproducible supplementary code and evidence for a local theory of one focal floral attraction trait (`A`) and one focal flower-specific barrier/defence trait (`D`).

## Submission claim

The repository supports two linked but unequal claims.

1. **Theory:** for a declared `A`–`D` pair, the local mixed partial can be organized into antagonist relief, mutualist interference, and direct joint cost **after the required mixed-curvature signs have been established for that focal model**. Environmental directional predictions require explicit assumptions about how ecological regime variables scale those channels.
2. **Literature context:** the current registry contains abstract-coded directional records. One predeclared three-cluster manipulation stratum for chemical barriers and pollinator preference/foraging is uniformly negative. This is restricted abstract-level directional consistency with a collateral pollinator-cost pathway; it does not identify the focal mutualist mixed curvature, estimate the complete mixed partial, or validate the regime comparative statics.

The core quantity is

```text
W_AD = d2W / dA dD
```

for a declared, twice-differentiable fitness or fitness-score surface. A positive value means that one focal trait raises the other's local marginal fitness return; a negative value means that it lowers that return. The result does not by itself predict trait covariance, genetic correlation, an evolved environmental cline, or an evolutionary endpoint.

## Focal-trait rule

`A` and `D` are not omnibus trait categories.

```text
A = one biologically defined floral attraction trait
D = one biologically defined flower-specific barrier/defence trait
```

A concrete application must declare the focal traits and their scales. `D` is defined by a flower-specific antagonist-reduction role; a pollinator-use cost is a possible collateral effect of that same trait.

## Core theoretical structure

For bookkeeping,

```text
W_AD = M_AD - G_AD - C_AD
```

is always the unrestricted signed decomposition. The non-negative magnitude form

```text
local A x D marginal-fitness interaction
= antagonist relief
- mutualist interference
- direct joint cost
```

is used only after an explicit model or local derivative argument establishes the orientation conditions

```text
M_AD <= 0
G_AD <= 0
C_AD >= 0.
```

The trait names alone do not guarantee those mixed-curvature signs. For example, a negative `D -> pollinator use` effect does not by itself identify `M_AD < 0`; it must show that `D` reduces the marginal mutualist return to the particular focal `A`.

Under the oriented mechanism class, local complementarity requires antagonist relief to exceed mutualist interference plus direct joint cost.

Environmental predictions need an additional regime-scaling layer. In the general local form

```text
W_AD = a(H) * relief_rate
     - b(P) * interference_rate
     - joint_cost(P, H)
```

stronger antagonist pressure shifts the interaction toward complementarity only when the local increase in relief scaling exceeds any countervailing change in direct cross-cost. The mutualist-service prediction is likewise conditional on its derivative inequality.

The linear expression

```text
W_AD = H * relief_rate - P * interference_rate - joint_cost
```

is one special case, not a universal law.

See `docs/GENERAL_SIGN_CRITERION.md` for assumptions and derivation and `docs/NOVELTY_POSITIONING.md` for the claim boundary and prior-art positioning.

## Supplement structure

```text
configs/                         declared sensitivity configuration
theory/                          mathematical definitions and interpretation
trait_architecture/              active criterion, sensitivity, and validation code
scripts/                         command-line reproduction entry points
empirical/broad_reality_evidence abstract-level route records and evidence readout
empirical/part_i_robustness/     manuscript-facing theory outputs
docs/                            scope, methods, assumptions, and claim boundaries
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
```

The GitHub Actions workflows reproduce the theory outputs and validate the theory–literature inference boundary.

## Data policy

Only derived, aggregate, or bibliographic evidence required for the stated claims is committed. Exploratory search queues, abandoned matched-study and network-audit machinery, obsolete optimum/covariance analyses, repository probes, and raw third-party observations are outside the active supplement. Git history remains the archive of earlier exploration.

## Interpretation boundary

The theory grid is a finite, predeclared sensitivity analysis, not an empirical frequency distribution and not proof of mathematical structural robustness. The literature layer is abstract-level route coding, not a full-text systematic review or pooled universal meta-analysis. It does not establish the focal `M_AD` curvature, the complete local `A`–`D` interaction, an observed attraction–defence correlation, or the response of that interaction to changing ecological regimes in nature.
