"""Convert a deposited primary effect-size table into declared effect rows.

The repository's extraction protocol asks a human reader to copy group means,
dispersions, and sample sizes out of a published full text. A deposited
effect-size table from a published synthesis already contains exactly those
quantities, per primary study, in machine-readable form. This module turns one
such table into rows in the declared ``EFFECT_FIELDS`` schema so that the
already-committed pooling and context-dependence code can run on it unmodified.

Three properties are deliberately built in, because the value of a secondary
analysis rests entirely on them.

**Recompute, never copy.** The deposited effect column is treated as a claim to
be checked, not as the effect. Every value is recomputed from the deposited
group means by :func:`verify_deposited_effect`, and every disagreement is
written to an audit table rather than resolved silently. This caught two real
problems in the larceny dataset: the effect column is labelled Hedges' g but
holds log response ratios, and seven rows disagree with their own group means.

**Aggregate to one effect per cluster.** The deposited table has many effects
per study. Rather than relying on cluster-robust standard errors to absorb that,
each cluster is reduced to a single effect by :func:`aggregate_within_cluster`
under a declared within-cluster correlation, defaulting to the conservative
``rho_w = 1``. The pooled estimate and every moderator analysis then run on an
identical, fully independent set.

**Carry the source locator.** Every emitted row names the source repository, the
pinned commit, and the constituent source-row identifiers, so any number can be
traced back to the deposit it came from.

Only the standard library is used.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable, Sequence

from trait_architecture.broad_meta_analysis import ORIENTATION, _float, _text


AUDIT_FIELDS = (
    "source_row_id", "study_cluster_id", "source_metric", "deposited_effect",
    "deposited_variance", "recomputed_log_response_ratio", "recomputed_variance",
    "effect_agreement", "variance_agreement", "agreement_verdict", "handling",
)

#: Agreement tolerance for treating a deposited value as reproduced.
EFFECT_TOLERANCE = 1e-6
VARIANCE_TOLERANCE = 1e-6


@dataclass(frozen=True)
class GroupContrast:
    """One deposited two-group contrast, before any orientation or aggregation."""

    source_row_id: str
    study_cluster_id: str
    n_treatment: float
    mean_treatment: float
    sd_treatment: float
    n_control: float
    mean_control: float
    sd_control: float
    deposited_effect: float | None
    deposited_variance: float | None


def log_response_ratio(contrast: GroupContrast) -> tuple[float, float]:
    """Return the oriented log response ratio and its variance.

    Orientation is ``positive_is_more_declared_trait_more_declared_outcome``:
    the treatment group is the one with more of the declared exposure, so a
    negative value means the exposure lowers the declared outcome.
    """

    if contrast.mean_treatment <= 0 or contrast.mean_control <= 0:
        raise ValueError("log response ratio needs strictly positive group means")
    value = math.log(contrast.mean_treatment / contrast.mean_control)
    variance = (
        contrast.sd_treatment ** 2 / (contrast.n_treatment * contrast.mean_treatment ** 2)
        + contrast.sd_control ** 2 / (contrast.n_control * contrast.mean_control ** 2)
    )
    return value, variance


def verify_deposited_effect(contrast: GroupContrast) -> dict[str, object]:
    """Check a deposited effect against a recomputation from its own group means.

    Returns an audit row. ``agreement_verdict`` is one of:

    ``reproduced``
        Both the effect and its variance recompute to within tolerance.
    ``variance_disagrees``
        The point estimate reproduces; the deposited variance does not.
    ``sign_disagrees``
        The deposited effect equals the negative of the recomputation. Which
        side is correct cannot be decided from the deposit alone.
    ``effect_disagrees``
        The deposited effect differs in some other way.
    ``not_recomputable``
        The group means do not admit a log response ratio.
    """

    audit: dict[str, object] = {
        "source_row_id": contrast.source_row_id,
        "study_cluster_id": contrast.study_cluster_id,
        "deposited_effect": "" if contrast.deposited_effect is None else f"{contrast.deposited_effect:.10g}",
        "deposited_variance": "" if contrast.deposited_variance is None else f"{contrast.deposited_variance:.10g}",
    }
    try:
        value, variance = log_response_ratio(contrast)
    except ValueError:
        return {
            **audit, "recomputed_log_response_ratio": "", "recomputed_variance": "",
            "effect_agreement": "", "variance_agreement": "",
            "agreement_verdict": "not_recomputable",
        }

    audit["recomputed_log_response_ratio"] = f"{value:.10g}"
    audit["recomputed_variance"] = f"{variance:.10g}"

    if contrast.deposited_effect is None:
        audit["effect_agreement"] = ""
        audit["variance_agreement"] = ""
        audit["agreement_verdict"] = "no_deposited_effect_to_check"
        return audit

    effect_matches = abs(contrast.deposited_effect - value) <= EFFECT_TOLERANCE
    sign_flipped = (
        not effect_matches and abs(contrast.deposited_effect + value) <= EFFECT_TOLERANCE
    )
    variance_matches = (
        contrast.deposited_variance is not None
        and abs(contrast.deposited_variance - variance) <= VARIANCE_TOLERANCE
    )
    audit["effect_agreement"] = "match" if effect_matches else "sign_flipped" if sign_flipped else "differs"
    audit["variance_agreement"] = "match" if variance_matches else "differs"

    if effect_matches and variance_matches:
        verdict = "reproduced"
    elif effect_matches:
        verdict = "variance_disagrees"
    elif sign_flipped:
        verdict = "sign_disagrees"
    else:
        verdict = "effect_disagrees"
    audit["agreement_verdict"] = verdict
    return audit


def aggregate_within_cluster(
    values: Sequence[float],
    variances: Sequence[float],
    correlation: float,
) -> tuple[float, float]:
    """Combine several effects from one study cluster into one.

    The aggregate is the unweighted mean, whose variance under an assumed
    common within-cluster correlation ``rho_w`` is

    .. code-block:: text

        var = (1/m^2) * [ sum(v_i) + rho_w * sum_{i != j} sqrt(v_i * v_j) ]

    ``rho_w = 0`` treats the effects as independent and is anticonservative;
    ``rho_w = 1`` treats them as carrying no independent information at all and
    is the declared primary choice. Inverse-variance weighting is deliberately
    not used within a cluster: it would let one precisely measured outcome of a
    study speak for the study.
    """

    if not values or len(values) != len(variances):
        raise ValueError("values and variances must be non-empty and the same length")
    if not 0.0 <= correlation <= 1.0:
        raise ValueError("within-cluster correlation must lie in [0, 1]")
    if any(v <= 0 for v in variances):
        raise ValueError("effect variances must be positive")

    count = len(values)
    mean = sum(values) / count
    total = sum(variances)
    standard_deviations = [math.sqrt(v) for v in variances]
    cross = sum(
        standard_deviations[i] * standard_deviations[j]
        for i in range(count)
        for j in range(count)
        if i != j
    )
    variance = (total + correlation * cross) / (count ** 2)
    return mean, variance


def _optional_float(value: object) -> float | None:
    text = _text(value)
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def read_group_contrasts(
    rows: Iterable[dict[str, str]],
    *,
    row_id_field: str,
    cluster_field: str,
    treatment_prefix: str,
    control_prefix: str,
    effect_field: str = "",
    variance_field: str = "",
) -> list[GroupContrast]:
    """Read deposited rows into :class:`GroupContrast` objects.

    ``treatment_prefix`` and ``control_prefix`` name the deposited column
    families, e.g. ``"larcenist"`` for ``n_larcenist``/``mean_larcenist``/
    ``sd_larcenist``.
    """

    contrasts: list[GroupContrast] = []
    for row in rows:
        source_row_id = _text(row.get(row_id_field))
        cluster = _text(row.get(cluster_field))
        if not source_row_id or not cluster:
            raise ValueError("deposited rows need a row identifier and a study cluster")
        contrasts.append(GroupContrast(
            source_row_id=source_row_id,
            study_cluster_id=cluster,
            n_treatment=_float(row.get(f"n_{treatment_prefix}"), "n_treatment", positive=True),
            mean_treatment=_float(row.get(f"mean_{treatment_prefix}"), "mean_treatment"),
            sd_treatment=_float(row.get(f"sd_{treatment_prefix}"), "sd_treatment", nonnegative=True),
            n_control=_float(row.get(f"n_{control_prefix}"), "n_control", positive=True),
            mean_control=_float(row.get(f"mean_{control_prefix}"), "mean_control"),
            sd_control=_float(row.get(f"sd_{control_prefix}"), "sd_control", nonnegative=True),
            deposited_effect=_optional_float(row.get(effect_field)) if effect_field else None,
            deposited_variance=_optional_float(row.get(variance_field)) if variance_field else None,
        ))
    return contrasts


#: Verdicts that disqualify a deposited row from the primary analysis.
QUARANTINED_VERDICTS = {"sign_disagrees", "effect_disagrees", "not_recomputable"}

QUARANTINE_REASON = {
    "sign_disagrees": "deposited_effect_sign_disagrees_with_deposited_group_means",
    "effect_disagrees": "deposited_effect_disagrees_with_deposited_group_means",
    "not_recomputable": "non_positive_group_mean",
}


def build_cluster_effects(
    contrasts: Sequence[GroupContrast],
    *,
    correlation: float,
    include_quarantined: bool = False,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Aggregate verified contrasts to one effect per study cluster.

    Returns ``(cluster_effects, audit_rows)``. Each cluster effect carries the
    aggregate value and variance, the constituent source-row identifiers, and
    the number of deposited effects it combines.
    """

    audit_rows: list[dict[str, object]] = []
    usable: dict[str, list[tuple[str, float, float]]] = defaultdict(list)
    group_sizes: dict[str, tuple[float, float]] = {}

    for contrast in contrasts:
        audit = verify_deposited_effect(contrast)
        verdict = audit["agreement_verdict"]
        quarantined = verdict in QUARANTINED_VERDICTS
        if quarantined and not include_quarantined:
            audit["handling"] = f"excluded:{QUARANTINE_REASON.get(str(verdict), str(verdict))}"
            audit_rows.append(audit)
            continue
        if verdict == "not_recomputable":
            audit["handling"] = f"excluded:{QUARANTINE_REASON['not_recomputable']}"
            audit_rows.append(audit)
            continue
        value, variance = log_response_ratio(contrast)
        if quarantined and verdict == "sign_disagrees":
            # Declared sensitivity run: adopt the deposited sign.
            value = -value
            audit["handling"] = "included_at_deposited_sign:declared_sensitivity_run"
        elif verdict == "variance_disagrees":
            audit["handling"] = "included:variance_recomputed_from_group_means"
        else:
            audit["handling"] = "included:recomputed_from_group_means"
        audit_rows.append(audit)
        usable[contrast.study_cluster_id].append((contrast.source_row_id, value, variance))
        group_sizes[contrast.source_row_id] = (contrast.n_treatment, contrast.n_control)

    cluster_effects: list[dict[str, object]] = []
    for cluster, members in sorted(usable.items()):
        members.sort()
        value, variance = aggregate_within_cluster(
            [member[1] for member in members],
            [member[2] for member in members],
            correlation,
        )
        # Experimental-unit counts are carried as metadata so the canonical row
        # records sample size and not only its standard error. For a cluster
        # aggregating several contrasts these are means across contrasts, not
        # sums: the contrasts may share plants, so summing would overstate the
        # units observed.
        sizes = [group_sizes[row_id] for row_id, _, _ in members]
        mean_treatment_n = sum(size[0] for size in sizes) / len(sizes)
        mean_control_n = sum(size[1] for size in sizes) / len(sizes)
        cluster_effects.append({
            "study_cluster_id": cluster,
            "effect_value": value,
            "standard_error": math.sqrt(variance),
            "source_row_count": len(members),
            "source_row_ids": ";".join(member[0] for member in members),
            "n_treatment": mean_treatment_n,
            "n_control": mean_control_n,
            "n_total": mean_treatment_n + mean_control_n,
        })
    return cluster_effects, audit_rows


def declared_effect_row(
    cluster_effect: dict[str, object],
    *,
    effect_id: str,
    stratum: dict[str, str],
    taxon: str,
    doi: str,
    source_basis: str,
    source_locator: str,
    extraction_note: str,
) -> dict[str, object]:
    """Render one aggregated cluster effect in the declared ``EFFECT_FIELDS`` schema."""

    return {
        "effect_id": effect_id,
        "study_id": cluster_effect["study_cluster_id"],
        "study_cluster_id": cluster_effect["study_cluster_id"],
        "doi": doi,
        "taxon": taxon,
        "route": stratum["route"],
        "trait_role": "H",
        "trait_class": stratum["trait_class"],
        "outcome_class": stratum["outcome_class"],
        "design_class": stratum["design_class"],
        "effect_input_type": "reported_effect",
        "effect_metric": stratum["effect_metric"],
        "effect_value": f"{cluster_effect['effect_value']:.10g}",
        "standard_error": f"{cluster_effect['standard_error']:.10g}",
        "n_treatment": f"{cluster_effect['n_treatment']:.10g}",
        "n_control": f"{cluster_effect['n_control']:.10g}",
        "n_total": f"{cluster_effect['n_total']:.10g}",
        "mean_treatment": "", "sd_treatment": "",
        "mean_control": "", "sd_control": "", "event_treatment": "", "non_event_treatment": "",
        "event_control": "", "non_event_control": "", "correlation_r": "",
        "effect_orientation": ORIENTATION,
        "is_primary_effect": "true",
        "analysis_status": "eligible_for_quantitative_synthesis",
        "source_basis": source_basis,
        "source_locator": source_locator,
        "extraction_note": extraction_note,
    }
