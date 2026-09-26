from scripts.screen_direct_access_geometry_oa_fulltext_structural import classify_fulltext, MIN_EXTRACTED_CHARS


def _pad(text: str) -> str:
    return text + " filler" * (MIN_EXTRACTED_CHARS // 6 + 100)


def test_retain_when_route_and_geometry_signals_present() -> None:
    text = _pad("nectar robbing increased with corolla length")
    assert classify_fulltext(text) == "RETAIN_STRUCTURAL_SIGNALS_PRESENT"


def test_exclude_when_route_signal_absent() -> None:
    text = _pad("corolla length affected legitimate visitation and pollen transfer")
    assert classify_fulltext(text) == "EXCLUDE_NO_ROUTE_SIGNAL"


def test_exclude_when_geometry_signal_absent() -> None:
    text = _pad("nectar robbing affected seed production and flower visitation")
    assert classify_fulltext(text) == "EXCLUDE_NO_GEOMETRY_SIGNAL"


def test_short_extraction_is_retained() -> None:
    assert classify_fulltext("nectar robbing corolla length") == "RETAIN_EXTRACTION_INSUFFICIENT"
