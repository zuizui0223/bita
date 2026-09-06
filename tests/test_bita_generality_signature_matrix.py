import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "BITA_GENERALITY_SIGNATURE_MATRIX_V1.csv"


def _rows():
    with MATRIX.open(encoding="utf-8", newline="") as handle:
        return {row["system"]: row for row in csv.DictReader(handle)}


def test_pedicularis_same_system_release_is_not_marked_executed():
    rows = _rows()
    assert rows["Pedicularis_rex"]["release_status"] == "R_STATE_NOT_YET_EXECUTED"


def test_peucedanum_remains_natural_partial_differentiation_anchor():
    rows = _rows()
    assert rows["Peucedanum_multivittatum"]["release_status"] == "CAUSAL_R_STATE_NOT_IDENTIFIED"
    assert "NATURAL_PARTIAL" in rows["Peucedanum_multivittatum"]["program_role"]


def test_cross_domain_and_history_anchors_are_not_parameterized_bita_proofs():
    rows = _rows()
    assert "do_not_assign_s_K" in rows["Cichlid_oral_pharyngeal_jaws"]["next_gate"]
    assert rows["Dalechampia"]["release_status"] == "CONTEMPORARY_CAUSAL_RELEASE_NOT_IDENTIFIED"


def test_hisa_trpf_is_experimental_differentiation_anchor_not_bita_threshold_test():
    rows = _rows()
    item = rows["Salmonella_HisA_TrpF"]
    assert item["program_role"] == "G2_CROSS_DOMAIN_EXPERIMENTAL_DIFFERENTIATION_ANCHOR"
    assert "do_not_assign_BITA_s_K_R_state" in item["next_gate"]
