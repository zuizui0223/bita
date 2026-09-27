from scripts.screen_direct_access_geometry_openalex_title_abstract import (
    _abstract_text,
    classify_title_abstract,
)


def test_abstract_reconstruction_orders_tokens() -> None:
    index = {
        "Nectar": [0],
        "robbers": [1],
        "bypass": [3],
        "flowers": [4],
        "can": [2],
    }
    assert _abstract_text(index) == "Nectar robbers can bypass flowers"


def test_route_signal_is_retained_for_fulltext() -> None:
    assert (
        classify_title_abstract(
            "Flower morphology and visitor behavior",
            "Short-tongued bees frequently engage in nectar robbing.",
        )
        == "FULLTEXT_REQUIRED"
    )


def test_no_route_signal_can_be_excluded() -> None:
    assert (
        classify_title_abstract(
            "Flower size and pollination",
            "We measured legitimate visitation and pollen transfer across populations.",
        )
        == "EXCLUDE_NO_ROUTE_SIGNAL"
    )


def test_missing_abstract_is_never_auto_excluded() -> None:
    assert classify_title_abstract("Floral morphology", "") == "FULLTEXT_REQUIRED"
