import copy

import pytest

from scripts.fingerprint_existing_k3_inputs import fingerprint_rows
from trait_architecture.existing_k3_inputs import (
    canonical_stable_json_sha256,
    canonicalize_aubert,
    canonicalize_sakhalkar,
)


def _sakh():
    return [
        {"tube_length": 0.0, "balance": 1.0, "route_class": "robber_only"},
        {"tube_length": 2.0, "balance": -1.0, "route_class": "thief_only"},
        {"tube_length": 1.0, "balance": 0.25, "route_class": "mixed"},
    ]


def _aubert():
    return [
        {
            "site": "alpha",
            "bird_group": "hummingbird",
            "n_interactions": 3,
            "robbery_rate": 1 / 3,
            "mismatch_log_t_over_b": 0.2,
            "trait_barrier": True,
        },
        {
            "site": "beta",
            "bird_group": "flowerpiercer",
            "n_interactions": 2,
            "robbery_rate": 0.0,
            "mismatch_log_t_over_b": -0.3,
            "trait_barrier": False,
        },
        {
            "site": "alpha",
            "bird_group": "flowerpiercer",
            "n_interactions": 5,
            "robbery_rate": 0.4,
            "mismatch_log_t_over_b": -0.1,
            "trait_barrier": False,
        },
    ]


def test_sakhalkar_zero_tube_length_is_retained_not_rejected() -> None:
    rows = canonicalize_sakhalkar(_sakh())
    assert len(rows) == 3
    assert rows[0]["tube_length"] == 0.0


def test_aubert_digest_is_invariant_to_row_order_and_arbitrary_site_labels() -> None:
    rows = _aubert()
    first = canonical_stable_json_sha256("aubert_ephi", rows)

    relabelled = []
    for row in reversed(rows):
        changed = copy.deepcopy(row)
        changed["site"] = {"alpha": "ZZZ", "beta": "AAA"}[row["site"]]
        relabelled.append(changed)

    second = canonical_stable_json_sha256("aubert_ephi", relabelled)
    assert first == second
    assert canonicalize_aubert(rows) == canonicalize_aubert(relabelled)


def test_fingerprint_is_content_sensitive_not_label_sensitive() -> None:
    first = fingerprint_rows(_sakh(), _aubert())
    changed = copy.deepcopy(_aubert())
    changed[0]["robbery_rate"] = 2 / 3
    second = fingerprint_rows(_sakh(), changed)
    assert (
        first["networks"]["aubert_ephi"]["canonical_stable_json_sha256"]
        != second["networks"]["aubert_ephi"]["canonical_stable_json_sha256"]
    )


def test_canonicalizers_reject_inconsistent_derived_fields() -> None:
    bad = _sakh()
    bad[0]["route_class"] = "mixed"
    with pytest.raises(ValueError, match="route_class is inconsistent"):
        canonicalize_sakhalkar(bad)

    bad_aubert = _aubert()
    bad_aubert[0]["trait_barrier"] = False
    with pytest.raises(ValueError, match="trait_barrier is inconsistent"):
        canonicalize_aubert(bad_aubert)
