# WP01 notebook refresh from Raghav PR #13

Imported only WP01 from Raghav's PR #13 commit
`d555f01541eed69ac54c2f11ceed3e9f4ccaed5b` into PR #5 baseline
`9d96b85e14296b464c9545749048eb7077dec64f`.

The explanation is shorter: 13 to 9 Markdown cells and 7 to 5 code cells.
The scaling-identity check, numerical maximum check, polynomial-root example
and verbose residual printouts are omitted from the presentation. The shared
implementation, tests, three WP01 figures, thresholds and stability results
are unchanged. The illustrative maximum catch is approximately 263 tonnes/year.

The only adaptation to Raghav's supplied section is putting the main-result
body outside raw HTML while keeping its colored heading and identical prose
and mathematics, so Colab can render dollar-delimited equations.

## Preservation and checks

- Every non-WP01 cell and all notebook metadata are exactly identical to the
  latest baseline in all five assembled/portable notebooks. In particular,
  the latest WP02, WP03, WP04 and Rohan WP05 changes are retained.
- The owned WP01 fragment reproduces the assembled sections. All model/trainer
  source, configs, runtime loader/pin, frozen tables, figures, introduction,
  acknowledgements and blank Overleaf template are unchanged.
- Legacy embedded payloads and their source-file inventories are unchanged;
  only WP01 display cells and the outer notebook checksums are refreshed.
- Fresh-kernel final Colab notebook: **27 code cells, zero errors, 45.83 seconds**,
  **17 PNG outputs**, using the existing public runtime.
- **195 WP01 and Colab-export tests passed in 17.89 seconds**. Ruff lint/format,
  whitespace, assembly, checksum and scope checks passed. The unchanged full
  source suite previously passed 531 tests at the WP05 baseline; it was not
  rerun for this presentation-only change.
- All **19 EPS figures** are byte-identical to v3. Only the notebook changes
  inside the 20-file minimal ZIP. The source PR's older ZIP was not imported.

## Current download

- [Open in Colab](https://colab.research.google.com/github/devam2006/mm-allee-notebook-runtime/blob/main/project.ipynb)
- [Download notebook](https://github.com/devam2006/mm-allee-notebook-runtime/releases/download/notebook-eps-v4/project.ipynb)
- [Download notebook and 19 EPS figures](https://github.com/devam2006/mm-allee-notebook-runtime/releases/download/notebook-eps-v4/mm-allee-final-notebook-eps.zip)

Notebook: **88,495 bytes**, 62 cells / 27 code cells.
SHA-256: `f309913a7f32c191dc7f8d86d3b174f6cd063d41cc2896e9a99e05b37673b799`.
ZIP: **526,471 bytes**, 20 files.
SHA-256: `ee61d1224e4eac36fe29c4c6068e7ec1400068cb95356bc00ed7f2956edce0c3`.

Older versioned releases remain unchanged. This is a selective integration,
not a formal merge or human approval of Raghav's PR. All examples are synthetic;
report writing and remaining human reviews remain separate.
