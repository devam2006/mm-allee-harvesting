# Prem PR #10 reporting-fix verification

Reviewed exact head `00393cd78057e8b16c50698521f0a91ed341fb12`, comprising
`7b502cc` reporting fixes and `00393cd` evidence/wording follow-up, at Devam's
request on 31 October 2026. Prepared with Codex; no human approval or merge.

The two reproduced code findings are addressed. Validation loss is measured
without controlling training when selection is disabled, and the returned loss
matches the returned model. The tests change validation observations while
checking that trained parameters and training loss stay identical. Injected
L-BFGS exceptions now expose `lbfgs_failed`, `success=False`, the exception and
a usable Adam fallback. SciPy exit status/message/iterations are retained;
iteration-limit and abnormal exits have separate optimizer outcomes.

The API keeps the legacy `status=converged` as a training-completed label.
It must always be read with `optimizer.lbfgs_outcome`; it does not assert
that L-BFGS reached a tolerance. This is now explicit in the integrated notebook.
Unifying the forward/inverse vocabulary remains an owner decision.

Observed independent checks:

- Ten new reporting regressions passed; full Prem source suite: 301 passed.
- Both GitHub CI jobs succeeded on this exact head:
  https://github.com/devam2006/mm-allee-harvesting/actions/runs/41137292297 .
- All 324 rows of `wp05_parameter_metrics.csv` match the previous evidence
  exactly. All 108 prediction rows preserve their error values; runtime changed
  and exit columns were added. All 54 PINN rows report `iteration_limit` with
  the corresponding SciPy message, no error or abnormal exit. Clean recovery
  remains 10/18. This audits the author's rerun; the full sweep was not repeated
  independently here.
- The five-package source passed 521 tests after the merge. Four additional
  integration tests passed against the inverse trainer's actual physics loss
  and the forward residual API, for both models at two nonunit growth/population
  scales. They freeze learning and check the time/harvest conversion rather
  than copy the inverse formula into an oracle. No engine change was required.

The main scientific text now separates poor conditioning under tested settings
from the proven four-unknown Model B ambiguity, and does not claim statistical
equivalence from a handful of seeds. Minor editorial leftovers remain in the
PR description and one source-notebook sentence (universal/structural wording);
the PR #5 notebook uses the scoped wording. The report remains in Overleaf.

Next: owners review the shared settings, physical-parameter/status contracts
and parity evidence. Retarget PR #10 after its WP03 dependency is resolved;
obtain the required human reviews. Working integration is established by
execution checks, not certification of every PINN fit or human agreement.
