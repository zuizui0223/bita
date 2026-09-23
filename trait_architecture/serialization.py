"""Canonical serialization helpers for generated BITA scientific receipts.

These helpers are for generated outputs only. Raw/source analysis inputs must
remain byte-exact and are never quantized through this module.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

GENERATED_FLOAT_SIGNIFICANT_DIGITS = 15


def canonicalize_generated_floats(value: object) -> object:
    """Normalize runtime-only final-bit differences in generated output floats."""
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("generated JSON contains non-finite float")
        return float(format(value, f".{GENERATED_FLOAT_SIGNIFICANT_DIGITS}g"))
    if isinstance(value, dict):
        return {
            key: canonicalize_generated_floats(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [canonicalize_generated_floats(item) for item in value]
    if isinstance(value, tuple):
        return [canonicalize_generated_floats(item) for item in value]
    return value


def generated_json_text(payload: object) -> str:
    canonical = canonicalize_generated_floats(payload)
    return json.dumps(canonical, indent=2, sort_keys=True) + "\n"


def write_generated_json(path: str | Path, payload: object) -> object:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    canonical = canonicalize_generated_floats(payload)
    output.write_text(
        json.dumps(canonical, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return canonical
