from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"


def _text() -> str:
    return MANUSCRIPT.read_text(encoding="utf-8")


def _abstract(text: str) -> str:
    return text.split("## Abstract", 1)[1].split("**Keywords:**", 1)[0]


def test_identification_manuscript_has_required_structure() -> None:
    text = _text()
    required = [
        "## 1. Introduction",
        "## 2. The estimand: a trait interaction that can actually be measured",
        "## 3. A crossed intervention design for channel identification",
        "## 4. How close do existing studies come?",
        "## 5. Designing an identifiable experiment",
        "## 6. Discussion",
        "## 7. Conclusions",
    ]
    for heading in required:
        assert heading in text


def test_old_theorem_led_headlines_are_absent_from_abstract() -> None:
    abstract = _abstract(_text())
    forbidden = [
        "2,592",
        "77.2%",
        "selectivity window",
        "one-sided bound",
        "Leal et al.",
        "Sasidharan et al.",
    ]
    for phrase in forbidden:
        assert phrase not in abstract


def test_identification_gates_are_explicit() -> None:
    text = _text()
    required = [
        "16 cells",
        "selective interventions",
        "four-way interaction",
        "m_{0,\\Delta}",
        "independent cost assay",
        "unallocated",
        "secant interaction",
    ]
    for phrase in required:
        assert phrase in text


def test_empirical_anchor_roles_are_not_collapsed() -> None:
    text = _text()
    assert "A trait-factorial anchor: Kessler et al. 2008" in text
    assert "A consumer-factorial counterpart: Egan et al. 2021" in text
    assert "Public-data retrofit: Soper Gorden and Adler 2018" in text
    assert "The missing object is their intersection" in text


def test_joint_residual_is_not_defined_as_kappa() -> None:
    text = _text()
    assert "This residual is not automatically a joint construction or allocation cost" in text
    assert "The cost channel therefore requires a separate" in text
