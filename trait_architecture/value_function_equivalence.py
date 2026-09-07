from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class LatentAffineState:
    baseline_loss: float
    coupling_penalties: tuple[float, ...]

    def loss(self, coupling: Sequence[float]) -> float:
        if len(coupling) != len(self.coupling_penalties):
            raise ValueError("coupling dimension does not match latent-state penalty dimension")
        return self.baseline_loss + sum(
            lam * penalty for lam, penalty in zip(coupling, self.coupling_penalties)
        )


def optimized_differentiated_loss(
    states: Sequence[LatentAffineState],
    coupling: Sequence[float],
) -> float:
    if not states:
        raise ValueError("at least one latent state is required")
    return min(state.loss(coupling) for state in states)


def recoverable_fitness(
    *,
    shared_loss: float,
    states: Sequence[LatentAffineState],
    coupling: Sequence[float],
) -> float:
    return shared_loss - optimized_differentiated_loss(states, coupling)


def value_profile(
    *,
    shared_loss: float,
    states: Sequence[LatentAffineState],
    coupling_grid: Sequence[Sequence[float]],
) -> tuple[float, ...]:
    return tuple(
        recoverable_fitness(shared_loss=shared_loss, states=states, coupling=point)
        for point in coupling_grid
    )


def profiles_equivalent(
    *,
    shared_loss: float,
    states_a: Sequence[LatentAffineState],
    states_b: Sequence[LatentAffineState],
    coupling_grid: Sequence[Sequence[float]],
    atol: float = 0.0,
) -> bool:
    if atol < 0:
        raise ValueError("atol must be nonnegative")
    profile_a = value_profile(
        shared_loss=shared_loss,
        states=states_a,
        coupling_grid=coupling_grid,
    )
    profile_b = value_profile(
        shared_loss=shared_loss,
        states=states_b,
        coupling_grid=coupling_grid,
    )
    return all(abs(a - b) <= atol for a, b in zip(profile_a, profile_b))
