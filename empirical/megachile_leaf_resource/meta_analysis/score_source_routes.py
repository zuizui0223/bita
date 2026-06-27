"""Score evidence-first source routes after manual study-card screening.

Usage:
    python score_source_routes.py study_cards.csv

The script deliberately evaluates source routes, not papers. It does not infer
E1/E2/E3 eligibility from titles or abstracts; reviewers enter those fields.
"""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path


def yes(value: str) -> bool:
    return value.strip().casefold() in {"yes", "true", "1"}


def main(path: str) -> int:
    rows = list(csv.DictReader(Path(path).open(encoding="utf-8")))
    rows = [r for r in rows if r.get("source_id", "").strip() and not r["source_id"].startswith("EXAMPLE_")]
    routes: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        routes[row.get("source_route", "unknown") or "unknown"].append(row)

    for route, cards in sorted(routes.items()):
        screened = [c for c in cards if c.get("screen_status", "").strip() not in {"", "unscreened"}]
        e1 = sum(yes(c.get("E1_eligible", "")) for c in screened)
        e2 = sum(yes(c.get("E2_eligible", "")) for c in screened)
        e3 = sum(yes(c.get("E3_eligible", "")) for c in screened)
        high = sum(bool(c.get("high_information_reason", "").strip()) for c in screened)
        decision = "continue_to_15_cards"
        if len(screened) >= 15:
            if e2 + e3 >= 3:
                decision = "expand_and_citation_chase"
            elif e2 + e3 >= 1:
                decision = "retain_secondary_harvest_links_then_pivot"
            elif e1 >= 3:
                decision = "retain_E1_ledger_only_then_pivot"
            else:
                decision = "stop_primary_route"
        print(f"{route}: screened={len(screened)} high_information={high} E1={e1} E2={e2} E3={e3} decision={decision}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python score_source_routes.py path/to/study_cards.csv")
    raise SystemExit(main(sys.argv[1]))
