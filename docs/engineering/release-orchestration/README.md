# Release Orchestration Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata, typed relations, and lifecycle state—not this directory or index.

This domain governs the repository-specific last mile that starts after a released RLS is merged into `main`: deterministic reconstruction, immutable tag and GitHub Release creation, exact PyPI promotion, release-bound demonstration deployment, replay rules, and post-publication observation.

The orchestration composes the existing `pypi-publication` and `dashboard-publication` controls. It does not replace their operating contracts, authorize a release, or become part of the consumer installation.

## Packet

- `INT-RLO-001`: remove manual identity reconstruction from an authorized release.
- `CAP-RLO-001`: complete the last mile from one governed identity.
- `REQ-RLO-001` through `REQ-RLO-008`: normative orchestration obligations.
- `SPEC-RLO-001`: exact workflow, record, state, and recovery contract.
- `ARCH-RLO-001` and `ADR-RLO-001`: trust-separated orchestration and stable PyPI publisher identity.
- `VER-RLO-001`: deterministic and failure-oriented evidence contract.
- `WO-RLO-001`: bounded implementation authorization proposal.

Acceptance scenarios live under `acceptance/`; implementation evidence will be retained under `evidence/` only after authorized execution.
