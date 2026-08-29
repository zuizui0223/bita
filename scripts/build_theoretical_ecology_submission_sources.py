from __future__ import annotations

import json
from pathlib import Path
import re
import shutil

import build_identification_candidate_package_sources as candidate


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_IDENTIFICATION_DESIGN.md"
COVER_LETTER = ROOT / "submission" / "COVER_LETTER_THEORETICAL_ECOLOGY.md"
OUT = ROOT / "submission" / "theoretical_ecology" / "generated"
DATA_OUT = OUT / "open_research_data"
FIG_OUT = OUT / "figures"

TARGET_TITLE = "From floral trait interactions to mechanism identification: a crossed-intervention framework for attraction and defence"
TARGET_ABSTRACT = (
    "Trait interactions can be measured without identifying the ecological pathways that generate them. "
    "We use floral attraction and defence to develop an experimental identification framework for this problem. "
    "The primary estimand is the measurable two-level interaction Delta_AD W = W11 - W10 - W01 + W00. "
    "A total interaction defines an identified set of compatible antagonist-relief, pollinator-interference and remaining joint-channel allocations rather than a unique mechanism. "
    "Explicit bounds or channel measurements shrink that set, while a crossed attraction × defence × antagonist × pollinator design can allocate the biotic channels when interventions are selective and a four-way separability diagnostic is satisfied. "
    "An independent assay is required before the remaining residual is interpreted as joint cost. "
    "Published systems locate different points on this identification sequence. Kessler et al. (2008) supplies a manipulated attraction-by-defence-like field factorial whose published female-outcrossing summaries retain a positive aggregate interaction sign under registered sensitivity analysis, but source/design-based interaction uncertainty remains unresolved. "
    "A public Impatiens capensis reanalysis supplies uncertainty-bearing observational interactions whose intervals cross zero. "
    "We therefore separate deciding whether complementarity occurs from explaining why it occurs, and provide a staged prospective programme in which a four-cell Stage-1 experiment identifies the total sign before channel-specific pilot data are used to power a full mechanism experiment."
)
TARGET_KEYWORDS = (
    "causal identification",
    "factorial experiment",
    "floral defence",
    "florivory",
    "pollination",
    "trait interaction",
)


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w][\w'’-]*\b", text, flags=re.UNICODE))


def _strip_old_backmatter(pre_refs: str) -> str:
    pattern = re.compile(
        r"\n\n## Author contributions, funding, acknowledgments and competing interests\n\n"
        r"\[Author-controlled; complete before submission\.\]\s*$",
        flags=re.S,
    )
    return pattern.sub("", pre_refs).rstrip()


def _replace_abstract_and_keywords(text: str) -> str:
    if "## Abstract" not in text or "**Keywords:**" not in text:
        raise RuntimeError("canonical manuscript lacks Abstract/Keywords markers")
    before, after = text.split("## Abstract", 1)
    abstract_body, after_keywords_marker = after.split("**Keywords:**", 1)
    # Preserve everything after the existing keyword line beginning at the next section.
    match = re.search(r"\n\n## 1\. Introduction", after_keywords_marker)
    if match is None:
        raise RuntimeError("cannot locate Introduction after keyword line")
    remainder = after_keywords_marker[match.start():]
    keywords = "; ".join(TARGET_KEYWORDS)
    return (
        before.rstrip()
        + "\n\n## Abstract\n\n"
        + TARGET_ABSTRACT
        + "\n\n**Keywords:** "
        + keywords
        + remainder
    )


def _statements_and_declarations() -> str:
    return """## Statements and Declarations

### Funding

[Author-controlled; insert funding statement or confirmed no-funding statement before submission.]

### Competing Interests

[Author-controlled; insert the all-author approved financial and non-financial competing-interest statement before submission.]

### Author Contributions

[Author-controlled; insert the all-author approved contribution statement before submission.]

### Data and code availability

Review-stage code, derived evidence ledgers, registered analysis receipts and public-data reanalysis products are maintained in the project repository. The exact accepted data/code version will be deposited in a permanent versioned archive and cited in the final article. Publisher full texts and other copyrighted source files are not redistributed.
"""


def build_main_source() -> str:
    canonical = MANUSCRIPT.read_text(encoding="utf-8").strip()
    if not canonical.startswith(f"# {TARGET_TITLE}"):
        raise RuntimeError("canonical manuscript title does not match Theoretical Ecology target title")
    canonical = _replace_abstract_and_keywords(canonical)
    pre_refs = canonical.split("## References", 1)[0].rstrip()
    pre_refs = _strip_old_backmatter(pre_refs)

    refs = candidate._focused_reference_text()
    captions = candidate._figure_captions()

    figures: list[str] = []
    for idx, caption in enumerate(captions, 1):
        figures.append(
            f"{caption}\n\n"
            f"![](../../../manuscript/identification_figures/FIGURE_{idx}_IDENTIFICATION_DESIGN.svg)"
        )

    journal_header = "**Journal:** Theoretical Ecology\n\n**Article type:** Regular Article"
    # Keep the canonical title-page placeholders, but make the target/article type explicit.
    first_heading_end = pre_refs.find("\n")
    pre_refs = (
        pre_refs[:first_heading_end]
        + "\n\n"
        + journal_header
        + pre_refs[first_heading_end:]
    )

    return (
        pre_refs
        + "\n\n## References\n\n"
        + refs
        + "\n\n"
        + _statements_and_declarations().strip()
        + "\n\n## Figures\n\n"
        + "\n\n".join(figures)
        + "\n"
    )


def build_supplement_source() -> str:
    text = candidate.build_supplement_source()
    text = text.replace("**Journal:** Ecology", "**Journal:** Theoretical Ecology")
    text = text.replace("../../../../manuscript/", "../../../manuscript/")
    text = text.replace("# Appendix S1 — Identification design", "# Online Resource 1 — Identification design")
    return text


def copy_open_research_data() -> list[dict[str, str]]:
    DATA_OUT.mkdir(parents=True, exist_ok=True)
    sources = [
        ("HIGH_INFORMATION_IDENTIFICATION_COVERAGE_V1.csv", "high_information_identification_coverage.csv"),
        ("DEFENCE_ESCAPE_ROUTE_HYPOTHESIS_RECOVERY_V1.csv", "defence_escape_route_hypothesis_recovery.csv"),
        ("IMPATIENS_2018_IDENTIFICATION_RETROFIT_V1.json", "impatiens_identification_retrofit.json"),
        ("KESSLER_TYPE_REPLICATION_POWER_V1.json", "kessler_type_replication_power.json"),
        ("KESSLER_TYPE_STAGE1_TRIAL_TEMPLATE_V1.csv", "kessler_type_stage1_trial_template.csv"),
    ]
    copied: list[dict[str, str]] = []
    for source_name, target_name in sources:
        src = ROOT / "empirical" / "identification_design" / source_name
        if not src.exists():
            raise RuntimeError(f"missing required open-research source: {src}")
        dst = DATA_OUT / target_name
        shutil.copyfile(src, dst)
        copied.append({"source": str(src.relative_to(ROOT)), "package_file": target_name})
    return copied


def copy_figures() -> list[str]:
    FIG_OUT.mkdir(parents=True, exist_ok=True)
    names: list[str] = []
    for idx in range(1, 6):
        src = ROOT / "manuscript" / "identification_figures" / f"FIGURE_{idx}_IDENTIFICATION_DESIGN.svg"
        if not src.exists():
            raise RuntimeError(f"missing identification figure: {src}")
        dst = FIG_OUT / f"Fig{idx}.svg"
        shutil.copyfile(src, dst)
        names.append(dst.name)
    return names


def _extract_title(source: str) -> str:
    first = source.splitlines()[0]
    return first.removeprefix("# ").strip()


def _cover_letter_reviewer_placeholders() -> int:
    text = COVER_LETTER.read_text(encoding="utf-8")
    return len(re.findall(r"^\d+\. \[Name — institution — e-mail — expertise — conflict check\]$", text, flags=re.M))


def build_qa_receipt(main_source: str, copied_data: list[dict[str, str]], figures: list[str]) -> dict[str, object]:
    title = _extract_title(main_source)
    refs_pos = main_source.find("## References")
    declarations_pos = main_source.find("## Statements and Declarations")
    methods_ai = "AI-assisted workflow transparency" in main_source or "AI-assisted workflow" in main_source
    abstract_words = word_count(TARGET_ABSTRACT)
    keyword_count = len(TARGET_KEYWORDS)
    cover_text = COVER_LETTER.read_text(encoding="utf-8")
    title_matches_cover = f"**“{title},”**" in cover_text
    reviewer_slots = _cover_letter_reviewer_placeholders()

    automated = {
        "journal_is_theoretical_ecology": "**Journal:** Theoretical Ecology" in main_source,
        "article_type_regular_article": "**Article type:** Regular Article" in main_source,
        "abstract_150_to_250_words": 150 <= abstract_words <= 250,
        "keywords_4_to_6": 4 <= keyword_count <= 6,
        "cover_title_matches": title_matches_cover,
        "five_reviewer_placeholders": reviewer_slots == 5,
        "ai_disclosure_present": methods_ai,
        "declarations_after_references": refs_pos >= 0 and declarations_pos > refs_pos,
        "funding_heading_present": "### Funding" in main_source,
        "competing_interests_heading_present": "### Competing Interests" in main_source,
        "author_contributions_heading_present": "### Author Contributions" in main_source,
        "data_code_heading_present": "### Data and code availability" in main_source,
        "five_identification_figures_present": len(figures) == 5,
        "no_ecology_page_limit_rule": "30_PAGE" not in main_source and "Concepts & Synthesis" not in main_source,
    }
    return {
        "analysis_id": "theoretical_ecology_submission_package_v2",
        "target_journal": "Theoretical Ecology",
        "article_type": "Regular Article",
        "title": title,
        "abstract_word_count": abstract_words,
        "keyword_count": keyword_count,
        "reviewer_placeholder_count": reviewer_slots,
        "automated_gates": automated,
        "automated_status": "TECHNICALLY_READY" if all(automated.values()) else "TECHNICAL_QA_FAIL",
        "human_status": "BLOCKED_AUTHOR_METADATA",
        "human_blockers": [
            "final author names/order and affiliations",
            "corresponding-author contact and ORCIDs",
            "funding and competing-interest statements",
            "author contributions and acknowledgements",
            "repository licence and archival DOI",
            "five real conflict-checked reviewers",
            "all-author approval of exact submitted version",
        ],
        "open_research_files": copied_data,
        "figure_files": figures,
        "claim_boundary": (
            "Technical readiness does not authorize scientific overclaiming or portal submission. "
            "Kessler remains aggregate-sign-positive with source/design uncertainty unresolved; Stage 1 decides only the total A x D sign, not channel allocation."
        ),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    main_source = build_main_source()
    supplement = build_supplement_source()
    copied_data = copy_open_research_data()
    figures = copy_figures()
    (OUT / "MANUSCRIPT_THEORETICAL_ECOLOGY.md").write_text(main_source, encoding="utf-8")
    (OUT / "ONLINE_RESOURCE_1.md").write_text(supplement, encoding="utf-8")
    shutil.copyfile(COVER_LETTER, OUT / "COVER_LETTER_THEORETICAL_ECOLOGY.md")
    receipt = build_qa_receipt(main_source, copied_data, figures)
    (OUT / "PACKAGE_QA_RECEIPT.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps({"automated_status": receipt["automated_status"], "abstract_words": receipt["abstract_word_count"], "keywords": receipt["keyword_count"]}))
    if receipt["automated_status"] != "TECHNICALLY_READY":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
