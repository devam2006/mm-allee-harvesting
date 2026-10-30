"""Independent checks for the two follow-up findings on PR #8."""

import importlib.util
import json
from decimal import Decimal, localcontext
from pathlib import Path

import numpy as np
import pytest

from mm_allee.equilibria import FOLD_RTOL, equilibria_a, fold_a

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("a,factor", [(1 - 2.0**-30, 4), (0.99999999, 1.1)])
def test_near_fold_roots_are_distinct_and_match_independent_decimal(a, factor):
    q = fold_a(a)[1] * (1 - factor * FOLD_RTOL)
    actual = equilibria_a(a, q)
    with localcontext() as ctx:
        ctx.prec = 90
        da, dq = Decimal(a), Decimal(q)
        star = (1 + da + (1 - da + da * da).sqrt()) / 3

        def field(x):
            return x * (1 - x) * (x - da) / da - dq

        expected = []
        for lo, hi, increasing in [(da, star, True), (star, Decimal(1), False)]:
            for _ in range(300):
                mid = (lo + hi) / 2
                if (field(mid) < 0) == increasing:
                    lo = mid
                else:
                    hi = mid
            expected.append(float((lo + hi) / 2))
    assert actual[0].x < actual[1].x
    assert [r.stability for r in actual] == ["unstable", "stable"]
    assert [(r.left_sign, r.right_sign) for r in actual] == [(-1, 1), (1, -1)]
    assert actual[0].derivative > 0 > actual[1].derivative
    # The rounded maximum/critical yield can shift the final offset addition
    # by one population ulp. Distinctness and phase labels are exact checks.
    assert all(abs(r.x - x) <= np.spacing(x) for r, x in zip(actual, expected, strict=True))
    assert "threshold" in actual[0].note
    assert actual[1].note == "persistent state"


def test_unsupported_rtol_is_rejected_before_any_output(tmp_path):
    spec = importlib.util.spec_from_file_location(
        "wp01_followup_cli", ROOT / "experiments/wp01/run.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    config = json.loads((ROOT / "configs/wp01.json").read_text())
    config["solver"]["rtol"] = 1e-16
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))
    output = tmp_path / "unsupported"
    with pytest.raises(ValueError, match="RK45 rtol must be at least"):
        module.main(["--config", str(path), "--output", str(output)])
    assert not output.exists()
    config["solver"]["rtol"] = 100 * np.finfo(float).eps
    assert module.solver_settings(config)["rtol"] == config["solver"]["rtol"]
