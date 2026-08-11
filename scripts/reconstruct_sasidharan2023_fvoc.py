"""Reproduce and dependence-audit Sasidharan et al. (2023) FVOC synthesis.

The source unit is categorical (detected/not detected; attractive/repellent/no response).
This script intentionally does not invent a common continuous effect size across assays.
Only aggregate results and anonymized publication-cluster summaries are persisted.
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
    "Brassica",
    "Cirsium",
    "Cucurbita",
    "Daucus",
    "Dichaea",
    "Fragaria",
    "Helianthus",
    "Nicotiana",
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
SOURCE_SHARED = {
    "behavioural_fvocs": 102,
    "shared_both_roles": 32,
    "shared_attractive": 8,
    "shared_repellent": 1,
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
            statistic += (delta * delta) / expected
    df = (rows - 1) * (cols - 1)
    if df == 1:
        p = math.erfc(math.sqrt(statistic / 2.0))
    elif df == 2:
        p = math.exp(-statistic / 2.0)
    else:
        raise RuntimeError("this bounded reproduction only needs chi-square df 1 or 2")
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


def run(output_path: str | Path) -> dict[str, Any]:
    import openpyxl  # type: ignore

    oa_url = _oa_package_url()
    package, package_url, package_attempts = _download_package(oa_url)
    supplement_name, supplement, _ = _supplement_from_package(package)
    workbook = openpyxl.load_workbook(io.BytesIO(supplement), read_only=True, data_only=True)
    ws = workbook[SHEET]
    index, row_iter, header_absolute_row = _find_header(ws.iter_rows(values_only=True))

    required = {
        "Compound", "Genus", "Insect species", "Insect function",
        "Physio_resp", "Physio_No_resp", "Behaviour choice", REFERENCE_COLUMN,
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
            "physio_resp": _is_one(source_row[index["Physio_resp"]]),
            "physio_no_resp": _is_one(source_row[index["Physio_No_resp"]]),
            "behaviour": _text(source_row[index["Behaviour choice"]]),
            "cluster": _cluster_key(source_row[index[REFERENCE_COLUMN]]),
        })

    eligible = [row for row in rows if row["genus"] in ELIGIBLE_GENERA]

    # Source-unit reconstruction from deposited S1 rows.
    detection = {role: Counter() for role in ROLES}
    behaviour = {role: Counter() for role in ROLES}
    physio_conflicts = 0
    for row in eligible:
        role = row["role"]
        if row["physio_resp"] and row["physio_no_resp"]:
            physio_conflicts += 1
        elif row["physio_resp"]:
            detection[role]["detected"] += 1
        elif row["physio_no_resp"]:
            detection[role]["not_detected"] += 1
        choice = row["behaviour"]
        if choice == "+":
            behaviour[role]["attractive"] += 1
        elif choice == "-":
            behaviour[role]["repellent"] += 1
        elif choice == "0":
            behaviour[role]["no_response"] += 1

    # Check whether duplicate FVOC x insect-species rows alter the source-unit totals.
    groups: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in eligible:
        key = (row["genus"], row["compound"].casefold(), row["insect"].casefold(), row["role"])
        groups[key].append(row)
    duplicate_groups = {key: values for key, values in groups.items() if len(values) > 1}
    unique_detection = {role: Counter() for role in ROLES}
    unique_behaviour = {role: Counter() for role in ROLES}
    unique_behaviour_conflicts = 0
    for values in groups.values():
        role = values[0]["role"]
        if any(row["physio_resp"] for row in values):
            unique_detection[role]["detected"] += 1
        elif any(row["physio_no_resp"] for row in values):
            unique_detection[role]["not_detected"] += 1
        choices = {row["behaviour"] for row in values if row["behaviour"] in {"+", "-", "0"}}
        if len(choices) == 1:
            choice = next(iter(choices))
            unique_behaviour[role][{"+": "attractive", "-": "repellent", "0": "no_response"}[choice]] += 1
        elif len(choices) > 1:
            unique_behaviour_conflicts += 1

    # Shared compound tracking at genus x FVOC level, preserving categorical response sets.
    role_choices: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    behavioural_fvocs: set[tuple[str, str]] = set()
    for row in eligible:
        if row["behaviour"] not in {"+", "-", "0"}:
            continue
        compound_key = row["compound"].casefold()
        behavioural_fvocs.add((row["genus"], compound_key))
        role_choices[(row["genus"], compound_key, row["role"])].add(row["behaviour"])

    shared_keys = sorted({
        (genus, compound)
        for genus, compound in behavioural_fvocs
        if (genus, compound, "Pollinator") in role_choices
        and (genus, compound, "Florivore") in role_choices
    })
    shared_counts = Counter()
    genus_shared: dict[str, Counter[str]] = defaultdict(Counter)
    for genus, compound in shared_keys:
        poll = role_choices[(genus, compound, "Pollinator")]
        flor = role_choices[(genus, compound, "Florivore")]
        flags = {
            "shared_attractive": "+" in poll and "+" in flor,
            "shared_repellent": "-" in poll and "-" in flor,
            "pollinator_attractive_florivore_repellent": "+" in poll and "-" in flor,
            "pollinator_repellent_florivore_attractive": "-" in poll and "+" in flor,
        }
        if any(flags.values()):
            for label, present in flags.items():
                if present:
                    shared_counts[label] += 1
                    genus_shared[genus][label] += 1
        else:
            shared_counts["role_specific_or_null"] += 1
            genus_shared[genus]["role_specific_or_null"] += 1
        genus_shared[genus]["shared_both_roles"] += 1

    genus_behavioural_fvocs = Counter(genus for genus, _ in behavioural_fvocs)
    genus_table = {
        genus: {
            "behavioural_fvocs": genus_behavioural_fvocs[genus],
            "shared_both_roles": genus_shared[genus]["shared_both_roles"],
            "shared_attractive": genus_shared[genus]["shared_attractive"],
            "shared_repellent": genus_shared[genus]["shared_repellent"],
            "pollinator_attractive_florivore_repellent": genus_shared[genus]["pollinator_attractive_florivore_repellent"],
            "pollinator_repellent_florivore_attractive": genus_shared[genus]["pollinator_repellent_florivore_attractive"],
            "role_specific_or_null": genus_shared[genus]["role_specific_or_null"],
        }
        for genus in sorted(ELIGIBLE_GENERA)
    }

    # Publication-cluster sensitivity on source-unit categorical rows.
    cluster_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in eligible:
        cluster_rows[row["cluster"]].append(row)

    publication_summary = []
    detection_fractions: dict[tuple[str, str], float] = {}
    behaviour_fractions: dict[tuple[str, str], dict[str, float]] = {}
    for cluster, values in cluster_rows.items():
        anon = _anon_cluster(cluster)
        roles = sorted({row["role"] for row in values})
        genera = {row["genus"] for row in values}
        fvocs = {row["compound"].casefold() for row in values}
        role_metrics = {}
        for role in ROLES:
            subset = [row for row in values if row["role"] == role]
            det_rows = [row for row in subset if row["physio_resp"] or row["physio_no_resp"]]
            beh_rows = [row for row in subset if row["behaviour"] in {"+", "-", "0"}]
            if det_rows:
                fraction = sum(row["physio_resp"] for row in det_rows) / len(det_rows)
                detection_fractions[(cluster, role)] = fraction
            else:
                fraction = None
            if beh_rows:
                fractions = {
                    "attractive": sum(row["behaviour"] == "+" for row in beh_rows) / len(beh_rows),
                    "repellent": sum(row["behaviour"] == "-" for row in beh_rows) / len(beh_rows),
                    "no_response": sum(row["behaviour"] == "0" for row in beh_rows) / len(beh_rows),
                }
                behaviour_fractions[(cluster, role)] = fractions
            else:
                fractions = None
            role_metrics[role] = {
                "detection_tests": len(det_rows),
                "detected_fraction": fraction,
                "behaviour_tests": len(beh_rows),
                "behaviour_fractions": fractions,
            }
        publication_summary.append({
            "publication_cluster": anon,
            "response_rows": len(values),
            "genera": len(genera),
            "consumer_roles": roles,
            "fvocs": len(fvocs),
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

    detection_table = [
        [detection["Pollinator"]["detected"], detection["Pollinator"]["not_detected"]],
        [detection["Florivore"]["detected"], detection["Florivore"]["not_detected"]],
    ]
    behaviour_table = [
        [behaviour["Pollinator"]["attractive"], behaviour["Pollinator"]["repellent"], behaviour["Pollinator"]["no_response"]],
        [behaviour["Florivore"]["attractive"], behaviour["Florivore"]["repellent"], behaviour["Florivore"]["no_response"]],
    ]
    det_chi, det_df, det_p = _chisq(detection_table, yates=True)
    beh_chi, beh_df, beh_p = _chisq(behaviour_table, yates=False)
    shared_binom_p = _two_sided_sign_p(shared_counts["shared_attractive"], shared_counts["shared_repellent"])

    detection_exact = all(
        detection[role][category] == expected
        for role, values in SOURCE_DETECTION.items()
        for category, expected in values.items()
    )
    behaviour_exact = all(
        behaviour[role][category] == expected
        for role, values in SOURCE_BEHAVIOUR.items()
        for category, expected in values.items()
    )
    behaviour_denominators_exact = all(
        sum(behaviour[role].values()) == sum(SOURCE_BEHAVIOUR[role].values())
        for role in ROLES
    )
    shared_exact = (
        len(behavioural_fvocs) == SOURCE_SHARED["behavioural_fvocs"]
        and len(shared_keys) == SOURCE_SHARED["shared_both_roles"]
        and shared_counts["shared_attractive"] == SOURCE_SHARED["shared_attractive"]
        and shared_counts["shared_repellent"] == SOURCE_SHARED["shared_repellent"]
    )

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
        },
        "source_unit_reconstruction": {
            "eligible_s1_rows": len(eligible),
            "physiology_conflict_rows": physio_conflicts,
            "detection": {role: dict(detection[role]) for role in ROLES},
            "behaviour": {role: dict(behaviour[role]) for role in ROLES},
            "detection_chisq_yates": {"statistic": det_chi, "df": det_df, "p": det_p},
            "behaviour_chisq": {"statistic": beh_chi, "df": beh_df, "p": beh_p},
            "duplicate_fvoc_insect_groups": len(duplicate_groups),
            "unique_group_detection": {role: dict(unique_detection[role]) for role in ROLES},
            "unique_group_behaviour": {role: dict(unique_behaviour[role]) for role in ROLES},
            "unique_group_behaviour_conflicts": unique_behaviour_conflicts,
        },
        "shared_tracking": {
            "behavioural_fvocs": len(behavioural_fvocs),
            "shared_both_roles": len(shared_keys),
            **dict(shared_counts),
            "shared_attractive_vs_shared_repellent_two_sided_sign_p": shared_binom_p,
            "by_genus": genus_table,
            "classification_note": "Directional categories are recurrence flags within genus x FVOC context and need not be mutually exclusive when different insect tests disagree within a role.",
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
            "published_detection_counts": SOURCE_DETECTION,
            "published_behaviour_counts_implied_by_reported_percentages": SOURCE_BEHAVIOUR,
            "published_shared_counts": SOURCE_SHARED,
            "detection_counts_exact": detection_exact,
            "behaviour_counts_exact": behaviour_exact,
            "behaviour_role_denominators_exact": behaviour_denominators_exact,
            "shared_counts_exact": shared_exact,
            "publication_identifier_recovered": bool(cluster_rows) and all(row["cluster"] != "ref:" for row in eligible),
            "publication_cluster_sensitivity_executed": bool(paired_detection),
        },
        "gate_c": {
            "automatic_status": "PASS_CANDIDATE" if detection_exact and behaviour_exact and shared_exact and paired_detection else "ADJUDICATION_REQUIRED",
            "reason": "Gate C is finalized in the source-audit readout. Any paper-versus-deposit discrepancy must be explicitly adjudicated rather than hidden.",
        },
        "guardrails": [
            "No observation-level source rows or literal references are persisted.",
            "Publication identifiers are anonymized by a stable SHA-256 prefix in persisted summaries.",
            "Categorical response structure is retained; no cross-assay continuous effect is fabricated.",
            "Counts across this information-rich deposited synthesis are coverage, not prevalence in nature.",
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
        "source_unit_reconstruction": result["source_unit_reconstruction"],
        "shared_tracking": {k: v for k, v in result["shared_tracking"].items() if k != "by_genus"},
        "publication_dependence": {
            k: v for k, v in result["publication_dependence"].items()
            if k not in {"publication_cluster_summaries", "paired_detection_differences"}
        },
        "checkpoints": result["checkpoints"],
        "gate_c": result["gate_c"],
    }, indent=2))
