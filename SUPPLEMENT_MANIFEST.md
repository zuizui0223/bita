# Supplement manifest

This map links the one primary submission claim and its preliminary supporting context to the files needed to inspect or reproduce them.

## Primary claim: local attraction–defence interaction theory

Primary theory, assumptions, and positioning:

- `docs/GENERAL_SIGN_CRITERION.md`
- `docs/NOVELTY_POSITIONING.md`
- `docs/BACKGROUND_NOVELTY_GAP_REVIEW.md`
- `theory/README.md`
- `trait_architecture/sign_criterion.py`
- `tests/test_sign_criterion.py`

Implemented corollary and finite-set sensitivity analysis:

- `trait_architecture/model.py`
- `trait_architecture/robustness.py`
- `configs/part_i_robustness_grid.json`
- `scripts/run_part_i_robustness.py`
- `docs/PART_I_ROBUSTNESS_PROTOCOL.md`
- `tests/test_robustness.py`
- `tests/test_run_part_i_robustness.py`
- `tests/test_committed_part_i_results_current.py`

Canonical V2 outputs and manuscript-facing builders:

- `empirical/part_i_robustness/endpoint_normalized_grid_v2_report.json`
- `empirical/part_i_robustness/PART_I_SENSITIVITY_READOUT_V2.md`
- `scripts/build_part_i_manuscript_readout.py`
- `scripts/build_part_i_regime_figure_svg.py`
- `tests/test_build_part_i_manuscript_readout.py`
- `tests/test_build_part_i_regime_figure_svg.py`

Interpretive boundary:

- `P` and `H` are exogenous reference-regime indices.
- Environmental directional predictions depend on derivatives of all channel contributions, not on `P` or `H` alone.
- The non-negative relief/interference decomposition requires an explicit local orientation gate.
- Reproductive assurance `R` is an auxiliary background moderator in the implemented corollary, not a third focal trait.
- Reported percentages are unweighted occupancies of the declared finite grid, not empirical probabilities or prevalence estimates.
- `tested_set_unanimous` and `mixed_or_sensitive` are the only categorical finite-set agreement labels; `modal_sign_agreement` is continuous and no arbitrary majority threshold defines a third class.

## Preliminary literature context: collateral pollinator-cost route

Active route-level context:

- `empirical/broad_reality_evidence/broad_route_records.csv`
- `empirical/broad_reality_evidence/broad_effect_extractions.csv`
- `empirical/broad_reality_evidence/broad_meta_analysis_strata.csv`
- `empirical/broad_reality_evidence/LITERATURE_EVIDENCE_READOUT.md`

Reproduction and validation:

- `scripts/run_broad_meta_analysis.py`
- `scripts/validate_current_theory_meta.py`
- `trait_architecture/broad_meta_analysis.py`
- `trait_architecture/theory_meta_validation.py`
- `tests/test_theory_meta_validation.py`
- `.github/workflows/validate-current-theory-meta.yml`

All currently active directional records are coded from `crossref_deposited_abstract`. The relevant declared `B_to_pollination × chemical_barrier × pollinator_preference_or_foraging × manipulation` stratum contains three independent primary clusters, all coded negative. A separate `visitation_rate` stratum contains one mixed record and is not pooled into that three-cluster directional fraction.

The current quantitative extraction table contains no eligible effect rows, and the abstract-level registry has not undergone full-text verification and independent duplicate coding or documented adjudication. The literature layer is therefore **preliminary mechanism context only**. It is not a second independent submission claim, does not calibrate model parameters, and does not validate the regime map.

## Declared empirical target: the mutualist-interference constituent pathway

The literature layer above is preliminary context. It is not the project's empirical target. The
target is a quantitative meta-analysis, over multiple independent studies, of **one constituent
pathway** of the three-channel balance, reporting both its realised direction and whether that
direction is context dependent.

Declared target, theory bridge, and inference boundary:

- `docs/IOTA_PATHWAY_EMPIRICAL_TARGET.md`
- `empirical/broad_reality_evidence/iota_pathway/IOTA_PATHWAY_EXTRACTION_PROTOCOL_v1.md`

Declared machine-readable inputs:

- `empirical/broad_reality_evidence/iota_pathway/iota_moderator_registry.csv`
- `empirical/broad_reality_evidence/iota_pathway/iota_moderator_coding.csv`
- `empirical/broad_reality_evidence/iota_pathway/iota_reading_queue.csv`
- the `BP_chemical_pollinator_use_lrr_manipulation` row of `broad_meta_analysis_strata.csv`

Analysis and reproduction:

- `trait_architecture/context_dependence.py`
- `scripts/run_context_dependence.py`
- `tests/test_context_dependence.py`
- `empirical/broad_reality_evidence/iota_pathway/IOTA_PATHWAY_STATUS_READOUT_V1.md`

The pathway is `D -> legitimate pollinator use`, which feeds the mutualist-interference magnitude
`iota`. Under bridge assumption B1 (the effect of `D` on pollinator access is multiplicatively
separable from `A`), the oriented log response ratio of this route identifies `sign(c_D)` and
therefore `sign(iota)` in the implemented corollary. B1 is declared, not demonstrated; without it
the pooled arrow stays a marginal-route statement.

The effect table currently holds no eligible rows, so all four declared moderator analyses return
`insufficient_moderator_capacity` and the verdict `not_evaluated`. No pooled effect and no
context-dependence verdict exists for this pathway yet.

### Design adequacy and empirical leverage of that target

Both questions are answerable without data and both constrain what the extraction should aim for.

- `trait_architecture/design_power.py`, `scripts/run_declared_design_power.py`,
  `tests/test_design_power.py`, `empirical/design_power/DECLARED_DESIGN_POWER_READOUT_V1.md`
- `trait_architecture/empirical_leverage.py`, `scripts/run_empirical_leverage.py`,
  `tests/test_empirical_leverage.py`,
  `empirical/empirical_leverage/EMPIRICAL_LEVERAGE_READOUT_V1.md`

Simulating the declared design through the deployed code showed that the fixed-effect `Q_between`
statistic rejects a true null up to 60% of the time under realistic heterogeneity, so it is now
reported descriptively and issues no verdict; inference comes from the random-effects
meta-regression contrast, whose null rate stays at or below 0.062. The direction-reversal verdict
now additionally requires both level intervals to exclude zero with opposite signs, which cut its
null rate from 21–35% to at most 0.014. The primary moderator thresholds were raised from 3 to 5
clusters per level, and the protocol carries a declared detectable effect.

The leverage analysis shows that 97 of 216 declared regime points are insensitive to `c_D`
altogether, and that settling 80% of the remainder needs a `c_D` interval half-width of 0.20 —
out of reach at plausible cluster counts. The empirical half of the project is therefore scoped
to one channel's direction and context dependence, not to an empirically resolved
complementarity map.

### Which channel is worth measuring

- `trait_architecture/channel_leverage.py`, `scripts/run_channel_leverage.py`,
  `tests/test_channel_leverage.py`, `tests/test_committed_channel_leverage_current.py`,
  `empirical/channel_leverage/CHANNEL_LEVERAGE_READOUT_V1.md`

Ranking every parameter of the three-channel balance by how much of the declared grid its
measurement would settle places `c_D` fourth of five. `attraction_tracking` leads, in all four
endpoint-normalized response-shape variants. The declared target is retained on feasibility
grounds — it is the only channel with a manipulative literature that measures the channel
directly — but the repository states plainly that the tractable channel is not the decisive one,
and records `d_A` in the `A_to_antagonism` route as the highest-leverage next target.

## Boundary between theory and literature context

- `README.md`
- `docs/SUBMISSION_SCOPE.md`
- `docs/FINAL_SUBMISSION_AUDIT.md`
- `docs/BACKGROUND_NOVELTY_GAP_REVIEW.md`
- `scripts/validate_current_theory_meta.py`
- `trait_architecture/theory_meta_validation.py`
- `tests/test_submission_scope.py`
- `tests/test_submission_narrative_contract.py`

A negative `D -> pollinator use` route does not by itself identify the focal mutualist mixed curvature `M_AD < 0`; that would require showing how `D` changes the marginal mutualist return to the same focal `A`. Route records from different traits and taxa also do not jointly estimate one system-specific `D` axis, the complete local `A`–`D` mixed partial, its environmental derivative, trait covariance, or an evolutionary endpoint.

## Deliberately absent

Raw third-party observations, the former *Impatiens capensis* case-study pipeline, optimum/covariance analyses, matched-study discovery architecture, network/trait-coverage audits, regime-discrimination audits based on abstract-level direction records, exploratory candidate scouting, repository-access probes, broad candidate-harvesting machinery, and superseded manuscript-planning files are not part of this supplement. Git history is the archive for those earlier branches.