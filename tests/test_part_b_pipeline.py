import json

from trait_architecture.broad_meta_analysis import EFFECT_FIELDS, ORIENTATION, read_csv_rows, read_strata
from trait_architecture.part_b_pipeline import (
    run_break_even_map,
    run_moderator_hypotheses,
    write_part_b_outputs,
)

REPO_ROUTE_RECORDS = "empirical/broad_reality_evidence/broad_route_records.csv"
REPO_EFFECTS = "empirical/broad_reality_evidence/part_b_arrow_effects.csv"
REPO_STRATA = "empirical/broad_reality_evidence/part_b_arrow_strata.csv"


def _effect(cluster: str, value: float, level: str) -> dict[str, str]:
    row = {field: "" for field in EFFECT_FIELDS}
    row.update({
        "effect_id": f"{cluster}_{level}",
        "study_id": cluster,
        "study_cluster_id": cluster,
        "route": "A_to_antagonism",
        "trait_role": "A",
        "trait_class": "visual_signal",
        "outcome_class": "floral_damage_proportion",
        "design_class": "observational",
        "effect_input_type": "reported_effect",
        "effect_metric": "log_odds_ratio",
        "effect_value": str(value),
        "standard_error": "0.15",
        "effect_orientation": ORIENTATION,
        "is_primary_effect": "true",
        "analysis_status": "eligible_for_quantitative_synthesis",
    })
    row["moderator_variable"] = "pollination_generalization"
    row["moderator_level"] = level
    return row


def test_moderator_hypotheses_flow_through_pipeline() -> None:
    rows = [
        _effect("g1", 0.9, "generalized"),
        _effect("g2", 1.0, "generalized"),
        _effect("g3", 0.8, "generalized"),
        _effect("s1", 0.0, "specialized"),
        _effect("s2", -0.1, "specialized"),
        _effect("s3", 0.1, "specialized"),
    ]
    hypotheses = [{
        "label": "demo",
        "route": "A_to_antagonism",
        "trait_class": "visual_signal",
        "outcome_class": "floral_damage_proportion",
        "effect_metric": "log_odds_ratio",
        "design_class": "observational",
        "moderator_variable": "pollination_generalization",
        "low_level": "specialized",
        "high_level": "generalized",
        "predicted_contrast_sign": "positive",
    }]
    out = run_moderator_hypotheses(rows, hypotheses)
    assert len(out) == 1
    assert out[0]["part_i_parameter"] == "d_A"
    assert out[0]["status"] == "moderator_supported"


def test_break_even_map_reflects_tracking_scenario() -> None:
    config = {
        "case_grid": {
            "attraction": [0.5],
            "defence": [0.5],
            "assurance": [0.0],
            "pollinator_service": [0.5],
            "floral_damage_pressure": [0.5],
        },
        "channel_envelopes": {
            "high_tracking": {
                "attraction_gain": 1.2,
                "attraction_tracking": 1.6,
                "floral_defence_efficacy": 0.9,
                "defence_pollinator_cost": 0.3,
            },
        },
        "shared_cost_scenarios": [0.1],
    }
    rows = run_break_even_map(config)
    assert len(rows) == 1
    assert rows[0]["regime_at_c_AD_0.1"] == "complementary"


def test_full_pipeline_on_repo_inputs_is_honest(tmp_path) -> None:
    hypotheses = json.loads(
        open("configs/part_b_moderator_hypotheses.json", encoding="utf-8").read()
    )["hypotheses"]
    break_even_config = json.loads(
        open("configs/part_b_break_even_scenarios.json", encoding="utf-8").read()
    )
    diagnostics = write_part_b_outputs(
        tmp_path,
        route_rows=read_csv_rows(REPO_ROUTE_RECORDS),
        effect_rows=read_csv_rows(REPO_EFFECTS),
        strata=read_strata(REPO_STRATA),
        moderator_hypotheses=hypotheses,
        break_even_config=break_even_config,
    )
    # Five verified anchors are eligible, but none pool (each is a single cluster).
    assert diagnostics["b2_eligible_primary_effects"] == 5
    assert diagnostics["b2_pooled_strata"] == 0
    # Moderator hypotheses run but have no coded data yet.
    assert diagnostics["b3_moderator_hypotheses"] == 3
    assert diagnostics["b3_supported"] == 0
    assert diagnostics["b3_contradicted"] == 0
    # The two d_A anchors occupy different compatibility strata, so they are not a
    # within-stratum sign conflict and do not warrant a B3 moderator claim yet.
    assert diagnostics["b5_arrows_within_stratum_conflict"] == 0
    assert diagnostics["b5_arrows_cross_stratum_heterogeneity"] == 1
    # All five artefacts plus diagnostics were written.
    for name in (
        "part_b_b1_direction_map.csv",
        "part_b_b2_arrow_envelopes.csv",
        "part_b_b3_moderator_contrasts.csv",
        "part_b_b4_break_even_regime_map.csv",
        "part_b_b5_arrow_evidence_priority.csv",
        "part_b_diagnostics.json",
    ):
        assert (tmp_path / name).exists()
