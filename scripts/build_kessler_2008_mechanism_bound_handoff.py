from __future__ import annotations

import argparse
import json
from math import inf
from pathlib import Path

from trait_architecture.partial_identification import (
    Interval,
    partial_identification_from_total_bounds,
)


def build_report(source_json: Path) -> dict[str, object]:
    source = json.loads(source_json.read_text(encoding="utf-8"))
    profiles = source["profiles"]
    if not profiles:
        raise ValueError("aggregate-bound source contains no profiles")

    delta_lower = min(float(p["probability_delta_min"]) for p in profiles)
    delta_bounds = Interval(delta_lower, inf)

    unconditional = partial_identification_from_total_bounds(delta_bounds)
    conditional = partial_identification_from_total_bounds(
        delta_bounds,
        kappa_bounds=Interval(0.0, inf),
    )
    if not unconditional.feasible or not conditional.feasible or conditional.biotic_balance is None:
        raise ValueError("registered Kessler bounds produced an infeasible handoff")

    return {
        "analysis_id": "kessler_2008_mechanism_bound_handoff_v1",
        "source_analysis_id": source.get("analysis_id"),
        "source_workflow_run": source.get("workflow_run"),
        "delta_ad_lower_bound": delta_lower,
        "delta_ad_upper_bound_used": None,
        "conditional_restriction": "kappa_delta >= 0",
        "conditional_biotic_balance_lower_bound": conditional.biotic_balance.low,
        "conditional_biotic_balance_upper_bound": None,
        "unconditional_channel_allocation": "NOT_POINT_IDENTIFIED",
        "rho_delta": "NOT_POINT_IDENTIFIED",
        "iota_delta": "NOT_POINT_IDENTIFIED",
        "kappa_delta": "SIGN_RESTRICTED_ONLY_NOT_POINT_IDENTIFIED",
        "channel_allocation": "NOT_POINT_IDENTIFIED",
        "claim_boundary": (
            "This is a conditional partial-identification bound obtained by propagating the registered "
            "aggregate lower bound on Delta_AD W through rho_delta-iota_delta=Delta_AD W+kappa_delta. "
            "It is not a measured channel effect, does not point-identify rho_delta or iota_delta, and "
            "does not upgrade Kessler 2008 to Level-2 or Level-3 release."
        ),
    }


def render_markdown(report: dict[str, object]) -> str:
    lower = float(report["delta_ad_lower_bound"])
    balance_lower = float(report["conditional_biotic_balance_lower_bound"])
    return f"""# Kessler 2008 mechanism-bound handoff V1

## Decision

The registered aggregate sensitivity analysis supplies a robust probability-scale lower bound on the total attraction-by-defence interaction. Propagating only that lower bound through BITA's mechanism identity yields one additional quantitative result under an explicit channel restriction.

```text
DELTA_AD_W_LOWER_BOUND = +{lower:.7f}
ASSUMPTION = kappa_delta >= 0
KESSLER_CONDITIONAL_BIOTIC_BALANCE_LOWER_BOUND = +{balance_lower:.7f}
RHO_DELTA = NOT_POINT_IDENTIFIED
IOTA_DELTA = NOT_POINT_IDENTIFIED
CHANNEL_ALLOCATION = NOT_POINT_IDENTIFIED
```

Because

```text
rho_delta - iota_delta = Delta_AD W + kappa_delta,
```

`kappa_delta >= 0` implies

```text
rho_delta - iota_delta >= +{balance_lower:.7f}.
```

This is a **conditional partial-identification bound** on the contrast between antagonist relief and pollinator interference. It is not a measured channel effect, and neither `rho_delta` nor `iota_delta` is separately bounded by this restriction alone.

## Why this is stronger than a sign statement

The previous Kessler result established that the total interaction remains positive over the registered aggregate-compatible denominator profiles. The handoff now carries the worst-case lower edge of that identified set into mechanism space. Under the declared `kappa_delta >= 0` restriction, the biotic balance must exceed the total-interaction floor rather than merely being positive.

## Claim ceiling

This result does **not** establish that `kappa_delta >= 0` is empirically measured in Kessler et al. (2008). The restriction is assumption-indexed. It also does not identify strict Level-2 constraint release, Level-3 reversal, or the individual ecological channels. Those claims remain governed by the existing Stage-1 and mechanism-identification gates.

## Provenance

```text
analysis: {report['analysis_id']}
source analysis: {report['source_analysis_id']}
source workflow run: {report['source_workflow_run']}
source file: KESSLER_2008_AGGREGATE_BOUNDS_V1.json
```
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_json", type=Path)
    parser.add_argument("output_markdown", type=Path)
    args = parser.parse_args()

    report = build_report(args.source_json)
    args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
    args.output_markdown.write_text(render_markdown(report), encoding="utf-8")


if __name__ == "__main__":
    main()
