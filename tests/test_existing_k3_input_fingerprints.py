import json

import pytest

from scripts.fingerprint_existing_k3_inputs import fingerprint_rows
from trait_architecture.existing_k3_inputs import (
    MATCH_STATUS,
    load_canonical_fingerprints,
    stable_json_sha256,
    validate_existing_network_payloads,
)


def test_existing_network_fingerprint_contract_is_content_sensitive() -> None:
    sakh = [{"tube_length": 1.0, "balance": 0.5}]
    aubert = [{
        "site": "S1",
        "mismatch_log_t_over_b": 0.2,
        "robbery_rate": 0.3,
        "trait_barrier": True,
        "n_interactions": 2,
        "bird_group": "hummingbird",
    }]
    first = fingerprint_rows(sakh, aubert)
    second = fingerprint_rows([{**sakh[0], "balance": 0.6}], aubert)

    assert first["receipt"] == "BITA_EXISTING_K3_INPUT_FINGERPRINTS_V1"
    assert first["networks"]["sakhalkar"]["analysis_units"] == 1
    assert first["networks"]["aubert_ephi"]["analysis_units"] == 1
    assert (
        first["networks"]["sakhalkar"]["stable_json_sha256"]
        != second["networks"]["sakhalkar"]["stable_json_sha256"]
    )
    assert first["networks"]["sakhalkar"]["source_doi"] == "10.5281/zenodo.8398202"
    assert first["networks"]["aubert_ephi"]["source_doi"] == "10.5281/zenodo.14185547"



def _ready_receipt(sakh, aubert):
    return {
        "receipt": "BITA_EXISTING_K3_INPUT_FINGERPRINTS_V1",
        "status": "CANONICAL_PUBLIC_INPUTS_FROZEN",
        "networks": {
            "sakhalkar": {
                "analysis_units": len(sakh),
                "stable_json_sha256": stable_json_sha256(sakh),
                "source_doi": "10.5281/zenodo.8398202",
            },
            "aubert_ephi": {
                "analysis_units": len(aubert),
                "stable_json_sha256": stable_json_sha256(aubert),
                "source_doi": "10.5281/zenodo.14185547",
            },
        },
    }


def test_canonical_validator_accepts_only_exact_frozen_payloads(tmp_path) -> None:
    sakh = [{"tube_length": 1.0, "balance": 0.5, "route_class": "mixed"}]
    aubert = [{
        "site": "S1",
        "mismatch_log_t_over_b": 0.2,
        "robbery_rate": 0.3,
        "trait_barrier": True,
        "n_interactions": 2,
        "bird_group": "hummingbird",
    }]
    path = tmp_path / "fingerprints.json"
    path.write_text(json.dumps(_ready_receipt(sakh, aubert)), encoding="utf-8")

    result = validate_existing_network_payloads(
        sakh,
        aubert,
        receipt_path=path,
    )
    assert result["status"] == MATCH_STATUS
    assert result["failures"] == []

    changed = [{**sakh[0], "balance": 0.6}]
    result = validate_existing_network_payloads(
        changed,
        aubert,
        receipt_path=path,
    )
    assert result["status"] == "CANONICAL_EXISTING_K3_INPUTS_MISMATCH"
    assert "canonical_stable_digest_mismatch:sakhalkar" in result["failures"]


def test_placeholder_canonical_receipt_is_fail_closed() -> None:
    with pytest.raises(ValueError, match="EXISTING_K3_FINGERPRINTS_NOT_FROZEN"):
        load_canonical_fingerprints()
