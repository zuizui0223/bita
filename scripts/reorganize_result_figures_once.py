from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def must_replace(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing expected text for {label}")
    return text.replace(old, new, 1)


# 1) Canonical manuscript: make the five Main figures result-bearing.
path = "manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md"
text = read(path)
old = (
    "The cross-system evidence architecture is summarized in Fig. 3 and Table 3, with the quantitative modules in Table 4; "
    "full route, conditionality, direct-identification, and stopping-rule records are provided in Tables S3–S6, with same-system and module-robustness displays in Supplementary Figs. S3–S4. "
    "The complete Mechanism → Pattern inference sequence—from the elementary one-sided exclusion to theory-defined evidence classes and experimental triage—is summarized in Fig. 4."
)
new = (
    "The cross-system evidence architecture is summarized in Fig. 3 and Table 3, with the quantitative modules in Table 4. "
    "The reproduced quantitative results and their identification boundary are shown directly in Fig. 4, while the 14 same-system multi-route clusters are shown study-by-study in Fig. 5. "
    "Full route, conditionality, direct-identification, and stopping-rule records are provided in Tables S3–S6, with numerical implementation and robustness diagnostics in Supplementary Figs. S1–S3."
)
text = must_replace(text, old, new, "manuscript 5.6 figure hierarchy")
caption_pattern = re.compile(r"\*\*Fig\. 4\*\*.*?\n\n\*\*Fig\. 5\*\*.*?(?=\n\n## Table captions)", re.S)
replacement = (
    "**Fig. 4** Quantitative evidence, identification boundary, and next empirical tests. The Leal et al. floral-larceny module shows negative pooled directions for female fitness, nectar standing crop, and legitimate visitation while retaining a female-fitness prediction interval spanning both signs and weak moderator explanation. The Sasidharan et al. floral-volatile module retains a positive assembled florivore-minus-pollinator contrast under all leave-one-component-out refits but lacks a paired within-study consumer-role difference. Neither module estimates \\(\\rho\\), \\(\\iota\\), \\(\\kappa\\), or total \\(W_{AD}\\). The remaining direct-identification state is one strict sign-unresolved total-outcome cluster and zero strict joint-cost estimates, motivating first a 2 × 2 cost assay for the sign of \\(\\kappa\\), then a full attraction × defence factorial for total and channel-resolved calibration.\n\n"
    "**Fig. 5** Same-system route architecture across the saturated evidence universe. Rows are the 14 independent biological clusters with at least two linked marginal route families, or an explicit same-system linkage retained by the evidence audit. Filled cells indicate categorical presence of A → pollination, A → antagonism, D → antagonism, and D → pollination routes. The matrix shows recurrence of linked constituent mechanisms within biological systems; cells are not effect sizes and do not constitute direct \\(A\\times D\\) evidence."
)
text, n = caption_pattern.subn(replacement, text, count=1)
if n != 1:
    raise RuntimeError("failed to replace Fig. 4–5 captions")
write(path, text)

# 2) Reader-facing supplement: retain only verification/detail/robustness figures.
path = "manuscript/supplementary/SUPPLEMENTARY_MATERIAL.md"
text = read(path)
text, n = re.subn(r"\n\n\*\*Fig\. S3\*\*.*?(?=\n\n\*\*Fig\. S4\*\*)", "", text, count=1, flags=re.S)
if n != 1:
    raise RuntimeError("failed to remove old Supplementary Fig. S3 caption")
text = must_replace(text, "**Fig. S4**", "**Fig. S3**", "renumber robustness figure")
text = text.replace("FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg\n", "")
text = text.replace("FIGURE_S4_QUANTITATIVE_ROBUSTNESS.svg", "FIGURE_S4_QUANTITATIVE_ROBUSTNESS.svg  # reader-facing Fig. S3 source")
text = text.replace("Supplementary Figures S1–S4", "Supplementary Figures S1–S3")
write(path, text)

# 3) Figure provenance: drop orientation-only Fig. 4 and document result-first hierarchy.
path = "manuscript/figures/README.md"
text = read(path)
pattern = re.compile(r"## Figure 4\n\n.*?(?=\n## Current EPS export validation)", re.S)
replacement = (
    "## Figure 4\n\n"
    "Main Figure 4 uses the existing frozen source `FIGURE_5_QUANTITATIVE_IDENTIFICATION_BOUNDARY.svg`. The retained filename records its origin on PR #141; in the Ecology Main Document it is numbered Figure 4. It visualizes only frozen Leal and Sasidharan quantitative results, their inference boundaries, the one strict sign-unresolved total-outcome cluster, zero strict joint-cost estimates, and the two next empirical tests. It must not be interpreted as a pooled estimate of `W_AD`.\n\n"
    "## Figure 5\n\n"
    "Main Figure 5 reuses the frozen source `manuscript/supplementary/figures/FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg`. It displays the 14 independent same-system biological clusters and categorical presence of the four constituent route families. Its promotion to Main changes presentation hierarchy only; it adds no analysis and does not convert linked marginal routes into direct `A × D` evidence.\n"
)
text, n = pattern.subn(replacement, text, count=1)
if n != 1:
    raise RuntimeError("failed to rewrite figure provenance 4–5")
text = text.replace("The five committed SVG sources are the canonical Main-figure sources.", "The Ecology Main Document contains five figures; Figures 4–5 reuse frozen sources without duplicating them solely for renumbering.")
write(path, text)

# 4) Submission builder: Main Fig.4 = quantitative, Main Fig.5 = same-system; Appendix = S1,S2,robustness only.
path = "scripts/build_ecology_submission_sources.py"
text = read(path)
text = text.replace(
    '"full route, conditionality, direct-identification, and stopping-rule records are provided as machine-readable Open Research data products, with same-system and module-robustness displays in Appendix S1: Figures S3–S4.":\n            "full route, conditionality, direct-identification, and stopping-rule records are provided as machine-readable Open Research data products, with same-system and module-robustness displays in Appendix S1: Figures S3–S4.",',
    '"full route, conditionality, direct-identification, and stopping-rule records are provided as machine-readable Open Research data products, with numerical robustness in Appendix S1: Figure S3.":\n            "full route, conditionality, direct-identification, and stopping-rule records are provided as machine-readable Open Research data products, with numerical robustness in Appendix S1: Figure S3.",'
)
text = text.replace('"Supplementary Figs. S3–S4": "Appendix S1: Figures S3–S4",', '"Supplementary Fig. S3": "Appendix S1: Figure S3",\n        "Supplementary Figs. S1–S3": "Appendix S1: Figures S1–S3",')
fig_block = re.compile(r"    figure_pages = \[\]\n    figure_names = \{.*?\n    for idx in range\(1, 6\):\n        figure_pages\.append\(.*?\n        \)\n", re.S)
new_fig_block = '''    figure_pages = []
    figure_paths = {
        1: "../../../manuscript/figures/FIGURE_1_MECHANISTIC_ARCHITECTURE.svg",
        2: "../../../manuscript/figures/FIGURE_2_THEORY_REGIME_MAP.svg",
        3: "../../../manuscript/figures/FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg",
        4: "../../../manuscript/figures/FIGURE_5_QUANTITATIVE_IDENTIFICATION_BOUNDARY.svg",
        5: "../../../manuscript/supplementary/figures/FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg",
    }
    for idx in range(1, 6):
        figure_pages.append(
            f"{PAGEBREAK}\\n\\n**Figure {idx}**\\n\\n"
            f"![]({figure_paths[idx]})"
        )
'''
text, n = fig_block.subn(new_fig_block, text, count=1)
if n != 1:
    raise RuntimeError("failed to replace main figure path block")
text = text.replace("for idx in range(1, 5):", "for idx in range(1, 4):", 2)
text = text.replace(
    '        3: "FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg",\n        4: "FIGURE_S4_QUANTITATIVE_ROBUSTNESS.svg",',
    '        3: "FIGURE_S4_QUANTITATIVE_ROBUSTNESS.svg",'
)
write(path, text)

# 5) Figure/table plan: make Main 4 quantitative, Main 5 same-system; Supplement only checks/details.
path = "submission/FIGURE_AND_TABLE_PLAN.md"
text = read(path)
text = must_replace(
    text,
    "### Figure 4. Mechanism → Pattern overview\n\n**Purpose:** give readers one map from the ecological problem through the elementary one-sided exclusion, theory-defined evidence classes, the recurrent Pattern, remaining identification gaps, and experimental triage. It is a synthesis/orientation figure and introduces no new analysis.\n\n### Figure 5. Quantitative evidence, identification boundary, and next tests\n\n**Purpose:** make the two reproduced quantitative modules visible in the Main Document while preserving their incompatible scales and explicit limitations. The figure must show the Leal pooled directions/prediction interval/moderator range, the Sasidharan assembled contrast/LOCO result and paired-role limitation, then terminate at the direct-identification gap and the 2 × 2 cost-test versus full-factorial calibration sequence.",
    "### Figure 4. Quantitative evidence, identification boundary, and next tests\n\n**Purpose:** make the two reproduced quantitative modules visible in the Main Document while preserving their incompatible scales and explicit limitations. The figure shows the Leal pooled directions/prediction interval/moderator range, the Sasidharan assembled contrast/LOCO result and paired-role limitation, then terminates at the direct-identification gap and the 2 × 2 cost-test versus full-factorial calibration sequence.\n\n### Figure 5. Same-system route architecture\n\n**Purpose:** show that the constituent mechanisms are not only assembled across unrelated studies. Display the 14 independent biological clusters with linked route families as a categorical matrix. Presence is not an effect size and same-system linkage is not direct `A x D` evidence.",
    "figure plan 4–5",
)
text = must_replace(
    text,
    "### Figure S3\nStudy-level same-system Pattern ledger as a categorical matrix.\n\n### Figure S4\nQuantitative robustness panels: Leal leave-one-cluster-out/sensitivity summaries and Sasidharan leave-one-study-component-out range. Keep metrics visually separate. **These robustness panels remain supplementary rather than being added to main Figure 3.**",
    "### Figure S3\nQuantitative robustness panels: Leal leave-one-cluster-out/sensitivity summaries and Sasidharan leave-one-study-component-out range. Keep metrics visually separate. **These robustness panels remain supplementary rather than being folded into Main Figure 4.**",
    "supp figure plan",
)
text = text.replace("Integration:         Figures 4–5", "Part II — Pattern:   Figures 3–5, Tables 3–4")
write(path, text)

# 6) Supplement manifest: state the promoted same-system matrix and three reader-facing Supplement figures.
path = "SUPPLEMENT_MANIFEST.md"
text = read(path)
text = text.replace("- `manuscript/figures/FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg`\n- `manuscript/TABLES_THEORETICAL_ECOLOGY.md`", "- `manuscript/figures/FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg`\n- `manuscript/figures/FIGURE_5_QUANTITATIVE_IDENTIFICATION_BOUNDARY.svg` (Main Fig. 4 source)\n- `manuscript/supplementary/figures/FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg` (Main Fig. 5 source)\n- `manuscript/TABLES_THEORETICAL_ECOLOGY.md`")
text = text.replace("- `FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg`\n- `FIGURE_S4_QUANTITATIVE_ROBUSTNESS.svg`", "- `FIGURE_S4_QUANTITATIVE_ROBUSTNESS.svg` (reader-facing Fig. S3 source)")
text = text.replace("Supplementary Figures S1–S4", "Supplementary Figures S1–S3")
text = text.replace("All seven figure sources have been rendered and visually inspected.", "All reader-facing figure sources have been rendered and visually inspected; the same-system matrix is now promoted to Main Figure 5 rather than duplicated in Appendix S1.")
write(path, text)

# 7) Packaging tests: assert the new hierarchy.
path = "tests/test_ecology_submission_packaging.py"
text = read(path)
text = text.replace('assert "Appendix S1: Figures S3–S4" in text', 'assert "Appendix S1: Figure S3" in text')
text = text.replace("for idx in range(1, 5):\n        assert f\"### Figure S{idx}\" in text", "for idx in range(1, 4):\n        assert f\"### Figure S{idx}\" in text\n    assert \"### Figure S4\" not in text")
old_test = re.compile(r"def test_main_figures_4_5_are_present_and_frozen\(\) -> None:.*", re.S)
new_test = '''def test_main_figures_4_5_are_present_and_frozen() -> None:
    quantitative = ROOT / "manuscript" / "figures" / "FIGURE_5_QUANTITATIVE_IDENTIFICATION_BOUNDARY.svg"
    same_system = ROOT / "manuscript" / "supplementary" / "figures" / "FIGURE_S3_SAME_SYSTEM_ROUTE_MATRIX.svg"
    overview = ROOT / "manuscript" / "figures" / "FIGURE_4_MECHANISM_PATTERN_OVERVIEW.svg"
    assert quantitative.exists() and same_system.exists()
    assert not overview.exists()
    tq = quantitative.read_text(encoding="utf-8")
    ts = same_system.read_text(encoding="utf-8")
    for token in ("Floral larceny", "+0.129", "35/48", "0 strict estimates", "Next tests"):
        assert token in tq
    for token in ("A → pollination", "D → pollination", "Rows are independent biological clusters"):
        assert token in ts
'''
text, n = old_test.subn(new_test, text, count=1)
if n != 1:
    raise RuntimeError("failed to replace figure 4–5 packaging test")
write(path, text)

print("result-first figure hierarchy synchronized")
