"""Resolve metadata and file manifest for the Caruso-linked Dryad dataset.

The prior C3-I probe found a DataCite Dataset record explicitly related to Caruso
2019. This stage checks whether the public Dryad record exposes a file manifest and
whether filenames/mime types suggest a *primary-study bibliographic index*. It never
downloads file contents, reads database rows, or imports selection gradients or
primary-study effects.
"""

from __future__ import annotations

import csv
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Iterable
from urllib.error import HTTPError
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen


CARUSO_SOURCE_DOI = "10.1111/evo.13639"
DRYAD_DATASET_DOI = "10.5061/dryad.2v8c5g0"
DATACITE_DOI = "https://api.datacite.org/dois/"
# Dryad treats the DOI identifier as one API path component, so both the colon and
# slash must be percent-encoded. The two variants cover API deployments that expect
# either `doi:<id>` or bare `<id>` as the resource identifier.
DRYAD_DATASET_ENDPOINTS = (
    "https://datadryad.org/api/v2/datasets/" + quote(f"doi:{DRYAD_DATASET_DOI}", safe=""),
    "https://datadryad.org/api/v2/datasets/" + quote(DRYAD_DATASET_DOI, safe=""),
)
USER_AGENT = "biotic-interaction-trait-architecture d-a-caruso-dryad-manifest/0.1"
INDEX_NAME_TERMS = ("study", "studies", "reference", "citation", "bibliograph", "database", "metadata")
TABULAR_EXTENSIONS = (".csv", ".tsv", ".txt", ".xlsx", ".xls", ".ods")
MANIFEST_FIELDS = (
    "source_doi", "dataset_doi", "probe_source", "http_status", "access_status",
    "file_identifier", "filename", "mime_type", "size_bytes", "file_url",
    "primary_study_index_candidate", "discovery_basis", "notes", "do_not_infer",
)
DO_NOT_INFER = (
    "Dataset metadata and file-manifest receipt only. Do not infer file contents, primary-study identifiers, "
    "trait-to-antagonism routes, selection gradients, effect values, denominators, uncertainty, or B2 eligibility."
)


@dataclass(frozen=True)
class DryadManifestReceipt:
    source_doi: str
    dataset_doi: str
    probe_source: str
    http_status: str
    access_status: str
    file_identifier: str
    filename: str
    mime_type: str
    size_bytes: str
    file_url: str
    primary_study_index_candidate: str
    discovery_basis: str
    notes: str
    do_not_infer: str = DO_NOT_INFER


class PublicJSONClient:
    def __init__(self, *, min_interval_seconds: float = 0.25):
        self.min_interval_seconds = min_interval_seconds
        self._next_allowed = 0.0

    def json(self, url: str) -> tuple[int, Any]:
        wait = self._next_allowed - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        self._next_allowed = time.monotonic() + self.min_interval_seconds
        request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
        try:
            with urlopen(request, timeout=60) as response:  # nosec B310: fixed public metadata endpoints
                status = int(getattr(response, "status", response.getcode()))
                return status, json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            return int(error.code), None
        except (UnicodeDecodeError, json.JSONDecodeError):
            return 0, None


def _text(value: object) -> str:
    return str(value or "").strip()


def _receipt(
    source: str,
    status: int | str,
    access_status: str,
    *,
    file_identifier: str = "",
    filename: str = "",
    mime_type: str = "",
    size_bytes: str = "",
    file_url: str = "",
    index_candidate: str = "false",
    discovery_basis: str = "",
    notes: str = "",
) -> DryadManifestReceipt:
    return DryadManifestReceipt(
        source_doi=CARUSO_SOURCE_DOI,
        dataset_doi=DRYAD_DATASET_DOI,
        probe_source=source,
        http_status=str(status),
        access_status=access_status,
        file_identifier=file_identifier,
        filename=filename,
        mime_type=mime_type,
        size_bytes=size_bytes,
        file_url=file_url,
        primary_study_index_candidate=index_candidate,
        discovery_basis=discovery_basis,
        notes=notes,
    )


def _resource(payload: Any) -> dict[str, Any]:
    """Unwrap JSON:API-style `data` envelopes without assuming one provider format."""

    if not isinstance(payload, dict):
        return {}
    data = payload.get("data")
    return data if isinstance(data, dict) else payload


def _absolute(url: str, base_url: str) -> str:
    return urljoin(base_url, url) if url else ""


def _links(value: Any, *, base_url: str = "") -> dict[str, str]:
    resource = _resource(value)
    links = resource.get("_links")
    if not isinstance(links, dict):
        return {}
    output: dict[str, str] = {}
    for key, item in links.items():
        if isinstance(item, dict):
            href = _text(item.get("href"))
        elif isinstance(item, str):
            href = item.strip()
        else:
            href = ""
        if href:
            output[_text(key)] = _absolute(href, base_url)
    return output


def _embedded_entries(value: Any, term: str) -> list[dict[str, Any]]:
    resource = _resource(value)
    embedded = resource.get("_embedded")
    if not isinstance(embedded, dict):
        return []
    output: list[dict[str, Any]] = []
    for key, item in embedded.items():
        if term not in _text(key).casefold() or not isinstance(item, list):
            continue
        output.extend(entry for entry in item if isinstance(entry, dict))
    return output


def _extract_files(payload: Any) -> list[dict[str, Any]]:
    """Return likely HATEOAS file dictionaries, tolerating Dryad API key variants."""

    return _embedded_entries(payload, "file")


def _filename(row: dict[str, Any]) -> str:
    for key in ("path", "filename", "name", "fileName"):
        value = _text(row.get(key))
        if value:
            return value
    return ""


def _mime(row: dict[str, Any]) -> str:
    for key in ("mimeType", "mime_type", "contentType"):
        value = _text(row.get(key))
        if value:
            return value
    return ""


def _size(row: dict[str, Any]) -> str:
    for key in ("size", "sizeBytes", "byteSize"):
        value = _text(row.get(key))
        if value:
            return value
    return ""


def _identifier(row: dict[str, Any]) -> str:
    return _text(row.get("id") or row.get("fileId") or row.get("uuid"))


def _file_url(row: dict[str, Any], *, base_url: str) -> str:
    links = _links(row, base_url=base_url)
    for key in ("stash:download", "download", "self"):
        if key in links:
            return links[key]
    return ""


def _index_candidate(filename: str, mime_type: str) -> bool:
    folded_name = filename.casefold()
    tabular = folded_name.endswith(TABULAR_EXTENSIONS) or "spreadsheet" in mime_type.casefold() or "csv" in mime_type.casefold()
    return tabular and any(term in folded_name for term in INDEX_NAME_TERMS)


def _first_link(links: dict[str, str], *terms: str) -> str:
    for key, url in links.items():
        if any(term in key.casefold() for term in terms):
            return url
    return ""


def _files_from_version_payload(version_payload: Any, *, version_url: str) -> str:
    """Find a files link from a version resource or its version collection entries."""

    files = _first_link(_links(version_payload, base_url=version_url), "file")
    if files:
        return files
    for entry in _embedded_entries(version_payload, "version"):
        files = _first_link(_links(entry, base_url=version_url), "file")
        if files:
            return files
    return ""


def _dryad_file_endpoint(
    dataset_payload: Any,
    *,
    dataset_url: str,
    dataset_status: int,
    fetch_json: Callable[[str], tuple[int, Any]],
    output: list[DryadManifestReceipt],
) -> tuple[int, str]:
    """Resolve a direct files link or the normal dataset -> version -> files chain."""

    links = _links(dataset_payload, base_url=dataset_url)
    direct = _first_link(links, "file")
    if direct:
        return dataset_status, direct
    version_url = _first_link(links, "version")
    if not version_url:
        return dataset_status, ""
    try:
        status, version_payload = fetch_json(version_url)
    except Exception as error:
        output.append(_receipt("dryad_version", "", "request_failed", notes=f"{type(error).__name__}: {error}"))
        return dataset_status, ""
    if status >= 400 or not isinstance(version_payload, dict):
        output.append(_receipt("dryad_version", status, "version_metadata_unavailable", notes=version_url))
        return status, ""
    output.append(_receipt("dryad_version", status, "version_metadata_recovered", discovery_basis="dryad_hateoas_version", notes=version_url))
    return status, _files_from_version_payload(version_payload, version_url=version_url)


def probe_dryad_manifest(
    *,
    fetch_json: Callable[[str], tuple[int, Any]],
) -> list[DryadManifestReceipt]:
    """Probe DataCite relationship then Dryad metadata and files HATEOAS routes."""

    output: list[DryadManifestReceipt] = []
    datacite_url = DATACITE_DOI + quote(DRYAD_DATASET_DOI, safe="")
    try:
        status, payload = fetch_json(datacite_url)
    except Exception as error:
        output.append(_receipt("datacite_dataset", "", "request_failed", notes=f"{type(error).__name__}: {error}"))
    else:
        if status >= 400 or not isinstance(payload, dict):
            output.append(_receipt("datacite_dataset", status, "metadata_unavailable"))
        else:
            attrs = payload.get("data", {}).get("attributes", {}) if isinstance(payload.get("data"), dict) else {}
            relations = attrs.get("relatedIdentifiers") if isinstance(attrs, dict) else []
            linked = any(
                isinstance(item, dict)
                and _text(item.get("relatedIdentifier")).casefold().replace("https://doi.org/", "") == CARUSO_SOURCE_DOI
                for item in (relations if isinstance(relations, list) else [])
            )
            output.append(_receipt(
                "datacite_dataset", status,
                "dataset_metadata_related_to_source_doi" if linked else "dataset_metadata_relation_not_confirmed",
                discovery_basis="datacite_related_identifier" if linked else "datacite_metadata",
                notes="DataCite relationship check only.",
            ))

    dataset_payload: Any = None
    dataset_status = 0
    dataset_url = ""
    for endpoint in DRYAD_DATASET_ENDPOINTS:
        try:
            status, payload = fetch_json(endpoint)
        except Exception as error:
            output.append(_receipt("dryad_dataset", "", "request_failed", notes=f"{type(error).__name__}: {error}"))
            continue
        if status < 400 and isinstance(payload, dict):
            dataset_payload, dataset_status, dataset_url = payload, status, endpoint
            output.append(_receipt("dryad_dataset", status, "dataset_metadata_recovered", discovery_basis="dryad_dataset_endpoint", notes=endpoint))
            break
        output.append(_receipt("dryad_dataset", status, "dataset_endpoint_unavailable", notes=endpoint))
    if dataset_payload is None:
        return output

    file_status, file_endpoint = _dryad_file_endpoint(
        dataset_payload,
        dataset_url=dataset_url,
        dataset_status=dataset_status,
        fetch_json=fetch_json,
        output=output,
    )
    if not file_endpoint:
        output.append(_receipt("dryad_files", file_status, "file_manifest_link_not_found", notes=dataset_url))
        return output

    try:
        status, file_payload = fetch_json(file_endpoint)
    except Exception as error:
        output.append(_receipt("dryad_files", "", "request_failed", notes=f"{type(error).__name__}: {error}"))
        return output
    files = _extract_files(file_payload)
    if status >= 400 or not files:
        output.append(_receipt("dryad_files", status, "file_manifest_unavailable", notes=file_endpoint))
        return output
    output.append(_receipt("dryad_files", status, "file_manifest_recovered", discovery_basis="dryad_hateoas_files", notes=file_endpoint))
    for row in files:
        filename, mime_type = _filename(row), _mime(row)
        candidate = _index_candidate(filename, mime_type)
        output.append(_receipt(
            "dryad_files", status, "file_manifest_entry",
            file_identifier=_identifier(row),
            filename=filename,
            mime_type=mime_type,
            size_bytes=_size(row),
            file_url=_file_url(row, base_url=file_endpoint),
            index_candidate="true" if candidate else "false",
            discovery_basis="filename_and_mime_manifest_screen",
            notes="File metadata only; contents not downloaded.",
        ))
    return output


def summarise(receipts: Iterable[DryadManifestReceipt]) -> dict[str, object]:
    rows = list(receipts)
    files = [row for row in rows if row.access_status == "file_manifest_entry"]
    candidates = [row for row in files if row.primary_study_index_candidate == "true"]
    return {
        "source_doi": CARUSO_SOURCE_DOI,
        "dataset_doi": DRYAD_DATASET_DOI,
        "manifest_file_count": len(files),
        "primary_study_index_file_candidate_count": len(candidates),
        "next_action": (
            "inspect_capped_candidate_file_schema"
            if candidates else "stop_before_file_download_no_bibliographic_index_filename_candidate"
        ),
        "decision_boundary": DO_NOT_INFER,
    }


def write_outputs(out_dir: str | Path, receipts: Iterable[DryadManifestReceipt]) -> dict[str, object]:
    rows = list(receipts)
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "d_a_caruso_dryad_manifest.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    report = summarise(rows)
    (destination / "d_a_caruso_dryad_manifest_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    return report
