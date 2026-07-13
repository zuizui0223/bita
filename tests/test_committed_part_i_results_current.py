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


def test_committed_part_i_report_matches_current_config_and_code() -> None:
    config = json.loads(
        (ROOT / "configs" / "part_i_robustness_grid.json").read_text(encoding="utf-8")
    )
    committed = json.loads(
        (
            ROOT
            / "empirical"
            / "part_i_robustness"
            / "initial_grid_report.json"
        ).read_text(encoding="utf-8")
    )

    rows, form_summaries, envelope_summaries = RUNNER.run(config)
    reproduced = RUNNER.build_report(config, rows, form_summaries, envelope_summaries)

    assert committed["case_count"] == reproduced["case_count"]
    assert committed["evaluation_count"] == reproduced["evaluation_count"]
    assert committed["functional_form_summary_count"] == reproduced["functional_form_summary_count"]
    assert committed["neutral_tolerance"] == reproduced["neutral_tolerance"]
    assert committed["neutral_tolerance_scale"] == reproduced["neutral_tolerance_scale"]
    assert committed["response_shape_normalization"] == reproduced["response_shape_normalization"]
    assert committed["functional_form_class_counts"] == reproduced["functional_form_class_counts"]
    assert committed["parameter_envelope_class_counts"] == reproduced["parameter_envelope_class_counts"]

    assert committed["evaluation_sign_counts"] == dict(
        Counter(row["sign"] for row in rows)
    )


def test_committed_scenario_readout_matches_current_modal_and_sign_counts() -> None:
    config = json.loads(
        (ROOT / "configs" / "part_i_robustness_grid.json").read_text(encoding="utf-8")
    )
    committed = json.loads(
        (
            ROOT
            / "empirical"
            / "part_i_robustness"
            / "initial_grid_report.json"
        ).read_text(encoding="utf-8")
    )
    rows, form_summaries, _ = RUNNER.run(config)

    scenario_ids = {
        row["parameter_scenario_id"] for row in rows
    }
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
