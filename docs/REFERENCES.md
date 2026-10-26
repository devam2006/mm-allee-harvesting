# Sources to verify and cite

Course source: supplied PDF in `docs/course/`. The approved equations and project title were supplied by the group; the report must find and verify appropriate ecological context and any published model it builds on. Do not cite an unverified AI-generated bibliography entry.

Implementation primary sources (documentation checked during scaffold preparation):

- [SciPy solve_ivp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html): RK45, dense output, terminal events, tolerances and return fields.
- [SciPy least_squares](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html): inverse ODE-fit baseline; read before implementation.
- [PyTorch autograd](https://docs.pytorch.org/docs/stable/autograd.html) and [installation selector](https://pytorch.org/get-started/locally/): automatic differentiation and appropriate CPU/GPU installation.
- [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches): review/status gates and plan availability.
- [actions/checkout](https://github.com/actions/checkout) and [actions/setup-python](https://github.com/actions/setup-python): CI configuration.

WP01/WP02 find a small number of credible primary/textbook sources on strong Allee effects and harvesting. WP04 verifies the original PINN method source and records the particular loss/architecture used. WP05 cites any inference/identifiability method borrowed rather than derived here. Put **verified** entries in `report/references.bib`, cite them where used, and distinguish this group's derivations from adapted material.
