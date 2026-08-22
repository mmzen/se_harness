+++
id = "REQ-REB-013"
type = "requirement"
title = "Assess successor candidates through the exact predecessor-compatible view"
status = "approved"
owners = ["requirements-steward", "repository-owner", "security-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"
statement = "WHEN the locked predecessor evaluator cannot parse an exact closed rejected-bootstrap pair during hosted assessment, THE SYSTEM SHALL run that unchanged evaluator against the same deterministic two-artifact compatibility view while separately retaining its exact full-checkout refusal and complete-graph candidate validation."
verification_method = "automated-hosted-predecessor-assessment-view-and-exact-refusal-replay"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T07:15:02Z"
decided_by = "requirements-steward"
+++

# Requirement: Assess successor candidates through the exact predecessor-compatible view

## Rationale

Hosted C4 run `32558379907` proved that exact released evaluator 0.5.0 still reaches the formal graph and refuses rejected `RLS-SEH-009` with `E009`. That is the already documented syntax boundary, but `WO-REB-006` applied the compatibility view only to predecessor release preparation. The ordinary hosted workflow therefore cannot complete against any candidate retaining the required rejection history.

The released evaluator must remain unchanged and must not be claimed to understand the full graph. Hosted assurance can nevertheless exercise its managed-integrity, doctor, validation, and dashboard behavior against the exact same closed view used for preparation, while candidate validation continues assessing the complete graph.

## Preconditions and trigger

- The candidate is one clean committed SHA and passes complete-graph candidate validation.
- The only unsupported history is the exact rejected `REL-SEH-008` and `RLS-SEH-009` pair already governed by `REQ-REB-012`.
- Their candidate-commit paths, Git blobs, raw hashes, statuses, relations, and predecessor tuple match retained governance.
- The external interpreter, entry point, wheel, payload, version, and schema-2 lock prove exact released evaluator 0.5.0.
- The unchanged legacy full-checkout workflow reaches validation and reports exactly the expected rejected-status diagnostic, with no identity, integrity, structure, policy, or additional governance failure.

## Required response

- Reuse one shared closed-pair derivation and exact-commit view implementation for preparation and assessment.
- Run released 0.5.0 identity, `doctor`, `validate`, and dashboard generation only inside the exact two-artifact view.
- Run candidate validation against the complete checkout before and after the assessment and prove the source checkout is unchanged.
- Emit canonical assessment evidence binding candidate commit/tree, view paths/specification, omitted Git/raw identities, evaluator identity, exact commands, return codes, graph counts, and output digests.
- Retain the legacy full-checkout `E009` result explicitly as an expected predecessor limitation; never relabel that workflow as passing.
- Fail qualification on any additional legacy diagnostic, changed omission, view drift, candidate failure, runtime contamination, checkout mutation, or evidence mismatch.

## Failure and boundary behavior

The assessment refuses arbitrary paths, more or fewer than the exact pair, an uncommitted or mismatched source, a different evaluator, an unexpected full-checkout result, partial output, credential-bearing environment, or any attempt to turn candidate-owned orchestration into lifecycle authority. Failure produces no repository mutation and cannot be waived by a generic expected-failure rule.

## Constraints

- Do not modify `.engineering-harness.toml`, `.engineering-harness.lock`, `.github/workflows/engineering-harness.yml`, any other root-managed file, released 0.5.0, rejected history, or maintenance state.
- The new hosted lane is candidate evidence executed by the released evaluator; it is not full-graph predecessor acceptance.
- The complete graph remains candidate-validated, and the exact legacy refusal remains independently visible.
- No workflow result approves work, verifies a VREC, releases an RLS, tags, publishes, deploys, or upgrades the root.

## Acceptance examples

### Example: normal behavior

**Given** exact C5, the closed rejected pair, and isolated released 0.5.0

**When** hosted predecessor assessment runs

**Then** the unchanged full-checkout lane records only expected `E009`, the compatibility-view lane passes `doctor` and `validate`, the complete candidate graph passes separately, and no checkout byte changes.

### Example: failure behavior

**Given** an assessment view omitting a third path or a legacy run reporting any second error

**When** qualification evaluates the evidence

**Then** it fails before verification, release preparation, credentials, or publication.

## Open decisions

The draft selects a separate candidate-owned hosted assessment workflow so root-managed files and the locked predecessor remain unchanged. Approval must explicitly accept the honest expected-red legacy workflow plus green exact-view replacement evidence for this transitional release.
