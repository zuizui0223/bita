"""Reproduce and dependence-audit Sasidharan et al. (2023) FVOC synthesis.

The article defines the total Table 2 unit as an unrepeated FVOC x insect-species
combination, irrespective of plant genus. Responses remain categorical. The script
persists aggregate results and anonymized publication-cluster summaries only.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import io
import json
import math
import re
import statistics
from pathlib import Path
from typing import Any, Iterable

from audit_sasidharan2023_pmc_supplement import (
    _download_package,
    _oa_package_url,
    _supplement_from_package,
)

DOI = "10.1093/aob/mcad064"
PMCID = "PMC10550281"
SHEET = "S1"
REFERENCE_COLUMN = "Reference (doi TBA)"
ELIGIBLE_GENERA = {
    "Brassica", "Cirsium", "Cucurbita", "Daucus",
    "Dichaea", "Fragaria", "Helianthus", "Nicotiana",
}
ROLES = ("Pollinator", "Florivore")
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.I)

SOURCE_DETECTION = {
    "Pollinator": {"detected": 151, "not_detected": 69},
    "Florivore": {"detected": 83, "not_detected": 19},
}
SOURCE_BEHAVIOUR = {
    "Pollinator": {"attractive": 37, "repellent": 9, "no_response": 66},
    "Florivore": {"attractive": 35, "repellent": 9, "no_response": 115},
}
SOURCE_TABLE2_GENUS_N = {
    "Brassica": {"Pollinator": {"detection": 23, "behaviour": 25}, "Florivore": {"detection": 8, "behaviour": 4}},
    "Cirsium": {"Pollinator": {"detection": 81, "behaviour": 54}, "Florivore": {"detection": 11, "behaviour": 66}},
    "Cucurbita": {"Pollinator": {"detection": 2, "behaviour": 3}, "Florivore": {"detection": 29, "behaviour": 65}},
    "Daucus": {"Pollinator": {"detection": 13, "behaviour": 3}, "Florivore": {"detection": 8, "behaviour": 0}},
    "Dichaea": {"Pollinator": {"detection": 0, "behaviour": 1}, "Florivore": {"detection": 1, "behaviour": 1}},
    "Fragaria": {"Pollinator": {"detection": 13, "behaviour": 4}, "Florivore": {"detection": 36, "behaviour": 2}},
    "Helianthus": {"Pollinator": {"detection": 54, "behaviour": 2}, "Florivore": {"detection": 1, "behaviour": 1}},
    "Nicotiana": {"Pollinator": {"detection": 50, "behaviour": 23}, "Florivore": {"detection": 10, "behaviour": 21}},
}
SOURCE_SHARED = {
    "behavioural_fvocs": 102,
    "shared_both_roles": 32,
    "shared_attractive": 8,
    "shared_repellent": 1,
}
SOURCE_SHARED_BY_GENUS = {
    "Brassica": {"behavioural_fvocs": 22, "shared_both_roles": 3, "shared_attractive": 2, "shared_repellent": 0},
    "Cirsium": {"behavioural_fvocs": 14, "shared_both_roles": 9, "shared_attractive": 3, "shared_repellent": 0},
    "Cucurbita": {"behavioural_fvocs": 31, "shared_both_roles": 3, "shared_attractive": 1, "shared_repellent": 0},
    "Daucus": {"behavioural_fvocs": 3, "shared_both_roles": 0, "shared_attractive": 0, "shared_repellent": 0},
    "Dichaea": {"behavioural_fvocs": 1, "shared_both_roles": 1, "shared_attractive": 0, "shared_repellent": 0},
    "Fragaria": {"behavioural_fvocs": 6, "shared_both_roles": 0, "shared_attractive": 0, "shared_repellent": 0},
    "Helianthus": {"behavioural_fvocs": 5, "shared_both_roles": 0, "shared_attractive": 0, "shared_repellent": 0},
    "Nicotiana": {"behavioural_fvocs": 20, "shared_both_roles": 16, "shared_attractive": 1, "shared_repellent": 1},
}


def _text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def _is_one(value: Any) -> bool:
    if isinstance(value, bool):
        return bool(value)
    if isinstance(value, (int, float)):
        return float(value) == 1.0
    return _text(value) == "1"


def _cluster_key(reference: Any) -> str:
    text = _text(reference)
    match = DOI_RE.search(text)
    if match:
        return "doi:" + match.group(0).rstrip(".,;)").lower()
    normalized = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    return "ref:" + normalized


def _anon_cluster(cluster: str) -> str:
    return "pub_" + hashlib.sha256(cluster.encode("utf-8")).hexdigest()[:12]


def _find_header(rows: Iterable[tuple[Any, ...]]) -> tuple[dict[str, int], Iterable[tuple[Any, ...]], int]:
    iterator = iter(rows)
    for absolute_row, row in enumerate(iterator, start=1):
        headers = [_text(value) for value in row]
        index = {name: i for i, name in enumerate(headers) if name}
        if {"Compound", "Genus", "Insect species", "Insect function", REFERENCE_COLUMN}.issubset(index):
            return index, iterator, absolute_row
    raise RuntimeError("could not locate S1 header")


def _chisq(table: list[list[int]], yates: bool = False) -> tuple[float, int, float]:
    rows = len(table)
    cols = len(table[0])
    row_totals = [sum(row) for row in table]
    col_totals = [sum(table[r][c] for r in range(rows)) for c in range(cols)]
    total = sum(row_totals)
    statistic = 0.0
    for r in range(rows):
        for c in range(cols):
            expected = row_totals[r] * col_totals[c] / total
            delta = abs(table[r][c] - expected)
            if yates and rows == 2 and cols == 2:
                delta = max(0.0, delta - 0.5)
            statistic += delta * delta / expected
    df = (rows - 1) * (cols - 1)
    if df == 1:
        p = math.erfc(math.sqrt(statistic / 2.0))
    elif df == 2:
        p = math.exp(-statistic / 2.0)
    else:
        raise RuntimeError("bounded reproduction only needs chi-square df 1 or 2")
    return statistic, df, p


def _two_sided_sign_p(positive: int, negative: int) -> float | None:
    n = positive + negative
    if n == 0:
        return None
    tail = min(positive, negative)
    probability = sum(math.comb(n, k) for k in range(tail + 1)) / (2**n)
    return min(1.0, 2.0 * probability)


def _median(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def _choice_label(choice: str) -> str:
    return {"+": "attractive", "-": "repellent", "0": "no_response"}[choice]


def _collapse_groups(
    rows: list[dict[str, Any]],
    include_genus: bool,
) -> tuple[dict[str, Counter[str]], dict[str, Counter[str]], dict[str, Any]]:
    groups: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        base = (row["compound"].casefold(), row["insect"].casefold(), row["role"])
        key = (row["genus"], *base) if include_genus else base
        groups[key].append(row)

    detection = {role: Counter() for role in ROLES}
    behaviour = {role: Counter() for role in ROLES}
    detection_conflicts = 0
    behaviour_conflicts = 0
    detection_units = 0
    behaviour_units = 0
    duplicate_groups = 0

    for values in groups.values():
        if len(values) > 1:
            duplicate_groups += 1
        role = values[0]["role"]
        det_states = set()
        for row in values:
            if row["physio_resp"]:
                det_states.add("detected")
            if row["physio_no_resp"]:
                det_states.add("not_detected")
        if det_states:
            detection_units += 1
            if len(det_states) == 1:
                detection[role][next(iter(det_states))] += 1
            else:
                detection_conflicts += 1

        choices = {row["behaviour"] for row in values if row["behaviour"] in {"+", "-", "0"}}
        if choices:
            behaviour_units += 1
            if len(choices) == 1:
                behaviour[role][_choice_label(next(iter(choices)))] += 1
            else:
                behaviour_conflicts += 1

    audit = {
        "group_count": len(groups),
        "duplicate_groups": duplicate_groups,
        "detection_units": detection_units,
        "behaviour_units": behaviour_units,
        "detection_conflicts": detection_conflicts,
        "behaviour_conflicts": behaviour_conflicts,
    }
    return detection, behaviour, audit


def _genus_source_unit_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for genus in sorted(ELIGIBLE_GENERA):
        output[genus] = {}
        for role in ROLES:
            subset = [row for row in rows if row["genus"] == genus and row["role"] == role]
            det, beh, audit = _collapse_groups(subset, include_genus=False)
            observed = {
                "detection": sum(det[role].values()),
                "behaviour": sum(beh[role].values()),
                "detection_categories": dict(det[role]),
                "behaviour_categories": dict(beh[role]),
                "conflicts": {
                    "detection": audit["detection_conflicts"],
                    "behaviour": audit["behaviour_conflicts"],
                },
            }
            expected = SOURCE_TABLE2_GENUS_N[genus][role]
            observed["published_n"] = expected
            observed["n_match"] = {
                "detection": observed["detection"] == expected["detection"],
                "behaviour": observed["behaviour"] == expected["behaviour"],
            }
            output[genus][role] = observed
    return output


def _table3_candidate(rows: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    role_compounds: dict[tuple[str, str], set[str]] = defaultdict(set)
    role_choices: dict[tuple[str, str, str], set[str]] = defaultdict(set)

    def included(row: dict[str, Any]) -> bool:
        coded = row["behaviour"] in {"+", "-", "0"}
        named = bool(row["behaviour_test"])
        detection_mentions = "behaviour" in row["detection_label"].casefold()
        if mode == "choice_coded":
            return coded
        if mode == "behaviour_test_named":
            return named
        if mode == "detection_mentions_behaviour":
            return detection_mentions
        if mode == "choice_or_named_test":
            return coded or named
        if mode == "choice_or_detection_mentions":
            return coded or detection_mentions
        raise ValueError(mode)

    for row in rows:
        compound = row["compound"].casefold()
        if included(row):
            role_compounds[(row["genus"], row["role"])].add(compound)
        if row["behaviour"] in {"+", "-", "0"}:
            role_choices[(row["genus"], compound, row["role"])].add(row["behaviour"])

    by_genus: dict[str, Any] = {}
    totals = Counter()
    for genus in sorted(ELIGIBLE_GENERA):
        poll = role_compounds[(genus, "Pollinator")]
        flor = role_compounds[(genus, "Florivore")]
        union = poll | flor
        shared = poll & flor
        attr = 0
        repel = 0
        for compound in shared:
            poll_choices = role_choices[(genus, compound, "Pollinator")]
            flor_choices = role_choices[(genus, compound, "Florivore")]
            attr += int("+" in poll_choices and "+" in flor_choices)
            repel += int("-" in poll_choices and "-" in flor_choices)
        observed = {
            "behavioural_fvocs": len(union),
            "shared_both_roles": len(shared),
            "shared_attractive": attr,
            "shared_repellent": repel,
        }
        expected = SOURCE_SHARED_BY_GENUS[genus]
        observed["published"] = expected
        observed["matches_published"] = {
            key: observed[key] == expected[key] for key in expected
        }
        by_genus[genus] = observed
        for key in ("behavioural_fvocs", "shared_both_roles", "shared_attractive", "shared_repellent"):
            totals[key] += observed[key]

    total_dict = dict(totals)
    total_dict["published"] = SOURCE_SHARED
    total_dict["matches_published"] = {
        key: totals[key] == SOURCE_SHARED[key] for key in SOURCE_SHARED
    }
    exact_genus_denominators = all(
        by_genus[g]["behavioural_fvocs"] == SOURCE_SHARED_BY_GENUS[g]["behavioural_fvocs"]
        for g in ELIGIBLE_GENERA
    )
    return {
        "mode": mode,
        "by_genus": by_genus,
        "total": total_dict,
        "exact_genus_denominators": exact_genus_denominators,
    }


def run(output_path: str | Path) -> dict[str, Any]:
    import openpyxl  # type: ignore

    oa_url = _oa_package_url()
    package, package_url, package_attempts = _download_package(oa_url)
    supplement_name, supplement, _ = _supplement_from_package(package)
    workbook = openpyxl.load_workbook(io.BytesIO(supplement), read_only=True, data_only=True)
    ws = workbook[SHEET]
    index, row_iter, header_absolute_row = _find_header(ws.iter_rows(values_only=True))

    required = {
        "Compound", "Genus", "Insect species", "Insect function", "Detection",
        "Physio_resp", "Physio_No_resp", "Behaviour_test", "Behaviour choice", REFERENCE_COLUMN,
    }
    missing = sorted(required - set(index))
    if missing:
        raise RuntimeError(f"missing required S1 columns: {missing}")

    rows: list[dict[str, Any]] = []
    for source_row in row_iter:
        compound = _text(source_row[index["Compound"]])
        genus = _text(source_row[index["Genus"]])
        insect = _text(source_row[index["Insect species"]])
        role = _text(source_row[index["Insect function"]])
        if not compound or not genus or not insect or role not in ROLES:
            continue
        rows.append({
            "compound": compound,
            "genus": genus,
            "insect": insect,
            "role": role,
            "detection_label": _text(source_row[index["Detection"]]),
            "physio_resp": _is_one(source_row[index["Physio_resp"]]),
            "physio_no_resp": _is_one(source_row[index["Physio_No_resp"]]),
            "behaviour_test": _text(source_row[index["Behaviour_test"]]),
            "behaviour": _text(source_row[index["Behaviour choice"]]),
            "cluster": _cluster_key(source_row[index[REFERENCE_COLUMN]]),
        })

    eligible = [row for row in rows if row["genus"] in ELIGIBLE_GENERA]

    # Article Table 2 total: unique FVOC x insect, not unique within plant genus.
    unique_detection, unique_behaviour, unit_audit = _collapse_groups(eligible, include_genus=False)
    genus_audit = _genus_source_unit_audit(eligible)

    detection_table = [
        [unique_detection["Pollinator"]["detected"], unique_detection["Pollinator"]["not_detected"]],
        [unique_detection["Florivore"]["detected"], unique_detection["Florivore"]["not_detected"]],
    ]
    behaviour_table = [
        [unique_behaviour["Pollinator"]["attractive"], unique_behaviour["Pollinator"]["repellent"], unique_behaviour["Pollinator"]["no_response"]],
        [unique_behaviour["Florivore"]["attractive"], unique_behaviour["Florivore"]["repellent"], unique_behaviour["Florivore"]["no_response"]],
    ]
    det_chi, det_df, det_p = _chisq(detection_table, yates=True)
    beh_chi, beh_df, beh_p = _chisq(behaviour_table, yates=False)

    table3_candidates = [
        _table3_candidate(eligible, mode)
        for mode in (
            "choice_coded",
            "behaviour_test_named",
            "detection_mentions_behaviour",
            "choice_or_named_test",
            "choice_or_detection_mentions",
        )
    ]
    exact_table3_modes = [candidate["mode"] for candidate in table3_candidates if candidate["exact_genus_denominators"]]
    preferred_table3 = next(
        (candidate for candidate in table3_candidates if candidate["mode"] in exact_table3_modes),
        table3_candidates[0],
    )
    shared_attr = preferred_table3["total"]["shared_attractive"]
    shared_rep = preferred_table3["total"]["shared_repellent"]
    shared_binom_p = _two_sided_sign_p(shared_attr, shared_rep)

    # Publication-cluster sensitivity. Keep source rows within publications and treat each publication equally.
    cluster_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in eligible:
        cluster_rows[row["cluster"]].append(row)

    publication_summary = []
    detection_fractions: dict[tuple[str, str], float] = {}
    behaviour_fractions: dict[tuple[str, str], dict[str, float]] = {}
    for cluster, values in cluster_rows.items():
        anon = _anon_cluster(cluster)
        roles = sorted({row["role"] for row in values})
        role_metrics = {}
        for role in ROLES:
            subset = [row for row in values if row["role"] == role]
            det, beh, audit = _collapse_groups(subset, include_genus=False)
            det_n = sum(det[role].values())
            beh_n = sum(beh[role].values())
            det_fraction = det[role]["detected"] / det_n if det_n else None
            beh_fractions = None
            if beh_n:
                beh_fractions = {
                    category: beh[role][category] / beh_n
                    for category in ("attractive", "repellent", "no_response")
                }
            if det_fraction is not None:
                detection_fractions[(cluster, role)] = det_fraction
            if beh_fractions is not None:
                behaviour_fractions[(cluster, role)] = beh_fractions
            role_metrics[role] = {
                "detection_tests": det_n,
                "detected_fraction": det_fraction,
                "behaviour_tests": beh_n,
                "behaviour_fractions": beh_fractions,
                "within_publication_conflicts": {
                    "detection": audit["detection_conflicts"],
                    "behaviour": audit["behaviour_conflicts"],
                },
            }
        publication_summary.append({
            "publication_cluster": anon,
            "response_rows": len(values),
            "genera": len({row["genus"] for row in values}),
            "consumer_roles": roles,
            "fvocs": len({row["compound"].casefold() for row in values}),
            "role_metrics": role_metrics,
        })
    publication_summary.sort(key=lambda item: item["publication_cluster"])

    paired_detection = []
    for cluster in cluster_rows:
        poll_key = (cluster, "Pollinator")
        flor_key = (cluster, "Florivore")
        if poll_key in detection_fractions and flor_key in detection_fractions:
            paired_detection.append({
                "publication_cluster": _anon_cluster(cluster),
                "florivore_minus_pollinator": detection_fractions[flor_key] - detection_fractions[poll_key],
            })
    paired_diffs = [item["florivore_minus_pollinator"] for item in paired_detection]
    positive = sum(value > 0 for value in paired_diffs)
    negative = sum(value < 0 for value in paired_diffs)
    zero = sum(value == 0 for value in paired_diffs)

    behaviour_role_medians = {}
    for role in ROLES:
        role_values = [value for (cluster, r), value in behaviour_fractions.items() if r == role]
        behaviour_role_medians[role] = {
            "publication_role_units": len(role_values),
            "median_attractive_fraction": _median([value["attractive"] for value in role_values]),
            "median_repellent_fraction": _median([value["repellent"] for value in role_values]),
            "median_no_response_fraction": _median([value["no_response"] for value in role_values]),
        }

    detection_exact = all(
        unique_detection[role][category] == expected
        for role, values in SOURCE_DETECTION.items()
        for category, expected in values.items()
    ) and unit_audit["detection_conflicts"] == 0
    behaviour_exact = all(
        unique_behaviour[role][category] == expected
        for role, values in SOURCE_BEHAVIOUR.items()
        for category, expected in values.items()
    ) and unit_audit["behaviour_conflicts"] == 0
    table3_exact = bool(exact_table3_modes) and all(preferred_table3["total"]["matches_published"].values())

    report = {
        "source": {
            "doi": DOI,
            "pmcid": PMCID,
            "supplement_name": supplement_name,
            "oa_package_url_used": package_url,
            "oa_package_attempts": package_attempts,
            "sheet": SHEET,
            "header_absolute_row": header_absolute_row,
            "eligible_genera": sorted(ELIGIBLE_GENERA),
            "article_unit_definition": "Table 2 total is every unique FVOC x insect combination; genus is not part of the total-level deduplication key.",
        },
        "table2_reconstruction": {
            "eligible_s1_rows": len(eligible),
            "global_unique_unit_audit": unit_audit,
            "detection": {role: dict(unique_detection[role]) for role in ROLES},
            "behaviour": {role: dict(unique_behaviour[role]) for role in ROLES},
            "detection_chisq_yates": {"statistic": det_chi, "df": det_df, "p": det_p},
            "behaviour_chisq": {"statistic": beh_chi, "df": beh_df, "p": beh_p},
            "published_detection": SOURCE_DETECTION,
            "published_behaviour_implied_by_percentages": SOURCE_BEHAVIOUR,
            "by_genus_n_audit": genus_audit,
        },
        "table3_reconstruction": {
            "candidate_denominator_definitions": table3_candidates,
            "exact_genus_denominator_modes": exact_table3_modes,
            "preferred_mode": preferred_table3["mode"],
            "preferred_total": preferred_table3["total"],
            "shared_attractive_vs_shared_repellent_two_sided_sign_p": shared_binom_p,
            "published": SOURCE_SHARED,
        },
        "publication_dependence": {
            "unique_publication_clusters": len(cluster_rows),
            "publication_cluster_summaries": publication_summary,
            "paired_detection_publications": len(paired_detection),
            "paired_detection_differences": paired_detection,
            "paired_detection_median_difference": _median(paired_diffs),
            "paired_detection_positive": positive,
            "paired_detection_negative": negative,
            "paired_detection_zero": zero,
            "paired_detection_exact_sign_p": _two_sided_sign_p(positive, negative),
            "behaviour_publication_medians": behaviour_role_medians,
        },
        "checkpoints": {
            "table2_detection_exact": detection_exact,
            "table2_behaviour_exact": behaviour_exact,
            "table3_exact": table3_exact,
            "publication_identifier_recovered": bool(cluster_rows),
            "publication_cluster_sensitivity_executed": bool(paired_detection),
        },
        "gate_c": {
            "automatic_status": "PASS_CANDIDATE" if detection_exact and behaviour_exact and table3_exact and paired_detection else "ADJUDICATION_REQUIRED",
            "reason": "Gate C is finalized only after source-paper/deposit discrepancies, if any, are explicitly adjudicated in the readout.",
        },
        "guardrails": [
            "No observation-level source rows or literal references are persisted.",
            "Publication identifiers are anonymized by a stable SHA-256 prefix.",
            "Categorical response structure is retained; no cross-assay continuous effect is fabricated.",
            "Counts from this information-rich synthesis are coverage, not prevalence in nature.",
        ],
    }

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    args = parser.parse_args()
    try:
        result = run(args.output)
    except Exception as error:
        safe = f"{type(error).__name__}: {error}".replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
        print(f"::error title=Sasidharan FVOC reconstruction failure::{safe}")
        raise
    print(json.dumps({
        "table2_reconstruction": result["table2_reconstruction"],
        "table3_reconstruction": result["table3_reconstruction"],
        "publication_dependence": {
            k: v for k, v in result["publication_dependence"].items()
            if k not in {"publication_cluster_summaries", "paired_detection_differences"}
        },
        "checkpoints": result["checkpoints"],
        "gate_c": result["gate_c"],
    }, indent=2))
