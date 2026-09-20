from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LETTER = ROOT / "manuscript" / "MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md"


def _main_words(text: str) -> list[str]:
    body = re.sub(r"~~~[\s\S]*?~~~", " ", text)
    body = re.sub(r"\\\[[\s\S]*?\\\]", " ", body)
    body = re.sub(r"^#.*$", " ", body, flags=re.MULTILINE)
    body = body.replace("**", "")
    return [token for token in re.split(r"\s+", body.strip()) if token]


def _abstract_words(text: str) -> list[str]:
    match = re.search(r"## Abstract\n\n([\s\S]*?)\n\n## Introduction", text)
    assert match is not None
    body = re.sub(r"\\\([^)]*\\\)", " ", match.group(1))
    body = body.replace("**", "")
    return [token for token in re.split(r"\s+", body.strip()) if token]


def test_letter_stays_within_ecology_letters_limits() -> None:
    text = LETTER.read_text(encoding="utf-8")
    assert len(_main_words(text)) <= 5000
    assert len(_abstract_words(text)) <= 150


def test_letter_centers_one_joint_access_routing_result() -> None:
    text = LETTER.read_text(encoding="utf-8")
    assert "r_J=0.3487" in text
    assert "p_{\\mathrm{joint}}=0.0001" in text
    assert "r_S=0.3468" in text
    assert "r_A=0.3505" in text
    assert "equal-network" in text
    assert "2-network" not in text


def test_letter_keeps_causal_and_replication_boundaries() -> None:
    text = LETTER.read_text(encoding="utf-8").lower()
    assert "result remains observational" in text
    assert "not an exact reconstruction" in text
    assert "not a universal causal coefficient" in text
    assert "raw observations were not pooled" in text


def test_letter_has_no_internal_repo_program_names() -> None:
    text = LETTER.read_text(encoding="utf-8")
    # "SCH" can occur legitimately as an author initial (e.g. Barrett SCH).
    # Guard project-routing language rather than bare initials.
    forbidden = [
        "SCH/SLK",
        "SCH owns",
        "SLK owns",
        "PAYOFF-B",
        "IWE repo",
        "BITA repo",
    ]
    assert all(token not in text for token in forbidden)
