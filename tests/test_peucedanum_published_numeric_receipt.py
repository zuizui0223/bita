from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "empirical" / "identification_design" / "PEUCEDANUM_PUBLISHED_NUMERIC_RECEIPT_V1.json"


def test_published_receipt_recovers_key_cross_study_results_without_overclaim() -> None:
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert receipt["status"] == "PUBLISHED_NUMERIC_PARTIAL_DIFFERENTIATION_EVIDENCE_RECOVERED"
    assert receipt["data_status"] == "PUBLISHED_RESULTS_ONLY_NOT_RAW_DRYAD_REANALYSIS"

    study_2021 = receipt["sources"][0]["published_numeric_results"]
    association = study_2021["population_male_flower_proportion_vs_seed_predation"]
    assert association["direction"] == "positive"
    assert association["r_squared"] == 0.64
    assert association["p"] == "<0.0001"
    assert study_2021["individual_predation_glmm"]["flowering_time"]["estimate"] == -0.803
    assert study_2021["individual_predation_glmm"]["male_flower_number"]["p"] == 0.63

    study_2025 = receipt["sources"][1]["published_numeric_results"]
    assert study_2025["high_predation_focal_experiment_n"] == 106
    assert study_2025["perfect_vs_male_flower_correlation"]["r"] == -0.43
    assert study_2025["estimated_fruit_predation_rate"]["mean"] == 0.57
    assert study_2025["initial_fruit_set_selection_differentials"]["perfect_flower_number"]["S"] == 0.100

    predation = study_2025["predation_selection"]
    assert predation["perfect_flower_number"]["beta"] == 0.178
    assert predation["male_flower_number"]["beta"] == -0.042
    assert predation["perfect_flower_number"]["S"] == 0.218
    assert predation["male_flower_number"]["S"] == -0.087

    final_fruit = study_2025["final_fruit_set_selection"]
    assert final_fruit["perfect_flower_number"]["beta"] == -0.108
    assert final_fruit["male_flower_number"]["beta"] == 0.006

    oviposition = study_2025["oviposition_glmm"]
    assert oviposition["perfect_flower_number"]["z"] == 5.97
    assert oviposition["male_flower_number"]["z"] == -2.38

    recovery = receipt["cross_study_recovery"]
    assert recovery["perfect_flower_predation_cross_loading"].startswith("SUPPORTED")
    assert recovery["male_flower_predation_relief"].startswith("SUPPORTED")
    assert recovery["partial_functional_differentiation_interpretation"].startswith("SUPPORTED")
    assert recovery["causal_R_state"] == "NOT_IDENTIFIED"
    assert recovery["historical_origin_of_andromonoecy"] == "NOT_IDENTIFIED"
    assert "not_raw_reanalysis" in receipt["claim_ceiling"]
