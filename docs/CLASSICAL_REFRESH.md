# Reviewed WP01–WP03 refresh, 31 October 2026

This refresh brings the reviewed classical changes into draft integration PR #5.
It does not merge or approve any source PR, update Overleaf, or publish a new
final ZIP. Prem and Rohan's subsequent updates will be integrated separately.

| Package | Reviewed source | Changes included |
|---|---|---|
| WP01 | PR #12 `6deae943d56ce0481a80d2321ce590dbfa567180` | Three clearer Markdown cells: introduction, stable critical-yield evaluation, root algorithm |
| WP01 checksum follow-up | PR #12 `58ff57a9cb183d6df868014a9e789778761232ea` | Corrected legacy notebook checksums; embedded payloads verified unchanged |
| WP02 | PR #9 `cba9051dec77b82f7cf0aafb2ce3d82f1e14d832` | Catch derivation, six comparison rows, four history rows, current evidence and source provenance |
| WP02 Windows fix | PR #9 `49722c6e083e3e0c0517c7ef214c854b0add8ce1` | Canonical POSIX manifest keys and a regression checking their format |
| WP03 | PR #4 `16a05ce2f2c8eabfca7a95bcecf78dd7b5e190c8` | Existing reviewed analysis and user-finalized Colab math delimiters retained |

The shared exact-control fold convention, semistability, basin uncertainty,
extinction policy and dimensional units are unchanged. The examples use
different declared parameter scales: WP02 has `rK=500`, whereas WP03's threshold
example has `rK=70`; their different dimensional critical catches are consistent.
No new mathematical agreement or urgent WP01 source fix is required by this pass.

WP02's runner now reuses `MIN_RK45_RTOL` and records the threshold/basin source
hashes. Current curated WP02 files are copied with their source manifest;
roundoff differences do not change conclusions. Its code, tests and config
match the reviewed source. WP01 changes no code. Existing WP04/WP05 source,
configs, notebook fragments and evidence are retained at their previously
integrated versions, pending the next integration pass.

The small Colab notebook is rebuilt from the owned fragments, preserving all
six of Devam's WP03 Markdown delimiter changes. The public runtime snapshot
must be refreshed to carry the WP02 source/provenance corrections. Legacy
embedded notebooks are also regenerated with consistent manifests.

## Verification

Before applying this refresh, the combined notebook with Raghav's text and
Ashwath's tables ran all 32 code cells without errors in a fresh kernel
(36.82 seconds), using the prior fixed runtime. The WP02/classical tests passed
48 cases on Windows, including the previously failing provenance assertion.
Final refreshed-source and runtime verification is recorded below after it runs.

## Handoff

Devam owns this integration, runtime refresh, reproduction and eventual ZIP.
Raghav owns WP01 content; Ashwath owns WP02 content and provenance. Prem and
Rohan retain WP04/WP05 ownership. Human approvals and any main merge remain
separate from these computational checks.

The tracked ZIPs and public `notebook-eps-v1` release remain earlier snapshots.
Rebuild the final notebook/EPS ZIP once the remaining WP04/WP05 updates land;
do not describe the existing ZIP as containing this refresh.
