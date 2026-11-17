"""Original-source gated Pineau et al. 2024 forward divergence evidence readout.

Scope: ONE independent snowflake yeast evolution programme, 5 biological
aerobic evolution lines, not isolated clusters or 8 competition assays.
Numerical size ratios and evolved-line success classifications are from
the publication's prose/Extended Data Figure 1, *not* re-extracted from
the author's binary XLSX (currently unavailable via text-only connector).

Recompute code-derived competition equilibrium directly from the
author GitHub F2.m, pinned by a Git-blob SHA-1.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

DOI = "10.1038/s41559-024-02367-y"
PMCID = "PMC11090753"
AUTHOR_REPO_COMMIT = "071affa79f16f0a469f099058372a7488c35c0c2"
AUTHOR_F2_GIT_BLOB_SHA1 = "4b5dba14b244b335294ca28be52a77c5dc278d79"
PUBLISHED_SOURCE_URL = "https://www.nature.com/articles/s41559-024-02367-y"
ARTICLE_JATS_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11090753/fullTextXML"
AUTHOR_F2_URL = (
    "https://raw.githubusercontent.com/Ratcliff-Lab/coexistence-paper/"
    + AUTHOR_REPO_COMMIT + "/F2.m"
)
AUTHOR_XLSX_REPO_PATH = "data_used_to_generate_figs_in_coexistence_paper.xlsx"
AUTHOR_XLSX_GIT_BLOB_SHA1 = "8f7d01b388489374aba210db96495f387d4338e2"
PO_LINE_VOLUMES = (("PO-1", 2.0), ("PO-2", 1.5), ("PO-3", 37.0),
                   ("PO-4", 27.0), ("PO-5", 16.0))
ORIGINAL_AUTHOR_POSITIVE_LINE_IDS = ("PO-3", "PO-4", "PO-5")


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\\0" + raw).hexdigest()


def check_article_jats(xml: bytes) -> dict:
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        raise ValueError("source article is not valid JATS XML") from e
    doi_ids = {n.text.strip() for n in root.iter()
               if n.tag.rsplit("}", 1)[-1] == "article-id"
               and n.attrib.get("pub-id-type") == "doi" and n.text}
    if DOI not in doi_ids:
        raise ValueError("publisher article DOI is not the expected Pineau source")
    plain = " ".join(" ".join(root.itertext()).split())
    low = plain.lower()
    for phrase in ("emergence and maintenance of stable coexistence",
                   "715", "po-3", "po-4", "po-5", "oxygen",
                   "small", "large"):
        if phrase not in low:
            raise ValueError(f"article text misses required provenance token: {phrase}")
    # Fail-closed on the *published experimental design*, rather than
    # asserting generalization across independently published programmes.
    if not (re.search(r"three (?:out of |of )five populations", low)
            or re.search(r"3 (?:out of |of )5 populations", low)
            or re.search(r"three of five", low)):
        raise ValueError("unable to verify 3/5 PO original line result in full text")
    return {
        "publisher_doi": DOI,
        "jats_article_pmcid": PMCID,
        "jats_sha256": hashlib.sha256(xml).hexdigest(),
        "article_doi_source_gate": True,
        "three_of_five_source_text_gate": True,
        "full_author_manuscript_text_not_primary_raw_xlsx": True,
    }


def author_source_fit(mcode: bytes) -> dict:
    if git_blob_sha1(mcode) != AUTHOR_F2_GIT_BLOB_SHA1:
        raise ValueError("author original F2.m Git blob changed")
    code = mcode.decode("utf-8")
    expression = re.search(
        r"plot\\(freq_at_start\\(idx\\),\\s*([0-9.]+)\\s*-\\s*"
        r"([0-9.]+)\\.\\*freq_at_start\\(idx\\)", code
    )
    if not expression:
        raise ValueError("source F2.m Large frequency-change fit missing")
    intercept, slope = (float(v) for v in expression.groups())
    if (intercept, slope) != (0.095083, 1.0274):
        raise ValueError("author's frozen fitted competition coefficients changed")
    if not 0 < intercept / slope < 1:
        raise ValueError("source code predicts invalid composition equilibrium")
    loops = [int(x) for x in re.findall(r"for\\s+i\\s*=\\s*1:(\\d+)", code)]
    if loops[:2] != [8, 7]:
        raise ValueError("author code standard/high O2 plotted-series gate changed")
    if "data_used_to_generate_figs_in_coexistence_paper.xlsx" not in code:
        raise ValueError("Figure 2 depends on uninspected original workbook")
    return {
        "author_f2_git_blob_sha1": AUTHOR_F2_GIT_BLOB_SHA1,
        "author_f2_sha256": hashlib.sha256(mcode).hexdigest(),
        "source_code_fitted_large_delta_intercept": intercept,
        "source_code_fitted_large_delta_slope": -slope,
        "equilibrium_large_fraction_recovered_from_fit": intercept / slope,
        "original_standard_O2_competition_code_series": loops[0],
        "original_high_O2_competition_code_series": loops[1],
        "publisher_high_O2_figure_caption_n": 6,
        "publisher_high_O2_methods_describes_5_initial_populations": True,
        "high_O2_count_discrepancy_unresolved": True,
        "code_assays_in_one_PO_4_isolate_pair_not_evolution_independent_origins": True,
    }


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if not (isinstance(k, int) and isinstance(n, int) and 0 <= k <= n and n > 0):
        raise ValueError("n must count started evolution lines and k positive lines")
    p = k/n
    den = 1 + z*z/n
    center = (p + z*z/(2*n)) / den
    half = z/den * math.sqrt(p*(1-p)/n+z*z/(4*n*n))
    return (center-half, center+half)


def build(article_xml: bytes, f2_code: bytes) -> dict:
    article = check_article_jats(article_xml)
    fit = author_source_fit(f2_code)
    line = []
    for label, ratio in PO_LINE_VOLUMES:
        positive = label in ORIGINAL_AUTHOR_POSITIVE_LINE_IDS
        line.append({
            "evolved_population": label,
            "published_large_vs_small_isolate_volume_fold": ratio,
            "authors_endpoint_phenotypically_dimorphic": positive,
            "source_scope": "t715 original authors' long-term aerobic evolved population",
        })
    k = sum(x["authors_endpoint_phenotypically_dimorphic"] for x in line)
    if len(line) != 5 or k != 3:
        raise ValueError("published five-line evolutionary denominator changed")
    if [x["evolved_population"] for x in line if x["authors_endpoint_phenotypically_dimorphic"]] != list(ORIGINAL_AUTHOR_POSITIVE_LINE_IDS):
        raise ValueError("published successful population IDs changed")
    ci = wilson(k, len(line))
    return {
        "publication": {"doi": DOI, "primary_article": PUBLISHED_SOURCE_URL,
            "article_full_text": ARTICLE_JATS_URL,
            "author_repo": "Ratcliff-Lab/coexistence-paper",
            "author_repo_commit": AUTHOR_REPO_COMMIT,
            "author_original_xlsx_path": AUTHOR_XLSX_REPO_PATH,
            "author_original_xlsx_git_blob_sha1": AUTHOR_XLSX_GIT_BLOB_SHA1},
        "source_audit": {"jats": article, "figure2_code_fit": fit},
        "single_evolution_programme": {
            "independent_initial_aerobic_populations": 5,
            "original_common_ancestor": "engineered ACE2-deleted snowflake yeast",
            "evolution_treatment": "obligately_aerobic_glycerol_with_growth_and_settling",
            "daily_transfers": 715,
            "estimated_generations": 4300,
            "sampled_small_and_large_isolates_per_evolution_population": 20,
            "line_specific_outcomes_from_published_article": line,
            "authors_dimorphism_successes": k,
            "authors_dimorphism_failures": 5-k,
            "reported_observed_fraction": k/5,
            "descriptive_wilson_95pct_interval": list(ci),
            "is_a_general_species_level_diversification_probability": False,
            "independent_programme_count": 1,
        },
        "mechanism_and_maintenance": {
            "representative_focal_fitness_pair": "PO-4 Small versus PO-4 Large only",
            "size_based_growth_survival_tradeoff": True,
            "negative_frequency_dependence_demonstrated_within_PO4_pair": True,
            "source_fitted_large_fraction_approx": fit["equilibrium_large_fraction_recovered_from_fit"],
            "source_article_standard_O2_large_fraction_approx": 0.09,
            "source_article_high_O2_large_fraction_approx": 0.86,
            "standard_O2_percent_atmospheric_level_approx": 26,
            "high_O2_percent_atmospheric_level_approx": 84,
            "high_O2_fraction_difference_descriptive_from_rounded_publisher_values": 0.86-0.09,
            "PO3_small_large_genomes_nonshared_mutations_reported": True,
            "t715_lineage_sequence_from_every_founder_population": False,
            "oxygen_intervention_tests_retention_not_de_novo_origin": True,
        },
        "comparability_and_scope": {
            "other_metabolic_treatments_have_5_populations_each": True,
            "PM_PA_715_individual_endpoint_screen_equal_to_PO_not_source_verified": True,
            "no_primary_cross_treatment_risk_ratio_or_fisher_test": True,
            "source_authors_report_no_size_dimorphism_in_PA_PM_context": True,
            "source_figure_workbook_binary_not_reanalyzed": True,
            "reconstruction_from_article_and_author_source_code_only": True,
            "not_20_independent_evolution_origin_replicates_per_population": True,
            "not_8_independent_evolution_origin_replicates_from_competition_tests": True,
            "high_O2_n_discrepancy_unresolved": True,
            "genotype_level_architecture_module_duplication_not_identified": True,
            "no_Ku_or_fitness_invasion_coefficient_calibrated": True,
            "no_evolution_programme_meta_analysis_performed": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jats", type=Path, required=True)
    parser.add_argument("--f2", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.jats.read_bytes(), args.f2.read_bytes())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False,
                                       allow_nan=False)+"\\n", encoding="utf8")
    print("BITA_PINEAU_ORIGINAL_SOURCE_REPRO:" + json.dumps({
        "jats_sha256": result["source_audit"]["jats"]["jats_sha256"],
        "f2_git_sha1": result["source_audit"]["figure2_code_fit"]["author_f2_git_blob_sha1"],
        "evolved_populations": result["single_evolution_programme"]["independent_initial_aerobic_populations"],
        "positive": result["single_evolution_programme"]["authors_dimorphism_successes"],
        "fraction_CI": result["single_evolution_programme"]["descriptive_wilson_95pct_interval"],
        "source_code_equilibrium": result["source_audit"]["figure2_code_fit"]["equilibrium_large_fraction_recovered_from_fit"],
        "high_O2_source_n_discrepancy": result["source_audit"]["figure2_code_fit"]["high_O2_count_discrepancy_unresolved"],
    }, separators=(",",":")))


if __name__ == "__main__":
    main()
