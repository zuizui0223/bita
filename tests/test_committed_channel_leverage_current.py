"""Guard the committed value-of-information result.

The full ranking crosses four parameter scenarios and four response-shape
variants, which is too slow for a unit test, so it follows the repository's Part I
convention: the expensive analysis is committed as an artifact and the tests check
that artifact for internal consistency and for the claim the readout makes.

Regenerate with:

    python scripts/run_channel_leverage.py \
      configs/part_i_robustness_grid.json empirical/channel_leverage 0.25
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEVERAGE = ROOT / "empirical" / "channel_leverage"


def _rows(name: str) -> list[dict[str, str]]:
    with (LEVERAGE / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _voi(total: int, settled: int, sensitive: int) -> float:
    return max(0.0, settled / total - (total - sensitive) / total)


def test_committed_ranking_covers_every_declared_channel() -> None:
    ranking = _rows("channel_leverage_ranking.csv")

    assert len(ranking) == 5
    assert {row["channel"] for row in ranking} == {
        "antagonist_relief_rho",
        "mutualist_interference_iota",
        "direct_joint_cost_kappa",
    }
    assert [int(row["rank"]) for row in ranking] == [1, 2, 3, 4, 5]
    scores = [float(row["value_of_information"]) for row in ranking]
    assert scores == sorted(scores, reverse=True)


def test_committed_ranking_matches_the_committed_grid() -> None:
    grid = _rows("channel_leverage_grid.csv")
    ranking = _rows("channel_leverage_ranking.csv")

    pooled: dict[str, list[int]] = defaultdict(lambda: [0, 0, 0])
    for row in grid:
        if row["relative_half_width"] != "0.25":
            continue
        totals = pooled[row["parameter"]]
        totals[0] += int(row["grid_points"])
        totals[1] += int(row["settled_points"])
        totals[2] += int(row["prior_sensitive_points"])

    for row in ranking:
        total, settled, sensitive = pooled[row["parameter"]]
        assert int(row["grid_points"]) == total
        assert abs(float(row["value_of_information"]) - _voi(total, settled, sensitive)) < 1e-6


def test_relief_tracking_leads_every_response_shape_variant() -> None:
    """The headline result, and the reason the readout recommends a next target.

    The declared empirical target measures the interference channel because that
    literature is tractable. It is not the highest-leverage measurement, and the
    ordering does not depend on which endpoint-normalized response shape is used.
    """

    grid = _rows("channel_leverage_grid.csv")
    by_form: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(lambda: [0, 0, 0]))
    for row in grid:
        if row["relative_half_width"] != "0.25":
            continue
        totals = by_form[row["form_id"]][row["parameter"]]
        totals[0] += int(row["grid_points"])
        totals[1] += int(row["settled_points"])
        totals[2] += int(row["prior_sensitive_points"])

    assert len(by_form) == 4
    for form_id, parameters in by_form.items():
        ordered = sorted(
            ((_voi(*totals), name) for name, totals in parameters.items()), reverse=True
        )
        assert ordered[0][1] == "attraction_tracking", form_id

    ranking = _rows("channel_leverage_ranking.csv")
    target = next(row for row in ranking if row["parameter"] == "defence_pollinator_cost")
    assert int(target["rank"]) > 1


def test_committed_diagnostics_agree_with_the_committed_ranking() -> None:
    diagnostics = json.loads((LEVERAGE / "channel_leverage_diagnostics.json").read_text(encoding="utf-8"))
    ranking = _rows("channel_leverage_ranking.csv")

    assert diagnostics["top_parameter"] == ranking[0]["parameter"]
    assert diagnostics["top_channel"] == ranking[0]["channel"]
    assert diagnostics["declared_target_parameter"] == "defence_pollinator_cost"
    target = next(row for row in ranking if row["parameter"] == "defence_pollinator_cost")
    assert diagnostics["declared_target_rank"] == int(target["rank"])
