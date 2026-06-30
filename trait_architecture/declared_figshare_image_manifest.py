"""Audit declared Figshare image ZIP manifests without reading image pixels.

The audit resolves exact archive names from an article-declared Figshare
accession. It emits aggregate member counts, extensions, and predeclared morph
and timestamp-token coverage only. It never emits image files, pixel data, full
member paths, or visit annotations.
"""

from __future__ import annotations

import json
import re
import zipfile
from collections import Counter
from io import BytesIO
from pathlib import Path
from typing import Any, Callable

from trait_architecture.declared_figshare_receipts import FIGSHARE_API
from trait_architecture.declared_figshare_xlsx_headers import _fetch_bytes
from trait_architecture.public_repository_resolver import _as_url, _fetch_json, _text


MORPH_TOKENS = ("black", "red", "white")
IMAGE_EXTENSIONS = frozenset({".jpg", ".jpeg", ".png", ".tif", ".tiff"})
TIMESTAMP_PATTERN = re.compile(r"(?:19|20)\d{2}[-_]?\d{2}[-_]?\d{2}|\d{2}[-_:]\d{2}[-_:]\d{2}")


def _declared_file(payload: dict[str, Any], file_name: str) -> dict[str, Any]:
    matches = [item for item in payload.get("files", []) if isinstance(item, dict) and _text(item.get("name")) == file_name]
    if len(matches) != 1:
        raise ValueError("declared Figshare archive name is absent or ambiguous")
    return matches[0]


def _member_summary(archive: zipfile.ZipFile) -> dict[str, object]:
    members = [member for member in archive.infolist() if not member.is_dir()]
    extensions: Counter[str] = Counter()
    morph_hits: Counter[str] = Counter()
    timestamp_name_count = 0
    image_count = 0
    for member in members:
        basename = Path(member.filename).name.lower()
        suffix = Path(basename).suffix.lower()
        extensions[suffix or "[no_extension]"] += 1
        if suffix in IMAGE_EXTENSIONS:
            image_count += 1
        for morph in MORPH_TOKENS:
            if morph in basename:
                morph_hits[morph] += 1
        if TIMESTAMP_PATTERN.search(basename):
            timestamp_name_count += 1
    return {
        "member_file_count": len(members),
        "image_file_count": image_count,
        "counts_by_extension": dict(sorted(extensions.items())),
        "filename_morph_token_counts": {morph: morph_hits[morph] for morph in MORPH_TOKENS},
        "filename_timestamp_token_count": timestamp_name_count,
    }


def audit_declared_figshare_image_manifests(
    *,
    figshare_article_id: str,
    archive_names: list[str],
    fetch_json: Callable[[str], tuple[int, Any]] = _fetch_json,
    fetch_bytes: Callable[[str], bytes] = _fetch_bytes,
) -> dict[str, object]:
    """Return aggregate ZIP manifest facts for exact declared pollinator archives."""

    accession = _text(figshare_article_id)
    request_url = FIGSHARE_API + accession
    status, payload = fetch_json(request_url)
    if status >= 400:
        raise RuntimeError(f"HTTP {status}")
    if not isinstance(payload, dict) or _text(payload.get("id")) != accession:
        raise ValueError("Figshare response did not match declared article accession")

    archives = []
    for name in archive_names:
        item = _declared_file(payload, name)
        url = _as_url(item.get("download_url"))
        if not url:
            raise ValueError("declared Figshare archive has no public download URL")
        zip_bytes = fetch_bytes(url)
        summary = _member_summary(zipfile.ZipFile(BytesIO(zip_bytes)))
        archives.append({"archive_name": name, **summary})
    return {
        "figshare_article_id": accession,
        "figshare_dataset_doi": _text(payload.get("doi")),
        "archives": archives,
        "decision_boundary": (
            "This audit emits aggregate ZIP-manifest properties only. It does not emit image paths or pixels, "
            "map frames to floral morphs, establish camera exposure, or count pollinator visits."
        ),
    }


def write_declared_figshare_image_manifest_audit(out_dir: str | Path, report: dict[str, object]) -> None:
    output = Path(out_dir)
    output.mkdir(parents=True, exist_ok=True)
    (output / "declared_figshare_image_manifest_audit.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
