"""Measure which data-retrieval routes this environment can actually reach.

The extraction layer is blocked, and the project should record *why* as evidence
rather than as an assertion. This script probes a declared list of hosts that a
literature synthesis would need — bibliographic APIs, full-text archives, data
repositories, publishers, and code-hosting services — and writes a reproducible
audit of which ones answer.

It performs HEAD-equivalent requests only: no content is downloaded, no query is
issued against any service, and nothing is retrieved from a publisher. The point
is to establish reachability, not to fetch anything.

Usage:
    python scripts/audit_data_retrieval_reachability.py artifacts/retrieval_audit [timeout_seconds]

A host is reported as reachable when the request completes with any HTTP status,
including 4xx: a 403 from the origin means the network path works, whereas the
proxy refusing to open the tunnel yields no status at all. The two are recorded
distinctly because they have different remedies.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from trait_architecture.broad_meta_analysis import write_csv_rows


AUDIT_FIELDS = (
    "host", "role", "needed_for", "http_status", "reachable", "note",
)

#: Declared probe list. Each entry names why a literature synthesis would need it.
DECLARED_HOSTS: tuple[tuple[str, str, str], ...] = (
    ("api.crossref.org", "bibliographic_api", "DOI metadata and abstract retrieval for screening"),
    ("api.openalex.org", "bibliographic_api", "corpus-scale candidate discovery and citation graph"),
    ("api.semanticscholar.org", "bibliographic_api", "candidate discovery and reference resolution"),
    ("api.unpaywall.org", "bibliographic_api", "open-access full-text location"),
    ("www.ebi.ac.uk", "fulltext_archive", "Europe PMC search and full text"),
    ("europepmc.org", "fulltext_archive", "Europe PMC full text"),
    ("eutils.ncbi.nlm.nih.gov", "fulltext_archive", "PubMed and PMC programmatic access"),
    ("datadryad.org", "data_repository", "deposited primary datasets for extraction"),
    ("zenodo.org", "data_repository", "deposited primary datasets and supplements"),
    ("figshare.com", "data_repository", "deposited primary datasets and supplements"),
    ("osf.io", "data_repository", "deposited primary datasets and preregistrations"),
    ("dataverse.harvard.edu", "data_repository", "deposited primary datasets"),
    ("api.datacite.org", "data_repository", "dataset DOI metadata"),
    ("onlinelibrary.wiley.com", "publisher", "article and supplementary tables"),
    ("esajournals.onlinelibrary.wiley.com", "publisher", "Ecology and Ecological Monographs"),
    ("besjournals.onlinelibrary.wiley.com", "publisher", "Functional Ecology and Journal of Ecology"),
    ("academic.oup.com", "publisher", "Annals of Botany"),
    ("link.springer.com", "publisher", "Oecologia"),
    ("journals.plos.org", "publisher", "PLOS ONE"),
    ("www.nature.com", "publisher", "Scientific Reports and Nature Communications"),
    ("peerj.com", "publisher", "PeerJ"),
    ("www.biorxiv.org", "preprint", "preprint full text"),
    ("archive.org", "archive", "archived copies of withdrawn or moved sources"),
    ("cran.r-project.org", "package_index", "R packages shipping published meta-analysis data"),
    ("github.com", "code_hosting", "author-deposited data and analysis code (web and search)"),
    ("api.github.com", "code_hosting", "repository metadata and code search"),
    ("raw.githubusercontent.com", "code_hosting", "direct file download from public repositories"),
    ("codeload.github.com", "code_hosting", "repository archive download"),
    ("gitlab.com", "code_hosting", "author-deposited data and analysis code"),
    ("bitbucket.org", "code_hosting", "author-deposited data and analysis code"),
    ("pypi.org", "package_index", "Python packages shipping datasets"),
)


def probe(host: str, timeout: int) -> tuple[str, bool, str]:
    """Return (status, reachable, note) for one host without downloading content."""

    result = subprocess.run(
        [
            "curl", "-sS", "--max-time", str(timeout), "-o", "/dev/null",
            "-w", "%{http_code}", f"https://{host}/",
        ],
        capture_output=True,
        text=True,
    )
    status = (result.stdout or "").strip().splitlines()[-1] if result.stdout.strip() else "000"
    stderr = (result.stderr or "").strip()
    if status == "000":
        note = "no HTTP status: the egress proxy refused to open the tunnel"
        if "403" in stderr:
            note = "egress proxy answered 403 to CONNECT (organization policy denial)"
        return status, False, note
    return status, True, "origin answered; network path is open"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_dir")
    parser.add_argument("timeout_seconds", nargs="?", type=int, default=12)
    args = parser.parse_args(argv)

    destination = Path(args.out_dir)
    destination.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    for host, role, needed_for in DECLARED_HOSTS:
        status, reachable, note = probe(host, args.timeout_seconds)
        rows.append({
            "host": host,
            "role": role,
            "needed_for": needed_for,
            "http_status": status,
            "reachable": "true" if reachable else "false",
            "note": note,
        })

    write_csv_rows(destination / "retrieval_reachability.csv", AUDIT_FIELDS, rows)

    by_role: dict[str, dict[str, int]] = {}
    for row in rows:
        counts = by_role.setdefault(str(row["role"]), {"reachable": 0, "blocked": 0})
        counts["reachable" if row["reachable"] == "true" else "blocked"] += 1

    summary = {
        "hosts_probed": len(rows),
        "reachable": sum(row["reachable"] == "true" for row in rows),
        "blocked": sum(row["reachable"] == "false" for row in rows),
        "by_role": by_role,
        "reachable_hosts": [row["host"] for row in rows if row["reachable"] == "true"],
        "bibliographic_api_reachable": any(
            row["reachable"] == "true" and row["role"] == "bibliographic_api" for row in rows
        ),
        "data_repository_reachable": any(
            row["reachable"] == "true" and row["role"] == "data_repository" for row in rows
        ),
        "interpretation_boundary": (
            "This audit records the network reachability of declared hosts at the time it was run. "
            "It is a property of the execution environment's egress policy, not of the literature. "
            "A blocked host says nothing about whether the data exist."
        ),
    }
    (destination / "retrieval_reachability_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
