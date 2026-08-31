+++
id = "SPEC-REB-016"
type = "specification"
title = "Removal of the expired 0.6.0 bootstrap acceptance path"
status = "approved"
owners = ["technical-owner", "engineering-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[relations]
specifies = ["REQ-REB-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T18:55:32Z"
decided_by = "technical-owner"
reason = "Approved by the accountable owner on 2026-08-30 by selecting the presented option 'Approve, start, complete on green' for WO-REB-031: REB-BFH-001 to REB-BFH-006; the typed-only lane, no legacy fact or artifact, amendment records on SPEC-REB-010 and SPEC-REB-012."
+++

# Specification: Removal of the expired 0.6.0 bootstrap acceptance path

## Scope

Removes the legacy `accept-candidate` fallback from the candidate-evidence
workflow and the legacy acceptance-contract fact from the evaluator-facts
derivation. Changes no product qualification code, no tombstone guard, no
retained historical evidence and no root hash-locked file.

## Terms

- **Typed operation:** `qualify candidate-package` of the released verifier,
  producing a `se-harness-release-qualification-v1` result.
- **Legacy path:** the expired `accept-candidate` invocation, its
  digest-bound contract table, and the retention of its
  `se-harness-functional-acceptance-v1` output.

## Behavioral rules

**REB-BFH-001:** The `candidate-package` job of
`.github/workflows/candidate-evidence.yml` invokes the typed operation
unconditionally. The workflow text contains no `accept-candidate`
invocation, no `qualify --help` capability probe, and no conditional
dispatch between acceptance paths.

**REB-BFH-002:** `repository_tools.evaluator_facts` declares no
per-version legacy acceptance-contract digest table and derives no
`acceptance_contract_sha256` fact. Its GitHub-output lines carry no
acceptance-contract key, and no workflow environment variable named
`RELEASED_ACCEPTANCE_CONTRACT_SHA256` exists.

**REB-BFH-003:** The workflow retains the canonical qualification result
only. The legacy bootstrap retention step and the artifact name pattern
`candidate-package-legacy-bootstrap-*` are gone.

**REB-BFH-004:** Every other derived predecessor fact (version, wheel name,
wheel digest, payload digest) is unchanged, still derived from the declared
root at run time, and still asserted literal-free in the repository-owned
workflows.

**REB-BFH-005:** The conformance tests pin the typed-only shape: exactly one
acceptance invocation in the `candidate-package` job, absence of every
legacy string named in REB-BFH-001 to REB-BFH-003, and the existing typed
pins (result schema, `independence == "released-verifier"`) unchanged.

**REB-BFH-006:** The `accept-candidate` tombstone guard in `se_harness/cli.py`,
its refusal tests, and the note rows recording "removed after 0.11.0" are
outside this contract and unchanged by it.

## Coverage

| Requirement | Rules |
| --- | --- |
| REQ-REB-031 | REB-BFH-001 to REB-BFH-006 |

## Failure behaviour

A verifier that cannot run the typed operation fails the lane with the
operation's own diagnostics; no fallback engages. The facts derivation keeps
its `PRE0nn` fail-closed behaviour for an incomplete declared root.

## Compatibility and migration

The bootstrap exception of `SPEC-REB-010` declared its own expiry ("expires
when a released verifier exposes the typed command"); this contract executes
it. Amendment records on `SPEC-REB-010` (the initial 0.6.0 bootstrap
exception) and `SPEC-REB-012` (the legacy dispatch and the legacy bootstrap
retention it required of workflows) record the execution. Retained evidence
of past bootstrap runs under `docs/engineering/` stays valid as history and
is never relabeled, exactly as `SPEC-REB-010` requires.

## Explicitly unspecified decisions

The exact wording of workflow step names and test names is the
implementer's.
