"""Planning-only sensitivity simulation for the route-cost factorial experiment.

This script does not define confirmatory inference. It approximates design sensitivity
under a logistic random-intercept data-generating model and a paired normal
approximation to the two bee-level primary contrasts. The confirmatory analysis
remains the preregistered bee-level sign-flip randomization.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

BASELINE_BYPASS = 0.40
RANDOM_INTERCEPT_SD = 0.80
TRIALS_PER_CONDITION = 10
ALPHA_EACH = 0.025
DEFAULT_N = 60
DEFAULT_REPS = 5000
DEFAULT_SHIFTS = (0.35, 0.45, 0.55, 0.70)
SEED = 20260929


def _logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def _expit(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def _binomial(rng: random.Random, n: int, p: float) -> int:
    return sum(rng.random() < p for _ in range(n))


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _sd(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = _mean(values)
    return math.sqrt(sum((x - mean) ** 2 for x in values) / (len(values) - 1))


def _normal_one_sided_p(values: list[float], direction: str) -> float:
    mean = _mean(values)
    sd = _sd(values)
    if sd == 0.0:
        if direction == "greater":
            return 0.0 if mean > 0 else 1.0
        return 0.0 if mean < 0 else 1.0
    z = mean / (sd / math.sqrt(len(values)))
    cdf = 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
    return 1.0 - cdf if direction == "greater" else cdf


def simulate_scenario(
    *,
    n_bees: int,
    logit_shift: float,
    reps: int,
    seed: int,
) -> dict[str, float]:
    rng = random.Random(seed)
    base = _logit(BASELINE_BYPASS)
    passed = 0
    c_l_values: list[float] = []
    c_b_values: list[float] = []

    for _ in range(reps):
        d_l: list[float] = []
        d_b: list[float] = []
        for _bee in range(n_bees):
            intercept = rng.gauss(0.0, RANDOM_INTERCEPT_SD)
            p_ll = _expit(base + intercept)
            p_hl = _expit(base + intercept + logit_shift)
            p_lh = _expit(base + intercept - logit_shift)

            y_ll = _binomial(rng, TRIALS_PER_CONDITION, p_ll) / TRIALS_PER_CONDITION
            y_hl = _binomial(rng, TRIALS_PER_CONDITION, p_hl) / TRIALS_PER_CONDITION
            y_lh = _binomial(rng, TRIALS_PER_CONDITION, p_lh) / TRIALS_PER_CONDITION
            d_l.append(y_hl - y_ll)
            d_b.append(y_lh - y_ll)

        c_l = _mean(d_l)
        c_b = _mean(d_b)
        c_l_values.append(c_l)
        c_b_values.append(c_b)
        if (
            c_l > 0
            and c_b < 0
            and _normal_one_sided_p(d_l, "greater") < ALPHA_EACH
            and _normal_one_sided_p(d_b, "less") < ALPHA_EACH
        ):
            passed += 1

    return {
        "n_bees": n_bees,
        "logit_shift": logit_shift,
        "mean_C_L": _mean(c_l_values),
        "mean_C_B": _mean(c_b_values),
        "approx_joint_primary_pass_probability": passed / reps,
    }


def run(output: str | Path, *, reps: int = DEFAULT_REPS, seed: int = SEED) -> dict[str, object]:
    scenarios = []
    for i, shift in enumerate(DEFAULT_SHIFTS):
        scenarios.append(
            simulate_scenario(
                n_bees=DEFAULT_N,
                logit_shift=shift,
                reps=reps,
                seed=seed + i,
            )
        )

    result = {
        "analysis_name": "relative_route_cost_factorial_planning_sensitivity",
        "status": "PLANNING_ONLY_NOT_CONFIRMATORY_INFERENCE",
        "assumptions": {
            "baseline_bypass_probability": BASELINE_BYPASS,
            "bee_random_intercept_sd_logit": RANDOM_INTERCEPT_SD,
            "trials_per_condition": TRIALS_PER_CONDITION,
            "n_bees": DEFAULT_N,
            "alpha_each_primary_contrast": ALPHA_EACH,
            "data_generating_effect": (
                "symmetric +/- logit shift for legitimate-cost and bypass-cost manipulations"
            ),
        },
        "scenarios": scenarios,
        "reps": reps,
        "seed": seed,
        "claim_boundary": (
            "These Monte Carlo values justify design sensitivity only. The final "
            "experiment uses bee-level sign-flip randomization, not this normal approximation."
        ),
    }
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--reps", type=int, default=DEFAULT_REPS)
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args()
    print(json.dumps(run(args.output, reps=args.reps, seed=args.seed), indent=2, sort_keys=True))
