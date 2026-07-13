from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "run_part_i_robustness.py"
SPEC = importlib.util.spec_from_file_location("current_part_i_runner", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RUNNER
SPEC.loader.exec_module(RUNNER)
REPORT_PATH = (
    ROOT
    / "empirical"
    / "part_i_robustness"
    / "endpoint_normalized_grid_v2_report.json"
)


def _committed_report() -> dict:
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


def test_committed_part_i_report_matches_current_config_and_code() -> None:
    config = json.loads(
        (ROOT / "configs" / "part_i_robustness_grid.json").read_text(encoding="utf-8")
    )
    committed = _committed_report()

    rows, form_summaries, full_tested_set_summaries = RUNNER.run(config)
    reproduced = RUNNER.build_report(
        config, rows, form_summaries, full_tested_set_summaries
    )

    for key in (
        "run_id",
        "case_count",
        "evaluation_count",
        "functional_form_summary_count",
        "neutral_tolerance",
        "neutral_tolerance_scale",
        "response_shape_normalization",
        "finite_design_measure",
        "minimum_absolute_mixed_partial",
        "neutral_evaluation_count",
        "near_tolerance_evaluation_count",
        "functional_form_class_counts",
        "full_tested_set_class_counts",
    ):
        assert committed[key] == reproduced[key]

    sign_counts = Counter(row["sign"] for row in rows)
    reproduced_sign_counts = {
        sign: sign_counts.get(sign, 0)
        for sign in ("complementary", "substitutable", "neutral")
    }
    assert committed["evaluation_sign_counts"] == reproduced_sign_counts


def test_committed_scenario_readout_matches_current_modal_and_sign_counts() -> None:
    config = json.loads(
        (ROOT / "configs" / "part_i_robustness_grid.json").read_text(encoding="utf-8")
    )
    committed = _committed_report()
    rows, form_summaries, _ = RUNNER.run(config)

    scenario_ids = {row["parameter_scenario_id"] for row in rows}
    assert scenario_ids == set(committed["scenario_readout"])

    for scenario_id in scenario_ids:
        scenario_rows = [
            row for row in rows if row["parameter_scenario_id"] == scenario_id
        ]
        scenario_summaries = [
            row
            for row in form_summaries
            if row["parameter_scenario_id"] == scenario_id
        ]
        expected = committed["scenario_readout"][scenario_id]
        sign_counts = Counter(row["sign"] for row in scenario_rows)
        modal_counts = Counter(row["modal_sign"] for row in scenario_summaries)
        class_counts = Counter(
            row["functional_form_class"] for row in scenario_summaries
        )

        assert expected["evaluation_complementary"] == sign_counts["complementary"]
        assert expected["evaluation_substitutable"] == sign_counts["substitutable"]
        assert expected["modal_complementary"] == modal_counts["complementary"]
        assert expected["modal_substitutable"] == modal_counts["substitutable"]
        assert expected["modal_mixed"] == modal_counts["mixed"]
        assert expected["functional_form_tested_set_unanimous"] == class_counts[
            "tested_set_unanimous"
        ]
        assert expected["functional_form_mixed_or_sensitive"] == class_counts[
            "mixed_or_sensitive"
        ]
