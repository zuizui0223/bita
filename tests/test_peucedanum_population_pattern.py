from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.analyze_peucedanum_population_pattern import REQUIRED_FIELDS, analyze


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "identification_design" / "PEUCEDANUM_POPULATION_PATTERN_TEMPLATE_V1.csv"
CONFIG = ROOT / "empirical" / "identification_design" / "PEUCEDANUM_POPULATION_PATTERN_CONFIG_V1.json"
CONTRACT = ROOT / "docs" / "BITA_PEUCEDANUM_DRYAD_IMPORT_CONTRACT_V1.md"


def _config() -> dict:
    return {
        "min_populations_per_dataset": 5,
        "min_positive_male_fraction_predation_rho": 0.6,
        "max_negative_flowering_predation_rho": -0.6,
    }


def _rows(reverse_male_pattern: bool = False) -> list[dict[str, str]]:
    rows = []
    for dataset in ("D2021", "D2025"):
        for i in range(7):
            pred = (6 - i) / 6
            male_fraction = (i / 6) if reverse_male_pattern else pred
            rows.append(
                {
                    "dataset_id": dataset,
                    "source_doi": "10.5061/dryad.example",
                    "year": "2021" if dataset == "D2021" else "2025",
                    "population_id": f"P{i}",
                    "mean_flowering_day": str(100 + i),
                    "male_flower_mean": str(10 + 20 * male_fraction),
                    "perfect_flower_mean": str(30 - 10 * pred),
                    "male_fraction": str(male_fraction),
                    "fruit_set_mean": "0.5",
                    "seed_predation_rate": str(pred),
                    "n_plants": "20",
                }
            )
    return rows


def test_registered_template_and_config_are_fail_closed() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    assert cfg["min_populations_per_dataset"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in cfg["status"]


def test_directionally_consistent_geographic_pattern_is_supported() -> None:
    result = analyze(_rows(False), _config())
    assert result["status"] == "OBSERVATIONAL_GEOGRAPHIC_PARTIAL_DIFFERENTIATION_PATTERN_SUPPORTED"
    assert result["n_directionally_consistent_datasets"] == 2
    for summary in result["dataset_results"].values():
        assert summary["estimands"]["rho_male_fraction_vs_predation"] > 0.9
        assert summary["estimands"]["rho_flowering_day_vs_predation"] < -0.9
        assert all(summary["gates"].values())


def test_reversed_male_allocation_pattern_is_rejected() -> None:
    result = analyze(_rows(True), _config())
    assert result["status"] == "OBSERVATIONAL_PATTERN_NOT_FULLY_RECOVERED"
    assert all(
        not summary["gates"]["male_fraction_tracks_predation"]
        for summary in result["dataset_results"].values()
    )


def test_contract_keeps_observational_pattern_below_causal_release() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "OBSERVATIONAL_GEOGRAPHIC_PARTIAL_DIFFERENTIATION_PATTERN" in text
    assert "does **not** identify" in text
    assert "R_state" in text
    assert "10.5061/dryad.b5mkkwhcq" in text
    assert "10.5061/dryad.w3r2280v5" in text
