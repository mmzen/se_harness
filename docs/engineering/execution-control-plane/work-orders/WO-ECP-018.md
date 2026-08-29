+++
id = "WO-ECP-018"
type = "work_order"
title = "Introduce the delegation class: three transitions unlocked by the green pull-request gate"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "The change lets a non-human actor apply three lifecycle transitions; the reader that decides, the contract rows that bind it and the policy that names it are trusted engineering state every later delegated decision relies on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/gate_source.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/provenance.py",
  "se_harness/mutation_guard.py",
  "se_harness/cli.py",
  "se_harness/workflow_contract.py",
  "se_harness/workflow_contract.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/docs/engineering/DECISION_RIGHTS.md",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "templates/repository/standard/scripts/validate_engineering_artifacts.py",
  "templates/repository/standard/.engineering-harness.toml.tpl",
  "tests/",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harnessctl-check.md",
  "docs/notes/delegation-class.md",
  "docs/notes/README.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification/VER-ECP-015.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-004.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-006.md",
  "docs/engineering/agentic-execution/README.md",
]

[relations]
implements = ["REQ-ECP-011"]
specifications = ["SPEC-ECP-006"]
architecture = ["ARCH-ECP-001", "ADR-ECP-002"]
verification = ["VER-ECP-015"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T17:42:15Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29 with the words 'Approve and start WO-ECP-018', as a decision distinct from the approval of VER-ECP-015 in the same transaction, after the owner's question on how an actor learns it holds a delegated right was answered by the ECP-DLG-010 amendment record on SPEC-ECP-006. Authorizes start preflight and then only the declared scope: the gate-source reader, the delegated routes of transition and capture-verification, the restitution that names a delegated decision, the mutation guard's three delegated operations, the contract's three delegated bindings replacing the Phase 4 catalog, the toml, work-order and decision-rights templates, the template validator, tests, notes and indexes, and the evidence packet. It authorizes no hash-locked root file, no branch-protection rule, no use of the class by this repository before a release carrying it governs the root, no verification record, no release and no publication. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-29T17:42:22Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-29, 'Approve and start WO-ECP-018'. Start preflight PASS with no diagnostics over the approval commit 3bae69d carrying unmoved main d3b5a3f, run with the governing exact public 0.11.0 evaluator outside the checkout, on this Windows checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."
+++

# Work Order: Introduce the delegation class: three transitions unlocked by the green pull-request gate

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

It is the second of the three steps `WO-ECP-006` (revised 2026-08-29)
divided `SPEC-ECP-006` into: the removal is on `main`, this work order is
the delegation class (`REQ-ECP-011`, `ECP-DLG-001` to `ECP-DLG-007`,
`ECP-DLG-009`), and the shared journaled write path (`REQ-ECP-017`)
follows. `SPEC-ECP-006` receives one amendment record, `ECP-DLG-010`, so
that the restitution tells the actor when a decision is delegated to it;
no approved rule changes.

## Objective

Let a work order declare `[delegation] class = "execution"` and, while the
required pull-request check for the candidate head is `success`, let the
`delegated-executor` role apply exactly `DR-WO-START`, `DR-WO-COMPLETE`
and `DR-VREC-PREPARE` — the three mechanical decisions of every cycle —
with the gate read from the CI provider by commit id, the class read at
the pull request's base, and every other decision right refused for that
role. Audit follow-up of 2026-08-29; the roadmap's Phase 4 objective
achieved at the Git boundary (`ADR-ECP-002`).

## Why now

Today's eleven cycles show where the human time goes: start, implemented
and record-prepared are typed by the owner after reading a `check` result
and a green lane, which is exactly the reading the evaluator can take
itself. The definitions have been approved since 08-26 and the removal
that cleared the way is on `main`.

## In scope

- `se_harness/gate_source.py` (new): `read_gate(root, sha)` returning the
  check-run id and conclusion for the candidate head from the configured
  source — `github-checks` (`GET /repos/{repository}/commits/{sha}/check-runs`
  filtered by `check_name`, `GITHUB_TOKEN` from the environment, standard
  library only) or `local-file` (`{"sha": ..., "conclusion": ...,
  "check_run_id": ...}`); any conclusion other than `success`, a missing
  check, a head not found or a source error is `WEX-ECP-040` naming the
  head and the conclusion observed (`ECP-DLG-003`, `ECP-DLG-004`).
- `templates/repository/standard/.engineering-harness.toml.tpl`: an
  optional `[delegation]` table — `gate_source`, `check_name`,
  `repository`, `base_ref` (default the default branch on `origin`),
  `local_file` — read by the evaluator; `local-file` outside a rehearsal
  is `W-ECP-005`.
- `se_harness/workflow.py`: `transition --apply` accepts
  `--decision WO=delegated-executor` for `DR-WO-START` and `DR-WO-COMPLETE`
  when the work order carries the class *at the pull request's base*
  (`git merge-base HEAD <base_ref>`), consults the gate for the candidate
  head before writing, and writes the lifecycle event whose `reason` names
  the class, the check-run id and the head sha (`ECP-DLG-002`,
  `ECP-DLG-005`); the role on any other right is `WEX-ECP-022`; a work
  order without the class refuses the role on every right (`ECP-DLG-006`,
  `ECP-DLG-007`). The delegated `DR-WO-COMPLETE` runs the same handoff
  gate as the human one, so `QGP-G4I-PATHS` narrows the change set to
  `[execution_scope].paths` before the CI gate is consulted (`ECP-DLG-009`
  by the existing predicate, no new module).
- `check` and `next` (`workflow.py`, `workflow_compliance.py`): the
  restitution is how the actor knows it holds the right (`ECP-DLG-010`,
  by amendment record on `SPEC-ECP-006`). For a work order carrying the
  class at the base, when the decision due is one of the three rights and
  the configured gate reads `success` for the current head,
  `decision_required` is `delegated-executor` and `command_or_response` is
  the delegated command; when the gate is not `success`, it is a
  suggested-response naming the check, the head and the conclusion
  observed, so the actor waits or repairs rather than escalating; for every
  other right the restitution is unchanged and names the human role.
  Delegation is never shown for a class that is not at the base.
- `se_harness/provenance.py`: `capture-verification --owner
  delegated-executor` is the delegated `DR-VREC-PREPARE`, under the same
  class and gate checks; the record's `prepared_by` names the role and the
  reason line names the gate evidence.
- `se_harness/mutation_guard.py`: the three delegated operation names
  return to `PUBLIC_MUTATION_OPERATIONS`, bound to the delegated routes.
- `se_harness/workflow_contract.json`, `workflow_contract.py` and the
  template `WORKFLOW.json`/`.md`: the `agentic_operations` catalog becomes
  `delegated_operations` with exactly the three rows (`delegated-work-order-start`,
  `delegated-work-order-complete`, `delegated-vrec-prepare`); the inert
  `change-bundle-apply` row leaves (`WO-ECP-006` deviation 2); `WFL-*`
  text names the class where it names delegation.
- `templates/repository/standard/docs/engineering/DECISION_RIGHTS.md`:
  `DR-015` restated for the class — the `delegated-executor` role, the
  three rights, the green required check at the candidate head, the class
  read at the base, never verification, release, delivery, Git,
  credentials or external authority. `SPEC-ECP-004` receives an amendment
  record if its rules name Phase 4 delegation.
- `templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md`:
  the optional `[delegation] class = "execution"` table and one paragraph.
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`:
  `E-ECP-001` for any other key, value or artifact type (`ECP-DLG-001`);
  the root copy stays at 0.11.0 and the divergence is declared in
  `tests/test_predecessor_bootstrap_retirement.py` in the existing form.
- Tests: `tests/test_delegation_class.py` for every row of `VER-ECP-015`,
  including the `github-checks` stub server; contract and template tests
  updated; the root-versus-template declarations extended.
- Notes: `docs/notes/delegation-class.md` (what the class is, how a work
  order declares it, how the actor invokes it, what it can never do),
  indexed in `docs/notes/README.md`; the reference and the check note.
- The packet; this domain's index; the `agentic-execution` README's plan
  section, which promised the class.

## Out of scope

The branch-protection rule on `main` naming the managed check (an owner
act in GitHub, recorded in the note as the step that makes the class
prevention rather than reporting); the shared journaled write path
(`REQ-ECP-017`); any use of the class by this repository before the release
carrying it governs the root; any identity check on human decision actors;
any hash-locked root file; the release carrying this change.

## Authorized decision envelope

The reader module's shape; the exact TOML keys of `[delegation]` provided
the four facts above are expressible; the diagnostic texts under the coded
identifiers the specification fixes; the stub server's form; the wording of
the policy restatement and the note; test names.

## Constraints

- The gate is read from the configured source by commit id, never from a
  request body, an environment variable, a token or an actor name.
- The class is read from the base of the pull request, never from the
  branch's own copy.
- `check`'s stdout and `--json` bytes for non-delegated work are unchanged;
  the human routes are unchanged.
- No new dependency; no hash-locked root file moves.

## Expected change surface

One new module, four product modules, the contract loader and JSON, four
managed templates and the toml template, one new test module and several
updated ones, one new note and three touched, two indexes, one amendment
record, the packet.

## Required verification

Execute `VER-ECP-015` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-018/`.

## Stop and escalate conditions

A gate that can be satisfied from anything but the configured source; a
class that can be widened from the branch; a need to touch a hash-locked
root file or add a dependency; a contract change the released evaluator
refuses to load; any test that can only pass by weakening the human
routes.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
