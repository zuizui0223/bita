"""Audit conservative study clustering and discordant FVOC units in Sasidharan 2023.

The script never persists literal citations, insect names, compounds, or observation-level rows.
Study components are formed only by exact normalized citation identity or an explicit shared DOI.
Fuzzy similarity is diagnostic only and NEVER merges studies automatically.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
import hashlib
import io
import json
import re
import statistics
from pathlib import Path
from typing import Any, Iterable

from audit_sasidharan2023_pmc_supplement import (
    _download_package,
    _oa_package_url,
    _supplement_from_package,
)

SHEET = "S1"
REFERENCE_COLUMN = "Reference (doi TBA)"
ROLES = {"Pollinator", "Florivore"}
ELIGIBLE_GENERA = {
    "Brassica", "Cirsium", "Cucurbita", "Daucus",
    "Dichaea", "Fragaria", "Helianthus", "Nicotiana",
}
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.I)
DOI_PREFIX_RE = re.compile(r"https?\s*:?\s*/?/?\s*(?:dx\.)?doi\.org\s*/?", re.I)
YEAR_RE = re.compile(r"\b(?:19|20)\d{2}\b")


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


def _citation_stem(reference: Any) -> str:
    text = _text(reference).lower()
    text = DOI_RE.sub(" ", text)
    text = DOI_PREFIX_RE.sub(" ", text)
    text = re.sub(r"\bdoi\b", " ", text)
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _dois(reference: Any) -> set[str]:
    return {
        match.group(0).rstrip(".,;)").lower()
        for match in DOI_RE.finditer(_text(reference))
    }


def _tokens(stem: str) -> set[str]:
    return {
        token for token in stem.split()
        if len(token) >= 3 and not YEAR_RE.fullmatch(token)
    }


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def _hash(text: str, prefix: str) -> str:
    return prefix + hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _find_header(rows: Iterable[tuple[Any, ...]]) -> tuple[dict[str, int], Iterable[tuple[Any, ...]], int]:
    iterator = iter(rows)
    for absolute_row, row in enumerate(iterator, start=1):
        headers = [_text(value) for value in row]
        index = {name: i for i, name in enumerate(headers) if name}
        required = {
            "Compound", "Genus", "Insect species", "Insect function",
            "Physio_resp", "Physio_No_resp", "Behaviour choice", REFERENCE_COLUMN,
        }
        if required.issubset(index):
            return index, iterator, absolute_row
    raise RuntimeError("could not locate S1 header")


def _components(stem_dois: dict[str, set[str]]) -> tuple[list[set[str]], dict[str, int]]:
    stems = sorted(stem_dois)
    doi_to_stems: dict[str, set[str]] = defaultdict(set)
    for stem, dois in stem_dois.items():
        for doi in dois:
            doi_to_stems[doi].add(stem)

    adjacency: dict[str, set[str]] = {stem: set() for stem in stems}
    for linked in doi_to_stems.values():
        linked_list = sorted(linked)
        for i, left in enumerate(linked_list):
            for right in linked_list[i + 1:]:
                adjacency[left].add(right)
                adjacency[right].add(left)

    output: list[set[str]] = []
    stem_to_component: dict[str, int] = {}
    seen: set[str] = set()
    for start in stems:
        if start in seen:
            continue
        queue = deque([start])
        seen.add(start)
        component: set[str] = set()
        while queue:
            node = queue.popleft()
            component.add(node)
            for neighbor in adjacency[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        idx = len(output)
        output.append(component)
        for stem in component:
            stem_to_component[stem] = idx
    return output, stem_to_component


def _collapse_detection(rows: list[dict[str, Any]]) -> tuple[dict[str, Counter[str]], int]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["compound"], row["insect"], row["role"])].append(row)
    counts = {role: Counter() for role in ROLES}
    conflicts = 0
    for values in groups.values():
        states: set[str] = set()
        for row in values:
            if row["physio_resp"]:
                states.add("detected")
            if row["physio_no_resp"]:
                states.add("not_detected")
        if not states:
            continue
        if len(states) > 1:
            conflicts += 1
            continue
        counts[values[0]["role"]][next(iter(states))] += 1
    return counts, conflicts


def _detection_effect(rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    counts, conflicts = _collapse_detection(rows)
    role_stats: dict[str, Any] = {}
    for role in sorted(ROLES):
        detected = counts[role]["detected"]
        not_detected = counts[role]["not_detected"]
        total = detected + not_detected
        if total == 0:
            return None
        role_stats[role] = {
            "detected": detected,
            "not_detected": not_detected,
            "total": total,
            "detected_fraction": detected / total,
        }
    poll = role_stats["Pollinator"]
    flor = role_stats["Florivore"]
    poll_p = poll["detected_fraction"]
    flor_p = flor["detected_fraction"]
    odds_ratio = None
    if all(value > 0 for value in (poll["detected"], poll["not_detected"], flor["detected"], flor["not_detected"])):
        odds_ratio = (flor["detected"] * poll["not_detected"]) / (flor["not_detected"] * poll["detected"])
    return {
        "roles": role_stats,
        "florivore_minus_pollinator_risk_difference": flor_p - poll_p,
        "florivore_over_pollinator_risk_ratio": flor_p / poll_p if poll_p else None,
        "florivore_vs_pollinator_odds_ratio": odds_ratio,
        "detection_conflicts": conflicts,
    }


def _behaviour_bounds(rows: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["behaviour"] in {"+", "-", "0"}:
            groups[(row["compound"], row["insect"], row["role"])].append(row)
    uniform = {role: Counter() for role in ROLES}
    discordant = {role: [] for role in ROLES}
    for values in groups.values():
        role = values[0]["role"]
        choices = {row["behaviour"] for row in values}
        if len(choices) == 1:
            uniform[role][next(iter(choices))] += 1
        else:
            discordant[role].append(choices)
    output: dict[str, Any] = {}
    for role in sorted(ROLES):
        conflicts = discordant[role]
        output[role] = {
            "coded_unique_units": sum(uniform[role].values()) + len(conflicts),
            "uniform_attractive": uniform[role]["+"],
            "uniform_repellent": uniform[role]["-"],
            "uniform_no_response": uniform[role]["0"],
            "discordant_units": len(conflicts),
            "attractive_range": [
                uniform[role]["+"],
                uniform[role]["+"] + sum("+" in choices for choices in conflicts),
            ],
            "repellent_range": [
                uniform[role]["-"],
                uniform[role]["-"] + sum("-" in choices for choices in conflicts),
            ],
            "no_response_range": [
                uniform[role]["0"],
                uniform[role]["0"] + sum("0" in choices for choices in conflicts),
            ],
        }
    return output


def run(output_path: str | Path) -> dict[str, Any]:
    import openpyxl  # type: ignore

    oa_url = _oa_package_url()
    package, package_url, package_attempts = _download_package(oa_url)
    supplement_name, supplement, _ = _supplement_from_package(package)
    workbook = openpyxl.load_workbook(io.BytesIO(supplement), read_only=True, data_only=True)
    ws = workbook[SHEET]
    index, row_iter, header_absolute_row = _find_header(ws.iter_rows(values_only=True))

    rows: list[dict[str, Any]] = []
    stem_dois: dict[str, set[str]] = defaultdict(set)
    stem_row_count: Counter[str] = Counter()
    stem_roles: dict[str, set[str]] = defaultdict(set)
    stem_genera: dict[str, set[str]] = defaultdict(set)
    raw_reference_strings: set[str] = set()

    for source_row in row_iter:
        compound = _text(source_row[index["Compound"]])
        genus = _text(source_row[index["Genus"]])
        insect = _text(source_row[index["Insect species"]])
        role = _text(source_row[index["Insect function"]])
        reference = _text(source_row[index[REFERENCE_COLUMN]])
        if not compound or not genus or not insect or role not in ROLES or not reference:
            continue
        stem = _citation_stem(reference)
        raw_reference_strings.add(reference)
        stem_dois[stem].update(_dois(reference))
        stem_row_count[stem] += 1
        stem_roles[stem].add(role)
        stem_genera[stem].add(genus)
        rows.append({
            "compound": compound.casefold(),
            "genus": genus,
            "insect": insect.casefold(),
            "role": role,
            "physio_resp": _is_one(source_row[index["Physio_resp"]]),
            "physio_no_resp": _is_one(source_row[index["Physio_No_resp"]]),
            "behaviour": _text(source_row[index["Behaviour choice"]]),
            "stem": stem,
        })

    components, stem_to_component = _components(stem_dois)
    component_ids = {
        idx: _hash("||".join(sorted(component)), "study_")
        for idx, component in enumerate(components)
    }
    for row in rows:
        row["component"] = stem_to_component[row["stem"]]

    component_rows: Counter[int] = Counter()
    component_roles: dict[int, set[str]] = defaultdict(set)
    component_genera: dict[int, set[str]] = defaultdict(set)
    component_dois: dict[int, set[str]] = defaultdict(set)
    for stem in stem_dois:
        idx = stem_to_component[stem]
        component_rows[idx] += stem_row_count[stem]
        component_roles[idx].update(stem_roles[stem])
        component_genera[idx].update(stem_genera[stem])
        component_dois[idx].update(stem_dois[stem])

    component_summaries = []
    for idx, component in enumerate(components):
        component_summaries.append({
            "study_component": component_ids[idx],
            "citation_stems": len(component),
            "doi_count": len(component_dois[idx]),
            "rows": component_rows[idx],
            "roles": sorted(component_roles[idx]),
            "genera": len(component_genera[idx]),
        })
    component_summaries.sort(key=lambda item: item["study_component"])

    doi_free = [stem for stem, dois in stem_dois.items() if not dois]
    doi_bearing = [stem for stem, dois in stem_dois.items() if dois]
    similarity_candidates = []
    for fallback in doi_free:
        left = _tokens(fallback)
        ranked = sorted(
            ((_jaccard(left, _tokens(target)), target) for target in doi_bearing),
            reverse=True,
        )[:3]
        years_left = sorted(set(YEAR_RE.findall(fallback)))
        for score, target in ranked:
            years_right = sorted(set(YEAR_RE.findall(target)))
            similarity_candidates.append({
                "fallback_stem": _hash(fallback, "cite_"),
                "candidate_stem": _hash(target, "cite_"),
                "token_jaccard": round(score, 6),
                "year_overlap": bool(set(years_left) & set(years_right)),
                "candidate_doi_count": len(stem_dois[target]),
            })

    eligible = [row for row in rows if row["genus"] in ELIGIBLE_GENERA]
    behavior_groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in eligible:
        if row["behaviour"] in {"+", "-", "0"}:
            behavior_groups[(row["compound"], row["insect"], row["role"])].append(row)

    conflict_choice_sets: Counter[str] = Counter()
    conflict_roles: Counter[str] = Counter()
    conflict_rows_per_unit: list[int] = []
    conflict_component_span: Counter[str] = Counter()
    conflict_genus_span: Counter[str] = Counter()
    conflict_summaries = []
    for key, values in behavior_groups.items():
        choices = sorted({row["behaviour"] for row in values})
        if len(choices) <= 1:
            continue
        role = key[2]
        component_set = {row["component"] for row in values}
        genera = {row["genus"] for row in values}
        choice_label = "|".join(choices)
        conflict_choice_sets[choice_label] += 1
        conflict_roles[role] += 1
        conflict_rows_per_unit.append(len(values))
        conflict_component_span["multiple_components" if len(component_set) > 1 else "single_component"] += 1
        conflict_genus_span["multiple_genera" if len(genera) > 1 else "single_genus"] += 1
        conflict_summaries.append({
            "unit": _hash("||".join(key), "unit_"),
            "role": role,
            "choice_set": choices,
            "rows": len(values),
            "study_components": len(component_set),
            "genera": len(genera),
        })
    conflict_summaries.sort(key=lambda item: item["unit"])

    # Study-component sensitivity for the clean physiological-detection endpoint.
    full_detection = _detection_effect(eligible)
    leave_one_out = []
    for idx in range(len(components)):
        effect = _detection_effect([row for row in eligible if row["component"] != idx])
        if effect is None:
            continue
        leave_one_out.append({
            "excluded_study_component": component_ids[idx],
            "risk_difference": effect["florivore_minus_pollinator_risk_difference"],
            "risk_ratio": effect["florivore_over_pollinator_risk_ratio"],
        })
    loo_diffs = [item["risk_difference"] for item in leave_one_out]

    component_role_detection: dict[str, list[float]] = defaultdict(list)
    paired_component_diffs = []
    for idx in range(len(components)):
        subset = [row for row in eligible if row["component"] == idx]
        counts, conflicts = _collapse_detection(subset)
        fractions: dict[str, float] = {}
        for role in sorted(ROLES):
            n = counts[role]["detected"] + counts[role]["not_detected"]
            if n:
                fraction = counts[role]["detected"] / n
                fractions[role] = fraction
                component_role_detection[role].append(fraction)
        if ROLES.issubset(fractions):
            paired_component_diffs.append({
                "study_component": component_ids[idx],
                "florivore_minus_pollinator": fractions["Florivore"] - fractions["Pollinator"],
                "detection_conflicts": conflicts,
            })

    equal_weight = {}
    for role in sorted(ROLES):
        values = component_role_detection[role]
        equal_weight[role] = {
            "study_role_units": len(values),
            "mean_detected_fraction": statistics.mean(values) if values else None,
            "median_detected_fraction": statistics.median(values) if values else None,
        }
    paired_values = [item["florivore_minus_pollinator"] for item in paired_component_diffs]

    doi_cardinality = Counter(len(dois) for dois in stem_dois.values())
    component_size_stems = [len(component) for component in components]
    component_size_rows = [component_rows[idx] for idx in range(len(components))]

    report = {
        "source": {
            "supplement_name": supplement_name,
            "oa_package_url_used": package_url,
            "oa_package_attempts": package_attempts,
            "sheet": SHEET,
            "header_absolute_row": header_absolute_row,
        },
        "citation_topology": {
            "published_final_study_count": 32,
            "raw_reference_strings": len(raw_reference_strings),
            "exact_citation_stems": len(stem_dois),
            "doi_cardinality_per_stem": {str(k): v for k, v in sorted(doi_cardinality.items())},
            "doi_free_stems": len(doi_free),
            "conservative_components_same_doi_or_exact_stem": len(components),
            "matches_published_study_count": len(components) == 32,
            "components_with_multiple_stems": sum(len(component) > 1 for component in components),
            "components_with_multiple_dois": sum(len(component_dois[idx]) > 1 for idx in range(len(components))),
            "components_with_both_roles": sum(component_roles[idx] >= ROLES for idx in range(len(components))),
            "component_stem_size_median": statistics.median(component_size_stems) if component_size_stems else None,
            "component_stem_size_max": max(component_size_stems) if component_size_stems else None,
            "component_row_size_median": statistics.median(component_size_rows) if component_size_rows else None,
            "component_row_size_max": max(component_size_rows) if component_size_rows else None,
            "component_summaries": component_summaries,
            "fallback_similarity_candidates_diagnostic_only": similarity_candidates,
        },
        "detection_study_sensitivity": {
            "full_current_deposit": full_detection,
            "leave_one_study_component_out": {
                "runs": len(leave_one_out),
                "risk_difference_min": min(loo_diffs) if loo_diffs else None,
                "risk_difference_median": statistics.median(loo_diffs) if loo_diffs else None,
                "risk_difference_max": max(loo_diffs) if loo_diffs else None,
                "positive_direction_runs": sum(value > 0 for value in loo_diffs),
                "zero_direction_runs": sum(value == 0 for value in loo_diffs),
                "negative_direction_runs": sum(value < 0 for value in loo_diffs),
                "anonymized_runs": leave_one_out,
            },
            "equal_weight_study_role_fractions": equal_weight,
            "paired_both_role_components": {
                "n": len(paired_component_diffs),
                "median_difference": statistics.median(paired_values) if paired_values else None,
                "positive": sum(value > 0 for value in paired_values),
                "zero": sum(value == 0 for value in paired_values),
                "negative": sum(value < 0 for value in paired_values),
                "anonymized_components": paired_component_diffs,
            },
            "interpretation_guardrail": "Leave-one-study-out stability tests influence of any single study but does not remove study-by-role composition imbalance; paired both-role components are reported separately.",
        },
        "behaviour_conflicts": {
            "global_fvoc_insect_role_units_with_coded_behaviour": len(behavior_groups),
            "discordant_units": len(conflict_summaries),
            "choice_set_counts": dict(conflict_choice_sets),
            "role_counts": dict(conflict_roles),
            "study_component_span": dict(conflict_component_span),
            "genus_span": dict(conflict_genus_span),
            "rows_per_discordant_unit_median": statistics.median(conflict_rows_per_unit) if conflict_rows_per_unit else None,
            "rows_per_discordant_unit_max": max(conflict_rows_per_unit) if conflict_rows_per_unit else None,
            "current_deposit_category_bounds": _behaviour_bounds(eligible),
            "anonymized_units": conflict_summaries,
        },
        "adjudication_rules": [
            "Exact normalized citation stems are identical bibliographic labels.",
            "Different stems are linked automatically only when they share an explicit DOI.",
            "Token-Jaccard candidates are diagnostic only; they are not auto-merged.",
            "A discordant repeated FVOC x insect x role unit is retained as discordant rather than resolved by arbitrary row order.",
        ],
        "guardrails": [
            "No literal citation, compound, insect name, or observation-level source row is persisted.",
            "All displayed study/unit identifiers are stable SHA-256 prefixes.",
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
    result = run(args.output)
    compact = {
        "citation_topology": {k: v for k, v in result["citation_topology"].items() if k not in {"component_summaries", "fallback_similarity_candidates_diagnostic_only"}},
        "detection_study_sensitivity": {
            "full_current_deposit": result["detection_study_sensitivity"]["full_current_deposit"],
            "leave_one_study_component_out": {k: v for k, v in result["detection_study_sensitivity"]["leave_one_study_component_out"].items() if k != "anonymized_runs"},
            "equal_weight_study_role_fractions": result["detection_study_sensitivity"]["equal_weight_study_role_fractions"],
            "paired_both_role_components": {k: v for k, v in result["detection_study_sensitivity"]["paired_both_role_components"].items() if k != "anonymized_components"},
        },
        "behaviour_conflicts": {k: v for k, v in result["behaviour_conflicts"].items() if k != "anonymized_units"},
    }
    print(json.dumps(compact, indent=2))
