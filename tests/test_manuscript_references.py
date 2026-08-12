from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"


def _split_manuscript() -> tuple[str, str]:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    body, after_refs = text.split("\n## References\n", 1)
    refs = after_refs.split("\n## Statements and Declarations\n", 1)[0]
    return body, refs


def test_known_reference_corrections_are_preserved() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")

    assert "*Functional Ecology* 31:65–75" in text
    assert "https://doi.org/10.1111/1365-2435.12761" in text
    assert "10.1146/annurev-ento-031616-035013" not in text
    assert "*Annual Review of Entomology* 62:117–138" not in text

    assert "10.1111/nph.12930" not in text
    assert "Floral integration, modularity, and accuracy" not in text

    for obsolete in (
        "Fenster CB, Armbruster WS",
        "Harder LD, Johnson SD",
        "Krupnick GA, Weis AE, Campbell DR",
        "McCall AC, Irwin RE",
        "Mothershead K, Marquis RJ",
        "Schiestl FP, Johnson SD",
    ):
        assert obsolete not in text


def test_core_empirical_reference_identities_remain_present() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    for doi in (
        "10.1002/ecy.70036",
        "10.1093/aob/mcad064",
        "10.1002/ajb2.1182",
        "10.1093/aob/mcaf258",
        "10.1111/evo.13639",
        "10.1093/aob/mcq045",
        "10.1371/journal.pone.0098755",
        "10.1093/aobpla/plv019",
        "10.1093/jpe/rtad036",
        "10.1111/evo.13965",
    ):
        assert doi in text


def test_cited_reference_spine_is_present_in_body_and_bibliography() -> None:
    body, refs = _split_manuscript()
    cited = {
        "Lande and Arnold 1983": "Lande R, Arnold SJ (1983)",
        "Phillips and Arnold 1989": "Phillips PC, Arnold SJ (1989)",
        "Blows and Brooks 2003": "Blows MW, Brooks R (2003)",
        "Herrera et al. 2002": "Herrera CM et al. (2002)",
        "Knauer et al. 2018": "Knauer AC, Bakhtiari M, Schiestl FP (2018)",
        "Strauss et al. 1999": "Strauss SY, Siemens DH, Decher MB, Mitchell-Olds T (1999)",
        "Theis and Adler 2012": "Theis N, Adler LS (2012)",
        "Wright et al. 2013": "Wright GA et al. (2013)",
        "Richardson et al. 2015": "Richardson LL et al. (2015)",
        "Stevenson et al. 2017": "Stevenson PC, Nicolson SW, Wright GA (2017)",
        "Leal et al. (2025)": "Leal LC et al. (2025)",
        "Sasidharan et al. (2023)": "Sasidharan R, Junker RR, Eilers EJ, Müller C (2023)",
        "Gorden and Adler's (2018)": "Soper Gorden NL, Adler LS (2018)",
        "Haas-Desmarais et al. (2026)": "Haas-Desmarais S, Castagneyrol B, Abdala-Roberts L, Lortie CJ, Traveset A, Moreira X (2026)",
        "Caruso et al. (2019)": "Caruso CM, Eisen KE, Martin RA, Sletvold N (2019)",
        "Junker and Blüthgen (2010)": "Junker RR, Blüthgen N (2010)",
        "Page et al. 2014": "Page P, Favre A, Schiestl FP, Karrenberg S (2014)",
        "Sun and Huang 2015": "Sun SG, Huang SQ (2015)",
        "Wu and Gao 2024": "Wu SM, Gao JY (2024)",
        "Zhou et al. 2020": "Zhou J, Reynolds RJ, Zimmer EA, Dudash MR, Fenster CB (2020)",
    }
    for in_text, reference in cited.items():
        assert in_text in body, in_text
        assert reference in refs, reference


def test_bibliography_has_only_the_cited_reference_spine() -> None:
    _, refs = _split_manuscript()
    entries = [block for block in refs.strip().split("\n\n") if block.strip()]
    assert len(entries) == 20
    first_authors = [entry.split()[0] for entry in entries]
    assert first_authors == sorted(first_authors, key=str.casefold)
