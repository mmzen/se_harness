+++
id = "WO-AUT-004"
type = "work_order"
title = "Report authoring advisories apart from errors and warnings"
status = "approved"
owners = ["engineering-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the validator report every harnessctl command reads and the summary the managed lane prints; later decisions rely on the exact candidate behaviour."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "templates/repository/standard/scripts/inspect_engineering_artifacts.py",
  "se_harness/cli.py",
  "tests/test_artifact_authoring_policy.py",
  "tests/test_validation_taxonomy.py",
  "tests/test_inspection.py",
  "tests/test_harnessctl.py",
  "tests/test_predecessor_bootstrap_retirement.py",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harnessctl-check.md",
  "docs/engineering/artifact-authoring/README.md",
  "docs/engineering/artifact-authoring/evidence/",
  "docs/engineering/artifact-authoring/requirements/REQ-AUT-007.md",
  "docs/engineering/artifact-authoring/requirements/REQ-AUT-002.md",
  "docs/engineering/artifact-authoring/specifications/SPEC-AUT-002.md",
  "docs/engineering/artifact-authoring/specifications/SPEC-AUT-001.md",
  "docs/engineering/artifact-authoring/verification/VER-AUT-002.md",
]

[relations]
implements = ["REQ-AUT-007"]
specifications = ["SPEC-AUT-002", "SPEC-AUT-001"]
architecture = ["ARCH-AUT-001", "ADR-AUT-001"]
verification = ["VER-AUT-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T08:59:22Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-30 with the words 'Approve and start WO-AUT-004', as a decision distinct from the approval of its definitions in the same transaction. Authorizes start preflight and then only the declared scope: the template validator's advisory class, summary and JSON, the template inspect script if the report requires it, validate --advisories in cli.py, the five test modules, the two notes, the amendment records on REQ-AUT-002 and SPEC-AUT-001, this domain's index and the evidence packet. It authorizes no change to a hash-locked root file, any error code or plane, the authoring policy, doctor, any verification record, no release and no publication. Start preflight has not been run."
+++

# Work Order: Report authoring advisories apart from errors and warnings

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Give the validator report a third class, *advisory*, and move the
`W-AUT-*` family into it (`AUT-ADV-001`); raise those signals only on
drafts (`AUT-ADV-002`); print a fourth number in the summary and list
advisories on request (`AUT-ADV-003`, `AUT-ADV-005`); keep the JSON
complete (`AUT-ADV-004`); leave the consumers untouched beyond what the
report gives them (`AUT-ADV-006`); say so in two notes (`AUT-ADV-007`);
and record on `REQ-AUT-002` and `SPEC-AUT-001` that the four codes are
advisories now. Issue #283, functional assessment of 2026-08-30.

## Why now

`validate .` reads `0 errors, 485 warnings` on a clean tree; 416 are
`W-AUT-*` on approved artifacts. The number an operator and every lane
reads first has stopped meaning anything.

## In scope

- The template validator: the advisory list in the report, the status
  condition, the summary and `--advisories` rendering, the JSON keys.
- The template inspect script only if it reads a key the report renames
  (expected: no change).
- `se_harness/cli.py`: `validate --advisories` passed to the script.
- Tests named in the scope; `test_predecessor_bootstrap_retirement.py`
  only because its root-versus-candidate validator ledger must declare
  the inserted lines.
- The two notes; the domain index; the packet; the two amendment records.

## Out of scope

The root copies under `scripts/` (hash-locked 0.11.0); any error code or
plane; the authoring policy document; the `create-artifact` checklist;
`doctor`; the release carrying this change.

## Authorized decision envelope

The wording of the summary and of the notes; test names; whether the
inspect script needs any edit.

## Constraints

- No root hash-locked file moves.
- Errors, planes and every non-`W-AUT` warning are unchanged in code and
  count.

## Expected change surface

One template script (possibly two), one product module, up to five test
modules, two notes, two amendment records, the packet and the index.

## Required verification

Execute `VER-AUT-002` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/artifact-authoring/evidence/WO-AUT-004/`.

## Stop and escalate conditions

Any need to change an error code or a plane; any hash-locked file in the
change set; any consumer test that can only pass by re-adding advisories
to `warnings`.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
