+++
id = "WO-REB-031"
type = "work_order"
title = "Remove the expired 0.6.0 bootstrap acceptance path"
status = "approved"
owners = ["engineering-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters how the candidate lane produces acceptance evidence for every pull request; later release decisions rely on that evidence, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".github/workflows/candidate-evidence.yml",
  "repository_tools/evaluator_facts.py",
  "tests/test_release_qualification.py",
  "tests/test_standard_repository_lifecycle.py",
  "tests/test_ci_pipeline.py",
  "tests/test_predecessor_bootstrap_retirement.py",
  "docs/notes/developing-se-harness.md",
  "docs/notes/release-qualification-roles.md",
  "docs/notes/ci-pipeline.md",
  "docs/engineering/released-evaluator-boundary/README.md",
  "docs/engineering/released-evaluator-boundary/evidence/",
  "docs/engineering/released-evaluator-boundary/requirements/REQ-REB-031.md",
  "docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-016.md",
  "docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-010.md",
  "docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-012.md",
  "docs/engineering/released-evaluator-boundary/verification/VER-REB-015.md",
]

[relations]
implements = ["REQ-REB-031"]
specifications = ["SPEC-REB-016", "SPEC-REB-010", "SPEC-REB-012"]
verification = ["VER-REB-015"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T18:55:32Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-30 by selecting the presented option 'Approve, start, complete on green', as a decision distinct from the approval of its definitions in the same transaction. Authorizes start preflight and then only the declared scope: the typed-only acceptance step, the evaluator-facts table and fact removal, the four re-pinned test modules, the three notes, the amendment records on SPEC-REB-010 and SPEC-REB-012, this domain's index and the evidence packet; and authorizes marking the work order implemented once the declared evidence is green. It authorizes no change to a hash-locked root file, no product module, no verification record, no release and no publication; the pull request's merge remains the owner's decision. Start preflight has not been run."
+++

# Work Order: Remove the expired 0.6.0 bootstrap acceptance path

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Make the typed operation the only acceptance path of the candidate lane
(`REB-BFH-001`); remove the legacy acceptance-contract table and fact from
the evaluator-facts derivation (`REB-BFH-002`); stop retaining a legacy
bootstrap artifact (`REB-BFH-003`); keep every other derived fact and its
literal-free assertion (`REB-BFH-004`); re-pin the conformance tests to the
typed-only shape (`REB-BFH-005`); leave the tombstone and history alone
(`REB-BFH-006`); and record the executed expiry on `SPEC-REB-010` and
`SPEC-REB-012` with amendment records. Issue #285 item #285a, on the owner's
floor decision of 2026-08-30: "the 0.6.0 bootstrap path is history."

## Why now

The fallback expired by `SPEC-REB-010`'s own words when 0.7.0 exposed the
typed command; the declared root is 0.11.0 and the command it would call is
a tombstone. What remains is a dead branch, a digest table, environment
plumbing and tests that pin all of it byte-wise.

## In scope

- The `candidate-package` job's acceptance step: typed invocation only, no
  probe, no legacy retention step, no legacy environment value.
- `repository_tools/evaluator_facts.py`: the legacy table, the derived
  fact, and its output line removed.
- The four test modules named in the scope, re-pinned to the typed-only
  shape.
- The three notes' sentences describing the legacy fallback.
- The two amendment records; this domain's index; the evidence packet.

## Out of scope

The `accept-candidate` tombstone in `se_harness/cli.py` and its tests
(assessment item #285c); `se_harness/release_qualification.py` and
`se_harness/candidate_acceptance.py` (the typed operation itself, and issue
#213's proposed relocation of the self-hosting operations, which stays
open); retained historical evidence; any hash-locked root file; the release
carrying this change.

## Authorized decision envelope

Workflow step wording; test names; how the notes phrase the removal. The
implementer may not add any new acceptance path, fact, or artifact.

## Constraints

- No version or digest literal for the evaluator returns to the
  repository-owned workflows.
- Retained evidence under `docs/engineering/` is never edited or relabeled.
- The word "governor" is not introduced into `docs/notes/`.

## Expected change surface

One workflow, one repository tool, four test modules, three notes, two
amendment records, the packet and the index.

## Required verification

Execute `VER-REB-015` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/released-evaluator-boundary/evidence/WO-REB-031/`.

## Stop and escalate conditions

Any need to touch `se_harness/` product code; any hash-locked file in the
change set; any test that can only pass by keeping a second acceptance
path; any lane that needs a fact the derivation no longer exports.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
