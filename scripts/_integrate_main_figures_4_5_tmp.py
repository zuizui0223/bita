from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"expected text not found in {path}: {old[:100]!r}")
    text = text.replace(old, new, 1)
    p.write_text(text, encoding="utf-8")


def append_before(path: str, marker: str, block: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if marker not in text:
        raise RuntimeError(f"marker not found in {path}: {marker!r}")
    if block.strip() not in text:
        text = text.replace(marker, block + "\n\n" + marker, 1)
    p.write_text(text, encoding="utf-8")


# 1. Make the matplotlib SVG builders byte-stable by removing timestamp metadata.
p = ROOT / "scripts/build_main_figures_4_5.py"
text = p.read_text(encoding="utf-8")
text = text.replace('fig.savefig(path, bbox_inches="tight")', 'fig.savefig(path, bbox_inches="tight", metadata={"Date": None})')
p.write_text(text, encoding="utf-8")

# 2. Add manuscript callouts and captions without changing any result.
replace_once(
    "manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md",
    "The cross-system evidence architecture is summarized in Fig. 3 and Table 3, with the quantitative modules in Table 4; full route, conditionality, direct-identification, and stopping-rule records are provided in Tables S3–S6, with same-system and module-robustness displays in Supplementary Figs. S3–S4.",
    "The cross-system evidence architecture is summarized in Fig. 3 and Table 3, with the quantitative modules in Table 4; full route, conditionality, direct-identification, and stopping-rule records are provided in Tables S3–S6, with same-system and module-robustness displays in Supplementary Figs. S3–S4. The complete Mechanism → Pattern inference sequence—from the elementary one-sided exclusion to theory-defined evidence classes and experimental triage—is summarized in Fig. 4.",
)
replace_once(
    "manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md",
    "The mechanism-first order therefore turns synthesis into experimental triage. The literature need not be enlarged indefinitely once the structural uncertainty has been localized: a comparatively cheap test of \\(\\kappa\\) can challenge applicability of the bound, whereas only a channel-resolved factorial can calibrate the full interaction. The synthesis thus resolves an empirical ambiguity by converting heterogeneous evidence into an ordered sequence of falsification and calibration rather than another call for undirected data collection.",
    "The mechanism-first order therefore turns synthesis into experimental triage. The literature need not be enlarged indefinitely once the structural uncertainty has been localized: a comparatively cheap test of \\(\\kappa\\) can challenge applicability of the bound, whereas only a channel-resolved factorial can calibrate the full interaction. The synthesis thus resolves an empirical ambiguity by converting heterogeneous evidence into an ordered sequence of falsification and calibration rather than another call for undirected data collection. The quantitative evidence, remaining identification gaps, and the two ordered next tests are summarized in Fig. 5.",
)
append_before(
    "manuscript/MANUSCRIPT_THEORETICAL_ECOLOGY.md",
    "## Table captions",
    "**Fig. 4** Mechanism-before-Pattern overview of the paper's inference sequence. The ecological attraction–defence problem is first decomposed into antagonist relief, pollinator interference, and direct joint-cost curvature. Under non-negative joint-cost curvature, the algebraic exclusion confines complementarity to a permissive selectivity window but does not make the converse true. These theory-defined mechanism classes then determine what evidence is counted in the cross-system synthesis. The recurrent empirical result is constituent mechanisms plus switching architectures rather than one universal sign, while direct total \\(A\\times D\\) evidence remains sparse and direct joint-cost curvature remains unidentified. The final step separates a 2 × 2 cost-assay applicability test from full channel-resolved calibration.\n\n**Fig. 5** Quantitative evidence, identification boundary, and next empirical tests. The Leal et al. floral-larceny module shows negative pooled directions for female fitness, nectar standing crop, and legitimate visitation while retaining a female-fitness prediction interval spanning both signs and weak moderator explanation. The Sasidharan et al. floral-volatile module retains a positive assembled florivore-minus-pollinator contrast under all leave-one-component-out refits but lacks a paired within-study consumer-role difference. Neither module estimates \\(\\rho\\), \\(\\iota\\), \\(\\kappa\\), or total \\(W_{AD}\\). The remaining direct-identification state is one strict sign-unresolved total-outcome cluster and zero strict joint-cost estimates, motivating first a 2 × 2 cost assay for the sign of \\(\\kappa\\), then a full attraction × defence factorial for total and channel-resolved calibration.",
)

# 3. Teach the Ecology submission builder to embed all five main figures.
replace_once(
    "scripts/build_ecology_submission_sources.py",
    '    figure_names = {\n        1: "MECHANISTIC_ARCHITECTURE",\n        2: "THEORY_REGIME_MAP",\n        3: "EMPIRICAL_MECHANISM_ARCHITECTURE",\n    }\n    for idx in range(1, 4):',
    '    figure_names = {\n        1: "MECHANISTIC_ARCHITECTURE",\n        2: "THEORY_REGIME_MAP",\n        3: "EMPIRICAL_MECHANISM_ARCHITECTURE",\n        4: "MECHANISM_PATTERN_OVERVIEW",\n        5: "QUANTITATIVE_IDENTIFICATION_BOUNDARY",\n    }\n    for idx in range(1, 6):',
)

# 4. Tighten package validation for five main figures.
replace_once(
    ".github/workflows/build-ecology-submission-package.yml",
    "          pdftotext \"$MAIN_PDF\" - | grep -q 'Figure 3'",
    "          pdftotext \"$MAIN_PDF\" - | grep -q 'Figure 3'\n          pdftotext \"$MAIN_PDF\" - | grep -q 'Figure 4'\n          pdftotext \"$MAIN_PDF\" - | grep -q 'Figure 5'",
)
replace_once(
    ".github/workflows/build-ecology-submission-package.yml",
    '            echo "main_figures=Figures 1-3 embedded, one figure page each"',
    '            echo "main_figures=Figures 1-5 embedded, one figure page each"',
)

# 5. Packaging regressions: five figures, canonical SVG presence, and frozen values.
p = ROOT / "tests/test_ecology_submission_packaging.py"
text = p.read_text(encoding="utf-8")
text = text.replace(
    '        "**Figure 3**",\n    ]',
    '        "**Figure 3**",\n        "**Figure 4**",\n        "**Figure 5**",\n    ]',
    1,
)
if "def test_main_figures_4_5_are_present_and_frozen" not in text:
    text += '''\n\ndef test_main_figures_4_5_are_present_and_frozen() -> None:\n    fig4 = ROOT / "manuscript" / "figures" / "FIGURE_4_MECHANISM_PATTERN_OVERVIEW.svg"\n    fig5 = ROOT / "manuscript" / "figures" / "FIGURE_5_QUANTITATIVE_IDENTIFICATION_BOUNDARY.svg"\n    assert fig4.exists() and fig5.exists()\n    t4 = fig4.read_text(encoding="utf-8")\n    t5 = fig5.read_text(encoding="utf-8")\n    for token in ("Mechanism before Pattern", "2,592 evaluations", "56 route records", "25 independent clusters"):\n        assert token in t4\n    for token in ("Floral larceny", "+0.129", "35/48", "0 strict estimates", "Next tests"):\n        assert token in t5\n'''
p.write_text(text, encoding="utf-8")

# 6. Reader-facing figure provenance and visual plan.
append_before(
    "manuscript/figures/README.md",
    "## Current EPS export validation",
    "## Figure 4\n\n`FIGURE_4_MECHANISM_PATTERN_OVERVIEW.svg` is generated by `scripts/build_main_figures_4_5.py` from frozen manuscript-facing constants only. It is a reader-orientation figure: it connects the ecological problem, the one-line selectivity exclusion, theory-defined evidence classes, the 56-record/25-cluster Pattern architecture, the remaining direct-identification gaps, and the ordered falsification/calibration programme. It does not add a new analysis or claim.\n\n## Figure 5\n\n`FIGURE_5_QUANTITATIVE_IDENTIFICATION_BOUNDARY.svg` is generated by the same script. It visualizes only frozen Leal and Sasidharan quantitative results, their inference boundaries, the one strict sign-unresolved total-outcome cluster, zero strict joint-cost estimates, and the two next empirical tests. It must not be interpreted as a pooled estimate of \\(W_{AD}\\).",
)
replace_once(
    "manuscript/figures/README.md",
    "The three committed SVG sources have passed a reproducible EPS vector-export workflow using Inkscape CLI with text converted to paths to prevent font substitution.",
    "The five committed SVG sources are the canonical Main-figure sources. Figures 1–3 have already passed the existing reproducible EPS vector-export workflow using Inkscape CLI with text converted to paths to prevent font substitution; Figures 4–5 must be included when that export workflow is rerun from the final submission commit.",
)

# 7. Keep supplement/repository manifests and figure plan synchronized.
p = ROOT / "SUPPLEMENT_MANIFEST.md"
text = p.read_text(encoding="utf-8")
needle = "- `manuscript/figures/FIGURE_3_EMPIRICAL_MECHANISM_ARCHITECTURE.svg`"
if needle in text and "FIGURE_4_MECHANISM_PATTERN_OVERVIEW.svg" not in text:
    text = text.replace(needle, needle + "\n- `manuscript/figures/FIGURE_4_MECHANISM_PATTERN_OVERVIEW.svg`\n- `manuscript/figures/FIGURE_5_QUANTITATIVE_IDENTIFICATION_BOUNDARY.svg`", 1)
text = text.replace("All seven figure sources", "All nine figure sources")
p.write_text(text, encoding="utf-8")

p = ROOT / "submission/FIGURE_AND_TABLE_PLAN.md"
text = p.read_text(encoding="utf-8")
text = text.replace(
    "Part I — Mechanism: Figures 1–2, Tables 1–2\nPart II — Pattern:   Figure 3, Tables 3–4",
    "Part I — Mechanism: Figures 1–2, Tables 1–2\nPart II — Pattern:   Figure 3, Tables 3–4\nIntegration:         Figures 4–5",
    1,
)
if "### Figure 4. Mechanism → Pattern overview" not in text:
    marker = "### Table 3. Cross-study Pattern scaffold"
    block = "### Figure 4. Mechanism → Pattern overview\n\n**Purpose:** give readers one map from the ecological problem through the elementary one-sided exclusion, theory-defined evidence classes, the recurrent Pattern, remaining identification gaps, and experimental triage. It is a synthesis/orientation figure and introduces no new analysis.\n\n### Figure 5. Quantitative evidence, identification boundary, and next tests\n\n**Purpose:** make the two reproduced quantitative modules visible in the Main Document while preserving their incompatible scales and explicit limitations. The figure must show the Leal pooled directions/prediction interval/moderator range, the Sasidharan assembled contrast/LOCO result and paired-role limitation, then terminate at the direct-identification gap and the 2 × 2 cost-test versus full-factorial calibration sequence.\n\n"
    text = text.replace(marker, block + marker, 1)
p.write_text(text, encoding="utf-8")

print("integrated main Figures 4 and 5")
