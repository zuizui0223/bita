import io
import zipfile

from trait_architecture.dryad_archive_schema import inspect_archive_receipt
from trait_architecture.title_validated_dryad_manifest import DryadManifestReceipt


def receipt() -> DryadManifestReceipt:
    return DryadManifestReceipt(
        target_id="TV001", queue_id="Q001", study_id="Example", study_doi="10.1002/example",
        dataset_doi="10.5061/dryad.example", expected_dataset_title="Data from: Example",
        observed_dataset_title="Data from: Example", title_match="yes", manifest_status="manifest_recovered",
        datacite_request_url="https://api.datacite.org/dois/10.5061/dryad.example",
        dryad_request_url="https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.example;https://datadryad.org/api/v2/versions/4805;https://datadryad.org/api/v2/versions/4805/files",
        landing_page_url="https://datadryad.org/dataset/doi:10.5061/dryad.example",
        file_name="traits.csv", file_url="https://datadryad.org/api/v2/files/1/download", notes="fixture",
    )


def zip_bytes() -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        archive.writestr("Raw_Flower_Size.csv", "Plant_ID,Treatment,Flower_Size\nP1,C,4.2\n")
        archive.writestr("README.txt", "metadata")
    return buffer.getvalue()


def test_version_archive_header_screen_does_not_retain_raw_rows() -> None:
    rows = inspect_archive_receipt(receipt(), download_archive=lambda _url, _landing: zip_bytes())

    assert len(rows) == 1
    assert rows[0].schema_status == "header_recovered"
    assert rows[0].file_name == "Raw_Flower_Size.csv"
    assert rows[0].column_names == "Plant_ID;Treatment;Flower_Size"
    assert "P1" not in rows[0].column_names
    assert rows[0].version_archive_url == "https://datadryad.org/api/v2/versions/4805/download"


def test_archive_access_failure_remains_explicit() -> None:
    rows = inspect_archive_receipt(
        receipt(),
        download_archive=lambda _url, _landing: (_ for _ in ()).throw(TimeoutError("archive unavailable")),
    )

    assert rows[0].schema_status == "archive_access_failed"
    assert "TimeoutError" in rows[0].notes
