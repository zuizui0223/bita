"""Execute the pre-registered search against Europe PMC and write the log.

This is the piece the web execution environment could not run. Its egress policy
refuses every bibliographic host, so the declared search had to be executed
through a connector that caps boolean operators at 20 and serves metadata in
truncated batches. Run from a machine with ordinary network access, this script
executes the declared query **as declared** — Europe PMC's REST API imposes no
operator cap, so the decomposition amendment recorded in
`IOTA_PATHWAY_SEARCH_EXECUTION_V1.md` is not needed here.

It writes, in the committed schema:

- `search_log.csv`      one row per declared query, with counts and the run date
- `search_hits.csv`     one row per retrieved record, with identifiers and OA status
- `search_diagnostics.json`

It deliberately does **not** screen, extract, or code anything. Screening is a
judgement made against the declared criteria in
`IOTA_PATHWAY_EXTRACTION_PROTOCOL_v1.md`, and effect extraction requires reading
the full text. This script only turns the declared query into a retrieved,
logged record set.

Usage:
    python scripts/fetch_declared_search.py empirical/broad_reality_evidence/iota_pathway/local_run
    python scripts/fetch_declared_search.py OUT_DIR --queries c_D d_A --page-size 1000

Network: needs `www.ebi.ac.uk` only. No key, no account. If the host is
unreachable the script says so plainly and exits non-zero rather than writing a
partial log that could be mistaken for a completed search.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

from trait_architecture.broad_meta_analysis import write_csv_rows


EUROPE_PMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

LOG_FIELDS = (
    "query_id", "run_date", "database", "query_string", "hit_count",
    "records_retrieved", "status", "note",
)
HIT_FIELDS = (
    "query_id", "pmid", "pmcid", "doi", "title", "journal", "year",
    "is_open_access", "has_full_text_in_pmc", "source",
)

#: The declared queries, verbatim from IOTA_PATHWAY_SEARCH_STRATEGY_v1.md.
#: Europe PMC accepts them whole; do not decompose them here.
DECLARED_QUERIES: dict[str, str] = {
    "c_D": (
        '(ABSTRACT:"nectar" OR ABSTRACT:"pollen" OR ABSTRACT:"floral" OR ABSTRACT:"flower" '
        'OR ABSTRACT:"flowers" OR TITLE:"nectar" OR TITLE:"floral" OR TITLE:"flower")'
        ' AND (ABSTRACT:"alkaloid" OR ABSTRACT:"alkaloids" OR ABSTRACT:"secondary metabolite" '
        'OR ABSTRACT:"secondary metabolites" OR ABSTRACT:"secondary compound" '
        'OR ABSTRACT:"secondary compounds" OR ABSTRACT:"toxin" OR ABSTRACT:"toxins" '
        'OR ABSTRACT:"nicotine" OR ABSTRACT:"caffeine" OR ABSTRACT:"amygdalin" '
        'OR ABSTRACT:"grayanotoxin" OR ABSTRACT:"gelsemine" OR ABSTRACT:"anabasine" '
        'OR ABSTRACT:"iridoid" OR ABSTRACT:"phenolic")'
        ' AND (ABSTRACT:"pollinator" OR ABSTRACT:"pollinators" OR ABSTRACT:"pollination" '
        'OR ABSTRACT:"bee" OR ABSTRACT:"bees" OR ABSTRACT:"bumblebee" OR ABSTRACT:"bumblebees" '
        'OR ABSTRACT:"Bombus" OR ABSTRACT:"Apis mellifera" OR ABSTRACT:"hummingbird" '
        'OR ABSTRACT:"visitation" OR ABSTRACT:"foraging" OR ABSTRACT:"preference" '
        'OR ABSTRACT:"consumption")'
    ),
    "d_A": (
        '(ABSTRACT:"floral" OR ABSTRACT:"flower" OR ABSTRACT:"flowers" '
        'OR ABSTRACT:"inflorescence" OR ABSTRACT:"inflorescences")'
        ' AND (ABSTRACT:"display size" OR ABSTRACT:"flower number" OR ABSTRACT:"flower size" '
        'OR ABSTRACT:"corolla size" OR ABSTRACT:"color" OR ABSTRACT:"colour" '
        'OR ABSTRACT:"scent" OR ABSTRACT:"volatile" OR ABSTRACT:"volatiles" '
        'OR ABSTRACT:"floral signal" OR ABSTRACT:"attractiveness")'
        ' AND (ABSTRACT:"florivory" OR ABSTRACT:"florivore" OR ABSTRACT:"florivores" '
        'OR ABSTRACT:"floral herbivory" OR ABSTRACT:"flower damage" '
        'OR ABSTRACT:"bud predation" OR ABSTRACT:"seed predation" OR ABSTRACT:"herbivory" '
        'OR ABSTRACT:"nectar robbing")'
    ),
}


def _request(query: str, page_size: int, cursor: str) -> dict:
    params = urllib.parse.urlencode({
        "query": query,
        "format": "json",
        "pageSize": str(page_size),
        "cursorMark": cursor,
        "resultType": "core",
    })
    request = urllib.request.Request(
        f"{EUROPE_PMC}?{params}",
        headers={"User-Agent": "bita-declared-search (research use; contact via repository)"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def run_query(query_id: str, query: str, page_size: int, max_records: int) -> tuple[dict, list[dict]]:
    cursor = "*"
    hits: list[dict[str, object]] = []
    hit_count = 0
    while True:
        payload = _request(query, page_size, cursor)
        hit_count = int(payload.get("hitCount", 0))
        results = payload.get("resultList", {}).get("result", [])
        for record in results:
            hits.append({
                "query_id": query_id,
                "pmid": record.get("pmid", ""),
                "pmcid": record.get("pmcid", ""),
                "doi": record.get("doi", ""),
                "title": (record.get("title", "") or "").replace("\n", " ").strip(),
                "journal": record.get("journalTitle", ""),
                "year": record.get("pubYear", ""),
                "is_open_access": record.get("isOpenAccess", ""),
                "has_full_text_in_pmc": record.get("inPMC", ""),
                "source": record.get("source", ""),
            })
        next_cursor = payload.get("nextCursorMark")
        if not results or not next_cursor or next_cursor == cursor or len(hits) >= min(hit_count, max_records):
            break
        cursor = next_cursor

    log = {
        "query_id": query_id,
        "run_date": date.today().isoformat(),
        "database": "Europe PMC",
        "query_string": query,
        "hit_count": hit_count,
        "records_retrieved": len(hits),
        "status": "executed",
        "note": (
            "Declared query executed whole; Europe PMC imposes no boolean-operator cap, "
            "so the connector decomposition amendment does not apply to this run."
        ),
    }
    return log, hits


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_dir")
    parser.add_argument("--queries", nargs="*", default=sorted(DECLARED_QUERIES))
    parser.add_argument("--page-size", type=int, default=1000)
    parser.add_argument("--max-records", type=int, default=5000)
    args = parser.parse_args(argv)

    unknown = [name for name in args.queries if name not in DECLARED_QUERIES]
    if unknown:
        parser.error(f"undeclared query id(s): {', '.join(unknown)}")

    logs: list[dict[str, object]] = []
    hits: list[dict[str, object]] = []
    for query_id in args.queries:
        try:
            log, query_hits = run_query(
                query_id, DECLARED_QUERIES[query_id], args.page_size, args.max_records
            )
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as error:
            print(
                f"Europe PMC is unreachable from this machine: {error}\n"
                "Nothing was written. This script needs ordinary outbound access to "
                "www.ebi.ac.uk; the web execution environment's egress policy refuses it. "
                "Run it locally, or widen the environment's network policy.",
                file=sys.stderr,
            )
            return 2
        logs.append(log)
        hits.extend(query_hits)

    destination = Path(args.out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    write_csv_rows(destination / "search_log.csv", LOG_FIELDS, logs)
    write_csv_rows(destination / "search_hits.csv", HIT_FIELDS, hits)

    open_access = sum(1 for row in hits if str(row["is_open_access"]).upper() == "Y")
    in_pmc = sum(1 for row in hits if str(row["has_full_text_in_pmc"]).upper() == "Y")
    diagnostics = {
        "run_date": date.today().isoformat(),
        "queries_executed": args.queries,
        "records_retrieved": len(hits),
        "open_access_records": open_access,
        "records_with_pmc_full_text": in_pmc,
        "interpretation_boundary": (
            "This is a retrieval log, not a screening result and not evidence. No record here "
            "has been screened against the declared inclusion criteria, and no effect has been "
            "extracted. Screening and extraction remain manual steps under "
            "IOTA_PATHWAY_EXTRACTION_PROTOCOL_v1.md."
        ),
    }
    (destination / "search_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(diagnostics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
