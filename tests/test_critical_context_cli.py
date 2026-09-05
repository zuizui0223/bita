import csv
from pathlib import Path

import pytest

from scripts.compare_sch_bita_critical_contexts import EXPECTED_SEMANTICS, REQUIRED_FIELDS, compare_files


def _write(path: Path, rows: list[tuple[str, float, float, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REQUIRED_FIELDS)
        writer.writeheader()
        for context_id, context_value, margin, scale in rows:
            writer.writerow(
                {
                    "context_id": context_id,
                    "context_value": context_value,
                    "margin": margin,
                    "fitness_scale_id": scale,
                    "margin_semantics": EXPECTED_SEMANTICS,
                }
            )


def test_file_comparator_recovers_same_critical_context(tmp_path: Path) -> None:
    sch = tmp_path / "sch.csv"
    bita = tmp_path / "bita.csv"
    _write(sch, [("a", 0.0, -1.0, "seed"), ("b", 2.0, 1.0, "seed")])
    _write(bita, [("a", 0.0, -2.0, "seed"), ("b", 2.0, 2.0, "seed")])
    result = compare_files(sch, bita, {"context_tolerance": 0.05})
    assert result["sch_critical_context"] == 1.0
    assert result["bita_critical_context"] == 1.0
    assert result["classification"] == "SAME_CRITICAL_CONTEXT_COMPATIBLE"


def test_file_comparator_rejects_noncommensurable_scales(tmp_path: Path) -> None:
    sch = tmp_path / "sch.csv"
    bita = tmp_path / "bita.csv"
    _write(sch, [("a", 0.0, -1.0, "seed"), ("b", 2.0, 1.0, "seed")])
    _write(bita, [("a", 0.0, -1.0, "fruit"), ("b", 2.0, 1.0, "fruit")])
    with pytest.raises(ValueError, match="same fitness_scale_id"):
        compare_files(sch, bita, {"context_tolerance": 0.05})
