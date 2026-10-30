import importlib.util
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load():
    spec = importlib.util.spec_from_file_location(
        "wp04_select", ROOT / "experiments" / "wp04" / "select_activation.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["wp04_select"] = module
    spec.loader.exec_module(module)
    return module


def rows(errors):
    return [
        {"case": "c", "relative_l2": str(e), "boundary_violations": "0", "wall_seconds": "1.0"}
        for e in errors
    ]


def test_summary_hand_values():
    sel = load()
    s = sel.summarise("x", rows([1e-3, 1e-1, 1e-2, 1e-5]))
    assert s["n_accurate"] == 3  # 1e-1 exceeds the 5e-2 threshold
    assert math.isclose(s["geomean_relative_l2"], 10 ** ((-3 - 1 - 2 - 5) / 4))


def test_most_accurate_runs_wins_even_with_worse_mean_error():
    sel = load()
    a = sel.summarise("a", rows([1e-2, 1e-2, 1e-2, 9.0]))  # 3 accurate, huge outlier
    b = sel.summarise("b", rows([4e-2, 4e-2, 6e-2, 7e-2]))  # 2 accurate, small errors
    assert sel.select([a, b]) == "a"


def test_tie_goes_to_smaller_geometric_mean():
    sel = load()
    a = sel.summarise("a", rows([1e-3, 1e-3]))
    b = sel.summarise("b", rows([1e-4, 4e-2]))  # also 2 accurate; geomean 6.3e-3 vs 1e-3
    assert sel.select([a, b]) == "a"
