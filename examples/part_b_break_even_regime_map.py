"""Empirically informed regime map via the Part B break-even bound (layer B4).

This demonstrates how B2 channel envelopes plus declared shared-cost scenarios
produce a regime label per local case, without ever estimating ``c_AD``. The
channel-parameter values below are placeholder low/mid/high envelopes standing in
for the eventual B2 pooled arrows; replace them with the real per-arrow envelopes
once ``parameter_envelopes.ready_parameter_overrides`` returns calibrated values.
"""

from __future__ import annotations

import csv
from pathlib import Path

from trait_architecture.part_b_support import envelope_break_even_map
from trait_architecture.robustness import cartesian_cases


# Placeholder channel envelopes (b_A, d_A, e_F, c_D). NOT calibrated values — a
# transparent low/mid/high illustration of the B4 mechanics only.
PLACEHOLDER_CHANNEL_ENVELOPES = {
    "low_tracking": {
        "attraction_gain": 1.2,
        "attraction_tracking": 0.4,
        "floral_defence_efficacy": 0.5,
        "defence_pollinator_cost": 0.6,
    },
    "baseline": {
        "attraction_gain": 1.2,
        "attraction_tracking": 1.1,
        "floral_defence_efficacy": 0.75,
        "defence_pollinator_cost": 0.45,
    },
    "high_tracking": {
        "attraction_gain": 1.2,
        "attraction_tracking": 1.6,
        "floral_defence_efficacy": 0.9,
        "defence_pollinator_cost": 0.3,
    },
}
# Declared shared-cost sensitivity scenarios (never estimated from data).
SHARED_COST_SCENARIOS = (0.0, 0.1, 0.3)


if __name__ == "__main__":
    cases = cartesian_cases(
        attraction=(0.2, 0.5, 0.8),
        defence=(0.2, 0.5, 0.8),
        assurance=(0.0, 0.5),
        pollinator_service=(0.2, 0.5, 0.8),
        floral_damage_pressure=(0.2, 0.5, 0.8),
    )
    rows = envelope_break_even_map(
        cases,
        PLACEHOLDER_CHANNEL_ENVELOPES,
        shared_cost_scenarios=SHARED_COST_SCENARIOS,
    )
    fieldnames = list(rows[0].keys()) if rows else []
    destination = Path("part_b_break_even_regime_map.csv")
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    scenario_col = f"regime_at_c_AD_{SHARED_COST_SCENARIOS[1]:g}"
    complementary = sum(1 for row in rows if row.get(scenario_col) == "complementary")
    print(
        f"wrote {len(rows)} envelope-level x case rows to {destination}; "
        f"{complementary}/{len(rows)} complementary at c_AD={SHARED_COST_SCENARIOS[1]:g} "
        "(placeholder envelopes - not a calibrated result)"
    )
