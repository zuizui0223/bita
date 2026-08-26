from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAN = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
SUPP = ROOT / "manuscript" / "supplementary" / "SUPPLEMENT_IDENTIFICATION_DESIGN.md"
CAP = ROOT / "manuscript" / "IDENTIFICATION_DESIGN_FIGURE_CAPTIONS.md"
PORTAL = ROOT / "submission" / "AUTHOR_AND_PORTAL_METADATA_TEMPLATE.md"
COVER = ROOT / "submission" / "COVER_LETTER_ECOLOGY_CONCEPTS_SYNTHESIS.md"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return text.replace(old, new, 1)


def replace_section(text: str, start: str, end: str, replacement: str, label: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1:
        raise RuntimeError(f"{label}: section markers are not unique")
    a = text.index(start)
    b = text.index(end, a)
    return text[:a] + replacement.rstrip() + "\n\n" + text[b:]


def manuscript_abstract(text: str) -> str:
    return text.split("## Abstract\n\n", 1)[1].split("\n\n**Keywords:**", 1)[0].strip()


def patch_manuscript() -> None:
    text = MAN.read_text(encoding="utf-8")

    old_abs = "The algebra then diagnoses the sign of any still-unallocated joint channel rather than serving as a standalone theorem."
    new_abs = "The total interaction instead defines an identified set that additional assumptions or interventions progressively shrink before point identification."
    text = replace_once(text, old_abs, new_abs, "abstract partial identification")

    sec22 = r'''### 2.2 From non-identification to an identified set

For bookkeeping, write the reproductive outcome as

\[
W=M-G-C,
\]

where \(M\) is a mutualist-mediated contribution, \(G\) is antagonist-mediated loss, and \(C\) is a remaining direct or allocation channel. Orient the corresponding two-level channel contrasts as

\[
\rho_\Delta=-\Delta_{AD}G,\qquad
\iota_\Delta=-\Delta_{AD}M,
\]

and write \(\kappa_\Delta=\Delta_{AD}C\) as a bookkeeping coordinate whose biological interpretation still requires an independent assay. Then

\[
\Delta_{AD}W=\rho_\Delta-\iota_\Delta-\kappa_\Delta.
\]

If the observed total interaction is \(\Delta_{AD}W=\delta\), the compatible channel allocations form the identified set

\[
\mathcal I(\delta)=\{(\rho,\iota,\kappa):\rho-\iota-\kappa=\delta\}.
\]

With no additional information this is a two-dimensional plane in three-dimensional channel space. More precise measurement of the same total four-cell surface does not collapse that plane to a point; the obstacle is structural rather than sampling error. Biological restrictions or channel-specific measurements can nevertheless intersect and shrink the set, so the relevant progression is from non-identification, through partial identification, to point identification.

Positive \(\rho_\Delta\) means that defence reduces antagonist loss more strongly at high attraction than at low attraction. Positive \(\iota_\Delta\) means that defence erodes the mutualist return to attraction. The experimental problem is therefore to replace assumptions about these coordinates with contrasts that identify or bound them.'''
    text = replace_section(
        text,
        "### 2.2 Why the total interaction does not identify its channels",
        "## 3. A crossed intervention design for channel identification",
        sec22,
        "section 2.2",
    )

    sec36 = r'''### 3.6 Partial identification before point identification

The same accounting identity is useful before all channel terms have been measured. Rearranging gives

\[
\rho_\Delta-\iota_\Delta=\Delta_{AD}W+\kappa_\Delta.
\]

Thus any defensible bound on the remaining joint-cost channel maps directly to a bound on the biotic balance. In particular,

\[
\kappa_\Delta\ge0
\quad\Longrightarrow\quad
\rho_\Delta-\iota_\Delta\ge\Delta_{AD}W.
\]

If complementarity is observed, \(\Delta_{AD}W>0\), this restriction forces antagonist relief to exceed pollinator interference by at least the observed total interaction on the declared scale, even though \(\rho_\Delta\) and \(\iota_\Delta\) can remain individually unidentified. This is the useful interpretation of the earlier one-sided relation: a sharp partial-identification bound under an explicit restriction, not a standalone prediction theorem.

Additional measurements shrink the identified set. A bounded independent cost assay narrows \(\rho_\Delta-\iota_\Delta\); a selective estimate of either consumer channel narrows the remaining coordinates; and the crossed intervention design, after baseline correction and a successful separability check, point-identifies the two biotic channels. Once those channels are measured, the identity also provides a diagnostic in the opposite direction: if \(\Delta_{AD}W>0\) but \(\rho_\Delta\le\iota_\Delta\), the still-unallocated joint channel required by the data must be negative. Calling that channel \(\kappa_\Delta\) still requires the independent assay.'''
    text = replace_section(
        text,
        "### 3.6 What the simple algebra is useful for",
        "## 4. From mechanism to pattern: recurrence before identification",
        sec36,
        "section 3.6",
    )

    sec42 = r'''### 4.2 Identification-coverage audit

We reclassified a high-information set of published floral systems according to the experimental information required above. The screen was designed to expose distinct design classes, not to estimate their prevalence in the literature. For each study we asked whether \(A\) and \(D\) were distinct and biologically justified, whether they were manipulated or observed, whether a shared \(A\times D\) outcome was available, whether antagonist and pollinator interventions were crossed with the trait states, whether the pollinator-absent baseline could be characterized, and whether a joint-cost assay existed.

Sixteen high-information systems were retained. None reaches the full sequence from trait interaction to channel allocation and independent joint-cost measurement, but this is more informative than a binary 0-of-16 result. The studies occupy complementary faces of an identification frontier: some supply a trait factorial, others a consumer factorial, randomized context modification, or a selective defence mechanism. The empirical pattern is therefore **design fragmentation**. Existing studies contain different pieces of the information needed to shrink \(\mathcal I(\delta)\), but no screened system closes all dimensions of the allocation problem.

This reframes the practical question for each near miss. Rather than asking only whether a study fully identifies the mechanism, we ask which smallest additional intervention or measurement would most reduce its remaining identified set. The following systems make those missing dimensions concrete.'''
    text = replace_section(
        text,
        "### 4.2 Identification-coverage audit",
        "### 4.3 A trait-factorial anchor: Kessler et al. 2008",
        sec42,
        "section 4.2",
    )

    sec62 = r'''### 6.2 Why the algebra should be modest

The relation among \(\Delta_{AD}W\), antagonist relief, pollinator interference and a joint channel is bookkeeping, not a mathematical novelty claim. Its value is that it defines what can and cannot be learned at different information levels. A total interaction alone leaves a plane of compatible channel allocations. An explicit restriction on \(\kappa_\Delta\) partially identifies the biotic balance \(\rho_\Delta-\iota_\Delta\). Selective consumer interventions shrink the set further, and the crossed design can point-identify the biotic channels when its causal gates pass.

This interpretation also recovers the useful content of the earlier one-sided inequality without overstating it. Under \(\kappa_\Delta\ge0\), a positive total interaction implies a positive biotic balance and, more sharply, \(\rho_\Delta-\iota_\Delta\ge\Delta_{AD}W\). The statement is strong only to the extent that the cost restriction is biologically supported. An independent cost assay therefore does more than label a residual: it can convert a qualitative assumption into an empirically bounded identified set.

The broader methodological point is that ecological mechanism inference need not jump directly from non-identification to an expensive fully crossed experiment. Intermediate information can be scientifically useful when its assumptions are explicit and its effect is stated as a bound rather than a point estimate.'''
    text = replace_section(
        text,
        "### 6.2 Why the algebra should be modest",
        "### 6.3 Beyond flowers",
        sec62,
        "discussion 6.2",
    )

    sec7 = r'''## 7. Conclusions

A floral attraction-by-defence interaction can be measured without its mechanism being point-identified. The gap is not all-or-none. A total interaction defines an identified set of compatible channel allocations; biologically justified restrictions or partial channel measurements can shrink that set; and a crossed attraction-by-defence-by-antagonist-by-pollinator experiment can point-identify the consumer-mediated contrasts when selective intervention, baseline and separability requirements are met. An independent cost assay then constrains whether the remaining joint channel can be interpreted as joint cost.

The four constituent ecological pathway families recur across independent systems, while high-information studies already occupy complementary parts of this identification frontier. A direct trait factorial, a consumer factorial, a selective floral defence manipulation and a linked public-data panel each exist, but largely in different studies. The empirical gap is therefore not absence of relevant biology but fragmentation of the information needed to allocate a joint interaction. This also makes the next experiment study-specific: add the measurement or intervention that most reduces the remaining identified set rather than simply collecting another marginal association.

The resulting framework closes a three-step inference sequence: **interaction detection → partial identification → mechanism identification**. It moves floral attraction-defence research from detecting non-additivity and cataloguing recurrent pathways to stating exactly what current evidence constrains, what remains unidentified, and which additional observation would resolve it.'''
    text = replace_section(
        text,
        "## 7. Conclusions",
        "## Open Research statement",
        sec7,
        "conclusion",
    )

    MAN.write_text(text, encoding="utf-8")


def patch_supplement() -> None:
    text = SUPP.read_text(encoding="utf-8")
    marker = "Relevant existing sources:\n\n```text"
    addition = r'''### S1.1 Identified-set algebra and projection bounds

For a measured total interaction \(\Delta_{AD}W=\delta\), define

\[
\mathcal I(\delta)=\{(\rho,\iota,\kappa):\rho-\iota-\kappa=\delta\}.
\]

Suppose external knowledge or additional measurements restrict the coordinates to \(\rho\in[r_L,r_U]\), \(\iota\in[i_L,i_U]\), and \(\kappa\in[k_L,k_U]\). Intersecting the equality with these bounds gives the exact coordinate projections

\[
\rho\in[\delta+i_L+k_L,\;\delta+i_U+k_U]\cap[r_L,r_U],
\]

\[
\iota\in[r_L-k_U-\delta,\;r_U-k_L-\delta]\cap[i_L,i_U],
\]

and

\[
\kappa\in[r_L-i_U-\delta,\;r_U-i_L-\delta]\cap[k_L,k_U].
\]

The biotic balance has the especially simple projection

\[
\rho-\iota=\delta+\kappa,
\]

so any feasible cost interval \([k_L,k_U]\) maps one-to-one to

\[
\rho-\iota\in[\delta+k_L,\;\delta+k_U].
\]

Hence \(\kappa\ge0\) implies \(\rho-\iota\ge\delta\) without requiring separate sign restrictions on \(\rho\) or \(\iota\). These are structural, assumption-indexed identified sets; sampling uncertainty in \(\delta\) or in the auxiliary bounds must be propagated separately in empirical applications. The accompanying implementation is `trait_architecture/partial_identification.py`.

'''
    text = replace_once(text, marker, addition + marker, "supplement identified-set insertion")
    SUPP.write_text(text, encoding="utf-8")


def patch_captions() -> None:
    text = CAP.read_text(encoding="utf-8")
    old1 = "**Figure 1. A total attraction-by-defence interaction does not identify its mechanism.** A two-level attraction (`A`) by defence (`D`) factorial directly estimates the discrete interaction `Delta_AD W = W11 - W10 - W01 + W00` on the chosen outcome scale. The same total interaction can be generated by different allocations among antagonist relief, pollinator interference, and a remaining joint channel. The inferential problem is therefore mechanism allocation, not detection of non-additivity."
    new1 = "**Figure 1. A total attraction-by-defence interaction defines an identified set rather than a unique mechanism.** A two-level attraction (`A`) by defence (`D`) factorial directly estimates `Delta_AD W = W11 - W10 - W01 + W00`. The alternative allocations shown are examples from the set of channel combinations compatible with the same total interaction. Biological bounds or selective interventions shrink that set; the total interaction alone does not select one allocation."
    text = replace_once(text, old1, new1, "Figure 1 caption")

    old4 = "Across 16 screened high-information systems, independent joint-cost assays and full channel identification are absent."
    new4 = "Across 16 screened high-information systems, independent joint-cost assays and full channel identification are absent; the studies instead occupy complementary faces of a fragmented identification frontier."
    text = replace_once(text, old4, new4, "Figure 4 frontier caption")
    CAP.write_text(text, encoding="utf-8")


def patch_portal() -> None:
    manuscript = MAN.read_text(encoding="utf-8")
    abstract = manuscript_abstract(manuscript)
    text = PORTAL.read_text(encoding="utf-8")
    prefix, rest = text.split("### Abstract\n\n", 1)
    _, suffix = rest.split("\n\n### Keywords", 1)
    PORTAL.write_text(prefix + "### Abstract\n\n" + abstract + "\n\n### Keywords" + suffix, encoding="utf-8")


def patch_cover() -> None:
    text = COVER.read_text(encoding="utf-8")
    old = "The simple algebra linking total interaction and channel contrasts is deliberately not presented as the novelty. Its role is diagnostic after the relevant contrasts have been measured. For example, observed complementarity together with antagonist relief no greater than pollinator interference forces a negative remaining joint channel on the declared scale; attributing that channel specifically to joint cost still requires the independent assay."
    new = "The algebra is deliberately not presented as mathematical novelty. Its value is an identification ladder. A measured total interaction defines a set of compatible channel allocations; a bound on the joint-cost channel partially identifies the biotic balance; selective consumer interventions shrink the set further; and the full crossed design can point-identify the biotic channels when its causal gates pass. In particular, `kappa_delta >= 0` implies `rho_delta - iota_delta >= Delta_AD W`, recovering the earlier one-sided relation as a partial-identification bound rather than a standalone theorem."
    text = replace_once(text, old, new, "cover partial-identification paragraph")
    COVER.write_text(text, encoding="utf-8")


def main() -> None:
    patch_manuscript()
    patch_supplement()
    patch_captions()
    patch_portal()
    patch_cover()


if __name__ == "__main__":
    main()
