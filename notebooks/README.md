# Notebook ownership and execution

Edit only your chosen task fragment in `sections/`. Each needs detailed Markdown with equations, assumptions and the algorithm **before** code, labelled plots, output interpretation and limitations. Use accessible colour callouts; code imports the shared package rather than reimplementing equations.

The WP05 owner assembles `project.ipynb` with `python scripts/assemble_notebook.py`. The result is deterministic, clears execution outputs and has no hidden state. Execute a copy under `results/` for verification. Starter fragments are clearly labelled incomplete; successful starter execution does not satisfy scientific deliverables.

Final notebook execution must include the real budgeted forward/inverse pipeline or explicitly load curated outputs with supplied regeneration commands, distinguishing that from retraining. Remove scaffold markers only when their requested content is actually complete.
