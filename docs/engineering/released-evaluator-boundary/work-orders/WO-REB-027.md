+++
id = "WO-REB-027"
type = "work_order"
title = "Make the evaluator upgrade simple: payload identity, no packet, index installs"
status = "implemented"
owners = ["engineering-owner", "repository-owner", "security-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The upgrade transaction and the identity proofs are the trust boundary every root write and every managed lane depends on; the next release ships them and the next adoption relies on them."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "se_harness/mutation_guard.py",
  "se_harness/upgrade_authorization.py",
  "se_harness/installer.py",
  "se_harness/cli.py",
  "se_harness/evaluator_identity.py",
  "se_harness/runtime_identity.py",
  "se_harness/release_qualification.py",
  "templates/repository/standard/.github/workflows/engineering-harness.yml",
  ".github/workflows/candidate-evidence.yml",
  "repository_tools/predecessor_facts.py",
  "tests/",
  "docs/notes/developing-se-harness.md",
  "docs/engineering/released-evaluator-boundary/",
]

[relations]
implements = ["REQ-REB-027", "REQ-REB-028"]
specifications = ["SPEC-REB-012"]
architecture = ["ARCH-REB-011", "ADR-REB-011"]
verification = ["VER-REB-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T15:20:02Z"
decided_by = "engineering-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'Approve and start', on the owner's direction that the evaluator upgrade must be simple: the MG007 work-order packet and the MG004 and RID022 archive-digest requirements are retired, the installed evaluator's version and payload digest are its identity, index installs pass the managed lane, and the candidate-evidence lane selects the acceptance operation by the verifier's capability. REQ-REB-005 is superseded under WO-REB-027. Approval authorizes start preflight and then only the declared work inside the execution scope; completion, verification, release and adoption are separate acts."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-27T15:20:06Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's decision of 2026-08-27; start preflight PASS with the exact public 0.6.0 evaluator outside the checkout on branch governance/reb-027-simple-upgrade off main 7284743."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-27T15:46:46Z"
decided_by = "implementation-actor"
+++

# Work Order: Make the evaluator upgrade simple: payload identity, no packet, index installs

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.

## Objective

Carry out `ADR-REB-011`: an installed released evaluator — index or wheel
install — upgrades a standard root with `harnessctl upgrade . --apply`,
proving itself by version and installed-payload digest, without a work-order
packet; the managed workflow and the repository's candidate lanes pass on
index installs. This is the change the 0.7.0 adoption (`WO-HUP-006`,
rejected) needed and could not make.

## In scope

- `mutation_guard.py`: drop the PEP 610 archive requirement and the
  `MG007` packet path; `MG004` only when the evaluator cannot identify
  itself; the codes stay reserved.
- `upgrade_authorization.py`: retire (delete) with its tests.
- `installer.py`, `cli.py`: no `--work-order`; `--evidence-output` optional;
  evidence document without packet fields; lock `archive_sha256` nullable.
- `evaluator_identity.py`, `runtime_identity.py`: a missing archive digest
  is reported, not diagnosed; `RID022` only on a recorded digest that
  differs.
- `release_qualification.py`: `released-root` accepts a lock or an
  installation without an archive digest.
- Managed template `engineering-harness.yml`: keep the index install; the
  step passes once the evaluator accepts it. The root copy is not edited.
- `.github/workflows/candidate-evidence.yml`: `qualify candidate-package`
  when the verifier carries `qualify`, legacy `accept-candidate` otherwise,
  with assertions per operation; `predecessor_facts` derives the capability.
- Supersede `REQ-REB-005` by direct edit (Supersession section, as
  `REQ-DST-008`); amend `SPEC-REB-002` rule 1 with a dated paragraph.
- Tests for every case `VER-REB-011` lists; notes; evidence; packet index.

## Out of scope

Releasing (the next release packet); adopting the result as this
repository's root (a later work order); any other guard (`MG001`–`MG003`,
`MG005`, `MG006`), `RID018`, `RID021`; the lock schema.

## Authorized decision envelope

The evidence document's exact field set once the packet fields go; how the
candidate-evidence lane detects the verifier's `qualify` capability (derived
fact or `--help` probe); test fixture layout.

## Constraints

No credential, network write or root change of this repository; the root
stays exact public 0.6.0 and every lifecycle act uses it; candidate source
never acts as the evaluator; determinism of plan, lock and evidence.

## Expected change surface

Seven product modules (one deleted), the managed workflow template, the
candidate-evidence workflow, `predecessor_facts`, tests, one note, the
requirement supersession and specification amendment, evidence.

## Required verification

`VER-REB-011` in full; repository-required checks; full suites on both
runtimes; the pull request's lanes green (the managed lane under the 0.6.0
root is unaffected by the template change); handoff check.

## Evidence to record

`docs/engineering/released-evaluator-boundary/evidence/WO-REB-027-verification.md`.

## Stop and escalate conditions

Stop if isolation (`RID018`) or the payload proof (`RID021`) would weaken, if
a managed-root write could happen from candidate source, or if the lock
schema would have to change.

## Completion report format

The `harnessctl check . --artifact WO-REB-027 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
