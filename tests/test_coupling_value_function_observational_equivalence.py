from trait_architecture.value_function_equivalence import (
    LatentAffineState,
    optimized_differentiated_loss,
    profiles_equivalent,
    value_profile,
)


def test_dominated_latent_state_is_invisible_to_complete_sampled_value_profile():
    model_a = [
        LatentAffineState(0.0, (1.0,)),
        LatentAffineState(1.0, (0.0,)),
    ]
    model_b = [
        *model_a,
        LatentAffineState(2.0, (0.5,)),
    ]
    grid = [(x / 10.0,) for x in range(0, 51)]

    assert profiles_equivalent(
        shared_loss=3.0,
        states_a=model_a,
        states_b=model_b,
        coupling_grid=grid,
    )


def test_explicit_lower_envelope_matches_min_lambda_one():
    model = [
        LatentAffineState(0.0, (1.0,)),
        LatentAffineState(1.0, (0.0,)),
    ]
    assert optimized_differentiated_loss(model, (0.25,)) == 0.25
    assert optimized_differentiated_loss(model, (1.0,)) == 1.0
    assert optimized_differentiated_loss(model, (3.0,)) == 1.0


def test_value_function_can_distinguish_mechanisms_only_if_envelopes_differ():
    model_a = [
        LatentAffineState(0.0, (1.0,)),
        LatentAffineState(1.0, (0.0,)),
    ]
    model_c = [
        LatentAffineState(0.0, (0.5,)),
        LatentAffineState(1.0, (0.0,)),
    ]
    grid = [(0.25,), (0.5,), (1.0,), (2.0,)]

    assert value_profile(shared_loss=3.0, states=model_a, coupling_grid=grid) != value_profile(
        shared_loss=3.0,
        states=model_c,
        coupling_grid=grid,
    )


def test_finite_grid_equivalence_does_not_imply_latent_mechanism_identity():
    model_a = [LatentAffineState(0.0, (1.0,))]
    model_b = [
        LatentAffineState(0.0, (1.0,)),
        LatentAffineState(10.0, (0.0,)),
    ]
    grid = [(0.0,), (0.5,), (1.0,)]

    assert profiles_equivalent(
        shared_loss=2.0,
        states_a=model_a,
        states_b=model_b,
        coupling_grid=grid,
    )
    assert len(model_a) != len(model_b)
