# Biotic Interaction Trait Architecture

Reproducible supplementary code and evidence for a mechanistically oriented local theory of one focal floral attraction trait (`A`) and one focal flower-specific barrier/defence trait (`D`) on one declared outcome scale (`W`).

## Submission claim

The repository supports two linked but unequal claims.

1. **Theory:** for a declared `A`–`D` pair and declared `W` scale, the local mixed partial can be organized into antagonist relief, mutualist interference, and direct joint-cost curvature **after the channel decomposition and required mixed-curvature signs have been established for that focal model**. Environmental directional predictions depend on the local derivatives of all three channel contributions with respect to the ecological regime.
2. **Literature context:** the current registry contains abstract-coded directional records. One declared three-cluster manipulation stratum for chemical barriers and pollinator preference/foraging is uniformly negative. This is restricted abstract-level directional consistency with a collateral pollinator-cost pathway; it does not identify the focal mutualist mixed curvature, estimate the complete mixed partial, or validate the regime comparative statics.

The core quantity is

```text
W_AD = d2W / dA dD
```

for a declared, twice-differentiable outcome surface. A positive value means that one focal trait raises the other's local marginal return **on that declared `W` scale**; a negative value means that it lowers that return. The result does not by itself predict trait covariance, genetic correlation, an evolved environmental cline, or an evolutionary endpoint.

## Focal-trait and outcome-scale rule

`A`, `D`, and `W` must be declared explicitly.

```text
A = one biologically defined floral attraction trait and its scale
D = one biologically defined flower-specific barrier/defence trait and its scale
W = one declared fitness, relative-fitness, or score scale
```

`A` and `D` are not omnibus trait categories. `D` is defined by a flower-specific antagonist-reduction role; a pollinator-use cost is a possible collateral effect of that same trait.

The mixed-partial sign is not transformation free. Positive affine rescaling of the focal traits and `W` preserves the sign of a nonzero mixed partial, but arbitrary nonlinear trait or outcome transformations can change it. Fitness, relative fitness, log fitness, and an additive qualitative score must not be treated as interchangeable curvature scales.

## Core theoretical structure

For mechanistic bookkeeping,

```text
W_AD = M_AD - G_AD - C_AD
```

but the channel decomposition is **not identified by total W alone**. Different allocations of the same smooth cross term among `M`, `G`, and `C` can leave the total surface unchanged. Channel-specific curvatures therefore require operational definitions, channel-specific measurements, manipulations, or additional structural assumptions.

The non-negative magnitude form

```text
local A x D marginal interaction
= antagonist relief
- mutualist interference
- direct joint-cost curvature
```

is used only after an explicit model or local derivative argument establishes the orientation conditions

```text
M_AD <= 0
G_AD <= 0
C_AD >= 0.
```

The trait names alone do not guarantee those mixed-curvature signs. A negative `D -> pollinator use` effect does not by itself identify `M_AD < 0`; it must show that `D` reduces the marginal mutualist return to the particular focal `A`.

## Environmental comparative statics

After the oriented channel contributions have been defined, allow all three to depend on both regime variables:

```text
W_AD(P,H) = R(P,H) - I(P,H) - C_AD(P,H)
```

The general local derivatives are

```text
dW_AD/dH = dR/dH - dI/dH - dC_AD/dH
dW_AD/dP = dR/dP - dI/dP - dC_AD/dP
```

Thus stronger antagonist pressure shifts the interaction toward complementarity only when `dW_AD/dH > 0`, and stronger pollinator service shifts it toward substitutability only when `dW_AD/dP < 0`.

This general balance retains cross-environment effects: `H` may alter mutualist interference, and `P` may alter antagonist relief.

A separable nonlinear special case assumes

```text
R(P,H) = a(H) * relief_rate
I(P,H) = b(P) * interference_rate
```

and the linear special case further uses `a(H)=H`, `b(P)=P`, and regime-invariant direct cross-cost curvature:

```text
W_AD = H * relief_rate - P * interference_rate - joint_cost_curvature
```

The separable and linear expressions are special cases, not the general environmental derivative law.

See `docs/GENERAL_SIGN_CRITERION.md` for assumptions and derivation and `docs/NOVELTY_POSITIONING.md` for the claim boundary and prior-art positioning.

## Sensitivity analysis

The active numerical sweep compares four biological parameter scenarios and four nonlinear response-shape variants over a declared 0–1 focal-trait grid.

The nonlinear response shapes are **endpoint normalized**:

```text
attraction response at A=1                    matched across variants
defence response at D=1                       matched across variants
direct joint-cost scale at A=D=1              matched across variants
```

This reduces confounding between changing response shape and simply changing endpoint effect magnitude. The variants still differ in local derivatives and represent only a finite tested family.

`tested_set_unanimous` means unanimity across that finite set, not mathematical structural robustness. Exact complementary/substitutable modal ties are reported as `mixed`, not assigned to one sign. The configured `neutral_tolerance` is recorded as an absolute numerical zero threshold on the declared score scale; it is not a biologically invariant neutrality band.

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

The theory grid is a finite, declared sensitivity analysis, not an empirical frequency distribution and not proof of mathematical structural robustness. Its signs and numerical zero classifications are properties of the declared trait coordinates, score scale, and tolerance convention. The literature layer is abstract-level route coding, not a full-text systematic review or pooled universal meta-analysis. It does not establish the focal `M_AD` curvature, uniquely identify the three mechanism terms, estimate the complete local `A`–`D` interaction, or validate its environmental derivatives in nature.
