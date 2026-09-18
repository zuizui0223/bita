from __future__ import annotations

import json
from pathlib import Path

from scripts.build_floral_defence_selectivity_figures_svg import (
    build_figure1,
    build_figure2,
    build_figure3,
)
from trait_architecture.floral_defence_selectivity import load_csv_rows


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "empirical" / "floral_defence_selectivity"


def test_figure1_contains_effective_exposure_threshold_logic() -> None:
    svg = build_figure1()
    assert "Effective-exposure selectivity" in svg
    assert "x_H*" in svg
    assert "x_P*" in svg
    assert "selective / guarded" in svg
    assert "bypass" in svg.lower()


def test_figure2_contains_all_matched_systems_and_exact_gate() -> None:
    rows = load_csv_rows(MODULE / "results" / "analysis_ready_matched_systems.csv")
    gate = json.loads((MODULE / "results" / "stage2_model_gate.json").read_text(encoding="utf-8"))
    svg = build_figure2(rows, gate)

    assert len(rows) == 17
    assert "17 matched floral systems" in svg
    assert "Thunia alba" in svg
    assert "Caryopteris divaricata" in svg
    assert "Gelsemium sempervirens" in svg
    assert "Fisher p = 0.333" in svg
    assert "null-compatible" in svg
    assert "domain vs modality not identified" in svg.lower()


def test_figure2_does_not_duplicate_study_cluster_rows() -> None:
    rows = load_csv_rows(MODULE / "results" / "analysis_ready_matched_systems.csv")
    gate = json.loads((MODULE / "results" / "stage2_model_gate.json").read_text(encoding="utf-8"))
    svg = build_figure2(rows, gate)

    for cluster in {row["study_cluster_id"] for row in rows}:
        # Cluster ids are carried as one invisible data attribute per rendered row.
        assert svg.count(f'data-cluster="{cluster}"') == 1


def test_figure3_preserves_all_eight_conditionality_clusters() -> None:
    rows = load_csv_rows(MODULE / "d_side_conditionality_registry.csv")
    svg = build_figure3(rows)

    assert len(rows) == 8
    assert "8 defence-side state-switch systems" in svg
    assert "Polemonium viscosum" in svg
    assert "Aconitum lycoctonum" in svg
    assert "Nicotiana attenuata" in svg
    assert "same trait, different ecological state" in svg.lower()
    for cluster in {row["study_cluster_id"] for row in rows}:
        assert svg.count(f'data-cluster="{cluster}"') == 1
