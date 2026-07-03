"""Scout DOI-exact public article and repository routes for the fixed c_D queue.

Usage:
    python scripts/scout_c_d_public_sources.py \
      empirical/broad_reality_evidence/precision_expansions/fulltext/B_TO_P_FULLTEXT_READING_QUEUE_v1.csv \
      artifacts/c_d_public_sources \
      --unpaywall-email actions@users.noreply.github.com

Receipts distinguish publisher links, OpenAlex and Unpaywall public-fulltext
candidates, and linked repositories. They are access leads only and do not extract
effects.
"""

from __future__ import annotations

import argparse
import json

from trait_architecture.c_d_public_source_scout import scout_queue_file
from trait_architecture.public_article_source_scout import _fetch_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("queue_csv")
    parser.add_argument("out_dir")
    parser.add_argument("--unpaywall-email", required=True)
    args = parser.parse_args(argv)
    report = scout_queue_file(
        args.queue_csv,
        args.out_dir,
        fetch_json=_fetch_json,
        unpaywall_email=args.unpaywall_email,
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
