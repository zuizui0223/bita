from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = (ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md").read_text(encoding="utf-8")
REFERENCES = (ROOT / "manuscript" / "IDENTIFICATION_DESIGN_REFERENCES.md").read_text(encoding="utf-8")


def test_core_empirical_citations_are_in_manuscript_and_bibliography() -> None:
    manuscript_tokens = [
        "Kessler et al. (2008)",
        "Egan et al. (2021)",
        "Soper Gorden and Adler (2018)",
        "Sun and Huang (2015)",
        "Kessler et al. (2015)",
        "Theis and Adler (2012)",
    ]
    for token in manuscript_tokens:
        assert token in MANUSCRIPT

    dois = [
        "10.1126/science.1160072",
        "10.1002/evl3.262",
        "10.1002/ajb2.1182",
        "10.1093/aobpla/plv019",
        "10.7554/eLife.07641",
        "10.1890/11-0825.1",
    ]
    for doi in dois:
        assert doi in REFERENCES


def test_background_reference_spine_is_focused() -> None:
    dois = [
        "10.1016/j.tree.2021.09.007",
        "10.1111/j.1461-0248.2006.00975.x",
        "10.1111/j.1365-2435.2009.01639.x",
        "10.1016/j.tplants.2015.10.013",
        "10.1525/california/9780520251328.003.0012",
        "10.1093/oso/9780198570851.003.0007",
        "10.1002/ecs2.1326",
    ]
    for doi in dois:
        assert doi in REFERENCES


def test_old_quantitative_modules_are_not_in_focused_bibliography() -> None:
    assert "Leal et al." not in REFERENCES
    assert "Sasidharan" not in REFERENCES


def test_reference_entries_are_alphabetically_grouped_by_first_author() -> None:
    entries = [line for line in REFERENCES.splitlines() if line and not line.startswith("#") and not line.startswith("This ")]
    first_authors = [line.split()[0] for line in entries]
    assert first_authors == sorted(first_authors)
