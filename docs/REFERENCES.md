# Sources to verify and cite

Course source: supplied PDF in `docs/course/`. The approved equations and project title were supplied by the group; the report must find and verify appropriate ecological context and any published model it builds on. Do not cite an unverified AI-generated bibliography entry.

Implementation primary sources (documentation checked during scaffold preparation):

- [SciPy solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html): RK45, dense output, terminal events, tolerances and return fields.
- [SciPy least_squares](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html): inverse ODE-fit baseline; read before implementation.
- [JAX automatic differentiation](https://docs.jax.dev/en/latest/automatic-differentiation.html) and [installation](https://docs.jax.dev/en/latest/installation.html): `grad`/`vmap` used by the PINN engine; CPU installation.
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): review/status gates and plan availability.
- [actions/checkout](https://github.com/actions/checkout) and [actions/setup-python](https://github.com/actions/setup-python): CI configuration.

WP01/WP02 find a small number of credible primary/textbook sources on strong Allee effects and harvesting. WP04 verifies the original PINN method source and records the particular loss/architecture used. WP05 cites any inference/identifiability method borrowed rather than derived here. Put **verified** entries in `report/references.bib`, cite them where used, and distinguish this group's derivations from adapted material.

## WP03 numerical references checked 28 October 2026

- SciPy [solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html): RK45 5(4), DOP853 and terminal events.
- SciPy [quad](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html): QUADPACK integration/error-estimate semantics.
- SciPy [bounded minimisation](https://docs.scipy.org/doc/scipy/reference/optimize.minimize_scalar-bounded.html): independent maxima and its x tolerance.

The mathematical derivations are this project's calculations under the stated models, not empirical ecological validation. Bibliography entries are in report/references.bib.
