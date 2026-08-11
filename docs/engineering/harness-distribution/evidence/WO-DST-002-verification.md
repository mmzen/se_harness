# WO-DST-002 Implementation Evidence

Recorded on 2026-08-11 for the standard harness self-installation.

## Installation contract

- Configuration schema: 2.
- Harness version: 0.2.0.
- Installation profile: the single standard template.
- Lock schema: 1 with 23 managed entries.
- Managed root integrations: one bounded block in `AGENTS.md` and one in `.gitignore`.
- Installed workflow: `.github/workflows/engineering-harness.yml`.
- Installed engineering documents and complete formal artifact-template set are retained under `docs/engineering/`.

## Checks

- `harnessctl doctor`: all runtime, configuration, lock, required-file, and managed-content checks passed.
- Artifact graph: 37 artifacts, zero errors, zero warnings.
- Dashboard: 37 artifacts, 130 relations, zero errors, four `W-REV-001` readiness warnings, snapshot SHA-256 `72b5b9ec48a79a67fc62157e1155750360258b5e6f883dfee98c8c337b510bb4`.
- Full regression suite: 26 tests executed successfully with two expected Windows symlink-privilege skips.

The four dashboard warnings identify verified historical work orders `WO-DOC-001`, `WO-DOC-002`, `WO-DST-001`, and `WO-REV-002` that do not yet have commit-bound verification records under the newly active schema-2 policy. They are retained readiness debt, not artifact-graph validation failures.

The self-installation commit is intentionally obtained from Git history after creation. No tag, push, release, or publication is authorized.
