"""Export the exact analysis-ready tables for the Ecology Letters Letter archive.

The journal-facing archive contains the units used for inference, metadata,
reproduction code and frozen aggregate outputs. Source species identifiers are
not needed to reproduce the reported analyses and are therefore omitted.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_aubert2026_zenodo_extension import (
    FILES as AUBERT_FILES,
    _download as _download_aubert,
    _read as _read_aubert,
    build_pair_site_rows,
)
from scripts.analyze_sakhalkar2023_network import _find_workbook
from scripts.analyze_sakhalkar2023_trait_routing import build_species_trait_rows
from scripts.audit_sakhalkar2023_zenodo import (
    _download as _download_sakhalkar,
    read_xlsx_sheet_rows,
)

SAKHALKAR_DOI = "10.5281/zenodo.8398202"
AUBERT_EPHI_DOI = "10.5281/zenodo.14185547"


def _write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _sakhalkar_rows() -> list[dict[str, object]]:
    workbook = _find_workbook(_download_sakhalkar())
    visits = read_xlsx_sheet_rows(workbook, "cheater_data")
    traits = read_xlsx_sheet_rows(workbook, "plant_traits")
    rows = build_species_trait_rows(visits, traits)
    out: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        out.append({
            "analysis_unit": f"plant_{index:03d}",
            "route_balance": row["route_balance"],
            "tube_length": row["tube_length"],
            "tube_width": row["tube_width"],
            "brightness": row["brightness"],
            "shape": row["shape"],
        })
    return out


def _aubert_rows() -> list[dict[str, object]]:
    tables = {
        key: _read_aubert(_download_aubert(name))
        for key, name in AUBERT_FILES.items()
    }
    rows, _audit = build_pair_site_rows(
        tables["interactions"],
        tables["cameras"],
        tables["plants"],
        tables["birds"],
    )

    site_map = {
        site: f"site_{index:02d}"
        for index, site in enumerate(sorted({str(row["site"]) for row in rows}), start=1)
    }
    out: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=1):
        out.append({
            "analysis_unit": f"pair_site_{index:04d}",
            "site_id": site_map[str(row["site"])],
            "bird_group": row["bird_group"],
            "n_interactions": row["n_interactions"],
            "robbery_rate": row["robbery_rate"],
            "mismatch_log_t_over_b": row["mismatch_log_t_over_b"],
            "trait_barrier": "true" if bool(row["trait_barrier"]) else "false",
        })
    return out


def export_archive(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)

    sakh = _sakhalkar_rows()
    aubert = _aubert_rows()

    _write_csv(
        output_dir / "sakhalkar_species_analysis.csv",
        sakh,
        [
            "analysis_unit",
            "route_balance",
            "tube_length",
            "tube_width",
            "brightness",
            "shape",
        ],
    )
    _write_csv(
        output_dir / "aubert_ephi_pair_site_analysis.csv",
        aubert,
        [
            "analysis_unit",
            "site_id",
            "bird_group",
            "n_interactions",
            "robbery_rate",
            "mismatch_log_t_over_b",
            "trait_barrier",
        ],
    )

    metadata = [
        {
            "file": "sakhalkar_species_analysis.csv",
            "column": "analysis_unit",
            "description": "Anonymous plant-species analysis unit; source species identifier omitted.",
            "unit": "identifier",
        },
        {
            "file": "sakhalkar_species_analysis.csv",
            "column": "route_balance",
            "description": "(robbing-thieving)/(robbing+thieving) species-level frequency balance.",
            "unit": "unitless",
        },
        {
            "file": "sakhalkar_species_analysis.csv",
            "column": "tube_length",
            "description": "Floral tube length from the source trait table.",
            "unit": "source scale",
        },
        {
            "file": "sakhalkar_species_analysis.csv",
            "column": "tube_width",
            "description": "Floral tube width from the source trait table.",
            "unit": "source scale",
        },
        {
            "file": "sakhalkar_species_analysis.csv",
            "column": "brightness",
            "description": "Source-defined brightness trait; missing in the current cheating-species subset.",
            "unit": "source scale",
        },
        {
            "file": "sakhalkar_species_analysis.csv",
            "column": "shape",
            "description": "Source-defined flower-shape category.",
            "unit": "categorical",
        },
        {
            "file": "aubert_ephi_pair_site_analysis.csv",
            "column": "analysis_unit",
            "description": "Anonymous bird x plant x site inferential unit.",
            "unit": "identifier",
        },
        {
            "file": "aubert_ephi_pair_site_analysis.csv",
            "column": "site_id",
            "description": "Deterministically relabelled site identifier preserving within-site grouping.",
            "unit": "identifier",
        },
        {
            "file": "aubert_ephi_pair_site_analysis.csv",
            "column": "bird_group",
            "description": "Hummingbird or flowerpiercer source grouping.",
            "unit": "categorical",
        },
        {
            "file": "aubert_ephi_pair_site_analysis.csv",
            "column": "n_interactions",
            "description": "Resolved interactions aggregated into the pair-site unit.",
            "unit": "count",
        },
        {
            "file": "aubert_ephi_pair_site_analysis.csv",
            "column": "robbery_rate",
            "description": "Robbing interactions divided by robbing + legitimate interactions.",
            "unit": "proportion",
        },
        {
            "file": "aubert_ephi_pair_site_analysis.csv",
            "column": "mismatch_log_t_over_b",
            "description": "log(flower tube length cm / mean bird culmen length cm).",
            "unit": "log ratio",
        },
        {
            "file": "aubert_ephi_pair_site_analysis.csv",
            "column": "trait_barrier",
            "description": "True when flower tube length exceeds bird bill length.",
            "unit": "boolean",
        },
    ]
    _write_csv(
        output_dir / "metadata.csv",
        metadata,
        ["file", "column", "description", "unit"],
    )

    manifest = {
        "archive_schema": "BITA_ACCESS_ROUTING_LETTER_ARCHIVE_V1",
        "source_data": {
            "sakhalkar_2023_zenodo_doi": SAKHALKAR_DOI,
            "aubert_ephi_zenodo_mirror_doi": AUBERT_EPHI_DOI,
        },
        "analysis_tables": {
            "sakhalkar_species_analysis.csv": len(sakh),
            "aubert_ephi_pair_site_analysis.csv": len(aubert),
        },
        "identifier_policy": (
            "Analysis-unit identifiers are anonymous. EPHI site labels are deterministically "
            "relabelled while preserving within-site permutation groups. Source species identifiers "
            "are not required for reproduction of the reported Letter statistics."
        ),
    }
    (output_dir / "archive_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(export_archive(args.output_dir), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
