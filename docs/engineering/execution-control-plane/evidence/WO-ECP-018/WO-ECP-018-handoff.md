```toml
artifact = "WO-ECP-018"
checkpoint = "handoff"
formal_snapshot_sha256 = "790ced083ac4fad200aada4e9c67d01e45d8a9732a473e3f61078e08c507c732"
rebound_at = "2026-08-29T18:12:09Z"
```

# WO-ECP-018 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

A work order that carries `[delegation] class = "execution"` at the base of
its pull request lets the `delegated-executor` role apply exactly
`DR-WO-START` and `DR-WO-COMPLETE` (through `transition`) and
`DR-VREC-PREPARE` (through `capture-verification`), only while the required
check for the candidate head reads `success` from the configured gate
source; the lifecycle event names the check-run id and the head sha; every
other right for the role is refused; no class, no delegation, whatever the
environment says; and `check`/`next` tell the actor when the decision due
is its own (`REQ-ECP-011`; `ECP-DLG-001` to `ECP-DLG-007`, `ECP-DLG-009`,
`ECP-DLG-010`).

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included.
- Candidate: this checkout, branch `wo/ecp-018-delegation-class` off `main`
  at `d3b5a3f`; the suite and the demonstration run candidate source.

## Change

- `se_harness/gate_source.py` (new): `load_configuration` (the owner file
  `.engineering-harness.delegation.toml`), `class_at_base` (`git merge-base
  HEAD <base_ref>` and the base's copy of the work order), `read_gate`
  (`github-checks`: `GET /repos/{repository}/commits/{sha}/check-runs`
  filtered by `check_name`, `GITHUB_TOKEN` when present, standard library
  only; `local-file`: `{"sha", "conclusion", "check_run_id"}`, `W-ECP-005`
  outside a rehearsal), `authorize_delegated_right` (right, class, base,
  gate, in that order; `WEX-ECP-022` / `WEX-ECP-040`), `delegated_reason`
  (`ECP-DLG-005`), `delegation_overlay` (`ECP-DLG-010`).
- `se_harness/workflow.py`: `plan_transition` routes
  `--decision WO=delegated-executor` through `authorize_delegated_right`
  for the (family, status, target) pairs of the two transitions, calls the
  mutation guard with the delegated operation on apply, and writes the
  delegated reason.
- `se_harness/provenance.py`: `capture-verification --owner
  delegated-executor` is the delegated `DR-VREC-PREPARE` for exactly one
  work order; the record's `prepared_by` names the role and its body
  carries the gate evidence.
- `se_harness/workflow_compliance.py`: the overlay applied to the
  projection and to a passed checkpoint restitution of a work order.
- `se_harness/mutation_guard.py`: the three delegated operation names.
- `se_harness/workflow_contract.py`, `workflow_contract.json` and the
  template `WORKFLOW.json`: the catalog is the three delegated bindings;
  the inert `change-bundle-apply` row is gone (`WO-ECP-006` deviation 2
  closed). The JSON key keeps its schema-v4 name (deviation 1).
- Templates: `WORKFLOW.md` "Delegated operations" restated for the class;
  `DECISION_RIGHTS.md` `DR-015` restated; `WORK_ORDER.template.md` carries
  the optional table and one paragraph; the validator gains
  `validate_work_order_delegation` (`E-ECP-001`).
- Tests: `tests/test_delegation_class.py` (15 tests, every row of
  `VER-ECP-015`); the contract, guard, template-exception and
  root-versus-candidate ledger tests updated (the validator's two inserted
  blocks, 23 lines, declared).
- Notes: `docs/notes/delegation-class.md` (indexed); the reference and the
  check note; the `agentic-execution` README.

## Tests

`tests/test_delegation_class.py`, all against a fixture repository with a
real Git history, the class committed on `main` and a branch checked out:

- scenario 1: green gate unlocks start; the event names the role, the
  class, check-run `4242` and the head sha;
- scenario 2: `failure`, `neutral`, `cancelled`, `pending`, a missing check
  and a head not found each refuse with `WEX-ECP-040` naming the head and
  the conclusion, and write nothing;
- scenario 3: `GATES_PASSED`, `GITHUB_ACTIONS` and a token in the
  environment change nothing while the source says `failure`;
- scenario 4 and `ECP-DLG-007`: `DR-WO-APPROVE` and `DR-VREC-DECIDE` with a
  green gate are `WEX-ECP-022`, no write;
- `ECP-DLG-006`: no class, a CI-like environment, `WEX-ECP-022`;
- the class added on the branch only: `WEX-ECP-022` naming the base;
- `ECP-DLG-009`: a delegated completion is refused by the implementation
  gate before any gate read;
- the human route on a class-bearing work order is unchanged;
- `ECP-DLG-010`: `check` names `delegated-executor` with the delegated
  command at `success`, a response naming check, head and conclusion at
  `pending` and `failure`, and the human route without the class or with it
  only on the branch;
- delegated `DR-VREC-PREPARE`: refused at `failure`, prepared at `success`
  with the role and the gate evidence in the record;
- `ECP-DLG-001`: a second key, another value, or the table on a
  requirement is `E-ECP-001`;
- `ECP-DLG-004`: the `github-checks` source against a stub server, request
  path and `check_name` filter pinned, bearer header only with a token,
  `failure` read as not passing; `local-file` outside a rehearsal prints
  `W-ECP-005`.

## Suite readings

- Windows 11 workstation (CPython 3.14, CRLF checkout, `8a63762`): 1,143
  tests, 26 skipped, one failing name, present on `main` and outside this
  work order (`test_artifact_authoring...test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`).
- Linux: the pull request's suite lane, read on the pull request.

## Demonstration on a fixture repository

Candidate CLI over the test fixture (class at the base, branch checked out,
`local-file` gate):

- gate `pending`: `check` returns `decision_required.role =
  delegated-executor`, `delegation.gate = "not passing"`, and the response
  `Wait for or repair the required check before the delegated DR-WO-START:
  required check 'validate' at head 82a49f0 is pending, not success`;
- gate `success`: `decision_required.role = delegated-executor`,
  `delegation = {gate: success, check_run_id: 4242, head: 82a49f0...}`, and
  the command `harnessctl transition . --set WO-PRD-001=in_progress
  --decision WO-PRD-001=delegated-executor --apply`;
- the delegated start with the gate at `failure`: exit 1,
  `WEX-ECP-040: required check 'validate' at head 82a49f0 is failure, not
  success`; with the gate at `success`: exit 0, `in_progress`, the event's
  reason `Delegated DR-WO-START under [delegation] class 'execution':
  required check 'validate' success at 82a49f0... (check-run 4242, source
  local-file)`.

The hosted demonstration with the real required check (`VER-ECP-015`,
last row) waits for the release carrying this change and its adoption as
root; this repository's own work orders cannot carry the class before then.

## Readings under the 0.11.0 root

- `validate .`: 1155 artifacts, 0 errors, 484 warnings.
- `doctor .`: 0 FAIL.
- `validate_release_distributions.py`: PASS (8 records).
- Start preflight for `WO-ECP-018`: PASS over `3bae69d`.

## Deviations, recorded for the completion decision

1. **The contract's JSON key keeps its name.** The work order said the
   `agentic_operations` catalog "becomes `delegated_operations`"; renaming
   the key inside schema v4 would change the loader's schema contract for
   every consumer for a cosmetic gain, so the key stays and the catalog is
   reduced to the three delegated rows; the loader's constant is
   `DELEGATED_OPERATIONS`.
2. **The gate configuration is not in the toml template.** The work order
   put `[delegation]` in `.engineering-harness.toml.tpl`; the rehearsal
   showed that a consumer editing the managed toml reads as customization
   under `QGP-G3-PREFLIGHT`, so the configuration is owner content in
   `.engineering-harness.delegation.toml`, beside the managed file, and the
   toml template is untouched. The scope path is unused.
3. **`resolve_delegation` is not restored as a function.** `ECP-DLG-009`'s
   narrowing is the existing `QGP-G4I-PATHS` predicate of the handoff gate
   the delegated completion runs; the test asserts the gate refuses before
   the CI source is consulted.
4. **`SPEC-ECP-004` is not amended.** It names no Phase 4 delegation, so the
   conditional amendment the work order listed was not needed; the scope
   path is unused.

## Complete changed-path set

Every path this work order changed since `main` at `d3b5a3f`, packet
included, as Git derived it; the handoff check completed at its fixed point
with every predicate of `QG-G4-IMPLEMENTATION-EVIDENCE` passing, run by
the released 0.11.0 evaluator on this Windows checkout: see `handoff.json`
beside this file.
