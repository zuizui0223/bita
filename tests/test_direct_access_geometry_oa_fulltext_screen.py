from scripts.screen_direct_access_geometry_oa_fulltext import (
    ACCESS_RE,
    QUANT_RE,
    ROUTE_RE,
    _title_coverage,
)


def test_route_patterns_cover_primary_robbery_language() -> None:
    assert ROUTE_RE.search("nectar robbing increased at long flowers")
    assert ROUTE_RE.search("floral larceny was recorded")
    assert ROUTE_RE.search("illegitimate visits were scored")


def test_access_patterns_cover_geometry_and_mismatch() -> None:
    assert ACCESS_RE.search("corolla length was measured")
    assert ACCESS_RE.search("tongue length mismatch")
    assert ACCESS_RE.search("legitimate access was constrained")


def test_quantitative_patterns_cover_common_tests() -> None:
    assert QUANT_RE.search("we fitted a regression model")
    assert QUANT_RE.search("robbery frequency")
    assert QUANT_RE.search("p < 0.05")


def test_title_coverage_detects_matching_pdf_text() -> None:
    title = "Trait matching affects the probability of nectar robbing in plant pollinator networks"
    text = "Trait matching affects the probability of nectar robbing in plant pollinator networks\nMethods..."
    assert _title_coverage(title, text) >= 0.8


def test_title_coverage_rejects_unrelated_pdf() -> None:
    title = "Trait matching affects the probability of nectar robbing in plant pollinator networks"
    text = "A completely unrelated article on marine sediment biogeochemistry"
    assert _title_coverage(title, text) < 0.4
