from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
SUPP = ROOT / "manuscript" / "supplementary" / "SUPPLEMENT_IDENTIFICATION_DESIGN.md"
REFS = ROOT / "manuscript" / "IDENTIFICATION_DESIGN_REFERENCES.md"
FIG_BUILDER = ROOT / "scripts" / "build_identification_design_figures_svg.py"
FIG_TEST = ROOT / "tests" / "test_identification_design_figures.py"
TE_BUILDER = ROOT / "scripts" / "build_theoretical_ecology_submission_sources.py"
TE_TEST = ROOT / "tests" / "test_theoretical_ecology_submission_package.py"


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one occurrence, found {count}: {old[:100]!r}")
    return text.replace(old, new, 1)


def promote_manuscript() -> None:
    text = MAN.read_text(encoding="utf-8")

    # Fail closed if the post-PR-153 outcome hierarchy or Kessler partial-ID result drifted.
    invariants = (
        "**Level 1 — positive interaction relief**",
        "**Level 2 — constraint release**",
        "**Level 3 — strict reversal**",
        r"A_0=p_{10}-p_{00}\in[-0.02993,+0.02993]",
        r"A_1=p_{11}-p_{01}\in[+0.20013,+0.23984]",
        "It does **not** identify Level-2 constraint release or Level-3 strict reversal",
    )
    for token in invariants:
        if token not in text:
            raise RuntimeError(f"canonical invariant missing before V2 promotion: {token}")

    text = replace_once(
        text,
        "none of 16 screened high-information systems combines the full allocation design and independent joint-cost assay",
        "none of 17 screened high-information systems combines the full allocation design and independent joint-cost assay",
        label="abstract frontier count",
    )

    old_42 = (
        "Sixteen high-information systems were retained. None reaches the full sequence from trait interaction to channel allocation and independent joint-cost measurement, but this is more informative than a binary 0-of-16 result. The studies occupy complementary faces of an identification frontier: some supply a trait factorial, others a consumer factorial, randomized context modification, or a selective defence mechanism. The empirical pattern is therefore **design fragmentation**. Existing studies contain different pieces of the information needed to shrink \\(\\mathcal I(\\delta)\\), but no screened system closes all dimensions of the allocation problem."
    )
    new_42 = (
        "Seventeen high-information systems were retained. None reaches the full sequence from trait interaction to channel allocation and independent joint-cost measurement, but this is more informative than a binary 0-of-17 result. The studies occupy complementary lower-dimensional faces of the target \\(A\\times D\\times E_G\\times E_P\\) architecture. Kessler et al. (2008) supplies the strongest direct \\(A\\times D\\)-like trait face; Theis and Adler (2012) supplies a manipulated attraction \\(\\times\\) beetle-removal \\(\\times\\) pollination-supplementation bridge; Santangelo et al. (2019) supplies a defence \\(\\times\\) herbivore-suppression \\(\\times\\) hand-pollination backbone with observed floral traits; Egan et al. (2021) supplies the consumer-factorial face; Soper Gorden and Adler (2018) supplies observational A/D coordinates under randomized context modification; and Sun and Huang (2015) supplies a selective flower-associated defence mechanism. These are structural faces, not equivalent treatments: in particular, supplemental hand pollination is not a selective pollinator-access toggle. The empirical pattern is therefore a **fragmented identification frontier**. Existing studies contain different pieces of the information needed to shrink \\(\\mathcal I(\\delta)\\), but no screened system closes all dimensions of the allocation problem."
    )
    text = replace_once(text, old_42, new_42, label="section 4.2 frontier paragraph")

    old_46 = (
        "### 4.6 Other informative near misses\n\n"
        "Two additional systems isolate different design requirements. Kessler et al. (2015) crossed floral scent and nectar production, but nectar is a reward axis rather than an independently justified antagonist-reducing defence trait; this biological orientation problem is more fundamental than the absence of a recovered machine-readable outcome table. In *Pedicularis rex*, Sun and Huang (2015) manipulated a water-holding bract barrier that strongly affected seed predation without a detected effect on legitimate pollinator or nectar-robber visitation. This provides a practical model for selective access, but no independent attraction manipulation was present.\n\n"
        "Across the 16 screened systems, failure modes therefore differ—missing trait interactions, missing consumer factorials, invalid floral coordinates, or missing attraction manipulation—but no system includes an independent attraction-by-defence joint-cost assay."
    )
    new_46 = (
        "### 4.6 Complementary experimental faces\n\n"
        "Theis and Adler (2012) adds a distinct structural face. Enhanced floral fragrance was crossed with repeated beetle removal and supplemental hand pollination on female reproduction, creating an attraction \\(\\times\\) antagonist-removal \\(\\times\\) pollination-supplementation backbone. This is substantially closer to the target architecture than a trait-only experiment, but it is not channel identification: the study lacks an independently manipulated defence coordinate, and supplemental hand pollination adds pollen rather than creating pollinator absence/presence. It therefore cannot identify the target pollinator increment or \\(m_{0,\\Delta}\\).\n\n"
        "Other systems isolate additional missing axes. Kessler et al. (2015) crossed floral scent and nectar production, but nectar is a reward axis rather than an independently justified antagonist-reducing defence trait. In *Pedicularis rex*, Sun and Huang (2015) manipulated a water-holding bract barrier that strongly affected seed predation without a detected effect on legitimate pollinator or nectar-robber visitation, but no independent attraction manipulation was present. Santangelo et al. (2019) provides a defence-by-herbivore-suppression-by-hand-pollination backbone, but its defence axis is whole-plant HCN rather than a strict flower-associated \\(D\\), and hand pollination again is not selective pollinator access.\n\n"
        "Across the 17 screened systems, failure modes therefore differ—missing trait interactions, missing consumer factorials, invalid floral coordinates, missing attraction manipulation, missing pollinator-absent baseline characterization, or missing independent cost measurement—but no system closes the full allocation design or includes an independent attraction-by-defence joint-cost assay."
    )
    text = replace_once(text, old_46, new_46, label="section 4.6 complementary faces")

    text = replace_once(
        text,
        "The 16 systems were selected because they are close to the identification target or expose informative failure modes. A future systematic review could quantify design prevalence, but such a count is not needed to demonstrate the logical distinction among total interaction, consumer-context modification and channel identification.",
        "The 17 systems were selected because they are close to the identification target or expose informative failure modes. Their face counts describe screened-set evidence capacity, not literature prevalence. A future systematic review could quantify design prevalence, but such a count is not needed to demonstrate the logical distinction among total interaction, consumer-context modification and channel identification.",
        label="limits frontier count",
    )

    old_conclusion = (
        "The four constituent ecological pathway families recur across independent systems, while high-information studies already occupy complementary parts of this identification frontier. A direct trait factorial, a consumer factorial, a selective floral defence manipulation and a linked public-data panel each exist, but largely in different studies. The empirical gap is therefore not absence of relevant biology but fragmentation of the information needed to allocate a joint interaction and to establish the strongest outcome claim."
    )
    new_conclusion = (
        "The four constituent ecological pathway families recur across independent systems, while the 17-system high-information audit shows that complementary experimental faces already exist but largely in different studies: a direct trait factorial, an attraction-by-antagonist-removal-by-pollination-supplementation bridge, a consumer factorial, a selective floral defence manipulation and a linked public-data panel. The empirical gap is therefore not absence of relevant biology but fragmentation of the information needed to allocate a joint interaction and to establish the strongest outcome claim."
    )
    text = replace_once(text, old_conclusion, new_conclusion, label="conclusion frontier synthesis")

    text = replace_once(
        text,
        "and Sun and Huang (2015).",
        "Sun and Huang (2015), and Theis and Adler (2012).",
        label="main reference prose",
    )

    MAN.write_text(text, encoding="utf-8")


def promote_supplement() -> None:
    text = SUPP.read_text(encoding="utf-8")
    text = replace_once(text, "The current matrix contains 16 systems. Fixed conclusions are:", "The current matrix contains 17 systems. Fixed conclusions are:", label="supplement count")
    text = replace_once(
        text,
        "closest full A×D-like trait factorial:      Kessler et al. 2008\nclosest crossed G×P-like consumer factorial: Egan et al. 2021\nindependent kappa assay:                    0\nfull rho/iota/kappa identification:         0",
        "closest full A×D-like trait factorial:      Kessler et al. 2008\nA×G×pollination-supplementation bridge:     Theis & Adler 2012\nclosest crossed G×P-like consumer factorial: Egan et al. 2021\nindependent kappa assay:                    0/17\nfull rho/iota/kappa identification:         0/17",
        label="supplement fixed coverage",
    )
    text = replace_once(text, "empirical/identification_design/HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv", "empirical/identification_design/HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V2.csv", label="supplement authoritative table")
    text = replace_once(
        text,
        "8. **One dual-function chemical trait rather than two axes** — Gronquist et al. 2001.",
        "8. **One dual-function chemical trait rather than two axes** — Gronquist et al. 2001.\n9. **Manipulated attraction × antagonist removal × pollination supplementation without D or true P-access** — Theis & Adler 2012.",
        label="supplement Theis class",
    )
    SUPP.write_text(text, encoding="utf-8")


def promote_refs() -> None:
    text = REFS.read_text(encoding="utf-8")
    if "Theis N" not in text:
        text = text.rstrip() + "\n\nTheis N, Adler LS (2012) Advertising to the enemy: enhanced floral fragrance increases beetle attraction and reduces plant reproduction. *Ecology* 93:430–435. https://doi.org/10.1890/11-0825.1\n"
    REFS.write_text(text, encoding="utf-8")


def promote_figure_contract() -> None:
    text = FIG_BUILDER.read_text(encoding="utf-8")
    text = replace_once(text, 'HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv', 'HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V2.csv', label="figure coverage source")
    FIG_BUILDER.write_text(text, encoding="utf-8")

    test = FIG_TEST.read_text(encoding="utf-8")
    test = replace_once(test, 'assert len(_read_coverage()) == 16', 'rows = _read_coverage()\n    assert len(rows) == 17\n    assert any(row["study_id"] == "Theis_Adler_2012_Cucurbita" for row in rows)', label="figure test count")
    test = replace_once(test, 'assert "All eight target intervals cross zero" in texts[3]', 'assert "17-system audit" in texts[3]\n    assert "All eight target intervals cross zero" in texts[3]', label="figure test rendered count")
    FIG_TEST.write_text(test, encoding="utf-8")


def promote_te_package() -> None:
    text = TE_BUILDER.read_text(encoding="utf-8")
    text = replace_once(text, '("HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv", "high_information_identification_coverage.csv")', '("HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V2.csv", "high_information_identification_coverage.csv")', label="TE open-research coverage")
    TE_BUILDER.write_text(text, encoding="utf-8")

    test = TE_TEST.read_text(encoding="utf-8")
    anchor = 'assert "strict reversal" in text\n'
    if 'assert "17 screened high-information systems" in text' not in test:
        test = replace_once(test, anchor, anchor + '    assert "17 screened high-information systems" in text\n    assert "Theis and Adler (2012)" in text\n', label="TE generated manuscript frontier test")
    TE_TEST.write_text(test, encoding="utf-8")


def main() -> None:
    promote_manuscript()
    promote_supplement()
    promote_refs()
    promote_figure_contract()
    promote_te_package()


if __name__ == "__main__":
    main()
