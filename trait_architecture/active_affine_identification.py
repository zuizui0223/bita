from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class ActiveAffinePlane:
    baseline_loss: float
    coupling_penalties: tuple[float, ...]
    differentiated_loss: float

    def loss_at(self, coupling: Sequence[float]) -> float:
        if len(coupling) != len(self.coupling_penalties):
            raise ValueError("coupling dimension does not match active-plane dimension")
        return self.baseline_loss + sum(
            lam * penalty for lam, penalty in zip(coupling, self.coupling_penalties)
        )


def identify_active_affine_plane_from_recovery(
    *,
    shared_loss: float,
    recovery: float,
    recovery_gradient: Sequence[float],
    coupling: Sequence[float],
    atol: float = 1e-12,
) -> ActiveAffinePlane:
    if len(recovery_gradient) != len(coupling) or not coupling:
        raise ValueError("recovery_gradient and coupling must have the same nonzero length")
    if atol < 0:
        raise ValueError("atol must be nonnegative")

    penalties = tuple(-float(component) for component in recovery_gradient)
    if any(penalty < -atol for penalty in penalties):
        raise ValueError("recovery gradient violates nonnegative coupling-penalty orientation")
    penalties = tuple(0.0 if abs(penalty) <= atol else penalty for penalty in penalties)

    differentiated_loss = shared_loss - recovery
    baseline_loss = differentiated_loss - sum(
        lam * penalty for lam, penalty in zip(coupling, penalties)
    )
    return ActiveAffinePlane(
        baseline_loss=baseline_loss,
        coupling_penalties=penalties,
        differentiated_loss=differentiated_loss,
    )
