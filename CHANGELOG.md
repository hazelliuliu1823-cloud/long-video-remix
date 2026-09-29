# Changelog

## v1.0.1 — Structure observation layer restored

- Restored a formal human-readable **Frame Observation Index** for Broad Structure instead of leaving downstream users with only contact sheets / raw frame evidence.
- Added `assets/frame-observation-template.csv`.
- Added a formal **Deep Observation Index** for Directed Deep Structure.
- Added `assets/deep-observation-template.csv`.
- Expanded Directed Deep Structure to capture complete visual description, content description, setting context, narrative context, before / after state, dialogue / audio verification, interpretations, unknowns and counterevidence before cut decisions.
- Updated README, workflow, data contracts, worked example, handoff rules and agent metadata accordingly.
- No change to the core Direct boundary, timeline compiler, renderer-neutral architecture or render-audit scripts.

## v1.0.0 — Initial public release

- Broad Structure → Human Direct → Directed Deep Structure → Execute.
- Content Map / Brief / Editorial Plan templates.
- Evidence and timeline contracts.
- Render-manifest compiler and render audit tooling.
- MIT License.
