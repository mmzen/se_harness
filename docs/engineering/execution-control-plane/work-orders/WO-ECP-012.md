+++
id = "WO-ECP-012"
type = "work_order"
title = "Resolve evaluator-derived paths on every host, and document the check command"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "The change touches the resolver every evidence packet and handoff check depends on, and the reference operators will read before trusting a check result; both are engineering state later decisions rely on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/artifact_layout.py",
  "se_harness/workflow_compliance.py",
  "tests/test_artifact_authoring.py",
  "tests/test_workflow_compliance.py",
  "tests/test_progressive_documentation.py",
  "docs/notes/harnessctl-check.md",
  "docs/notes/README.md",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
]

[relations]
implements = ["REQ-ECP-019"]
specifications = ["SPEC-ECP-008"]
verification = ["VER-ECP-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T07:45:12Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29 with the words 'i approve the artifact packet, you can start WO-ECP-012', as a decision distinct from the approval of its definitions seconds earlier. Authorizes start preflight and then only the declared scope: the two product modules, the three test modules, the check reference and its index and pointer, this domain's index and the evidence packet. It authorizes no change to a managed or hash-locked file, no verification record, no release and no publication. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-29T07:45:38Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-29, 'you can start WO-ECP-012'. Start preflight PASS with no diagnostics over the approval commit 3433b7d carrying unmoved main aa99773, run with the governing exact public 0.9.0 evaluator outside the checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."
+++

# Work Order: Resolve evaluator-derived paths on every host, and document the check command

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Make `harnessctl evidence` and `harnessctl check` work on Windows by
rendering the evaluator's own artifact path as POSIX before the domain
resolver's text guard sees it (issue #254), prove it with tests that run on
the Linux lane, and add the missing plain-English reference for
`harnessctl check`.

## Why now

Released 0.9.0 refuses both commands on Windows for every work order.
`WO-HUP-009` could hand off only from a Linux runtime, and the same refusal
hides behind ~60 workstation-only test failures that the Linux-only hosted
suite never sees. The reference is added in the same work order because the
refusal showed that an operator reading `WEX-ECP-010` has nowhere to learn
what the command was trying to do.

## In scope

- `se_harness/workflow_compliance.py`: `evidence_packet_path` passes
  `artifact.path.relative_to(root).as_posix()` (`ECP-HST-001`).
- `se_harness/artifact_layout.py`: `artifact_domain_from_relative_path`
  renders a `PurePath` argument with `.as_posix()` before the text guard;
  `str` handling unchanged (`ECP-HST-002`).
- Regression tests with `PureWindowsPath` in `tests/test_artifact_authoring.py`
  (resolver) and `tests/test_workflow_compliance.py` (packet path, including
  the outside-a-domain refusal) (`ECP-HST-004`).
- `docs/notes/harnessctl-check.md` with the sections `ECP-HST-005` lists;
  its line in `docs/notes/README.md`; a pointer from
  `docs/notes/harnessctl-reference.md`; the documentation tests extended so
  the note's identifiers are checked against the contracts.
- The Windows before-and-after suite reading and the caller grep, retained
  in the evidence packet.

## Out of scope

The managed template registry and every hash-locked root file
(`ECP-HST-003`); the line-ending-dependent formal snapshot (issue #256);
the pull-request gate's behaviour after `in_progress` (issue #255); a hosted
Windows test lane; any change to `WORKFLOW.json` or `QUALITY_GATES.json`;
release or publication.

## Authorized decision envelope

The wording and layout of the note within `ECP-HST-005`'s section list; the
names and placement of the test cases; whether the documentation test
checks identifiers by regular expression or by parsing the note's tables.

## Constraints

- No change to the text guard's behaviour for `str` input.
- Template bytes under `templates/` do not move.
- The note derives its tables from the contracts and restates no policy.

## Expected change surface

Two product modules, three test modules, three files under `docs/notes/`,
this domain's index, and the evidence packet.

## Required verification

Execute `VER-ECP-008` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-012/`.

## Stop and escalate conditions

A second caller that passes a `PurePath` and needs a behavioural decision; a
test that cannot express the Windows form with `PureWindowsPath`; any need
to touch a hash-locked file; a contract identifier the note needs that does
not exist.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
