from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LETTER = ROOT / "manuscript" / "MANUSCRIPT_ACCESS_ROUTING_LETTER_V0.md"


def _main_words(text: str) -> list[str]:
    # Ecology Letters defines the 5,000-word limit for main text only,
    # excluding title page, abstract, acknowledgements, references, and legends.
    start = text.index("## Introduction")
    end = text.index("## Data accessibility and reproducibility")
    body = text[start:end]
    body = re.sub(r"~~~[\s\S]*?~~~", " ", body)
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
    assert "r_J=0.4282" in text
    assert "p_{\\mathrm{joint}}=0.0001" in text
    assert "r_S=0.3468" in text
    assert "r_A=0.5032" in text
    assert "equal-network" in text
    assert "2-network" not in text


def test_letter_reports_within_bird_behavioral_routing_and_formal_boundary_asymmetry() -> None:
    text = LETTER.read_text(encoding="utf-8")
    assert "Thirty-six bird species occurred in both barrier states" in text
    assert "1,285 bird × plant dyads" in text
    assert "centered-rank \\(\\rho=0.340\\)" in text
    assert "24 of 28 bird-specific correlations were positive" in text
    assert "1/23, 4.3%" in text
    assert "3/10, 30%" in text
    assert "not a test of literature bias" in text
    assert "does not show that the theory prospectively predicts every exception" in text


@pytest.mark.prose_contract
def test_letter_keeps_causal_and_replication_boundaries() -> None:
    text = LETTER.read_text(encoding="utf-8").lower()
    assert "result remains observational" in text
    assert "not an exact reconstruction" in text
    assert "not a universal causal coefficient" in text
    assert "raw observations were not pooled" in text
    assert "k=2" in text
    assert "does not estimate between-network heterogeneity" in text
    assert "generality beyond the two network systems" in text


@pytest.mark.prose_contract
def test_letter_weights_ecuador_primary_and_insects_as_corroboration() -> None:
    text = LETTER.read_text(encoding="utf-8")
    abstract = text.split("## Abstract", 1)[1].split("## Introduction", 1)[0]
    assert "in an all-Ecuador bird–flower network" in abstract
    assert "independent insect network" in abstract
    assert abstract.index("259 Ecuadorian plant species") < abstract.index("57 plant species")

    assert "### Primary Ecuadorian test" in text
    assert "### Independent insect corroboration" in text
    assert text.index("### Primary Ecuadorian test") < text.index("### Independent insect corroboration")


@pytest.mark.prose_contract
def test_letter_demotes_matched_domain_corpus_to_mechanistic_context() -> None:
    text = LETTER.read_text(encoding="utf-8").lower()
    assert "mechanistic context, not independent validation" in text
    assert "have not yet undergone outcome-blinded independent recoding" in text
    assert "do not make an 11/11 success-rate argument" in text
    assert "network analyses—not the matched-domain alignment—carry the inferential contribution" in text

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


@pytest.mark.prose_contract
def test_letter_separates_relational_result_mechanism_and_generality() -> None:
    text = LETTER.read_text(encoding="utf-8").lower()
    assert "relational property of trait matching" in text
    assert "nested claim rather than a universal law" in text
    assert "relative route cost is the mechanistic interpretation" in text
    assert "remain prospective predictions" in text


@pytest.mark.prose_contract
def test_letter_states_decisive_relative_route_cost_falsification() -> None:
    text = LETTER.read_text(encoding="utf-8").lower()
    assert "factorial manipulation of route costs" in text
    assert "raising legitimate-route cost while bypass cost is fixed should increase bypass" in text
    assert "raising bypass cost while legitimate cost is fixed should decrease bypass" in text
    assert "raising both similarly should produce little route-composition shift" in text


@pytest.mark.prose_contract
def test_letter_separates_case_directional_recurrence_from_standardized_k() -> None:
    text = LETTER.read_text(encoding="utf-8")
    assert "A third independent multispecies bird–flower dataset" in text
    assert "Case et al. (2026)" in text
    assert "11 plant and seven bird species" in text
    assert "directional corroboration rather than a third standardized network contribution" in text
    assert "standardized replication count remain \\(k=2\\)" in text


@pytest.mark.prose_contract
def test_letter_names_zero_inclusive_estimand_as_feeding_visitation() -> None:
    text = LETTER.read_text(encoding="utf-8").lower()
    assert "resolved feeding visits (legitimate + robbing)" in text
    assert "total route-resolved exploitation" not in text
    assert "waypoint fixed effects absorb" in text
    assert "time-invariant plant/waypoint reward main effect" in text
    assert "bird-specific reward responses" in text


@pytest.mark.prose_contract
def test_letter_integrates_postopen_route_split_and_boundary_mass() -> None:
    text = LETTER.read_text(encoding="utf-8")
    assert "legitimate/non-robbing visits (1.883, 1.111–3.190)" in text
    assert "robbery-only counts (0.463, 0.147–1.461)" in text
    assert "585 of 999 finite bootstrap fits (58.6%)" in text
    assert "should not be described as greater exploitation or greater robbery" in text
    assert "public EPHI tables contain no direct nectar-reward covariate" in text
