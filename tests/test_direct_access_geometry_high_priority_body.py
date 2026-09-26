from scripts.adjudicate_direct_access_geometry_high_priority_body import (
    signal_counts,
    strip_reference_tail,
    triage_body,
)


def test_reference_tail_is_cut_when_late() -> None:
    body = "Methods\nnectar robbing and corolla length were measured.\n" + "x" * 3000
    text = body + "\nReferences\nnectar robbing corolla length regression"
    stripped, cut = strip_reference_tail(text)
    assert cut is True
    assert "References" not in stripped


def test_route_only_in_references_does_not_survive_cut() -> None:
    text = "Methods\nWe measured visitation.\n" + "x" * 3000 + "\nReferences\nnectar robbing corolla length"
    stripped, _ = strip_reference_tail(text)
    assert triage_body(stripped) == "EXCLUDE_NO_ROUTE_SIGNAL_IN_MAIN_TEXT"


def test_access_absent_is_excluded() -> None:
    text = "Results\nNectar robbing frequency was modelled with a regression.\n" + "x" * 3000
    assert triage_body(text) == "EXCLUDE_NO_ACCESS_SIGNAL_IN_MAIN_TEXT"


def test_local_cooccurrence_is_retained() -> None:
    text = (
        "Methods\nWe measured corolla length and nectar robbing frequency. "
        "A regression model tested the association.\n"
        + "x" * 3000
    )
    counts = signal_counts(text)
    assert counts["cooccur"] > 0
    assert triage_body(text) == "RETAIN_LOCAL_ROUTE_ACCESS_QUANT_COOCCURRENCE"
