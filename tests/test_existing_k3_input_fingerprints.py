import json

import pytest

from scripts.fingerprint_existing_k3_inputs import fingerprint_rows
from trait_architecture.existing_k3_inputs import (
    MATCH_STATUS,
    canonical_stable_json_sha256,
    load_canonical_fingerprints,
    validate_existing_network_payloads,
)


def test_existing_network_fingerprint_contract_is_content_sensitive() -> None:
    sakh = [{"tube_length": 1.0, "balance": 0.5, "route_class": "mixed"}]
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
        first["networks"]["sakhalkar"]["canonical_stable_json_sha256"]
        != second["networks"]["sakhalkar"]["canonical_stable_json_sha256"]
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
                "canonical_stable_json_sha256": canonical_stable_json_sha256("sakhalkar", sakh),
                "source_doi": "10.5281/zenodo.8398202",
            },
            "aubert_ephi": {
                "analysis_units": len(aubert),
                "canonical_stable_json_sha256": canonical_stable_json_sha256("aubert_ephi", aubert),
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


def test_committed_canonical_receipt_is_frozen_and_well_formed() -> None:
    receipt = load_canonical_fingerprints()
    assert receipt["status"] == "CANONICAL_PUBLIC_INPUTS_FROZEN"
    assert receipt["networks"]["sakhalkar"]["analysis_units"] == 57
    assert receipt["networks"]["aubert_ephi"]["analysis_units"] == 1378
    assert (
        receipt["source_file_integrity"]["sakhalkar"][
            "SaileeSakhalkar/cheaters-among-pollinators-ecosphere-v1.0.0.zip"
        ]["md5"]
        == "c2f722804372c2011a5f60f3afcf8084"
    )
    assert (
        receipt["source_file_integrity"]["aubert_ephi"][
            "Interactions_data_Ecuador.txt"
        ]["md5"]
        == "19cf81367979dd8676fc35713859d638"
    )



def test_canonicalization_rejects_type_coercion_and_inconsistent_rows(tmp_path) -> None:
    sakh = [{"tube_length": 1.0, "balance": 1.0, "route_class": "robber_only"}]
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

    bad_barrier = [{**aubert[0], "trait_barrier": "false"}]
    with pytest.raises(ValueError, match="trait_barrier must be boolean"):
        validate_existing_network_payloads(sakh, bad_barrier, receipt_path=path)

    bad_n = [{**aubert[0], "n_interactions": "2"}]
    with pytest.raises(ValueError, match="n_interactions must be an integer"):
        validate_existing_network_payloads(sakh, bad_n, receipt_path=path)

    bad_sign = [{**aubert[0], "mismatch_log_t_over_b": -0.2}]
    with pytest.raises(ValueError, match="trait_barrier is inconsistent"):
        validate_existing_network_payloads(sakh, bad_sign, receipt_path=path)

    bad_route = [{**sakh[0], "route_class": "mixed"}]
    with pytest.raises(ValueError, match="route_class is inconsistent"):
        validate_existing_network_payloads(bad_route, aubert, receipt_path=path)
