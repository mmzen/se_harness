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
- `WO-RLO-002`: implemented bounded correction with commit-bound assurance recorded by verified `VREC-RLO-002`; no release or publication is implied.

Correction acceptance scenarios are retained in `acceptance/release-policy-boundary.feature`; implementation evidence is retained in `evidence/WO-RLO-002-verification.md`. The approved RLO-001 artifacts and their verification records remain unchanged historical authority.

## Maintenance-line packet

The repository release workflow currently materializes the exact tag, GitHub Release, PyPI files, and demonstration but leaves maintenance-line creation as a separate manual action. RLO-003 proposes closing that repository-local gap without adding branching policy to portable SE Harness.

- `REQ-RLO-012`: create or verify the canonical `release/MAJOR.MINOR` line from the released candidate.
- `SPEC-RLO-003`: exact derivation, creation, replay, conflict, and failure contract.
- `ARCH-RLO-003` and `ADR-RLO-003`: repository-owned mutable-ref boundary with fail-closed reconciliation.
- `VER-RLO-003`: workflow, state, security, replay, and portable-boundary verification.
- `WO-RLO-003`: completed bounded repository workflow implementation with commit-bound assurance recorded by verified `VREC-RLO-003`; no release, publication, or branch action is implied.

Acceptance scenarios are retained in `acceptance/maintenance-line-reconciliation.feature`; implementation evidence is retained in `evidence/WO-RLO-003-verification.md`. The completed work creates no production branch and implies no VREC, release, publication, or deployment.

## Publication-rehearsal packet

Issue [#111](https://github.com/mmzen/se_harness/issues/111) records `RC-060-11` from the immutable `0.6.0` release-recovery analysis: real hosted platform details were tested too late. The orchestrator's credential-free work is split so that `resolve` runs only on `ubuntu-latest` and `qualify` only on `windows-2022`, leaving each half unexercised on the other platform until a live release. RLO-005 rehearses the whole credential-free surface on both platforms before release approval and leaves the orchestrator unchanged.

- `CAP-RLO-003`: rehearse the credential-free last mile before release approval.
- `REQ-RLO-015`: run every credential-free mechanic on both runner platforms, creating no external state.
- `REQ-RLO-016`: fail closed when the orchestrator's credential-free mechanics and the rehearsal's coverage diverge in either direction.
- `SPEC-RLO-005`: exact mechanic inventory, platform-neutrality, determinism, teardown, and divergence contract.
- `ARCH-RLO-005` and `ADR-RLO-005`: a parallel credential-free lane behind a checked equivalence seam, recording the deferred shared-implementation refactor and its revisiting condition.
- `VER-RLO-005`: platform, determinism, teardown, classification, and divergence verification.
- `WO-RLO-005`: bounded implementation authorized on 2026-08-24; no release, publication, deployment, or external action is implied.
- `WO-RLO-006`: repair the teardown link probe, which is inert before Python 3.12 and therefore inert on the pinned runtime, so a junction is unlinked rather than recursed through under `SPEC-RLO-005` rules 19 and 21. Drafted, approved, started, and `implemented` on 2026-08-25 on an owner routing decision taken during the 0.7.0 qualification; it amends no governing artifact and places no bytes in the distributed surface. Commit-bound verification is `required` and still owed.
- `WO-RLO-007`: make the recipe replay complete on a hosted runner by handing the producer's root-owned workspace back to the runner user before teardown. Drafted 2026-08-26 after the first hosted execution of the reusable qualification definition (pull request #173, `WO-CIP-002`) showed that every hosted recipe replay to date fails with `Operation not permitted` in `repository_tools.release_build`'s teardown; the 0.7.0 release path depends on it. Draft; nothing is approved.

Acceptance scenarios are retained in `acceptance/publication-rehearsal.feature`; implementation evidence is retained in `evidence/WO-RLO-005-implementation.md`. A rehearsal result is derived operational evidence: it does not approve, prepare, verify, or release anything, and it does not substitute for the qualification that runs inside an authorized release.

This packet was written as `RLO-004` and renumbered to `RLO-005` when the build-recipe packet below merged first and bound those identifiers to verified `VREC-RLO-004`. The two packets are independent: the build recipe governs *what* an authorized release builds, and this one rehearses the credential-free path that builds it.

## Complete build-recipe implementation

GitHub issue [#110](https://github.com/mmzen/se_harness/issues/110) records RCA root cause `RC-060-10`: the accepted distribution hashes were bound, but the complete producer that created them was split between release metadata, workflow YAML, hosted-runner state, and unrecorded environment/tool details. The approved RLO-004 packet governs one candidate-tree declarative recipe, an immutable OCI producer, recipe-bearing distribution schema 2, and exact hosted replay before release approval.

- `REQ-RLO-013`: bind the complete producer, runtime, toolchain, environment, command, normalization, and output recipe.
- `REQ-RLO-014`: independently replay that bound recipe in a hosted no-credential lane before release approval.
- `SPEC-RLO-004`: exact recipe, bundle/RLS schema, interpreter, replay, compatibility, and failure contract.
- `ARCH-RLO-004` and `ADR-RLO-004`: one strict repository interpreter and digest-pinned producer, with isolated schema-1 history.
- `VER-RLO-004`: independent schema, supply, environment, command, local/hosted replay, workflow, and compatibility evidence.
- `WO-RLO-004`: approved bounded work currently in progress; completion, hosted dispatch, later lifecycle, commit, push, release, and external actions remain separate decisions.

Acceptance scenarios are retained in `acceptance/release-build-recipe.feature`; implementation evidence is retained in `evidence/WO-RLO-004-verification.md`. The packet preserves `RLS-SEH-012`, v0.6.0 bytes, portable release governance, and consumer installations. Native Linux and Windows publication-path rehearsals remain the separate scope of issue [#111](https://github.com/mmzen/se_harness/issues/111).
