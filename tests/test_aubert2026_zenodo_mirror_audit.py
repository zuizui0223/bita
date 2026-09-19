from __future__ import annotations

from scripts.audit_aubert2026_zenodo_mirror import _read, summarize_tables


def test_read_and_aggregate_schema_without_raw_rows() -> None:
    interactions = (
        b"site\tnectar_robbing\tbird_family\n"
        b"A\tyes\tTrochilidae\n"
        b"A\tno\tTrochilidae\n"
        b"B\tyes\tThraupidae\n"
    )
    header, rows = _read(interactions)
    result = summarize_tables({
        "interactions": (header, rows),
        "cameras": (["waypoint"], [{"waypoint": "w1"}]),
        "plants": (["plant_species"], [{"plant_species": "p1"}]),
        "birds": (["species"], [{"species": "b1"}]),
    })
    x = result["tables"]["interactions"]
    assert x["rows"] == 3
    assert x["sites"] == ["A", "B"]
    assert x["site_count"] == 2
    assert x["nectar_robbing_counts"] == {"no": 1, "yes": 2}
    assert x["bird_family_counts"] == {"Thraupidae": 1, "Trochilidae": 2}
    assert "raw_rows" not in result
