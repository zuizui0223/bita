from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "probe_kessler_2008_supplement.py"
SPEC = importlib.util.spec_from_file_location("kessler_supplement_probe", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_candidate_link_discovery_is_publisher_scoped_and_supplement_targeted() -> None:
    html = '''
    <a href="/doi/suppl/10.1126/science.1160072/suppl_file/1160072s1.pdf">supp</a>
    <a href="https://example.com/1160072s1.pdf">offsite</a>
    <a href="/doi/10.1126/science.1160072">article</a>
    '''
    links = MODULE.discover_candidate_links("https://www.science.org/doi/10.1126/science.1160072", html)
    assert links == [
        "https://www.science.org/doi/10.1126/science.1160072",
        "https://www.science.org/doi/suppl/10.1126/science.1160072/suppl_file/1160072s1.pdf",
    ]
    assert all("example.com" not in link for link in links)


def test_probe_fails_closed_when_registered_routes_are_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(MODULE, "SEED_URLS", ("https://www.science.org/doi/10.1126/science.1160072",))

    def fail_fetch(url: str):
        raise RuntimeError("publisher unavailable")

    report = MODULE.probe(fetch=fail_fetch)
    assert report["supplement_status"] == "NOT_RECOVERED_FROM_REGISTERED_PUBLIC_ROUTES"
    assert report["figure_s8a_text_status"] == "NOT_EVALUABLE"
    assert "Do not infer" in report["claim_boundary"]
    assert report["attempts"][0]["status"] == "fetch_failed"


def test_recovered_supplement_without_target_text_does_not_claim_uncertainty(monkeypatch) -> None:
    monkeypatch.setattr(MODULE, "SEED_URLS", ("https://www.science.org/doi/suppl/10.1126/science.1160072/suppl_file/1160072s1.pdf",))
    monkeypatch.setattr(MODULE, "_extract_target_text", lambda payload: {
        "text_extraction_status": "success",
        "page_count": 12,
        "matched_pages": [],
    })

    def fake_fetch(url: str):
        return MODULE.FetchResult(
            requested_url=url,
            final_url=url,
            status=200,
            content_type="application/pdf",
            payload=b"%PDF-1.4 synthetic",
        )

    report = MODULE.probe(fetch=fake_fetch)
    assert report["supplement_status"] == "SUPPLEMENT_PDF_RECOVERED"
    assert report["figure_s8a_text_status"] == "PDF_RECOVERED_TARGET_NOT_TEXT_EXTRACTABLE"
    assert "formal A:D interaction uncertainty still requires exact day/cell values" in report["claim_boundary"]


def test_markdown_preserves_access_not_inference_boundary(monkeypatch) -> None:
    monkeypatch.setattr(MODULE, "SEED_URLS", ("https://www.science.org/doi/10.1126/science.1160072",))

    def fail_fetch(url: str):
        raise RuntimeError("no route")

    md = MODULE.render_markdown(MODULE.probe(fetch=fail_fetch))
    assert "NOT_RECOVERED_FROM_REGISTERED_PUBLIC_ROUTES" in md
    assert "NOT_EVALUABLE" in md
    assert "Do not infer a formal A:D interaction SE/CI" in md
