"""Probe the live Web of Life endpoints for backbone eligibility.

This is a source-contract test, not an ecological analysis. It writes a small
JSON audit and a CSV preview of normalised edge metadata. A pass means only
that the data source is technically and structurally usable enough for the
next test (plant-side orientation and trait joins); it does not mean that the
source has been adopted as the empirical backbone.

Usage:
    python scripts/probe_web_of_life.py out_dir
"""

from __future__ import annotations

import csv
import io
import json
import sys
from collections import Counter
from pathlib import Path
from urllib.request import Request, urlopen

METADATA_URL = "https://www.web-of-life.es/get_network_info.php"
EDGES_URL = "https://www.web-of-life.es/get_networks.php"
USER_AGENT = "biotic-interaction-trait-architecture source probe/0.1"


def fetch(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:  # nosec B310: fixed public source endpoint
        return response.read()


def nonempty(row: dict[str, object], field: str) -> bool:
    return bool(str(row.get(field, "")).strip())


def main(out_dir: str) -> int:
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)

    metadata_bytes = fetch(METADATA_URL)
    edge_bytes = fetch(EDGES_URL)
    metadata = list(csv.DictReader(io.StringIO(metadata_bytes.decode("utf-8-sig"))))
    edges = json.loads(edge_bytes.decode("utf-8-sig"))
    if not metadata:
        raise RuntimeError("Web of Life returned empty network metadata")
    if not isinstance(edges, list) or not edges:
        raise RuntimeError("Web of Life returned no edge records")

    metadata_columns = sorted(metadata[0])
    edge_columns = sorted(edges[0])
    required_metadata = {"network_name", "network_type", "latitude", "longitude"}
    required_edges = {"network_name", "species1", "species2", "connection_strength"}
    missing_metadata = sorted(required_metadata - set(metadata_columns))
    missing_edges = sorted(required_edges - set(edge_columns))
    metadata_by_name = {str(row.get("network_name", "")).strip(): row for row in metadata}
    matched_edges = [row for row in edges if str(row.get("network_name", "")).strip() in metadata_by_name]
    unmatched_edges = len(edges) - len(matched_edges)
    type_counts = Counter(str(row.get("network_type", "")).strip() for row in metadata)
    mapped_type_counts = {
        "pollination": type_counts.get("Pollination", 0),
        "herbivory": type_counts.get("Plant-Herbivore", 0),
    }
    coordinate_complete = sum(nonempty(row, "latitude") and nonempty(row, "longitude") for row in metadata)
    weighted_edges = sum(nonempty(row, "connection_strength") for row in edges)
    named_taxa = {str(row.get("species1", "")).strip() for row in edges} | {str(row.get("species2", "")).strip() for row in edges}
    named_taxa.discard("")

    # Web of Life's all-network feed does not label plant versus animal for each
    # side. That must be recovered per network before trait joins; record this as
    # a blocking schema gap rather than silently guessing orientation.
    report = {
        "source": "Web of Life",
        "endpoints": {"metadata": METADATA_URL, "edges": EDGES_URL},
        "metadata_rows": len(metadata),
        "edge_rows": len(edges),
        "metadata_columns": metadata_columns,
        "edge_columns": edge_columns,
        "missing_required_metadata_columns": missing_metadata,
        "missing_required_edge_columns": missing_edges,
        "edge_to_metadata_match_rate": len(matched_edges) / len(edges),
        "unmatched_edge_rows": unmatched_edges,
        "network_type_counts": dict(sorted(type_counts.items())),
        "mapped_candidate_layers": mapped_type_counts,
        "coordinate_complete_networks": coordinate_complete,
        "coordinate_complete_rate": coordinate_complete / len(metadata),
        "weighted_edge_rows": weighted_edges,
        "weighted_edge_rate": weighted_edges / len(edges),
        "unique_named_taxa_across_both_sides": len(named_taxa),
        "plant_animal_side_is_explicit": False,
        "decision": "advance_to_orientation_and_trait_join_test"
        if not missing_metadata and not missing_edges and len(matched_edges) == len(edges)
        else "reject_or_repair_source_adapter",
        "blocking_next_test": "Recover plant-vs-animal orientation per bipartite network before any plant-trait join.",
    }
    (output / "web_of_life_source_probe.json").write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")

    preview_fields = ["network_name", "network_type", "latitude", "longitude", "species1", "species2", "connection_strength"]
    with (output / "web_of_life_edge_preview.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=preview_fields)
        writer.writeheader()
        for edge in matched_edges[:100]:
            meta = metadata_by_name[str(edge["network_name"]).strip()]
            writer.writerow({
                "network_name": edge.get("network_name", ""),
                "network_type": meta.get("network_type", ""),
                "latitude": meta.get("latitude", ""),
                "longitude": meta.get("longitude", ""),
                "species1": edge.get("species1", ""),
                "species2": edge.get("species2", ""),
                "connection_strength": edge.get("connection_strength", ""),
            })
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python scripts/probe_web_of_life.py out_dir")
    raise SystemExit(main(sys.argv[1]))
