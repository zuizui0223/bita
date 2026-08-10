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

### The completed synthesis: the antagonist-relief gate

The pathway with a pooled estimate is **floral antagonist pressure `H`**, the multiplicative gate on
the antagonist-relief channel `rho = H · d_A · e_F`. Every other declared route measures a trait
slope; none measures whether antagonists impose any realised cost at all. That gate decides whether
the project's central claim is even askable: **if `H = 0` then `rho = 0`, so `W_AD = −iota − kappa
≤ 0` and attraction and defence are unconditionally substitutable, with no conditionality to
explain.**

Oriented log response ratios of larcenist-exposed against unexposed flowers, one aggregated effect
per independent study cluster, DerSimonian–Laird random effects:

| route | clusters | pooled LRR | 95% CI | % change |
|---|---|---|---|---|
| `H_to_fitness` (female reproductive success) | **48** | −0.210 | −0.351, −0.070 | −19.0% |
| `H_to_reward` (nectar standing crop) | 28 | −0.483 | −0.757, −0.210 | −38.3% |
| `H_to_pollination` (legitimate visitation) | 22 | −0.291 | −0.523, −0.059 | −25.2% |
| `H_to_fitness` (male reproductive success) | 11 | −0.148 | −1.154, +0.857 | uninformative |

The gate is open, and the mechanism chain — reward depletion, then visitation loss, then fitness
loss — is intact link by link with monotonically attenuating magnitudes. All six pre-registered
context moderators return **no detected context dependence**, and the more telling number is that
they explain 0–8% of a heterogeneity running at *I*² = 97–99.5%: the effect varies enormously and
none of the declared ecological axes captures it.

This is **constituent-path evidence only**. It does not estimate `rho`, `iota`, `kappa`, or `W_AD`,
and it does not identify `M_AD`; that needs a design varying `A` and `D` jointly. Bridge assumption
B2 is an interpretive assumption in the analysis layer, not part of the fixed theory. The result is
also a **secondary analysis of a deposited effect-size table** (Leal et al. 2025, *Ecology*,
doi:10.1002/ecy.70036), not an independent literature search, and it inherits that synthesis's
inclusion criteria. Funnel asymmetry is detected on the primary stratum and reported. See
`empirical/broad_reality_evidence/larceny_gate/LARCENY_GATE_READOUT_V1.md`, pre-registered in
`LARCENY_GATE_PROTOCOL_V1.md` and committed before any estimate was computed.

### The blocked pathway: `D -> legitimate pollinator use`

The originally declared pathway feeds the mutualist-interference magnitude `iota`, under a bridge
assumption stated in `docs/IOTA_PATHWAY_EMPIRICAL_TARGET.md`. **It still has zero effect rows, zero
independent clusters, and zero pooled estimates.** The declared search produced 15
include-candidates, roughly 14 independent clusters, which clears the declared thresholds — but
only 4 have a PMC record. The other 11, including every field-pollination candidate in *Ecology*,
*Ecology Letters*, *Oecologia*, and *Current Biology*, are unreachable from this environment. The
shortfall is access, not the size of the literature. Its search and screening are also themselves
incomplete: several logged sub-queries are unscreened and six records were never retrieved. See
`empirical/broad_reality_evidence/iota_pathway/IOTA_PATHWAY_FEASIBILITY_V1.md`.

`docs/LOCAL_EXECUTION_RUNBOOK.md` gives the path from clone to pooled estimate on a machine with
ordinary network access, and `scripts/fetch_declared_search.py` executes the declared query against
Europe PMC **undecomposed**, since that API imposes no boolean-operator cap.

The search log, screening decisions, exclusion classification, design power analysis, and
value-of-information ranking are preparatory or diagnostic for that pathway, and must not be
reported as partial progress toward its pooled estimate.

Two properties of that design are established without data and bound what the extraction can
deliver:

- **Design power.** Simulating the declared design through the deployed code sets a declared
  detectable effect: at 5 clusters per moderator level it reaches 80% power against a halving of
  pollinator use, and does not reach it against a 30% shift. The fixed-effect `Q_between`
  statistic is reported descriptively only — its false-positive rate reaches 0.60 under realistic
  heterogeneity — and inference comes from the random-effects meta-regression contrast. See
  `empirical/design_power/DECLARED_DESIGN_POWER_READOUT_V1.md`.
- **Empirical leverage.** 97 of the 216 declared regime points are insensitive to `c_D`
  altogether, and settling 80% of the remainder would need a `c_D` interval half-width of 0.20.
  The pathway meta-analysis can therefore anchor one channel's direction and context dependence;
  it cannot resolve the regime map. See
  `empirical/empirical_leverage/EMPIRICAL_LEVERAGE_READOUT_V1.md`.
- **Channel value of information.** Ranking every parameter of the three-channel balance by how
  much of the declared grid its measurement would settle puts `c_D` **fourth of five**. The
  leading parameter is `attraction_tracking` — how strongly floral antagonists track the focal
  attraction trait — in the antagonist-relief channel, and it leads in all four response-shape
  variants. The declared target stands, because it is the only channel with a manipulative
  literature that measures the channel directly, but the tractable channel is not the decisive
  one and the repository says so. See
  `empirical/channel_leverage/CHANNEL_LEVERAGE_READOUT_V1.md`.

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

python scripts/run_declared_design_power.py artifacts/supplement/design_power 2000

python scripts/run_empirical_leverage.py \
  configs/part_i_robustness_grid.json 0.45 0.25 artifacts/supplement/leverage

python scripts/run_channel_leverage.py \
  configs/part_i_robustness_grid.json artifacts/supplement/channel_leverage 0.25
```

The canonical committed Part I metadata are in:

```text
empirical/part_i_robustness/endpoint_normalized_grid_v2_report.json
empirical/part_i_robustness/PART_I_SENSITIVITY_READOUT_V2.md
```

## Data policy

Only derived, aggregate, or bibliographic material required for the active theory claim or its preliminary context belongs in the submission tree. Exploratory discovery machinery, raw third-party observations, former case-study pipelines, optimum/covariance analyses, network/trait-coverage audits, and superseded manuscript-planning material remain outside the active supplement. Git history is the archive for those earlier branches.
