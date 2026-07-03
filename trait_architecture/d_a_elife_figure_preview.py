"""Create temporary research previews for the two primary eLife d_A figures.

This consumes exact figure-graphic asset receipts from the fixed Schiestl source.
It downloads only Figure 1 and Figure 2 TIFFs, converts them to PNG previews, and
writes a manifest. The previews are for internal C4 visual reading only: they do
not extract values, digitize axes, classify treatments, or establish an effect.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable
from urllib.request import Request, urlopen


MAX_IMAGE_BYTES = 30 * 1024 * 1024
USER_AGENT = "bita d-a-elife-figure-preview/0.1"
PRIMARY_FIGURES = {"Figure 1.", "Figure 2."}
MANIFEST_FIELDS = (
    "candidate_id", "doi", "figure_label", "asset_url", "preview_filename", "source_bytes",
    "preview_status", "preview_width", "preview_height", "do_not_infer",
)
DO_NOT_INFER = (
    "Preview image only. Do not infer treatment coding, outcome definition, numerical values, "
    "uncertainty, or B2 eligibility without reading the source figure and methods context."
)


@dataclass(frozen=True)
class FigurePreview:
    candidate_id: str
    doi: str
    figure_label: str
    asset_url: str
    preview_filename: str
    source_bytes: str
    preview_status: str
    preview_width: str
    preview_height: str
    do_not_infer: str = DO_NOT_INFER


def _text(value: object) -> str:
    return str(value or "").strip()


def read_assets(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = [{key: _text(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    return [
        row for row in rows
        if row.get("asset_kind") == "figure_graphic"
        and row.get("access_status") == "asset_prefix_recovered"
        and row.get("figure_label") in PRIMARY_FIGURES
    ]


def _download(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "image/tiff,image/*,*/*"})
    with urlopen(request, timeout=90) as response:  # nosec B310: exact public eLife figure receipt
        payload = response.read(MAX_IMAGE_BYTES + 1)
    if len(payload) > MAX_IMAGE_BYTES:
        raise ValueError(f"image exceeds {MAX_IMAGE_BYTES} byte cap")
    return payload


def render_previews(
    assets: Iterable[dict[str, str]],
    out_dir: str | Path,
    *,
    download: Callable[[str], bytes] = _download,
) -> list[FigurePreview]:
    try:
        from PIL import Image
    except ImportError as error:  # pragma: no cover - workflow installs pillow
        raise RuntimeError("Pillow is required for figure previews") from error
    import io

    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    output: list[FigurePreview] = []
    for asset in assets:
        label = asset["figure_label"]
        filename = f"{asset['candidate_id']}_{label.replace(' ', '_').replace('.', '').lower()}.png"
        try:
            payload = download(asset["asset_url"])
            with Image.open(io.BytesIO(payload)) as image:
                image.seek(0)
                image = image.convert("RGB")
                image.thumbnail((2400, 2400))
                width, height = image.size
                image.save(destination / filename, format="PNG", optimize=True)
            output.append(FigurePreview(
                candidate_id=asset["candidate_id"], doi=asset["doi"], figure_label=label,
                asset_url=asset["asset_url"], preview_filename=filename, source_bytes=str(len(payload)),
                preview_status="preview_rendered", preview_width=str(width), preview_height=str(height),
            ))
        except Exception as error:
            output.append(FigurePreview(
                candidate_id=asset["candidate_id"], doi=asset["doi"], figure_label=label,
                asset_url=asset["asset_url"], preview_filename="", source_bytes="",
                preview_status=f"preview_failed:{type(error).__name__}", preview_width="", preview_height="",
            ))
    return output


def write_manifest(out_dir: str | Path, rows: Iterable[FigurePreview]) -> dict[str, object]:
    rows = list(rows)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_elife_figure_preview_manifest.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = {
        "primary_figure_count": len(rows),
        "previews_rendered": sum(row.preview_status == "preview_rendered" for row in rows),
        "decision_boundary": DO_NOT_INFER,
    }
    (destination / "d_a_elife_figure_preview_report.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report
