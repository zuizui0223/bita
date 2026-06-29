from trait_architecture.title_validated_dryad_manifest import probe_targets


def target() -> dict[str, str]:
    return {
        "target_id": "TV001",
        "queue_id": "Q001",
        "study_id": "Example_study",
        "study_doi": "10.1002/example",
        "repository": "Dryad",
        "dataset_doi": "10.5061/dryad.example",
        "expected_dataset_title": "Data from: Exact Study Title",
        "validation_rule": "exact_normalized_dataset_title_match",
        "status": "ready_for_manifest_probe",
    }


def test_exact_title_match_allows_manifest_recovery() -> None:
    def fetch(url: str):
        if "api.datacite.org" in url:
            return 200, {
                "data": {
                    "attributes": {
                        "titles": [{"title": "Data from Exact Study Title"}],
                        "url": "https://datadryad.org/dataset/doi:10.5061/dryad.example",
                    }
                }
            }
        if "datasets/doi%3A10.5061%2Fdryad.example" in url:
            return 200, {
                "_embedded": {
                    "stash:files": [
                        {
                            "attributes": {
                                "filename": "processed.csv",
                                "download_url": "https://datadryad.org/download/processed.csv",
                            }
                        }
                    ]
                }
            }
        return 404, {}

    receipts, report = probe_targets([target()], fetch_json=fetch)

    assert len(receipts) == 1
    assert receipts[0].title_match == "yes"
    assert receipts[0].manifest_status == "manifest_recovered"
    assert receipts[0].file_name == "processed.csv"
    assert report["counts_by_manifest_status"]["manifest_recovered"] == 1


def test_title_mismatch_blocks_any_dryad_manifest_request() -> None:
    calls: list[str] = []

    def fetch(url: str):
        calls.append(url)
        return 200, {"data": {"attributes": {"titles": [{"title": "Different dataset"}]}}}

    receipts, _ = probe_targets([target()], fetch_json=fetch)

    assert receipts[0].manifest_status == "title_mismatch"
    assert len(calls) == 1
    assert "api.datacite.org" in calls[0]


def test_dryad_failure_remains_distinct_from_missing_title_validation() -> None:
    def fetch(url: str):
        if "api.datacite.org" in url:
            return 200, {"data": {"attributes": {"titles": [{"title": "Data from Exact Study Title"}]}}}
        raise TimeoutError("Dryad endpoint timed out")

    receipts, _ = probe_targets([target()], fetch_json=fetch)

    assert receipts[0].title_match == "yes"
    assert receipts[0].manifest_status == "dryad_access_failed"
    assert "TimeoutError" in receipts[0].notes
