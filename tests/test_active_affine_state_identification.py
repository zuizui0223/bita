import pytest

from trait_architecture.active_affine_identification import (
    identify_active_affine_plane_from_recovery,
)


def test_active_affine_plane_is_recovered_from_value_and_gradient():
    # Active latent plane: D(lambda)=0.4 + 1.2*lambda1 + 0.5*lambda2.
    coupling = (0.3, 0.8)
    penalties = (1.2, 0.5)
    baseline = 0.4
    differentiated_loss = baseline + sum(
        lam * penalty for lam, penalty in zip(coupling, penalties)
    )
    shared_loss = 3.0
    recovery = shared_loss - differentiated_loss
    recovery_gradient = tuple(-penalty for penalty in penalties)

    identified = identify_active_affine_plane_from_recovery(
        shared_loss=shared_loss,
        recovery=recovery,
        recovery_gradient=recovery_gradient,
        coupling=coupling,
    )

    assert identified.baseline_loss == pytest.approx(baseline)
    assert identified.coupling_penalties == pytest.approx(penalties)
    assert identified.differentiated_loss == pytest.approx(differentiated_loss)


def test_identified_active_plane_can_be_continued_without_claiming_global_optimality():
    identified = identify_active_affine_plane_from_recovery(
        shared_loss=2.0,
        recovery=1.0,
        recovery_gradient=(-1.0,),
        coupling=(0.5,),
    )
    assert identified.baseline_loss == pytest.approx(0.5)
    assert identified.loss_at((0.2,)) == pytest.approx(0.7)


def test_gradient_with_wrong_penalty_orientation_fails_closed():
    with pytest.raises(ValueError):
        identify_active_affine_plane_from_recovery(
            shared_loss=2.0,
            recovery=1.0,
            recovery_gradient=(0.2,),
            coupling=(0.5,),
        )
