"""Rank-binned retrieval diagnostics for the broad Crossref evidence corpus.

The broad corpus is deliberately high recall. A retrieval cap therefore cannot be
interpreted as an exhaustive search, and a larger cap should not be chosen solely
because the existing cap was reached. This module records metadata-screen yield
for every retrieved rank page within each existing query. It provides a transparent
saturation diagnostic for deciding whether a deeper retrieval is worth the
additional source-coding workload.

The diagnostic is strictly bibliographic/metadata based. It does not establish
that a study measured an arrow, reported an effect, or should be included in a
meta-analysis.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .broad_reality_evidence import Candidate
from .broad_reality_screen import screen_row


DEPTH_SATURATION_FIELDS = (
    "query_id",
    "route_family",
    "rank_start",
    "rank_end",
    "raw_records_returned",
    "candidate_memberships",
    "priority_memberships",
    "biological_context_memberships",
    "uncertain_context_memberships",
    "likely_nonbiological_memberships",
    "priority_membership_rate",
    "interpretation_boundary",
)

INTERPRETATION_BOUNDARY = (
    "Counts are retrieved query memberships after metadata-only screening. They do "
    "not establish direct-route measurement, effect direction, effect size, study "
    "eligibility, or a stopping rule for the literature search."
)


@dataclass
class DepthSaturationCollector:
    """Collect rank-page metadata yields as a paged harvest proceeds."""

    bin_size: int
    records: list[dict[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.bin_size < 1:
            raise ValueError("bin_size must be positive")

    def observe(
        self,
        query: dict[str, str],
        offset: int,
        candidates: list[Candidate],
        raw_records_returned: int,
    ) -> None:
        """Record one Crossref rank page before candidate-level deduplication.

        ``candidates`` contains valid title-bearing candidate memberships from the
        page. A work retrieved by more than one query is intentionally counted once
        per query membership here: the question is page yield within each query,
        not corpus-wide unique-study prevalence.
        """

        if offset < 0:
            raise ValueError("offset must be non-negative")
        if raw_records_returned < 0:
            raise ValueError("raw_records_returned must be non-negative")
        if raw_records_returned == 0:
            return
        if raw_records_returned > self.bin_size:
            raise ValueError("one observed page cannot exceed the configured bin_size")

        screened = [screen_row(candidate.to_row()) for candidate in candidates]
        statuses = Counter(row["shallow_screen_status"] for row in screened)
        membership_count = len(screened)
        priority = statuses["priority_for_shallow_source_coding"]
        self.records.append({
            "query_id": query["query_id"],
            "route_family": query["route_family"],
            "rank_start": str(offset + 1),
            "rank_end": str(offset + raw_records_returned),
            "raw_records_returned": str(raw_records_returned),
            "candidate_memberships": str(membership_count),
            "priority_memberships": str(priority),
            "biological_context_memberships": str(statuses["biological_context_needs_route_screen"]),
            "uncertain_context_memberships": str(statuses["metadata_context_uncertain"]),
            "likely_nonbiological_memberships": str(statuses["likely_nonbiological_retrieval_noise"]),
            "priority_membership_rate": f"{(priority / membership_count) if membership_count else 0.0:.6f}",
            "interpretation_boundary": INTERPRETATION_BOUNDARY,
        })

    def ordered_records(self) -> list[dict[str, str]]:
        return sorted(
            self.records,
            key=lambda row: (row["route_family"], row["query_id"], int(row["rank_start"])),
        )

    def summary(self) -> dict[str, object]:
        """Summarise head/tail metadata yield without imposing a stopping rule."""

        rows = self.ordered_records()
        total_memberships = sum(int(row["candidate_memberships"]) for row in rows)
        total_priority = sum(int(row["priority_memberships"]) for row in rows)
        by_rank_bin: dict[str, dict[str, int]] = defaultdict(
            lambda: {"candidate_memberships": 0, "priority_memberships": 0}
        )
        for row in rows:
            key = f"{row['rank_start']}-{row['rank_end']}"
            by_rank_bin[key]["candidate_memberships"] += int(row["candidate_memberships"])
            by_rank_bin[key]["priority_memberships"] += int(row["priority_memberships"])

        rank_bin_summary = {
            key: {
                **counts,
                "priority_membership_rate": (
                    counts["priority_memberships"] / counts["candidate_memberships"]
                    if counts["candidate_memberships"] else 0.0
                ),
            }
            for key, counts in sorted(
                by_rank_bin.items(), key=lambda item: int(item[0].split("-", 1)[0])
            )
        }
        return {
            "query_count": len({row["query_id"] for row in rows}),
            "page_count": len(rows),
            "bin_size": self.bin_size,
            "retrieved_candidate_memberships": total_memberships,
            "priority_memberships": total_priority,
            "overall_priority_membership_rate": (
                total_priority / total_memberships if total_memberships else 0.0
            ),
            "by_rank_bin": rank_bin_summary,
            "decision_boundary": (
                "Do not automatically increase or stop retrieval from metadata yield. "
                "Compare head and tail yields, then adjudicate a route-balanced sample "
                "from the tail before changing the depth cap."
            ),
            "interpretation_boundary": INTERPRETATION_BOUNDARY,
        }


def write_depth_saturation_outputs(
    out_dir: str | Path,
    collector: DepthSaturationCollector,
) -> None:
    """Write the rank-binned table and its explicitly non-decisive summary."""

    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "broad_reality_evidence_depth_saturation.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=DEPTH_SATURATION_FIELDS)
        writer.writeheader()
        writer.writerows(collector.ordered_records())
    (destination / "broad_reality_evidence_depth_saturation_summary.json").write_text(
        json.dumps(collector.summary(), indent=2, sort_keys=True), encoding="utf-8"
    )
