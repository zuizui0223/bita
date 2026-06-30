"""Load the fixed M0 candidate universe produced by PR #20.

The candidate universe must not be silently regenerated from a live search API:
search rankings and metadata can change. This module retrieves the archived
GitHub Actions artifact from the successful PR #20 workflow, verifies the ZIP
SHA-256 published by GitHub, and extracts only the bibliographic candidate CSV.

The artifact contains article metadata, not raw biological observations. It is a
fixed discovery universe for shallow public-route auditing; it never promotes a
candidate beyond M0.
"""

from __future__ import annotations

import csv
import hashlib
import io
import os
import zipfile
from dataclasses import dataclass
from typing import Callable
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


REPOSITORY = "zuizui0223/biotic-interaction-trait-architecture"
SOURCE_PR = 20
SOURCE_WORKFLOW_RUN = 28356795187
SOURCE_ARTIFACT_ID = 7945611222
SOURCE_ARTIFACT_SHA256 = "99c45e769eadb5768291d8762acdd34c6046e493640667f0c0a521b6cb7f5f23"
SOURCE_MEMBER = "openalex_matched_flower_all_candidates.csv"
EXPECTED_CANDIDATE_COUNT = 258
USER_AGENT = "biotic-interaction-trait-architecture fixed-candidate-universe/0.1"
REQUIRED_COLUMNS = frozenset({
    "candidate_id", "title", "doi", "open_access_url", "is_open_access",
    "metadata_match_score", "metadata_attraction_signal", "metadata_barrier_signal",
    "metadata_pollination_signal", "metadata_antagonist_signal",
})


@dataclass(frozen=True)
class CandidateSnapshotReceipt:
    source_pr: int
    source_workflow_run: int
    source_artifact_id: int
    source_member: str
    artifact_sha256: str
    candidate_count: int


class _StripAuthorizationOnCrossHostRedirect(HTTPRedirectHandler):
    """Keep the GitHub token on api.github.com, never on signed storage URLs."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        redirected = super().redirect_request(req, fp, code, msg, headers, newurl)
        if redirected and urlparse(req.full_url).netloc != urlparse(newurl).netloc:
            redirected.remove_header("Authorization")
            redirected.remove_header("authorization")
        return redirected


def _artifact_url() -> str:
    return f"https://api.github.com/repos/{REPOSITORY}/actions/artifacts/{SOURCE_ARTIFACT_ID}/zip"


def _download(url: str, token: str, *, timeout: int = 90) -> bytes:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": USER_AGENT,
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    opener = build_opener(_StripAuthorizationOnCrossHostRedirect())
    with opener.open(request, timeout=timeout) as response:  # nosec B310: fixed GitHub artifact endpoint
        return response.read()


def load_fixed_candidate_universe(
    *,
    token: str | None = None,
    download: Callable[[str, str], bytes] = _download,
) -> tuple[list[dict[str, str]], CandidateSnapshotReceipt]:
    """Return the validated 258-row candidate snapshot and its provenance receipt."""

    archive_bytes = download(_artifact_url(), token if token is not None else os.environ.get("GITHUB_TOKEN", ""))
    actual_sha256 = hashlib.sha256(archive_bytes).hexdigest()
    if actual_sha256 != SOURCE_ARTIFACT_SHA256:
        raise ValueError(
            "fixed candidate artifact checksum mismatch: "
            f"expected {SOURCE_ARTIFACT_SHA256}, got {actual_sha256}"
        )
    archive = zipfile.ZipFile(io.BytesIO(archive_bytes))
    if SOURCE_MEMBER not in archive.namelist():
        raise ValueError(f"fixed candidate artifact lacks {SOURCE_MEMBER}")
    content = archive.read(SOURCE_MEMBER).decode("utf-8-sig")
    rows = [{key: str(value or "").strip() for key, value in row.items()} for row in csv.DictReader(io.StringIO(content))]
    if not rows:
        raise ValueError("fixed candidate artifact has no candidate rows")
    missing = sorted(REQUIRED_COLUMNS.difference(rows[0]))
    if missing:
        raise ValueError(f"fixed candidate CSV lacks columns: {', '.join(missing)}")
    if len(rows) != EXPECTED_CANDIDATE_COUNT:
        raise ValueError(f"expected {EXPECTED_CANDIDATE_COUNT} candidates, recovered {len(rows)}")
    ids = [row["candidate_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("fixed candidate artifact has duplicate candidate IDs")
    return rows, CandidateSnapshotReceipt(
        source_pr=SOURCE_PR,
        source_workflow_run=SOURCE_WORKFLOW_RUN,
        source_artifact_id=SOURCE_ARTIFACT_ID,
        source_member=SOURCE_MEMBER,
        artifact_sha256=actual_sha256,
        candidate_count=len(rows),
    )