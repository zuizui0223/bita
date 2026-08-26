from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
CAP = ROOT / "manuscript" / "IDENTIFICATION_DESIGN_FIGURE_CAPTIONS.md"
SUPP = ROOT / "manuscript" / "supplementary" / "SUPPLEMENT_IDENTIFICATION_DESIGN.md"
COVER = ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md"
MANIFEST = ROOT / "SUPPLEMENT_MANIFEST.md"
BUILDER = ROOT / "scripts" / "build_identification_design_figures_svg.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def patch_manuscript() -> None:
    text = MAN.read_text(encoding="utf-8")

    old = (
        "A Dryad reanalysis of *Impatiens capensis* reaches randomized context modification of an observational trait interaction but not channel identification. "
        "Across 16 screened high-information systems, no study combines the trait factorial, selective consumer interventions, pollinator-independent baseline characterization, and an independent joint-cost assay. "
        "The main empirical gap is therefore not absence of interaction studies, but the missing intersection between trait-interaction estimation and mechanism allocation."
    )
    new = (
        "A Dryad reanalysis of *Impatiens capensis* reaches randomized context modification of an observational trait interaction but not channel identification. "
        "A retained source-adjudicated mechanism-route synthesis shows that the four constituent marginal pathways recur across 56 route records from 25 independent biological clusters; those records establish biological recurrence, not estimates of the channel interactions or total attraction-by-defence interaction. "
        "Across 16 screened high-information systems, no study combines the trait factorial, selective consumer interventions, pollinator-independent baseline characterization, and an independent joint-cost assay. "
        "The main empirical gap is therefore not absence of the constituent biology, but the missing intersection between recurrent ecological pathways and an experiment that allocates their joint interaction."
    )
    text = replace_once(text, old, new, "abstract mechanism-pattern bridge")

    intro_anchor = (
        "These examples reveal a consistent gap: trait-interaction estimation and mechanism allocation have usually been achieved in different experiments."
    )
    intro_insert = intro_anchor + (
        "\n\nWe therefore use existing evidence in two empirical layers. First, the retained source-adjudicated mechanism-route synthesis asks whether the four marginal pathways required by the decomposition—attraction to pollination, attraction to antagonism, defence to antagonism, and defence to pollination—recur across independent biological systems. Second, a stricter identification-coverage audit asks whether those recurrent ingredients have been crossed on the same attraction and defence coordinates with selective consumer interventions and an independent joint-cost assay. This preserves the original Mechanism → Pattern logic while preventing marginal recurrence from being relabelled as channel identification."
    )
    text = replace_once(text, intro_anchor, intro_insert, "introduction bridge")

    old_section = "## 4. How close do existing studies come?\n\n### 4.1 Identification-coverage audit"
    new_section = """## 4. From mechanism to pattern: recurrence before identification

### 4.1 Constituent ecological channels recur across systems

The identification problem would be biologically uninteresting if the proposed channels were peculiar to a single model system. The retained source-adjudicated mechanism-route synthesis instead contains 56 directional route records from 25 independent biological study clusters. Coverage includes attraction → pollination in 5 clusters, attraction → antagonism in 8, defence → antagonism in 18, and defence → pollination in 10. Fourteen clusters contain more than one route in the same biological system, and 17 show context- or state-dependent switching. These categories overlap: route counts are not additive independent-study totals, and none of these counts is an estimate of natural prevalence.

The conclusion is deliberately limited. The constituent ecological ingredients required by the channel decomposition recur across systems, so the framework is not built around one exceptional case. But marginal route recurrence does not estimate \\(\\Delta_{AD}W\\), \\(\\rho_\\Delta\\), \\(\\iota_\\Delta\\), or \\(\\kappa_\\Delta\\). The Mechanism → Pattern bridge is therefore two-stage: first establish recurrence of the biological channels; then ask whether any existing experiment jointly identifies their allocation on the same attraction-by-defence contrast.

### 4.2 Identification-coverage audit"""
    text = replace_once(text, old_section, new_section, "section 4 mechanism-pattern bridge")

    for old_h, new_h in (
        ("### 4.5 Other informative near misses", "### 4.6 Other informative near misses"),
        ("### 4.4 Public-data retrofit: Soper Gorden and Adler 2018", "### 4.5 Public-data retrofit: Soper Gorden and Adler 2018"),
        ("### 4.3 A consumer-factorial counterpart: Egan et al. 2021", "### 4.4 A consumer-factorial counterpart: Egan et al. 2021"),
        ("### 4.2 A trait-factorial anchor: Kessler et al. 2008", "### 4.3 A trait-factorial anchor: Kessler et al. 2008"),
    ):
        text = replace_once(text, old_h, new_h, f"renumber {old_h}")

    old_disc = (
        "### 6.1 The gap is mechanism allocation, not interaction detection\n\n"
        "The strongest conclusion from the reanalysis and coverage audit is narrower and more useful than the claim that attraction–defence interactions are understudied. Ecologists already manipulate floral traits, pollination and antagonists in sophisticated experiments. Kessler et al. (2008) shows that a direct attraction-by-defence-like trait factorial can be built in the field. Egan et al. (2021) shows that pollination and herbivory can be crossed to estimate context-dependent selection. What is rare in the screened evidence is the intersection of these designs on the same trait coordinates and outcome scale."
    )
    new_disc = (
        "### 6.1 Constituent mechanisms recur; mechanism allocation remains missing\n\n"
        "The strongest conclusion from the reanalysis and coverage audit is narrower and more useful than the claim that attraction–defence biology is understudied. The retained route synthesis shows that the four constituent marginal pathways recur across 25 independent biological clusters, including same-system and context-switching architectures. Ecologists also manipulate floral traits, pollination and antagonists in sophisticated experiments. Kessler et al. (2008) shows that a direct attraction-by-defence-like trait factorial can be built in the field, whereas Egan et al. (2021) shows that pollination and herbivory can be crossed to estimate context-dependent selection. What remains rare in the screened evidence is the intersection of these recurrent biological channels and these experimental design components on the same trait coordinates and outcome scale."
    )
    text = replace_once(text, old_disc, new_disc, "discussion bridge")

    old_conc = (
        "Existing high-information studies already contain important pieces of this design. A direct trait factorial, a consumer factorial, a selective floral defence manipulation and a linked public-data panel each exist, but in different studies. The empirical opportunity is therefore concrete: combine those pieces in one system. The resulting experiment would move floral attraction–defence research from detecting non-additivity to identifying why that non-additivity occurs."
    )
    new_conc = (
        "The four constituent ecological pathway families also recur across independent systems, while high-information studies already contain important pieces of the required identification design. A direct trait factorial, a consumer factorial, a selective floral defence manipulation and a linked public-data panel each exist, but largely in different studies. The empirical opportunity is therefore concrete: combine recurrent biological ingredients and the currently separated design pieces in one system. The resulting experiment would move floral attraction–defence research from detecting non-additivity and cataloguing marginal pathways to identifying why that non-additivity occurs."
    )
    text = replace_once(text, old_conc, new_conc, "conclusion bridge")

    MAN.write_text(text, encoding="utf-8")


def patch_captions() -> None:
    text = CAP.read_text(encoding="utf-8")
    old = (
        "**Figure 4. Existing studies occupy complementary parts of the identification design.** Kessler et al. (2008) is the closest trait-factorial anchor, experimentally crossing floral benzylacetone and nicotine; Egan et al. (2021) supplies the complementary consumer-factorial structure by crossing herbivory and pollination. The lower panel shows the *Impatiens capensis* retrofit: the observational `A×D` term and its randomized robbing, florivory, and pollination modifiers are estimable, but all eight target 95% intervals cross zero. Across 16 screened high-information systems, independent joint-cost assays and full channel identification are absent. Counts describe this screened set, not literature prevalence."
    )
    new = (
        "**Figure 4. Constituent ecological channels recur, but mechanism allocation remains unidentified.** The retained mechanism-route synthesis contains 56 route records across 25 independent biological clusters and covers all four marginal pathway families; these overlapping counts demonstrate recurrence rather than channel-interaction identification or natural prevalence. Kessler et al. (2008) is the closest trait-factorial anchor, whereas Egan et al. (2021) supplies the complementary consumer-factorial structure. The lower panel shows the *Impatiens capensis* retrofit: the observational `A×D` term and its randomized robbing, florivory, and pollination modifiers are estimable, but all eight target 95% intervals cross zero. Across 16 screened high-information systems, independent joint-cost assays and full channel identification are absent."
    )
    CAP.write_text(replace_once(text, old, new, "Figure 4 caption"), encoding="utf-8")


def patch_supplement() -> None:
    text = SUPP.read_text(encoding="utf-8")
    old = """## S5. Broader mechanism-route evidence retained as background

The earlier mechanism-pattern synthesis contains 56 source-adjudicated route records from 25 independent biological study clusters, including 14 same-system multi-route clusters and 17 context/sign-switch clusters. These records remain useful for demonstrating that attraction, pollination, antagonism and defence pathways recur in nature.

They are not used in the identification manuscript as estimates of `rho_delta`, `iota_delta`, `Delta_AD W`, or `kappa_delta`. Marginal `A→pollination`, `A→antagonism`, `D→antagonism`, and `D→pollination` evidence does not estimate a cross-trait channel interaction. The full route ledger therefore moves from the old Main argument to supplementary/background evidence."""
    new = """## S5. Constituent mechanism recurrence supporting the Main Pattern layer

The mechanism-pattern synthesis contains 56 source-adjudicated route records from 25 independent biological study clusters: `A→pollination` occurs in 5 clusters, `A→antagonism` in 8, `D→antagonism` in 18, and `D→pollination` in 10. Fourteen clusters contain same-system multi-route evidence and 17 contain context/sign-switch evidence. These overlapping classifications demonstrate that attraction, pollination, antagonism and defence pathways recur across biological systems; they are not additive study counts or natural-prevalence estimates.

The Main manuscript now uses this synthesis only for that recurrence claim. It does not use the route records as estimates of `rho_delta`, `iota_delta`, `Delta_AD W`, or `kappa_delta`. Marginal `A→pollination`, `A→antagonism`, `D→antagonism`, and `D→pollination` evidence does not estimate a cross-trait channel interaction. Full source-level details remain here and in the machine-readable route ledger so that the Mechanism → Pattern bridge is explicit without collapsing recurrence into identification."""
    SUPP.write_text(replace_once(text, old, new, "Supplement S5"), encoding="utf-8")


def patch_cover() -> None:
    text = COVER.read_text(encoding="utf-8")
    anchor = (
        "The simple algebra linking total interaction and channel contrasts is deliberately not presented as the novelty. Its role is diagnostic after the relevant contrasts have been measured. For example, observed complementarity together with antagonist relief no greater than pollinator interference forces a negative remaining joint channel on the declared scale; attributing that channel specifically to joint cost still requires the independent assay."
    )
    insert = anchor + (
        "\n\nThe cross-system synthesis provides a separate Pattern layer rather than validation of that algebra. Across 56 source-adjudicated route records from 25 independent biological clusters, all four constituent marginal pathway families recur, including same-system and context-switching architectures. We use this result only to establish that the biological ingredients of the decomposition recur across systems; the route records do not estimate `rho_delta`, `iota_delta`, `Delta_AD W`, or `kappa_delta`. The stricter identification audit then asks whether those recurrent ingredients have ever been jointly crossed in one experiment."
    )
    COVER.write_text(replace_once(text, anchor, insert, "cover bridge"), encoding="utf-8")


def patch_manifest() -> None:
    text = MANIFEST.read_text(encoding="utf-8")
    old = """## 7. Historical Mechanism → Pattern provenance retained

The previous synthesis remains available as a provenance layer:"""
    new = """## 7. Mechanism → Pattern recurrence layer retained in the Main argument

The previous synthesis is now reused in a deliberately bounded role: it establishes cross-system recurrence of the constituent ecological pathways before the stricter identification-coverage audit. It does not validate the algebra or identify the channel interactions. Full provenance remains available:"""
    text = replace_once(text, old, new, "manifest section 7 heading")
    old2 = "These overlapping counts are not added as independent-study prevalence and no longer constitute the Main empirical endpoint."
    new2 = "These overlapping counts are not added as independent-study prevalence. Their Main-text role is limited to constituent-channel recurrence; the empirical endpoint remains whether recurrent pathways are jointly identified on common attraction-by-defence coordinates."
    text = replace_once(text, old2, new2, "manifest section 7 boundary")
    MANIFEST.write_text(text, encoding="utf-8")


def patch_builder() -> None:
    text = BUILDER.read_text(encoding="utf-8")
    old_const = 'IMPATIENS = ROOT / "empirical" / "identification_design" / "IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json"'
    new_const = old_const + '\nPATTERN_STATUS = ROOT / "empirical" / "mechanism_pattern_synthesis" / "COMPLETION_STATUS_V2.md"'
    text = replace_once(text, old_const, new_const, "builder pattern source")

    marker = "\ndef _xscale(value: float, x0: float=600, lo: float=-1.8, hi: float=1.3, width: float=600) -> float:\n"
    helper = '''\ndef _pattern_counts() -> dict[str, int]:
    import re
    text = PATTERN_STATUS.read_text(encoding="utf-8")
    patterns = {
        "records": r"route-ledger records:\\s+(\\d+)",
        "clusters": r"independent biological clusters:\\s+(\\d+)",
        "a_poll": r"A -> pollination clusters:\\s+(\\d+)",
        "a_ant": r"A -> antagonism clusters:\\s+(\\d+)",
        "d_ant": r"D -> antagonism clusters:\\s+(\\d+)",
        "d_poll": r"D -> pollination clusters:\\s+(\\d+)",
        "same": r"same-system multi-route clusters:\\s+(\\d+)",
        "switch": r"context/sign-switch clusters:\\s+(\\d+)",
    }
    out: dict[str, int] = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match is None:
            raise ValueError(f"Missing mechanism-pattern count {key}")
        out[key] = int(match.group(1))
    return out

'''
    text = replace_once(text, marker, helper + marker, "builder count helper")

    old_start = 'def fig4() -> str:\n    rows=_read_coverage(); targets=_impatiens_targets()\n    b=[\'<text x="650" y="42" text-anchor="middle" class="title">Existing studies occupy complementary parts of the identification design</text>\']'
    new_start = 'def fig4() -> str:\n    rows=_read_coverage(); targets=_impatiens_targets(); pattern=_pattern_counts()\n    b=[\'<text x="650" y="42" text-anchor="middle" class="title">Constituent channels recur, but mechanism allocation remains unidentified</text>\']'
    text = replace_once(text, old_start, new_start, "Figure 4 title")

    old_summary = '    b.append(f\'<text x="650" y="375" text-anchor="middle" class="body">High-information coverage matrix: {len(rows)} systems; independent κ assay = 0; full channel identification = 0</text>\')'
    new_summary = '''    b.append(f'<text x="650" y="378" text-anchor="middle" class="tiny">Mechanism Pattern: {pattern["records"]} routes / {pattern["clusters"]} clusters | A→P {pattern["a_poll"]} | A→G {pattern["a_ant"]} | D→G {pattern["d_ant"]} | D→P {pattern["d_poll"]} | same-system {pattern["same"]} | switches {pattern["switch"]}</text>')
    b.append(f'<text x="650" y="405" text-anchor="middle" class="small">Route counts overlap; recurrence ≠ channel identification | {len(rows)}-system audit: independent κ assay 0; full identification 0</text>')'''
    text = replace_once(text, old_summary, new_summary, "Figure 4 pattern summary")
    BUILDER.write_text(text, encoding="utf-8")


def main() -> None:
    patch_manuscript()
    patch_captions()
    patch_supplement()
    patch_cover()
    patch_manifest()
    patch_builder()


if __name__ == "__main__":
    main()
