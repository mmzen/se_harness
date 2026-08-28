+++
id = "WO-ECP-003"
type = "work_order"
title = "Make the pull-request gate mandatory and scope-aware, and widen the digest"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-27"
updated = "2026-08-28"

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
  "templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed",
  "docs/engineering/execution-control-plane/verification/VER-ECP-003.md",
]

[relations]
implements = ["REQ-ECP-006", "REQ-ECP-007"]
specifications = ["SPEC-ECP-003"]
architecture = ["ARCH-ECP-001", "ADR-ECP-002"]
verification = ["VER-ECP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T21:40:17Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-28 with the words 'Approve and start with the amendments', as the third work order of the execution-control-plane plan, after WO-ECP-001 and WO-ECP-002 merged (main e75fac8). Its definitions REQ-ECP-006, REQ-ECP-007, SPEC-ECP-003, ARCH-ECP-001, ADR-ECP-002 and VER-ECP-003 were approved separately on 2026-08-28; three pre-start amendments are recorded on the work order and VER-ECP-003: the demonstration runs locally with the hosted form deferred to the first release carrying WO-ECP-001 to -003, the pull-request template seed joins the scope, and the released-0.7.1 golden digest is re-pinned to the widened block with a dated note. Authorizes start preflight and then only the declared scope. Measured before this transition: validate PASS at 0 errors under the governing 0.8.0 root. It authorizes no verification record, no release and no publication."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-28T21:40:21Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-28, 'Approve and start with the amendments'. Start preflight Completed with nothing not done over the approval commit 0f31f1d carrying unmoved main e75fac8, run with the governing exact public 0.8.0 evaluator outside the checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."
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

## Pre-start amendments, 2026-08-28

Put to the engineering owner before approval, on a reading of the packet
against `main` at `e75fac8`, and answered "Approve and start with the
amendments":

1. **Demonstration.** The two throwaway pull requests of `VER-ECP-003`
   cannot run here: this repository's pull requests run the root managed
   workflow, released 0.8.0's, which installs `se-harness==0.8.0` in CI and
   has no `--from-git`; the template edited here reaches consumers, and this
   repository, through the next release and root adoption. `VER-ECP-003` is
   amended by date: the demonstration runs the template step's shell
   locally against two throwaway branches with the candidate evaluator
   installed outside the checkout, and the hosted demonstration becomes a
   verification condition of the first release that carries `WO-ECP-001` to
   `WO-ECP-003`, to be recorded on that release's contract.
2. **Seed.** `ECP-GTE-007` edits
   `templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed`;
   it is added to the scope, with `VER-ECP-003` for its amendment.
3. **Golden digest.** `ECP-DIG-001` widens the canonical block, so every
   `result_sha256` changes, including the released-0.7.1 `focus` digest that
   `test_focus_digest_equals_the_released_evaluator_golden` pins for issue
   #212 criterion 3. The pin is moved to the widened block with a dated
   note: the criterion holds within one block definition and this work
   order changes the definition knowingly, as `SPEC-ECP-003`'s
   compatibility section states.

Two deviations are accepted in advance: readings under the governing exact
public 0.8.0 root, not the 0.7.1 named on 2026-08-27; the root managed
workflow and selector stay unedited, so this repository's own gate remains
the 0.8.0 one until its next root adoption.

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
