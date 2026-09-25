from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.normalize_direct_access_geometry_bibliographic_export import (
    OUTPUT_FIELDS,
    normalize,
)


def test_normalizes_scopus_csv_without_filtering(tmp_path: Path) -> None:
    path = tmp_path / "q1.csv"
    path.write_text(
        "EID,DOI,Title,Year,Authors,Source title,Link\n"
        "2-s2.0-1,10.1/a,Alpha study,2021,A Author,Journal A,https://example/a\n"
        "2-s2.0-2,,Beta study,2022,B Author,Journal B,https://example/b\n",
        encoding="utf-8",
    )
    rows = normalize(
        path,
        fmt="scopus_csv",
        source_db=None,
        query_id="Q1",
        search_date="2026-09-25",
    )
    assert len(rows) == 2
    assert rows[0] == {
        "source_db": "Scopus",
        "query_id": "Q1",
        "record_id": "2-s2.0-1",
        "doi": "10.1/a",
        "title": "Alpha study",
        "year": "2021",
        "authors": "A Author",
        "publication": "Journal A",
        "url": "https://example/a",
        "search_date": "2026-09-25",
    }
    assert rows[1]["title"] == "Beta study"


def test_normalizes_wos_tsv(tmp_path: Path) -> None:
    path = tmp_path / "q2.tsv"
    path.write_text(
        "UT\tDI\tTI\tPY\tAU\tSO\tURL\n"
        "WOS:1\t10.2/test\tGamma\t2020\tG Author\tJournal G\thttps://example/g\n",
        encoding="utf-8",
    )
    rows = normalize(
        path,
        fmt="wos_tsv",
        source_db=None,
        query_id="Q2",
        search_date="2026-09-25",
    )
    assert rows[0]["source_db"] == "WebOfScience"
    assert rows[0]["record_id"] == "WOS:1"
    assert rows[0]["doi"] == "10.2/test"


def test_normalizes_crossref_json(tmp_path: Path) -> None:
    path = tmp_path / "q3.json"
    payload = {
        "message": {
            "items": [
                {
                    "DOI": "10.3/test",
                    "title": ["Delta title"],
                    "published-online": {"date-parts": [[2019, 2, 1]]},
                    "author": [{"given": "D", "family": "Author"}],
                    "container-title": ["Journal D"],
                    "URL": "https://doi.org/10.3/test",
                }
            ]
        }
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    rows = normalize(
        path,
        fmt="crossref_json",
        source_db=None,
        query_id="Q3",
        search_date="2026-09-25",
    )
    assert rows[0]["source_db"] == "Crossref"
    assert rows[0]["record_id"] == "10.3/test"
    assert rows[0]["doi"] == "10.3/test"
    assert rows[0]["year"] == "2019"


def test_normalizes_openalex_json(tmp_path: Path) -> None:
    path = tmp_path / "q4.json"
    payload = {
        "results": [
            {
                "id": "https://openalex.org/W1",
                "doi": "https://doi.org/10.4/test",
                "title": "Epsilon",
                "publication_year": 2024,
                "authorships": [{"author": {"display_name": "E Author"}}],
                "primary_location": {
                    "landing_page_url": "https://example/e",
                    "source": {"display_name": "Journal E"},
                },
            }
        ]
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    rows = normalize(
        path,
        fmt="openalex_json",
        source_db=None,
        query_id="Q4",
        search_date="2026-09-25",
    )
    assert rows[0]["source_db"] == "OpenAlex"
    assert rows[0]["record_id"] == "https://openalex.org/W1"
    assert rows[0]["doi"] == "10.4/test"


def test_rejects_missing_record_id_and_out_of_window_year(tmp_path: Path) -> None:
    missing = tmp_path / "missing.csv"
    missing.write_text(
        "record_id,doi,title,year,authors,publication,url\n"
        ",,Missing ID,2020,A,J,\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="BIB_EXPORT_MISSING_RECORD_ID"):
        normalize(
            missing,
            fmt="generic_csv",
            source_db="ExampleDB",
            query_id="Q5",
            search_date="2026-09-25",
        )

    old = tmp_path / "old.csv"
    old.write_text(
        "record_id,doi,title,year,authors,publication,url\n"
        "x,,Old study,1999,A,J,\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="BIB_EXPORT_YEAR_OUT_OF_WINDOW"):
        normalize(
            old,
            fmt="generic_csv",
            source_db="ExampleDB",
            query_id="Q6",
            search_date="2026-09-25",
        )


def test_rejects_duplicate_record_id_within_query(tmp_path: Path) -> None:
    path = tmp_path / "dup.csv"
    path.write_text(
        "record_id,doi,title,year,authors,publication,url\n"
        "x,,One,2020,A,J,\n"
        "x,,Two,2021,B,J,\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="BIB_EXPORT_DUPLICATE_RECORD_ID_WITHIN_QUERY"):
        normalize(
            path,
            fmt="generic_csv",
            source_db="ExampleDB",
            query_id="Q7",
            search_date="2026-09-25",
        )


def test_output_schema_is_exact() -> None:
    assert OUTPUT_FIELDS == (
        "source_db",
        "query_id",
        "record_id",
        "doi",
        "title",
        "year",
        "authors",
        "publication",
        "url",
        "search_date",
    )
