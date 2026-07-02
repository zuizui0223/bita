"""Build and summarize a fixed-corpus audit for broad abstract labels.

The audit calibrates high-recall A/B/P/H abstract co-mention labels without
changing the candidate universe, making causal claims from abstracts, or fitting
the attraction--defence model.
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Iterable

EDGE_FIELDS = {
    "A_to_pollination": "candidate_A_to_P",
    "A_to_antagonism": "candidate_A_to_H",
    "B_to_antagonism": "candidate_B_to_H",
    "B_to_pollination": "candidate_B_to_P",
    "joint_channels": "candidate_joint_channels",
}
EDGE_ORDER = tuple(EDGE_FIELDS)
CORE_EDGES = EDGE_ORDER[:4]
SOURCE_BUCKETS = ("empirical_nonreview", "other")
CONTROL_LABEL = "floral_no_predicted_edge_control"
DEFAULT_NONJOINT_TARGET = 25
DEFAULT_SEED = 20260702
BINARY_CODES = frozenset({"yes", "no", "uncertain", "not_applicable"})
STUDY_ROLE_CODES = frozenset({"empirical_direct", "empirical_indirect", "review_synthesis", "background_or_other", "uncertain"})
CODING_STATUS_CODES = frozenset({"unreviewed", "reviewed"})

PACKET_FIELDS = (
    "audit_id", "candidate_id", "doi", "title", "publication_year", "work_type", "container_title", "publisher",
    "route_families", "source_queries", "shallow_screen_status", "source_bucket", "abstract_retrieval_state",
    "crossref_lookup_status", "crossref_abstract_available", "abstract_code_status", "floral_context_signal",
    "empirical_language_signal", "review_language_signal", "A_signal", "B_signal", "P_signal", "H_signal", "W_signal",
    "shared_cost_language_signal", "candidate_A_to_P", "candidate_A_to_H", "candidate_B_to_H", "candidate_B_to_P",
    "candidate_joint_channels", "audit_strata", "target_model_edges", "selection_mode", "crossref_abstract_text",
    "coding_warning",
)
CODING_FIELDS = PACKET_FIELDS + (
    "coding_status", "coder_id", "coding_date", "human_floral_context", "human_A", "human_B", "human_P", "human_H",
    "human_W", "human_flower_specific_B", "human_study_role", "human_shared_cost", "adjudication_note",
)
DESIGN_FIELDS = (
    "target_label", "source_bucket", "sampling_scope", "population_count", "selected_count", "sampling_method",
    "selection_seed", "selection_rule", "source_artifact_boundary",
)
PRECISION_FIELDS = (
    "target_label", "source_bucket", "sampling_scope", "population_count", "selected_count", "reviewed_count",
    "human_coherent_count", "observed_precision", "calibration_status", "interpretation_boundary",
)
COVERAGE_FIELDS = (
    "target_label", "raw_predicted_candidate_coverage", "reviewed_audit_records", "human_coherent_audit_records",
    "calibrated_candidate_coverage_mean", "calibrated_candidate_coverage_ci_low", "calibrated_candidate_coverage_ci_high",
    "calibration_status", "interpretation_boundary",
)
CONTROL_FIELDS = (
    "source_bucket", "population_count", "selected_count", "reviewed_count", "human_any_edge_count",
    "observed_undetected_edge_rate", "calibration_status", "interpretation_boundary",
)
COMPLETION_FIELDS = ("metric", "value", "interpretation_boundary")


class BroadAbstractAuditError(ValueError):
    """Raised when fixed-map, design, or coding-table contracts are violated."""


def text(value: object) -> str:
    return str(value or "").strip()


def is_true(value: object) -> bool:
    return text(value).lower() in {"true", "1", "yes", "y"}


def read_rows(path: str | Path, required: Iterable[str]) -> list[dict[str, str]]:
    location = Path(path)
    with location.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(required).difference(reader.fieldnames or [])
        if missing:
            raise BroadAbstractAuditError(f"{location} missing required columns: {', '.join(sorted(missing))}")
        return [{key: text(value) for key, value in row.items()} for row in reader]


def source_bucket(row: dict[str, str]) -> str:
    return "empirical_nonreview" if is_true(row.get("empirical_language_signal")) and not is_true(row.get("review_language_signal")) else "other"


def _validate_alignment(records: list[dict[str, str]], packet: list[dict[str, str]]) -> None:
    left, right = [row["candidate_id"] for row in records], [row["candidate_id"] for row in packet]
    if len(left) != len(set(left)) or len(right) != len(set(right)):
        raise BroadAbstractAuditError("candidate IDs must be unique in both fixed-map files")
    if set(left) != set(right):
        raise BroadAbstractAuditError("evidence records and abstract packet must have identical fixed candidate IDs")


def _allocate(population: dict[str, int], target: int) -> dict[str, int]:
    available = {bucket: count for bucket, count in population.items() if count > 0}
    if sum(available.values()) <= target:
        return dict(available)
    allocation = {bucket: min(count, 5) for bucket, count in available.items()}
    remaining = target - sum(allocation.values())
    if remaining <= 0:
        return allocation
    total = sum(available.values())
    ideals = {bucket: remaining * available[bucket] / total for bucket in available}
    for bucket in available:
        allocation[bucket] += min(available[bucket] - allocation[bucket], int(math.floor(ideals[bucket])))
    remaining = target - sum(allocation.values())
    order = sorted(available, key=lambda bucket: (ideals[bucket] % 1, available[bucket] - allocation[bucket], bucket), reverse=True)
    index = 0
    while remaining:
        bucket = order[index % len(order)]
        if allocation[bucket] < available[bucket]:
            allocation[bucket] += 1
            remaining -= 1
        index += 1
    return allocation


def _sample_ids(rows: list[dict[str, str]], count: int, seed: int) -> list[str]:
    ids = sorted(row["candidate_id"] for row in rows)
    return ids if count >= len(ids) else sorted(random.Random(seed).sample(ids, count))


def _core_edge_predicted(row: dict[str, str]) -> bool:
    return any(is_true(row.get(EDGE_FIELDS[edge])) for edge in CORE_EDGES)


def _design_row(label: str, bucket: str, scope: str, population: int, selected: int, method: str, seed: int, rule: str, boundary: str) -> dict[str, str]:
    return {
        "target_label": label, "source_bucket": bucket, "sampling_scope": scope,
        "population_count": str(population), "selected_count": str(selected), "sampling_method": method,
        "selection_seed": str(seed), "selection_rule": rule, "source_artifact_boundary": boundary,
    }


def build_audit_packet(
    evidence_records: Iterable[dict[str, str]],
    abstract_packet: Iterable[dict[str, str]],
    *, seed: int = DEFAULT_SEED,
    nonjoint_target: int = DEFAULT_NONJOINT_TARGET,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Return packet, blank coding sheet, and sampling design from a fixed map.

    Joint records are all censused for the joint channel *and* included in each
    component-edge partition.  This preserves correct edge totals while avoiding
    the false claim that the sparse joint cell was sampled.
    """
    records, packet = list(evidence_records), list(abstract_packet)
    _validate_alignment(records, packet)
    packet_by_id = {row["candidate_id"]: row for row in packet}
    rows = []
    for record in records:
        merged = {**record, **packet_by_id[record["candidate_id"]]}
        merged["source_bucket"] = source_bucket(merged)
        rows.append(merged)

    membership: dict[str, set[str]] = defaultdict(set)
    design: list[dict[str, str]] = []
    boundary = "Selected from the supplied fixed broad-map artifact only; no discovery query or candidate expansion is performed."
    joint = [row for row in rows if is_true(row.get(EDGE_FIELDS["joint_channels"]))]

    for edge in EDGE_ORDER:
        for bucket in SOURCE_BUCKETS:
            census = [row for row in joint if row["source_bucket"] == bucket]
            for row in census:
                membership[row["candidate_id"]].add(f"{edge}__{bucket}__joint_census")
            rule = "All predicted joint A+B+P+H records." if edge == "joint_channels" else "All predicted joint records, included in this component-edge partition."
            design.append(_design_row(edge, bucket, "joint_census", len(census), len(census), "census", seed, rule, boundary))

    for edge_index, edge in enumerate(CORE_EDGES, start=1):
        residual = [row for row in rows if is_true(row.get(EDGE_FIELDS[edge])) and not is_true(row.get(EDGE_FIELDS["joint_channels"]))]
        allocation = _allocate({bucket: sum(row["source_bucket"] == bucket for row in residual) for bucket in SOURCE_BUCKETS}, nonjoint_target)
        for bucket in SOURCE_BUCKETS:
            frame = [row for row in residual if row["source_bucket"] == bucket]
            draw_seed = seed + 100 * edge_index + SOURCE_BUCKETS.index(bucket)
            selected = _sample_ids(frame, allocation.get(bucket, 0), draw_seed)
            for candidate_id in selected:
                membership[candidate_id].add(f"{edge}__{bucket}__nonjoint_sample")
            method = "census" if len(selected) == len(frame) else "stratified_simple_random_sample"
            rule = f"Predicted {edge} excluding joint records; stratified by empirical/nonreview language."
            design.append(_design_row(edge, bucket, "nonjoint_sample", len(frame), len(selected), method, draw_seed, rule, boundary))

    control = [row for row in rows if is_true(row.get("floral_context_signal")) and not _core_edge_predicted(row)]
    allocation = _allocate({bucket: sum(row["source_bucket"] == bucket for row in control) for bucket in SOURCE_BUCKETS}, nonjoint_target)
    for bucket in SOURCE_BUCKETS:
        frame = [row for row in control if row["source_bucket"] == bucket]
        draw_seed = seed + 900 + SOURCE_BUCKETS.index(bucket)
        selected = _sample_ids(frame, allocation.get(bucket, 0), draw_seed)
        for candidate_id in selected:
            membership[candidate_id].add(f"{CONTROL_LABEL}__{bucket}__control_sample")
        method = "census" if len(selected) == len(frame) else "stratified_simple_random_sample"
        rule = "Flower-context records with no predicted A→P, A→H, B→H, or B→P candidate edge."
        design.append(_design_row(CONTROL_LABEL, bucket, "control_sample", len(frame), len(selected), method, draw_seed, rule, boundary))

    by_id = {row["candidate_id"]: row for row in rows}
    packet_rows: list[dict[str, str]] = []
    for index, candidate_id in enumerate(sorted(membership), start=1):
        row, strata = by_id[candidate_id], sorted(membership[candidate_id])
        targets = sorted({item.split("__", 1)[0] for item in strata if not item.startswith(CONTROL_LABEL)})
        packet_rows.append({
            "audit_id": f"BAA{index:03d}", "candidate_id": candidate_id, "doi": text(row.get("doi")),
            "title": text(row.get("title")), "publication_year": text(row.get("publication_year")),
            "work_type": text(row.get("work_type")), "container_title": text(row.get("container_title")),
            "publisher": text(row.get("publisher")), "route_families": text(row.get("route_families")),
            "source_queries": text(row.get("source_queries")), "shallow_screen_status": text(row.get("shallow_screen_status")),
            "source_bucket": row["source_bucket"], "abstract_retrieval_state": text(row.get("abstract_retrieval_state")),
            "crossref_lookup_status": text(row.get("crossref_lookup_status")),
            "crossref_abstract_available": text(row.get("crossref_abstract_available")),
            "abstract_code_status": text(row.get("abstract_code_status")), "floral_context_signal": text(row.get("floral_context_signal")),
            "empirical_language_signal": text(row.get("empirical_language_signal")),
            "review_language_signal": text(row.get("review_language_signal")), "A_signal": text(row.get("A_signal")),
            "B_signal": text(row.get("B_signal")), "P_signal": text(row.get("P_signal")),
            "H_signal": text(row.get("H_signal")), "W_signal": text(row.get("W_signal")),
            "shared_cost_language_signal": text(row.get("shared_cost_language_signal")),
            "candidate_A_to_P": text(row.get("candidate_A_to_P")), "candidate_A_to_H": text(row.get("candidate_A_to_H")),
            "candidate_B_to_H": text(row.get("candidate_B_to_H")), "candidate_B_to_P": text(row.get("candidate_B_to_P")),
            "candidate_joint_channels": text(row.get("candidate_joint_channels")), "audit_strata": ";".join(strata),
            "target_model_edges": ";".join(targets),
            "selection_mode": ";".join(sorted({"census" if "census" in item else "sample" for item in strata})),
            "crossref_abstract_text": text(row.get("crossref_abstract_text")),
            "coding_warning": "Audit abstract-label validity only; this packet is not an effect-size, causal-design, or model-parameter extraction.",
        })
    coding = [{
        **row, "coding_status": "unreviewed", "coder_id": "", "coding_date": "", "human_floral_context": "",
        "human_A": "", "human_B": "", "human_P": "", "human_H": "", "human_W": "",
        "human_flower_specific_B": "", "human_study_role": "", "human_shared_cost": "", "adjudication_note": "",
    } for row in packet_rows]
    return packet_rows, coding, design


def _human_yes(row: dict[str, str], field: str) -> bool:
    return text(row.get(field)).lower() == "yes"


def human_coherent_edge(row: dict[str, str], edge: str) -> bool:
    if not _human_yes(row, "human_floral_context"):
        return False
    if edge == "A_to_pollination":
        return _human_yes(row, "human_A") and _human_yes(row, "human_P")
    if edge == "A_to_antagonism":
        return _human_yes(row, "human_A") and _human_yes(row, "human_H")
    if edge == "B_to_antagonism":
        return _human_yes(row, "human_B") and _human_yes(row, "human_flower_specific_B") and _human_yes(row, "human_H")
    if edge == "B_to_pollination":
        return _human_yes(row, "human_B") and _human_yes(row, "human_flower_specific_B") and _human_yes(row, "human_P")
    if edge == "joint_channels":
        return all(_human_yes(row, field) for field in ("human_A", "human_B", "human_flower_specific_B", "human_P", "human_H"))
    raise BroadAbstractAuditError(f"unknown edge: {edge}")


def _in_partition(row: dict[str, str], label: str, bucket: str, scope: str) -> bool:
    return f"{label}__{bucket}__{scope}" in set(filter(None, text(row.get("audit_strata")).split(";")))


def validate_coding_rows(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    rows = list(rows)
    seen: set[str] = set()
    for row in rows:
        audit_id, status = text(row.get("audit_id")), text(row.get("coding_status")).lower()
        if not audit_id or audit_id in seen:
            raise BroadAbstractAuditError("coding rows require unique audit_id values")
        seen.add(audit_id)
        if status not in CODING_STATUS_CODES:
            raise BroadAbstractAuditError(f"invalid coding_status: {status}")
        if status == "reviewed":
            for field in ("human_floral_context", "human_A", "human_B", "human_P", "human_H", "human_W", "human_flower_specific_B", "human_shared_cost"):
                if text(row.get(field)).lower() not in BINARY_CODES:
                    raise BroadAbstractAuditError(f"reviewed {audit_id} has invalid {field}")
            if text(row.get("human_study_role")).lower() not in STUDY_ROLE_CODES:
                raise BroadAbstractAuditError(f"reviewed {audit_id} has invalid human_study_role")
    return rows


def _beta_projection(correct: int, reviewed: int, population: int, seed: int, draws: int = 20_000) -> list[float]:
    if reviewed == population:
        return [float(correct)] * draws
    rng = random.Random(seed)
    return [population * rng.betavariate(1 + correct, 1 + reviewed - correct) for _ in range(draws)]


def _interval(values: list[float]) -> tuple[float, float]:
    ordered = sorted(values)
    return ordered[round((len(ordered) - 1) * .025)], ordered[round((len(ordered) - 1) * .975)]


def summarize_audit(coding_rows: Iterable[dict[str, str]], design_rows: Iterable[dict[str, str]], *, seed: int = DEFAULT_SEED) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    coding, design = validate_coding_rows(coding_rows), list(design_rows)
    if any(set(DESIGN_FIELDS).difference(row) for row in design):
        raise BroadAbstractAuditError("audit design lacks required columns")
    reviewed = [row for row in coding if text(row.get("coding_status")).lower() == "reviewed"]
    completion = [
        {"metric": "packet_records", "value": str(len(coding)), "interpretation_boundary": "Fixed-packet records selected for manual abstract adjudication."},
        {"metric": "reviewed_records", "value": str(len(reviewed)), "interpretation_boundary": "Only reviewed rows can contribute to calibration."},
        {"metric": "completion_fraction", "value": f"{len(reviewed) / len(coding):.6f}" if coding else "", "interpretation_boundary": "A calibrated coverage estimate remains incomplete until every selected partition row is reviewed."},
    ]
    partitions: dict[tuple[str, str, str], tuple[int, int, int, int]] = {}
    precision: list[dict[str, str]] = []
    for design_row in design:
        label, bucket, scope = text(design_row["target_label"]), text(design_row["source_bucket"]), text(design_row["sampling_scope"])
        population, selected = int(text(design_row["population_count"]) or 0), int(text(design_row["selected_count"]) or 0)
        sample = [row for row in coding if _in_partition(row, label, bucket, scope)]
        if len(sample) != selected:
            raise BroadAbstractAuditError(f"design/sample mismatch for {label} {bucket} {scope}")
        completed = [row for row in sample if text(row.get("coding_status")).lower() == "reviewed"]
        coherent = sum(
            any(human_coherent_edge(row, edge) for edge in CORE_EDGES) if label == CONTROL_LABEL else human_coherent_edge(row, label)
            for row in completed
        )
        state = "complete" if len(completed) == selected else "incomplete"
        partitions[(label, bucket, scope)] = (population, selected, len(completed), coherent)
        precision.append({
            "target_label": label, "source_bucket": bucket, "sampling_scope": scope,
            "population_count": str(population), "selected_count": str(selected), "reviewed_count": str(len(completed)),
            "human_coherent_count": str(coherent), "observed_precision": f"{coherent / len(completed):.6f}" if completed else "",
            "calibration_status": state,
            "interpretation_boundary": "Human coherence evaluates broad abstract-label validity, not direct causal-effect evidence.",
        })
    coverage: list[dict[str, str]] = []
    for edge_index, edge in enumerate(EDGE_ORDER, start=1):
        cells = [row for row in design if text(row["target_label"]) == edge]
        raw, reviewed_n, coherent_n, complete = 0, 0, 0, True
        draws = [0.0] * 20_000
        for cell_index, cell in enumerate(cells, start=1):
            key = (edge, text(cell["source_bucket"]), text(cell["sampling_scope"]))
            population, selected, reviewed_count, correct = partitions[key]
            raw += population
            reviewed_n += reviewed_count
            coherent_n += correct
            if selected != reviewed_count:
                complete = False
                continue
            contribution = _beta_projection(correct, reviewed_count, population, seed + edge_index * 1000 + cell_index)
            draws = [left + right for left, right in zip(draws, contribution)]
        if complete:
            low, high = _interval(draws)
            mean, status = sum(draws) / len(draws), "complete"
            output = (f"{mean:.3f}", f"{low:.3f}", f"{high:.3f}")
        else:
            status, output = "incomplete", ("", "", "")
        coverage.append({
            "target_label": edge, "raw_predicted_candidate_coverage": str(raw), "reviewed_audit_records": str(reviewed_n),
            "human_coherent_audit_records": str(coherent_n), "calibrated_candidate_coverage_mean": output[0],
            "calibrated_candidate_coverage_ci_low": output[1], "calibrated_candidate_coverage_ci_high": output[2],
            "calibration_status": status,
            "interpretation_boundary": "Label-calibrated fixed-corpus abstract coverage, not confirmed causal-study counts or biological effect sizes.",
        })
    controls: list[dict[str, str]] = []
    for bucket in SOURCE_BUCKETS:
        key = (CONTROL_LABEL, bucket, "control_sample")
        if key not in partitions:
            continue
        population, selected, reviewed_count, coherent = partitions[key]
        controls.append({
            "source_bucket": bucket, "population_count": str(population), "selected_count": str(selected),
            "reviewed_count": str(reviewed_count), "human_any_edge_count": str(coherent),
            "observed_undetected_edge_rate": f"{coherent / reviewed_count:.6f}" if reviewed_count else "",
            "calibration_status": "complete" if selected == reviewed_count else "incomplete",
            "interpretation_boundary": "Control estimates missed broad edge labels among flower-context abstracts only.",
        })
    return completion, precision, coverage, controls


def _write_csv(path: Path, fields: Iterable[str], rows: Iterable[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)


def write_audit_packet(out_dir: str | Path, packet: list[dict[str, str]], coding: list[dict[str, str]], design: list[dict[str, str]]) -> None:
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    _write_csv(destination / "broad_abstract_label_audit_packet.csv", PACKET_FIELDS, packet)
    _write_csv(destination / "broad_abstract_label_audit_coding_sheet.csv", CODING_FIELDS, coding)
    _write_csv(destination / "broad_abstract_label_audit_design.csv", DESIGN_FIELDS, design)
    (destination / "README.md").write_text(
        "# Broad abstract label audit packet\n\n"
        "Set `coding_status` to `reviewed` only after completing every human-code field. Binary fields accept `yes`, `no`, `uncertain`, or `not_applicable`. "
        "The packet is fixed-corpus label calibration, not a new literature search.\n",
        encoding="utf-8",
    )


def write_audit_summary(out_dir: str | Path, completion: list[dict[str, str]], precision: list[dict[str, str]], coverage: list[dict[str, str]], control: list[dict[str, str]]) -> None:
    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    _write_csv(destination / "broad_abstract_label_audit_completion.csv", COMPLETION_FIELDS, completion)
    _write_csv(destination / "broad_abstract_label_precision.csv", PRECISION_FIELDS, precision)
    _write_csv(destination / "broad_abstract_edge_coverage_calibrated.csv", COVERAGE_FIELDS, coverage)
    _write_csv(destination / "broad_abstract_negative_control.csv", CONTROL_FIELDS, control)
    (destination / "broad_abstract_label_audit_summary.json").write_text(
        json.dumps({"completion": completion, "precision": precision, "coverage": coverage, "control": control}, indent=2),
        encoding="utf-8",
    )
