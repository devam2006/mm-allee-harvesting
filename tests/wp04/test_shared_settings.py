import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load():
    spec = importlib.util.spec_from_file_location(
        "shared_settings_mod", ROOT / "experiments" / "integration" / "shared_settings.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["shared_settings_mod"] = module
    spec.loader.exec_module(module)
    return module


def fwd(statuses):
    return [{"status": s, "wall_seconds": 1.0} for s in statuses]


def inv(errors):
    return [
        {"max_rel_error": e, "wall_seconds": 2.0, "collapsed": e is not None and e > 0.9}
        for e in errors
    ]


def test_counts_forward_ok_and_inverse_recovered_against_the_threshold():
    mod = load()
    s = mod.summarise_candidate(
        "x",
        fwd(["ok", "ok", "inaccurate", "invalid_prediction"]),
        inv([1e-3, 0.05, 0.051, None, 1.0]),
        0.05,
    )
    assert s["forward_accurate"] == 2 and s["forward_runs"] == 4
    assert (
        s["inverse_recovered"] == 2
    )  # 1e-3 and exactly 0.05 count; 0.051, a missing score and 1.0 do not
    assert s["inverse_fits"] == 5 and s["score"] == 4 and s["collapsed_fits"] == 1
    assert s["median_recovered_error"] == (1e-3 + 0.05) / 2


def test_highest_total_score_wins_even_if_its_errors_are_larger():
    mod = load()
    a = mod.summarise_candidate("a", fwd(["ok"] * 3), inv([1e-1, 1e-1, 1e-1]), 0.05)  # score 3
    b = mod.summarise_candidate("b", fwd(["ok"] * 2), inv([4e-2, 4e-2, 1e-1]), 0.05)  # score 4
    assert mod.choose([a, b]) == "b"


def test_ties_go_to_the_lower_median_recovered_error_and_no_recovery_counts_as_worst():
    mod = load()
    a = mod.summarise_candidate(
        "a", fwd(["ok", "ok"]), inv([1e-2, 1e-2]), 0.05
    )  # score 4, median 1e-2
    b = mod.summarise_candidate(
        "b", fwd(["ok", "ok"]), inv([1e-4, 1e-4]), 0.05
    )  # score 4, median 1e-4
    c = mod.summarise_candidate(
        "c", fwd(["ok"] * 4), inv([None, None]), 0.05
    )  # score 4, no recovery
    assert mod.choose([a, c, b]) == "b"
    assert mod.choose([a, c]) == "a"


def _smoke_fit(validation_selection):
    """Short seeded inverse fit on noisy synthetic data (the pattern of WP05's own smoke test)."""
    import numpy as np
    import pytest

    pytest.importorskip("jax")
    from mm_allee.data import generate_noisy_observations
    from mm_allee.pinn.inverse import InversePINNTrainer, TrainableParameters
    from mm_allee.pinn.network import NetworkConfig

    times = np.linspace(0, 8, 41)
    pops = 45.0 + 50.0 * (1 - np.exp(-times / 1.5))  # smooth saturating curve, not a model solution
    obs = generate_noisy_observations(
        times, pops, trajectory_id="vs", model="A", noise_sigma=0.01, noise_seed=11, n_ref=100.0
    )
    known = {"known_K": 100.0, "known_initial_population": 45.0}
    trainer = InversePINNTrainer(
        NetworkConfig(layers=(1, 8, 8, 1), activation="tanh"),
        TrainableParameters(
            "A", fit_params=["r", "A", "H"], known_conditions=known,
            initial_guesses={"r": 0.5, "A": 25.0, "H": 8.0},
        ),
        lr_net=5e-3, lr_params=1e-2, lbfgs_iters=0, validation_selection=validation_selection,
    )  # fmt: skip
    return trainer.fit(
        obs, known_conditions=known, epochs=60, patience=1, n_collocation=20, seed=11, eval_every=1
    )


def test_validation_selection_off_trains_the_full_budget_and_default_is_unchanged():
    on = _smoke_fit(True)  # the trainer's default: early stopping on validation loss
    off = _smoke_fit(False)
    n_adam = lambda r: sum(1 for ph in r.training_history["phase"] if ph == "adam")  # noqa: E731
    assert on.status == "validation_stopped" and n_adam(on) < 60  # patience 1 stops it early
    assert off.status != "validation_stopped" and n_adam(off) == 60  # switch off: full budget
    assert off.success and off.train_loss < on.train_loss  # and it ends at a lower training loss
