# Operating-contract activation

This packet governs the accountable activation of the six operating contracts already present in the repository. It separates continuing operational commitments from draft release proposals, makes each contract complete enough to operate, and keeps approval distinct from software release.

Chain: `INT-OCA-001` -> `CAP-OCA-001` -> `REQ-OCA-001` -> `SPEC-OCA-001`, `VER-OCA-001` -> `WO-OCA-001`.

The repository owner explicitly approved this packet and authorized `WO-OCA-001` on 2026-08-16. That approval accepts review of the six continuing operating obligations and authorizes only the six contract definitions, their domain indexes, the operating-contract template correction, managed parity, and retained evidence. It does not authorize validator behavior changes, release-contract changes, verification transitions, commits, pushes, pull requests, releases, tags, publication, or deployment.

The bounded implementation is complete. All six contracts are `approved`, assure only their domain requirements, and contain the canonical operating sections. The managed authoring example and lock are synchronized, the six release contracts remain `draft`, and exact results are retained in `evidence/WO-OCA-001-verification.md`. `WO-OCA-001` is `implemented`; one later aggregate VREC may cover this work together with the preceding supersession maintenance at their shared clean candidate commit.

## Executable assurance readiness

The implemented `OCA-002` packet adds only two follow-up controls: enforce `OPS.assures -> REQ` target typing, and require every active operating contract's assured requirement to have active status, completed implementing work, and eligible VREC coverage when commit-bound provenance is configured. It also migrates the two older approved contracts that predate the requirement-only model. No release-to-OPS relation, traceability-diagram redesign, recurring operational assessment artifact, or other operating-model extension is included.

- Requirement: `REQ-OCA-002`
- Specification: `SPEC-OCA-002`
- Verification contract: `VER-OCA-002`
- Implemented work order: `WO-OCA-002`

No architecture artifact or ADR applies. The work changes a local validation invariant and managed policy wording; it introduces no structural software choice and no active architecture addresses `REQ-OCA-002`.
