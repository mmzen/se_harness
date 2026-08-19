# Release Orchestration Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata, typed relations, and lifecycle state—not this directory or index.

This domain governs the repository-specific last mile that starts after a released RLS is merged into `main`: deterministic reconstruction, immutable tag and GitHub Release creation, exact PyPI promotion, release-bound demonstration deployment, replay rules, and post-publication observation.

The orchestration composes the existing `pypi-publication` and `dashboard-publication` controls. It does not replace their operating contracts, authorize a release, or become part of the consumer installation.

## Initial orchestration packet

- `INT-RLO-001`: remove manual identity reconstruction from an authorized release.
- `CAP-RLO-001`: complete the last mile from one governed identity.
- `REQ-RLO-001` through `REQ-RLO-008`: normative orchestration obligations.
- `SPEC-RLO-001`: exact workflow, record, state, and recovery contract.
- `ARCH-RLO-001` and `ADR-RLO-001`: trust-separated orchestration and stable PyPI publisher identity.
- `VER-RLO-001`: deterministic and failure-oriented evidence contract.
- `WO-RLO-001`: completed bounded implementation work.
- `VREC-RLO-001`: verified commit-bound assurance for the RLO-001 candidate.

Acceptance scenarios live under `acceptance/`; retained RLO-001 implementation evidence lives under `evidence/`.

## Portable-boundary correction packet

Issue [#71](https://github.com/mmzen/se_harness/issues/71) identified that the repository-specific workflow remained local while its Python distribution schema leaked into portable `harnessctl`, managed validation, and consumer templates. The correction preserves the original release outcome while restoring repository-policy independence.

- `CAP-RLO-002`: separate portable release governance from repository publication.
- `REQ-RLO-009` through `REQ-RLO-011`: format-neutral core preparation, repository-owned binding, and preserved one-input publication.
- `SPEC-RLO-002`: exact responsibility, compatibility, state, and failure contract.
- `ARCH-RLO-002` and `ADR-RLO-002`: one-way dependency from repository policy to portable governance, without a plugin framework.
- `VER-RLO-002`: package, consumer, binder, workflow, and failure-oriented verification.
- `WO-RLO-002`: implemented bounded correction awaiting separate commit-bound assurance.

Correction acceptance scenarios are retained in `acceptance/release-policy-boundary.feature`; implementation evidence is retained in `evidence/WO-RLO-002-verification.md`. The approved RLO-001 artifacts and `VREC-RLO-001` remain unchanged historical authority.
