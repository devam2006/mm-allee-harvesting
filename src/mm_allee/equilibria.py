"""Equilibria and stability for the logistic baseline and Model A (constant yield).

Everything here uses the dimensionless variables of the scientific contract:
``x = N/K``, ``tau = r t``, ``a = A/K`` and ``q = H/(rK)``. The vector fields are

* logistic: ``f(x) = x(1-x) - q``
* Model A:  ``f(x) = G(x) - q`` with ``G(x) = x(1-x)(x/a - 1)``.

An equilibrium is a root of ``f``. Stability is decided from the sign of ``f`` just
below and just above the root (a phase-line argument), not from ``f'`` alone, so the
repeated root at the fold is classified correctly as semistable. The linearisation
``f'(x_eq)`` is reported alongside and agrees with the sign test at simple roots.

Root finding avoids a generic polynomial solver. The calculus of Section 1 of the
report brackets every physical root between points where ``f`` changes sign, and
Brent's method (``scipy.optimize.brentq``) refines it. Near the fold the two roots are
returned separately until ``q`` is within ``FOLD_TOL`` of ``q_c``; they are never
silently merged or dropped.

Tolerances (dimensionless, documented in the report):

* ``FOLD_TOL = 1e-12``: ``|q - q_c| <= FOLD_TOL`` is treated as the critical case.
  ``q_c`` is computed in double precision to roughly ``1e-16`` relative error, so this
  margin only absorbs roundoff. Just below it the two roots are still about
  ``sqrt(2*FOLD_TOL/|G''(x_star)|) ~ 1e-6`` apart and are resolved separately.
* ``XTOL = 1e-14``: Brent bracket width at termination (absolute, on ``x in [0,1]``).
* One-sided sign probes sit at ``x_eq +/- delta`` with
  ``delta = min(1e-4, gap/4)``, where ``gap`` is the distance to the nearest other root,
  so a probe never crosses a neighbouring root.

For ``q > 0`` the point ``x = 0`` is **not** an equilibrium of Model A or the logistic
model (``f(0) = -q``). Trajectories reach it in finite time; the solver stops there
(absorbing extinction convention). That boundary is reported separately by
:func:`extinction_boundary`, never inside the equilibrium list.
"""

from dataclasses import asdict, dataclass
from math import isfinite, sqrt

import numpy as np
from scipy.optimize import brentq

from .models import growth, rhs

FOLD_TOL = 1e-12
XTOL = 1e-14
PROBE_MAX = 1e-4

STABLE = "stable"
UNSTABLE = "unstable"
SEMISTABLE = "semistable"


@dataclass(frozen=True)
class Equilibrium:
    """One root of the dimensionless vector field and its classification.

    ``stability`` is ``stable``, ``unstable`` or ``semistable`` for physical roots and
    ``excluded`` for a negative algebraic root. ``attracts_from`` says from which
    side nearby trajectories approach (``both``, ``above``, ``below`` or ``neither``).
    ``left_sign``/``right_sign`` are the signs of ``f`` at the probes; ``left_sign`` is
    ``None`` at the physical boundary ``x = 0`` where only ``x >= 0`` matters.
    """

    model: str
    a: float | None
    q: float
    x: float
    physical: bool
    multiplicity: int
    derivative: float
    left_sign: int | None
    right_sign: int | None
    stability: str
    attracts_from: str
    residual: float
    note: str

    def as_row(self):
        return asdict(self)


def _validate_a(a):
    if not isfinite(a) or not 0 < a < 1:
        raise ValueError("Require 0<a<1")


def _validate_q(q):
    if not isfinite(q) or q < 0:
        raise ValueError("Harvest q must be finite and nonnegative")


def growth_derivative(x, a):
    """``G'(x) = -3x^2/a + 2(1+a)x/a - 1``, derived by differentiating ``growth``."""
    _validate_a(a)
    return -3 * x**2 / a + 2 * (1 + a) * x / a - 1


def rhs_derivative(x, model, *, a=None, q=0.0):
    """Derivative of the logistic or Model A vector field with respect to ``x``.

    The constant harvest ``q`` does not change the derivative; it is accepted for a
    uniform call signature and validated.
    """
    _validate_q(q)
    if model == "logistic":
        return 1 - 2 * x
    if model == "A":
        return growth_derivative(x, a)
    raise ValueError("rhs_derivative supports model 'logistic' or 'A'")


def fold_a(a):
    """Fold (saddle-node) point of Model A: ``(x_star, q_c)``.

    ``G'(x) = 0`` is the quadratic ``3x^2 - 2(1+a)x + a = 0`` with roots
    ``((1+a) +/- sqrt(1-a+a^2))/3``. The larger root lies in ``(a, 1)`` because
    ``G'(a) = 1-a > 0`` and ``G'(1) = (a-1)/a < 0``; it is the maximum of ``G`` on
    ``[a, 1]``. Substituting gives the closed form

    ``q_c = [2(1-a+a^2)^(3/2) + (1+a)(2a-1)(a-2)] / (27a)``.

    WP03's ``thresholds.critical_a`` is planned to provide the same quantity with an
    independent numerical-maximisation check; this helper exists so WP01 can classify
    the critical case without depending on an unmerged module.
    """
    _validate_a(a)
    s = sqrt(1 - a + a * a)
    x_star = (1 + a + s) / 3
    q_c = (2 * s**3 + (1 + a) * (2 * a - 1) * (a - 2)) / (27 * a)
    return x_star, q_c


def _sign(value):
    return int(np.sign(value))


def _classify(f, x_eq, neighbours, *, boundary=False):
    """Phase-line classification from one-sided signs of ``f``."""
    gaps = [abs(x_eq - other) for other in neighbours if other != x_eq]
    delta = min([PROBE_MAX] + [g / 4 for g in gaps])
    right = _sign(f(x_eq + delta))
    left = None if boundary else _sign(f(x_eq - delta))
    if boundary:
        # Only x >= 0 is physical: the root attracts if trajectories just above move down.
        if right < 0:
            return STABLE, "above", left, right
        return UNSTABLE, "neither", left, right
    if left > 0 and right < 0:
        return STABLE, "both", left, right
    if left < 0 and right > 0:
        return UNSTABLE, "neither", left, right
    if left < 0 and right < 0:
        return SEMISTABLE, "above", left, right
    if left > 0 and right > 0:
        return SEMISTABLE, "below", left, right
    raise RuntimeError(f"Sign probe hit zero near x={x_eq}; refine probe settings")


def _records(model, a, q, roots, f, *, multiplicities=None, boundary_roots=(), notes=None):
    multiplicities = multiplicities or {}
    notes = notes or {}
    out = []
    for x_eq in roots:
        physical = x_eq >= 0
        deriv = float(rhs_derivative(x_eq, model, a=a, q=q))
        residual = float(abs(f(x_eq)))
        if physical:
            stability, attracts, left, right = _classify(
                f, x_eq, roots, boundary=x_eq in boundary_roots
            )
        else:
            stability, attracts, left, right = "excluded", "neither", None, None
        out.append(
            Equilibrium(
                model=model,
                a=a,
                q=float(q),
                x=float(x_eq),
                physical=physical,
                multiplicity=multiplicities.get(x_eq, 1),
                derivative=deriv,
                left_sign=left,
                right_sign=right,
                stability=stability,
                attracts_from=attracts,
                residual=residual,
                note=notes.get(x_eq, ""),
            )
        )
    return out


def equilibria_logistic(q, *, include_excluded=False):
    """Equilibria of ``dx/dtau = x(1-x) - q``.

    Roots are ``(1 +/- sqrt(1-4q))/2``. The smaller root is computed as ``q/x_plus``
    (product of roots equals ``q``) to avoid cancellation when ``q`` is small.
    Logistic roots are never negative for ``q >= 0``; ``include_excluded`` is accepted
    for a uniform interface.
    """
    _validate_q(q)

    def f(x):
        return rhs(x, "logistic", a=0.5, harvest=q)

    q_c = 0.25
    if q == 0:
        roots = [0.0, 1.0]
        return _records(
            "logistic",
            None,
            q,
            roots,
            f,
            boundary_roots=(0.0,),
            notes={0.0: "extinct state; unstable for logistic growth", 1.0: "carrying capacity"},
        )
    if abs(q - q_c) <= FOLD_TOL:
        return _records(
            "logistic",
            None,
            q,
            [0.5],
            f,
            multiplicities={0.5: 2},
            notes={0.5: "fold: double root at x=1/2 (maximum sustainable constant yield)"},
        )
    if q > q_c:
        return []
    disc = sqrt(1 - 4 * q)
    upper = (1 + disc) / 2
    lower = q / upper
    return _records(
        "logistic",
        None,
        q,
        [lower, upper],
        f,
        notes={lower: "harvest-induced threshold", upper: "persistent state"},
    )


def _negative_root_a(a, q):
    """Single negative root of ``G(x) = q`` for ``q > 0``.

    For ``x < 0``, ``G(x) > 0`` and ``G'(x) < 0`` so ``G`` decreases from ``+inf`` to 0
    and crosses ``q`` exactly once. It is a polynomial root but not a population.
    """
    lo = -1.0
    while growth(lo, a) - q <= 0:
        lo *= 2
    return brentq(lambda x: growth(x, a) - q, lo, 0.0, xtol=XTOL, rtol=4 * np.finfo(float).eps)


def equilibria_a(a, q, *, include_excluded=False):
    """Equilibria of Model A, ``dx/dtau = x(1-x)(x/a-1) - q``.

    Physical cases (proved in the report via the sign and monotonicity of ``G``):

    * ``q = 0``: roots ``0, a, 1`` (stable, unstable, stable).
    * ``0 < q < q_c``: one root in ``(a, x_star)`` (unstable) and one in
      ``(x_star, 1)`` (stable).
    * ``|q - q_c| <= FOLD_TOL``: one double root at ``x_star`` (semistable, attracts
      from above).
    * ``q > q_c``: no physical equilibrium.

    For ``q > 0`` the cubic always has one negative root; it is returned only when
    ``include_excluded=True`` with ``physical=False`` and ``stability='excluded'``.
    """
    _validate_a(a)
    _validate_q(q)

    def f(x):
        return rhs(x, "A", a=a, harvest=q)

    x_star, q_c = fold_a(a)
    excluded = []
    if q > 0 and include_excluded:
        excluded = [_negative_root_a(a, q)]
    excluded_notes = {r: "negative algebraic root; not a population" for r in excluded}

    if q == 0:
        roots = [0.0, a, 1.0]
        return _records(
            "A",
            a,
            q,
            roots,
            f,
            boundary_roots=(0.0,),
            notes={
                0.0: "extinct state; stable under strong Allee growth",
                a: "Allee threshold (minimum viable population)",
                1.0: "carrying capacity",
            },
        )
    if abs(q - q_c) <= FOLD_TOL:
        physical = [x_star]
        mult = {x_star: 2}
        notes = {x_star: "fold: double root, one-sided signs decide stability"}
    elif q < q_c:
        lower = brentq(f, a, x_star, xtol=XTOL, rtol=4 * np.finfo(float).eps)
        upper = brentq(f, x_star, 1.0, xtol=XTOL, rtol=4 * np.finfo(float).eps)
        physical = [lower, upper]
        mult = {}
        notes = {lower: "harvest-shifted Allee threshold", upper: "persistent state"}
    else:
        physical, mult, notes = [], {}, {}
    roots = sorted(excluded + physical)
    return _records("A", a, q, roots, f, multiplicities=mult, notes={**notes, **excluded_notes})


def extinction_boundary(model, q):
    """Describe ``x = 0`` for constant-yield models without calling it an equilibrium."""
    _validate_q(q)
    if model not in {"logistic", "A"}:
        raise ValueError("Constant-yield boundary applies to 'logistic' or 'A'")
    if q == 0:
        return {"x": 0.0, "is_equilibrium": True, "policy": "zero_equilibrium"}
    return {
        "x": 0.0,
        "is_equilibrium": False,
        "rhs_at_zero": -float(q),
        "policy": "stop_at_zero (absorbing extinction; harvest shuts down)",
    }


def classify_equilibrium(model, x_eq, *, a=None, q=0.0):
    """Classify a user-supplied root by one-sided signs (convenience for WP02/WP03).

    Raises if ``x_eq`` is not a root to within ``1e-10`` absolute residual.
    """
    _validate_q(q)
    if model == "A":
        _validate_a(a)
        records = equilibria_a(a, q)
    elif model == "logistic":
        records = equilibria_logistic(q)
    else:
        raise ValueError("classify_equilibrium supports 'logistic' or 'A'")
    for record in records:
        if abs(record.x - x_eq) <= 1e-10:
            return record
    raise ValueError(f"x={x_eq} is not an equilibrium of {model} at q={q}")


def branch_rows(model, q_values, *, a=None):
    """Long-form branch data for plots and CSV export.

    One row per physical equilibrium per ``q``. ``branch`` is ``upper``/``lower`` for
    the two populated branches, ``fold`` at the double root and ``zero``/``threshold``/
    ``capacity`` at ``q = 0``.
    """
    rows = []
    for q in q_values:
        q = float(q)
        records = equilibria_a(a, q) if model == "A" else equilibria_logistic(q)
        for i, rec in enumerate(records):
            if q == 0:
                branch = ["zero", "threshold" if model == "A" else "capacity", "capacity"][i]
            elif rec.multiplicity == 2:
                branch = "fold"
            else:
                branch = "lower" if i == 0 and len(records) == 2 else "upper"
            rows.append({**rec.as_row(), "branch": branch})
    return rows
