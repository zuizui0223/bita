from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "reanalyze_impatiens_identification_retrofit.py"
SPEC = importlib.util.spec_from_file_location("impatiens_retrofit", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def _synthetic_rows() -> list[dict[str, str]]:
    rows = []
    index = 0
    for rep in range(8):
        for r in ("N", "Y"):
            for f in ("N", "Y"):
                for p in ("N", "Y"):
                    # Continuous observational A/D values vary inside each randomized cell.
                    a = -1.2 + 0.35 * (rep % 4) + 0.08 * (index % 3)
                    d = -0.9 + 0.28 * ((rep + 1) % 5) - 0.05 * (index % 2)
                    rc = -0.5 if r == "N" else 0.5
                    fc = -0.5 if f == "N" else 0.5
                    pc = -0.5 if p == "N" else 0.5
                    # Inject a positive A:D modification by randomized Robbing only.
                    y1 = 2.0 + 0.2*a - 0.1*d + 0.3*a*d + 0.7*a*d*rc + 0.05*rep + 0.01*(index % 5)
                    y2 = 10.0 + 0.4*a + 0.2*d - 0.2*a*d + 0.5*a*d*rc + 0.03*rep + 0.02*(index % 7)
                    rows.append({
                        "Early_Season_Flower_Redness": str(a),
                        "Early_Season_Condensed_Tannins": str(d),
                        "Date_of_First_CH_Flower": str(100 + rep + (index % 4)),
                        "Robbing": r,
                        "Florivory": f,
                        "Pollination": p,
                        "Average_CH_Fruits_Per_Day": str(max(0.0, y1)),
                        "Average_Seeds_Per_CH_Fruit": str(y2),
                    })
                    index += 1
    return rows


def test_registered_model_recovers_randomized_AxD_robbing_modification() -> None:
    report = MODULE.analyze(_synthetic_rows())
    assert report["analysis_id"] == "impatiens_2018_identification_retrofit_v1"
    assert len(report["model_summaries"]) == 2
    for summary in report["model_summaries"]:
        assert summary["n_complete"] == 64
        assert summary["minimum_cell_n"] == 8
        assert summary["maximum_cell_n"] == 8
        rob = summary["target_coefficients"]["A_z:D_z:Robbing_c"]
        assert rob["estimate"] > 0


def test_output_boundary_does_not_claim_channel_identification() -> None:
    report = MODULE.analyze(_synthetic_rows())
    boundary = report["causal_boundary"]
    for token in ("rho_delta", "iota_delta", "M0_delta", "kappa_delta"):
        assert token in boundary
    assert "do not identify" in boundary
    md = MODULE.render_markdown(report)
    assert "not** a rho/iota/kappa reconstruction" in md
    assert "selective present/excluded channel toggles" in md


def test_design_is_hierarchical_for_targeted_three_way_terms() -> None:
    terms = set(MODULE.TERMS)
    for treatment in ("Robbing_c", "Florivory_c", "Pollination_c"):
        assert f"A_z:D_z:{treatment}" in terms
        assert "A_z:D_z" in terms
        assert f"A_z:{treatment}" in terms
        assert f"D_z:{treatment}" in terms
        assert treatment in terms
