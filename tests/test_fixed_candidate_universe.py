import csv
import hashlib
import io
import zipfile

import trait_architecture.fixed_candidate_universe as snapshot


def make_artifact(rows: list[dict[str, str]]) -> bytes:
    buffer = io.BytesIO()
    fields = sorted(snapshot.REQUIRED_COLUMNS)
    text = io.StringIO()
    writer = csv.DictWriter(text, fieldnames=fields)
    writer.writeheader()
    writer.writerows(rows)
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr(snapshot.SOURCE_MEMBER, text.getvalue())
    return buffer.getvalue()


def test_fixed_snapshot_rejects_changed_artifact_checksum(monkeypatch) -> None:
    payload = make_artifact([{field: "x" for field in snapshot.REQUIRED_COLUMNS}])
    monkeypatch.setattr(snapshot, "EXPECTED_CANDIDATE_COUNT", 1)
    monkeypatch.setattr(snapshot, "SOURCE_ARTIFACT_SHA256", "0" * 64)

    try:
        snapshot.load_fixed_candidate_universe(download=lambda _url, _token: payload)
    except ValueError as error:
        assert "checksum mismatch" in str(error)
    else:
        raise AssertionError("checksum mismatch should reject a changed artifact")


def test_fixed_snapshot_recovers_validated_candidate_rows(monkeypatch) -> None:
    row = {field: "" for field in snapshot.REQUIRED_COLUMNS}
    row.update({
        "candidate_id": "openalex:W1",
        "title": "Example",
        "doi": "https://doi.org/10.1/example",
        "metadata_match_score": "4",
    })
    payload = make_artifact([row, {**row, "candidate_id": "openalex:W2"}])
    monkeypatch.setattr(snapshot, "EXPECTED_CANDIDATE_COUNT", 2)
    monkeypatch.setattr(snapshot, "SOURCE_ARTIFACT_SHA256", hashlib.sha256(payload).hexdigest())

    rows, receipt = snapshot.load_fixed_candidate_universe(download=lambda _url, _token: payload)

    assert [item["candidate_id"] for item in rows] == ["openalex:W1", "openalex:W2"]
    assert receipt.candidate_count == 2
    assert receipt.artifact_sha256 == hashlib.sha256(payload).hexdigest()
