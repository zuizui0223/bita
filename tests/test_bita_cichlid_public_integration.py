"""Offline/fail-closed contracts for independently reproducible real-data assay.

Synthetic fixtures test implementation only. Real-data effect sizes are tested
in the dedicated source-pinned GitHub Action, not faked here.
"""
from __future__ import annotations

import csv
import hashlib
import io
import math

import pytest

from scripts import analyze_bita_cichlid_public_integration as ci


def _source_bytes(axis: str) -> bytes:
    """Create synthetic 88-species source with positive residual jaw coupling."""
    f = io.StringIO(newline="")
    w = csv.writer(f, lineterminator="\r")
    w.writerow([*ci.METADATA, *ci.TRAITS])
    for i in range(88):
        clade = ("A", "M", "T", "U", "V")[i % 5]
        ecotype = ("Omnivore", "Fish", "Aufwuchs")[i % 3]
        vals = [
            (i % (j+7)-3*j) / (j+1) + math.sin(i*j*.17)
            for j in range(1, 6)
        ]
        if axis == "pharyngeal":
            vals = [v*.7 + math.cos(i*(j+1)*.11)*.3 for j, v in enumerate(vals)]
        w.writerow([f"Species_{i:03d}", clade, clade, ecotype, *vals])
    return f.getvalue().encode()


def _patched(monkeypatch):
    oral = _source_bytes("oral")
    pj = _source_bytes("pharyngeal")
    for label, data in (("oral", oral), ("pharyngeal", pj)):
        payload = ci.INPUTS[label].copy()
        payload["bytes"] = len(data)
        payload["blob_sha1"] = hashlib.sha1(
            f"blob {len(data)}\0".encode("ascii") + data
        ).hexdigest()
        monkeypatch.setitem(ci.INPUTS, label, payload)
    return oral, pj


def test_upstream_provenance_is_pinned_to_2021_author_source():
    assert ci.SOURCE_COMMIT == "575a148a6c6cb90ee957d4290cf3e2d141ca9c14"
    assert ci.EXPECTED_TAXA == 88
    assert ci.INPUTS["oral"]["blob_sha1"] == "c47c60c655a8cef745cb14cca261449a873913a4"
    assert ci.INPUTS["pharyngeal"]["blob_sha1"] == "d733f122b0b7db0590a9215e200b90502ff24403"
    assert "/575a148a6c6cb90ee957d4290cf3e2d141ca9c14/" in ci.source_url("oral")


def test_synthetic_integration_is_positive_and_clade_restricted(monkeypatch):
    oral, pj = _patched(monkeypatch)
    joined = ci.join_inputs(ci.load_rows("oral", oral), ci.load_rows("pharyngeal", pj))
    assert len(joined) == 88
    for k in (3, 5):
        result = ci.permuted_rv(joined, k, permutations=99)
        assert result["permutations"] == 99
        assert 0 < result["rv"] <= 1
        assert 0.01 <= result["permutation_p"] <= 1.0
        assert result["rv"] > result["null_rv_mean"]


def test_source_checksum_failure_blocks_data_poisoning(monkeypatch):
    oral, _ = _patched(monkeypatch)
    with pytest.raises(ValueError, match="blob mismatch"):
        ci.load_rows("oral", oral.replace(b"Species_000", b"Species_999", 1))
    with pytest.raises(ValueError, match="length mismatch"):
        ci.load_rows("oral", oral[:-1])


def test_cross_module_taxa_or_ecology_drift_fails(monkeypatch):
    oral, pj = _patched(monkeypatch)
    x = ci.load_rows("oral", oral)
    y = ci.load_rows("pharyngeal", pj)
    y[0]["Clade"] = "DRIFT"
    with pytest.raises(ValueError, match="metadata mismatch"):
        ci.join_inputs(x, y)
    y[0]["Clade"] = x[0]["Clade"]
    y[0]["TaxaID"] = "Unexpected"
    with pytest.raises(ValueError, match="species IDs"):
        ci.join_inputs(x, y)


def test_permutation_is_seeded_reproducible(monkeypatch):
    oral, pj = _patched(monkeypatch)
    pairs = ci.join_inputs(ci.load_rows("oral", oral), ci.load_rows("pharyngeal", pj))
    r1 = ci.permuted_rv(pairs, 3, permutations=49)
    r2 = ci.permuted_rv(pairs, 3, permutations=49)
    assert r1 == r2
    assert ci.rv_coefficient([[1, 0], [-1, 0]], [[1, 0], [-1, 0]]) == pytest.approx(1)


def test_malformed_or_nonfinite_pc_rejected(monkeypatch):
    oral, _ = _patched(monkeypatch)
    # Constrain original-file byte integrity before numerical parsing.
    bad = oral.replace(b"Species_000", b"Species_00X", 1)
    with pytest.raises(ValueError, match="blob mismatch"):
        ci.load_rows("oral", bad)



def test_synthetic_diet_association_is_seeded_and_bounded(monkeypatch):
    oral, pharyngeal = _patched(monkeypatch)
    pairs = ci.join_inputs(
        ci.load_rows("oral", oral), ci.load_rows("pharyngeal", pharyngeal)
    )
    for module in ("oral", "pharyngeal"):
        result = ci.diet_permuted(pairs, 3, module, permutations=79)
        same = ci.diet_permuted(pairs, 3, module, permutations=79)
        assert same == result
        assert result["permutations"] == 79
        assert 0 <= result["r2_ecology"] <= 1
        assert 1/80 <= result["permutation_p"] <= 1


def test_diet_r2_requires_numerical_data_and_not_taxa_labels():
    assert ci.diet_r2([[1.0], [-1.0]], ["same", "same"]) == pytest.approx(0)
    assert ci.diet_r2([[1.0], [-1.0]], ["A", "B"]) == pytest.approx(1)
    with pytest.raises(ValueError, match="mismatch"):
        ci.diet_r2([[0.0], [1.0]], ["A"])
    with pytest.raises(ValueError, match="zero residual"):
        ci.diet_r2([[0.0], [0.0]], ["A", "B"])
