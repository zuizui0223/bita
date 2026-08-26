from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_identification_reaudit_queue.py"
SOURCE = ROOT / "empirical" / "mechanism_pattern_synthesis" / "DIRECT_AXD_AUDIT_V1.csv"


def test_reaudit_queue_keeps_old_unknowns_as_unknown(tmp_path: Path) -> None:
    output = tmp_path / "queue.csv"
    subprocess.run([sys.executable, str(SCRIPT), str(SOURCE), str(output)], check=True)
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 14
    assert rows[0]["study_id"] == "Gorden_Adler_2018_Impatiens_capensis"
    assert rows[0]["reaudit_priority"] == "1"
    assert rows[0]["identification_design_class"] == "TOTAL_INTERACTION_OBSERVATIONAL"

    for row in rows:
        assert row["selective_antagonist_toggle"] == "REQUIRES_SOURCE_REAUDIT"
        assert row["selective_pollinator_toggle"] == "REQUIRES_SOURCE_REAUDIT"
        assert row["m0_delta"] == "REQUIRES_SOURCE_REAUDIT"
        assert row["independent_kappa_assay"] == "REQUIRES_SOURCE_REAUDIT"
        assert "do not infer absence" in row["interpretation"]


def test_high_information_near_misses_are_prioritized() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("reaudit", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    rows = module.build_rows(SOURCE)
    by_id = {row["study_id"]: row for row in rows}

    assert by_id["Kessler_et_al_2015_Nicotiana"]["reaudit_priority"] == "2"
    assert by_id["Santangelo_Thompson_Johnson_2019_Trifolium"]["reaudit_priority"] == "2"
    assert by_id["Garcia_Dow_Vezina_Parachnowitsch_2024_Asclepias"]["reaudit_priority"] == "3"
