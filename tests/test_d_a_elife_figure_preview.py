from __future__ import annotations

import csv
import io
import json

from PIL import Image

from trait_architecture.d_a_elife_figure_preview import read_assets, render_previews, write_manifest


def _asset(label: str = "Figure 1.") -> dict[str, str]:
    return {
        "candidate_id": "dA_cand_schiestl2015",
        "doi": "10.7554/eLife.07641",
        "figure_label": label,
        "asset_kind": "figure_graphic",
        "asset_url": f"https://cdn.example/{label.replace(' ', '_')}.tif",
        "access_status": "asset_prefix_recovered",
    }


def _tiff_bytes() -> bytes:
    image = Image.new("RGB", (80, 40), "white")
    output = io.BytesIO()
    image.save(output, format="TIFF")
    return output.getvalue()


def test_render_previews_converts_primary_tiff_without_digitization(tmp_path) -> None:
    rows = render_previews([_asset("Figure 1."), _asset("Figure 2.")], tmp_path, download=lambda _url: _tiff_bytes())

    assert len(rows) == 2
    assert all(row.preview_status == "preview_rendered" for row in rows)
    assert all((tmp_path / row.preview_filename).exists() for row in rows)
    assert all("Do not infer" in row.do_not_infer for row in rows)


def test_read_assets_excludes_supplements_and_unavailable_images(tmp_path) -> None:
    path = tmp_path / "assets.csv"
    valid = _asset()
    excluded = [
        _asset("Figure 2—figure supplement 1."),
        {**_asset(), "asset_kind": "figure_media"},
        {**_asset(), "access_status": "asset_http_error"},
    ]
    fields = list(valid)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([valid, *excluded])
    assert read_assets(path) == [valid]


def test_write_manifest_has_no_effect_field(tmp_path) -> None:
    rows = render_previews([_asset()], tmp_path, download=lambda _url: _tiff_bytes())
    report = write_manifest(tmp_path, rows)
    with (tmp_path / "d_a_elife_figure_preview_manifest.csv").open(encoding="utf-8", newline="") as handle:
        written = list(csv.DictReader(handle))
    saved = json.loads((tmp_path / "d_a_elife_figure_preview_report.json").read_text(encoding="utf-8"))
    assert "effect_value" not in written[0]
    assert report["previews_rendered"] == 1
    assert saved["primary_figure_count"] == 1
