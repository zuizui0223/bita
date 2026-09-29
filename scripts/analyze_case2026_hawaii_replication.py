"""Post-publication independent-network replication using Case et al. (2026).

This lane is deliberately NOT confirmatory: the Case paper and Dryad metadata
already disclose the direction of the bill-flower / nectar-robbing relationship.
The analysis therefore asks a narrower question: does this independently sampled
Hawaiian bird-flower network satisfy the pre-existing data-quality gates needed to
contribute a third network-level rank association on the same access-routing scale?

No gate is relaxed to admit this dataset. The original third-fauna preregistration
still excludes Aves; this module reports a separate POST_PUBLICATION_REPLICATION
status and may only be used to describe k=3 independent-network recurrence, not a
three-fauna confirmatory test.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import math
import random
import tempfile
import urllib.request
import zipfile
from collections import defaultdict
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.analyze_joint_access_routing import combine_rhos_equal_network
from scripts.analyze_joint_access_routing_species_robust import (
    build_existing_network_species_inputs,
)
from scripts.analyze_sakhalkar2023_network import _pearson, _rankdata

CASE_DOI = "10.5061/dryad.sj3tx96kr"
DRYAD_BASE = "https://datadryad.org"
CASE_DATASET_API_URL = (
    DRYAD_BASE
    + "/api/v2/datasets/doi%3A10.5061%2Fdryad.sj3tx96kr"
)
CASE_MEMBER = "Case_FE_2026_Analysis_2.csv"
SEED = 20260929

MIN_UNITS = 30
MIN_VISITOR_SPECIES = 5
MIN_PLANT_SPECIES = 5


def _mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean requires data")
    return sum(values) / len(values)


def _as_float(value: object) -> float | None:
    try:
        out = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def _url_json(url: str) -> dict[str, object]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "BITA-public-replication/1.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def _absolute_dryad_url(href: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return DRYAD_BASE + href


def discover_case_public_file_url() -> tuple[str, dict[str, object]]:
    """Resolve the current public Case CSV without authenticated download API.

    Dryad's dataset-level /download endpoint requires an API token, but public
    version/file metadata are readable and expose file IDs. Public files can then
    be retrieved through the landing-page file_stream endpoint.
    """
    dataset = _url_json(CASE_DATASET_API_URL)
    links = dataset.get("_links", {})
    if not isinstance(links, dict):
        raise ValueError("Dryad dataset metadata lacks _links")
    version_link = links.get("stash:version", {})
    if not isinstance(version_link, dict) or not version_link.get("href"):
        raise ValueError("Dryad dataset metadata lacks stash:version href")
    version = _url_json(_absolute_dryad_url(str(version_link["href"])))
    version_links = version.get("_links", {})
    files_href = None
    if isinstance(version_links, dict):
        files_link = version_links.get("stash:files", {})
        if isinstance(files_link, dict):
            files_href = files_link.get("href")
    if not files_href:
        version_id = version.get("id")
        if version_id is None:
            raise ValueError("Dryad version metadata lacks files link and id")
        files_href = f"/api/v2/versions/{version_id}/files"

    files_payload = _url_json(_absolute_dryad_url(str(files_href)))
    embedded = files_payload.get("_embedded", {})
    entries = embedded.get("stash:files", []) if isinstance(embedded, dict) else []
    matches = [
        entry
        for entry in entries
        if isinstance(entry, dict) and str(entry.get("path", "")) == CASE_MEMBER
    ]
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one public {CASE_MEMBER}, found {len(matches)}"
        )
    entry = matches[0]
    entry_links = entry.get("_links", {})
    self_href = None
    if isinstance(entry_links, dict):
        self_link = entry_links.get("self", {})
        if isinstance(self_link, dict):
            self_href = self_link.get("href")
    if not self_href:
        raise ValueError("Dryad file metadata lacks self href")
    match = __import__("re").search(r"/api/v2/files/(\\d+)$", str(self_href))
    if match is None:
        raise ValueError(f"cannot recover Dryad file id from {self_href}")
    file_id = match.group(1)
    return (
        f"{DRYAD_BASE}/stash/downloads/file_stream/{file_id}",
        {
            "dryad_version_id": version.get("id"),
            "dryad_file_id": int(file_id),
            "dryad_file_size": entry.get("size"),
            "dryad_digest": entry.get("digest"),
            "dryad_digest_type": entry.get("digestType"),
        },
    )


def download_case_file(path: str | Path) -> tuple[Path, dict[str, object]]:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    url, provenance = discover_case_public_file_url()
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "BITA-public-replication/1.0"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        target.write_bytes(response.read())
    if target.stat().st_size == 0:
        raise ValueError("downloaded Case CSV is empty")
    provenance["public_file_stream_url"] = url
    return target, provenance


def read_case_rows(source: str | Path) -> list[dict[str, str]]:
    path = Path(source)
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            members = [name for name in zf.namelist() if name.endswith(CASE_MEMBER)]
            if len(members) != 1:
                raise ValueError(
                    f"expected exactly one {CASE_MEMBER}, found {len(members)}"
                )
            text = zf.read(members[0]).decode("utf-8-sig")
    else:
        text = path.read_text(encoding="utf-8-sig")
    return list(csv.DictReader(io.StringIO(text)))


