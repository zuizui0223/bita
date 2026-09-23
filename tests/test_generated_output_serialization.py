from __future__ import annotations

from trait_architecture.serialization import (
    GENERATED_FLOAT_SIGNIFICANT_DIGITS,
    canonicalize_generated_floats,
    generated_json_text,
)


def test_generated_float_canonicalization_removes_final_bit_runtime_noise() -> None:
    a = 0.953948731313742
    b = 0.9539487313137417

    ca = canonicalize_generated_floats({"rho": a})
    cb = canonicalize_generated_floats({"rho": b})

    assert GENERATED_FLOAT_SIGNIFICANT_DIGITS == 15
    assert ca == cb
    assert generated_json_text({"rho": a}) == generated_json_text({"rho": b})


def test_generated_float_canonicalization_is_recursive_but_non_numeric_values_survive() -> None:
    payload = {
        "nested": [0.12345678901234567, {"label": "x", "count": 3}],
        "flag": True,
    }
    canonical = canonicalize_generated_floats(payload)
    assert canonical["nested"][0] == float(format(payload["nested"][0], ".15g"))
    assert canonical["nested"][1] == {"label": "x", "count": 3}
    assert canonical["flag"] is True
