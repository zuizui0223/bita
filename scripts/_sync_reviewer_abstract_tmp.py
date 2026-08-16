from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_THEORETICAL_ECOLOGY.md"
PORTAL = ROOT / "submission" / "AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md"
HOUSE = ROOT / "tests" / "test_theoretical_ecology_house_style.py"
SELF = Path(__file__)
WORKFLOW = ROOT / ".github" / "workflows" / "_sync-reviewer-abstract-tmp.yml"

old_sentence = "We prove this implication algebraically, then use 2,592 declared evaluations across four response-shape variants to verify the implementation and quantify the bound's looseness: about 23% of points inside this selectivity window remain substitutable, so the window is necessary but not sufficient."
new_sentence = "We prove this algebraically, then use 2,592 evaluations across four response-shape variants to verify implementation and quantify looseness: about 23% of points inside this selectivity window remain substitutable, so the window is necessary but not sufficient."

for path in (MANUSCRIPT, PORTAL):
    text = path.read_text(encoding="utf-8")
    target = old_sentence if path == MANUSCRIPT else "Across 2,592 declared evaluations and four response-shape variants we find no counterexample, whereas about 23% of points inside this selectivity window remain substitutable, so the window is necessary but not sufficient."
    if text.count(target) != 1:
        raise RuntimeError(f"expected one abstract target in {path}, got {text.count(target)}")
    text = text.replace(target, new_sentence, 1)
    if path == PORTAL:
        old_data = "> Code, declared configurations, generated readouts, source-adjudication products, saturation receipts, quantitative-synthesis outputs, validation tests, and canonical manuscript figures are maintained in the public GitHub repository `https://github.com/zuizui0223/bita`. The completed Leal et al. (2025) floral-larceny meta-analysis is pinned to immutable repository commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`, while the Sasidharan et al. (2023) synthesis uses the 32-study-component citation topology recorded on the integration line. The saturated Pattern ledgers/context programs and source-access receipts for the secondary contextual syntheses are versioned with the candidate manuscript. The exact submitted repository release and archival DOI will be inserted before portal submission."
        new_data = "> Code, declared configurations, generated readouts, source-adjudication products, saturation receipts, quantitative-synthesis outputs, validation tests, and canonical manuscript figures are maintained in the public GitHub repository `https://github.com/zuizui0223/bita`. The complete Leal et al. (2025) floral-larceny module is included directly in the canonical repository tree, with provenance additionally pinned to immutable commit `ed33b25593c0d90ad6657753f6f5501d9efc7b82`; the Sasidharan et al. (2023) synthesis uses the 32-study-component citation topology recorded in the canonical integration state. The saturated Pattern ledgers/context programs and source-access receipts for the secondary contextual syntheses are versioned with the manuscript. The exact submitted repository release and archival DOI will be inserted before portal submission."
        if text.count(old_data) != 1:
            raise RuntimeError("expected one portal data-availability target")
        text = text.replace(old_data, new_data, 1)
    path.write_text(text, encoding="utf-8")

text = HOUSE.read_text(encoding="utf-8")
old = '    assert "OpenAI large language model" in block\n    assert "AI-generated output was not treated as empirical evidence" in block'
new = '    assert "OpenAI" in block\n    assert "Anthropic" in block\n    assert "AI-generated output was not treated as empirical evidence" in block'
if text.count(old) != 1:
    raise RuntimeError("expected one AI house-style assertion block")
HOUSE.write_text(text.replace(old, new, 1), encoding="utf-8")

if WORKFLOW.exists():
    WORKFLOW.unlink()
if SELF.exists():
    SELF.unlink()
