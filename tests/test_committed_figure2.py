from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "empirical" / "part_i_robustness" / "endpoint_normalized_grid_v2_report.json"
FIGURE = ROOT / "manuscript" / "figures" / "FIGURE_2_THEORY_REGIME_MAP.svg"


def test_committed_figure2_matches_canonical_scenario_readout() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    svg = FIGURE.read_text(encoding="utf-8")

    assert report["run_id"] == "endpoint_normalized_grid_v2"
    assert report["evaluation_count"] == 2592
    assert report["evaluation_sign_counts"] == {
        "complementary": 1342,
        "substitutable": 1250,
        "neutral": 0,
    }

    total_per_scenario = 648
    for scenario in report["scenario_readout"].values():
        expected = 100.0 * scenario["evaluation_complementary"] / total_per_scenario
        assert f"{expected:.1f}% complementary" in svg

    assert "unweighted occupancy fractions of the declared finite grid" in svg
    assert "not empirical probabilities" in svg
    assert "Endpoint-normalized response shapes" in svg
    assert "Interaction environment" in svg
