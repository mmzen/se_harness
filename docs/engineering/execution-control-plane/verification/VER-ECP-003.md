+++
id = "VER-ECP-003"
type = "verification"
title = "Independent evidence for the mandatory scope-aware pull-request gate and the widened restitution digest"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-27"
updated = "2026-08-28"

[relations]
verifies = ["REQ-ECP-006", "REQ-ECP-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Verification Contract: Independent evidence for the mandatory scope-aware pull-request gate and the widened restitution digest

## Amendment of 2026-08-28 (`WO-ECP-003`, before start)

The `REQ-ECP-006` demonstration is executed locally rather than as hosted
pull requests: the managed template step's shell is run against two
throwaway branches of this repository — one whose diff touches one
out-of-scope path, one entirely in scope, neither declaring a
`Harness-Restitution:` line — with the candidate evaluator installed outside
the checkout and the pull-request event payload synthesised from the
branch. The pass condition is unchanged (the scope step has no guard on a
declared digest and no early exit on its absence; the out-of-scope branch
fails with `QGP-G4I-PATHS` and the offending path in the log; the in-scope
branch passes). The hosted form of the same demonstration is a verification
condition of the first release that carries `WO-ECP-001` to `WO-ECP-003`:
this repository's own pull requests run the root managed workflow, released
0.8.0's, which cannot execute the step until the root advances.

## Independence

Expected behaviour derives from `REQ-ECP-006`, `REQ-ECP-007`, and the
`ECP-GTE-` and `ECP-DIG-` rules of `SPEC-ECP-003`, read against
`ARCH-ECP-001` and the proposed outcome of `ADR-ECP-002`. Expected digests
are recomputed by the test from the canonical block bytes with its own
SHA-256 call, never read from the candidate. Workflow behaviour is exercised
through the managed workflow file rendered into a disposable consumer
repository and through pull requests on throwaway branches of this
repository.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-006` gate enforces scope unconditionally | test: workflow YAML assertions; demonstration: throwaway pull requests | PR without any `Harness-Restitution:` line; PR whose diff touches one out-of-scope path; PR entirely in scope | the scope step has no guard on a declared digest and no early `exit 0` on its absence (today `templates/repository/standard/.github/workflows/engineering-harness.yml:65-68` exits 0 when no line is declared); the out-of-scope PR's required check is red with `QGP-G4I-PATHS` and the offending path in the log; the in-scope PR is green |
| `REQ-ECP-007` digest covers change set and gates | test: canonical block content; digest sensitivity | two results with equal restitution fields and different changed-path sets; a completeness assertion flipped; one predicate status flipped | the canonical block contains the sorted changed-path set, the completeness assertion, and every predicate status; each of the three edits changes `result_sha256`; two results with identical inputs share one digest across LF and CRLF rendering |

## Acceptance scenarios

### Scenario 1: out-of-scope path in the pull-request diff fails the gate

On a throwaway branch, name an approved work order in the trailer and add
one file outside its execution scope. Open a pull request. Assert the
required check fails, the log names the path and `QGP-G4I-PATHS`, and no
step was skipped on an absent restitution line.

### Scenario 2: no restitution line, still evaluated

Open a pull request whose body carries the work-order line and no
restitution line. Assert the scope step runs and reports the derived diff
set; assert it fails when the diff is out of scope and passes otherwise.

### Scenario 3: same restitution, different change set, different digest

Build two schema-2 results at one snapshot that differ only in the
changed-path set. Assert different `result_sha256` (today the preimage
renders restitution fields only, `se_harness/workflow_result.py:174-207`,
so the digests would be equal).

### Scenario 4: failure path, digest declared over a stale change set

Declare a restitution line computed before adding a file. Push the file.
Assert the recomputed digest differs and the check fails naming both digests
and the snapshot.

### Scenario 5: cross-platform digest equality

Render the same block on Linux and on Windows. Assert equal digests.

## Property and invariant tests

- The digest is a function of the canonical block only: permuting the input
  order of changed paths yields one digest.
- Every predicate status in `gate_results` appears in the block exactly
  once.

## Static and architecture checks

- The template workflow's scope step is unconditional on the pull-request
  event: `grep -n "nothing to verify" templates/repository/standard/.github/workflows/engineering-harness.yml`
  returns nothing.
- `templates/repository/standard/scripts/select_harness_work_order.py` and
  the root managed copy are byte-identical after the managed refresh.

## Security and privacy checks

- The gate reads the diff from `git`, never from the pull-request body;
  a body listing a smaller change set cannot narrow the evaluated set.
- The workflow keeps read-only `permissions` and uses no secrets.

## Performance and resilience checks

- The gate fetches the base with `--depth=1` and completes the check within
  the existing job time budget; figure recorded from the demonstration run.

## Manual assessments

The assurance owner reads the failing check log of Scenario 1 and confirms
the corrective names `DR-REMEDIATION-SCOPE`, not a rerun.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ID/`: the
throwaway pull-request URLs and run identifiers, the check logs, the two
canonical blocks and digests of Scenario 3, and per-platform test figures.

## Pass criteria

Every deterministic test passes on Linux and on Windows, figures labelled per
platform. Both demonstration pull requests are evaluated by the workflow
installing the exact released evaluator, se-harness 0.7.1, outside the
checkout, with the required-check outcomes stated above. The throwaway
branches are deleted afterwards and recorded as such.

## Residual uncertainty

Whether the check is marked required is a repository setting outside the
tree; the demonstration records the setting but cannot pin it.
