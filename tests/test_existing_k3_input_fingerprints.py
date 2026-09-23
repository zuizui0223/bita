from scripts.fingerprint_existing_k3_inputs import fingerprint_rows


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
