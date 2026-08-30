+++
id = "REQ-REB-031"
type = "requirement"
title = "Candidate acceptance evidence comes only from the typed operation"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-30"
updated = "2026-08-30"
statement = "WHEN candidate acceptance evidence is produced for a pull request or a push, THE SYSTEM SHALL obtain it only through the released verifier's typed qualify operation, deriving no legacy acceptance-contract fact and retaining no legacy bootstrap artifact."
verification_method = ["test", "analysis"]
priority = "must"
source = "issue #285 (functional assessment FA-6, item #285a) on the owner's floor decision of 2026-08-30: 'the 0.6.0 bootstrap path is history'; issue #213 (complexity audit P1-1), whose bootstrap-fallback finding this executes"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T18:55:32Z"
decided_by = "technical-owner"
reason = "Approved by the accountable owner on 2026-08-30 by selecting the presented option 'Approve, start, complete on green' for WO-REB-031: candidate acceptance evidence comes only from the typed operation, on the owner's floor decision of 2026-08-30 that the 0.6.0 bootstrap path is history (issue #285, item #285a)."
+++

# Requirement: Candidate acceptance evidence comes only from the typed operation

## Rationale

The candidate-evidence lane still carries a second acceptance path: when the
pinned released verifier does not expose `qualify`, the workflow falls back to
the exact public 0.6.0 `accept-candidate` contract, guarded by a digest table
declared in `repository_tools.evaluator_facts`. `SPEC-REB-010` created that
path as a bootstrap exception and stated its own expiry: it "expires when a
released verifier exposes the typed command." Released 0.7.0 exposed it; the
declared root today is 0.11.0; `accept-candidate` itself was removed from the
CLI after 0.11.0 under `WO-ECP-019` and answers only as a tombstone. The
fallback is unreachable by any released verifier this repository will ever pin
again, yet its dispatch probe, digest table, environment plumbing, retention
step and byte-pinning tests all remain. The owner's floor decision of
2026-08-30 makes the expiry an obligation rather than a possibility.

## Preconditions and trigger

The candidate-evidence workflow runs on a pull request or a push; the
`candidate-package` job produces acceptance evidence for the built wheel using
the released verifier derived from the declared root.

## Required response

- The workflow invokes the released verifier's typed `qualify
  candidate-package` operation unconditionally: no capability probe, no
  dispatch on the verifier's help text, and no alternative acceptance branch.
- The evaluator-facts derivation exports no legacy acceptance-contract fact.
  The per-version contract-digest table and the derived
  `acceptance_contract_sha256` output are gone, and no workflow environment
  variable carries a legacy contract digest.
- The workflow retains only the canonical qualification result. No artifact
  named or shaped as a legacy bootstrap result is produced.
- Retained historical evidence under `docs/engineering/` and the
  `accept-candidate` tombstone guard in the CLI are unchanged; the tombstone
  retires separately (assessment item #285c).

## Failure and boundary behavior

A pinned verifier that fails the typed operation fails the lane; nothing
falls back. The derivation still fails closed with its existing `PRE0nn`
codes when the declared root yields no complete fact set. A workflow edit
that reintroduces a second acceptance path is a test failure, not a warning.

## Constraints

No version or digest literal for the evaluator returns to the repository-owned
workflows; every fact still derives from the declared root at run time.

## Acceptance examples

### Example: normal behavior

**Given** this repository with the declared root 0.11.0,

**When** the candidate-evidence workflow runs on a pull request,

**Then** the `candidate-package` job runs exactly one acceptance invocation,
the typed `qualify candidate-package`, and uploads no legacy bootstrap
artifact.

### Example: failure behavior

**Given** a workflow text carrying any `accept-candidate` invocation, any
`qualify --help` capability probe, or any legacy acceptance-contract
environment value,

**When** the conformance tests run,

**Then** they fail naming the reintroduced path.

## Open decisions

None.
