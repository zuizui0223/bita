from __future__ import annotations

import csv
import json

from trait_architecture.d_a_elife_asset_locator import locate_assets, read_screen, write_outputs


XML = b"""<?xml version='1.0' encoding='UTF-8'?>
<article xmlns:xlink='http://www.w3.org/1999/xlink'><body>
  <sec><title>Oviposition trials</title>
    <p>Nectar and scent affected oviposition.</p><xref ref-type='fig' rid='f2'>Figure 2</xref>
  </sec>
</body>
<fig id='f2'><label>Figure 2</label>
  <graphic xlink:href='elife-07641-fig2-v1.jpg'/>
  <media xlink:href='elife-07641-fig2-data1-v1.csv'/>
</fig>
</article>
"""


def _screen() -> dict[str, str]:
    return {
        "candidate_id": "dA_cand_schiestl2015",
        "doi": "10.7554/eLife.07641",
        "xml_url": "https://elifesciences.org/articles/07641.xml",
        "route_structure_signal": "candidate_scent_reward_to_oviposition_structure_needs_numeric_context_check",
    }


def test_locator_collects_only_assets_from_shared_section_figures() -> None:
    rows = locate_assets(
        _screen(),
        fetch_xml=lambda _url: (200, XML),
        fetch_prefix=lambda url: (206, "text/csv" if url.endswith(".csv") else "image/jpeg", b"col1,col2\n"),
    )

    assert len(rows) == 2
    assert {row.asset_kind for row in rows} == {"figure_graphic", "figure_media"}
    data = next(row for row in rows if row.asset_kind == "figure_media")
    assert data.asset_url.endswith("elife-07641-fig2-data1-v1.csv")
    assert data.access_status == "asset_prefix_recovered"
    assert "Do not infer" in data.do_not_infer


def test_read_screen_filters_to_viable_source(tmp_path) -> None:
    path = tmp_path / "screen.csv"
    valid = _screen()
    invalid = {**valid, "route_structure_signal": "term_cooccurrence_without_same_section_link"}
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=valid)
        writer.writeheader()
        writer.writerows([invalid, valid])
    assert read_screen(path)["candidate_id"] == "dA_cand_schiestl2015"


def test_write_outputs_preserves_access_only_boundary(tmp_path) -> None:
    rows = locate_assets(
        _screen(),
        fetch_xml=lambda _url: (200, XML),
        fetch_prefix=lambda _url: (200, "text/csv", b"x,y\n"),
    )
    report = write_outputs(tmp_path, rows)
    with (tmp_path / "d_a_elife_asset_receipts.csv").open(encoding="utf-8", newline="") as handle:
        written = list(csv.DictReader(handle))
    saved = json.loads((tmp_path / "d_a_elife_asset_report.json").read_text(encoding="utf-8"))
    assert "effect_value" not in written[0]
    assert report["asset_count"] == 2
    assert saved["assets_with_prefix_recovered"] == 2
