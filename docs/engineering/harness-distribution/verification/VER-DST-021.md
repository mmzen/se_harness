+++
id = "VER-DST-021"
type = "verification"
title = "Repository-context retirement evidence contract"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
verifies = ["REQ-DST-065"]
+++

# Verification Contract: Repository-context retirement evidence contract

## Independence

Every automated expectation is derived from an observable artifact rather than from the implementation's own constants:

- Scaffold absence is asserted by enumerating the template tree for `*.seed` files, not by naming the retired file.
- Lock convergence is asserted by comparing regenerated locks across the four prior-state rows of `SPEC-DST-021`, not by asserting a hard-coded map.
- Owner-content preservation is asserted by byte comparison of the file before and after upgrade.
- Diagnostic-family retirement is asserted by scanning the emitted diagnostic codes of a full preflight run over a repository crafted to trigger the retired conditions, not by grepping for removed identifiers.

Verification must fail if the implementation narrows the scaffold instead of retiring it, or retains a lock tombstone, or deletes owner content.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-DST-065.1 | automated test | fresh `init` into an empty directory | no file exists at the retired path; no `*.seed` template maps to it; the template tree contains no successor seed for operational facts |
| REQ-DST-065.2 | automated test | fresh `init`, then `start` preflight for an approved work order | report is ready; emitted diagnostic codes contain no `C` family member; the retired path is absent from the reading manifest |
| REQ-DST-065.3 | automated test | four-row upgrade matrix from `SPEC-DST-021`'s state model | regenerated lock contains no entry for the retired path in all four rows, and the four locks are byte-identical to each other |
| REQ-DST-065.4 | automated test | upgrade over a repository whose retired path holds non-empty owner bytes | file bytes are identical before and after; `doctor` reports no drift, no missing managed file, and no integrity failure for the path |
| REQ-DST-065.5 | automated test | `start` and `review` preflight manifests | manifest equals the policy-path set plus the selected artifact order, with the retired path absent and every other entry and its order unchanged from the recorded baseline |
| REQ-DST-065.6 | automated test and inspection | `init` guidance sequence output | step 1 names the owner-controlled region of `AGENTS.md` and names no scaffolded context document; remaining steps are contiguous and unchanged in content |
| REQ-DST-065.7 | automated test | workflow-contract conformance over a fixture procedure declaring a repository-context action identifier | the contract is rejected; the resolver raises rather than resolving against ungoverned content |
| REQ-DST-065.8 | inspection | release migration note | the note enumerates the withdrawn seed, the retired `C` family, the removed `repository_commands` field, and the report schema advance |

## Acceptance scenarios

Executed against the domain acceptance feature:

1. Fresh installation yields no context document and a ready start preflight.
2. Upgrade preserves an owner-authored context file byte-for-byte and drops the lock entry.
3. Upgrade of a repository that had already deleted the seed produces the same lock as one that had not.
4. A repository blocked today only by unresolved context fields becomes ready with no owner action.
5. A workflow contract declaring a repository-context action identifier fails conformance.

## Property and invariant tests

- **Lock convergence.** For every prior state in the state model, the regenerated lock is byte-identical. This is the invariant that makes retirement idempotent.
- **Upgrade idempotence.** Two consecutive upgrades produce byte-identical locks and leave every owner file unchanged.
- **Owner-content immutability.** For a randomized set of file contents at the retired path, including empty, binary, and CRLF-bearing content, upgrade never alters a byte.
- **No successor scaffold.** No `*.seed` template and no generated path in the template tree declares any field name from the retired field set.
- **Diagnostic-code disjointness.** The set of codes emitted across the full preflight test corpus is disjoint from the retired `C` family.
- **Payload shape.** The `v2` payload differs from the recorded `v1` baseline by exactly the absence of `repository_commands` and the schema string.

## Static and architecture checks

- `python scripts/validate_engineering_artifacts.py --root .` reports zero errors. The warning count is compared against the recorded baseline of 44 rather than an absolute expectation.
- Superseding `REQ-DST-008` and `REQ-IAR-005` is verified to leave zero validator errors. The single expected consequence, `E017` on `OPS-IAR-001`, must be resolved within this work order rather than deferred; a run showing that error is a failure.
- No active governed artifact describes the retired document as a live obligation. Historical evidence, verification records, and release records are excluded from this check and must be unmodified.
- The full unittest suite is compared against the recorded baseline, including the two known environment conditions: the editable-install runtime-identity failure and the CRLF machine-contract comparison. Both are recorded explicitly as environment conditions rather than reported as regressions.

## Security and privacy checks

- Confirm the readiness path no longer reads any repository-authored file whose content is echoed into a report or payload. The retired parser was an untrusted-input surface; its removal is asserted by the absence of a read of the retired path during a traced preflight run.
- Confirm no new path is read or written outside the target root.
- Confirm managed integrity, the released-evaluator boundary, and the transactional upgrade guarantee are unchanged by comparing `doctor` behavior on a managed-drift fixture against the recorded baseline.

## Performance and resilience checks

- No performance expectation is asserted. One removed file read is not a measurable change and a threshold would be noise.
- Resilience: an unreadable file at the retired path, a read-only worktree at that path, and a lock write interrupted mid-upgrade each behave per the existing bounded-recovery contract with no partial writes.

## Manual assessments

- **Recorded 2026-08-21 at approval.** The repository owner accepted the loss of the structured `repository_commands` object from the preflight payload, on the corrected measurement that separates the live label-based parse from the unreachable `CTX-ACT-*` execution form. The owner declined both alternatives put to them: retaining a narrowed five-field scaffold, and relocating a typed command declaration into governed material. Verification shall confirm no replacement scaffold or typed declaration was added, per `SPEC-DST-021` rule 2.
- **Recorded 2026-08-21 at approval.** The technical owner determined that `ARCH-DST-002`, `ARCH-DST-007`, and `ARCH-IAR-001` require no revision and no deciding ADR, on the rationale recorded in `REQ-DST-065`. Verification shall confirm that the implementation revises only their descriptive references to the retired document and reopens no accepted decision, and that no architecture artifact is added.
- **Deferred to the release decision.** The release owner confirms the version increment and the migration note. This is release authority under a separate contract and is not a precondition for this work order leaving `draft`; verification confirms only that the migration note exists and carries the required content.

## Evidence retention

Retain under this domain's `evidence/` directory, keyed to the implementing work order:

- Template-tree seed enumeration before and after.
- The four regenerated locks from the state-model matrix and their byte-comparison result.
- Before and after digests of an owner-authored file at the retired path.
- Full preflight payloads for `start` and `review`, `v1` baseline and `v2` result.
- Validator output before and after the supersessions.
- Unittest output with the baseline comparison and both environment conditions named.
- `doctor` output from the released evaluator executed outside the checkout, with the evaluator identity recorded.
- Preflight output for both phases.

## Residual uncertainty

- Consumers of the preflight payload outside this repository cannot be enumerated, so the breaking-change impact is bounded by the migration note rather than measured.
- The withdrawn action-identifier reference form has zero uses in the shipped and candidate contracts today; a branch not visible from the checked refs could introduce one before this work lands, which the conformance test would surface as a failure rather than silently accept.
- Whether any consumer depends on the `C` diagnostic codes in tooling of their own is unknown and unknowable from this repository.
