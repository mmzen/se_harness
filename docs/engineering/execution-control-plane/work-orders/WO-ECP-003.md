+++
id = "WO-ECP-003"
type = "work_order"
title = "Make the pull-request gate mandatory and scope-aware, and widen the digest"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes the managed CI workflow that every consumer's required check runs and the preimage of `result_sha256` that CI compares. Integration and release decisions rely on the gate refusing exactly the out-of-scope diffs it claims to, so commit-bound assurance is required."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/.github/workflows/engineering-harness.yml",
  "se_harness/workflow_result.py",
  "se_harness/github_ci.py",
  "templates/repository/standard/scripts/select_harness_work_order.py",
  "tests/",
  "docs/engineering/execution-control-plane/evidence/",
]

[relations]
implements = ["REQ-ECP-006", "REQ-ECP-007"]
specifications = ["SPEC-ECP-003"]
architecture = ["ARCH-ECP-001", "ADR-ECP-002"]
verification = ["VER-ECP-003"]
+++

# Work Order: Make the pull-request gate mandatory and scope-aware, and widen the digest

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance-owner decision, integration, and release are
separate decisions by the roles that own them. Approval of `REQ-ECP-006`,
`REQ-ECP-007`, `SPEC-ECP-003`, `ARCH-ECP-001`, `ADR-ECP-002`, and
`VER-ECP-003` are separate acts by their owners and precede approval of
this work order. This work order follows `WO-ECP-001` (it needs
`check --from-git`) and `WO-ECP-002` (it needs the generated body), and
precedes `WO-ECP-006`.

## Objective

Turn scope from honour-based into enforced at the one boundary an agent
cannot bypass. Today the template CI checks scope only when a
`Harness-Restitution:` line is volunteered and exits 0 otherwise
(`templates/repository/standard/.github/workflows/engineering-harness.yml:56-68`),
and the `result_sha256` preimage renders restitution fields only, so
identical digests cover different change sets
(`se_harness/workflow_result.py:174-207`; the 2026-08 agentic execution
review, section 5, weakness 2).

## In scope

- The managed workflow's pull-request job evaluating
  `check --artifact WO --checkpoint handoff --from-git <base>` on every
  pull-request event and failing the required check on `QGP-G4I-PATHS`,
  per `ECP-GTE-*`; the digest comparison retained when a restitution line
  is present.
- The canonical block in `se_harness/workflow_result.py` extended with the
  sorted changed-path set, the completeness assertion, and every predicate
  status, per `ECP-DIG-*`; `se_harness/github_ci.py` and the template
  selector script consuming the new block.
- Tests, including the YAML assertions and the digest-sensitivity cases;
  two throwaway pull requests for the demonstration; work-order-keyed
  evidence.

## Out of scope

- The root managed copy `scripts/select_harness_work_order.py` and the
  root `.github/workflows/` (the template copy is edited and the root
  follows on the next managed upgrade); the delegation class
  (`WO-ECP-006`); marking the check required in repository settings
  (an owner act outside the tree); any change to lifecycle states, gate
  predicates, decision rights; any lifecycle transition of any artifact.

## Authorized decision envelope

The implementation agent may decide step names, the fetch depth strategy,
the canonical field order inside the block, and test names. It may not add
a workflow `if:` that skips scope evaluation, read the change set from the
body, use secrets, or write outside the listed paths.

## Constraints

- Use the exact released evaluator, se-harness 0.7.1, installed outside the
  checkout, for identity, integrity, graph, focus, and preflight readings;
  the workflow installs the same released version outside the checkout.
- Root managed copies are not edited.
- LF line endings; assert bytes against blobs.
- Stage every deletion before any preflight or check run.
- Delete the throwaway demonstration branches afterwards and record it.

## Expected change surface

One managed workflow file, the result renderer, the CI parser, the template
selector script, tests, evidence.

## Required verification

Execute `VER-ECP-003` completely, including both demonstration pull
requests, plus the repository-required checks; run the complete suite on
Linux and Windows with figures labelled per platform.

## Evidence to record

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-003/`:
the pull-request URLs and run identifiers, check logs, the two canonical
blocks and digests from Scenario 3, per-platform test figures, and the
complete changed-path set.

## Stop and escalate conditions

Stop if the required check cannot evaluate scope without a trailer because
work-order selection itself needs one (escalate to `DR-WO-SELECT` for the
selection source), if the widened block breaks the digest equality across
platforms, or if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-ECP-003 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and
its `result_sha256`.
